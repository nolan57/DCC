# Pre-registration — C1/C2 re-registration in the ME/CM system (2026-11-22)

**Registered before execution.** Output: `runs/S45/crosswalk_checks_results.txt`.

**Subject**: the instruction *"re-register C1/C2 under the ME/CM system, bypassing the retired naming family, then
talk about ordering."* Two operations are possible and they are not the same:

- **(a) rename** — `C1 → ME1`, `C2 → CM2` (or similar), so the constraints are *written* in the new namespace;
- **(b) bridge** — keep the constraint names and register, for each, its *test expression* in `ME`/`CM` at a
  declared scale, with the logical relation between them.

The checks below decide which is legal and which is content-preserving. They are not stylistic.

**Objects**: the five toy states below are used only to test *implication relations between predicates*; they carry
no physics beyond the registered numbers.

| id | state | thickness | column-conserving (`C1`) | intralayer strain | interlayer |
| --- | --- | --- | --- | --- | --- |
| `S_A` | ideal 2D state | `d_∥ = 15.4 fm` | **yes** | zero | continuous |
| `S_B` | thin slab, not column-conserving | `10 fm` | no | zero | continuous |
| `S_C` | intact body | `0.070 m` | no | zero | continuous |
| `S_D` | 2-sheet stack | `7 d_∥` (gapped) | no | zero | **broken** |
| `S_E` | `S_A` with an intralayer strain field | `d_∥` | **yes** | **non-zero** | continuous |

---

## Checks

**X1 — is `C1` equivalent to its `ME1` expression, or only stronger than it?**
Evaluate `C1`, `ME1@Δz_res` for `Δz_res ∈ {100 μm, d_∥}` and `CM1@λ` for `λ = 500 nm` over `S_A…S_E`.
*Registered expectation*: `C1 ⟹ ME1` holds with **zero** counterexamples (no state has `C1` true and `ME1` false);
the converse fails with at least two witnesses (`S_B`, `S_C` at `100 μm`). So `ME1` is a **necessary proxy**, not
an equivalent.
*Falsifier*: if any state has `C1` true and `ME1` false, `C1 ⇏ ME1` and the bridge must be stated as a
co-satisfaction, not an implication — a weaker and less useful registration.

**X2 — can any `ME`/`CM` predicate express `C2` at all?**
`S_A` and `S_E` differ **only** in intralayer strain. Compare every proxy verdict on the pair.
*Registered expectation*: all proxy verdicts identical, i.e. the pair is **indistinguishable** to the gate
vocabulary, so no predicate in it can decide `C2`.
*This is the decisive check*: if `C2` is invisible to `ME`/`CM`, then "rename `C2` into `CM`" does not rename
`C2` — it deletes its content and substitutes a predicate that cannot see it.

**X3 — textual corroboration.** Count occurrences of the word `strain` in the adopted spec and in the `CM`
definitions, excluding its appearance inside the word `constraint`/`constraints`.
*Registered expectation*: `0`.

**X4 — is `C3` expressible?** `C3` is an in-action statement. Check whether any `ME`/`CM` definition mentions the
action or `T_μν`.
*Registered expectation*: none. And registry `S1` **forbids** it as an `ME` predicate (§5: "An `ME` predicate may
never be a chain constraint"), so this is a prohibition, not a gap.

**X5 — how much of the constraint diagonal is expressible in gate space?**
Count how many of `{C1, C2, C3}` have an `ME` proxy.
*Registered expectation*: `1 of 3`. Consequence: a ladder indexed by `ME` labels **cannot** walk the
constraint-relaxation diagonal — it can take at most one of its steps.

**X6 — blast radius of the literal rename.**
Count files and citations that would change meaning if `C1` became an `ME` label: (i) citations of `C1`/`C2` in
chain/gate documents, (ii) any `ME` label already used as a chain constraint (registry `S1` forbids this).
*Registered expectation*: (i) large — the constraints are cited by every gate and ledger row (registry `R2`'s stated
reason for awarding them `C`); (ii) `0`, so the rename would make all of (i) non-compliant under `S1`.

---

## Falsification

If X2 does **not** show `S_A`/`S_E` indistinguishable, then `C2` does have a gate expression and the bridge is
incomplete rather than impossible — I would withdraw the "no proxy" claim. If X1 shows `C1 ⇏ ME1`, the bridge is
demoted to co-satisfaction. Each verdict is reported separately; a failed prediction stands as recorded.
