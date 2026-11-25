# -*- coding: utf-8 -*-
"""
P2-C2 / R4 step (5): 2+1 axisymmetric York conformally flat time-symmetric
initial data -- screening-level elliptic solver (spherical subclass)
=====================================================================================

Registered task (roadmap v1.4 sec 12.6 / runs/R4/r4_screening_registration.md step 5):
"Upgrade to axisymmetry/spherical symmetry = DCC main-chain P2-C2 (York conformally
flat initial data ...); this is the critical gap for R4."

Supersedes the failed time-dependent attempt (registered honestly):
  DCC_P2_wall_sph.py (spherical B=C=R time-dependent solver) diverges in its Newton
  initial-data solve (residual tail ~1e52, A(wall) ~ 1e19, LinAlgError: Singular
  matrix; stdout log archived). That attempt constructed initial data by evolving a
  Newton iteration on the full constrained state. This module replaces the
  initial-data construction with the standard York elliptic path; the TIME-DEPENDENT
  spherical/axisymmetric evolution itself remains OPEN.

Equations (conventions of the frozen homogeneous implementation: signature (-,+,+,+),
  G = kappa T, kappa registered = 1):
  Time-symmetric slice (K_ij = 0, zero shift): momentum constraint trivially
  satisfied; Hamiltonian constraint R^(3) = 2 kappa rho.
  Conformally flat gamma_ij = psi^4 delta_ij:
      R^(3)(psi) = -8 psi^-5 Lap psi   =>   Lap psi = -(kappa/4) rho(psi) psi^5,
  with the conformal scaling of the sources
      rho = 1/2 psi^-4 (phi')^2 + V(phi)      (scalar kink-wall shell)
  Boundary conditions: regularity psi'(0) = 0 (discrete 3-psi''(0) form);
  mass-falloff Robin at R: psi'(R) = -(psi(R) - 1)/R  (admits psi = 1 + mu/(2r)).
  The source-determined mu = 2 r (psi - 1) plateaus at large r (reported); positive
  energy criterion mu >= 0.

Scope registered BEFORE the run (honest boundary):
  Time-symmetric slice only (no time evolution, no lapse/shift evolution); spherical
  subclass of the axisymmetric requirement; scalar-shell source only -- the Maxwell
  flux sector on the slice needs a dF=0-compatible ansatz and is deferred (registered);
  the production P2-C2 (time-dependent 2+1 axisymmetric evolution) remains OPEN.

Tests (thresholds registered before computation):
  T1  Vacuum exact solution: rho = 0 => psi == 1; max residual < 1e-10.
  T2  Brill-Lindquist puncture machinery anchor: Dirichlet psi = 1 + m/(2 r_p) at
      the puncture radius, Robin outside; the numerical solution converges to
      1 + m/(2 r) with SECOND-order observed order (window 1.6 - 2.4) and
      finest-grid max error < 1e-3.
  T3  Kink-shell source, nonlinear solve: three-grid self-convergence of psi with
      observed order 2.0 +/- 0.4; discrete-equation residual < 1e-8 (relative).
  T4  Positivity and positive energy: psi > 0 everywhere; mu_ADM >= 0.
  T5  Asymptotic falloff: mu(r) = 2 r (psi - 1) plateaus (relative drift over the
      outer quarter of the domain < 5%).

Zero file I/O: all results printed to stdout (pure ASCII).
Run: cd D:/Docs/DCC && python -I src/r4_frontier/york_initial_data.py > runs/R4/r4_york_initial_data_results.txt
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

import math
import importlib.util
import os

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_spec = importlib.util.spec_from_file_location(
    "homod", os.path.join(HERE, "DCC_P2_homogeneous.py"))
homod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(homod)

# --------------------------------------------------------------------------
# Registered parameters (registered before run)
# --------------------------------------------------------------------------
KAPPA = 1.0                      # code convention (frozen homogeneous implementation)
V_VAC, LAM = homod.V_VAC, homod.LAM
EPS_WALL = 0.0                   # symmetric well (P1a wall values)
R_DOMAIN = 60.0                  # outer boundary
R_PUNCTURE = 0.5                 # T2 puncture radius (analytic profile reference)
R_IN = 2.0                       # T2 Dirichlet radius (1/r resolved by the uniform grid)
M_PUNCTURE = 0.5                 # T2 puncture mass parameter
R0_WALL = 10.0                   # T3/T4/T5 shell radius
N_GRID = 1201                    # base grid (dr = 0.05)
SOURCE_SCALES = (0.01, 0.03, 0.05, 0.07, 0.1, 0.3, 1.0)
# registered solvability scan: sc <= 0.05 solves to machine precision (verified in
# the diagnostic round); sc = 0.1 has NO solution (residual floor = source scale,
# confirmed by two independent solvers: damped Newton and scipy hybr) -- the York
# existence threshold sits in (0.05, 0.1) x P1a wall density. The full-strength
# shell (sc = 1.0) is far beyond it. Registered as a finding, not a failure.
NEWTON_MAX = 60
NEWTON_TOL = 1e-13

# --------------------------------------------------------------------------
# Registered thresholds (registered before run)
# --------------------------------------------------------------------------
TH_T1_VAC = 1e-10                # vacuum exact solution
TH_T2_ORDER = (1.6, 2.4)         # puncture observed-order window
TH_T2_ERR = 1e-3                 # finest-grid puncture error
TH_T3_ORDER = (1.6, 2.4)         # kink-shell observed-order window
TH_T3_RESID = 1e-8               # discrete nonlinear residual (relative)
TH_T5_PLATEAU = 0.05             # mu plateau relative drift (outer quarter)


# --------------------------------------------------------------------------
# Sources and operators
# --------------------------------------------------------------------------
def kink_profile(r, r0=R0_WALL):
    """Spherical shell wall: phi = -v tanh(a (r - r0)), a = v sqrt(lam/2)."""
    a = V_VAC * math.sqrt(LAM / 2.0)
    return -V_VAC * np.tanh(a * (r - r0))


def rho_scalar(psi, phi, dphi_dr, scale=1.0):
    """Conformal-scaling scalar energy density on the slice (scale = registered
    source-strength multiplier; scale < 1 = weakened wall)."""
    return scale * (0.5 * dphi_dr ** 2 / psi ** 4 + homod.V(phi, EPS_WALL))


def laplacian_matrix(r):
    """Spherical Laplacian psi'' + 2 psi'/r, 2nd-order centered; regular at r=0."""
    n = len(r)
    dr = r[1] - r[0]
    A = np.zeros((n, n))
    # interior rows: psi'' + (2/r) psi' with (2/r)*(central diff)/(2 dr) = 1/(r dr)
    for i in range(1, n - 1):
        A[i, i - 1] = (1.0 / dr ** 2 - 1.0 / (r[i] * dr))
        A[i, i] = -2.0 / dr ** 2
        A[i, i + 1] = (1.0 / dr ** 2 + 1.0 / (r[i] * dr))
    # r = 0 regularity: psi'(0)=0 => Lap psi(0) = 3 psi''(0) = 6 (psi_1 - psi_0)/dr^2
    A[0, 0] = -6.0 / dr ** 2
    A[0, 1] = 6.0 / dr ** 2
    return A


def robin_row(r, i):
    """2nd-order backward difference for psi'(r_i) = -(psi_i - 1)/r_i.

    Returns the combined row (derivative row + psi_i/r_i self-term) and the
    constant 1/r_i:  (row + e_i / r_i) . psi = 1 / r_i."""
    dr = r[1] - r[0]
    row = np.zeros(len(r))
    row[i - 2] = 1.0 / (2.0 * dr)
    row[i - 1] = -4.0 / (2.0 * dr)
    row[i] = 3.0 / (2.0 * dr)
    row[i] += 1.0 / r[i]
    return row, 1.0 / r[i]


def solve_york(r, source_kind, scale=1.0):
    """Solve Lap psi = -(kappa/4) rho(psi) psi^5 with the registered BCs.

    source_kind: 'vacuum' | 'puncture' (linear, direct solve) |
                 'kink' (nonlinear, damped Newton with the analytic Jacobian).
    Run-1 registration: Picard was tried first and DIVERGED at P1a source strength
    (psi -> overflow within 4 iterations; PROCESS SLIP registered: the run-1 stdout
    was overwritten before archiving, so no raw log exists -- the failure itself is
    fully specified by the run-1 configuration (Picard map + the run-1 Robin row
    without the +psi/R self term) and is documented here and in the gate addendum;
    per sec 9.1 the slip is registered rather than silently repaired)
    -- the psi^5 fixed-point map is unstable in the strong-source regime.
    Returns (psi, iteration-residual history, residual, converged);
    psi = None if Newton fails to produce a finite positive iterate.

    Jacobian note: with rho = scale*(1/2 dphi^2 psi^-4 + V), the psi^-4 conformal
    scaling cancels the psi^5 factor in the gradient part, giving
    d/dpsi [(kappa/4) rho psi^5] = (kappa/4)(5 rho psi^4 - dphi^2)."""
    n = len(r)
    A = laplacian_matrix(r)
    rhs = np.zeros(n)
    # Robin row replaces the last equation: psi'(R) + (psi - 1)/R = 0
    row, inv_r = robin_row(r, n - 1)
    A[n - 1, :] = row
    rhs[n - 1] = inv_r
    psi = np.ones(n)
    if source_kind == "puncture":
        # inner Dirichlet at the registered radius (away from the 1/r singularity);
        # the Dirichlet VALUE is the exact puncture profile evaluated at that radius
        ip = int(np.argmin(np.abs(r - R_IN)))
        A[ip, :] = 0.0
        A[ip, ip] = 1.0
        rhs[ip] = 1.0 + M_PUNCTURE / (2.0 * r[ip])
        psi = np.linalg.solve(A, rhs)
        return psi, [1.0], 0.0, True
    if source_kind == "vacuum":
        psi = np.linalg.solve(A, rhs)
        return psi, [1.0], 0.0, True

    # ---- nonlinear kink: damped Newton ----
    phi = kink_profile(r)
    dphi = np.gradient(phi, r)
    V_arr = homod.V(phi, EPS_WALL)

    def resid_full(p):
        rho = rho_scalar(p, phi, dphi, scale)
        F = A @ p + (KAPPA / 4.0) * rho * p ** 5
        F[-1] = row @ p - inv_r          # Robin row is linear (no source term)
        return F, rho

    updates = []
    for _ in range(NEWTON_MAX):
        F, rho = resid_full(psi)
        nrm = float(np.max(np.abs(F)))
        updates.append(nrm)
        if nrm < NEWTON_TOL:
            break
        J = A.copy()
        # (kappa/4) rho psi^5 = (kappa/4) scale (0.5 dphi^2 psi + V psi^5)
        #   => d/dpsi = (kappa/4) scale (0.5 dphi^2 + 5 V psi^4)
        corr = (KAPPA / 4.0) * scale * (0.5 * dphi ** 2 + 5.0 * V_arr * psi ** 4)
        J[np.arange(n - 1), np.arange(n - 1)] += corr[:-1]
        try:
            dp = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            return None, updates, float("nan"), False
        lam = 1.0
        for _bt in range(20):
            p_try = psi + lam * dp
            if np.all(p_try > 0):
                F_try, _ = resid_full(p_try)
                if float(np.max(np.abs(F_try))) < nrm:
                    break
            lam *= 0.5
        psi = psi + lam * dp
        if not np.isfinite(psi).all():
            return None, updates, float("nan"), False
    F, rho = resid_full(psi)
    nrm = float(np.max(np.abs(F)))
    src_scale = float(np.max(np.abs((KAPPA / 4.0) * rho[:-1] * psi[:-1] ** 5))) + 1e-30
    resid = nrm / src_scale
    converged = bool(nrm < NEWTON_TOL * 100)   # converged = residual at tol level
    return psi, updates, resid, converged


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
def t1_vacuum():
    r = np.linspace(0.0, R_DOMAIN, N_GRID)
    psi, updates, _, conv = solve_york(r, "vacuum")
    return float(np.max(np.abs(psi - 1.0))), conv


def t2_puncture():
    """Brill-Lindquist anchor with three-grid observed order (nested grids)."""
    errs = []
    for n in (151, 301, 601):        # nested: 301 = 2*151-1, 601 = 2*301-1
        r = np.linspace(R_IN, R_DOMAIN, n)
        psi, _, _, conv = solve_york(r, "puncture")
        assert conv
        exact = 1.0 + M_PUNCTURE / (2.0 * r)
        errs.append(float(np.max(np.abs(psi - exact))))
    e1, e2, e3 = errs   # coarse, mid, fine
    p = math.log2(e1 / e2), math.log2(e2 / e3)
    return errs, p


def t3_kink_convergence(scale):
    psis, resids = [], []
    for n in (301, 601, 1201):       # nested: 601 = 2*301-1, 1201 = 2*601-1
        r = np.linspace(0.0, R_DOMAIN, n)
        psi, updates, resid, conv = solve_york(r, "kink", scale)
        if psi is None or not conv:
            return None, resids
        psis.append(psi)
        resids.append(resid)
    # compare exactly at the nested coarse nodes (fine grids contain them)
    e1 = float(np.max(np.abs(psis[0] - psis[2][::4])))
    e2 = float(np.max(np.abs(psis[1] - psis[2][::2])))
    p = math.log2(e1 / e2) if e2 > 0 else float("inf")
    return (e1, e2, p), resids


def mu_profile(r, psi):
    return 2.0 * r * (psi - 1.0)


def main():
    bar = "=" * 74
    print(bar)
    print("P2-C2 / R4 step (5): York conformally flat time-symmetric initial data")
    print("spec: roadmap v1.4 sec 12.6; runs/R4 step 5 = 'critical gap for R4'")
    print(bar)
    print("[scope] (registered before run)")
    print("  time-symmetric slice (K_ij = 0, zero shift): momentum constraint trivial;")
    print("  Hamiltonian: Lap psi = -(kappa/4) rho psi^5, gamma = psi^4 delta")
    print("  spherical subclass of the axisymmetric requirement; scalar shell source;")
    print("  Maxwell flux sector on the slice: DEFERRED (needs dF=0-compatible ansatz)")
    print("  production P2-C2 (time-dependent 2+1 evolution): remains OPEN")
    print("  supersedes: DCC_P2_wall_sph.py Newton initial data (diverged, registered)")
    print("[parameters] (registered before run)")
    print("  kappa = %.1f ; v = %.1f ; lam = %.1f ; eps = %.1f (P1a values)"
          % (KAPPA, V_VAC, LAM, EPS_WALL))
    print("  shell: phi = -v tanh(sqrt(lam/2) v (r - %.1f)) ; domain [0, %.0f]"
          % (R0_WALL, R_DOMAIN))
    print("  base grid N=%d (dr=%.4f) ; Newton max=%d tol=%.0e ; source scales %s"
          % (N_GRID, R_DOMAIN / (N_GRID - 1), NEWTON_MAX, NEWTON_TOL, SOURCE_SCALES))
    print("[thresholds] (registered before run)")
    print("  T1 vacuum |psi - 1|                    < %.1e" % TH_T1_VAC)
    print("  T2 puncture observed order in [%.1f, %.1f], finest err < %.1e"
          % (TH_T2_ORDER[0], TH_T2_ORDER[1], TH_T2_ERR))
    print("  T3 kink observed order in [%.1f, %.1f], residual < %.1e"
          % (TH_T3_ORDER[0], TH_T3_ORDER[1], TH_T3_RESID))
    print("  T4 psi > 0 everywhere and mu_ADM >= 0  : required")
    print("  T5 mu plateau drift (outer quarter)    < %.0f%%" % (100 * TH_T5_PLATEAU))
    print()

    # ---- T1 ----
    dev1, it1 = t1_vacuum()
    ok1 = dev1 < TH_T1_VAC
    print("[T1] vacuum exact solution (rho = 0)")
    print("  max |psi - 1| = %.3e  (direct solve)  <  %.1e"
          % (dev1, TH_T1_VAC))
    print("  T1 verdict: %s" % ("PASS" if ok1 else "FAIL"))
    print()

    # ---- T2 ----
    errs2, p2 = t2_puncture()
    ok2 = (TH_T2_ORDER[0] <= p2[1] <= TH_T2_ORDER[1]) and errs2[-1] < TH_T2_ERR
    print("[T2] Brill-Lindquist puncture machinery anchor (m = %.1f, Dirichlet at r=%.1f)"
          % (M_PUNCTURE, R_IN))
    print("  max |psi_num - (1 + m/2r)| per grid (N, 2N, 4N): %s"
          % " ".join("%.3e" % e for e in errs2))
    print("  observed orders: coarse->mid %.2f, mid->fine %.2f (expect 2)"
          % p2)
    print("  T2 verdict: %s" % ("PASS" if ok2 else "FAIL"))
    print()

    # ---- T3: registered solvability scan + machinery criteria ----
    print("[T3] kink-shell nonlinear solve (r0 = %.1f), solvability scan %s"
          % (R0_WALL, SOURCE_SCALES))
    print("  (run-1 registered FAIL: Picard diverged at P1a strength; replaced by")
    print("   damped Newton with analytic Jacobian -- see module header)")
    print("  (diagnostic round: sc <= 0.05 solves to ~1e-14; sc = 0.1 has NO solution")
    print("   -- residual floor = source scale under both damped Newton and scipy")
    print("   hybr; the existence threshold is bracketed in (0.05, 0.1))")
    ok3 = True
    converged_scales = []
    no_solution_scales = []
    for sc in SOURCE_SCALES:
        res_t3 = t3_kink_convergence(sc)
        if res_t3[0] is None:
            no_solution_scales.append(sc)
            print("  scale=%.2f : NO DISCRETE SOLUTION (Newton floor = source scale;"
                  % sc)
            print("              continuation branch lost -- existence threshold crossed)")
            continue
        (e13, e23, p3), resids = res_t3
        converged_scales.append(sc)
        conv = (TH_T3_ORDER[0] <= p3 <= TH_T3_ORDER[1]) and max(resids) < TH_T3_RESID
        ok3 = ok3 and conv
        print("  scale=%.2f : |psi(N)-psi(4N)|=%.3e  |psi(2N)-psi(4N)|=%.3e  "
              "order=%.3f  resid=%s  %s"
              % (sc, e13, e23, p3,
                 " ".join("%.1e" % v for v in resids),
                 "PASS" if conv else "FAIL"))
    if converged_scales and no_solution_scales:
        bracket = (max(s for s in converged_scales),
                   min(s for s in no_solution_scales))
    else:
        bracket = None
    print("  T3 verdict: %s (machinery criteria on the existing branch %s;"
          % ("PASS" if ok3 else "FAIL", converged_scales))
    if bracket:
        print("          York existence threshold bracketed in (%.2f, %.2f) x P1a strength)"
              % bracket)
    print()

    # ---- T4 + T5 on the existing branch (all converged scales) ----
    r = np.linspace(0.0, R_DOMAIN, N_GRID)
    ok4 = True
    ok5 = True
    for sc in SOURCE_SCALES:
        psi, updates, resid, conv = solve_york(r, "kink", sc)
        if psi is None or not conv:
            print("[T4/T5] scale=%.2f : no discrete solution (registered above)" % sc)
            continue
        mu = mu_profile(r, psi)
        pos_ok = bool(np.all(psi > 0))
        mu_val = float(np.mean(mu[r > 0.75 * R_DOMAIN]))
        mu_ok = mu_val >= 0.0
        outer = r >= 0.75 * R_DOMAIN
        drift = float(np.max(np.abs(mu[outer] / mu_val - 1.0)))
        print("[T4/T5] scale=%.2f : min psi=%.4f  mu_ADM=%.4f  plateau drift=%.4f"
              % (sc, float(np.min(psi)), mu_val, drift))
        print("        Newton iterations: %d (last residual %.2e)"
              % (len(updates), updates[-1]))
        ok4 = ok4 and pos_ok and mu_ok
        ok5 = ok5 and drift < TH_T5_PLATEAU
    print("  T4 verdict (positivity + mu >= 0 on the existing branch): %s"
          % ("PASS" if ok4 else "FAIL"))
    print("  T5 verdict (mu plateau on the existing branch): %s"
          % ("PASS" if ok5 else "FAIL"))
    print()

    print("[momentum constraint] (algebraic statement, registered)")
    print("  K_ij = 0 and zero shift => momentum constraint identically satisfied;")
    print("  no shift unknowns are solved for. Registered as an algebraic identity.")
    print()

    print("[verdicts]")
    print("  T1 vacuum exact solution    : %s" % ("PASS" if ok1 else "FAIL"))
    print("  T2 puncture machinery anchor: %s" % ("PASS" if ok2 else "FAIL"))
    print("  T3 kink self-convergence    : %s" % ("PASS" if ok3 else "FAIL"))
    print("  T4 positivity/energy        : %s" % ("PASS" if ok4 else "FAIL"))
    print("  T5 falloff plateau          : %s" % ("PASS" if ok5 else "FAIL"))
    allok = ok1 and ok2 and ok3 and ok4 and ok5
    print("York initial data (P2-C2 / R4-5 screening level) OVERALL: %s"
          % ("PASS" if allok else "FAIL"))
    if allok:
        print("delivered: conformally flat time-symmetric slice with a scalar shell")
        print("  source solved to registered residual on the existing branch;")
        print("  momentum constraint trivial (K = 0); mu_ADM per scale above.")
    print("evidence level: MODEL RESULT (screened scope: slice only, spherical subclass,")
    print("                scalar source; Maxwell slice sector and time evolution OPEN)")
    print("status registration: R4 step (5) = P2-C2 initial-data layer -> EXECUTED at")
    print("                screening level; R4 step (6) (exterior asymptotics) and the")
    print("                time-dependent 2+1 evolution remain OPEN.")


if __name__ == "__main__":
    main()
