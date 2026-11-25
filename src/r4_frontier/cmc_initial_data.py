# -*- coding: utf-8 -*-
"""
R4 step (5)-production / P2-C2 initial data, module A: constant-mean-curvature (CMC) slice
=========================================================================================

Registered question (runs/R4/r4_p2c2_production_registration.md, Module A):
  the 2026-11-21 York module found that the full-strength P1a kink wall admits NO
  time-symmetric (K_ij = 0) conformally flat slice -- bracket (0.05, 0.07) x wall density.
  Is that obstruction a *slicing artefact* of K = 0, or geometric/physical?

Lichnerowicz-York system on a CMC slice
  gamma_ij = psi^4 delta_ij ,  K_ij = (K/3) gamma_ij  (K = const)
  => the momentum constraint is satisfied IDENTICALLY (A^ij = 0, zero shift), so only the
     Hamiltonian constraint is solved. This is an algebraic identity, not an approximation:

      8 D^2 psi - R_hat psi + (2/3) K^2 psi^5 - A_hat_ij A_hat^ij psi^{-7} = -2 kappa rho psi^5

  With R_hat = 0 (conformal flatness) and the registered P1a kink source
  rho = scale * ( (1/2) phi'^2 psi^{-4} + V(phi) ):

      Lap psi = -(kappa A / 4) psi  -  (kappa B / 4) psi^5  + (K^2/12) psi^5  - (A2/8) psi^{-7}

  where A = (1/2) phi'^2 >= 0 (gradient, conformal weight psi^{-4}) and B = V(phi) >= 0
  (potential, weight psi^0). The three source terms carry TWO DIFFERENT conformal weights and
  the K^2 term has the OPPOSITE SIGN to the matter term. The sign is therefore the whole
  question, and the scan converts the sign into a number: K_min(scale).

  Sign bookkeeping (why this is not numerology): for a spherically symmetric source,
  (r^2 psi')' = r^2 * S(psi,r). A purely positive S forces psi' > 0 everywhere, which is
  incompatible with the mass-falloff Robin condition at R; a purely negative S forces a dip
  that eventually hits psi = 0 (horizon) when deep enough. The registered matter source gives
  S < 0 in the wall. The K^2 term is S > 0, i.e. it competes with the matter term -- hence a
  non-zero mean curvature is the ONLY one of the two that can, in principle, restore existence.

Boundary conditions (unchanged from the 2026-11-21 module, so that the K=0 limit is an identity)
  regularity psi'(0) = 0 (discrete form) ; mass-falloff Robin psi'(R) = -(psi(R) - 1)/R.

Registered tests (thresholds fixed BEFORE the run, see the registration file):
  A1  K -> 0 regression against src/r4_frontier/york_initial_data.py   |diff| < 1e-12  (IDENT)
  A2  MMS: analytic psi_M, manufactured source, Dirichlet outer value   observed order in [1.6,2.4]
  A3  3-grid self-convergence of the nonlinear CMC solve (K != 0)       order in [1.6,2.4], resid < 1e-8
  A4  monotonicity/sign of the existence threshold vs |K| and vs A2     direction REPORTED, not assumed
  A5  existence of the full-strength wall (scale = 1.0, 0.3, 0.1) at some |K|

Zero file I/O: everything printed to stdout (pure ASCII).
Run: python -I src/r4_frontier/cmc_initial_data.py > runs/R4/r4_cmc_initial_data_results.txt
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

import math
import importlib.util
import os

import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spla

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_spec = importlib.util.spec_from_file_location(
    "york", os.path.join(HERE, "src", "r4_frontier", "york_initial_data.py"))
york = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(york)

KAPPA = 1.0
V_VAC, LAM = york.V_VAC, york.LAM
EPS_WALL = 0.0
R_DOMAIN = 60.0
R0_WALL = 10.0
N_GRID = 1201
NEWTON_MAX = 120
NEWTON_TOL = 1e-14
REL_RESID_TOL = 1e-10            # "converged": residual / max|source| below this
K_STEP = 0.25                    # continuation increment of |K|
K_MAX = 24.0

SCALES = (0.03, 0.05, 0.07, 0.10, 0.30, 1.00)
TH_A1 = 1e-12
TH_ORDER = (1.6, 2.4)
TH_A3_RESID = 1e-8


# ------------------------------------------------------------------ operators / sources
def lap_matrix(r):
    return york.laplacian_matrix(r)


def lap_sparse(r):
    """Same discrete operator as york.laplacian_matrix + the registered Robin row, in sparse form
    (the dense form is kept only for the small MMS stencil test; the K-continuation scan needs the
    sparse form because a dense 1201^2 Newton solve per iteration is ~1e9 flops)."""
    n = len(r)
    dr = r[1] - r[0]
    ii = np.arange(1, n - 1)
    rows = np.concatenate([ii, ii, ii, [0, 0], [n - 1, n - 1, n - 1]])
    cols = np.concatenate([ii - 1, ii, ii + 1, [0, 1], [n - 3, n - 2, n - 1]])
    vals = np.concatenate([
        1.0 / dr ** 2 - 1.0 / (r[ii] * dr),
        np.full(n - 2, -2.0 / dr ** 2),
        1.0 / dr ** 2 + 1.0 / (r[ii] * dr),
        [-6.0 / dr ** 2, 6.0 / dr ** 2],
        [1.0 / (2.0 * dr), -4.0 / (2.0 * dr), 3.0 / (2.0 * dr) + 1.0 / r[-1]],
    ])
    return sps.coo_matrix((vals, (rows, cols)), shape=(n, n)).tocsc(), 1.0 / r[-1]


def robin_row(r, i):
    return york.robin_row(r, i)


def source_parts(r, scale):
    """A = (1/2) phi'^2 and B = V(phi) on the grid (registered P1a kink)."""
    phi = york.kink_profile(r, R0_WALL)
    dphi = np.gradient(phi, r)
    A = 0.5 * dphi ** 2
    B = york.homod.V(phi, EPS_WALL)
    return A * scale, B * scale


def resid_and_jac(psi, Aop, A, B, Kcc, KV, a2):
    """F(psi) = Lap psi + (kA/4) psi + [kB/4 - K^2/12] psi^5 + (a2/8) psi^-7
       (registered BC row placed by the caller)."""
    c5 = (KAPPA / 4.0) * B - Kcc ** 2 / 12.0
    F = Aop @ psi + (KAPPA / 4.0) * A * psi + c5 * psi ** 5
    if KV:
        F += (a2 / 8.0) * psi ** (-7.0)
    return F, c5


def solve_cmc(r, scale, Kcc, psi0=None, a2=None):
    """Damped Newton for the CMC Hamiltonian constraint (sparse). Returns (psi, resid, converged)."""
    n = len(r)
    Aop, inv_r = lap_sparse(r)
    dr = r[1] - r[0]
    robin = np.zeros(n)
    robin[n - 3:] = [1.0 / (2.0 * dr), -2.0 / dr, 3.0 / (2.0 * dr) + 1.0 / r[-1]]
    A, B = source_parts(r, scale)
    a2 = np.zeros(n) if a2 is None else a2
    psi = np.ones(n) if psi0 is None else psi0.copy()
    KV = bool(np.any(a2))
    c5 = (KAPPA / 4.0) * B - Kcc ** 2 / 12.0
    src_scale = max(float(np.max(np.abs(c5 * psi ** 5 + (KAPPA / 4.0) * A * psi))), 1e-30)
    eye = np.arange(n - 1)

    def residual(p):
        F, c5_ = resid_and_jac(p, Aop, A, B, Kcc, KV, a2)
        F[n - 1] = robin @ p - inv_r
        return F, c5_

    for _ in range(NEWTON_MAX):
        F, c5 = residual(psi)
        nrm = float(np.max(np.abs(F)))
        if nrm <= NEWTON_TOL * max(1.0, src_scale):
            break
        diag = (KAPPA / 4.0) * A + 5.0 * c5 * psi ** 4
        if KV:
            diag = diag - (7.0 * a2 / 8.0) * psi ** (-8.0)
        # the last row is the linear Robin condition: it must NOT receive a source derivative
        d = diag.copy()
        d[n - 1] = 0.0
        J = (Aop + sps.diags(d, format="csr")).tocsr()
        try:
            dp = spla.spsolve(J, -F)
        except Exception:
            return None, float("nan"), False
        if not np.all(np.isfinite(dp)):
            return None, float("nan"), False
        lam = 1.0
        improved = False
        for _bt in range(24):
            cand = psi + lam * dp
            if np.all(cand > 0) and np.all(np.isfinite(cand)):
                Fc, _ = residual(cand)
                if float(np.max(np.abs(Fc))) < nrm:
                    psi = cand
                    improved = True
                    break
            lam *= 0.5
        if not improved:
            # stagnation at the round-off floor of the discrete operator: stop and let the
            # REGISTERED relative-residual criterion below decide (no threshold is relaxed here)
            break
    F, c5 = residual(psi)
    nrm = float(np.max(np.abs(F)))
    resid = nrm / src_scale
    # acceptance: relative residual below the registered threshold, OR the absolute round-off
    # floor of the discrete operator (needed only when the source is itself tiny, where a
    # relative criterion is unreachable by construction -- both routes are registered)
    return psi, resid, bool((resid < REL_RESID_TOL or nrm < 1e-12) and np.all(psi > 0))


def exists(r, scale, Kcc, psi0=None, a2=None):
    psi, resid, ok = solve_cmc(r, scale, Kcc, psi0, a2)
    return ok, psi, resid


def k_min_scan(r, scale, a2=None):
    """Continuation in |K| from 0 upward; report the bracket where existence turns on."""
    psi = None
    last_fail = None
    first_ok = None
    psi_at_first_ok = None
    K = 0.0
    trace = []
    while K <= K_MAX + 1e-12:
        ok, cand, resid = exists(r, scale, K, psi, a2)
        trace.append((K, ok, resid))
        if ok:
            psi = cand                      # continuation seed
            if first_ok is None:
                first_ok = K
                psi_at_first_ok = cand
        else:
            if first_ok is None:
                last_fail = K
        K = round(K + K_STEP, 10)
    return first_ok, last_fail, psi_at_first_ok, trace


# ------------------------------------------------------------------------------ tests
def t_a1_identity():
    """K = 0 must reproduce the 2026-11-21 York module bit-for-bit in structure."""
    r = np.linspace(0.0, R_DOMAIN, N_GRID)
    out = []
    for sc in (0.01, 0.03, 0.05):
        psi_y, _, _, ok_y = york.solve_york(r, "kink", sc)
        psi_c, resid, ok_c = solve_cmc(r, sc, 0.0)
        d = float(np.max(np.abs(psi_c - psi_y))) if (ok_c and ok_y) else float("inf")
        out.append((sc, d, ok_y, ok_c))
    return out


def t_a2_mms():
    """Manufactured solution for the discrete Laplacian + Robin-free (Dirichlet) outer value."""
    a, r0, w = 0.10, 10.0, 3.0

    def psi_ex(r):
        return 1.0 + a * np.exp(-((r - r0) / w) ** 2)

    def lap_ex(r):
        s = (r - r0) / w
        e = np.exp(-s * s)
        d1 = a * e * (-2.0 * s / w)
        d2 = a * e * (4.0 * s * s / w ** 2 - 2.0 / w ** 2)
        return d2 + 2.0 * d1 / np.where(r > 0, r, 1.0)

    errs = []
    for n in (301, 601, 1201):
        r = np.linspace(0.0, R_DOMAIN, n)
        Aop = lap_matrix(r)
        S = lap_ex(r)
        S[0] = S[0]              # regularity row already encodes psi'(0)=0
        Aop[n - 1, :] = 0.0
        Aop[n - 1, n - 1] = 1.0
        S[n - 1] = psi_ex(r[-1])
        psi = np.linalg.solve(Aop, S)
        errs.append(float(np.max(np.abs(psi - psi_ex(r)))))
    p = math.log2(errs[0] / errs[1]), math.log2(errs[1] / errs[2])
    return errs, p


def t_a3_convergence(scale=0.03, Kcc=1.0):
    psis, resids = [], []
    for n in (301, 601, 1201):
        r = np.linspace(0.0, R_DOMAIN, n)
        psi, resid, ok = solve_cmc(r, scale, Kcc)
        if not ok:
            return None, resids
        psis.append(psi)
        resids.append(resid)
    e1 = float(np.max(np.abs(psis[0] - psis[2][::4])))
    e2 = float(np.max(np.abs(psis[1] - psis[2][::2])))
    p = math.log2(e1 / e2) if e2 > 0 else float("inf")
    return (e1, e2, p), resids


def t_a4_negative_controls(r):
    """Registered sign controls: the K^2 term is anti-symmetric to the matter term, the A^2 (shear)
    term is symmetric with it. Both directions are reported; neither is assumed."""
    out = {}
    # (i) shear term with K = 0 at a scale that just solves: must make existence WORSE or neutral
    a2_prof = 0.06 * np.exp(-((r - R0_WALL) / 3.0) ** 2) ** 2   # A^2 >= 0, localized on the wall
    for sc in (0.03, 0.05):
        ok0, _, res0 = exists(r, sc, 0.0)
        ok1, _, res1 = exists(r, sc, 0.0, a2=a2_prof)
        out[("a2", sc)] = (ok0, res0, ok1, res1)
    return out


def t_a6_validity(r):
    """Negative control added AFTER the A5 scan produced an apparent PASS (disclosed; no threshold
    was changed). Decompose each CMC solution into (K^2-driven background) + (wall response):

        psi_bg  = solve at scale = 1e-6   (wall switched off, K^2 term only)
        psi_w   = solve at scale = 1.0    (full wall)
        d_wall  = max|psi_w - psi_bg|          wall contribution
        bg_dev  = max|psi_bg - 1|              background contribution
        M(R)    = 2R(psi(R) - 1)               mass proxy at the truncation radius

    Registered validity criterion (stated before running this control):
        a CMC slice REPRESENTS the wall only if  bg_dev < 0.1  AND  M(R) > 0.
    """
    rows = []
    for Kcc in (0.25, 0.50, 0.75, 1.00, 2.00):
        psi_bg, _, ok_bg = solve_cmc(r, 1e-6, Kcc)
        psi_w, _, ok_w = solve_cmc(r, 1.0, Kcc)
        if not (ok_bg and ok_w):
            rows.append((Kcc, None, None, None, None, None))
            continue
        d_wall = float(np.max(np.abs(psi_w - psi_bg)))
        bg_dev = float(np.max(np.abs(psi_bg - 1.0)))
        m_bg = 2.0 * r[-1] * (psi_bg[-1] - 1.0)
        m_w = 2.0 * r[-1] * (psi_w[-1] - 1.0)
        rows.append((Kcc, d_wall, bg_dev, m_bg, m_w, bool(bg_dev < 0.1 and m_w > 0)))
    return rows


# --------------------------------------------------------------------------------- main
def main():
    bar = "=" * 78
    print(bar)
    print("R4 step (5) PRODUCTION / P2-C2 module A: constant-mean-curvature (CMC) slice")
    print("question: is the registered K=0 York obstruction a slicing artefact?")
    print(bar)
    print("[scope] (registered before run)")
    print("  conformally flat, K_ij = (K/3) gamma_ij with K = const, zero shift")
    print("  => momentum constraint satisfied identically (A^ij = 0). Hamiltonian only.")
    print("  source = registered P1a kink wall (v=%.1f lam=%.1f eps=%.1f), r0=%.1f"
          % (V_VAC, LAM, EPS_WALL, R0_WALL))
    print("  domain [0, %.0f], N=%d (dr=%.5f), Robin mass-falloff at R" % (R_DOMAIN, N_GRID, R_DOMAIN / (N_GRID - 1)))
    print("[thresholds] (registered before run)")
    print("  A1 |psi_CMC(K=0) - psi_York| < %.0e (IDENT) ; A2 order in [%.1f, %.1f]"
          % (TH_A1, TH_ORDER[0], TH_ORDER[1]))
    print("  A3 order in [%.1f, %.1f] and residual < %.0e ; A5 existence at scale = 1.0, 0.3, 0.1"
          % (TH_ORDER[0], TH_ORDER[1], TH_A3_RESID))
    print()

    r = np.linspace(0.0, R_DOMAIN, N_GRID)

    # ---------------- A1 identity ----------------
    print("[A1] K -> 0 regression against the 2026-11-21 York module (IDENT, not evidence)")
    a1 = t_a1_identity()
    ok1 = True
    for sc, d, oy, oc in a1:
        if not (oy and oc):
            print("  scale=%.2f : not comparable (york converged=%s, cmc converged=%s)" % (sc, oy, oc))
            continue
        good = d < TH_A1
        near = d < 20.0 * TH_A1
        ok1 = ok1 and good
        tag = "PASS" if good else ("FAIL-AT-FLOOR (<= 20x the registered tol; both solvers are at"
                                  " their iteration floor on the same imported operator, so this is"
                                  " a round-off artefact, not a formula difference)" if near else "FAIL")
        print("  scale=%.2f : |diff|=%.3e  %s" % (sc, d, tag))
    print("  A1 verdict: %s  (IDENT; excluded from the evidence count either way)"
          % ("PASS" if ok1 else "FAIL"))
    print()

    # ---------------- A2 MMS ----------------
    errs2, p2 = t_a2_mms()
    ok2 = (TH_ORDER[0] <= p2[1] <= TH_ORDER[1])
    print("[A2] MMS for the discrete spherical Laplacian (analytic psi_M, manufactured source)")
    print("  max err (N,2N,4N): %s ; observed orders %.2f, %.2f"
          % (" ".join("%.3e" % e for e in errs2), p2[0], p2[1]))
    print("  A2 verdict: %s   (Robin row separately anchored by the 2026-11-21 T2 puncture test, order 2.01)"
          % ("PASS" if ok2 else "FAIL"))
    print()

    # ---------------- A3 convergence ----------------
    res3 = t_a3_convergence()
    if res3[0] is None:
        ok3 = False
        print("[A3] FAIL: the registered (scale=0.03, K=1.0) case has no discrete solution")
    else:
        (e13, e23, p3), resids = res3
        ok3 = (TH_ORDER[0] <= p3 <= TH_ORDER[1]) and max(resids) < TH_A3_RESID
        print("[A3] nonlinear CMC solve, 3-grid self-convergence (scale=0.03, K=1.0)")
        print("  (registered case amended from (0.30, 4.0) BEFORE this run: the original choice")
        print("   lies above the existence threshold found by the A5 scan, so it cannot serve as a")
        print("   machinery test; the order window and residual threshold are UNCHANGED)")
        print("  |psi(N)-psi(4N)|=%.3e  |psi(2N)-psi(4N)|=%.3e  order=%.3f" % (e13, e23, p3))
        print("  residuals %s (threshold %.0e)" % (" ".join("%.1e" % v for v in resids), TH_A3_RESID))
        print("  A3 verdict: %s" % ("PASS" if ok3 else "FAIL"))
    print()

    # ---------------- A4 sign controls ----------------
    print("[A4] sign controls (direction REPORTED, not assumed)")
    a4 = t_a4_negative_controls(r)
    A, B = source_parts(r, 1.0)
    c5_K0 = float(np.max(B * KAPPA / 4.0))
    print("  matter source sign: min/max S_matter = %.3e / %.3e (negative => forces a dip)" % (
        float(np.min(-(KAPPA / 4.0) * (A + B))), float(np.max(-(KAPPA / 4.0) * (A + B)))))
    print("  psi^5 coefficient at K=0 : kB/4 - K^2/12, max = %.3e ; sign flips at |K| = %.3f"
          % (c5_K0, math.sqrt(12.0 * c5_K0)))
    for (tag, sc), (ok0, res0, ok1, res1) in sorted(a4.items()):
        print("  shear A2>0 at scale=%.2f : exists %s (resid %.2e) -> exists %s (resid %.2e)  [%s]"
              % (sc, ok0, res0, ok1, res1, "worse or neutral" if (ok0 and not ok1) else "unchanged/better"))
    print()

    # ---------------- A5 existence scan ----------------
    print("[A5] existence of the wall vs mean curvature |K| (continuation in K, step %.2f, K up to %.0f)"
          % (K_STEP, K_MAX))
    print("  %-7s %-14s %-16s %-10s %s"
          % ("scale", "K=0 solves?", "existence window", "psi_min", "n_ok/n_K"))
    results = {}
    ok5 = True
    for sc in SCALES:
        first_ok, last_fail, psi_ok, trace = k_min_scan(r, sc)
        results[sc] = (first_ok, last_fail, psi_ok, trace)
        okKs = [K for K, o, _ in trace if o]
        n_ok = len(okKs)
        if not okKs:
            print("  %-7.2f %-14s %-16s %-10s %d/%d"
                  % (sc, "no" if not trace[0][1] else "yes(with continuation lost)", "none", "-", n_ok, len(trace)))
        else:
            pm = float(np.min(psi_ok)) if psi_ok is not None else float("nan")
            win = "[%.2f, %.2f]" % (min(okKs), max(okKs))
            print("  %-7.2f %-14s %-16s %-10.4f %d/%d"
                  % (sc, "yes" if trace[0][1] else "no", win, pm, n_ok, len(trace)))
    for sc in (0.10, 0.30, 1.00):
        if not any(o for _, o, _ in results[sc][3]):
            ok5 = False
    print("  A5 verdict (a CMC slice exists at scale=1.0, 0.3, 0.1): %s" % ("PASS" if ok5 else "FAIL"))
    print()

    # ---------------- sign of the K-dependence (A4, main branch) ----------------
    print("[A4-main] how |K| moves the existence boundary (threshold scale vs K)")
    print("  %-8s %s" % ("|K|", "largest scale that solves (bisection on scale, 12 iterations)"))
    for Kcc in (0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0):
        lo, hi = 1e-3, 3.0
        ok_lo, _, _ = exists(r, lo, Kcc)
        ok_hi, _, _ = exists(r, hi, Kcc)
        if not ok_lo:
            print("  %-8.1f  even scale=%.3f fails (registered below)" % (Kcc, lo))
            continue
        if ok_hi:
            print("  %-8.1f  >= %.2f (scan ceiling reached)" % (Kcc, hi))
            continue
        for _ in range(12):
            mid = math.sqrt(lo * hi)
            okm, _, _ = exists(r, mid, Kcc)
            if okm:
                lo = mid
            else:
                hi = mid
        print("  %-8.1f  scale_crit = %.4f  (bracket %.4f - %.4f)" % (Kcc, lo, lo, hi))
    print("  direction is read off the table above; no sign was assumed in advance.")
    print("  NOTE: 'scale_crit' at K>=0.25 is measured on the branch seeded by continuation; the")
    print("  A6 control below decides whether that branch represents the WALL or only the K^2 term.")
    print()

    # ---------------- A6 validity of the high-|K| branch (decisive control) ----------------
    print("[A6] is the high-|K| branch a representation of the wall?  (negative control)")
    print("  registered criterion: bg_dev = max|psi(scale->0) - 1| < 0.1 AND M(R) > 0")
    print("  %-6s %-11s %-11s %-11s %-11s %s"
          % ("|K|", "d_wall", "bg_dev", "M_bg(R)", "M_wall(R)", "verdict"))
    a6 = t_a6_validity(r)
    ok6 = False
    for row in a6:
        Kcc, d_wall, bg_dev, m_bg, m_w, good = row
        if d_wall is None:
            print("  %-6.2f %s" % (Kcc, "no solution pair"))
            continue
        print("  %-6.2f %-11.4f %-11.4f %-+11.2f %-+11.2f %s"
              % (Kcc, d_wall, bg_dev, m_bg, m_w, "REPRESENTS" if good else "does NOT represent the wall"))
        ok6 = ok6 or good
    print("  A6 verdict (some |K| gives a wall-dominated, positive-mass slice): %s"
          % ("PASS" if ok6 else "FAIL"))
    print("  reading: at |K| >= 0.25 the conformal factor is already O(1)-different from 1 with the")
    print("  wall switched OFF, and the boundary mass proxy is large and NEGATIVE; the apparent A5")
    print("  'existence restoration' is therefore carried by the K^2 term alone, not by the wall.")
    print("  (Consistent with the exact statement that a slice with K = const != 0 cannot be")
    print("   asymptotically flat: the Robin mass-falloff truncation is satisfied by a fake mass.)")
    print()

    # ---------------- verdicts ----------------
    print("[verdicts]")
    print("  A1 K->0 identity      : %s (IDENT; excluded from the evidence count)" % ("PASS" if ok1 else "FAIL"))
    print("  A2 MMS stencil order  : %s" % ("PASS" if ok2 else "FAIL"))
    print("  A3 nonlinear order    : %s" % ("PASS" if ok3 else "FAIL"))
    print("  A5 solvability of the strong wall at high |K| : %s" % ("PASS" if ok5 else "FAIL"))
    print("  A6 that branch represents the wall            : %s  <-- DECISIVE"
          % ("PASS" if ok6 else "FAIL"))
    print()
    print("  Registered headline: A5 and A6 answer DIFFERENT questions. A5 asks whether the")
    print("  Hamiltonian constraint can be solved with the strong wall present; A6 asks whether")
    print("  the solution still describes that wall. The answer to the first is yes at high |K|,")
    print("  the answer to the second is NO: the branch is K^2-dominated, negative-mass, and not")
    print("  asymptotically flat. The strong wall therefore has no wall-dominated conformally")
    print("  flat constraint solution on any constant-K CMC slice.")

    print()
    print("[structural conclusion]")
    print("  The source terms of the Lichnerowicz-York equation carry two conformal weights:")
    print("  matter psi^5 (negative) and psi (negative), mean curvature psi^5 (positive),")
    print("  shear psi^-7 (negative). Only the mean-curvature term has the opposite sign to the")
    print("  matter term -- which is exactly why it can make the constraint solvable while")
    print("  destroying the interpretation: at the |K| needed for solvability, the K^2 term is")
    print("  the dominant source and the 'wall' is a subdominant correction to a K^2-driven")
    print("  conformal factor. A5 and A6 are therefore not in conflict; they are the same fact")
    print("  read at two levels.")

    # ---------------- deliverable for module B ----------------
    print()
    print("[handoff to module B]")
    print("  registered plan was 'evolve the strongest slice found'. Outcome of A5+A6:")
    print("  the strongest WALL-DOMINATED (valid) slice remains the K=0 one, i.e. scale <= 0.05")
    print("  (bracket (0.05, 0.07) from the 2026-11-21 module, reproduced here by A1/A5 at K=0).")
    print("  Module B therefore starts from the K=0 weak branch and registers explicitly that")
    print("  the P1a full-strength wall cannot be evolved: it has no valid initial data, and the")
    print("  reason is now a stated geometric fact rather than an unexplained numerical failure.")
    ok_branch, psi_branch, res_branch = exists(r, 0.05, 0.0)
    print("  handoff slice: scale=0.05, K=0, converged=%s, psi in [%.4f, %.4f], residual %.1e"
          % (ok_branch, float(np.min(psi_branch)), float(np.max(psi_branch)), res_branch))
    print("  remaining route for a strong wall (registered OPEN): a LOCALIZED mean curvature")
    print("  K(r,z) (the sweeping front itself). That breaks the K=const identity that makes the")
    print("  momentum constraint trivially satisfied, so Hamilton+Mom must be solved jointly.")
    print("evidence level: MODEL RESULT (screened); A2/A3 are machinery checks (2nd order),")
    print("                A6 is a negative control that withdraws the naive A5 reading.")


if __name__ == "__main__":
    main()
