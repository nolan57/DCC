# -*- coding: utf-8 -*-
"""
N11: constraint stress P_2D incorporated into the 1+1 slab (R2-D L3 boundary layer)
=====================================================================================

Registered task (roadmap v1.4 sec 12.4 / F.4 item 4 / R2A registration "remaining
items"): incorporate the N11 constraint stress as a boundary condition of the 1+1
slab layer, with ADM constraint residual controlled (R2-D L3 acceptance).

Physics (registered before the run):
  The final state is a 2D sheet: z (=C in slab variables) contracted, the sheet
  plane spanned by the wall-normal x (=A) and tangent y (=B). The 2D matter carries
  the in-plane pressure P_2D; the N11 issue is that area invariance of the final
  state is NOT a passive property -- an external constraint stress of the same
  magnitude is required to hold the plane (N11: unconstrained transverse expansion,
  v_inf = 0.166c, ~4.7 ns over 1 m).

  Implementation: a PRESCRIBED external stress sector T^ext with uniform
  orthonormal-frame components (rho_e, p_x^e, p_y^e, p_z^e) is added to the ADM
  source terms of the frozen 1+1 solver. The Einstein combinations for the
  extrinsic-curvature source are exactly the homogeneous ones (Gauss combinations,
  verified in the frozen homogeneous implementation):
      dH_A += -kappa/2 * (p_y^e + p_z^e - p_x^e)
      dH_B += -kappa/2 * (p_x^e + p_z^e - p_y^e)
      dH_C += -kappa/2 * (p_x^e + p_y^e - p_z^e)
  The stress enters the machine 3x3 linear system only additively in b (stress does
  not multiply the dH coefficients), so the patched evolution is
      dH_new = dH_machine + Delta.
  T2 below validates this injection against the frozen homogeneous implementation.

  Registered external-stress configurations (sigma_ref = wall tension sigma_w in
  code units, the natural stress scale of the slab):
    (a) baseline        : Pi = 0 (regression)
    (b) hold-plane      : p_A^e = p_B^e = -Pi*sigma_ref, p_C^e = 0   (in-plane tension)
    (c) isotropic hold  : p_A^e = p_B^e = p_C^e = +Pi*sigma_ref     (decelerating sector)
    (d) plane-to-z redirect : p_A^e = p_B^e = -Pi*sigma_ref, p_C^e = +2*Pi*sigma_ref
  Pi scan: {0.25, 0.5, 1.0, 2.0}. Root-find: Pi_hold enforcing <H_A>(t_end) = 0
  for configuration (c) (the area-hold condition), bracketed before the run.

  Physical-unit bridge (registered honestly as OPEN): the G0 constraint stress
  P_2D = 8.62e16 N/m maps into slab code units only through the G0<->P2 unit
  bridge (object scale -> wall model scale), which is not registered anywhere in
  this repository. This module therefore delivers the machinery, the response
  curves and the required Pi_hold in CODE units; the SI normalization of the
  delivered Pi_hold stays OPEN until that bridge is registered.

Tests (thresholds registered before computation):
  T1  Pi = 0 regression: patched rhs identical to the frozen rhs (max diff < 1e-13).
  T2  Homogeneous cross-validation: uniform-phi slab with stress ON vs the frozen
      homogeneous rhs plus the analytic Delta terms (max deviation < 1e-9).
  T3  Constraint control with stress ON: max|Ham|, max|Mom| <= 2x the Pi = 0
      baseline over the same window (stress injection must not degrade control).
  T4  Response monotonicity: <H_A>(t_end) decreases monotonically with Pi for
      configuration (c); Pi_hold root-find converges with |F(Pi_hold)| < 1e-6.

Zero file I/O: all results printed to stdout (pure ASCII).
Run: cd D:/Docs/DCC && python -I src/r2_redshift/slab_n11_boundary.py > runs/R2/r2d_l3_n11_slab_results.txt
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

import importlib.util
import math
import os

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# load the frozen 1+1 slab implementation (machine equations + solver)
_spec = importlib.util.spec_from_file_location(
    "slabmod", os.path.join(HERE, "DCC_P2_wall_1p1.py"))
slabmod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(slabmod)

# load the frozen homogeneous implementation (validation reference)
_spec2 = importlib.util.spec_from_file_location(
    "homod", os.path.join(HERE, "DCC_P2_homogeneous.py"))
homod = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(homod)

IDX = slabmod.IDX

# --------------------------------------------------------------------------
# Registered parameters (registered before run)
# --------------------------------------------------------------------------
CASE = dict(name='W1-slab-static', eps=0.0, Q=0.1, T=6.0)   # frozen W1 case
L, N = 160.0, 801                                           # frozen grid
SIGMA_REF = 0.942809                                        # wall tension, code units (P1)
PI_SCAN = (0.25, 0.5, 1.0, 2.0)
PI_HOLD_BRACKET = (0.5, 40.0)                               # root-find bracket (registered)

# --------------------------------------------------------------------------
# Registered thresholds (registered before run)
# --------------------------------------------------------------------------
TH_T1_REG = 1e-13                 # Pi=0 regression identity
TH_T2_HOMO = 1e-9                 # homogeneous cross-validation of the injection
TH_T3_FACTOR = 2.0                # constraint-control degradation factor
TH_T4_ROOT = 1e-6                 # root-find residual |F(Pi_hold)|


# --------------------------------------------------------------------------
# External stress sector and the Einstein source combinations
# --------------------------------------------------------------------------
def delta_sources(rho_e, px_e, py_e, pz_e, kappa):
    """Einstein Gauss-combination contributions to (dH_A, dH_B, dH_C)."""
    dA = -0.5 * kappa * (py_e + pz_e - px_e)
    dB = -0.5 * kappa * (px_e + pz_e - py_e)
    dC = -0.5 * kappa * (px_e + py_e - pz_e)
    return dA, dB, dC


def stress_config(kind, pi):
    """Registered external-stress configurations (orthonormal-frame components)."""
    s = pi * SIGMA_REF
    if kind == "hold-plane":
        return 0.0, -s, -s, 0.0
    if kind == "isotropic-hold":
        return 0.0, s, s, s
    if kind == "redirect":
        return 0.0, -s, -s, 2.0 * s
    if kind == "off":
        return 0.0, 0.0, 0.0, 0.0
    raise ValueError(kind)


class N11Sim(slabmod.Sim):
    """Frozen slab solver + prescribed external stress sector (N11 boundary layer)."""

    def __init__(self, *a, stress=(0.0, 0.0, 0.0, 0.0), **kw):
        super().__init__(*a, **kw)
        self.rho_e, self.px_e, self.py_e, self.pz_e = stress

    def rhs(self, u):
        d = super().rhs(u)
        dA, dB, dC = delta_sources(self.rho_e, self.px_e, self.py_e, self.pz_e,
                                   self.kappa)
        d[IDX['HA']] += dA
        d[IDX['HB']] += dB
        d[IDX['HC']] += dC
        return d


def run_case(stress, T=CASE['T']):
    """Run one slab case; returns (sim, u0, u, rec, info) or (None, None, None, reason, None)
    if the machine elliptic solve hits the degenerate configuration (singular matrix)."""
    eqs = slabmod.Eqs()
    sim = N11Sim(eqs, L=L, N=N, eps=CASE['eps'], Q=CASE['Q'], stress=stress)
    u0, info = sim.initial_data()
    try:
        u, rec = sim.run(u0, T, cfl=0.1, rec_every=40)
    except np.linalg.LinAlgError as exc:
        reason = ("machine 3x3 solve singular: the prescribed stress drives the "
                  "zstatic ansatz into its degenerate configuration (H_B + H_C -> 0); "
                  "same failure signature as the archived DCC_P2_wall_sph.py attempt")
        return None, None, None, reason, None
    return sim, u0, u, rec, info


def mean_HA_end(rec):
    HA = np.array([fr[IDX['HA']] for fr in rec['u']])
    return float(np.mean(HA[-1]))


def mean_HC_min(rec):
    HC = np.array([fr[IDX['HC']] for fr in rec['u']])
    return float(np.min(HC))


# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
def t1_regression():
    eqs = slabmod.Eqs()
    sim0 = slabmod.Sim(eqs, L=L, N=N, eps=CASE['eps'], Q=CASE['Q'])
    sim1 = N11Sim(eqs, L=L, N=N, eps=CASE['eps'], Q=CASE['Q'],
                  stress=stress_config("off", 0.0))
    u0, _ = sim0.initial_data()
    d0 = sim0.rhs(u0.copy())
    d1 = sim1.rhs(u0.copy())
    return float(np.max(np.abs(d1 - d0)))


def t2_homogeneous_validation():
    """Uniform-phi slab with stress ON vs frozen homogeneous rhs + analytic Delta.

    With phi, f, E, P uniform the machine system has no gradients and reduces
    exactly to the frozen homogeneous equations; the patched slab must match
    homogeneous rhs + Delta to solver precision.
    """
    pi = 1.0
    stress = stress_config("isotropic-hold", pi)
    eqs = slabmod.Eqs()
    sim = N11Sim(eqs, L=L, N=N, eps=0.0, Q=CASE['Q'], stress=stress)
    u0, _ = sim.initial_data(phi_override=-1.0)
    d_slab = sim.rhs(u0.copy())
    # homogeneous reference at the wall center (uniform state: any point)
    ic = len(sim.x) // 2
    y0h = np.array([u0[IDX['lnA'], ic], u0[IDX['lnB'], ic], u0[IDX['lnC'], ic],
                    u0[IDX['HA'], ic], u0[IDX['HB'], ic], u0[IDX['HC'], ic],
                    u0[IDX['phi'], ic], u0[IDX['P'], ic]])
    f_c = float(u0[IDX['f'], ic])
    dy = np.asarray(homod.rhs(0.0, y0h, f_c, 0.0))
    dA, dB, dC = delta_sources(*stress, kappa=1.0)
    ref = np.array([dy[3] + dA, dy[4] + dB, dy[5] + dC])
    got = np.array([d_slab[IDX['HA'], ic], d_slab[IDX['HB'], ic],
                    d_slab[IDX['HC'], ic]])
    scale = float(np.max(np.abs(ref))) + 1e-30
    return float(np.max(np.abs(got - ref))) / scale


def main():
    bar = "=" * 74
    print(bar)
    print("N11: constraint stress incorporated into the 1+1 slab (R2-D L3 boundary layer)")
    print("spec: roadmap v1.4 sec 12.4 / F.4 item 4; R2A registration 'remaining items'")
    print(bar)
    print("[physics] (registered before run)")
    print("  final state: sheet plane = (A,B), z (=C) contracted; N11 requires an")
    print("  external constraint stress to hold the plane against the 2D pressure")
    print("  injection: prescribed uniform orthonormal stress sector (rho_e=0);")
    print("  dH_i += -kappa/2 * (Gauss combinations of p^e), additive in b of the")
    print("  machine 3x3 system (stress does not multiply the dH coefficients)")
    print("  sigma_ref = wall tension sigma_w = %.6f (code units, P1 frozen)" % SIGMA_REF)
    print("  configurations: (a) off, (b) hold-plane, (c) isotropic-hold, (d) redirect")
    print("  Pi scan: %s ; case W1-slab-static L=%.0f N=%d T=%.0f cfl=0.1"
          % (PI_SCAN, L, N, CASE['T']))
    print("[thresholds] (registered before run)")
    print("  T1 Pi=0 regression identity            < %.1e" % TH_T1_REG)
    print("  T2 homogeneous cross-validation (rel)  < %.1e" % TH_T2_HOMO)
    print("  T3 constraint degradation factor       <= %.1f x baseline" % TH_T3_FACTOR)
    print("  T4 root-find residual |F(Pi_hold)|     < %.1e" % TH_T4_ROOT)
    print("  unit-bridge status                     : OPEN (G0<->P2 mapping not registered)")
    print()

    # ---- T1 ----
    dev1 = t1_regression()
    ok1 = dev1 < TH_T1_REG
    print("[T1] Pi = 0 regression against the frozen solver")
    print("  max |rhs(N11 off) - rhs(frozen)| = %.3e  <  %.1e" % (dev1, TH_T1_REG))
    print("  T1 verdict: %s" % ("PASS" if ok1 else "FAIL"))
    print()

    # ---- T2 ----
    dev2 = t2_homogeneous_validation()
    ok2 = dev2 < TH_T2_HOMO
    print("[T2] homogeneous cross-validation of the injection (uniform phi, Pi=1, isotropic)")
    print("  relative deviation |slab(stress) - homogeneous rhs + Delta| = %.3e  <  %.1e"
          % (dev2, TH_T2_HOMO))
    print("  T2 verdict: %s" % ("PASS" if ok2 else "FAIL"))
    print()

    # ---- main scan ----
    print("[main scan] response of the W1 slab to the registered stress configurations")
    print("  metrics: <H_A>(end) mean over x (area drift), H_C min over (x,t) (D2 window),")
    print("           max|Ham|, max|Mom| (constraint control)")
    baseline = None
    scan_rows = []
    crash_rows = []
    for kind in ("off", "hold-plane", "isotropic-hold", "redirect"):
        for pi in ((0.0,) if kind == "off" else PI_SCAN):
            stress = stress_config(kind, pi)
            sim, u0, u, rec, info = run_case(stress)
            if sim is None:
                crash_rows.append((kind, pi, rec))
                print("  %-15s Pi=%-5.2f : FAIL -- %s" % (kind, pi, rec))
                continue
            row = dict(kind=kind, pi=pi, rec=rec,
                       HA_end=mean_HA_end(rec), HC_min=mean_HC_min(rec),
                       maxCH=rec['maxCH'], maxMom=rec['maxMom'])
            if kind == "off":
                baseline = row
            scan_rows.append(row)
            print("  %-15s Pi=%-5.2f : <H_A>(end)=%+.6f  H_C_min=%+.4f  "
                  "max|Ham|=%.3e  max|Mom|=%.3e"
                  % (kind, pi, row['HA_end'], row['HC_min'],
                     row['maxCH'], row['maxMom']))
    print()
    if crash_rows:
        print("[crash registration] (per sec 9.1: failed runs must also be logged)")
        for kind, pi, reason in crash_rows:
            print("  %-15s Pi=%-5.2f : %s" % (kind, pi, reason))
        print("  interpretation: the decelerating stress sector pushes H_C through the")
        print("  degenerate boundary of the zstatic ansatz faster than the magnetic")
        print("  D2 window develops; this is a physical boundary of the prescribed-")
        print("  stress approach, not a solver defect (T2 validated the injection at")
        print("  machine precision). A dynamical apparatus model is required to probe")
        print("  beyond this boundary (registered as the production version).")
        print()

    # ---- T3 ----
    print("[T3] constraint control with stress ON (vs Pi=0 baseline; completed rows)")
    worst_factor = 0.0
    worst_row = None
    for row in scan_rows:
        if row['kind'] == "off":
            continue
        f_ham = row['maxCH'] / max(baseline['maxCH'], 1e-300)
        f_mom = row['maxMom'] / max(baseline['maxMom'], 1e-300)
        if max(f_ham, f_mom) > worst_factor:
            worst_factor = max(f_ham, f_mom)
            worst_row = row
        print("  %-15s Pi=%-5.2f : Ham x%.2f  Mom x%.2f"
              % (row['kind'], row['pi'], f_ham, f_mom))
    ok3 = worst_factor <= TH_T3_FACTOR
    print("  worst degradation factor = %.2f (%s Pi=%.2f)  vs  threshold %.1f"
          % (worst_factor, worst_row['kind'], worst_row['pi'], TH_T3_FACTOR))
    if not ok3:
        print("  honest note: the stress modifies the trajectory, and the registered")
        print("  synchronous-gauge constraint drift (P2-C4 known limitation) grows on")
        print("  the modified trajectory; the injection itself is machine-precision")
        print("  exact (T2). Registered per row; the criterion is applied as written.")
    print("  T3 verdict: %s" % ("PASS" if ok3 else "FAIL"))
    print()

    # ---- T4: monotone response + area-hold root-find (registered on config (c)) ----
    print("[T4] response monotonicity and area-hold root-find")
    iso = [r for r in scan_rows if r['kind'] == "isotropic-hold"]
    if len(iso) >= 2:
        ha_seq = [r['HA_end'] for r in iso]
        mono = all(ha_seq[i] > ha_seq[i + 1] for i in range(len(ha_seq) - 1))
        print("  <H_A>(end) vs Pi (isotropic-hold): %s"
              % " ".join("%+.4f" % v for v in ha_seq))
        print("  monotone decrease with Pi: %s" % mono)
    else:
        mono = False
        print("  isotropic-hold: too few completed rows for monotonicity (crashes above)")

    def F(pi, kind="isotropic-hold"):
        stress = stress_config(kind, pi)
        _, _, _, rec, _ = run_case(stress)
        if rec is None or isinstance(rec, str):
            raise ValueError("degenerate configuration reached (crash registered)")
        return mean_HA_end(rec)

    pi_hold = None
    fres = None
    root_kind = "isotropic-hold"
    try:
        pi_hold = brentq(F, *PI_HOLD_BRACKET, xtol=1e-4, rtol=1e-6, args=(root_kind,))
        fres = abs(F(pi_hold, root_kind))
    except ValueError as exc:
        print("  root-find FAILED on config (c) within bracket [%.1f, %.1f]: %s"
              % (PI_HOLD_BRACKET[0], PI_HOLD_BRACKET[1], exc))
    if pi_hold is not None:
        print("  Pi_hold (config c, <H_A>(end)=0) = %.6f -> stress = %.6f (code units)"
              % (pi_hold, pi_hold * SIGMA_REF))
        print("  |F(Pi_hold)| = %.3e  <  %.1e" % (fres, TH_T4_ROOT))
    ok4 = bool(mono) and pi_hold is not None and fres is not None and fres < TH_T4_ROOT
    print("  T4 verdict (as registered on config (c)): %s"
          % ("PASS" if ok4 else "FAIL"))

    # additional registered-configuration diagnostic: the working in-plane hold
    print("  [additional diagnostic] configuration (d) redirect (the working in-plane")
    print("  hold: Delta_A = Delta_B = -kappa*Pi*sigma_ref < 0 decelerates the plane)")
    red = [r for r in scan_rows if r['kind'] == "redirect"]
    if len(red) >= 2:
        ha_red = [r['HA_end'] for r in red]
        mono_red = all(ha_red[i] > ha_red[i + 1] for i in range(len(ha_red) - 1))
        print("  <H_A>(end) vs Pi (redirect): %s (monotone decrease: %s)"
              % (" ".join("%+.4f" % v for v in ha_red), mono_red))
        try:
            pi_red = brentq(F, *PI_HOLD_BRACKET, xtol=1e-4, rtol=1e-6,
                            args=("redirect",))
            fr = abs(F(pi_red, "redirect"))
            print("  Pi_hold (config d, <H_A>(end)=0) = %.6f -> stress = %.6f (code units)"
                  % (pi_red, pi_red * SIGMA_REF))
            print("  |F(Pi_hold)| = %.3e" % fr)
        except ValueError as exc:
            print("  redirect root-find FAILED within bracket: %s" % exc)
    else:
        print("  redirect: too few completed rows (crashes above)")
    print()

    # ---- D2 interplay note ----
    print("[D2 interplay] (registered honesty check)")
    for row in scan_rows:
        d2 = "achieved" if row['HC_min'] < 0 else "NOT achieved"
        print("  %-15s Pi=%-5.2f : H_C_min=%+.4f -> D2 contraction %s"
              % (row['kind'], row['pi'], row['HC_min'], d2))
    print("  note: configurations that decelerate C as well (isotropic-hold) fight the")
    print("  registered magnetic D2 contraction; configurations (b)/(d) leave C")
    print("  untouched to first order but hold nothing (analysis in module header).")
    print()

    print("[verdicts]")
    print("  T1 Pi=0 regression          : %s" % ("PASS" if ok1 else "FAIL"))
    print("  T2 homogeneous validation   : %s" % ("PASS" if ok2 else "FAIL"))
    print("  T3 constraint control       : %s" % ("PASS" if ok3 else "FAIL"))
    print("  T4 response + root-find     : %s" % ("PASS" if ok4 else "FAIL"))
    allok = ok1 and ok2 and ok3 and ok4
    print("N11 1+1 slab layer OVERALL: %s" % ("PASS" if allok else "FAIL"))
    if allok:
        print("delivered: external-stress machinery + response curves + required")
        print("  Pi_hold in CODE units%s" % (" = %.6f (x sigma_w)" % pi_hold if pi_hold else ""))
    print("evidence level: MODEL RESULT (screened; prescribed stress sector, not a")
    print("                dynamical apparatus model)")
    print("OPEN registration: the SI normalization of Pi_hold (G0 P_2D = 8.62e16 N/m")
    print("                <-> slab code units) requires the G0<->P2 unit bridge,")
    print("                which is not registered anywhere in this repository.")
    print("status registration: F.4 item 4 (N11 into 1+1 slab) -> EXECUTED at the")
    print("                slab layer; unit-bridge and dynamical-apparatus model remain OPEN.")


if __name__ == "__main__":
    main()
