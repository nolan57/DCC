# G-73-01 — Pre-registration (frozen before instrument, before products)

**Directive**: G-73-01, round 73. **Written**: 2026-11-24T03:52:00Z.
**Instruments**: `src/g73/verify_g73_numbers.py` (arithmetic), no symbolic engine required.
**Products**: `runs/G-73-01/adiabaticity_provenance_analysis.md`,
`runs/G-73-01/b3_numerical_analysis.md`.
**PROVENANCE**: NEITHER. This round re-reads archived constants and archived sentences. It derives no
new physics and asserts none.

## 0. What this round is allowed to change

Nothing existing. G-73-01 §Prohibitions forbids modifying records, moving gates/thresholds/prices/RQ
entries, proving or disproving adiabaticity, judging engineering feasibility, and introducing new
physical assumptions. Every clause below is a **read**, not an edit: no file outside `runs/G-73-01/`
and `src/g73/` is written, except the ledger, the queue JSON's cursor and board note, and the memory
log.

## 1. Sources that will be read (declared before reading)

| tag | file | what is taken from it |
|---|---|---|
| `S1` | `Macro3D_to_2D_Smooth_Reduction_Roadmap.md` | D1 named as a module; "adiabatic criterion (complete)" |
| `S2` | `DCC_Macro_2D_Execution_Spec_v1.2.md` §0.2, §2.1, §2.2 | D1 status row; η_rough; ε_mn; the β_C>1 deletion |
| `S3` | `DCC_P3_Effective_Theory_v1.md` §2 | m_eff = \|p_z\|/C(t); \|ṁ_eff\|/m_eff² = \|β_C\|C/(\|p_z\|t) |
| `S4` | `DCC_P3_C5_Scan_Report_v1.md` §2.1, §7.2, §7.3 | η(t) monotonicity; withdrawal of "critical = 1"; rerun condition |
| `S5` | `docs/decisions/front_sweep_v1.md` §2, §2.1 | "smoothness holds at the front, fails between layers"; the two timescales |
| `S6` | `docs/decisions/kinematic_vs_dynamic_unfolding_v1.md` §7, §12 | R/(2δ)=4.19e8; the WORKING-HYPOTHESIS promotion and its honest note |
| `S7` | `docs/specs/surface_conductivity_v1.md` §4 | branches A/B/C/D |
| `S8` | `docs/decisions/scifi_boundary_v1.md` §3, §4 | the 3–5 ns lifetime; the {E,S,W} corners |
| `S9` | `docs/decisions/G0p_seven_row_verdict_v3.md` §2 | N_s, n_2D, E_F, u_2D, P_2D, c_s, v_∞, t_rip(1 m) |
| `S10` | `runs/RR-DT/constraint_relaxation_record.md` B3, B4 | the two B3 figures as emitted; the B4 corner |
| `S11` | `docs/decisions/demo_object_ruling_v1.md` | H = 1.74 m, δ = 0.215 nm |
| `S12` | `docs/specs/R1_B1_Microscopic_Matter_Model_v1.0.md` | n₀ = 0.16 fm⁻³ (MEASURED, saturation) |

## 2. Constants and their declared provenance

| symbol | value | source | status |
|---|---|---|---|
| `c` | 2.99792458e8 m/s | defined | exact |
| `G` | 6.67430e-11 | CODATA | exact for this round |
| `ħc` | 197.3269804 MeV·fm | CODATA | exact for this round |
| `P_2D` | 8.6227e16 N/m | `S9` | archived |
| `Σ` | 70 kg/m² | `S9` | archived |
| `t_rip` | 8.2553e-9 s | `S6`, `S5` | archived |
| `L_z` | 1.0 fm | `S9`, `S10` | archived normalisation |
| `E_F` | 73.37 MeV | `S9` | archived |
| `E_F`(ALL2D) | 6.2221 MeV | `S10` B2 | archived |
| `ε_relief` | 1.7e-4 | `S10` B3 | archived |
| `λ_relief` | 1.0e-3 m | `S10` B3 | archived |
| `ρ_nuc` | `0.16 × 939.565 MeV / fm³ = 2.4086e34 J/m³` | `S12` + `m_N c²` | **convention declared here** (rest-mass normalisation; a binding-corrected value differs by 1.8 % and does not move the 1.3e12) |
| `δ_plate` | 0.215 nm | `S11` | archived |
| `R_body` | **not declared in the record** | — | to be reverse-engineered, §4 |
| `c_s`(elastic) | **not declared in the record** | — | to be reverse-engineered, §4 |

The two rows marked "not declared" are the reason this registration exists: §4 fixes how they will be
inferred *before* the products are allowed to use them.

## 2.1 External reference magnitudes (added pre-run; NOT record values)

G-73-01 Task 2.3 asks what energy densities known physics and current technology produce. Those
numbers are not in the record, so they are declared here as **comparison anchors only** — formulae
stated so each is checkable, none used as a premise for any DCC claim.

| id | anchor | formula | declared value |
|---|---|---|---|
| `X1` | Casimir, 1 µm gap | `−π²ħc/(720 d⁴)`, `d=1e-6 m` | −4.3338e-4 J/m³ |
| `X2` | Casimir, 1 nm gap | same, `d=1e-9 m` | −4.3338e8 J/m³ |
| `X3` | focused laser, `1e22 W/cm²` | `u = I/c` | 3.3356e17 J/m³ |
| `X4` | neutron-star core, `5 n₀` | `5 ρ_nuc` | 1.2043e35 J/m³ |
| `X5` | quark-gluon plasma, `12 GeV/fm³` | `12 × 1.602176634e32` | 1.9226e33 J/m³ |
| `X6` | Planck density | `c⁵/(ħG²)·c²` | 4.6329e113 J/m³ |

## 2.2 Declared ratios against the anchors (all `log10(anchor / ρ_req)` or its inverse)

| id | quantity | declared value |
|---|---|---|
| `N33` | orders by which `ρ_req` exceeds the 1 µm Casimir magnitude (`X1`) | 49.873 |
| `N34` | same, 1 nm gap (`X2`) | 37.873 |
| `N35` | same, focused laser (`X3`) | 28.986 |
| `N36` | same, neutron-star core (`X4`) | 11.429 |
| `N37` | same, QGP (`X5`) | 13.226 |
| `N38` | orders from `ρ_req` up to Planck (`X6`) | 67.156 |
| `N39` | `(c⁴/8πG)/ρ_nuc` — the cost of 1 m⁻² of extrinsic curvature in nuclear densities | 1.9993e8 |
| `N40` | `Σ·πR²` at `R = 0.180 m` | 7.125 kg |
| `N41` | aspect ratio before growth, `2δ/(2R)` | 1.194e-9 |

`N39` is the ratio that makes the relief number intelligible and is quoted in both products: the
conversion factor between extrinsic curvature and energy density is large, so a geometrically gentle
modulation is energetically enormous.



## 3. Declared arithmetic (every number either product may quote)

Tolerance: relative 5e-4 unless stated. Any failure aborts emission.

| id | quantity | expression | declared value |
|---|---|---|---|
| N01 | `a = P/Σ` | 8.6227e16/70 | 1.2318e15 m/s² |
| N02 | `ΔL = ½at_rip²` | N01·(8.2553e-9)²/2 | 4.1974e-2 m |
| N03 | `v/c` at `t_rip` | N01·t_rip/c | 3.392e-2 |
| N04 | `γ−1` at `t_rip` | 1/√(1−N03²)−1 | 5.76e-4 |
| N05 | `ΔL/L_z` | N02/1e-15 | 4.197e13 |
| N06 | `ΔE_z(1 fm)` | πħc/1 | 619.921 MeV |
| N07 | `L_z,max` frozen | πħc/E_F | 8.4492 fm |
| N08 | `t_w` to `L_z,max` | √(2(N07−1)fm/N01) | 3.4778e-15 s |
| N09 | `t_w/t_rip` | N08/8.2553e-9 | 4.2127e-7 |
| N10 | `L_z,max` ALL2D | πħc/6.2221 | 99.632 fm |
| N11 | `t_w` ALL2D / fraction | √(2·98.632fm/N01) | 1.2655e-14 s / 1.5329e-6 |
| N12 | `v_∞ t_rip` | 4.9635e7·t_rip | 0.4098 m |
| N13 | `c_s t_rip` | 2.1199e8·t_rip | 1.7501 m |
| N14 | `c⁴/(8πG)` | — | 4.81545e42 Pa·m² |
| N15 | `k²ε` | (2π/1e-3)²·1.7e-4 | 6.7113e3 m⁻² |
| N16 | `ρ_req` | N14·N15 | 3.23181e46 J/m³ |
| N17 | `ρ_req` in MeV/fm³ | N16/1.602176634e32 | 2.01714e14 |
| N18 | `ρ_nuc` | §2 | 2.4086e34 J/m³ |
| N19 | `ρ_req/ρ_nuc` | N16/N18 | 1.3418e12 |
| N20 | `ρ_req^(1/4)` | (N16·(ħc)³)^¼ | 198.4 GeV |
| N21 | `T_rad` at `g=86.25` | (30N16(ħc)³/(π²g))^¼ | 86.0 GeV |
| N22 | `λ` for `ρ=ρ_nuc` | 1e-3·√N19 | 1158 m |
| N23 | curvature radius | 1/√N15 | 1.221e-2 m |
| N24 | aspect ratio after growth | N02/(2·0.18 m) | 0.1166 |
| N25 | `c_s` implied by 2δ/c_s=4.30e-13 s | 2·0.215e-9/4.30e-13 | 1.000e3 m/s |
| N26 | `R` implied by R/c_s=1.80e-4 s | N25·1.80e-4 | 0.180 m |
| N27 | `2δ/c_s` at `c/√2` | 2·0.215e-9/2.1199e8 | 2.0284e-18 s |
| N28 | `R/c_s` at `c/√2` | 0.180/2.1199e8 | 8.4912e-10 s |
| N29 | `t_rip` from `√2·1.75/c` | — | 8.2553e-9 s |
| N30 | `t` to reach 0.1 nm | √(2·1e-10/N01) | 4.030e-13 s |
| N31 | `t` to reach 1 µm / 1 mm | √(2·1e-6/N01) / √(2·1e-3/N01) | 4.0294e-11 s / 1.2738e-9 s |
| N32 | `η(t)` exponent for `β_C<0` | `β_C−1` | monotone decreasing; `η→0` |

`N32` is a property of `S4`'s printed formula, not a new derivation: `η ∝ (t/t_0)^{β_C−1}`, and
`β_C−1 < −1 < 0`.

## 3.1 Declared set closure (added pre-run, second amendment)

Two ways a number enters the products, both now closed:

**(a) Instrument-printed derived ratios.** Fractions of `t_rip`, growth-ladder times, estimate spreads,
decade counts and the relief-scaling series are declared by their appearance in
`runs/G-73-01/g73_01_verification.txt` Sections C–E. That report is part of the declared set: it is
emitted by the same instrument from the same constants, and its hash is recorded with the products.
No product may quote a derived ratio that the instrument does not print.

**(b) Individually declared values.** Everything else, including quantities archived in the record but
not previously tabulated here:

| id | quantity | expression | declared value |
|---|---|---|---|
| `N42` | `u_2D` | `G0′ §2` (archived) | 1.7245e17 J/m² |
| `N43` | radiation density, `kT=160 GeV`, `g_*=106.75` | `(π²/30)g T⁴/(ħc)³` | 4.797e47 J/m³ |
| `N44` | `log10(N43/ρ_req)` — how far `ρ_req` sits **below** the 160 GeV bath | — | 1.172 |
| `N45` | `λ` at which the relief costs a neutron-star-core density | `1e-3·√(ρ_req/1.2043e35)` | 518 m |
| `N46` | `B` at `L_z = 1 fm` under v1.4's convention `B ≡ L_z/0.07 m` | `1e-15/0.07` | 1.4286e-14 |
| `N47` | decades by which `N46` lies outside v1.4's window `B ≳ 2.4e-9` | `log10(2.4e-9/N46)` | 5.2253 |
| `N48` | `2δ` | `2 × 0.215 nm` | 4.30e-10 m |
| `N49` | `a` in gravities | `N01/9.80665` | 1.256e14 g |

`N46`/`N47` are the only numbers in either product that depend on a *convention from a Layer-B document*
rather than from the record's constants, and both are quoted solely inside Product 1's open question
`Q4`. They support no claim.

## 4. The reverse-engineering rule (fixed before use)



`S5`/`S6` print two times but only two lengths (`δ = 0.215 nm` from `S11`, `R/(2δ) = 4.19e8`). Read as
a pair of equations in the two unknowns `(c_s, R)`:

```
2δ/c_s = 4.30e-13 s      (thickness response)
R/c_s  = 1.80e-4  s      (in-plane response)
```

Solved: `c_s = 1.000e3 m/s`, `R = 0.180 m`, and `R/(2δ) = 4.186e8`, reproducing the printed `4.19e8`
to 0.1 %. **The reconstruction is accepted only if that consistency check passes** (`CK1`). If it
fails, the products may not name `c_s` or `R` at all and must report the timescales as unreconstructible.

Two consequences are then *arithmetic*, and both will be reported whether or not they are convenient:
`c_s = 1.000e3 m/s` is 5.33 decades below `S9`'s `c_s = c/√2 = 2.1199e8 m/s`, which appears under the
same symbol; and at `c/√2` both response times fall *before* `t_rip` (`N27`, `N28`), which reverses the
word "brackets" in `S6` §7.

## 5. Structure and claim guards

Both products must carry `Date:`, `Directive: G-73-01`, a `SUMMARY` block and an `OPEN QUESTIONS`
block, and every subsection must present `Finding` / `Evidence` / `Assessment`. The instrument checks
these strings (`CK2`–`CK5`) and rejects, anywhere in either product, the claim tokens
`"survives"`, `"is visible"`, `"route adopted"`, `"feasible"`, `"proves"`, `"disproves"` used about the
object or the hypothesis (`CK6`). Descriptive uses inside quoted archived text are exempted by the
marker convention **defined here**: a line whose first non-space characters are `> ` is a citation of
archived text, and claim tokens on such a line are attributed to the record, not to this round. No
other exemption exists, and the products may not use `> ` for their own prose.

## 5.1 Pre-run corrections (disclosed before the instrument was executed)

Two corrections, both made while no product and no instrument output existed:

1. `N31` was first declared as `1.2739e-11 s / 1.2739e-9 s`. That is wrong by the factor
   `√(10)` in the first entry: the growth law is `t ∝ √ΔL`, so `0.1 nm → 1 µm` is a factor `10^4` in
   length and `10^2` in time, not `10`. Corrected to `4.0294e-11 s / 1.2738e-9 s`. The second entry
   stood.
2. §5 referred to "a `QUOTE` marker convention declared here" without defining it. Defined above as
   the blockquote prefix `> `. The definition was added before the guard existed, so the guard cannot
   have been shaped to fit the products.
3. §2 and §3 as first written contained only record values, so Task 2.3's question ("what do lasers,
   accelerators and known processes produce?") had no declared numbers to answer it. §2.1 and §2.2
   were added, with formulae, **before any product was written**. These are external comparison
   anchors, marked as such, and no DCC claim rests on them: they appear in Product 2 only as
   `log10` ratios against `ρ_req`.
4. §3 as first written did not close the declared set. Two classes of number appeared in the products
   that it did not cover: derived ratios (fractions of `t_rip`, growth-ladder times, estimate spreads)
   and eight archived-but-untabulated quantities. §3.1 was added to close both, with the instrument's
   own Sections C–E named as the declaration of record for the first class. Added after the products
   were drafted and before this file, any hash, or the ledger entry was issued.
5. **One declaration error and one instrument bug, both caught by the instrument, both fixed before
   emission.** `N47` was first declared `5.221`; the correct value is `5.2253`, and the declaration was
   corrected. Separately, the `N43`/`N44` formula used `160.0 × 1.602e-13` J, i.e. MeV where GeV was
   meant, returning `4.799e35 J/m³` against the declared `4.797e47`. In that case the **declaration was
   right and the code was wrong**; the formula was corrected to `160.0e3 × MEV_J`. The failure was
   visible only because the declared value was frozen first — which is the reason §3 exists.

## 6. Disclosure policy

If the instrument fails a declared value, the *declaration* is corrected with a visible note and the
reason, before emission — never the computed value to match the prose. If a check is discovered to be
testing the wrong object after emission, it is disclosed in the product's final section rather than
removed.

## 7. Result-class ceiling

The maximum admissible claim is: *a functional map of adiabaticity's role, a provenance record of its
two introduction points, an arithmetic characterisation of two B3 figures, and the identification of
undeclared parameters in the timescale measurement.* No survival, visibility, feasibility, route, gate,
threshold, price, terminal-class or RQ claim is made or implied.
