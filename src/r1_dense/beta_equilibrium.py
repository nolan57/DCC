# -*- coding: utf-8 -*-
"""
R1-B1: beta equilibrium, neutronized dense-matter EOS (v1.4 sec 8.3, highest priority)
=============================================================================

Model (registered assumption checklist, evidence level capped at MODEL RESULT):
  Cold (T=0) ideal npe Fermi gas: n, p (spin 1/2, NR nucleons), e (spin 1/2, exact relativistic integration).
  Charge neutrality: n_e = n_p; beta equilibrium: mu_n = mu_p + mu_e.
  mu_i = m_i + k_Fi²/(2m_i) (nucleons NR); mu_e = sqrt((hbar k_Fe)² + m_e²) (c=1).
  Electron pressure/energy via the exact Chandrasekhar integral (the UR limit automatically returns P=u/3).
  Deliverables: P(n_B), P(Σ) (Σ = m_n n_B L_z, with convention L_z=1 fm), c_s²=dP/dε,
                neutronization fraction X_n(n_B), mu_e(n_B), and the N7 bridge: the density corresponding to mu_eq=23.2 MeV.

Inherited prohibition (v1.4 sec 8.1): before R1-B1 is complete, the "two-dimensional degenerate electron gas"
must not be cited as the final state -- this module is the basis for lifting that ban; the final-state baseline
is set by this EOS (not a cold electron gas, see N7).

Zero file I/O: stdout in ASCII sections (adapted to safety-hook constraints).
Run: python -I src/r1_dense/beta_equilibrium.py > runs/R1B/r1b1_eos_results.txt
Thresholds (registered in advance): beta residual <1e-6 MeV; mu_e(n_B→1e-8) in 0.782±0.01 MeV;
                                    c_s²<1 throughout; P monotonically increasing; P_e/u_e→1/3 deviation <1e-3.
"""
import math

import numpy as np

# Registered parameters (c=1, energy in MeV, length in fm)
# v2 (2026-11-21, review-driven):
#   F-R1B1-1 Unit correction: momentum unified as p = hbar*c*k_F [MeV] (v1 plugged the fm^-1 k_F
#     directly into the MeV formula, missing the (hbar c)^2=3.89e4 factor); electron u/P multiplied by (hbar c)^-3.
#   F-R1B1-2 Density baseline: G0 baryon density n_B = 0.04216 fm^-3 (v1's 0.026 fm^-3 was
#     neither the document's "0.026*n_nuc" nuclear density 0.004216 fm^-3 nor the baryon density).
#   F-R1B1-3 Registered-threshold consistency: mu_e equilibrium limit = m_n-m_p = 1.293 MeV (total chemical potential);
#     the capture-threshold table Q=0.782(p) uses the kinetic-energy convention (= mu_e - m_e).
#   F-R1B1-4 N7 bridge redone: compare same-density same-species particles; mu_e,frozen recomputed with the corrected
#     convention n_2D = 2.20e28 m^-2 (the 23.2 MeV cited in v1 is revoked).
HBARC = 197.3269804        # MeV fm
M_N = 939.565
M_P = 938.272
M_E = 0.511
LZ_FM = 1.0                # areal-density conversion convention (explicit convention in v1.4 sec 3.4)
N_B_GRID = np.logspace(-8, 0, 41)   # fm^-3
N0 = 0.16                  # nuclear-matter saturation density fm^-3 (reference)
ZA_G0 = 0.522              # electron fraction per baryon (G0 v2 convention)
N_G0_B_FM3 = 0.04216       # G0 baryon density = N_B/L_z (F-R1B1-2)
N_G0_NUCLEI_FM3 = 0.004216  # document's "0.026*n_nuc" = nuclear density (convention reconciled)
N_E_FROZEN_FM3 = ZA_G0 * N_G0_B_FM3         # frozen-state electron density 0.02201 fm^-3
MU_G0_FROZEN_MEV = HBARC * (3.0 * math.pi ** 2 * N_E_FROZEN_FM3) ** (1.0 / 3.0)
N_B_DIAG = 0.026           # reviewer diagnostic anchor density (for cross-checks)
TH_BETA = 1e-6
TH_MU_LOW = 0.01
TH_PE_UR = 1e-3
TH_EF_N0 = 2.0             # T7: ideal-gas nucleon Fermi kinetic energy at n_0 near the literature anchor ~58 MeV
REP_POINTS = (1e-6, 1e-4, 1e-3, 0.004216, 0.01, 0.026, 0.04216, 0.1, 0.16, 0.3, 1.0)


def kF_of_n(n):
    return (3.0 * math.pi ** 2 * n) ** (1.0 / 3.0)


def p_of_n(n):
    """Momentum [MeV] = hbar*c*k_F (core of the F-R1B1-1 correction)."""
    return HBARC * kF_of_n(n)


def mu_electron(n):
    p = p_of_n(n)
    return math.sqrt(p * p + M_E * M_E)


def electron_uP(n):
    """Exact T=0 relativistic result: u, P [MeV/fm^3] (momentum p=hbar*c*k_F, including (hbar c)^-3)."""
    p = p_of_n(n)
    E = math.sqrt(p * p + M_E * M_E)
    lg = math.log((p + E) / M_E)
    hc3 = HBARC ** 3
    u = (1.0 / (8.0 * math.pi ** 2 * hc3)) * (p * (2 * p * p + M_E ** 2) * E
                                              - M_E ** 4 * lg)
    P = (1.0 / (24.0 * math.pi ** 2 * hc3)) * (p * (2 * p * p - 3 * M_E ** 2) * E
                                               + 3 * M_E ** 4 * lg)
    return u, P


def beta_solve(n_B):
    """Given n_B, solve for X_p: mu_n(mu_n) = mu_p + mu_e, charge neutrality n_e=n_p."""
    def f(X):
        n_p = X * n_B
        n_n = (1.0 - X) * n_B
        p_n = p_of_n(max(n_n, 1e-300))
        p_p = p_of_n(max(n_p, 1e-300))
        mu_n = M_N + p_n * p_n / (2.0 * M_N)
        mu_p = M_P + p_p * p_p / (2.0 * M_P)
        return mu_n - mu_p - mu_electron(n_p)
    lo, hi = 1e-12, 1.0 - 1e-12
    if f(hi) > 0:      # pure protons still not in beta equilibrium (should not happen)
        return 1.0, f(hi)
    if f(lo) < 0:
        return 0.0, f(lo)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    X = 0.5 * (lo + hi)
    return X, f(X)


def eos_point(n_B):
    X_p, res = beta_solve(n_B)
    n_p = X_p * n_B
    n_n = (1.0 - X_p) * n_B
    p_n = p_of_n(n_n)
    p_p = p_of_n(n_p)
    u_n = n_n * (M_N + 0.6 * (p_n * p_n / (2.0 * M_N)))
    u_p = n_p * (M_P + 0.6 * (p_p * p_p / (2.0 * M_P)))
    u_e, P_e = electron_uP(n_p)
    P_n = n_n * p_n * p_n / (5.0 * M_N)
    P_p = n_p * p_p * p_p / (5.0 * M_P)
    P = P_n + P_p + P_e
    eps = u_n + u_p + u_e
    return dict(n_B=n_B, X_p=X_p, X_n=1.0 - X_p, mu_e=mu_electron(n_p),
                beta_res=res, P=P, eps=eps, P_e=P_e, u_e=u_e,
                n_e=n_p, Ekin_n=p_n * p_n / (2.0 * M_N))


def main():
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("<<<LOG>>>")
    L = []
    w = L.append
    w("=" * 84)
    w("R1-B1 v2: beta-equilibrium EOS -- units/density/threshold corrected (review)")
    w("=" * 84)
    w("model: cold ideal npe gas; charge neutrality; beta equilibrium mu_n=mu_p+mu_e")
    w("registered: M_N=%.3f M_P=%.3f M_E=%.3f MeV, hbarc=%.4f MeV fm, L_z=%.1f fm"
      % (M_N, M_P, M_E, HBARC, LZ_FM))
    w("v2 corrections: (1) p=hbar*c*k_F everywhere; e-uP has (hbar*c)^-3;")
    w("  (2) G0 density basis: n_B=%.5f fm^-3 (baryon); doc '0.026*n_nuc'=%.6f fm^-3"
      % (N_G0_B_FM3, N_G0_NUCLEI_FM3))
    w("  (3) threshold convention: Q-table=kinetic (mu_e-m_e); equilibrium limit")
    w("      mu_e(n->0)=m_n-m_p=1.293 MeV total-convention (registered & tested)")
    w("thresholds (registered): |beta resid|<%.0e MeV; mu_e(n->1e-8)=1.293+/-%.3f;"
      % (TH_BETA, TH_MU_LOW))
    w("                         c_s^2<1 all scan; P monotone; P_e/u_e->1/3 |dev|<%.0e;" % TH_PE_UR)
    w("                         |Ekin_n(n0)-58.4|<%.1f MeV (ideal-gas literature anchor)" % TH_EF_N0)
    w("")

    w("[EOS scan: representative points]")
    w("  %-10s %-10s %-10s %-12s %-12s" % ("n_B[fm-3]", "X_p", "mu_e[MeV]", "P[MeV/fm3]",
                                          "P[Sigma N/m]"))
    rows = []
    for nB in N_B_GRID:
        rows.append(eos_point(nB))
    rep = {r["n_B"]: r for r in rows}
    for nB in REP_POINTS:
        # find the nearest grid point
        key = min(rep.keys(), key=lambda k: abs(math.log(k / nB)))
        r = rep[key]
        P2d = r["P"] * 1.602176634e-13 * 1e45 * LZ_FM * 1e-15       # N/m
        w("  %-10.3g %-10.3e %-10.3f %-12.4e %-12.3e"
          % (r["n_B"], r["X_p"], r["mu_e"], r["P"], P2d))

    # c_s^2 = dP/deps numerically
    nB_arr = np.array([r["n_B"] for r in rows])
    P_arr = np.array([r["P"] for r in rows])
    e_arr = np.array([r["eps"] for r in rows])
    cs2 = np.gradient(P_arr, e_arr)
    w("")
    w("[sound speed] c_s^2 = dP/deps (numeric, c=1): max=%.4f (must be <1), min=%.4f"
      % (float(np.max(cs2[cs2 > 0])), float(np.min(cs2[cs2 > 0]))))

    w("")
    w("[N7 bridge v2: same-density same-species comparison (F-R1B1-4)]")
    w("  frozen state: n_e=%.6e fm^-3 -> mu_e,frozen=%.2f MeV (G0 v2 corrected basis)"
      % (N_E_FROZEN_FM3, MU_G0_FROZEN_MEV))
    r_g0 = eos_point(N_G0_B_FM3)
    w("  beta-eq at n_B=%.5f fm^-3: X_p=%.4e, mu_e=%.2f MeV, n_e=%.4e fm^-3"
      % (N_G0_B_FM3, r_g0["X_p"], r_g0["mu_e"], r_g0["n_e"]))
    w("  same-species ratio: n_e,eq/n_e,frozen = %.3e ; mu_e,eq/mu_e,frozen = %.3f"
      % (r_g0["n_e"] / N_E_FROZEN_FM3, r_g0["mu_e"] / MU_G0_FROZEN_MEV))
    r_diag = eos_point(N_B_DIAG)
    w("  reviewer diagnostic anchor @n_B=0.026: X_p=%.3e (reviewer 1.07e-3), mu_e=%.2f MeV"
      % (r_diag["X_p"], r_diag["mu_e"]))
    w("  => electrons are captured and reduced by ~%.0e times rather than disappearing "
      "(F-R1B1-4: v1's comparison of n_e against n_B compares unlike species and is invalid); "
      % (N_E_FROZEN_FM3 / r_g0["n_e"])
      + "whether the residual electrons are negligible must be decided by the R1-B4 v2 energy spectrum")

    w("")
    w("[verdicts]")
    ok1 = max(abs(r["beta_res"]) for r in rows) < TH_BETA
    mu_low = eos_point(1e-8)["mu_e"]
    ok2 = abs(mu_low - (M_N - M_P)) < TH_MU_LOW   # equilibrium limit mu_e -> m_n-m_p = 1.293 (total convention)
    ok3 = bool(np.all(cs2[1:-1] < 1.0))
    ok4 = bool(np.all(np.diff(P_arr) > 0))
    # UR electron limit: test the Chandrasekhar integral directly on a pure electron gas
    # (beta-equilibrium electrons are dilute and NR, so this does not apply)
    u_t, P_t = electron_uP(1.0)     # p_F=610.5 MeV >> m_e (x=1195): x is even larger after the unit correction
    ok5 = abs(P_t / u_t - 1.0 / 3.0) < TH_PE_UR
    ok6 = (r_g0["mu_e"] < MU_G0_FROZEN_MEV) and (r_g0["n_e"] < N_E_FROZEN_FM3)
    ok7 = bool(all(r["X_p"] >= 0.0 for r in rows))
    # literature anchor: ideal-gas nucleon Fermi kinetic energy of pure neutron matter at n_0 ~58.4 MeV
    r_n0 = eos_point(N0)
    ok8 = abs(r_n0["Ekin_n"] - 58.4) < TH_EF_N0
    # reviewer diagnostic anchor: at n_B=0.026, X_p≈1.07e-3, mu_e≈18.5 MeV (evidence of convergence of independent recalculations)
    ok9 = (abs(r_diag["X_p"] - 1.07e-3) / 1.07e-3 < 0.15
           and abs(r_diag["mu_e"] - 18.5) < 1.5)
    w("  beta equilibrium residual < %.0e      : %.2e  %s" % (
        TH_BETA, max(abs(r["beta_res"]) for r in rows), "PASS" if ok1 else "FAIL"))
    w("  mu_e(n_B=1e-8) = m_n-m_p=1.293+/-%.3f  : %.4f  %s" % (
        TH_MU_LOW, mu_low, "PASS" if ok2 else "FAIL"))
    w("  c_s^2 < 1 across scan                 : max %.3e  %s" % (
        float(np.max(cs2[1:-1])), "PASS" if ok3 else "FAIL"))
    w("  P monotone increasing                 : %s" % ("PASS" if ok4 else "FAIL"))
    w("  UR limit P_e/u_e -> 1/3 (pure e-gas @1.0 fm^-3): %.6f  %s" % (
        P_t / u_t, "PASS" if ok5 else "FAIL"))
    w("  N7: mu_e,eq & n_e,eq < frozen values  : %.2f MeV / %.2e  %s" % (
        r_g0["mu_e"], r_g0["n_e"], "PASS" if ok6 else "FAIL"))
    w("  X_p >= 0 everywhere                   : %s" % ("PASS" if ok7 else "FAIL"))
    w("  literature anchor Ekin_n(n0) ~ 58.4   : %.2f MeV  %s" % (
        r_n0["Ekin_n"], "PASS" if ok8 else "FAIL"))
    w("  reviewer diagnostic @0.026 (X_p, mu_e): %.3e / %.2f  %s" % (
        r_diag["X_p"], r_diag["mu_e"], "PASS" if ok9 else "FAIL"))
    w("")
    w("[findings]")
    w("  F-R1B1-5: after the dimensional correction X_p rises from ~1e-5 to ~1e-3 and mu_e,eq from 1.29 to ~25 MeV --")
    w("            v1's conclusion that 'almost all electrons disappear' is revoked: electrons are reduced ~3e2-fold, not eliminated;")
    w("            the spectral status of the residual electrons is to be decided by R1-B4 v2 (excitation-gap convention).")
    P_g0_2d = r_g0["P"] * 1.602176634e-13 * 1e45 * LZ_FM * 1e-15
    w("  F-R1B1-6: the ideal npe gas at G0 density has P=%.3f MeV/fm^3 (areal pressure %.2e N/m)"
      % (r_g0["P"], P_g0_2d))
    w("            -- of the same order as the G0 v2 frozen electron-gas pressure 8.62e16 N/m; the final-state EOS remains model-level and unfrozen.")
    w("  F-R1B1-7: v1's OVERALL: PASS is revoked (runs/R1B/r1b1_eos_results_v1_REVOKED.txt);")
    w("            these v2 results may serve as a downstream baseline only after reviewer verification.")
    w("")
    allpass = all([ok1, ok2, ok3, ok4, ok5, ok6, ok7, ok8, ok9])
    w("R1-B1 v2 OVERALL: %s" % ("PASS" if allpass else "FAIL"))
    w("evidence level: MODEL RESULT (cold ideal npe gas; assumptions registered above)")
    print("\n".join(L))


if __name__ == "__main__":
    main()
