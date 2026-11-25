# DCC Dimensional Conventions v1 (Dimensional Conventions)

**Version**: v1 (2026-11-21, mandatory after the second D5 review round)
**Status**: **Mandatory**. If any module conflicts with this file, this file takes precedence; a conflict is a defect.
**Machine implementation**: `src/common/conv.py` (single source of truth; modules are prohibited from recopying constants)
**Trigger**: The review found that the same 1 fm slab used mutually incompatible dimensional assignments across four modules, causing X_p to span 28×, the electron reduction factor to span 27×, and the electron partial pressure to span 40× (B2).

---

## 1. The Object Being Described (Unique Geometry)

70 kg, $A_\perp=1\ \mathrm{m^2}$, $\bar m=10$ amu, $Z/A=0.522$, particle number conservation:

| Quantity | Value | Description |
|---|---|---|
| $N_s$ (nuclear column density) | $4.2155\times10^{27}\ \mathrm{m^{-2}}$ | $M/(\bar m A_\perp)$ |
| $N_B$ (baryon column density) | $4.2155\times10^{28}\ \mathrm{m^{-2}}$ | $M/(\mathrm{amu}\,A_\perp)$ |
| Layer thickness $L_z$ | $1.0\ \mathrm{fm}$ | **Inferred from density**: $70\ \mathrm{kg}/(1\ \mathrm{m^2}\times0.026n_{\rm nuc})$ |
| Baryon volume density $n_B$ | $4.2155\times10^{-2}\ \mathrm{fm^{-3}}$ | $N_B/L_z$ |
| Nuclear volume density $n_{\rm nuc}$ | $4.2155\times10^{-3}\ \mathrm{fm^{-3}}$ | $N_s/L_z$ |
| Electron areal density $n_{2D}$ | $2.2005\times10^{-2}\ \mathrm{fm^{-2}}$ | $Z_A N_B$ |

$L_z=1\ \mathrm{fm}$ is a **physical thickness** (inferred from the table above), not a free parameter; but it is also the conversion factor between areal and volume densities, so the **numerical values** of $n_{2D}\,[\mathrm{fm^{-2}}]$ and $n_e\,[\mathrm{fm^{-3}}]$ are **exactly the same** (both 0.0220). This is the direct breeding ground for the factor-of-10 error in v2.

## 2. Dimensional Assignments and Their Rationale

### 2.1 Electrons: Two-Dimensional (Single Subband) — This Is Computable, Not a Convention

The slab thickness $L_z=1$ fm gives a transverse subband spacing

$$E_{\rm sub}=\frac{\pi\hbar c}{L_z}=\frac{\pi\times197.327}{1}=619.9\ \mathrm{MeV}$$

while the frozen-state Fermi energy is $E_F=73.37$ MeV. Since $E_F\ll E_{\rm sub}$, **only the $n=1$ subband is occupied**, and electrons must use the 2D dispersion:

$$n_{2D}=\frac{g k_F^2}{4\pi},\qquad E_F=\hbar c k_F,\qquad u_{2D}=\tfrac23 n_{2D}E_F,\qquad P_{2D}=\tfrac12 u_{2D}$$

If the 3D dispersion ($k_F=(3\pi^2 n)^{1/3}$) were used instead at the same density, $E_F$ would become **171.07 MeV**, **2.33 times** the 2D value. The two cannot be mixed: G0 using 2D and R1-B1 using 3D was the core defect of v2.

### 2.2 Nucleons: 3D by Default, 2D as a Parallel Branch — This Is a Convention and Must Be Declared

There is only one rationale for the 3D assignment: **nucleons are in nuclear bound states or dynamic layers, not hard-wall single-particle states**, so the $E_{\rm sub}$ quantization condition does not apply. This rationale fails in the "dissolved npe matter" branch (no nuclei, no binding), where nucleons should be taken as 2D.

Parallel registration (neither branch may be deleted):

- **HYB (default)**: electrons 2D + nucleons 3D — the electron dimensionality is argued in §2.1; nucleons follow the standard npe EOS;
- **ALL3D**: electrons 3D + nucleons 3D — the historical v2 convention, retained for comparison only, **must not be used as a baseline**;
- **ALL2D**: electrons 2D + nucleons 2D — the fully quantized limit, self-consistent with the 204 MeV subband spacing of R1-B4.

**Residual tension (registered as F-R1B4-4)**: R1-B4's $\Delta E_{12}=430$ MeV and $E_1=204.5$ MeV imply that, if nucleons really were in that potential well, their $E_{F,n}=58$ MeV (3D) would be far below $E_1$ ⇒ they should fall into a single band ⇒ 2D. The 3D nucleon assignment in HYB can only be defended by "non-hard-wall" arguments. That defense fails in the npe branch, so ALL2D must be kept in parallel.

## 3. β-Equilibrium Envelope ($n_B=4.2155\times10^{-2}\ \mathrm{fm^{-3}}$, $L_z=1$ fm)

Produced by `conv.beta_envelope()` (reproducible from the `src/common/conv.py` self-check output):

| Convention | $X_p$ | $\mu_e$ [MeV] | $n_e$ [fm⁻³] | Electron reduction | $P_{\rm tot}(\Sigma)$ [N/m] |
|---|---|---|---|---|---|
| ALL3D (v2 historical) | $1.620\times10^{-3}$ | 24.96 | $6.83\times10^{-5}$ | 322 | $6.48\times10^{16}$ |
| **HYB (default)** | $4.501\times10^{-2}$ | 21.54 | $1.897\times10^{-3}$ | 11.6 | $6.27\times10^{16}$ |
| ALL2D | $4.396\times10^{-3}$ | 6.73 | $1.853\times10^{-4}$ | 119 | $1.84\times10^{16}$ |

**Envelope**: $X_p\in[1.6\times10^{-3},\,4.5\times10^{-2}]$ (28×), $\mu_e\in[6.7,\,25.0]$ MeV (3.7×), electron reduction $\in[11.6,\,322]$ (28×).

Two robust conclusions (still valid outside the envelope):

1. $P_{\rm tot}$ is dominated by **nucleon degeneracy pressure**, being $1.8\text{–}6.5\times10^{16}$ N/m in all three conventions ⇒ the N11 constrained-stress scale $O(10^{16})$ N/m is robust (G0's $8.62\times10^{16}$ is a frozen-electron-gas single-point value, consistent with it but of different origin: the equilibrium state is nucleon-dominated, not electron-dominated);
2. As long as $\mu_e$ is always below the upper or lower bound of any $Q$ threshold, the direction of "electrons are partially captured" is unchanged, but **"reduced by 3×10² times, residual negligible" holds only in ALL3D**; in HYB the residual electrons account for 8.6%, which is not negligible and must be decided by the sector weights of R1-B4.

## 4. Handoff Quantities: Four Routes and One Regression Guard

`n_e` must be computed by any of the following routes; the three must agree to $10^{-12}$:

| Route | Expression | Value [fm⁻³] | Notes |
|---|---|---|---|
| r1 | $Z_A\,n_B$ | $2.2005\times10^{-2}$ | electrons per baryon × baryon density |
| r2 | $n_{2D}/L_z$ | $2.2005\times10^{-2}$ | areal density definition |
| r3 | $Z_{\rm eff}\,n_{\rm nuc}$ | $2.2005\times10^{-2}$ | electrons per nucleus × nuclear density |
| ~~r4~~ | $Z_{\rm eff}\,n_B$ | $2.2005\times10^{-1}$ | **the actual v2 expression, wrong by 10× (= $\bar m$)** |

Rule: $Z_{\rm eff}=5.22$ is the **per-nucleus** electron number and may only be multiplied by the **nuclear** density $n_{\rm nuc}=4.22\times10^{-3}$; multiplying by the baryon density $n_B=4.22\times10^{-2}$ introduces an extra factor $\bar m=10$. `handoff_routes()` explicitly asserts in regression tests that the r4 deviation = $\bar m$, so anyone reverting to that expression immediately gets FAIL.

## 5. Mandatory Rules

1. **No single-point registration**: any conclusion depending on $X_p,\mu_e,n_e,P(\Sigma)$ must be written as an "envelope"; a single-convention value is not allowed.
2. **No cross-module borrowing of dimensionality**: the dimensionality of a quantity may only come from §2 of this file; modules may not establish their own.
3. **No recopying of constants**: always use `from common.conv import ...`; the appearance of literals such as `0.04216`, `0.522`, `2.20e28` in a module is a defect.
4. **Do not treat "self-consistent" as "correct"**: a dual-path recomputation can only prove that two paths share the same convention, not that the convention is right. Dimensional/convention conclusions must provide an envelope or an independent argument (such as the comparison of $E_{\rm sub}$ and $E_F$).
5. Changing the convention requires rerunning downstream calculations and updating the envelope; old results are retained and marked SUPERSEDED, not overwritten.

---

**Machine reproducible**: `python -I src/common/conv.py`
**Referencing modules**: `scale_budget_v3.py`, `beta_equilibrium_v3.py`, `dense_screening_v3.py`
**Related defects**: F-G0-9 (10× handoff), F-R1B1-8 (convention envelope), F-R1B2-5 (screening), F-R1B4-4 (nucleon dimensionality tension)
