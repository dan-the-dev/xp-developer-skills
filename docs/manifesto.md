# AMPD manifesto

**Amplified XP & Product Development** — an experimental, **AI-native** layer on top of disciplined engineering. Not a replacement for craft; a **constraint system** so agents participate inside the same habits great teams already value.

## Principles

1. **Amplify, don’t bypass** — AI should strengthen tests, refactoring, delivery, and clarity—not skip them for speed.
2. **Skills over prompts** — Reusable **operational workflows** (versioned, composable), not one-off chat magic.
3. **Verify every change** — If it isn’t testable, reviewable, and incremental, it isn’t done. Re-run **scoped** (affected) tests after every edit; choose the **right test layers and techniques** per slice ([`test-strategy-selection.md`](test-strategy-selection.md)); run **all verify steps the current project defines** at **slice boundary** ([`delivery-process.md`](delivery-process.md), [`project-verification.md`](project-verification.md)). Deliver a feature on **one feature branch** (commits per increment; PR per feature — §1a). See [`technical-excellence-catalog.md`](technical-excellence-catalog.md) for the practice inventory we amplify.
4. **Simplicity first** — Prefer small steps, honest commits, and validated learning over big designs and speculation. Structure work follows [`simple-design.md`](simple-design.md): Simple Design + YAGNI as compass; **Object Calisthenics mandatory**; GoF patterns as destinations that emerge via refactoring — not up-front blueprints.
5. **Human + machine** — Product judgment, risk, and ethics stay human; repetition, consistency, and guardrails scale with tooling.

## Stance

We take **Extreme Programming**, **Continuous Delivery**, **clean design**, and **lean product** seriously, and ask: *what if agents had to follow the same rules?*

This repository stays **lightweight**, **implementation-driven**, and **open to evolution**—the manifesto included.
