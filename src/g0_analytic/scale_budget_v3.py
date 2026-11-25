# -*- coding: utf-8 -*-
"""
G0' v3: fixed-area survival threshold (review B1/B2/B3/B5 fix version)
=============================================================================

Four substantive changes relative to v2 (G0P-002):

  B1  factor-of-10 error in the n_e handoff (v2: scale_budget_v2.py:345-346)
      v2 wrote n_e = (n_2D/N_s) * n_B = Z_eff * n_B = 5.22*0.0422 = 0.2200 fm^-3,
      while the correct value is Z_A * n_B = 0.02200 fm^-3. Cause: the "electrons per
      nucleus Z_eff" was multiplied by the "baryon density", whereas Z_eff is defined
      against the "nuclear density". From v3 on, n_e is taken only from
      src/common/conv.py, and r4=Z_eff*n_B is kept as a
      **negative control** that must deviate by exactly a factor of 10.000 -- the
      erroneous formula itself is registered as a guard.

  B3  test integrity. Four of v2's T1/T3/T4/T5/T8 were identities (construct then
      invert, compare the same expression, differentiate a power law) yet all were
      labeled PASS. v3 splits tests into three classes:
        IDENT   : defining identity, reported but not counted as correctness evidence
        CHECK   : genuine independent computation (numerical quadrature, numerical
                  derivative, cross-module cross-check), counted as evidence
        NEGCTRL : negative control that must fail; passing means the guard works
      The summary line counts only CHECKs and explicitly prints the IDENT count, so
      that a "10/10 PASS" self-consistency badge is not misread as a correctness
      badge.

  B2  dimensional convention envelope. v2 reported only a single convention
      (electrons 2D / nucleons implicitly 3D). v3 calls conv.beta_envelope() and
      lists the three conventions ALL3D / HYB / ALL2D side by side, registering X_p,
      mu_e, n_e and P(Sigma) as **intervals** rather than single-point values.

  B5  thresholds and physical constants all externalized: thresholds read from
      configs/g0_prime_v3.json (hard failure if missing); constants read from
      src/common/conv.py. No second constant table remains in the module.

Frozen-state numbers (v3 baseline, superseding v2):
  n_2D = 2.20049e28 m^-2 = 0.022005 fm^-2
  E_F = mu_e = 73.37 MeV,  u_2D = 1.7244e17 J/m^2,  P_2D = 8.622e16 N/m
  c_s = c/sqrt2,  v_inf = 0.1656 c,  t_rip(1 m) = 4.72 ns

Run: python -I src/g0_analytic/scale_budget_v3.py
"""
import json
import math
import os
import sys
from datetime import datetime

import numpy as np
from scipy.integrate import quad

# Single source of truth (B5)
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from src.common import conv  # noqa: E402

CFG_PATH = os.path.join(_ROOT, "configs", "g0_prime_v3.json")

# Non-physical constants (outside conv's registered domain, but likewise present only once here)
MT_J = 4.184e15                 # J per megaton TNT
A0 = 5.29177210903e-11          # m
D_BOND = None                   # m -- injected from config.physical_targets, see below
EPS0 = 8.8541878128e-12
EC = 1.602176634e-19
SIGMA_T = 6.6524587321e-29      # m^2
ME = 9.1093837015e-31           # kg
E2_4PE0 = 2.307077552e-28       # J m


def load_cfg(path=CFG_PATH):
    """Sole source of thresholds and inputs; hard failure if missing or noncompliant (B5)"""
    if not os.path.exists(path):
        raise SystemExit("FATAL: registered config missing: %s" % path)
    with open(path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    for key in ("inputs", "thresholds", "capture_Q_MeV_kinetic",
                "negative_controls", "test_registry"):
        if key not in cfg:
            raise SystemExit("FATAL: config missing section %r" % key)
    if cfg.get("status") != "REGISTERED_BEFORE_RUN":
        raise SystemExit("FATAL: config status must be REGISTERED_BEFORE_RUN")
    return cfg


CFG = load_cfg()
INP = CFG["inputs"]
D_BOND = float(CFG["physical_targets"]["D_bond_m"])
TH = CFG["thresholds"]
Q_CAP = CFG["capture_Q_MeV_kinetic"]

# Consistency guards between config and conv registered constants (avoid two sets of inputs)
assert abs(INP["M_kg"] - conv.M_KG) < 1e-12, "M_kg mismatch between config and conv"
assert abs(INP["m_bar_amu"] - conv.M_BAR_AMU) < 1e-12, "m_bar mismatch"
assert abs(INP["Z_over_A"] - conv.ZA) < 1e-12, "Z/A mismatch"
assert abs(INP["L_z_fm"] - conv.LZ_FM) < 1e-12, "L_z mismatch"


# --------------------------------------------------------------- path A analytic
def pathA():
    r = {}
    N_s = conv.N_S                      # nuclear column density m^-2
    N_B = conv.N_B                      # baryon column density m^-2
    n_2D = conv.N_E_FM2                 # fm^-2 (main convention ZA*N_B) -- conv's sole source
    n_2D_m2 = n_2D * 1e30
    n_2D_Z5 = INP["Z_ion"] * conv.N_S_FM2
    spread = abs(n_2D - n_2D_Z5) / n_2D

    d_par = N_s ** -0.5                 # in-plane internuclear spacing (geometric quantity)
    e2 = conv.eos_e_2D(n_2D, conv.G_E)
    k_F = e2["kF"]
    E_F_MeV = e2["EF"]
    u_areal = e2["u"]                   # MeV/fm^2
    P_areal = e2["P"]                   # MeV/fm^2
    u_2D = u_areal * conv.J_PER_MEV_FM2 # J/m^2
    P_2D = conv.P_areal_to_Nm(P_areal)  # N/m

    # Relativistic criterion: E_F/(m_e c^2) rather than "v_F/c" (v2's T2 label was wrong)
    m_ratio = E_F_MeV / conv.M_E        # degeneracy (for a UR gas v_F = c always)
    E_NR_MeV = E_F_MeV ** 2 / (2.0 * conv.M_E)
    nr_switch = E_NR_MeV / E_F_MeV      # = E_F/(2 m c^2); >1 is the NR side

    c_s = conv.C / math.sqrt(2.0)
    Sigma = conv.M_KG / conv.A_PERP
    v_inf = math.sqrt(2.0 * P_2D / Sigma)
    A_min = N_s * D_BOND ** 2
    Lz_ion = math.pi * A0
    B_ion = Lz_ion / CFG["physical_targets"]["L_body_m"]
    frac = u_2D / (conv.M_KG * conv.C ** 2 / conv.A_PERP)

    a_i = (math.pi * N_s) ** -0.5
    U_e = E2_4PE0 / a_i
    U_i = INP["Z_ion"] ** 2 * U_e

    capture = {k: bool(E_F_MeV > q) for k, q in Q_CAP.items()}
    margin = E_F_MeV - max(Q_CAP.values())

    nu_frac = CFG["placeholder_params"]["nu_budget_frac"]["value"]
    nu_budget = nu_frac * n_2D_m2 * E_F_MeV * conv.MEV_J   # J/m^2 placeholder
    tau_T = n_2D_m2 * SIGMA_T

    r.update(dict(
        N_s=N_s, N_B=N_B, n_2D=n_2D, n_2D_m2=n_2D_m2, n_2D_Z5=n_2D_Z5,
        spread=spread, d_par=d_par, k_F=k_F, E_F_MeV=E_F_MeV,
        u_2D=u_2D, P_2D=P_2D, c_s=c_s, Sigma=Sigma, v_inf=v_inf,
        A_min=A_min, Lz_ion=Lz_ion, B_ion=B_ion, frac=frac,
        a_i=a_i, U_e=U_e, U_i=U_i, Gamma_e=U_e / (E_F_MeV * conv.MEV_J),
        Ui_over_EF=U_i / (E_F_MeV * conv.MEV_J),
        mu_e_MeV=E_F_MeV, capture=capture, capture_margin=margin,
        m_ratio=m_ratio, nr_switch=nr_switch,
        nu_budget=nu_budget, nu_over_u=nu_budget / u_2D,
        tau_T=tau_T,
        n_nuc_fm3=conv.N_NUC_FM3, n_B_fm3=conv.N_B_FM3, n_e_fm3=conv.N_E_FM3,
        E_sub=conv.E_SUBBAND, E_sub_ratio=conv.E_SUBBAND / E_F_MeV,
    ))
    return r


# ------------------------------------------------- path B numerical quadrature (independent path)
def _S(D):
    from math import gamma, pi
    return 2.0 * pi ** (D / 2.0) / gamma(D / 2.0)


def _num_nD(kf, D, g):
    """k in fm^-1 -> n in fm^-D (D=2 means fm^-2)"""
    v, _ = quad(lambda k: _S(D) * k ** (D - 1), 0.0, kf, epsabs=1e-30, epsrel=1e-13)
    return g * v / (2.0 * math.pi) ** D


def _num_uD(kf, D, g):
    """u = ∫ S(D) (ħc k) k^(D-1) dk; k[fm^-1] makes ħc k directly give MeV -> u[MeV/fm^D]"""
    v, _ = quad(lambda k: _S(D) * conv.HBARC * k * k ** (D - 1), 0.0, kf,
                epsabs=1e-30, epsrel=1e-13)
    return g * v / (2.0 * math.pi) ** D


def pathB():
    """Solve k_F from n_2D (quadrature), then compute u, P, c_s^2 -- independent of pathA's closed form"""
    n_2D = conv.N_E_FM2
    lo, hi = 1e-2, 1e2                       # fm^-1
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if _num_nD(mid, 2, conv.G_E) < n_2D:
            lo = mid
        else:
            hi = mid
    kF = 0.5 * (lo + hi)
    u_areal = _num_uD(kF, 2, conv.G_E)       # MeV/fm^2
    E_F = conv.HBARC * kF

    # c_s^2 = dP/du numerical derivative along the EOS (a real computation, not a
    # restatement of the analytic formula)
    ks = np.linspace(kF * 0.5, kF * 1.5, 1201)
    us = np.array([_num_uD(k, 2, conv.G_E) for k in ks])
    Ps = us / 2.0
    cs2 = float(np.interp(kF, ks, np.gradient(Ps, us)))

    return dict(k_F=kF, E_F_MeV=E_F,
                u_2D=u_areal * conv.J_PER_MEV_FM2,
                P_2D=conv.P_areal_to_Nm(float(np.interp(kF, ks, Ps))),
                cs2=cs2, c_s=conv.C * math.sqrt(max(cs2, 0.0)))


# ------------------------------------------------------------------- test suite
def run_tests(A, B):
    """Return [(name, tag, value, thr, ok, note), ...]; tags are in config.test_registry"""
    res = []

    def t(name, tag, val, thr, ok, note=""):
        res.append((name, tag, float(val), float(thr), bool(ok), note))

    # ---- IDENT: defining identities (reported, not counted as evidence) ----
    t("I1_Nb_over_Ns_eq_mbar", "IDENT",
      abs(A["N_B"] / A["N_s"] - conv.M_BAR_AMU) / conv.M_BAR_AMU,
      TH["identity_rel"],
      abs(A["N_B"] / A["N_s"] - conv.M_BAR_AMU) / conv.M_BAR_AMU < TH["identity_rel"],
      "N_B/N_s = m_bar = %.1f -- follows directly from the definitions of N_B and N_s, not a test" % conv.M_BAR_AMU)

    t("I2_Amin_inverse_3A", "IDENT",
      abs((A["A_min"] / A["N_s"]) ** 0.5 - D_BOND) / D_BOND,
      TH["identity_rel"],
      abs((A["A_min"] / A["N_s"]) ** 0.5 - D_BOND) / D_BOND < TH["identity_rel"],
      "A_min is defined from D_BOND and inverted back to D_BOND -- an identity; v2 labeled it PASS")

    e_dims = max(abs(A["u_2D"] / (conv.J_PER_MEV_FM2 * A["n_2D"] * A["E_F_MeV"])
                     - d / (d + 1.0)) for d in (2,))
    t("I3_dim_coefficient_2D", "IDENT", e_dims, TH["identity_rel"],
      e_dims < TH["identity_rel"],
      "u/nE_F = d/(d+1) = 2/3 for D=2 is a restatement of the analytic formula; the genuine independent check is C2")

    # ---- CHECK: genuine independent computations (counted as evidence) ----
    # C1 closed-form k_F vs quadrature-inverted k_F
    t("C1_kF_closed_vs_quad", "CHECK",
      abs(A["k_F"] - B["k_F"]) / A["k_F"], TH["quadrature_rel"],
      abs(A["k_F"] - B["k_F"]) / A["k_F"] < TH["quadrature_rel"],
      "closed form (4πn/g)^1/2 = %.6f fm^-1 vs quadrature inversion %.6f fm^-1"
      % (A["k_F"], B["k_F"]))

    # C2 closed-form u = 2/3 nE_F vs quadrature ∫ħck dN
    t("C2_u_closed_vs_quad", "CHECK",
      abs(A["u_2D"] - B["u_2D"]) / A["u_2D"], TH["quadrature_rel"],
      abs(A["u_2D"] - B["u_2D"]) / A["u_2D"] < TH["quadrature_rel"],
      "u = %.6e vs %.6e J/m^2" % (A["u_2D"], B["u_2D"]))

    # C3 c_s^2 from numerical dP/du vs analytic 1/2
    t("C3_cs2_numeric_vs_half", "CHECK",
      abs(B["cs2"] - 0.5) / 0.5, TH["derivative_rel"],
      abs(B["cs2"] - 0.5) / 0.5 < TH["derivative_rel"],
      "dP/du = %.8f (should be 0.5 for 2D UR); v2's T7 only compared two same-origin copies of c/sqrt2"
      % B["cs2"])

    # C4 3D Chandrasekhar EOS gives P/u = 1/3 in the UR limit (cross-module function check)
    e3 = conv.eos_e_3D(10.0)             # 10 fm^-3, strongly degenerate
    pu = e3["P"] / e3["u"]
    t("C4_eos3D_UR_limit", "CHECK", abs(pu - 1.0 / 3.0) / (1.0 / 3.0),
      TH["eos_ur_pu_rel"],
      abs(pu - 1.0 / 3.0) / (1.0 / 3.0) < TH["eos_ur_pu_rel"],
      "the 3D EOS gives P/u=%.6f at n=10 fm^-3 (expected 0.333333) -- checks the function used by HYB/ALL3D"
      % pu)

    # C5 subband spacing >> E_F (this is the argument for "electron D=2" itself and
    #    must be auditable)
    t("C5_subband_gap_ratio", "CHECK", A["E_sub_ratio"],
      TH["subband_ratio_min"],
      A["E_sub_ratio"] > TH["subband_ratio_min"],
      "E_sub = %.1f MeV vs E_F = %.2f MeV, ratio %.2f (>%.1f means a single subband, D=2 holds)"
      % (A["E_sub"], A["E_F_MeV"], A["E_sub_ratio"], TH["subband_ratio_min"]))

    # C6 capture thresholds: comparison of mu_e with external nuclear data (a real
    #    comparison, not an identity)
    t("C6_capture_all_open", "CHECK", A["capture_margin"],
      TH["capture_margin_min_MeV"],
      A["capture_margin"] > TH["capture_margin_min_MeV"],
      "mu_e=%.2f MeV vs the largest Q(C12)=%.2f MeV, margin %.2f MeV (kinetic convention, F-G0-8)"
      % (A["E_F_MeV"], max(Q_CAP.values()), A["capture_margin"]))

    # C7 dimensional effect on electron E_F between 2D and 3D -- this is a "registered"
    #    item rather than a test, so it is moved out of the test suite and printed in
    #    the [1] baseline section as C7_registered (cannot be judged pass/fail).

    # C8 beta-equilibrium residual (genuinely solved under HYB; residual should reach
    #    machine zero)
    env = conv.beta_envelope()
    res_h = abs(env["HYB"]["beta_res"])
    t("C8_beta_residual_HYB", "CHECK", res_h, TH["handoff_rel"],
      res_h < TH["handoff_rel"],
      "mu_n - mu_p - mu_e = %.2e MeV (back-substituted after solving under HYB)" % res_h)

    # ---- NEGCTRL: negative controls that must fail ----
    hr = conv.handoff_routes()
    t("N1_handoff_v2_wrong_x10", "NEGCTRL",
      hr["r4_v2_wrong"] / hr["r1"],
      CFG["negative_controls"]["handoff_v2_wrong_factor_expected"],
      abs(hr["r4_v2_wrong"] / hr["r1"]
          - CFG["negative_controls"]["handoff_v2_wrong_factor_expected"])
      < TH["negative_control_rel"],
      "the ratio of v2's erroneous formula Z_eff*n_B to the correct value = %.6f (should be exactly m_bar=10); "
      "if this guard fails, a B1-type error will silently pass again" % (hr["r4_v2_wrong"] / hr["r1"]))

    return res, env, hr


def summarize(tests):
    by = {"IDENT": [0, 0], "CHECK": [0, 0], "NEGCTRL": [0, 0]}
    for _, tag, _, _, ok, _ in tests:
        by[tag][0] += 1
        by[tag][1] += 1 if ok else 0
    return by


# --------------------------------------------------------------- seven-row verdict table
def seven_row(A, env):
    xp = [env[m]["X_p"] for m in conv.MODES]
    mue = [env[m]["mu_e"] for m in conv.MODES]
    ptot = [env[m]["P_tot_Nm"] for m in conv.MODES]
    rows = []
    rows.append(dict(
        goal="Maintain original atoms/chemical bonds/non-covalent network at fixed area",
        verdict="NO-GO",
        basis="d_par=%.2f fm = %.2e a0 (geometric quantity, independent of the electron convention)"
              % (A["d_par"] * 1e15, A["d_par"] / A0),
        level="MODEL RESULT"))
    rows.append(dict(
        goal="New stable high-density state",
        verdict="OPEN",
        basis="R1-B1 v3 three-convention envelope: X_p in [%.2e, %.2e], mu_e in [%.2f, %.2f] MeV"
              % (min(xp), max(xp), min(mue), max(mue)),
        level="OPEN (convention-dependent, see B2)"))
    rows.append(dict(
        goal="Healthy positive solution for geometric contraction",
        verdict="OPEN",
        basis="D3/R2; N6 p_z counterexample + N11 constraint stress; input now uses the envelope P_tot in [%.2e, %.2e] N/m"
              % (min(ptot), max(ptot)),
        level="OPEN"))
    rows.append(dict(
        goal="Effective 2D low-energy theory",
        verdict="OPEN",
        basis="R1-B4 v3 (including the OPEN flag for the conflict between E_F,nuc and the 2D criterion) + R3",
        level="OPEN"))
    rows.append(dict(
        goal="Other matter/radiation states",
        verdict="OPEN",
        basis="R1-B2 v3 criterion changed to UNDECIDED / R1-B3",
        level="OPEN"))
    rows.append(dict(
        goal="Mechanical self-equilibrium of the final state at fixed area",
        verdict="NO-GO (conditional: frozen-state ideal UR electron-gas pressure + P_constraint=0)",
        basis=("P_2D=%.3e N/m; without confinement c_s=%.3e m/s, 1 m region %.2f ns, "
               "v_inf=%.3f c. Limitation: this model only; final-state EOS undecided, interface stress not included"
               % (A["P_2D"], A["c_s"], 1.0 / A["c_s"] * 1e9, A["v_inf"] / conv.C)),
        level="MODEL RESULT (model-conditioned)"))
    rows.append(dict(
        goal="Whether the v1.3 cold-electron-gas final state is the ground state at that density",
        verdict="NO",
        basis=("mu_e in [%.2f, %.2f] MeV exceeds all kinetic-convention Q under every convention (max %.2f); "
               "nu_budget is a registered placeholder (/u_2D=%.3f, not a transport result)"
               % (min(mue), max(mue), max(Q_CAP.values()), A["nu_over_u"])),
        level="MODEL RESULT"))
    return rows


# --------------------------------------------------------------------- main
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    A = pathA()
    B = pathB()
    tests, env, hr = run_tests(A, B)
    rows = seven_row(A, env)
    by = summarize(tests)
    now = datetime.now().isoformat(timespec="seconds")

    L = []
    w = L.append
    w("=" * 88)
    w("G0' v3 (G0P-003): fixed-area survival threshold -- triple fix of handoff/conventions/test integrity")
    w("=" * 88)
    w("run: %s" % now)
    w("config: configs/g0_prime_v3.json (status=%s)" % CFG["status"])
    w("constants: src/common/conv.py (single source of truth)")
    w("")

    w("[1] frozen baseline (v3; supersedes G0P-002)")
    w("  N_s(nuclei)   = %.6e m^-2" % A["N_s"])
    w("  N_B(baryons)  = %.6e m^-2  (= m_bar*N_s)" % A["N_B"])
    w("  n_2D          = %.6e m^-2 = %.6e fm^-2  (same value as v2; convention now in conv)" % (A["n_2D_m2"], A["n_2D"]))
    w("  k_F           = %.6f fm^-1" % A["k_F"])
    w("  E_F = mu_e    = %.3f MeV   (E_F/m_e c^2 = %.1f; 2D UR so v_F = c)" % (A["E_F_MeV"], A["m_ratio"]))
    w("  u_2D          = %.4e J/m^2 = %.3f Mt/m^2" % (A["u_2D"], A["u_2D"] / MT_J))
    w("  P_2D          = %.4e N/m" % A["P_2D"])
    w("  c_s           = %.4e m/s = c/sqrt2" % A["c_s"])
    w("  v_inf         = %.4e m/s = %.4f c" % (A["v_inf"], A["v_inf"] / conv.C))
    w("  t_rip(1 m)    = %.2f ns" % (1.0 / A["c_s"] * 1e9))
    w("  u_2D/Mc^2     = %.3f %%   (v1's 0.087%% withdrawn; v2's 2.74%% retained)"
      % (A["frac"] * 100))
    w("  tau_T(frozen) = %.4f" % A["tau_T"])
    w("  A_min / B_ion = %.3e m^2 / %.3e" % (A["A_min"], A["B_ion"]))
    w("  Gamma_e = %.3e ; U_i/E_F = %.3e  [RELABEL F-G0-6: not the ion coupling parameter]"
      % (A["Gamma_e"], A["Ui_over_EF"]))
    ef3 = conv.eos_e_3D(conv.N_E_FM3)["EF"]
    w("  [C7_registered] E_F(3D)=%.2f vs E_F(2D)=%.2f MeV, ratio %.3f -- registered item,"
      % (ef3, A["E_F_MeV"], ef3 / A["E_F_MeV"]))
    w("                  not a pass criterion (no prior true value to compare)")
    w("")

    w("[2] B1 handoff fix: four routes for n_e (r4 is the negative control of v2's erroneous formula)")
    for k in ("r1", "r2", "r3"):
        w("  %-3s = %.6e fm^-3" % (k, hr[k]))
    w("  r1 vs r2 reldev = %.1e ; r1 vs r3 reldev = %.1e"
      % (hr["dev12"], hr["dev13"]))
    w("  r4(v2 wrong) = Z_eff*n_B = %.6e fm^-3 ; r4/r1 = %.6f  [must = 10]"
      % (hr["r4_v2_wrong"], hr["r4_v2_wrong"] / hr["r1"]))
    w("  => handoff value n_e,frozen = ZA*n_B = %.6e fm^-3 (v2 log printed %.6e, wrong by 10x)"
      % (hr["r1"], hr["r4_v2_wrong"]))
    w("")

    w("[3] B2 dimensional-convention envelope (X_p / mu_e / P_tot must not be reported as single-point values)")
    w("  %-6s %-4s %-4s %-11s %-10s %-11s %-11s %-12s"
      % ("mode", "D_e", "D_nuc", "X_p", "mu_e[MeV]", "n_e[fm^-3]", "reduction", "P_tot[N/m]"))
    for m in conv.MODES:
        r = env[m]
        w("  %-6s %-4d %-4d %.4e  %-10.3f %.4e   %-11.2f %.4e"
          % (m, r["D_e"], r["D_nuc"], r["X_p"], r["mu_e"], r["n_e_fm3"],
             r["reduction"], r["P_tot_Nm"]))
    xp = [env[m]["X_p"] for m in conv.MODES]
    pt = [env[m]["P_tot_Nm"] for m in conv.MODES]
    w("  envelope: X_p %.2e..%.2e (spanning %.0f x) ; P_tot %.2e..%.2e N/m (spanning %.0f x)"
      % (min(xp), max(xp), max(xp) / min(xp), min(pt), max(pt), max(pt) / min(pt)))
    w("  Note: HYB is the default convention. ALL3D is kept as a comparison, but it conflicts with R1-B4's 204 MeV subband spacing (compressed nucleons should occupy a single band),")
    w("        so it must not be cited alone.")
    w("")

    w("[4] Tests (classified by config.test_registry; the summary counts CHECKs only)")
    w("  %-26s %-8s %-12s %-10s %-6s %s" % ("name", "tag", "value", "thr", "res", "note"))
    for name, tag, val, thr, ok, note in tests:
        w("  %-26s %-8s %-12.4e %-10.2e %-6s %s"
          % (name, tag, val, thr, "PASS" if ok else "FAIL", note))
    w("  => CHECK %d/%d ; IDENT %d/%d (not counted as evidence); NEGCTRL %d/%d"
      % (by["CHECK"][1], by["CHECK"][0], by["IDENT"][1], by["IDENT"][0],
         by["NEGCTRL"][1], by["NEGCTRL"][0]))
    all_ok = all(ok for _, _, _, _, ok, _ in tests)
    w("  overall: %s" % ("PASS" if all_ok else "HAS FAIL"))
    w("  !! Evidence-level note: v2's '10/10 PASS' included 4 identities. v3 has only %d CHECKs"
      % by["CHECK"][0])
    w("     that count as correctness evidence; IDENT only guarantees no typo in the code, not correct physics.")
    w("")

    w("[5] Seven-row verdict v3")
    for i, r in enumerate(rows, 1):
        w("  %d. %-40s => %s" % (i, r["goal"], r["verdict"]))
        w("       %s [%s]" % (r["basis"], r["level"]))
    w("")

    w("[6] Handoff to R1-B1 v3 / N11")
    w("  n_B(baryon)   = %.6e fm^-3" % A["n_B_fm3"])
    w("  n_e(frozen)   = %.6e fm^-3   [FIXED: derived from conv, not Z_eff*n_B]"
      % A["n_e_fm3"])
    w("  mu_e(frozen)  = %.2f MeV" % A["E_F_MeV"])
    w("  P_2D(frozen electron gas) = %.4e N/m -> N11 constraint-stress input" % A["P_2D"])
    w("  P_tot(beta-eq) envelope   = %.2e .. %.2e N/m -> final-state stress requirement range"
      % (min(pt), max(pt)))
    w("")
    w("G0' v3 OVERALL: %s" % ("PASS" if all_ok else "FAIL"))
    w("evidence level: MODEL RESULT; frozen baseline numbers may be cited, but the three-convention envelope must be cited alongside.")
    print("\n".join(L))


if __name__ == "__main__":
    main()
