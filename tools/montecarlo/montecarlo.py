#!/usr/bin/env python3
"""Monte Carlo flow forecasting for work items.

Modes:
  single  -- cycle/lead time percentiles for one work item (Service Level Expectation)
  epic    -- "when will N items be done" (and optionally "how many by a deadline")
  epics   -- ordered groups done one after the other; one continuous simulation per trial

Reads normalized history only (CSV or JSON). No network calls, no tokens, no secrets.
Standard library only; Python >= 3.11.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import sys
from bisect import bisect_right
from collections import Counter
from dataclasses import dataclass, field
from datetime import date, datetime, time, timedelta, timezone

DEFAULTS = {
    "window_weeks": 12,
    "granularity": "day",
    "trials": 10000,
    "seed": None,
    "percentiles": "50,70,85,95",
    "calendar": "workdays",
    "holidays": None,
    "sampling": "uniform",
    "type": None,
    "tag": None,
    "as_of": None,
    "start": None,
    "out_dir": "montecarlo-out",
    "format": "both",
    "metric": "cycle",
    "elapsed_days": None,
    "remaining": None,
    "remaining_ids": None,
    "deadline": None,
    "split_rate": None,
    "groups": None,
    "group": None,
    "demo": False,
}
PATH_KEYS = ("history", "holidays", "groups", "out_dir")

EXAMPLES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")
MIN_SAMPLE_ITEMS = 20
MIN_HISTORY_WEEKS = 8
MIN_CONDITIONAL_ITEMS = 5
MAX_PERIODS = 3650
REQUIRED_COLUMNS = ("id", "completed_at")
WEEKDAY_NAMES = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
IT_WEEKDAYS = ("lun", "mar", "mer", "gio", "ven", "sab", "dom")
IT_MONTHS = ("gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic")

REJECT_REASONS_IT = {
    "missing_id": "id mancante",
    "duplicate_id": "id duplicato",
    "missing_completed_at": "completed_at mancante",
    "invalid_completed_at": "completed_at non è una data ISO 8601 valida",
    "invalid_started_at": "started_at non è una data ISO 8601 valida",
    "invalid_ready_at": "ready_at non è una data ISO 8601 valida",
    "started_after_completed": "started_at successivo a completed_at",
    "ready_after_completed": "ready_at successivo a completed_at",
}


class InputError(Exception):
    """Invalid or insufficient input; reported to the user without a traceback."""


# --------------------------------------------------------------------------- calendar


class Calendar:
    def __init__(self, workdays: set[int], holidays: set[date] | None = None, spec: str = ""):
        if not workdays:
            raise InputError("Il calendario non ha giorni lavorativi.")
        self.workdays = workdays
        self.holidays = holidays or set()
        self.spec = spec

    @classmethod
    def from_spec(cls, spec: str, holidays: set[date] | None = None) -> "Calendar":
        spec = (spec or "workdays").strip().lower()
        if spec == "workdays":
            days = {0, 1, 2, 3, 4}
        elif spec == "all":
            days = set(range(7))
        else:
            names = [n.strip()[:3] for n in spec.split(",") if n.strip()]
            unknown = [n for n in names if n not in WEEKDAY_NAMES]
            if unknown:
                raise InputError(
                    f"--calendar non valido: {spec!r}. Usa 'workdays', 'all' o giorni tipo 'mon,tue,wed'."
                )
            days = {WEEKDAY_NAMES.index(n) for n in names}
        return cls(days, holidays, spec)

    def is_working(self, day: date) -> bool:
        return day.weekday() in self.workdays and day not in self.holidays

    def working_days_between(self, start: datetime, end: datetime) -> float:
        """Elapsed time in days, counting only the working days of this calendar."""
        if end <= start:
            return 0.0
        total = 0.0
        day = start.date()
        while day <= end.date():
            if self.is_working(day):
                day_start = datetime.combine(day, time.min)
                lo = max(start, day_start)
                hi = min(end, day_start + timedelta(days=1))
                if hi > lo:
                    total += (hi - lo).total_seconds() / 86400
            day += timedelta(days=1)
        return total

    def working_days(self, start: date, end_exclusive: date) -> list[date]:
        days, day = [], start
        while day < end_exclusive:
            if self.is_working(day):
                days.append(day)
            day += timedelta(days=1)
        return days

    def nth_working_day(self, start: date, n: int) -> date:
        """The n-th working day on or after start (n >= 1). n == 0 returns start."""
        if n <= 0:
            return start
        day, seen = start, 0
        for _ in range(n * 7 + 3660):
            if self.is_working(day):
                seen += 1
                if seen == n:
                    return day
            day += timedelta(days=1)
        raise InputError("Calendario senza giorni lavorativi nell'orizzonte di previsione.")

    def working_days_inclusive(self, start: date, end: date) -> int:
        return len(self.working_days(start, end + timedelta(days=1)))


# --------------------------------------------------------------------------- parsing


def parse_datetime(text) -> datetime | None:
    if text is None:
        return None
    text = str(text).strip()
    if not text:
        return None
    if text[-1] in "Zz":
        text = text[:-1] + "+00:00"
    value = datetime.fromisoformat(text)
    if value.tzinfo is not None:
        value = value.astimezone(timezone.utc).replace(tzinfo=None)
    return value


def parse_date(text, name: str) -> date:
    try:
        return parse_datetime(text).date()
    except (ValueError, AttributeError):
        raise InputError(f"{name} non è una data ISO 8601 valida: {text!r}")


def parse_tags(value) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (list, tuple)):
        parts = value
    else:
        parts = str(value).split(";")
    return tuple(p.strip() for p in parts if str(p).strip())


def parse_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    return [v.strip() for v in str(value).split(",") if v.strip()]


def parse_split_rate(value) -> tuple[float, float] | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    try:
        if "-" in text:
            lo, hi = (float(p) for p in text.split("-", 1))
        else:
            lo = hi = float(text)
    except ValueError:
        raise InputError(f"--split-rate non valido: {value!r}. Usa un moltiplicatore (1.2) o un intervallo (1.0-1.3).")
    if lo < 1 or hi < lo:
        raise InputError(f"--split-rate non valido: {value!r}. Serve 1 <= min <= max.")
    return (lo, hi)


def parse_percentiles(value) -> list[float]:
    try:
        result = sorted({float(p) for p in parse_list(value)})
    except ValueError:
        raise InputError(f"--percentiles non valido: {value!r}")
    if not result or any(p <= 0 or p >= 100 for p in result):
        raise InputError("--percentiles: ogni valore deve essere tra 0 e 100 (esclusi).")
    return result


def load_holidays(value) -> set[date]:
    if not value:
        return set()
    if isinstance(value, (list, tuple)):
        entries = value
    elif os.path.isfile(str(value)):
        with open(value, encoding="utf-8") as handle:
            raw = handle.read()
        if raw.lstrip().startswith("["):
            entries = json.loads(raw)
        else:
            entries = [line.split("#", 1)[0].strip() for line in raw.splitlines()]
    else:
        entries = str(value).split(",")
    return {parse_date(e, "festività") for e in entries if str(e).strip()}


# --------------------------------------------------------------------------- history


@dataclass
class WorkItem:
    row: int
    id: str
    type: str
    tags: tuple[str, ...]
    ready_at: datetime | None
    started_at: datetime | None
    completed_at: datetime
    lead_time: float | None = None
    cycle_time: float | None = None
    lead_fallback: bool = False
    flags: list[str] = field(default_factory=list)


@dataclass
class Rejection:
    row: int
    id: str
    reason: str


def read_history_rows(path: str) -> list[dict]:
    if not path:
        raise InputError("Manca --history: serve lo storico dei work item completati (CSV o JSON).")
    if not os.path.isfile(path):
        raise InputError(f"File storico non trovato: {path}")
    with open(path, encoding="utf-8-sig") as handle:
        content = handle.read()
    if not content.strip():
        raise InputError(f"File storico vuoto: {path}")
    if path.lower().endswith(".json") or content.lstrip()[:1] in "[{":
        return _rows_from_json(content, path)
    return _rows_from_csv(content, path)


def _normalize_keys(record: dict) -> dict:
    return {str(k).strip().lower(): v for k, v in record.items() if k is not None}


def _rows_from_csv(content: str, path: str) -> list[dict]:
    reader = csv.DictReader(content.splitlines())
    header = [h.strip().lower() for h in (reader.fieldnames or [])]
    missing = [c for c in REQUIRED_COLUMNS if c not in header]
    if missing:
        raise InputError(
            f"Colonne obbligatorie mancanti in {path}: {', '.join(missing)}. "
            f"Intestazione trovata: {', '.join(header) or '(vuota)'}"
        )
    return [_normalize_keys(r) for r in reader]


def _rows_from_json(content: str, path: str) -> list[dict]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise InputError(f"JSON non valido in {path}: {exc}")
    if isinstance(data, dict):
        data = data.get("items")
    if not isinstance(data, list):
        raise InputError(f"{path}: atteso un array di record oppure un oggetto con chiave 'items'.")
    rows = [_normalize_keys(r) if isinstance(r, dict) else {} for r in data]
    for column in REQUIRED_COLUMNS:
        if rows and not any(column in r for r in rows):
            raise InputError(f"Colonna obbligatoria mancante in {path}: {column}")
    return rows


def build_items(rows: list[dict], calendar: Calendar) -> tuple[list[WorkItem], list[Rejection]]:
    items: list[WorkItem] = []
    rejected: list[Rejection] = []
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        item_id = str(row.get("id") or "").strip()
        result = _build_item(index, item_id, row, calendar, seen)
        if isinstance(result, Rejection):
            rejected.append(result)
        else:
            seen.add(item_id)
            items.append(result)
    return items, rejected


def _parse_field(row: dict, name: str) -> tuple[datetime | None, bool]:
    try:
        return parse_datetime(row.get(name)), True
    except (ValueError, TypeError):
        return None, False


def _build_item(index: int, item_id: str, row: dict, calendar: Calendar, seen: set[str]):
    def reject(reason: str) -> Rejection:
        return Rejection(index, item_id, reason)

    if not item_id:
        return reject("missing_id")
    if item_id in seen:
        return reject("duplicate_id")
    if not str(row.get("completed_at") or "").strip():
        return reject("missing_completed_at")
    completed, ok = _parse_field(row, "completed_at")
    if not ok:
        return reject("invalid_completed_at")
    started, ok = _parse_field(row, "started_at")
    if not ok:
        return reject("invalid_started_at")
    ready, ok = _parse_field(row, "ready_at")
    if not ok:
        return reject("invalid_ready_at")
    if started and started > completed:
        return reject("started_after_completed")
    if ready and ready > completed:
        return reject("ready_after_completed")

    item = WorkItem(
        row=index,
        id=item_id,
        type=str(row.get("type") or "").strip(),
        tags=parse_tags(row.get("tags")),
        ready_at=ready,
        started_at=started,
        completed_at=completed,
    )
    _compute_times(item, calendar)
    return item


def _compute_times(item: WorkItem, calendar: Calendar) -> None:
    if item.started_at:
        item.cycle_time = calendar.working_days_between(item.started_at, item.completed_at)
    else:
        item.flags.append("no_started_at")
    lead_start = item.ready_at
    if item.ready_at and item.started_at and item.ready_at > item.started_at:
        item.flags.append("ready_after_started")
        lead_start = None
    if lead_start is None:
        item.lead_fallback = True
        lead_start = item.started_at
    if lead_start:
        item.lead_time = calendar.working_days_between(lead_start, item.completed_at)


# --------------------------------------------------------------------------- sample


@dataclass
class Sample:
    items: list[WorkItem]
    filtered_out: dict[str, int]
    filter_reason: dict[str, str]
    window_start: date
    window_end: date
    weeks_effective: float


def select_sample(items: list[WorkItem], as_of: date, window_weeks: int, types: list[str], tags: list[str]) -> Sample:
    if not items:
        raise InputError("Nessun record valido nello storico.")
    coverage_start = min(i.completed_at.date() for i in items)
    if window_weeks and window_weeks > 0:
        window_start = max(as_of - timedelta(weeks=window_weeks), coverage_start)
    else:
        window_start = coverage_start
    wanted_types = {t.lower() for t in types}
    wanted_tags = {t.lower() for t in tags}
    chosen, reasons = [], {}
    for item in items:
        reason = _filter_reason(item, as_of, window_start, wanted_types, wanted_tags)
        if reason:
            reasons[item.id] = reason
        else:
            chosen.append(item)
    return Sample(
        items=chosen,
        filtered_out=dict(Counter(reasons.values())),
        filter_reason=reasons,
        window_start=window_start,
        window_end=as_of,
        weeks_effective=round((as_of - window_start).days / 7, 1),
    )


def _filter_reason(item: WorkItem, as_of: date, window_start: date, types: set[str], tags: set[str]) -> str | None:
    done = item.completed_at.date()
    if done >= as_of:
        return "completed_on_or_after_as_of"
    if done < window_start:
        return "outside_window"
    if types and item.type.lower() not in types:
        return "type"
    if tags and not tags.intersection(t.lower() for t in item.tags):
        return "tag"
    return None


# --------------------------------------------------------------------------- throughput


@dataclass
class Throughput:
    granularity: str
    periods: list[tuple[date, int]]  # (period start, completed count)

    @property
    def values(self) -> list[int]:
        return [count for _, count in self.periods]


def compute_throughput(sample: Sample, calendar: Calendar, granularity: str) -> Throughput:
    if granularity == "week":
        return _weekly_throughput(sample)
    days = calendar.working_days(sample.window_start, sample.window_end)
    if not days:
        raise InputError("Storico insufficiente: nessun giorno lavorativo nella finestra scelta.")
    counts = [0] * len(days)
    for item in sample.items:
        index = max(0, bisect_right(days, item.completed_at.date()) - 1)
        counts[index] += 1
    return Throughput("day", list(zip(days, counts)))


def _weekly_throughput(sample: Sample) -> Throughput:
    weeks = (sample.window_end - sample.window_start).days // 7
    if weeks < 1:
        raise InputError("Storico insufficiente: serve almeno una settimana intera di dati per --granularity week.")
    counts = [0] * weeks
    for item in sample.items:
        back = ((sample.window_end - item.completed_at.date()).days - 1) // 7
        if back < weeks:
            counts[weeks - 1 - back] += 1
    starts = [sample.window_end - timedelta(weeks=weeks - i) for i in range(weeks)]
    return Throughput("week", list(zip(starts, counts)))


def make_draw(throughput: Throughput, sampling: str, period_date):
    values = throughput.values
    if sum(values) == 0:
        raise InputError("Storico insufficiente: nessun item completato nella finestra (throughput sempre zero).")
    if sampling == "weekday" and throughput.granularity == "day":
        pools: dict[int, list[int]] = {}
        for day, count in throughput.periods:
            pools.setdefault(day.weekday(), []).append(count)

        def draw_weekday(rng: random.Random, period: int) -> int:
            pool = pools.get(period_date(period).weekday()) or values
            return pool[rng.randrange(len(pool))]

        return draw_weekday
    size = len(values)

    def draw_uniform(rng: random.Random, period: int) -> int:
        return values[rng.randrange(size)]

    return draw_uniform


# --------------------------------------------------------------------------- simulation


def apply_split(count: int, split: tuple[float, float] | None, rng: random.Random) -> int:
    if not split or count <= 0:
        return count
    lo, hi = split
    factor = lo if lo == hi else rng.uniform(lo, hi)
    return math.ceil(round(count * factor, 9))


def simulate_sequence(remaining, draw, trials: int, rng: random.Random, splits=None, max_periods: int = MAX_PERIODS):
    """One continuous throughput stream per trial; record the period each cumulative target is reached.

    Returns one list per trial with, for each group, the period (1-based) at which the group is done,
    0 if nothing was left, or math.inf if the horizon was exceeded.
    """
    splits = splits or [None] * len(remaining)
    results = []
    for _ in range(trials):
        targets, total = [], 0
        for count, split in zip(remaining, splits):
            total += apply_split(count, split, rng)
            targets.append(total)
        reached = [math.inf] * len(targets)
        done, period, group = 0, 0, 0
        while group < len(targets) and done >= targets[group]:
            reached[group] = 0
            group += 1
        while group < len(targets) and period < max_periods:
            period += 1
            done += draw(rng, period)
            while group < len(targets) and done >= targets[group]:
                reached[group] = period
                group += 1
        results.append(reached)
    return results


def simulate_how_many(periods: int, draw, trials: int, rng: random.Random) -> list[int]:
    return [sum(draw(rng, p) for p in range(1, periods + 1)) for _ in range(trials)]


def percentile_within(sorted_values: list, p: float):
    """Smallest value v such that at least p% of trials are <= v (nearest rank)."""
    index = max(0, math.ceil(round(p / 100 * len(sorted_values), 9)) - 1)
    return sorted_values[index]


def percentile_at_least(sorted_values: list, p: float):
    """Largest value v such that at least p% of trials are >= v."""
    index = min(len(sorted_values) - 1, math.floor(round(len(sorted_values) * (1 - p / 100), 9)))
    return sorted_values[index]


# --------------------------------------------------------------------------- forecasts


@dataclass
class Context:
    mode: str
    options: dict
    calendar: Calendar
    history_path: str
    rows_total: int
    items: list[WorkItem]
    rejected: list[Rejection]
    sample: Sample
    as_of: date
    start: date
    percentiles: list[float]
    rng: random.Random
    seed: int
    warnings: list[str] = field(default_factory=list)
    demo: bool = False
    assumptions: list[str] = field(default_factory=list)

    def period_date(self, period) -> date | None:
        if period == math.inf:
            return None
        if self.options["granularity"] == "week":
            return self.start if period == 0 else self.start + timedelta(days=7 * period - 1)
        return self.calendar.nth_working_day(self.start, period)


def build_context(mode: str, options: dict) -> Context:
    holidays = load_holidays(options.get("holidays"))
    calendar = Calendar.from_spec(options["calendar"], holidays)
    demo = _guard_example_history(options)
    rows = read_history_rows(options.get("history"))
    items, rejected = build_items(rows, calendar)
    as_of = parse_date(options["as_of"], "--as-of") if options.get("as_of") else date.today()
    start = parse_date(options["start"], "--start") if options.get("start") else as_of
    window_weeks = int(options["window_weeks"])
    sample = select_sample(items, as_of, window_weeks, parse_list(options.get("type")), parse_list(options.get("tag")))
    seed = options.get("seed")
    seed = int(seed) if seed not in (None, "") else random.SystemRandom().randrange(2**31)
    if options["granularity"] not in ("day", "week"):
        raise InputError("--granularity deve essere 'day' o 'week'.")
    context = Context(
        mode=mode,
        options=options,
        calendar=calendar,
        history_path=options["history"],
        rows_total=len(rows),
        items=items,
        rejected=rejected,
        sample=sample,
        as_of=as_of,
        start=start,
        percentiles=parse_percentiles(options["percentiles"]),
        rng=random.Random(seed),
        seed=seed,
    )
    context.demo = demo
    if demo:
        context.warnings.append(
            "DEMO su dati di esempio sintetici: non è una previsione per nessun team reale. Affidabilità bassa."
        )
    _common_assumptions(context, window_weeks, holidays)
    return context


def _guard_example_history(options: dict) -> bool:
    history = options.get("history")
    if not history:
        return False
    is_example = os.path.commonpath([os.path.realpath(history), os.path.realpath(EXAMPLES_DIR)]) == os.path.realpath(EXAMPLES_DIR)
    if is_example and not options.get("demo"):
        raise InputError(
            "--history punta ai dati di esempio sintetici: non sono lo storico di nessun team. "
            "Non usarli come sostituto: chiedi all'utente lo storico (incollato in chat o come file locale). "
            "Per una demo esplicitamente richiesta, aggiungi --demo."
        )
    return is_example


def _common_assumptions(ctx: Context, window_weeks: int, holidays: set[date]) -> None:
    s = ctx.sample
    window_text = f"ultime {window_weeks} settimane" if window_weeks else "tutto lo storico"
    ctx.assumptions.append(
        f"Finestra storica: {window_text} prima di {fmt_date(ctx.as_of)} "
        f"(effettiva {fmt_date(s.window_start)} → {fmt_date(s.window_end - timedelta(days=1))}, {s.weeks_effective} settimane)."
    )
    workdays = ", ".join(IT_WEEKDAYS[d] for d in sorted(ctx.calendar.workdays))
    ctx.assumptions.append(
        f"Calendario: giorni lavorativi {workdays}; festività escluse: {len(holidays)}. "
        "Lead e cycle time contano solo il tempo nei giorni lavorativi."
    )
    if ctx.rejected:
        ctx.warnings.append(
            f"{len(ctx.rejected)} record scartati perché malformati (dettaglio nel CSV di controllo)."
        )


def _sample_warnings(ctx: Context, sample_count: int, label: str) -> None:
    if sample_count < MIN_SAMPLE_ITEMS:
        ctx.warnings.append(
            f"Campione piccolo: {sample_count} {label} (servono almeno ~{MIN_SAMPLE_ITEMS}). Affidabilità bassa."
        )
    if ctx.sample.weeks_effective < MIN_HISTORY_WEEKS:
        ctx.warnings.append(
            f"Storico breve: {ctx.sample.weeks_effective} settimane (servono almeno ~{MIN_HISTORY_WEEKS}). Affidabilità bassa."
        )


def _reliability(ctx: Context) -> dict:
    low = any("Affidabilità bassa" in w for w in ctx.warnings)
    return {"level": "low" if low else "ok", "warnings": list(ctx.warnings)}


def forecast_single(ctx: Context) -> dict:
    metric = ctx.options.get("metric") or "cycle"
    if metric not in ("cycle", "lead"):
        raise InputError("--metric deve essere 'cycle' o 'lead'.")
    attr = "cycle_time" if metric == "cycle" else "lead_time"
    values = sorted(getattr(i, attr) for i in ctx.sample.items if getattr(i, attr) is not None)
    if not values:
        raise InputError(
            f"Storico insufficiente: nessun item nel campione ha le date per calcolare il {metric} time "
            "(serve almeno started_at e completed_at)."
        )
    _sample_warnings(ctx, len(values), "item con date di inizio e fine")
    if metric == "lead":
        fallbacks = sum(1 for i in ctx.sample.items if i.lead_fallback and i.lead_time is not None)
        if fallbacks:
            ctx.assumptions.append(f"Lead time: {fallbacks} item senza ready_at usano started_at (ripiego).")
    ctx.assumptions.append("Item singolo: nessuna simulazione sul throughput, percentili della distribuzione storica.")

    elapsed = ctx.options.get("elapsed_days")
    unit = "calendar_days" if len(ctx.calendar.workdays) == 7 and not ctx.calendar.holidays else "working_days"
    result = {"metric": metric, "unit": unit, "sample_size": len(values), "elapsed_days": None}
    population = values
    if elapsed not in (None, ""):
        elapsed = float(elapsed)
        population = [v for v in values if v > elapsed]
        older = sum(1 for v in values if v <= elapsed)
        result.update(
            elapsed_days=elapsed,
            conditional_sample_size=len(population),
            age_percentile=round(100 * older / len(values), 1),
        )
        ctx.assumptions.append(
            f"Item già in corso da {elapsed:g} giorni: percentili condizionati agli item storici durati più di {elapsed:g} giorni."
        )
        if len(population) < MIN_CONDITIONAL_ITEMS:
            ctx.warnings.append(
                f"L'item è già più vecchio di quasi tutto lo storico: solo {len(population)} item sono durati di più. "
                "Affidabilità bassa: una volta superata la previsione non si sa più con confidenza quando finirà."
            )
    result["percentiles"] = []
    for p in ctx.percentiles:
        days = percentile_within(population, p) if population else None
        result["percentiles"].append(_single_point(ctx, p, days, elapsed))
    result["histogram"] = histogram(values)
    result["min_days"] = round(values[0], 2)
    result["max_days"] = round(values[-1], 2)
    return result


def _single_point(ctx: Context, p: float, days, elapsed) -> dict:
    if days is None:
        return {"p": p, "days": None, "date": None}
    left = days - (elapsed or 0)
    target = ctx.calendar.nth_working_day(ctx.start, max(1, math.ceil(round(left, 9))))
    return {"p": p, "days": round(days, 2), "remaining_days": round(left, 2), "date": target.isoformat()}


def forecast_epic(ctx: Context) -> dict:
    remaining = _epic_remaining(ctx.options)
    deadline = ctx.options.get("deadline")
    if remaining is None and not deadline:
        raise InputError("Modalità epic: serve --remaining N (o --remaining-ids) oppure --deadline.")
    throughput = compute_throughput(ctx.sample, ctx.calendar, ctx.options["granularity"])
    draw = make_draw(throughput, ctx.options["sampling"], ctx.period_date)
    _sample_warnings(ctx, len(ctx.sample.items), "item completati")
    _throughput_assumptions(ctx)
    split = parse_split_rate(ctx.options.get("split_rate"))
    trials = int(ctx.options["trials"])
    result = {"throughput": throughput_summary(throughput)}
    deadline_periods = _deadline_periods(ctx, deadline) if deadline else None
    if remaining is not None:
        _split_assumption(ctx, split, "il gruppo")
        runs = simulate_sequence([remaining], draw, trials, ctx.rng, [split])
        result["when"] = when_summary(ctx, [r[0] for r in runs], deadline_periods)
        result["when"]["remaining"] = remaining
        result["when"]["split_rate"] = list(split) if split else None
    if deadline:
        outcomes = simulate_how_many(deadline_periods, draw, trials, ctx.rng)
        result["how_many"] = how_many_summary(ctx, outcomes, deadline, deadline_periods)
    return result


def _epic_remaining(options: dict) -> int | None:
    count, ids = options.get("remaining"), parse_list(options.get("remaining_ids"))
    if count not in (None, "") and ids:
        raise InputError("Usa --remaining oppure --remaining-ids, non entrambi.")
    if ids:
        return len(set(ids))
    if count in (None, ""):
        return None
    try:
        value = int(count)
    except ValueError:
        raise InputError(f"--remaining deve essere un intero: {count!r}")
    if value < 0:
        raise InputError("--remaining non può essere negativo.")
    return value


def load_groups(options: dict) -> list[dict]:
    groups = []
    if options.get("groups"):
        path = options["groups"]
        if not os.path.isfile(path):
            raise InputError(f"File dei gruppi non trovato: {path}")
        with open(path, encoding="utf-8") as handle:
            try:
                data = json.load(handle)
            except json.JSONDecodeError as exc:
                raise InputError(f"JSON non valido in {path}: {exc}")
        groups.extend(data.get("groups", []) if isinstance(data, dict) else data)
    for spec in options.get("group") or []:
        name, _, count = str(spec).rpartition(":")
        if not name:
            raise InputError(f"--group non valido: {spec!r}. Formato: 'Nome:N'.")
        groups.append({"name": name, "remaining": count})
    if not groups:
        raise InputError("Modalità epics: serve --groups file.json oppure almeno un --group 'Nome:N'.")
    return [_normalize_group(g, i) for i, g in enumerate(groups, start=1)]


def _normalize_group(group, index: int) -> dict:
    if not isinstance(group, dict):
        raise InputError(f"Gruppo #{index} non valido: atteso un oggetto con 'name' e 'remaining'.")
    name = str(group.get("name") or f"Gruppo {index}")
    ids = parse_list(group.get("remaining_ids"))
    if ids:
        remaining = len(set(ids))
    else:
        try:
            remaining = int(group.get("remaining"))
        except (TypeError, ValueError):
            raise InputError(f"Gruppo {name!r}: 'remaining' deve essere un intero (oppure usa 'remaining_ids').")
    if remaining < 0:
        raise InputError(f"Gruppo {name!r}: 'remaining' non può essere negativo.")
    return {"name": name, "remaining": remaining, "split_rate": group.get("split_rate")}


def forecast_epics(ctx: Context) -> dict:
    groups = load_groups(ctx.options)
    throughput = compute_throughput(ctx.sample, ctx.calendar, ctx.options["granularity"])
    draw = make_draw(throughput, ctx.options["sampling"], ctx.period_date)
    _sample_warnings(ctx, len(ctx.sample.items), "item completati")
    _throughput_assumptions(ctx)
    default_split = parse_split_rate(ctx.options.get("split_rate"))
    splits = [parse_split_rate(g["split_rate"]) if g["split_rate"] else default_split for g in groups]
    for group, split in zip(groups, splits):
        _split_assumption(ctx, split, f"il gruppo «{group['name']}»")
    ctx.assumptions.append(
        "Gruppi in sequenza: ogni gruppo parte quando finisce il precedente; un'unica serie di throughput per trial."
    )
    deadline = ctx.options.get("deadline")
    deadline_periods = _deadline_periods(ctx, deadline) if deadline else None
    runs = simulate_sequence([g["remaining"] for g in groups], draw, int(ctx.options["trials"]), ctx.rng, splits)
    ordered = all(all(r[i] >= r[i - 1] for i in range(1, len(r))) for r in runs)
    summaries = []
    for index, (group, split) in enumerate(zip(groups, splits)):
        summary = when_summary(ctx, [r[index] for r in runs], deadline_periods)
        summary.update(name=group["name"], remaining=group["remaining"], split_rate=list(split) if split else None)
        summary["cumulative_remaining"] = sum(g["remaining"] for g in groups[: index + 1])
        summaries.append(summary)
    return {
        "throughput": throughput_summary(throughput),
        "groups": summaries,
        "total": summaries[-1],
        "sequence_consistent": ordered,
    }


def _deadline_periods(ctx: Context, deadline) -> int:
    end = parse_date(deadline, "--deadline")
    if end < ctx.start:
        raise InputError("--deadline precede la data di partenza.")
    if ctx.options["granularity"] == "week":
        return ((end - ctx.start).days + 1) // 7
    return ctx.calendar.working_days_inclusive(ctx.start, end)


def _throughput_assumptions(ctx: Context) -> None:
    granularity = "giorni lavorativi" if ctx.options["granularity"] == "day" else "settimane"
    ctx.assumptions.append(
        f"Throughput per {granularity}, periodi a zero inclusi; {ctx.options['trials']} trial, seed {ctx.seed}."
    )
    if ctx.options["granularity"] == "day":
        ctx.assumptions.append("Item completati in un giorno non lavorativo attribuiti al giorno lavorativo precedente.")
        if ctx.options["sampling"] == "weekday":
            ctx.assumptions.append("Campionamento per giorno della settimana: un lunedì simulato usa i lunedì storici.")
    else:
        ctx.assumptions.append("Granularità settimanale: le festività future non sono modellate; settimana parziale iniziale scartata.")
    ctx.assumptions.append(f"Partenza della previsione: {fmt_date(ctx.start)}.")


def _split_assumption(ctx: Context, split, label: str) -> None:
    if not split:
        return
    lo, hi = split
    text = f"×{lo:g}" if lo == hi else f"tra ×{lo:g} e ×{hi:g} (estratto a ogni trial)"
    ctx.assumptions.append(f"Split rate per {label}: item rimanenti moltiplicati {text}, arrotondati per eccesso.")


def when_summary(ctx: Context, periods: list, deadline_periods: int | None) -> dict:
    ordered = sorted(periods)
    unit = "working_days" if ctx.options["granularity"] == "day" else "weeks"
    points = []
    for p in ctx.percentiles:
        value = percentile_within(ordered, p)
        date_value = ctx.period_date(value)
        points.append({
            "p": p,
            "periods": None if value == math.inf else value,
            "date": date_value.isoformat() if date_value else None,
        })
    beyond = sum(1 for v in ordered if v == math.inf)
    summary = {
        "unit": unit,
        "percentiles": points,
        "beyond_horizon_trials": beyond,
        "histogram": histogram([v for v in ordered if v != math.inf], integer=True),
    }
    if deadline_periods is not None:
        hits = sum(1 for v in ordered if v <= deadline_periods)
        summary["probability_by_deadline"] = round(100 * hits / len(ordered), 1)
    return summary


def how_many_summary(ctx: Context, outcomes: list[int], deadline, periods: int) -> dict:
    ordered = sorted(outcomes)
    return {
        "deadline": parse_date(deadline, "--deadline").isoformat(),
        "periods": periods,
        "percentiles": [{"p": p, "at_least": percentile_at_least(ordered, p)} for p in ctx.percentiles],
        "histogram": histogram(ordered, integer=True),
    }


def throughput_summary(throughput: Throughput) -> dict:
    values = throughput.values
    return {
        "granularity": throughput.granularity,
        "periods": len(values),
        "zero_periods": values.count(0),
        "items": sum(values),
        "distribution": {str(k): v for k, v in sorted(Counter(values).items())},
    }


def histogram(values: list, integer: bool = False, max_bins: int = 15) -> list[dict]:
    if not values:
        return []
    top = max(values)
    width = max(1, math.ceil(top / max_bins)) if top > 0 else 1
    bins = Counter(int(v // width) for v in values)
    return [{"from": b * width, "to": (b + 1) * width - (1 if integer else 0), "count": bins.get(b, 0)}
            for b in range(int(top // width) + 1)]


# --------------------------------------------------------------------------- output


def fmt_date(value) -> str:
    if value is None:
        return "oltre l'orizzonte"
    if isinstance(value, str):
        value = date.fromisoformat(value)
    return f"{IT_WEEKDAYS[value.weekday()]} {value.day} {IT_MONTHS[value.month - 1]} {value.year}"


def fmt_p(p: float) -> str:
    return f"{p:g}%"


def build_report(ctx: Context, result: dict, outputs: dict) -> dict:
    sample = ctx.sample
    reasons = Counter(r.reason for r in ctx.rejected)
    return {
        "mode": ctx.mode,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "parameters": {k: v for k, v in sorted(ctx.options.items()) if v is not None} | {"seed": ctx.seed},
        "data": {
            "source": ctx.history_path,
            "demo": ctx.demo,
            "records_total": ctx.rows_total,
            "records_valid": len(ctx.items),
            "rejected": {
                "count": len(ctx.rejected),
                "reasons": dict(reasons),
                "items": [{"row": r.row, "id": r.id, "reason": r.reason} for r in ctx.rejected],
            },
            "filtered_out": sample.filtered_out,
            "sample_size": len(sample.items),
            "lead_time_fallback": sum(1 for i in sample.items if i.lead_fallback),
            "window": {
                "start": sample.window_start.isoformat(),
                "end_exclusive": sample.window_end.isoformat(),
                "weeks_effective": sample.weeks_effective,
            },
        },
        "reliability": _reliability(ctx),
        "assumptions": ctx.assumptions,
        "result": result,
        "outputs": outputs,
    }


def render_markdown(report: dict) -> str:
    data, result = report["data"], report["result"]
    titles = {"single": "Previsione per singolo work item", "epic": "Previsione per un gruppo", "epics": "Previsione per una lista di gruppi"}
    lines = [f"# {titles[report['mode']]}", ""]
    lines += [
        f"**Dati:** `{data['source']}` — {data['records_total']} record letti, {data['records_valid']} validi, "
        f"{data['rejected']['count']} scartati, **{data['sample_size']} nel campione**.",
        "",
    ]
    reliability = report["reliability"]
    if reliability["level"] == "low":
        lines += ["> ⚠️ **Affidabilità bassa.** Il risultato è mostrato comunque, ma va letto con cautela.", ""]
    for warning in reliability["warnings"]:
        lines.append(f"- ⚠️ {warning}")
    if reliability["warnings"]:
        lines.append("")
    renderer = {"single": _md_single, "epic": _md_epic, "epics": _md_epics}[report["mode"]]
    lines += renderer(result)
    lines += ["## Assunzioni", ""] + [f"- {a}" for a in report["assumptions"]] + [""]
    if data["filtered_out"]:
        lines += ["## Esclusi dal campione", ""]
        lines += [f"- {reason}: {count}" for reason, count in sorted(data["filtered_out"].items())] + [""]
    if data["rejected"]["count"]:
        lines += ["## Record scartati", ""]
        lines += [f"- riga {r['row']} (`{r['id'] or '—'}`): {REJECT_REASONS_IT.get(r['reason'], r['reason'])}"
                  for r in data["rejected"]["items"]] + [""]
    return "\n".join(lines)


def _md_histogram(bins: list[dict], label: str) -> list[str]:
    if not bins:
        return []
    peak = max(b["count"] for b in bins) or 1
    width = max(len(f"{b['from']}–{b['to']}") for b in bins)
    lines = ["```", f"{label}"]
    for b in bins:
        bar = "█" * max(1 if b["count"] else 0, round(30 * b["count"] / peak))
        lines.append(f"{(str(b['from']) + '–' + str(b['to'])).rjust(width)} | {bar} {b['count']}")
    return lines + ["```", ""]


def _md_single(result: dict) -> list[str]:
    metric = "cycle time" if result["metric"] == "cycle" else "lead time"
    unit = "giorni" if result["unit"] == "calendar_days" else "giorni lavorativi"
    lines = ["## Service Level Expectation", ""]
    if result.get("elapsed_days") is not None:
        lines += [
            f"L'item è aperto da **{result['elapsed_days']:g} {unit}** (più vecchio del {result['age_percentile']:g}% "
            f"degli item completati). Percentili calcolati sui {result['conditional_sample_size']} item durati di più.",
            "",
        ]
    lines += ["| Probabilità | Si chiude entro | Data (se parte/continua oggi) |", "|---|---|---|"]
    for point in result["percentiles"]:
        if point["days"] is None:
            lines.append(f"| {fmt_p(point['p'])} | non stimabile | — |")
        else:
            lines.append(f"| {fmt_p(point['p'])} | {point['days']:g} {unit} | entro {fmt_date(point['date'])} |")
    lines.append("")
    p85 = next((pt for pt in result["percentiles"] if pt["p"] == 85 and pt["days"] is not None), None)
    if p85:
        lines += [f"**L'85% degli item di questo tipo si chiude entro {p85['days']:g} {unit}** ({metric}).", ""]
    lines += _md_histogram(result["histogram"], f"{metric} storico ({unit}) | item")
    return lines


def _md_when(summary: dict) -> list[str]:
    unit = "giorni lavorativi" if summary["unit"] == "working_days" else "settimane"
    lines = ["| Probabilità | Finito entro | " + unit.capitalize() + " |", "|---|---|---|"]
    for point in summary["percentiles"]:
        periods = "—" if point["periods"] is None else point["periods"]
        lines.append(f"| {fmt_p(point['p'])} | {fmt_date(point['date'])} | {periods} |")
    lines.append("")
    points = summary["percentiles"]
    if len(points) >= 2:
        lo, hi = points[0], points[-1]
        lines += [f"Tra il {fmt_p(lo['p'])} ({fmt_date(lo['date'])}) e il {fmt_p(hi['p'])} ({fmt_date(hi['date'])}) "
                  "c'è l'ampiezza dell'incertezza: la data va comunicata come probabilità, mai come data secca.", ""]
    if "probability_by_deadline" in summary:
        lines += [f"Probabilità di finire entro la scadenza: **{summary['probability_by_deadline']:g}%**.", ""]
    if summary["beyond_horizon_trials"]:
        lines += [f"⚠️ {summary['beyond_horizon_trials']} trial non finiscono entro l'orizzonte massimo di simulazione.", ""]
    return lines


def _md_throughput(throughput: dict) -> list[str]:
    unit = "giorni" if throughput["granularity"] == "day" else "settimane"
    return [f"Throughput storico: {throughput['items']} item in {throughput['periods']} {unit}, "
            f"di cui {throughput['zero_periods']} a zero.", ""]


def _md_epic(result: dict) -> list[str]:
    lines = _md_throughput(result["throughput"])
    if "when" in result:
        when = result["when"]
        lines += [f"## Quando finiscono {when['remaining']} item", ""] + _md_when(when)
        p85 = next((pt for pt in when["percentiles"] if pt["p"] == 85), None)
        if p85:
            lines += [f"**C'è l'85% di probabilità di finire entro {fmt_date(p85['date'])}.**", ""]
        lines += _md_histogram(when["histogram"], "periodi per finire | trial")
    if "how_many" in result:
        how = result["how_many"]
        lines += [f"## Quanti item entro {fmt_date(how['deadline'])}", "",
                  "| Probabilità | Item completati (almeno) |", "|---|---|"]
        lines += [f"| {fmt_p(pt['p'])} | {pt['at_least']} o più |" for pt in how["percentiles"]] + [""]
    return lines


def _md_epics(result: dict) -> list[str]:
    lines = _md_throughput(result["throughput"])
    for group in result["groups"]:
        lines += [f"## {group['name']} — {group['remaining']} item (cumulativi: {group['cumulative_remaining']})", ""]
        lines += _md_when(group)
    total = result["total"]
    p85 = next((pt for pt in total["percentiles"] if pt["p"] == 85), None)
    if p85:
        lines += [f"**Totale: c'è l'85% di probabilità di finire tutta la lista entro {fmt_date(p85['date'])}.**", ""]
    lines += ["I percentili di ogni gruppo vengono dalla stessa simulazione continua: non si sommano.", ""]
    return lines


def write_control_csv(path: str, ctx: Context) -> None:
    columns = ["row", "id", "status", "reason", "type", "tags", "ready_at", "started_at", "completed_at",
               "lead_time_days", "cycle_time_days", "lead_time_fallback", "flags"]
    in_sample = {i.id for i in ctx.sample.items}
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        for item in ctx.items:
            status = "used" if item.id in in_sample else "filtered_out"
            writer.writerow([
                item.row, item.id, status, ctx.sample.filter_reason.get(item.id, ""), item.type, ";".join(item.tags),
                _iso(item.ready_at), _iso(item.started_at), _iso(item.completed_at),
                _round(item.lead_time), _round(item.cycle_time), str(item.lead_fallback).lower(), ";".join(item.flags),
            ])
        for rejection in ctx.rejected:
            writer.writerow([rejection.row, rejection.id, "rejected", rejection.reason] + [""] * 9)


def _iso(value: datetime | None) -> str:
    return value.isoformat() if value else ""


def _round(value: float | None) -> str:
    return "" if value is None else f"{value:.3f}"


# --------------------------------------------------------------------------- cli


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monte Carlo flow forecasting (no network, normalized input only).")
    sub = parser.add_subparsers(dest="mode", required=True)
    common = argparse.ArgumentParser(add_help=False, argument_default=argparse.SUPPRESS)
    common.add_argument("--config", help="JSON file with default options (CLI wins)")
    common.add_argument("--history", help="CSV/JSON of completed work items")
    common.add_argument("--demo", action="store_true",
                        help="allow the bundled example history (explicitly requested demos only)")
    common.add_argument("--window-weeks", type=int, help="history window in weeks (0 = all; default 12)")
    common.add_argument("--as-of", help="reference date; history window ends the day before (default today)")
    common.add_argument("--granularity", choices=["day", "week"])
    common.add_argument("--trials", type=int)
    common.add_argument("--seed", type=int)
    common.add_argument("--percentiles", help="comma list, default 50,70,85,95")
    common.add_argument("--start", help="forecast start date (default --as-of)")
    common.add_argument("--calendar", help="workdays | all | mon,tue,wed,...")
    common.add_argument("--holidays", help="file (one ISO date per line or JSON list) or comma list of dates")
    common.add_argument("--sampling", choices=["uniform", "weekday"], help="throughput sampling technique")
    common.add_argument("--type", help="filter sample by type (comma list)")
    common.add_argument("--tag", help="filter sample by tag (comma list, any match)")
    common.add_argument("--out-dir")
    common.add_argument("--format", choices=["json", "markdown", "both"])

    single = sub.add_parser("single", parents=[common], help="one work item: cycle/lead time percentiles")
    single.add_argument("--metric", choices=["cycle", "lead"])
    single.add_argument("--elapsed-days", type=float, help="the item is already in progress since N days")

    epic = sub.add_parser("epic", parents=[common], help="one group: when will N items be done")
    epic.add_argument("--remaining", help="number of remaining items")
    epic.add_argument("--remaining-ids", help="comma list of remaining item ids")
    epic.add_argument("--deadline", help="also simulate how many items by this date")
    epic.add_argument("--split-rate", help="multiplier (1.2) or range (1.0-1.3) for not-yet-split work")

    epics = sub.add_parser("epics", parents=[common], help="ordered groups, one after the other")
    epics.add_argument("--groups", help="JSON file with the ordered groups")
    epics.add_argument("--group", action="append", help="'Name:N', repeatable, appended after --groups")
    epics.add_argument("--deadline", help="also report the probability of each group by this date")
    epics.add_argument("--split-rate", help="default split rate for groups without their own")
    return parser


def resolve_options(args: argparse.Namespace) -> dict:
    cli = {k: v for k, v in vars(args).items() if k not in ("mode", "config")}
    config = {}
    config_path = getattr(args, "config", None)
    if config_path:
        if not os.path.isfile(config_path):
            raise InputError(f"File di configurazione non trovato: {config_path}")
        with open(config_path, encoding="utf-8") as handle:
            try:
                raw = json.load(handle)
            except json.JSONDecodeError as exc:
                raise InputError(f"JSON non valido in {config_path}: {exc}")
        base = os.path.dirname(os.path.abspath(config_path))
        for key, value in raw.items():
            key = key.replace("-", "_")
            if key in PATH_KEYS and isinstance(value, str) and not os.path.isabs(value):
                value = os.path.join(base, value)
            config[key] = value
    return {**DEFAULTS, **config, **cli}


def run(mode: str, options: dict) -> dict:
    ctx = build_context(mode, options)
    forecast = {"single": forecast_single, "epic": forecast_epic, "epics": forecast_epics}[mode]
    result = forecast(ctx)
    out_dir = options["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    outputs = {"control_csv": os.path.join(out_dir, "control.csv")}
    if options["format"] in ("json", "both"):
        outputs["json"] = os.path.join(out_dir, "result.json")
    if options["format"] in ("markdown", "both"):
        outputs["markdown"] = os.path.join(out_dir, "summary.md")
    report = build_report(ctx, result, outputs)
    write_control_csv(outputs["control_csv"], ctx)
    if "json" in outputs:
        with open(outputs["json"], "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2, default=str)
    if "markdown" in outputs:
        with open(outputs["markdown"], "w", encoding="utf-8") as handle:
            handle.write(render_markdown(report))
    return report


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        options = resolve_options(args)
        report = run(args.mode, options)
    except InputError as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 2
    if options["format"] == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
    else:
        print(render_markdown(report))
    print("File generati: " + ", ".join(report["outputs"].values()), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
