# Definition of "Effective Two-Dimensional Reduction" v1

**Version**: v1 (2026-11-21)
**Status**: **Mandatory terminology definition**. This file does not change any numerical conclusion; it only specifies the usage of the term "effective two-dimensional reduction".
**Higher-level basis**: Roadmap v1.4 §1.2 (four cases), §2.6 (conditional statement S11), H5, N7.
**Trigger**: Within the project (including `docs/conventions/dimensional_conventions_v1.md` and `src/analysis/internal_consistency_v1.py`), "geometric thinning" has long been treated as a synonym for "effective two-dimensional reduction", leading to (a) treating $L_z$ as the main variable, (b) conflating the internal occupation scale with the external probe energy, and (c) skipping the carrier-conservation prerequisite check.

> **Pointer to Annex B (2026-11-22).** `docs/specs/effective_2d_definition_v1_annex_B.md` supplies the two numbers
> §1 and §3 require a caller to supply — `H_eff` and `ΔE_z` — **for the deposited object only**, with the model (B),
> the bound (**external only**; the internal bound fails by `2.3e3–2.5e4`), and the one slot that is still empty (no
> subsystem, so per §1 the conditional has no truth value yet). It is an **annex, not an amendment**: nothing above
> changes. A submission proposing to replace the blanket "no claim that the state is two-dimensional" was audited and
> **not adopted** (`docs/specs/eff_dim_claim_A6_PROPOSED.md`, `reports/reviews/eff_dim_claim_A6_v1_audit.md`).
> Note this file's own Trigger clause **(b)** is exactly the error that submission repeated: it compares the internal
> scale (`δ`, a layer spacing) to an external probe energy and calls the result a property of the system.

---

## 1. Definition

**Effective two-dimensional reduction is not a property, but a four-slot conditional implication.** It has a truth value only when all four slots are filled:

$$\Big(\text{model}\Big)\wedge\Big(\text{subsystem}\Big)\wedge\Big(E_{\rm occ}<\Delta E_z\Big)\wedge\Big(E_{\rm probe}<\Delta E_z\Big)\ \Longrightarrow\ \text{for that probe, the }z\text{ degree of freedom cannot be excited}$$

| Slot | Value | Consequence if missing |
|---|---|---|
| **Model** | B (deep finite-thickness potential well) / C (compactification) | The origin of $\Delta E_z$ cannot be determined; the proposition has no truth value |
| **Subsystem** | electrons / nucleons / collective modes (phonons, plasmons) | "2D" has no referent; different subsystems can give opposite conclusions |
| **Occupation scale** $E_{\rm occ}$ | $\max(E_F,\,k_BT)$ | the system itself excites the $z$ degree of freedom ⇒ not a 2D system |
| **Probe energy** $E_{\rm probe}$ | energy used for the observation (visible light 2.5 eV, X-rays, …) | cannot judge "whether it looks 2D" |

The original text of Roadmap §2.6 is the colloquial form of this expression:

> Under Model C (or the deep-binding limit of Model B), if $E_{\rm probe}\ll\Delta E_{\rm KK,1}$ (or the first bound excitation gap) holds,
> then a low-energy observer cannot excite the $z$-direction degree of freedom, and the system effectively appears 2D to that observer.

## 2. Three Negations (Getting These Wrong Conflicts with §1.2/§2.6)

1. **Not geometric contraction.** The first line of §1.2 states explicitly: a decrease in $B(t,x)$ is "anisotropic geometric contraction", **"is it equivalent to macroscopic two-dimensional reduction: No"**. $B\to0$ alone does not imply two-dimensional reduction.
2. **Not small thickness.** Thickness is only one parameter determining $\Delta E_z=\pi\hbar c/L_z$ under Model B. Under Model C an effective $2+1$-dimensional theory can be obtained without thinning, but **this does not automatically mean a macroscopic object has been flattened** (§1.2, third line).
3. **Not the disappearance of degrees of freedom.** §2.6 explicitly prohibits "calling the reduction in the number of coordinate modes the disappearance of physical degrees of freedom"; if one claims "information is retained in the fiber coordinates", one cannot simultaneously claim "that direction has disappeared" — the two are logically mutually exclusive.

## 3. The Two Bounds Must Be Written Separately (The Core Correction of This File)

$\Delta E_z$ must be compared with **two completely different energies**, which give opposite $L_z$ dependencies:

| Bound | Condition | Physical meaning | Requirement on $L_z$ ($\Delta E_z=\pi\hbar c/L_z$) |
|---|---|---|---|
| **Internal self-consistency bound** | $E_F(T)<\Delta E_z$ | the system **itself** does not excite $z$ ⇒ it **is** a 2D system | tight: $L_z\lesssim 2$ fm (since $E_F\propto\sqrt{n_eL_z}$, the ratio $\propto L_z^{-3/2}$) |
| **External resolvability bound** | $E_{\rm probe}<\Delta E_z$ | the probe **cannot see** $z$ ⇒ it **looks** 2D | loose: under visible light $L_z\ll 250$ nm, wider by $10^5$× |

**It is forbidden** to combine the two into a single number. Any expression of the form "effective 2D domain $E\le X$ MeV" must specify which bound this $X$ belongs to.

- If the internal bound fails ⇒ the conclusion fails for **all** probes (monotonicity), so the NO-GO direction is safe;
- If the internal bound holds but the external bound is used for a specific observation ⇒ one must return to $E_{\rm probe}$ and must not continue using $E_F$.

## 4. Carrier Conservation Prerequisite Check (N7, added in §2.6 v1.4)

First ask "are the carriers still present, and is their number conserved?" before discussing their two-dimensionality:

> Under $H_2+H_3$, if $\mu_e$ exceeds the electron-capture threshold of the nuclide hosting the carriers, then the "carriers" themselves are removed,
> and any low-energy effective description based on the electron gas **loses its object**.

This is not "an insufficient gap" but a **referential failure**. Therefore "electrons are 2D" must carry a state label:

| State | $n_e$ | $E_F$ | Are electrons still 2D carriers |
|---|---|---|---|
| Frozen state ($Z/A=0.522$) | $2.20\times10^{-2}\ \mathrm{fm^{-2}}$ | 73.37 MeV | gap sufficient ($73\ll620$), but **this state is unstable**, $\mu_e>Q$ ⇒ it will neutronize |
| HYB equilibrium state | $1.90\times10^{-3}\ \mathrm{fm^{-3}}$ | 21.54 MeV | gap sufficient; but the carrier number **has changed by 11.6×**, so the low-energy theory must be recomputed |
| ALL2D equilibrium state | $1.85\times10^{-4}\ \mathrm{fm^{-3}}$ | 6.73 MeV | same as above |

## 5. Boundary: $L_z$ Approaches but Never Reaches (Clarified 2026-11-21, Consistent with §2.8 Item 6)

**Effective two-dimensionality corresponds to $L_z$ being extremely small but nonzero; strictly $L_z=0$ is not "two-dimensional reduction completed" but "the definition of space fails".**

Three equivalent reasons, all consequences of known physics/geometry:

1. **Physical processes can only approach.** In Lorentz contraction, an object with rest mass can only approach the speed of light indefinitely, never reaching it; hence the longitudinal length can only approach 0, never equal 0. The same applies to compactification — $L_z\to0$ is a limiting process, and $L_z=0$ is not physically reachable.
2. **$L_z=0$ is a geometric singularity.** The metric in that direction degenerates completely, the distance rule fails there, and it is no longer a legitimate physical space (same origin as the Geroch prohibition: a singularity or CTC is required).
3. **The framework itself diverges.** In the model, $p_z^{\min}=\pi\hbar c/L_z$; $L_z\to0$ makes all KK mode energies diverge, the distinction between zero and excited modes fails, and the low-energy effective theory loses its object.

Therefore the correct physical picture of "smooth two-dimensional reduction" is:

> $L_z$ is compressed to **far below the observation scale and far below the characteristic scale of the relevant physical processes**, so that all excitations in the z direction are frozen at that scale and the system can only occupy the zero mode at finite energy — effectively appearing 2D, while $L_z$ remains a positive number.

**Scale hierarchy table (each entry is an "appearance", not "geometric dimensional reduction"):**

| $L_z$ scale | Physical appearance | Dimensionality |
|---|---|---|
| Macroscopic (m/km) | z degree of freedom fully available | 3D |
| Sub-millimeter | z begins to be constrained | 3D (constrained) |
| Atomic (Å) | electronic states quantized in the z direction | 2D material |
| Planck ($10^{-35}$ m) | z degree of freedom frozen | effectively 2D |
| $=0$ | metric degenerates, framework fails | undefined |

**Key distinction**: the Planck scale is already the smallest physically conceivable scale, but it is still **not zero**.

**Correspondence with quantum-gravity "two-dimensionalization"**: the spectral dimension $4\to2$ in CDT and $D_{\rm eff}\to2$ at Padmanabhan's zero-point length $\ell_0$ both refer to **effective dimensionality** (spacetime behaves as if 2D), not "the length of some direction equals 0". Spectral dimension is diffusion behavior at the probing scale, not geometric thickness.

**Two direct implications for this project:**

1. **Frozen-state/equilibrium-state registration is unaffected**: in this project $L_z$ is an external parameter set to 1 fm (inferred from density), and $p_z^{\min}$ is very large but finite — this is a legitimate branch, not the illegal $L_z=0$ limit.
2. **Optical conclusion revised**: the previous round's "zero-thickness perfect reflector ⇒ no shading/no highlights/no parallax/no intrinsic color" is a **degenerate limit** and physically unreachable; the physical branch is an "ultrathin film with $L_z$ extremely small but nonzero", whose optics are stated by the sheet conductivity $\sigma_s(\omega)$ rather than by a "zero-thickness mirror". Therefore: both the mirror direction and the transparent direction are **equally** forbidden until a self-consistent $\sigma_s(\omega)$ is completed (consistent with §3.7 and §6.4); a "zero-thickness mirror" **does not exist** as a legitimate object of description, because its corresponding parameter value is physically unreachable.

## 6. List of Known Misuses (Each Mapped to an Actual Statement That Occurred)

| Misuse | Correct statement | Source |
|---|---|---|
| "2D reduction = so thin that particles can only move in-plane" | This is a **phenomenological consequence** of the deep-binding limit of Model B, not a definition | verbal explanation in this round |
| "To be 2D one must compress to 1 fm" | $L_z=1$ fm is a density-**inferred value** from $70\ \mathrm{kg}/1\ \mathrm{m^2}$, an input rather than a requirement of 2D reduction | `dimensional_conventions_v1.md` §1 |
| "the feasible $L_z$ window is only 1.19×" | holds only for the **internal self-consistency bound**; under the external resolvability bound the window is $10^5$× wide | `internal_consistency_v1.py` K1 |
| "effective 2D domain $E_{\rm probe}\le43$ MeV, does it cover the occupied states" | uses the name $E_{\rm probe}$ to judge occupied states, mixing the two bounds; should be split into 43 MeV (external) and $E_1=204.5$ MeV (internal) | `runs/R1B/r1b234_v3_results.txt` L43–44 |
| "electrons are 2D (because $E_F\ll E_{\rm sub}$)" without a state label | must specify frozen/equilibrium state and whether the carrier number is conserved | `dimensional_conventions_v1.md` §2.1 |
| "zero-thickness perfect reflector ⇒ no shading/no highlights/no parallax" | this is the **degenerate limit** of $L_z=0$, physically unreachable; the physical branch is an **ultrathin film** with $L_z$ extremely small but nonzero, whose optics are stated by $\sigma_s(\omega)$ | verbal conclusion from the previous round |

## 7. Mandatory Rules

1. When using the term "effectively 2D", all four items **model + subsystem + occupation scale + probe energy** must be given; any missing item is a defect.
2. It is forbidden to use "effectively 2D" for an electron gas before performing the N7 carrier check.
3. It is forbidden to substitute the external resolvability bound for the internal self-consistency bound in order to support the claim "the system is 2D".
4. **It is forbidden to treat the $L_z\to0$ degenerate limit as a physical state**; any "zero-thickness" conclusion must explicitly state that its parameter value is physically unreachable, or be reformulated as an "extremely small but nonzero ultrathin film".
5. This file does not change any numerical value of G0P-003; the conclusions of K1 and R1-B4 still hold after being qualified according to §6.


---

## 8. Erratum E1 (round 58) — the `N7` threshold is host-specific; §4's table is a frozen-state table

**Nothing above is edited.** `RQ-08` re-evaluated the carrier check and its product is
`runs/R3/n7_recheck_results.txt` (instrument `src/r3/n7_recheck.py`, pre-registration
`runs/R3/n7_recheck_registration.md`).

- **E1** §4's rule — *"if `μ_e` exceeds the electron-capture threshold of the nuclide hosting the
  carriers, the carriers are removed"* — is correct for the frozen object and must not be transferred
  to a β-equilibrated state by the `μ_e` number alone. At the frozen baseline (`μ_e = 73.373 MeV`,
  kinetic `ħck_F`) all six registered captures are open, with a `59.49–72.08 MeV` margin; that is the
  comparison the rule was written for. At the solved `HYB` state the *vacuum* comparison still says
  `6/6` open (`μ_kin = 21.0335 MeV`, margin over `C12` = `7.664 MeV`), but the host is now a free
  proton whose daughter neutron sea is already filled to `E_F,n`. The host-specific kinetic threshold
  is therefore `Q_eff,p = 0.782 + (E_F,n − E_F,p) = 21.0335 MeV`, **equal** to `μ_kin` at equilibrium
  (`β` residual `−3.55e−15`). The antecedent is false at `T = 0` (equality, not excess); the state
  carries `n_e = 1.897e−3 fm⁻²` and `RQ-05` measured the free fraction to be `1.000`. A one-way
  removal rule applied to the equilibrium product of that same capture is circular.
- **E2** §4's table column headed `E_F` is not one quantity in three states. `73.37 MeV` is the frozen
  2D kinetic `ħck_F`; `21.54` and `6.73 MeV` are `conv.beta_eq` outputs occupying the *total*
  chemical-potential slot (`conv.eos_e_3D` returns `√(p²+m_e²)`, `conv.eos_e_2D` returns `ħck`), and
  `ALL3D`'s `24.96` is total while the `Q` table is kinetic. Normalizing every `β`-equilibrium output
  as `μ_kin = μ_e − 0.511 MeV` puts them on the capture table's scale; the `0.511 MeV` shift changes
  no `ALL2D` classification (distances to `N14` and `O16` are `0.342` and `0.898 MeV`). The table's
  `"carrier number changed by 11.6×"` compares an areal frozen density with a bulk solved density;
  the numerical factor is valid only at the registered `L_z = 1 fm` where the two units coincide.
- **E3** §7 rule 2 stands, with a corrected check: the prerequisite is the **host-specific** threshold
  (`Q_eff`, Pauli-shifted), not the vacuum `Q` of a nuclide the solved state no longer contains. This
  erratum does **not** pass `G5′`: the other three slots of §1's conditional, and `G4`, remain open.

---

## 9. Erratum E4 (round 65) — §5 reason 2 is not a universal geometric statement

**Nothing above is edited.** `runs/P1/phase1c_repricing_results.txt` (pre-registration
`runs/P1/phase1c_repricing_registration.md`, generated by
`src/p1_symbolic/phase1c_repricing.py --write`) audited the consequence of
`runs/P1/phase1b_singularity_results.txt`. The product was emitted before this append; the input
SHA-256 quoted there refers to the pre-append state of this file.

- **E4** §5 calls its three reasons “equivalent” and states reason 2 as *“$L_z=0$ is a geometric
  singularity.”* The flat Kasner control in Phase 1b (`f=t`, `K=R=E_ab=0`, `g_zz=t²→0`) is a
  coordinate-independent counterexample to that universal form: metric degeneration of the `z`
  circle need not be a curvature singularity. The generic contracting family with `f_tt≠0` still
  diverges (`K∼4p²(p−1)²t⁻⁴`), so the qualified statement is: **`L_z→0` is singular for the generic
  contracting sector, not for every geometry.** Reasons 1 and 3 are not tested by Phase 1b and are
  not repaired, withdrawn, or re-derived here. The dimensional mismatch in reason 3's
  `p_z^min=πħc/L_z` remains recorded in `hard_sf_effective_2d_route_candidate_v2_1.md` §1.2.
- **Scope** This is an observation-class erratum. It moves no gate, terminal class, threshold,
  `V`/`Φ` price, queue item, or route mark, and it does not establish that `L_z=0` is a physical
  object. The ladder's §6 exclusion of a zero-thickness perfect mirror stands.
