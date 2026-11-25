# Review — alternative formal definitions for ME1–ME5 (submitted 2026-11-22)

**Submitted text**: `docs/specs/meff_boundary_v0_2_alt_definitions_DECLINED.md` (verbatim, DECLINED)
**Compared against**: `docs/specs/meff_boundary_v0_2.md` (adopted), `docs/decisions/meff_boundary_disposition_v1.md` (rulings D-A, D-B)
**Method**: clause-by-clause, plus a pre-registered probe (`runs/S45/meff_alt_definitions_probe_registration.md` → `runs/S45/meff_alt_definitions_results.txt`, 6/6 criteria met)
**Evidence level**: IDENTITY / ARITHMETIC / LOGIC. No physics verdict.

---

## Verdict

**Not done, and not registerable as written.** The submission is not a refinement of v0.2 — it is a
**re-specification that reverses two settled rulings and reinstates two clauses the audit falsified.**

| Clause | Proposal | Verdict | Governing evidence |
| --- | --- | --- | --- |
| `ME1` | `Φ(p)=Φ(q) ⟺ p=q` on all of `ℳ`, "excluding topological singularities" | **REJECT as formulated** — violated by **every** closed object, so not a boundary any object can approach | probe E1: `μ_ov(ball) = 1.000000` |
| `ME2` | `δS_eff/δφ = 0` retains a conserved current | **REJECT — out of scope, and formally vacuous** | probe E4 (it is the Euler–Lagrange equation); S1 (matter sector is the `C` domain) |
| `ME3` | `ΔS_vN ≤ κ·A_eff` | **REJECT — it is `C_info` renamed**, i.e. ruling D-B reversed | probe E2a: relative difference `0.000e+00`, `A_crit = 8.013e-11 m²` (identical to Q2) |
| `ME4` | `dχ/dt = 0`, "except at phase transition points" | **REJECT — falsified by the project's own census, and unfalsifiable as qualified** | probe E5: `φ_conv = 8.5e-11`; `1000/1000` satisfiable |
| `ME5` | `\|∂ℳ_t/∂τ\| ≤ Λ_max` | **REJECT — directionally inverted**, and not a clock | probe E3: satisfied by a configuration `1.06e12` times too slow to photograph |
| §2 | namespace declarations | **PARTIALLY ACCEPT** — one rule adopted (S5), one check implemented (F), six statements corrected; and the stated conflict count is wrong by three | G4, G5 |
| §3 | ledger entry | **ACCEPT in shape, four fields need correcting** | G4 |

**The intents are right in all five cases.** Injectivity, no catastrophic leakage, bounded information loss,
no tearing, a time scale — every one of those is in v0.2. What fails is the formalisation, and in four cases
it fails by reproducing a defect that is already on the record with a number attached.

---

## A. What the submission gets right (recorded first, because it is not nothing)

1. **The S1 doctrine is stated correctly and is the right doctrine.** "The `ME` set must be strictly mutually
   exclusive with `C` (metric and `T_μν` evolution) and `CM` (observation channels)" — that is exactly the
   registry's rule, and stating it *before* the definitions is the correct order of operations.
2. **"Bare `M1`–`M5` is prohibited"** is right, and is in force.
3. **R4's closure of subscripts** (`M_geo`, `M_phys`) is right and already in force.
4. **The demand for a lint rule over the `ME` namespace** is right, was not yet implemented, and is now
   implemented (check F). This is the one concrete item from the submission that changed the repository.
5. **"Qualify the scope when `M`-class symbols from another system appear in the same context"** is a real
   improvement — better than what the registry had. Adopted as rule S5 (`Gate:M4` vs `Constraint:ME4`).

## B. Findings on the five definitions

### V1 — CRITICAL: proposed `ME1` is violated by every closed object, including the intact sphere

`∀p,q ∈ ℳ: Φ(p)=Φ(q) ⟺ p=q` requires the projection to be injective **on the whole body**. Measured: a solid
ball on a `200³` grid gives `μ_ov = 1.000000` — **every** occupied column contains two distinguishable points.
That is not a near miss at a corner; it is the entire object. And it must be: by invariance of domain, no
continuous injective map `ℝ³ → ℝ²` exists at all, and a body with interior volume cannot inject into a plane
by any map whatever.

Two consequences:

- **The escape clause does all the work.** "(excluding topological singularities)" would have to absorb the
  whole body, which is the conclusion the constraint was supposed to establish. An exclusion that covers
  100 % of the cases is not a tolerance.
- **The defect class is already on the record twice.** It is `C_info`'s: a constraint "the object is born
  outside of" (F2). Reintroducing it under a new letter does not change its attainability.

**The idea is right and is what v0.2 adopted.** One declared parameter separates the impossible form from the
usable one: with a depth resolution `Δz_res`, a converted plate (`d_∥ = 15.4 fm`) has `μ_ov = 0` at optical
resolution — *the sheet is a graph* — while a folded or hollow body does not. Probe E1 measures both: `μ_ov(plate)
= 0.000000`, `μ_ov(ball) = 1.000000`. The proposal's own sentence — "no non-physical topological folding
occurs" — is exactly `μ_ov ≤ δ_ov` at a declared scale, and not `Φ` injective on all of `ℳ`.

### V2 — the carrier of injectivity is `ME1`, and `ME1` is not descended from `C_geo`

"`ME1` (formerly `C_geo`) … inheriting the core demand of the original `M1`" is wrong twice.

- `C_geo` was the **curvature** clause, and the audit's central finding (F1) is that `C_geo` **assumed**
  injectivity via the notation `z = z(x_i)`. It cannot be the predecessor of the constraint that supplies it.
  The lineage is the reverse: `C_geo`'s defect is *why* `ME1` had to be created.
- `M1` never existed. `M1–M5` was a rejected label proposal (registry §3, §7).

The adopted lineage is: `ME1 ← new` (carrying `C_info`'s zero case), `ME2 ← C_geo`, `ME3 ← C_phys`,
`ME4 ← C_top`, `ME5 ← new`. The submission shifts the first three by one slot.

### V3 — proposed `ME2` is the field equation, and belongs to the `C` domain

`δS_eff/δφ = 0` is not a conservation statement. It is the **Euler–Lagrange equation** — computed
symbolically for `S = ∫[½(φ̇² − |∇φ|²) − V(φ)]`, it returns `φ̈ − ∇²φ + V′(φ) = 0`, which every solution of
the theory satisfies by definition. As a constraint it forbids nothing.

Conservation requires a symmetry of the action (`δS = 0` under a *transformation*), not a variation of the
*field*. "The EOM holds ⇒ a non-trivial conserved current survives in 2D" does not follow; what would carry
content is "the `z`-averaged 3D solution satisfies the 2D EOM", which is a statement about the **reduction
error**, not about a current — and v0.2's `ME3` (perpendicular energy fraction) is the measurable form of it.

**Scope violation (S1).** Even if it were well-formed, a claim about the matter action and its symmetries is
a predicate over `(γ_ij, K_ij, T_μν)` — the `C` domain. And specifically it enters `C3`'s territory
(weak-interaction preservation, self-consistent in action), whose in-action NO-GO is parameter-independent.
Registering it as `ME2` would let the branch make a matter-sector claim, which is precisely the inference
S1 now forbids. Separately, baryon-number conservation is already a consequence of `∇_μT^{μν} = 0` in the
chain's own equations — so the constraint is either redundant with what S0–S2 already solve, or false.

### V4 — proposed `ME3` is `C_info`, algebraically, and ruling D-B is reversed

With the project's own extensive model, `ΔS_vN/A_⊥` and `ΔH/A_⊥` are the **same number** (relative difference
`0.000e+00`). Setting `δ_info := κ·A_eff` turns the cap into `ΔH/A ≤ κ` — the retired `C_info` inequality —
and the implied critical area is `8.013e-11 m²`, identical to probe Q2's figure to four digits.

For **any** extensive entropy the conclusion is stronger and worse: `ΔS/A ≈ s·H`, so the cap reads
`H ≤ κ/s`. With one bit per atom (`s = 3.3e28 bit·m⁻³`) and `κ = 10¹² bit·m⁻²`, `H_max = 3.03e-17 m` — the
registered object is **16.8 decades** too tall. Scaling κ to admit 1.75 m would admit *every* object of that
height. **The cap is a bound on thickness wearing an information label**, which is exactly D3's finding about
`C_info`.

Also: `ΔS_vN` is undefined as used. After tracing out `z`, the von Neumann entropy depends on the *state*, not
on the geometry, and for a pure global state it is an entanglement entropy — not "the information lost by a
projection" of a classical object. And "downgrades the hard threshold to a reportable metric" contradicts
itself: an inequality with a cap is a gate. Ruling D-B put the magnitude **outside** scoring (`BUDGET-1`);
this clause puts it back inside.

### V5 — proposed `ME4` is the falsified `C_top` plus an unfalsifiability clause

`dχ/dt = 0` "except at phase transition points" is `C_top` unchanged, and `C_top` was falsified against the
project's own fragment census: `χ(2D) = 1.18e10` vs `χ(3D) = 2`, so `χ` has already changed once
`φ_conv = 8.5e-11` of the object converts — the condition holds on a set of measure `~10⁻¹⁰` of the branch,
and is directionally inverted.

The escape clause then removes what little testability remained: for **any** measured `χ(t)`, every
discontinuity can be declared a phase-transition point. Measured: `1000/1000` adversarial jump sets are
accommodated, so the condition cannot fail. This is v0.1's citation condition 2 again, rejected as **F8**
("true by construction"). A constraint that cannot fail is not a constraint.

What does carry content — and is what v0.2 adopted as `ME4` — is the **fragment census**: `N_comp(t)`
monotone in swept volume, matched to the registered `8.12e9` layers / `1.18e10` plates, with no handles
beyond the census. That is falsifiable, because the census numbers can be wrong.

### V6 — proposed `ME5` is directionally inverted, and is not a clock

A rate **cap** bounds elapsed time **from below**: `t_conv ≥ Δ/Λ_max`. L3 needs the opposite — an upper bound
on exposure, `τ_exp ≤ t_rip`. Measured: with an entirely admissible `Λ_max = 10⁻³ s⁻¹`, the constraint is
satisfied by a configuration whose minimum conversion time exceeds `t_rip` by a factor **`1.06e12`**. So the
proposed `ME5` **certifies exactly the case that cannot be photographed** — which is the failure mode the
audit warned about when it said a branch without a lifetime constraint "will silently produce 'L3 satisfied'
verdicts for configurations that cannot be photographed" (F9).

Two further problems: `∂ℳ_t/∂τ` is not a defined object (a manifold has no derivative with respect to time as
a set), and `Λ_max` is an unregistered arbitrary constant — the exact failure mode the audit prohibited
("must not adopt a δ that makes a constraint pass by construction").

The exact, scale-free statement the project already has is `t_rip = √2 L/c`, verified to `1e-15` (D4). That is
what v0.2's `ME5` registers, together with its corollary: no faithful reflected-light frame of a surviving
sheet exists.

## C. Governance findings

### G1 — the submission reverses ruling D-B while claiming to implement it

`ME3` is presented as "downgrading the hard threshold … to a reportable upper-limit metric". It does the
opposite: it is a **cap** (a gate), and it is the **same** cap. Implementing D-B means `ΔH` is reported and
never scored; v0.2 §3 and `BUDGET-1` do that. Any future re-proposal must state which ruling it supersedes.

### G2 — the submission lets the branch legislate in the `C` domain

`ME2` as proposed is a matter-sector constraint. That is the inference that S1 exists to block, and it is the
same error in the opposite direction as the one D-A was written to prevent (branch products scoring the
chain). A branch constraint may bound *where the approximation holds*; it may not bound *what the matter does*.

### G3 — the predecessor map is wrong, and the error matters

Claiming `ME1 ← C_geo` inverts F1: `C_geo` presupposed injectivity, so it cannot be its ancestor. The
practical risk is that a future reader concludes v0.1 was safer than it was, and that the audit's central
finding was a renaming exercise.

### G4 — technical corrections to §2 and §3

| Claim | Correction |
| --- | --- |
| "`ME1–ME5` are legal bare symbols" | They are legal **prefixed** labels. S2's prohibition is on bare single letters (`M1`); a two-letter prefix is the requirement, not an exemption from it. |
| "if they appear with `M`-class symbols, qualify the scope (`Gate:M4` vs `Constraint:ME4`)" | **Adopted as rule S5.** This is the submission's best contribution. |
| "`symbol_lint.py` Rule C extended to the `ME` namespace" | **Rule C is the `K1–K4` check.** The ME check is now **Rule F** (bare `M1–M5`; `ME` labels cited in chain-evidence contexts). |
| "Status: Active (Draft)" | `ADOPTED`. v0.2 is adopted, not a draft. |
| "Owner: v0.2 Draft / Theoretical Derivation" | Owner: the S3→S4 branch, governed by the disposition record. |
| "§12.x" ledger entry | §12 is the symbol section and §13 already records the disposition. A duplicate entry would give two sources of truth. |

### G5 — the proposal's stated reason for the `ME` prefix understates the problem by three owners

The submission justifies `ME` by "avoiding conflicts with the mass parameter or the external review gate `M4`".
Two owners are named. Implementing the check found **five**:

| Owner | Where | Meaning |
| --- | --- | --- |
| mass | throughout | `M`, `M(R)`, `M_STEP` |
| gate | roadmap §F.8 | `M4` external review |
| unfolding mode | `painting_render_v1.py` | `M1` uniform pack · `M2` density-preserving |
| visibility metric | `abandon_assumption_visual_v1.py` | `M1` peak brightness · `M2` visible duration · `M3` structural freedom · `M4` threshold |

So `M1` already means two different things in two active source files, and `M4` two more. This **strengthens**
the submission's conclusion (the `ME` prefix is mandatory) while destroying its premise (that two conflicts
needed resolving). It also means the proposed `Gate:M4`/`Constraint:ME4` qualifier separates two of five, not
two of two — which is why it was adopted as the general rule **S5** rather than as a two-term convention.

Registered in `docs/conventions/symbol_registry.md` §2a and coerced into `symbol_lint.py` rule F (advisory,
because `M1`–`M4` are legitimate pre-existing owners whose labels are embedded in archived stdout).

## D. What would make a re-specification adoptable
Not an opinion — the five tests each clause must pass, derived from the findings above:

1. **Attainable** — at least one physically realisable configuration must satisfy it, and at least one must
   fail it (V1, V4).
2. **In-domain** — the predicate must be over `ℳ_eff` membership only; no `T_μν`, no observation channel (V3).
3. **Not a rescaling of a retired clause** — must not reduce algebraically to `C_info`, `C_top`, `C_geo` or
   `C_phys` under a renaming (V4, V5).
4. **Falsifiable** — a stated observation must be able to break it; escape clauses that absorb all cases are
   disqualifying (V5).
5. **Correctly directed** — a bound must bind on the side the physics requires; a cap on a rate is not a bound
   on duration (E6).
6. **Threshold registered or OPEN** — never chosen to make a case pass (V6, and audit §D).

## E. Answer to the question asked

"Below is done?" — **No.** The definitions that are registered are `docs/specs/meff_boundary_v0_2.md` §2, and
they were adopted before this submission arrived. Of the submission: one idea improved the repository (rule
S5), one item it requested is now implemented (lint rule F), and five formalisations are declined with the
numbers above. Nothing in the submission changes any adopted definition, and nothing in it licenses a
visibility conclusion.

---

*Content generated by AI*
