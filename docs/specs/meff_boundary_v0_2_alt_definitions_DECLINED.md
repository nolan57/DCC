# Alternative formal definitions for ME1–ME5 (submitted 2026-11-22) — **DECLINED**

**Submitted**: 2026-11-22 11:59, by the project governor, as "the formal definition draft for ME1–ME5,
ready for direct registration into the project ledger"
**Status**: **DECLINED.** Not registered in the ledger. The adopted definitions are
`docs/specs/meff_boundary_v0_2.md` §2.
**Review**: `reports/reviews/meff_boundary_alt_definitions_review.md` (findings E1–E5, G1–G4)
**Probe**: `src/s45_branch/meff_alt_definitions_probe.py` → `runs/S45/meff_alt_definitions_results.txt`
(registered first in `runs/S45/meff_alt_definitions_probe_registration.md`)

## Registration notes

1. **Body reproduced verbatim**, including LaTeX macro artefacts (`mathbb{R}`, `mathcal{A}{text{eff}}`,
   `Lambda{text{max}}`, where an underscore appears to have been dropped). Not corrected here, for the same
   reason as in the v0.1 registration: correcting a submitted text silently would be editing it.
2. **Declined ≠ discarded.** The submission is preserved because four of its five clauses reproduce defects
   already recorded against v0.1, and a re-proposal six weeks from now must be able to see that this was
   answered. Deletion would guarantee the same text returns.
3. **The intent behind all five clauses is sound** and is honoured in v0.2: injectivity, no catastrophic
   leakage, bounded information loss, no tearing, a time scale. What is declined is the formalisation.
4. The proposed predecessor mapping (`ME1 ← C_geo`, `ME2 ← C_phys`, `ME3 ← C_info`) is **not** the adopted
   one; see review G3.

---

## 1. Formal Definitions and Predicate Scopes (S1)

According to the S1 rule, the predicate scope of the ME set must be strictly mutually exclusive with the C set (spacetime metric and energy-momentum tensor evolution) and the CM set (observation channels). The ME set is exclusively for the information topology and evolutionary boundaries during the smooth 2D conversion of macroscopic objects.

*   ME1 (formerly C_geo) - Geometric Injectivity
    *   Definition: The mapping from three-dimensional space to the two-dimensional plane Phi: mathbb{R}^3 to mathbb{R}^2 must maintain injectivity within local neighborhoods.
    *   Formalization: forall p, q in mathcal{M}, Phi(p) = Phi(q) iff p = q (excluding topological singularities).
    *   Physical Meaning: Ensures that no non-physical topological folding occurs during the smooth 2D conversion, inheriting the core demand of the original M1.
*   ME2 (formerly C_phys) - Physical Conservation Boundary
    *   Definition: During the dimensional reduction process, the system's effective action S_{text{eff}} must satisfy a controlled boundary of Noether symmetry breaking.
    *   Formalization: delta S_{text{eff}} / delta phi = 0 retains at least one non-trivial conserved current J^mu in the 2D limit.
    *   Physical Meaning: Constrains the core physical properties (such as charge, baryon number) of the 3D macroscopic object from suffering catastrophic leakage during 2D conversion.
*   ME3 (formerly C_info) - Information Budget Cap
    *   Definition: The von Neumann entropy change Delta S_{text{vN}} during the 2D conversion process must be limited within the bit budget the system can bear.
    *   Formalization: Delta S_{text{vN}} le kappa cdot mathcal{A}{text{eff}} (where mathcal{A}{text{eff}} is the effective 2D area, and kappa is the upper limit of information density).
    *   Physical Meaning: Downgrades the hard threshold of the original C_info to a reportable upper-limit metric, avoiding physical unattainability.
*   ME4 (formerly C_top) - Topological Invariance
    *   Definition: Within the smooth evolution parameter t in [0, 1], the system's Euler characteristic chi or Betti numbers b_i must remain piecewise constant.
    *   Formalization: frac{d}{dt} chi(mathcal{M}_t) = 0 (except at phase transition points).
    *   Physical Meaning: Ensures that the 2D conversion process is a continuous deformation rather than tearing or gluing.
*   ME5 (New) - Evolution Clock Constraint
    *   Definition: Introduces an intrinsic time scale tau to constrain the transition rate from three dimensions to two.
    *   Formalization: frac{partial mathcal{M}t}{partial tau} le Lambda{text{max}} (where Lambda_{text{max}} is the maximum allowable deformation rate).
    *   Physical Meaning: Fills the fatal gap of the current DCC model having "no clock", providing a hard constraint for the sheet survival time in the L3 stage.

## 2. Namespace and Anti-Pollution Declarations (R1-R4, S2-S4)

*   Namespace Isolation (R1, S4): The ME prefix is exclusively for the extended constraint set of the v0.2 draft. The use of bare M1–M5 is strictly prohibited in any new derivations (to avoid conflicts with the mass parameter or the external review gate M4).
*   Invalid Subscript Declaration (R4): Any attempt to distinguish semantics via subscripts (such as M_geo, M_phys) is considered a violation upon submission; the full ME prefix must be used.
*   Bare Symbol Legality (S2): In the ledger and derivations, ME1–ME5 are legal bare symbols; if they must appear in the same context as M-class symbols from other systems (such as gate M4), the scope must be explicitly qualified (e.g., Gate:M4 vs Constraint:ME4).
*   Conflict Detection (S3): src/common/symbol_lint.py needs a new scanning rule for the ME namespace to ensure it does not cause cross-reference pollution with existing namespaces such as C, CM, K, L, P, Q, etc.

## 3. Suggested Ledger Registration Entry

### §12.x ME1–ME5: v0.2 Extended Constraint Set
- **Owner**: v0.2 Draft / Theoretical Derivation
- **Namespace**: ME (M-Extended)
- **Predecessor**: C_geo, C_phys, C_info, C_top (v0.1, non-compliant per R4)
- **Scope**: Information topology and evolutionary boundaries of smooth 2D conversion for macroscopic objects
- **Status**: Active (Draft)
- **Hard Check**: symbol_lint.py Rule C extended to the ME namespace

---

*Submitted content, preserved verbatim. Assessment in `reports/reviews/meff_boundary_alt_definitions_review.md`.*
