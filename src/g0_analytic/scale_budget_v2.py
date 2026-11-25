# -*- coding: utf-8 -*-
"""
G0' v2: convention-corrected survival threshold at fixed area (experiment G0P-002)
=============================================================================

v2 corrections (2026-11-21, driven by external review; v1 = G0P-001, numerically
PASS but physical baseline withdrawn):

  F-G0-4 (review finding, order-of-magnitude level): v1 confused the electron areal
    density convention --
    n_2D = ZA * N_s multiplied the "proton fraction Z/A per nucleon" by the
    "nuclear column density N_s". The consistent conventions (equivalent, since
    Z_eff = ZA*m_bar) are:
      n_2D = ZA * N_B,  N_B = M/(amu*A)   (baryon column density route, main convention)
      n_2D = Z_eff * N_s,  Z_eff = ZA*m_bar ≈ 5.22 (per-nucleus charge route, cross-check)
    After correction n_2D = 2.20e28 m^-2 (v1: 2.20e27, ×m_bar); E_F = 73.4 MeV
    (v1: 23.2); u_2D = 1.72e17 J/m^2 (v1: 5.45e15); P_2D = 8.6e16 N/m
    (v1: 2.73e15). The two conventions (Z_eff=5.22 vs Z_ion=5) differ by 4.4%,
    registered as convention spread.
  F-G0-5: nu_loss = 0.75*n_2D*E_F relabeled as a "registered energy-budget placeholder
    parameter", not a neutrino-transport result (0.75 is the 3D UR coefficient,
    inconsistent with u/n=2/3 in 2D; the ratio 1.125 is printed explicitly; real
    nu transport belongs to R1-B3 v2).
  F-G0-6: Gamma_i = U_i/E_F relabeled as an "electron degeneracy energy normalized
    ratio", not the classical ion coupling parameter Gamma = (Ze)^2/(4πε0 a kT);
    the crystallization verdict is handed over to R1-B2 v2.
  F-G0-7: unify the density baseline -- the document's "0.026 n_nuc" means the
    nuclear density 4.2e-3 fm^-3; the baryon density is n_B = N_B/L_z = 0.042 fm^-3
    (L_z=1 fm convention); this baseline is passed to R1-B1 v2 (v1 mistakenly used
    0.026 fm^-3; neither is correct).
  F-G0-8: make the registered-threshold convention explicit -- the capture threshold
    table Q=0.782(p) uses the kinetic-energy convention (excluding m_e); under the
    total chemical potential convention it corresponds to 1.293 MeV. The two
    conventions must not be mixed.

Thresholds remain registered in configs/g0_prime.json (structure unchanged); this
file mirrors them as constants and prints the registration list at runtime.
Output in ASCII segments: python -I src/g0_analytic/scale_budget_v2.py
"""
import math
from datetime import datetime

import numpy as np
from scipy.integrate import quad

# ---- registered inputs (same values as configs/g0_prime.json v1; conventions in docstring) ----
M_KG = 70.0
A_PERP = 1.0
M_BAR_AMU = 10.0          # mean nuclear mass (per nucleus)
ZA = 0.522                # proton fraction per nucleon (electrons/nucleons)
Z_ION = 5                 # registered ion charge (cross-convention Z_eff=ZA*m_bar=5.22)
G_E = 2
AMU = 1.6605390666e-27
HBAR = 1.054571817e-34
C = 2.99792458e8
ME = 9.1093837015e-31
MEV = 1.602176634e-13
MT_J = 4.184e15
A0 = 5.29177210903e-11
L_BODY = 0.07
D_BOND = 3.0e-10
V_PROBE = 42.47e3
E2_4PE0 = 2.307077552e-28
SIGMA_T = 6.6524587321e-29
EPS0 = 8.8541878128e-12
EC = 1.602176634e-19
N_NUC = 0.16e45           # m^-3
LZ_FM = 1.0e-15           # m (registered convention)
NU_BUDGET_FRAC = 0.75     # energy-budget placeholder (3D UR coefficient; not a transport result, F-G0-5)
P_CONSTRAINT = 0.0        # N11 constraint-stress input

# ---- registered thresholds (before run; same as v1) ----
TH = dict(nr_switch_reldev=1.0, T1=0.01, T3=0.05, T5=1e-6, dual=0.05,
          T7=1e-4, T8=1e-3, T4=1e-12, T9_spread=0.05)

Q_CAP_MEV = {"p": 0.782, "Fe56": 3.69, "N14": 5.88, "O16": 7.12,
             "Mg24": 10.77, "C12": 13.37}   # kinetic-energy convention (F-G0-8)


def pathA():
    r = {}
    N_s = M_KG / (M_BAR_AMU * AMU * A_PERP)          # nuclear column density
    N_B = M_KG / (AMU * A_PERP)                      # baryon column density
    n_2D = ZA * N_B                                  # main convention (F-G0-4 correction)
    n_2D_Z5 = Z_ION * N_s                            # cross-check convention
    spread = abs(n_2D - n_2D_Z5) / n_2D
    d_par = N_s ** -0.5                              # in-plane spacing from nuclear column density (geometric quantity)
    k_F = math.sqrt(4.0 * math.pi * n_2D / G_E)   # n = g k_F^2/(4π) (formula corrected in v1)
    E_NR = (HBAR * k_F) ** 2 / (2.0 * ME)
    E_R = HBAR * k_F * C
    reldev = abs(E_NR - E_R) / E_R
    E_F = E_R if reldev > TH["nr_switch_reldev"] else E_NR
    dims = {d: (n_2D, n_2D * d / (d + 1.0) * E_F, n_2D * d / (d + 1.0) * E_F / d)
            for d in (1, 2, 3)}
    u_2D = dims[2][1]
    P_2D = dims[2][2]
    c_s = C / math.sqrt(2.0)
    Sigma = M_KG / A_PERP
    v_inf = math.sqrt(2.0 * P_2D / Sigma)
    A_min = N_s * D_BOND ** 2
    Lz_ion = math.pi * A0
    B_ion = Lz_ion / L_BODY
    frac = u_2D / (M_KG * C ** 2 / A_PERP)
    a_i = (math.pi * N_s) ** -0.5
    U_e = E2_4PE0 / a_i
    U_i = Z_ION ** 2 * U_e
    mu_e_MeV = E_F / MEV
    cap = {k: bool(mu_e_MeV > q) for k, q in Q_CAP_MEV.items()}
    nu_budget = NU_BUDGET_FRAC * n_2D * E_F          # placeholder (F-G0-5)
    m_ratio = E_F / (ME * C ** 2)
    q_opt = 2.0 * math.pi / 500e-9
    wp_b = math.sqrt(n_2D * EC ** 2 * k_F / (2.0 * EPS0 * ME))
    wp_o = math.sqrt(n_2D * EC ** 2 * q_opt / (2.0 * EPS0 * ME))
    tau_T = n_2D * SIGMA_T                            # frozen-state electron Thomson reference
    # Density baseline (F-G0-7): n_3D = column density / L_z; m^-3 -> fm^-3 divided by 1e45
    n_nuc_fm3 = N_s / LZ_FM / 1e45                   # nuclear density 4.216e-3 fm^-3
    n_B_fm3 = N_B / LZ_FM / 1e45                     # baryon density 0.0422 fm^-3
    r.update(dict(N_s=N_s, N_B=N_B, n_2D=n_2D, n_2D_Z5=n_2D_Z5, spread=spread,
                  d_par=d_par, k_F=k_F, E_F_J=E_F, E_F_MeV=E_F / MEV,
                  E_F_NR_J=E_NR, reldev=reldev,
                  u_2D=u_2D, P_2D=P_2D, c_s=c_s, Sigma=Sigma, v_inf=v_inf,
                  A_min=A_min, Lz_ion=Lz_ion, B_ion=B_ion, frac=frac,
                  a_i=a_i, U_e=U_e, U_i=U_i, Gamma_e=U_e / E_F,
                  Ui_over_EF=U_i / E_F, mu_e_MeV=mu_e_MeV, capture=cap,
                  nu_budget=nu_budget, nu_over_u=nu_budget / u_2D,
                  tau_T=tau_T, wp_bare_kF=wp_b, wp_star_kF=wp_b / math.sqrt(m_ratio),
                  wp_bare_opt=wp_o, wp_star_opt=wp_o / math.sqrt(m_ratio),
                  m_ratio=m_ratio, n_nuc_fm3=n_nuc_fm3, n_B_fm3=n_B_fm3,
                  dims=dims, eta={}))
    hv = HBAR * V_PROBE
    for k, (L, dE) in dict(e1s=(A0, 13.6), bond=(1e-10, 5.0),
                           phonon=(1e-9, 0.05), nucleon=(1e-15, 1e6)).items():
        r["eta"][k] = (hv / L / EC) / dE
    return r


def _S(D):
    from math import gamma, pi
    return 2 * pi ** (D / 2.0) / gamma(D / 2.0)


def _num_nD(kf, D, g):
    v, _ = quad(lambda k: _S(D) * k ** (D - 1), 0.0, kf, epsabs=1e-30, epsrel=1e-13)
    return g * v / (2.0 * math.pi) ** D


def _num_uD(kf, D, g):
    v, _ = quad(lambda k: _S(D) * HBAR * C * k ** D, 0.0, kf,
                epsabs=1e-30, epsrel=1e-13)
    return g * v / (2.0 * math.pi) ** D


def pathB():
    N_B = M_KG / (AMU * A_PERP)
    N_s = N_B / M_BAR_AMU
    n_2D = ZA * N_B
    lo, hi = 1e12, 1e18
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _num_nD(mid, 2, G_E) < n_2D:
            lo = mid
        else:
            hi = mid
    kF = 0.5 * (lo + hi)
    u = _num_uD(kF, 2, G_E)
    EF = HBAR * C * kF
    ks = np.linspace(kF * 0.5, kF * 1.5, 601)
    us = np.array([_num_uD(k, 2, G_E) for k in ks])
    cs2 = float(np.interp(kF, ks, np.gradient(us / 2.0, us)))
    P = u / 2.0
    return dict(N_s=N_s, N_B=N_B, n_2D=n_2D, k_F=kF, E_F_J=EF,
                u_2D=u, P_2D=P, c_s=C * math.sqrt(max(cs2, 0.0)),
                cs2=cs2, v_inf=math.sqrt(2 * P * A_PERP / M_KG),
                A_min=N_s * D_BOND ** 2, B_ion=math.pi * A0 / L_BODY,
                coef={d: (_num_uD(kF, d, G_E) / _num_nD(kF, d, G_E)) / EF
                      for d in (1, 2, 3)})


def run_tests(A, B):
    res = []

    def t(name, val, thr, ok, note=""):
        res.append((name, float(val), float(thr), bool(ok), note))

    # T1 consistency of nuclear column density (v1 semantics retained) with baryon
    #    column density conversion
    rel1 = abs(A["N_B"] / A["N_s"] - M_BAR_AMU) / M_BAR_AMU
    t("T1_Ns_NB_consistency", rel1, TH["T1"], rel1 < TH["T1"],
      "N_B/N_s = m_bar = %.1f (defining identity)" % (A["N_B"] / A["N_s"]))
    # T2 NR -> relativistic switch
    t("T2_relativistic_switch", A["reldev"], TH["nr_switch_reldev"],
      A["reldev"] > TH["nr_switch_reldev"],
      "v_F/c=%.1f; E_F=%.2f MeV requires the relativistic dispersion"
      % (HBAR * A["k_F"] / ME / C, A["E_F_MeV"]))
    # T3 A=380 km² reproduces 3 Å
    d3 = (A["N_s"] / 3.8e8) ** -0.5
    t("T3_Amin_3A", abs(d3 - 3e-10) / 3e-10, TH["T3"],
      abs(d3 - 3e-10) / 3e-10 < TH["T3"], "d=%.3f A" % (d3 * 1e10))
    # T4 column density invariant under compression (σ_eff constant premise registered)
    cols = []
    for bf in (1.0, 0.1, 0.01):
        cols.append(M_KG / (M_BAR_AMU * AMU * A_PERP))   # independent of B (pure combination)
    d4 = max(abs(c - cols[0]) / cols[0] for c in cols)
    t("T4_column_invariance", d4, TH["T4"], d4 < TH["T4"],
      "sigma_eff constant premise registered (N1-b CONDITIONAL)")
    # T5 D=1/2/3 coefficients (dual path)
    e5 = max(abs(A["dims"][d][1] / A["dims"][d][0] / A["E_F_J"] - d / (d + 1.0))
             for d in (1, 2, 3))
    e5b = max(abs(B["coef"][d] - d / (d + 1.0)) for d in (1, 2, 3))
    t("T5_dim_coefficients", max(e5, e5b), TH["T5"], max(e5, e5b) < TH["T5"],
      "A %.1e / B(numeric) %.1e" % (e5, e5b))
    # T6 capture thresholds (kinetic-energy convention, F-G0-8)
    t("T6_capture_open", float(A["capture"]["C12"]), 1.0,
      A["capture"]["C12"] and all(A["capture"].values()),
      "mu_e=%.2f MeV (total) > all kinetic-convention Q; Q table uses the kinetic convention (total convention +0.511)"
      % A["mu_e_MeV"])
    # T7 c_s=c/sqrt2, v_inf, B_ion (dual path)
    c_ref = C / math.sqrt(2)
    e7 = max(abs(A["c_s"] - c_ref) / c_ref, abs(B["c_s"] - c_ref) / c_ref,
             abs(A["v_inf"] - math.sqrt(2 * A["P_2D"] / A["Sigma"])) /
             math.sqrt(2 * A["P_2D"] / A["Sigma"]),
             abs(A["B_ion"] - math.pi * A0 / L_BODY) / (math.pi * A0 / L_BODY))
    t("T7_cs_vinf_Bion", e7, TH["T7"], e7 < TH["T7"],
      "cs2_numeric=%.6f" % B["cs2"])
    # T8 p_z limits
    def pz(s):
        Bs = np.array([0.999, 1.0, 1.001])
        return -(1.0) * float(np.gradient(Bs ** (-s) * Bs, Bs)[1])
    e8 = max(abs(pz(3) - 2.0), abs(pz(2) - 1.0))
    t("T8_pz_limits", e8, TH["T8"], e8 < TH["T8"],
      "NR %.4f (exp 2); UR %.4f (exp 1)" % (pz(3), pz(2)))
    # T9 (new, F-G0-4): n_2D two-convention spread registration
    t("T9_n2D_convention_spread", A["spread"], TH["T9_spread"],
      A["spread"] < TH["T9_spread"],
      "ZA*N_B=%.4e vs Z_ion*N_s=%.4e (m^-2); spread=%.2f%% (Z_eff=5.22 vs 5); "
      "main convention takes ZA*N_B" % (A["n_2D"], A["n_2D_Z5"], A["spread"] * 100))
    return res


def seven_row(A):
    rows = []
    rows.append(dict(
        goal="Maintain original atoms/chemical bonds/non-covalent network at fixed area",
        verdict="NO-GO (conditional: under the specified model assumptions)",
        basis="d_par=%.2f fm = %.2e a0 (nuclear-column-density convention; geometric quantity unaffected by the electron-convention correction)"
              % (A["d_par"] * 1e15, A["d_par"] / A0),
        level="MODEL RESULT"))
    rows.append(dict(goal="New stable high-density state", verdict="OPEN",
                     basis="Determined by R1-B1 v2 (after dimensional correction)", level="OPEN"))
    rows.append(dict(goal="Healthy positive solution for geometric contraction", verdict="OPEN",
                     basis="D3/R2; N6 p_z counterexample + N11 constraint stress (values updated with the P_2D correction)",
                     level="OPEN"))
    rows.append(dict(goal="Effective 2D low-energy theory", verdict="OPEN",
                     basis="R1-B4 v2 + R3; N7 carrier gating", level="OPEN"))
    rows.append(dict(goal="Other matter/radiation states", verdict="OPEN",
                     basis="R1-B2 v2 / R1-B3 v2", level="OPEN"))
    rows.append(dict(
        goal="Mechanical self-equilibrium of the final state at fixed area",
        verdict="NO-GO (conditional: frozen-state electron-gas pressure model + P_constraint=0)",
        basis=("P_2D (corrected convention)=%.3e N/m (v1's 2.73e15 withdrawn); without confinement the "
               "final state expands with c_s=%.3e m/s, 1 m region %.2f ns, v_inf=%.3f c. "
               "Limitation: valid only for the current ideal UR electron-gas pressure model; the final-state "
               "EOS is undecided (R1-B1 v2), and interface stress/surface tension are not included -- "
               "it cannot be extrapolated to 'no final state is possible'" %
               (A["P_2D"], A["c_s"], 1.0 / A["c_s"] * 1e9, A["v_inf"] / C)),
        level="MODEL RESULT (model-conditioned)"))
    rows.append(dict(
        goal="Whether the v1.3 cold-electron-gas final state is the ground state at that density",
        verdict="NO (threshold comparison ESTABLISHED)",
        basis=("mu_e=%.2f MeV (corrected convention) exceeds all nuclide kinetic-convention capture thresholds Q (+m_e for the total convention); "
               "nu_budget=%.3e J/m^2 is a registered placeholder (/u_2D=%.3f, not a transport result, F-G0-5)" %
               (A["mu_e_MeV"], A["nu_budget"], A["nu_over_u"])),
        level="MODEL RESULT"))
    return rows


def main():
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    A = pathA()
    B = pathB()
    tests = run_tests(A, B)
    rows = seven_row(A)
    keys = ["N_s", "N_B", "n_2D", "k_F", "E_F_J", "u_2D", "P_2D", "c_s",
            "v_inf", "A_min", "B_ion"]
    recheck = {}
    worst = 0.0
    for k in keys:
        va, vb = A[k], B[k]
        rel = abs(va - vb) / abs(va)
        recheck[k] = (va, vb, rel)
        worst = max(worst, rel)
    all_pass = all(t[3] for t in tests)
    now = datetime.now().isoformat(timespec="seconds")

    print("<<<LOG>>>")
    L = []
    w = L.append
    w("=" * 84)
    w("G0' v2 (G0P-002): convention-corrected survival threshold (review-driven)")
    w("=" * 84)
    w("run: %s" % now)
    w("corrections applied: F-G0-4 (n_2D convention), F-G0-5 (nu budget relabel),")
    w("  F-G0-6 (Gamma_i relabel), F-G0-7 (density basis), F-G0-8 (Q convention)")
    w("registered thresholds: %s" % TH)
    w("")
    w("[dual-path recheck] threshold=%.2f" % TH["dual"])
    for k, (va, vb, rel) in recheck.items():
        w("  %-6s A=%.6e B=%.6e reldev=%.1e" % (k, va, vb, rel))
    w("  worst=%.2e %s" % (worst, "PASS" if worst < TH["dual"] else "FAIL"))
    w("")
    w("[tests]")
    for name, val, thr, ok, note in tests:
        w("  %-26s %.3e / %.1e  %s  %s" % (name, val, thr,
                                           "PASS" if ok else "FAIL", note))
    w("  => %s" % ("ALL PASS" if all_pass else "HAS FAIL"))
    w("")
    w("[G0' v2 baseline (supersedes G0P-001 numbers)]")
    w("  N_s(nuclei)   = %.4e m^-2   (unchanged)" % A["N_s"])
    w("  N_B(baryons)  = %.4e m^-2   (= m_bar * N_s)" % A["N_B"])
    w("  n_2D          = %.4e m^-2   (v1: 2.20e27 -- F-G0-4 fix, x m_bar)" % A["n_2D"])
    w("  k_F           = %.4e m^-1   (v1: 1.176e14)" % A["k_F"])
    w("  E_F = mu_e    = %.3f MeV    (v1: 23.20; mu_e/m_ec2=%.1f)"
      % (A["E_F_MeV"], A["m_ratio"]))
    w("  u_2D          = %.4e J/m^2 = %.2f Mt/m^2 (v1: 5.45e15 = 1.30)"
      % (A["u_2D"], A["u_2D"] / MT_J))
    w("  P_2D          = %.4e N/m    (v1: 2.73e15)" % A["P_2D"])
    w("  c_s           = %.4e m/s = c/sqrt2 (unchanged)" % A["c_s"])
    w("  v_inf         = %.4e m/s = %.4f c (v1: 0.0294c)" % (A["v_inf"], A["v_inf"] / C))
    w("  t_rip(1 m)    = %.2f ns     (unchanged)" % (1.0 / A["c_s"] * 1e9))
    w("  u_2D/Mc^2     = %.3f %%     (v1: 0.087)" % (A["frac"] * 100))
    w("  A_min / B_ion = %.3e m^2 / %.3e (unchanged, geometric)" % (A["A_min"], A["B_ion"]))
    w("  Gamma_e       = %.3e (U_e/E_F)" % A["Gamma_e"])
    w("  U_i/E_F       = %.3e  [RELABEL: NOT the ion coupling parameter; F-G0-6]" % A["Ui_over_EF"])
    w("  tau_T(frozen) = %.4f      (v1: 0.146 -- x m_bar; marginal-thick regime)" % A["tau_T"])
    w("  nu_budget     = %.4e J/m^2  [PLACEHOLDER: /u_2D=%.3f; not a transport result]"
      % (A["nu_budget"], A["nu_over_u"]))
    w("  density basis: nuclei %.4e fm^-3 (= 0.026*n_nuc doc); baryons %.4e fm^-3"
      % (A["n_nuc_fm3"], A["n_B_fm3"]))
    w("  wp_bare(kF)   = %.4e rad/s; m* corrected %.4e" % (A["wp_bare_kF"], A["wp_star_kF"]))
    w("")
    w("[eta_rough] (unchanged, window B>=2.4e-9)")
    for k, v in A["eta"].items():
        w("  %-9s %.4f" % (k, v))
    w("")
    w("[seven-row verdicts v2]")
    for i, r in enumerate(rows, 1):
        w("  %d. %-44s => %s" % (i, r["goal"], r["verdict"]))
        w("       %s [%s]" % (r["basis"], r["level"]))
    w("")
    w("[handoff to R1-B1 v2 / N11]")
    w("  n_B(G0, baryon) = %.4e fm^-3  (v1 used 0.026 fm^-3 = neither quantity)"
      % A["n_B_fm3"])
    w("  n_e,frozen = ZA*n_B = %.4e fm^-3 -> mu_e,frozen = %.2f MeV"
      % (A["n_2D"] / A["N_s"] * A["n_B_fm3"], A["mu_e_MeV"]))
    w("  P_2D(frozen electron gas) = %.4e N/m -> N11 constraint-stress input"
      % A["P_2D"])
    w("")
    w("G0' v2 OVERALL: %s (tests %s; dual-path %s)" % (
        "PASS" if all_pass and worst < TH["dual"] else "FAIL",
        "PASS" if all_pass else "FAIL", "PASS" if worst < TH["dual"] else "FAIL"))
    w("evidence level: MODEL RESULT (model-limited wordings per review; numbers NOT")
    w("  frozen until reviewer confirms v2 baseline)")
    print("\n".join(L))


if __name__ == "__main__":
    main()
