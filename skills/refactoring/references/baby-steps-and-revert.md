# Baby steps and revert (Kent Beck style)

## The loop

Repeat until the refactoring goal is satisfied:

1. **Choose** the smallest mechanical next step (one Extract Method, one Rename, one Move).
2. **Apply** only that step.
3. **Run tests** starting with the narrowest meaningful scope.
4. **If green** — optionally widen (module, package, CI subset) if you touched shared code.
5. **If red** — **stop**. Treat the last change as **invalid** as a refactor:
   - **Revert** / undo the step (git checkout chunk, undo in editor, `git revert` if committed — team norm).
   - **Shrink** the step (split extract into two, rename in smaller scope).
   - Retry.

Do **not** “fix forward” under red during a refactor-only pass by tweaking assertions or outputs — that is **mixing hats**.

---

## What counts as “one step”

**One step** = one intention that tooling or a human can verify mechanically:

- Rename one symbol (with IDE rename when available)
- Extract one function / one class boundary
- Inline one indirection **or** unwrap one wrapper in a focused area
- Move one method / field between types

**Not** one step:

- Rename **and** extract **and** change import structure **before** running tests

---

## Tooling

Prefer **automated** refactorings (IDE, lang-specific tools) for renames and moves — fewer human typos, easier revert.

---

## Psychology

Small steps feel slower for five minutes and save **hours** when something subtle breaks.

The rule **revert then retry smaller** is the adult version of: *if the wing fell off, put the last brick back and try a gentler move.*
