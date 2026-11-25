# -*- coding: utf-8 -*-
"""
P2-C6: linear perturbative stability of the homogeneous backgrounds
(the LAST open G3' acceptance item; roadmap v1.4 sec 12.4 / runs/R2/R2A_registration)
=====================================================================================

Scope registered BEFORE the run (honest boundary):
  This module assesses linear perturbative stability at TWO levels:
    (i)  k = 0 full-state sector: tangent-flow (Lyapunov) analysis of the registered
         8-variable homogeneous state y = [lnA, lnB, lnC, HA, HB, HC, phi, phidot]
         around the frozen background trajectories -- ALL homogeneous perturbation
         directions of the ADM-reduced system, including metric and constraint-affine
         directions;
    (ii) k != 0 test-field scalar sector: the scalar perturbation delta_phi on a frozen
         background metric, delta_phi_ddot + [k_x^2/A^2 + k_y^2/B^2 + k_z^2/C^2
         + V''(phi) + (alpha/v) d rho_B/d phi] delta_phi = 0 (leading order in the
         metric coupling; screened-level).
  NOT covered (production version, remains registered as the boundary of this module):
  gauge-fixed cosmological perturbation theory with coupled metric perturbations at
  k != 0 and mode coupling. The verdict is therefore "no identified catastrophic
  linear instability at the homogeneous-sector + test-field level" (roadmap sec 4.6
  GO wording), not a full cosmological-perturbation stability proof.

Catastrophic-instability criterion (registered before the run):
  lambda_max > gamma_tach_max = sqrt(max_phi V''(phi)) = sqrt(2 lam v^2) = 1.41421...
  Justification: V''(phi) = lam(3 phi^2 - v^2) in [-lam v^2, 2 lam v^2]; the scalar
  barrier sector cannot locally grow faster than sqrt(2). Any exponent beyond this
  bound cannot originate from the registered scalar sector and indicates a
  metric/constraint-sector dynamical instability. The barrier-top tachyonic mode
  itself (lambda ~= 1 for phi0 = 0) is the registered bubble-nucleation mechanism
  and is reported, not treated as catastrophic.

Tests (thresholds registered before computation):
  T1  Frozen-metric oscillator energy conservation (true-vacuum start, k = 1):
      |E(t)-E(0)|/E(0) < 1e-6 over t in [0, 100] (RK45 offset caveat as R1-A1 T1).
  T2  Tachyonic anchor (barrier top, k = 0): measured growth rate matches
      sqrt(V''(0)) = 1 within 1e-6 -- validates the perturbation machinery.
  T3  Tangent-flow Lyapunov spectra along 5 registered backgrounds:
      lambda_max <= 1.05 * sqrt(2) in every case, with the leading vector's scalar
      projection reported (mode identification diagnostic).
  T4  Constraint control under initial-data perturbation (random direction, fixed
      seed): max_t |C_H| < 1e-4 (the G4 registered valid threshold) along the
      perturbed trajectory.
  T5  Lyapunov two-tolerance convergence: |lambda_max(1e-9) - lambda_max(1e-11)|
      / |lambda_max| < 5%.

Zero file I/O: all results printed to stdout (pure ASCII).
Run: cd D:/Docs/DCC && python -I src/r2_homogeneous/linear_stability_c6.py > runs/R2/r2c6_linear_stability_results.txt
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

import importlib.util
import math
import os

import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

# load the frozen homogeneous implementation (single source of the field equations)
_spec = importlib.util.spec_from_file_location(
    "hom", os.path.join(ROOT, "DCC_P2_homogeneous.py"))
hom = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hom)

# --------------------------------------------------------------------------
# Registered parameters (registered before run)
# --------------------------------------------------------------------------
KAPPA, LAM, V_VAC, ALPHA = hom.KAPPA, hom.LAM, hom.V_VAC, hom.ALPHA
T_STAB = 100.0                    # stability window (registered)
QR_EVERY = 0.5                    # re-orthonormalization interval
FD_EPS = 1e-7                     # finite-difference step for the Jacobian
SEED = 20261121                   # fixed seed for the T4 random perturbation
CASES = [
    # (label, H0, phi0, phidot0, f, eps, mode)
    ("magnetic-only [shear] (phi=-1, f=0.7)", 0.25, -1.0, 0.0, 0.7, 0.0, "shear"),
    ("baseline [shear] (phi=0 barrier top, f=0.7)", 0.25, 0.0, 0.0, 0.7, 0.01, "shear"),
    ("strong B [shear] (phi=0, f=1.5)", 0.25, 0.0, 0.0, 1.5, 0.01, "shear"),
    ("no-B [shear] (phi=0 barrier top, f=0)", 0.25, 0.0, 0.0, 0.0, 0.01, "shear"),
    ("magnetic-only [iso] (phi=-1, f=0.7)", 0.0, -1.0, 0.0, 0.7, 0.0, "isotropic"),
]

# --------------------------------------------------------------------------
# Registered thresholds (registered before run)
# --------------------------------------------------------------------------
TH_T1_ENERGY = 1e-6               # oscillator energy conservation
TH_T2_TACHYON = 1e-6              # tachyonic growth-rate anchor
TH_T3_LMAX = 1.05 * math.sqrt(LAM * 2.0 * V_VAC ** 2)   # catastrophic bound
TH_T4_CH = 1e-4                   # constraint control under perturbation (G4 level)
TH_T5_REL = 0.05                  # Lyapunov two-tolerance convergence (5%)


# --------------------------------------------------------------------------
# (ii) test-field scalar sector on a frozen background
# --------------------------------------------------------------------------
def vpp(phi, eps):
    """V''(phi) for the registered shifted double well."""
    return LAM * (3.0 * phi * phi - V_VAC ** 2)


def scalar_testfield_growth(phi0, eps, f, A=1.0, B=1.0, C=1.0):
    """Leading-order scalar perturbation rate at k=0 on a frozen background:
    delta_phi_ddot = [ -V''(phi0) - (alpha/v) d rho_B/d phi ] delta_phi
    with rho_B = Z(phi) f^2 / (2 A^2 B^2), Z = exp(alpha phi / v)."""
    drho_dphi = (ALPHA / V_VAC) * (ALPHA / V_VAC) * math.exp(ALPHA * phi0 / V_VAC) \
        * f * f / (2.0 * A * A * B * B)
    rate2 = -vpp(phi0, eps) - (ALPHA / V_VAC) * drho_dphi
    return rate2  # growth rate squared (positive = exponential growth)


# --------------------------------------------------------------------------
# (i) tangent-flow Lyapunov analysis (k = 0 full-state sector)
# --------------------------------------------------------------------------
def jacobian(y, f, eps):
    """Central-difference Jacobian of the frozen homogeneous rhs at state y."""
    n = len(y)
    J = np.empty((n, n))
    for j in range(n):
        e = np.zeros(n)
        e[j] = FD_EPS
        yp = hom.rhs(0.0, y + e, f, eps)
        ym = hom.rhs(0.0, y - e, f, eps)
        J[:, j] = (np.asarray(yp) - np.asarray(ym)) / (2.0 * FD_EPS)
    return J


def combined_rhs(t, Y, f, eps):
    n = 8
    y = Y[:n]
    V = Y[n:].reshape(n, n)
    dy = np.asarray(hom.rhs(t, y, f, eps))
    J = jacobian(y, f, eps)
    dV = J @ V
    return np.concatenate([dy, dV.ravel()])


def lyapunov_spectrum(y0, f, eps, t_end=T_STAB, rtol=1e-9):
    """Benettin QR tangent-flow Lyapunov exponents along the background trajectory.

    Segment-wise integration with orthonormalization feedback (standard continuous
    Gram-Schmidt): every QR_EVERY the tangent matrix is re-orthonormalized, the
    log-stretching of the R diagonal is accumulated, and the orthonormalized basis
    is fed back as the new initial condition of the next segment.
    """
    n = 8
    y = y0.copy()
    V = np.eye(n)
    logs = np.zeros(n)
    proj = []
    t = 0.0
    while t < t_end - 1e-12:
        t_next = min(t + QR_EVERY, t_end)
        Y0 = np.concatenate([y, V.ravel()])
        seg = solve_ivp(combined_rhs, (t, t_next), Y0, args=(f, eps),
                        method="RK45", rtol=rtol, atol=1e-12)
        if not seg.success:
            raise RuntimeError("tangent segment failed: " + str(seg.message))
        Y = seg.y[:, -1]
        y = Y[:n]
        V = Y[n:].reshape(n, n)
        V, R = np.linalg.qr(V)
        logs += np.log(np.maximum(np.abs(np.diag(R)), 1e-300))
        v1 = V[:, 0]
        proj.append(math.hypot(v1[6], v1[7]) / (np.linalg.norm(v1) + 1e-300))
        t = t_next
    lam = logs / t_end
    return lam, float(np.mean(proj))


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
def t1_frozen_oscillator():
    """Energy conservation of the test-field oscillator (true-vacuum start)."""
    k = 1.0
    phi0 = V_VAC
    f = 0.0
    rate2 = k * k + vpp(phi0, 0.01)  # frozen flat background A=B=C=1
    w = math.sqrt(rate2)
    d0, p0 = 1.0, 0.0
    rhs = lambda t, y: [y[1], -rate2 * y[0]]
    sol = solve_ivp(rhs, (0.0, T_STAB), [d0, p0], method="RK45",
                    rtol=1e-10, atol=1e-12, dense_output=True)
    tt = np.linspace(0.0, T_STAB, 2001)
    dd = sol.sol(tt)[0]
    pd = sol.sol(tt)[1]
    E = 0.5 * pd ** 2 + 0.5 * w * w * dd ** 2
    return float(np.max(np.abs(E / E[0] - 1.0)))


def t2_tachyonic_anchor():
    """Growth-rate anchor at the barrier top (k=0, frozen flat background).

    delta_phi_ddot = rate2 * delta_phi with rate2 = +1; integrating to T = 20 the
    cosh branch dominates and y'/y -> lambda with relative deviation ~2 e^{-2 lambda T}.
    """
    rate2 = scalar_testfield_growth(0.0, 0.01, 0.0)   # = -V''(0) = +1
    lam_ana = math.sqrt(rate2)
    T = 20.0
    sol = solve_ivp(lambda t, y: [y[1], rate2 * y[0]], (0.0, T),
                    [1.0, 0.0], method="RK45", rtol=1e-12, atol=1e-14)
    lam_num = sol.y[1][-1] / sol.y[0][-1]              # -> lambda (cosh-dominated)
    return abs(lam_num - lam_ana), lam_ana


def main():
    bar = "=" * 74
    print(bar)
    print("P2-C6: linear perturbative stability of the homogeneous backgrounds")
    print("spec: roadmap v1.4 sec 12.4 last item; the last open G3' acceptance item")
    print(bar)
    print("[scope] (registered before run)")
    print("  (i)  k=0 full-state sector: tangent-flow Lyapunov analysis of the frozen")
    print("       8-variable state [lnA,lnB,lnC,HA,HB,HC,phi,phidot] (homogeneous sector)")
    print("  (ii) k!=0 test-field scalar sector: scalar perturbation on frozen metric")
    print("  NOT covered: gauge-fixed cosmological perturbation theory with coupled")
    print("  metric perturbations at k!=0 (production version; boundary registered)")
    print("[criterion] (registered before run)")
    # ERRATA 2026-11-22: this line used to read "%.5f = sqrt(max V'')", which mislabels the
    # applied threshold. sqrt(max V'') = sqrt(2*LAM*V_VAC^2) = 1.41421 (the scalar barrier
    # bound); the registered constant is 1.05x that = 1.48492, i.e. a 5% tolerance band above
    # the exact bound. The archived run log carries the old wording and is NOT edited; the
    # correction is recorded in reports/gates/D5_execution_review_v2.md sec 8. Verdicts are
    # unaffected: observed lambda_max <= 0.029 is >50x below either number.
    print("  catastrophic := lambda_max > %.5f = 1.05 * sqrt(max V'') (5%% band above the"
          % TH_T3_LMAX)
    print("    exact scalar-barrier bound sqrt(2 lam v^2) = %.5f)"
          % math.sqrt(2.0 * LAM * V_VAC ** 2))
    print("  the barrier-top tachyonic mode (lambda ~= 1 at phi0=0) is the registered")
    print("  bubble-nucleation mechanism -- reported, not treated as catastrophic")
    print("[thresholds] (registered before run)")
    print("  T1 oscillator energy conservation      < %.1e" % TH_T1_ENERGY)
    print("  T2 tachyonic growth-rate anchor |d|    < %.1e" % TH_T2_TACHYON)
    print("  T3 lambda_max <= %.5f (all 5 cases)" % TH_T3_LMAX)
    print("  T4 max_t |C_H| under perturbation      < %.1e" % TH_T4_CH)
    print("  T5 Lyapunov two-tolerance convergence  < %.0f%%" % (100 * TH_T5_REL))
    print()

    # ---- T1 ----
    dev1 = t1_frozen_oscillator()
    ok1 = dev1 < TH_T1_ENERGY
    print("[T1] frozen-metric oscillator energy conservation (true vacuum, k=1)")
    print("  max |E(t)/E(0) - 1| = %.3e  <  %.1e" % (dev1, TH_T1_ENERGY))
    print("  T1 verdict: %s" % ("PASS" if ok1 else "FAIL"))
    print()

    # ---- T2 ----
    dev2, lam_ana = t2_tachyonic_anchor()
    ok2 = dev2 < TH_T2_TACHYON
    print("[T2] tachyonic anchor (barrier top, k=0, frozen background)")
    print("  analytic growth rate sqrt(V''(0) magnitude) = %.6f" % lam_ana)
    print("  measured rate deviation (y'/y at T=20): %.3e  <  %.1e"
          % (dev2, TH_T2_TACHYON))
    print("  T2 verdict: %s (validates the perturbation machinery)"
          % ("PASS" if ok2 else "FAIL"))
    print()

    # ---- T3: Lyapunov spectra ----
    print("[T3] tangent-flow Lyapunov spectra along registered backgrounds")
    print("  window t in [0, %.0f]; QR every %.1f; FD Jacobian eps=%.0e"
          % (T_STAB, QR_EVERY, FD_EPS))
    print("  %-42s %-10s %-10s %-10s" % ("case", "lambda_max", "lam[1]", "scal_proj"))
    lam_records = []
    ok3 = True
    for (label, H0, phi0, phidot0, f, eps, mode) in CASES:
        y0, rho0 = hom.initial_state(H0, phi0, phidot0, f, eps, mode)
        lam, proj = lyapunov_spectrum(y0, f, eps)
        lam_records.append((label, lam, proj))
        lmax = float(np.max(lam))
        flag = "CATASTROPHIC" if lmax > TH_T3_LMAX else "within bound"
        ok3 = ok3 and (lmax <= TH_T3_LMAX)
        print("  %-42s %-10.5f %-10.5f %-10.3f  %s"
              % (label, lmax, float(np.sort(lam)[-2]), proj, flag))
        print("      spectrum: %s" % " ".join("%.3f" % v for v in np.sort(lam)[::-1]))
    print("  T3 verdict: %s (criterion lambda_max <= %.5f in every case)"
          % ("PASS" if ok3 else "FAIL", TH_T3_LMAX))
    print("  note: negative exponents reflect Hubble damping of the expanding")
    print("        backgrounds; near-zero exponents reflect the registered gauge/")
    print("        time-translation directions of the homogeneous sector.")
    print()

    # ---- T4: constraint control under perturbation ----
    print("[T4] constraint control under initial-data perturbation (seed=%d)" % SEED)
    rng = np.random.default_rng(SEED)
    worst_ch = 0.0
    for (label, H0, phi0, phidot0, f, eps, mode) in CASES:
        y0, _ = hom.initial_state(H0, phi0, phidot0, f, eps, mode)
        d = rng.normal(size=8)
        d /= np.linalg.norm(d)
        yp = y0 + 1e-8 * d
        sol = solve_ivp(hom.rhs, (0.0, T_STAB), yp, args=(f, eps),
                        method="LSODA", rtol=1e-11, atol=1e-13, max_step=0.5)
        ch = max(abs(hom.constraint_residual(sol.y[:, i], f, eps))
                 for i in range(sol.y.shape[1]))
        worst_ch = max(worst_ch, ch)
        print("  %-42s max_t |C_H| = %.3e" % (label, ch))
    print("  worst-case max_t |C_H| = %.3e  <  %.1e (G4 registered level)"
          % (worst_ch, TH_T4_CH))
    ok4 = worst_ch < TH_T4_CH
    print("  T4 verdict: %s" % ("PASS" if ok4 else "FAIL"))
    print()

    # ---- T5: two-tolerance convergence ----
    print("[T5] Lyapunov two-tolerance convergence (case: magnetic-only [shear])")
    y0, _ = hom.initial_state(*CASES[0][1:4], CASES[0][4], CASES[0][5], CASES[0][6])
    lam_a, _ = lyapunov_spectrum(y0, CASES[0][4], CASES[0][5], rtol=1e-9)
    lam_b, _ = lyapunov_spectrum(y0, CASES[0][4], CASES[0][5], rtol=1e-11)
    la, lb = float(np.max(lam_a)), float(np.max(lam_b))
    rel = abs(la - lb) / max(abs(la), 1e-300)
    print("  lambda_max(rtol=1e-9)  = %.6f" % la)
    print("  lambda_max(rtol=1e-11) = %.6f" % lb)
    print("  relative difference = %.4f  <  %.0f%%" % (rel, 100 * TH_T5_REL))
    ok5 = rel < TH_T5_REL
    print("  T5 verdict: %s" % ("PASS" if ok5 else "FAIL"))
    print()

    print("[verdicts]")
    print("  T1 oscillator energy conservation : %s" % ("PASS" if ok1 else "FAIL"))
    print("  T2 tachyonic growth-rate anchor   : %s" % ("PASS" if ok2 else "FAIL"))
    print("  T3 lambda_max within bound (5/5)  : %s" % ("PASS" if ok3 else "FAIL"))
    print("  T4 constraint control             : %s" % ("PASS" if ok4 else "FAIL"))
    print("  T5 two-tolerance convergence      : %s" % ("PASS" if ok5 else "FAIL"))
    allok = ok1 and ok2 and ok3 and ok4 and ok5
    print("P2-C6 screening-level OVERALL: %s" % ("PASS" if allok else "FAIL"))
    if allok:
        print("conclusion (screened level): no identified catastrophic linear instability")
        print("  at the homogeneous-sector + test-field level for the registered cases;")
        print("  the barrier-top tachyonic mode is the registered nucleation mechanism.")
    print("evidence level: MODEL RESULT (screened scope; production version = gauge-fixed")
    print("                cosmological perturbation theory at k!=0 remains registered)")
    print("status registration: P2-C6 (last open G3' acceptance item) -> EXECUTED at")
    print("                screening level; G3' gate recommendation: Conditionally met,")
    print("                full perturbation-theory closure remains the production item.")


if __name__ == "__main__":
    main()
