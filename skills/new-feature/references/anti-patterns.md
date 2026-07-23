# Anti-patterns

- Monolithic increment (“build all of FizzBuzz” in one backlog line)
- Parallel open `[ ]` lines implemented without finishing one
- **Implementing in new-feature** — editing `src/`, `test/`, or marking `[x]` without **new-increment**
- Skipping **`new-increment`** (simulating slices in one chat)
- No increment backlog file
- **Documentation theater** — many `acceptance-examples/*.md` or per-increment test lists created during planning
- Asking **`new-increment`** to batch “increments 2–7”
- Claiming feature done while backlog still has `[ ]`
- Assuming **automatic** mode without explicit user opt-in
- Continuing to the next increment in **step** mode without user go-ahead
- Skipping **post-increment review** between increments when orchestrating
- Continuing **automatic** after a review that reported **blocking** gaps
- Treating post-increment review as a license to rewrite the feature
- Running **full** apply-capable review on every automatic increment when light depth would suffice
