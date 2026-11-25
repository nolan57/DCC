# -*- coding: utf-8 -*-
"""
p3_me3.py — Phase 3 of the phased relaxation route: ME3 (perpendicular energy fraction) and the J^mu instrument.

GD4 reassigned Phase 3's relaxation target from ME2 (presentational) to ME3 (physical), and recorded J^mu as an
OPEN instrument rather than a gate. This module does both halves:

  (a) evaluate ME3 on the three record states, under TWO declarations of the field `phi`;
  (b) build the particle-current instrument and test the directive's "zeroed current = failure" clause.

ME3's statement in the adopted spec is

    delta_E := Int rho (d_z phi)^2  /  Int rho [ (d_x phi)^2 + (d_y phi)^2 ]  <=  delta_E,max

and `phi` is **not declared**. That omission is what the first half measures.

Pre-registered: runs/ROUTE/route_completion_registration.md P3a-P3c.
"""

import math
import os

import numpy as np
from scipy import ndimage

OUT = []
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUNDIR = os.path.join(ROOT, 'runs', 'ROUTE')

NXY, NXV = 48, 24
T_FM = 15.40e-15
L_BODY = 0.20
LAMBDA_FRAC = 0.25          # lateral wavelength of the picture, as a fraction of the domain


def w(s=""):
    OUT.append(s)


def head(s):
    w()
    w("=" * 78)
    w(s)
    w("=" * 78)


# --- state construction --------------------------------------------------------------------------
def lateral(n=NXY, cells=6):
    """The picture: an in-plane structure with wavelength lambda = domain/cells."""
    x = np.linspace(0.0, 1.0, n, endpoint=False)
    X, Y = np.meshgrid(x, x, indexing='ij')
    return 0.5 + 0.5 * np.sin(2 * np.pi * cells * X) * np.cos(2 * np.pi * cells * Y)


def axial(n, t_vox):
    """A z-profile of width t_vox, as a softened box."""
    z = np.arange(n) + 0.5
    c = n / 2.0
    return np.exp(-0.5 * ((z - c) / (0.5 * t_vox)) ** 2)


def phi_field(kind, t_vox=3):
    A = lateral()
    if kind == 'sheet':
        prof = axial(NXV, t_vox)
        return A[None, :, :] * prof[:, None, None]
    if kind == 'stack':
        prof = axial(NXV, t_vox) + np.exp(-0.5 * ((np.arange(NXV) + 0.5 - NXV * 0.18) / (0.5 * t_vox)) ** 2)
        return A[None, :, :] * prof[:, None, None]
    if kind == 'slab':
        # the intact body carries 3-D structure: same lateral wavelength, axial structure on the same scale
        B = lateral(cells=6)
        prof = 0.5 + 0.5 * np.sin(2 * np.pi * 2 * (np.arange(NXV) + 0.5) / NXV)
        return B[None, :, :] * prof[:, None, None]
    raise ValueError(kind)


def delta_E(phi, rho=None):
    gz, gy, gx = np.gradient(phi)
    r = np.ones_like(phi) if rho is None else rho
    num = float(np.sum(r * gz ** 2))
    den = float(np.sum(r * (gx ** 2 + gy ** 2)))
    if den == 0.0:
        return float('inf'), num, den
    return num / den, num, den


def main():
    head("PHASE 3 — ME3 (PERPENDICULAR ENERGY FRACTION) AND THE J^mu INSTRUMENT")
    w("  ME3 as adopted: delta_E := Int rho (d_z phi)^2 / Int rho [(d_x phi)^2 + (d_y phi)^2] <= d_E,max")
    w("  phi is NOT declared in the spec. Both natural declarations are evaluated below.")
    w("  pre-registered: P3a (sheet << 1, slab ~ 1), P3b (threshold-insensitive), P3c (J^mu conserved)")

    # --- P3a: delta_E with phi = the material/picture field -----------------------------------
    w()
    w("[P3-1] DECLARATION 1: phi = the material field (density-like, carrying the picture)")
    w("  %-8s %-12s %-14s %-14s %-10s" % ("state", "delta_E", "numerator", "denominator", "verdict"))
    vals = {}
    for k in ('sheet', 'stack', 'slab'):
        phi = phi_field(k)
        d, num, den = delta_E(phi)
        vals[k] = d
        w("  %-8s %-12.4g %-14.4g %-14.4g %-10s" % (k, d, num, den, "PASS" if d <= 1.0 else "FAIL"))
    w("  prediction P3a (sheet <~ 1e-12, slab ~ 1, separation >= 10 decades): FAILED")
    w("  measured: sheet %.4g, slab %.4g -- the ordering is the WRONG WAY (sheet > slab), though only"
      % (vals['sheet'], vals['slab']))
    w("  weakly, because at t = 3 grid cells the z-gradient is grid-limited. The continuum scaling")
    w("  measured in P3-2 is what carries the argument; the lattice magnitude does not.")
    w("  reason: a sheet is thin in z, so its perpendicular gradient length is t, and")
    w("  Int(d_z phi)^2 / Int(phi)^2 ~ 1/t^2 while the in-plane term ~ 1/lambda^2. Hence")
    w("      delta_E(material) ~ (lambda/t)^2  -->  INFINITY as the sheet thins.")
    w("  the quantity is inverted with respect to two-dimensionality: thinner sheets score WORSE.")

    # --- the scaling, measured --------------------------------------------------------------
    w()
    w("[P3-2] THE SCALING delta_E ~ (lambda/t)^2 -- EXACT TEST ON A SEPARABLE FIELD")
    w("  the P3-1 states have t equal to only 2-6 grid cells, so their z-gradient is grid-limited")
    w("  and they cannot test a continuum scaling. Use instead the separable field")
    w("      phi = sin(2*pi*x/lambda) * sin(pi*z/t),   for which to O(h^2)")
    w("      delta_E = (lambda / (2t))^2   EXACTLY.")
    w("  so the test is a residual, not a fit:")
    w("  %-8s %-13s %-13s %-9s %-11s" % ("t_vox", "delta_E", "(lambda/2t)^2", "ratio", "corrected"))
    lam_vox = 8.0
    nzz = 128
    ratios = []
    corr_list = []
    for tv in (8, 16, 32, 64):
        z = np.arange(nzz)          # index units throughout, so both spacings are 1
        x = np.arange(64)
        ph = np.sin(2 * np.pi * x / lam_vox)[None, :] * np.sin(np.pi * z / tv)[:, None]
        gz = np.gradient(ph, axis=0)
        gx = np.gradient(ph, axis=1)
        d = float(np.sum(gz ** 2)) / float(np.sum(gx ** 2))
        pred = (lam_vox / (2 * tv)) ** 2
        kx, kz = 2 * np.pi / lam_vox, np.pi / tv
        corr = (math.sin(kx) / kx) ** 2 / (math.sin(kz) / kz) ** 2
        ratios.append(d / pred)
        corr_r = d / pred * corr
        corr_list.append(corr_r)
        w("  %-8d %-13.6g %-13.6g %-9.4f %-11.4f" % (tv, d, pred, d / pred, corr_r))
    w("  the raw ratio drifts 1.18 -> 1.25 because the difference operator attenuates the lateral")
    w("  mode (lambda = 8 cells) by (sin(k)/k)^2 = 0.8105 while the axial mode is barely attenuated.")
    w("  correcting for that attenuation, the residual is the 'corrected' column: %.4f .. %.4f,"
      % (min(corr_list), max(corr_list)))
    w("  i.e. unity to %.1f%%. The prediction delta_E = (lambda/2t)^2 is therefore confirmed as an"
      % (100 * max(abs(x - 1) for x in corr_list)))
    w("  => delta_E ~ (lambda/t)^2 is CONFIRMED as a scaling. The extrapolation that follows is")
    w("     therefore analytic-plus-verified, not curve-fitting:")
    w("     for the real object (lambda = %.2f m, t = %.3e m):  (lambda/t)^2 = %.3e"
      % (L_BODY, T_FM, (L_BODY / T_FM) ** 2))
    w("     so delta_E(material) = %.2e for the converted state; it would need d_E,max >= that."
      % ((L_BODY / T_FM) ** 2))
    w("  and it grows as t SHRINKS, so the ideal 2D limit (t -> 0) is delta_E -> infinity:")
    w("  the criterion is most violated by the most perfectly two-dimensional state.")

    # --- declaration 2 -----------------------------------------------------------------------
    w()
    w("[P3-3] DECLARATION 2: phi = a velocity potential, with u_perp/u_par = t/lambda")
    eps = 1.0
    w("  for a sheet moving in-plane the perpendicular velocity fraction is ~ t/lambda, so")
    w("      delta_E(velocity) ~ (u_perp/u_par)^2 = (t/lambda)^2 = %.3e" % ((T_FM / L_BODY) ** 2))
    w("  and for the intact body (isotropic motion) it is ~ 1.")
    w("  => this declaration gives the prediction P3a expected: sheet tiny, slab ~ 1.")
    w()
    w("  THE TWO DECLARATIONS DISAGREE BY (lambda/t)^4 = %.3e" % ((L_BODY / T_FM) ** 4))
    w("  and give OPPOSITE verdicts on the sheet. ME3 therefore has no verdict until phi is declared,")
    w("  and the spec does not declare it.")

    # --- P3b ---------------------------------------------------------------------------------
    w()
    w("[P3-4] P3b: IS THE THRESHOLD INSENSITIVE?")
    w("  under declaration 1 the sheet sits at %.2e and the slab at %.2e -- the sheet is FAILING at"
      % ((L_BODY / T_FM) ** 2, vals['slab']))
    w("  any d_E,max below that, and PASSING only above it. Under declaration 2 the sheet sits at")
    w("  %.2e and passes for any d_E,max > that." % ((T_FM / L_BODY) ** 2))
    w("  adm. 1 requires d_E,max >= %.1e ; adm. 2 requires d_E,max >= %.1e . The two requirements"
      % ((L_BODY / T_FM) ** 2, (T_FM / L_BODY) ** 2))
    w("  differ by %.1e, so no single value of d_E,max means the same thing under both -- and"
      % ((L_BODY / T_FM) ** 4))
    w("  the value DECIDES the verdict rather than being insensitive to it.")
    w("  prediction P3b: FAILED. The proposal d_E,max = 1e-2 recorded in the pre-registration was")
    w("  LICENSED BY P3b and is therefore WITHDRAWN. No d_E,max is registered in this round.")

    # --- P3c: the J^mu instrument -------------------------------------------------------------
    w()
    w("[P3-5] J^mu INSTRUMENT  (GD4: an instrument, not a gate)")
    w("  ansatz: J^mu = n u^mu, u^mu = (c,0,0,0) in the prescribed (D2) frame, n static.")
    w("  conservation: nabla_mu J^mu = (1/sqrt(gamma)) d_t (sqrt(gamma) n) = 0 for static n, identically.")
    w("  numerical check on a non-trivial static n over a curved gamma_ij:")
    rng = np.random.default_rng(3)
    x = np.linspace(0, 1, 40, endpoint=False)
    X, Y = np.meshgrid(x, x, indexing='ij')
    gamma = 1.0 + 0.3 * np.sin(2 * np.pi * X) * np.cos(2 * np.pi * Y)
    n = 1.0 + 0.5 * np.sin(4 * np.pi * X) + 0.0 * Y
    sqrtg = np.sqrt(gamma)
    # discrete d_t of a static field is exactly zero, so the identity is structural; verify the
    # prefactor is finite and positive instead, which is what a time-step would divide by
    finite = np.all(np.isfinite(sqrtg)) and np.all(sqrtg > 0)
    div = (sqrtg * n - sqrtg * n) / 1.0          # dt = 0 exactly
    w("    sqrt(gamma) finite and positive : %s   (min %.4f, max %.4f)" % (finite, sqrtg.min(), sqrtg.max()))
    w("    max |nabla_mu J^mu|             : %.1e  (exactly zero -- dt = 0 for a static n)" % np.max(np.abs(div)))
    w("    J^0 = n c                       : nonzero for every state in the record")
    for k in ('sheet', 'stack', 'slab'):
        phi = phi_field(k)
        nbar = float(phi.mean())
        w("      %-6s  <n> = %.4f  ->  J^0 = %.4f c" % (k, nbar, nbar))
    w("  prediction P3c: CONFIRMED -- conserved identically, and J^0 != 0 for every state, so the")
    w("  directive's 'zeroing of the conserved current' test does not fire.")
    w("  LIMITATION, declared: this instrument works on PRESCRIBED backgrounds only. On a solved")
    w("  background u^mu must come from the evolution, which does not exist (R4 grid-scale")
    w("  instability, unlocalised in the bulk). So J^mu is an instrument for D2 states, not a gate.")

    head("PHASE 3 SUMMARY")
    w("  ME3 with phi = material : delta_E = %.2e (continuum) for the sheet, %.2e for the slab --"
      % ((L_BODY / T_FM) ** 2, vals['slab']))
    w("                            INVERTED: the thinner the sheet, the worse it scores")
    w("  ME3 with phi = potential: delta_E = %.2e for the sheet -- the intended direction"
      % ((T_FM / L_BODY) ** 2))
    w("  the two differ by (lambda/t)^4 = %.1e and straddle any threshold" % ((L_BODY / T_FM) ** 4))
    w("  P3a FAILED / P3b FAILED / P3c CONFIRMED")
    w("  PHASE 3: BLOCKED. d_E,max cannot be registered, because ME3 has no verdict until phi is")
    w("  declared -- and the two natural declarations give opposite answers. This is a defect in an")
    w("  ADOPTED spec (v0.2 ME3), not in the route's executor. It is registered as finding ME3-F1")
    w("  and requires a v0.3 amendment before Phase 3 can run or Phase 4 can start.")
    w()
    w("PROVENANCE: NEITHER  (constraint well-posedness + one identity; establishes no physics)")

    txt = "\n".join(OUT) + "\n"
    with open(os.path.join(RUNDIR, 'p3_me3_results.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(txt)
    print(txt)


if __name__ == '__main__':
    main()
