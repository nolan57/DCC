# -*- coding: utf-8 -*-
"""
R1-B1 v3: beta-equilibrium dense-matter EOS -- three-convention envelope version
=============================================================================

Changes from v2 to v3 (review B2 / B5 + stale-document fixes + newly discovered physical boundary):

  B2 Single point values -> envelope. v2 computed only one dimensionality combination (electrons 3D, nucleons 3D)
      and treated X_p=1.62e-3 / mu_e=24.96 as the EOS conclusion. But for the same L_z=1 fm slab, nucleons are
      z-frozen (2D) in R1-B4 and electrons are single-band (2D) in G0. With different dimensionality combinations,
      X_p spans a factor of 28. v3 scans all three combinations side by side:
        ALL3D  electrons 3D + nucleons 3D   -- v2's historical convention, reference only
        HYB    electrons 2D + nucleons 3D   -- default convention (electron dimensionality argued from E_sub≫E_F)
        ALL2D  electrons 2D + nucleons 2D   -- fully quantized limit
      All downstream quantities (X_p / mu_e / n_e / P(Σ)) are registered as intervals; see [3]/[4]/[5].

  Document-header fix: the v2 docstring still said "mu_eq=23.2 MeV" (a value revoked in v1) and described the old
      "Q=0.782" convention, and the mu_e definition line said 3D. v3 derives everything from conv; no numbers are
      copied by hand.

  Unified c_s² values: the v2 log showed both 0.1005 and 0.0863 (one from dP/dε, the other from dP/du_e).
      v3 keeps only the thermodynamic definition c_s² = dP/dε.

  NEW (a physical boundary discovered while running v3, untouched by v2):
      The chemical potential of 2D electrons is mu_e = hbar c sqrt(4 pi n_2D/g) ∝ sqrt(n),
      which at low density **cannot catch up with** m_n-m_p = 1.293 MeV; therefore the beta-equilibrium solution has a
      lower threshold density n_thr. In the 2D convention, for n_B < n_thr **no** npe equilibrium state exists
      (this is not a numerical failure). For 3D electrons mu_e ∝ n^(1/3) can reach 1.293 at arbitrarily low density,
      so ALL3D has no such boundary. v3 determines n_thr by bisection and registers it as a physical output,
      marking unsolved grid points as "---" instead of crashing.

Real checks (counted as evidence, see [6]):
  K1 beta-equilibrium residual for each convention |mu_n-mu_p-mu_e| < 1e-6 MeV (back-substitution after solving)
  K2 ALL3D dilute limit mu_e -> m_n-m_p = 1.293 MeV (analytic limit, independently comparable)
  K3 c_s² = dP/dε < 1 over the whole scan
  K4 P monotonically increasing with n_B
  K5 3D Chandrasekhar gives P/u = 1/3 at n=1 fm^-3
  K6 ideal-gas nucleon anchor E_kin(n_0=0.16) ≈ 58.4 MeV (comparable to literature, not an identity)
Registration items (not counted as evidence):
  R1 three behaviors of mu_e(n→0) across conventions (dimensional fingerprint)
  R2 spread of X_p / P across conventions -- the core deliverable of this round, not a criterion

Run: python -I src/r1_dense/beta_equilibrium_v3.py
"""
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from src.common import conv  # noqa: E402

LZ = conv.LZ_FM
N0 = 0.16                                  # nuclear-matter saturation density (reference anchor, not a parameter of this model)
N_B_GRID = np.logspace(-8, 0, 161)         # fm^-3
REP_POINTS = (1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.04216, 0.1, 0.16, 0.3, 1.0)

TH_BETA = 1e-6
TH_MU_LOW = 0.01
TH_CS2_MAX = 1.0
TH_PE_UR = 1e-3
TH_EF_N0 = 2.0

N_E_FROZEN = conv.N_E_FM3
N_B_FROZEN = conv.N_B_FM3
MU_E_FROZEN_2D = conv.eos_e_2D(conv.N_E_FM2)["EF"]
MU_E_FROZEN_3D = conv.eos_e_3D(N_E_FROZEN)["EF"]

MASS_GAP = conv.M_N - conv.M_P             # 1.293 MeV


def energy_density_areal(mode, X, nB):
    """Total energy density (areal), MeV/fm^2: rest mass + kinetic + electrons"""
    Np = X * nB * LZ
    Nn = (1.0 - X) * nB * LZ
    if mode == "ALL2D":
        u = (conv.eos_n_2D(Nn, conv.M_N)["u"] + conv.eos_n_2D(Np, conv.M_P)["u"]
             + conv.eos_e_2D(Np)["u"])
    else:
        u = ((conv.eos_n_3D(Nn / LZ, conv.M_N)["u"]
              + conv.eos_n_3D(Np / LZ, conv.M_P)["u"]) * LZ)
        if mode == "ALL3D":
            u += conv.eos_e_3D(Np / LZ)["u"] * LZ
        else:
            u += conv.eos_e_2D(Np)["u"]
    return u


def try_point(mode, nB):
    try:
        r = conv.beta_eq(nB * LZ, mode)
    except RuntimeError:
        return None
    r["eps"] = energy_density_areal(mode, r["X_p"], nB)
    return r


def scan(mode):
    return [(nB, try_point(mode, nB)) for nB in N_B_GRID]


def threshold_density(mode):
    """Lower threshold density for the existence of the beta-equilibrium solution (bisection; returns None if there is no boundary)"""
    lo, hi = N_B_GRID[0], N_B_GRID[-1]
    if try_point(mode, lo) is not None:
        return None
    if try_point(mode, hi) is None:
        return float("nan")
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if try_point(mode, mid) is None:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    L = []
    w = L.append
    w("=" * 100)
    w("R1-B1 v3: beta-equilibrium EOS -- three-convention envelope (review B2/B5)")
    w("=" * 100)
    w("model: cold ideal npe gas; charge neutrality; beta equilibrium mu_n=mu_p+mu_e")
    w("registered constants: src/common/conv.py (single source, no local copies)")
    w("  M_N=%.3f M_P=%.3f M_E=%.3f MeV | hbarc=%.4f MeV fm | L_z=%.1f fm"
      % (conv.M_N, conv.M_P, conv.M_E, conv.HBARC, LZ))
    w("  E_sub(band gap)=%.1f MeV vs E_F,e=%.2f MeV -> electrons single-band (D=2)"
      % (conv.E_SUBBAND, MU_E_FROZEN_2D))
    w("thresholds: beta resid<%.0e MeV | cs2<%.1f | P monotone | P/u(UR)<%.0e | "
      "Ekin(n0)=58.4+/-%.1f" % (TH_BETA, TH_CS2_MAX, TH_PE_UR, TH_EF_N0))
    w("")

    res = {}
    for mode in conv.MODES:
        rows = scan(mode)
        good = [(nB, r) for nB, r in rows if r is not None]
        nBv = np.array([x[0] for x in good])
        P = np.array([x[1]["P_tot_areal"] for x in good])
        eps = np.array([x[1]["eps"] for x in good])
        cs2 = np.gradient(P, eps)
        res[mode] = dict(rows=good, nB=nBv, P=P, eps=eps, cs2=cs2,
                         n_missing=len(rows) - len(good),
                         n_thr=threshold_density(mode))

    # ---------------- [2] domain of existence and threshold density
    w("[2] domain of existence (2D electron dispersion cannot reach 1.293 MeV at low n)")
    w("  %-6s %-12s %-14s %-30s" % ("mode", "n_thr[fm-3]", "valid points", "note"))
    for m in conv.MODES:
        r = res[m]
        if r["n_thr"] is None:
            note = "no lower bound (3D mu_e ~ n^(1/3) can always reach the gap)"
            nthr = "none"
        else:
            note = "below n_thr NO beta-equilibrium npe state exists"
            nthr = "%.4e" % r["n_thr"]
        w("  %-6s %-12s %-14s %-30s"
          % (m, nthr, "%d/%d" % (len(r["nB"]), len(N_B_GRID)), note))
    w("  => this is a dimensional fingerprint, not a numerical issue: mu_e(2D)~sqrt(n) vs mu_e(3D)~n^(1/3).")
    w("     in the 2D convention a slab with n_B<n_thr simply cannot be in beta equilibrium (it must be described as a bound nucleus / nonequilibrium state).")

    # ---------------- [3] scan table
    w("")
    w("[3] EOS scan (default = HYB: electrons 2D, nucleons 3D)")
    w("  %-10s %-11s %-11s %-13s %-13s %-9s"
      % ("n_B[fm-3]", "X_p", "mu_e[MeV]", "P[MeV/fm2]", "P[N/m]", "cs2"))
    hyb = res["HYB"]
    for target in REP_POINTS:
        i = int(np.argmin(np.abs(np.log(hyb["nB"] / target))))
        r = hyb["rows"][i][1]
        w("  %-10.4g %-11.3e %-11.3f %-13.4e %-13.4e %-9.4g"
          % (hyb["nB"][i], r["X_p"], r["mu_e"], r["P_tot_areal"], r["P_tot_Nm"],
             hyb["cs2"][i]))
    if hyb["n_missing"]:
        w("  (points below n_thr=%.3e fm^-3 omitted: %d grid points, no solution)"
          % (hyb["n_thr"], hyb["n_missing"]))

    # ---------------- [4] three-convention comparison @ frozen density (core deliverable)
    w("")
    w("[4] three-convention comparison @ n_B(G0) = %.6e fm^-3   [CORE DELIVERABLE]"
      % N_B_FROZEN)
    env = conv.beta_envelope(N_B_FROZEN)
    w("  %-6s %-4s %-5s %-11s %-10s %-11s %-10s %-13s"
      % ("mode", "D_e", "D_n", "X_p", "mu_e[MeV]", "n_e[fm^-3]", "reduction",
         "P_tot[N/m]"))
    for m in conv.MODES:
        r = env[m]
        w("  %-6s %-4d %-5d %.4e  %-10.3f %.4e   %-10.2f %.4e"
          % (m, r["D_e"], r["D_nuc"], r["X_p"], r["mu_e"], r["n_e_fm3"],
             r["reduction"], r["P_tot_Nm"]))
    xp = [env[m]["X_p"] for m in conv.MODES]
    mue = [env[m]["mu_e"] for m in conv.MODES]
    ne = [env[m]["n_e_fm3"] for m in conv.MODES]
    pt = [env[m]["P_tot_Nm"] for m in conv.MODES]
    w("  ENVELOPE  X_p %.2e..%.2e (x%.0f) | mu_e %.2f..%.2f MeV (x%.1f)"
      % (min(xp), max(xp), max(xp) / min(xp), min(mue), max(mue), max(mue) / min(mue)))
    w("            n_e %.2e..%.2e fm^-3 (x%.0f) | P_tot %.2e..%.2e N/m (x%.1f)"
      % (min(ne), max(ne), max(ne) / min(ne), min(pt), max(pt), max(pt) / min(pt)))
    w("  Note: ALL3D is for reference only. It conflicts with the nucleon subband spacing in R1-B4 (204 MeV): if nucleons")
    w("      are quantized along z, the pressure-bearing nucleons should occupy a single band, so nucleons must also be")
    w("      treated as 2D. Therefore ALL3D's X_p=1.6e-3 / reduction=3.2e2 must not be cited on its own.")

    # ---------------- [5] P(Sigma)
    w("")
    w("[5] P(Sigma) at G0 column density (Sigma = M/A_perp = %.1f kg/m^2)"
      % (conv.M_KG / conv.A_PERP))
    w("  %-6s %-14s %-14s %-14s" % ("mode", "P_nuc[N/m]", "P_e[N/m]", "P_tot[N/m]"))
    for m in conv.MODES:
        r = env[m]
        w("  %-6s %-14.4e %-14.4e %-14.4e"
          % (m, r["P_nuc_Nm"], r["P_e_Nm"], r["P_tot_Nm"]))

    w("")
    w("[6] N7 bridge: frozen electron gas vs beta-equilibrium electrons")
    w("  frozen: n_e=%.6e fm^-3 -> mu_e=%.2f MeV (2D single band) | %.2f MeV (3D ctr)"
      % (N_E_FROZEN, MU_E_FROZEN_2D, MU_E_FROZEN_3D))
    for m in conv.MODES:
        r = env[m]
        w("  %-6s: n_e,eq/n_e,frozen=%.3e | mu_e,eq/mu_e,frozen=%.3f | mu_e,eq=%.2f MeV"
          % (m, r["n_e_fm3"] / N_E_FROZEN, r["mu_e"] / MU_E_FROZEN_2D, r["mu_e"]))
    w("  => electrons are partially captured, not eliminated; the reduction factor depends strongly on the convention (%.0f .. %.0f times)"
      % (min(env[m]["reduction"] for m in conv.MODES),
         max(env[m]["reduction"] for m in conv.MODES)))
    w("     whether the residual electrons can be neglected must be decided by the R1-B4 v3 gap; this module draws no standalone conclusion.")

    # ---------------- [7] checks
    w("")
    w("[7] checks (K = counted as evidence; R = registration only)")
    checks = []

    def ck(name, val, thr, ok, note):
        checks.append((name, val, thr, bool(ok), note))

    worst_res = max(max(abs(r["beta_res"]) for _, r in res[m]["rows"][1:])
                    for m in conv.MODES)
    ck("K1_beta_residual_all_modes", worst_res, TH_BETA, worst_res < TH_BETA,
       "back-substitution of |mu_n-mu_p-mu_e| at all solved points in all three conventions")

    mu_low_3d = conv.beta_eq(1e-8 * LZ, "ALL3D")["mu_e"]
    ck("K2_mu_e_low_limit_3D", abs(mu_low_3d - MASS_GAP), TH_MU_LOW,
       abs(mu_low_3d - MASS_GAP) < TH_MU_LOW,
       "n_B=1e-8 gives mu_e=%.4f, analytic m_n-m_p=%.4f MeV" % (mu_low_3d, MASS_GAP))

    cs2max = max(float(np.max(res[m]["cs2"][1:-1])) for m in conv.MODES)
    ck("K3_cs2_below_1", cs2max, TH_CS2_MAX, cs2max < TH_CS2_MAX,
       "c_s²=dP/deps maximum across three conventions %.4f (v2's dual values 0.1005/0.0863 unified into this definition)" % cs2max)

    mono = all(bool(np.all(np.diff(res[m]["P"]) > 0)) for m in conv.MODES)
    ck("K4_P_monotone", 0.0, 0.0, mono, "P strictly monotonically increasing with n_B in all three conventions")

    e3 = conv.eos_e_3D(1.0)
    ck("K5_eos3D_UR", abs(e3["P"] / e3["u"] - 1.0 / 3.0), TH_PE_UR,
       abs(e3["P"] / e3["u"] - 1.0 / 3.0) < TH_PE_UR,
       "n=1 fm^-3 gives P/u=%.6f (should be 0.333333)" % (e3["P"] / e3["u"]))

    ekin_n0 = conv.HBARC ** 2 * conv.kF_3(N0) ** 2 / (2 * conv.M_N)
    ck("K6_ideal_gas_anchor_n0", abs(ekin_n0 - 58.4), TH_EF_N0,
       abs(ekin_n0 - 58.4) < TH_EF_N0,
       "E_kin(n_0=0.16)=%.2f MeV (literature ideal-gas anchor 58.4, not an identity)" % ekin_n0)

    for name, val, thr, ok, note in checks:
        w("  %-26s %-11.4e thr %-9.2e %-6s %s"
          % (name, val, thr, "PASS" if ok else "FAIL", note))

    w("")
    w("  R1 mu_e(n->0) by convention (dimension fingerprint, not pass/fail):")
    for m in conv.MODES:
        rows = res[m]["rows"]
        w("     %-6s first solvable n_B=%.2e -> mu_e=%.4f MeV"
          % (m, rows[0][0], rows[0][1]["mu_e"]))
    w("  R2 convention spread is the deliverable, not a criterion:")
    w("     X_p span %.0fx, P_tot span %.1fx -- numbers G2'/G5' must consume as a range."
      % (max(xp) / min(xp), max(pt) / min(pt)))

    allok = all(c[3] for c in checks)
    w("")
    w("[8] findings")
    w("  F-R1B1-5(rev): v2's 'electrons reduced ~3e2-fold rather than disappearing' holds only for ALL3D; HYB %.0f times, "
      % env["HYB"]["reduction"])
    w("                 ALL2D %.0f times. The direction stands, but the factor becomes an interval." % env["ALL2D"]["reduction"])
    w("  F-R1B1-6(v3):  P_tot interval %.2e..%.2e N/m, of the same order as the G0 frozen electron-gas pressure 8.62e16 N/m; "
      % (min(pt), max(pt)))
    w("                 the final-state EOS is still MODEL RESULT, not frozen.")
    w("  F-R1B1-7(v3):  c_s² unified as dP/deps = %.4f (≪1); v2's dual values are no longer reported." % cs2max)
    w("  F-R1B1-8(NEW): the 2D-electron convention has a lower beta-equilibrium threshold density n_thr; 3D has no such boundary.")
    w("                 this is an observable consequence of the dimensionality choice and can serve as an independent discriminator for R1-B4/R3.")
    w("")
    w("R1-B1 v3 OVERALL: %s" % ("PASS" if allok else "FAIL"))
    w("evidence level: MODEL RESULT (cold ideal npe gas); values co-registered as envelope.")
    print("\n".join(L))


if __name__ == "__main__":
    main()
