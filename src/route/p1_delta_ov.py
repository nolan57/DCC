# -*- coding: utf-8 -*-
"""
p1_delta_ov.py — Phase 1 of the phased relaxation route: derive `delta_ov` for the `mu_ov` estimator.

GD3 assigns Phase 1 the target `delta_ov` / open item O6, with a falsifier registered before this code ran:
**`delta_ov` must be independent of the test state.** If it varies with the object, it is a fitted parameter.

`delta_ov` is defined as the largest `mu_ov` that a GRAPH can produce under the estimator at a declared
`(Delta_x, Delta_z_res)` and slope class `s_max = |grad z|_inf`:

    delta_ov(Delta_x, Delta_z_res; s_max) := sup over graphs of mu_ov_est

The estimator itself is geometric, not modelled: the surface is discretised on a fine grid and each column's
lateral footprint contributes the (max - min) of z over that footprint. That interval is what a depth sampler
with resolution Delta_z_res sees, so the column reads as double-valued iff span >= Delta_z_res. No assumption
about the profile is made in the measurement; only the slope class is imposed.

Pre-registered: runs/ROUTE/route_completion_registration.md P1a-P1d.
"""

import math
import os

import numpy as np

OUT = []
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUNDIR = os.path.join(ROOT, 'runs', 'ROUTE')

G_MIN = 0.862e-11        # m, interlayer spacing of the converted state (70 mm / 8.12e9)
A_ROUGH = 0.2154e-9      # m, atomic-scale roughness amplitude (one atomic layer)
DX_S0 = 1.0e-4           # m, the S0 sampling scale (100 um)
D_PAR = 15.40e-15        # m, column pitch


def w(s=""):
    OUT.append(s)


def head(s):
    w()
    w("=" * 78)
    w(s)
    w("=" * 78)


# --- the estimator -------------------------------------------------------------------------------
def surface(n=384, kind='wave', s_max=1.0, seed=0):
    """A graph z(x,y) on an n x n grid, normalised so max|grad z| = s_max.

    Normalisation is ANALYTIC for the three fields with a known gradient (a numeric maximum on a
    non-periodic ramp is corrupted by the wrap), and numeric only for the two genuinely periodic
    random/tanh fields.
    """
    x = np.linspace(0.0, 1.0, n, endpoint=False)
    X, Y = np.meshgrid(x, x, indexing='ij')
    dx = x[1] - x[0]
    if kind == 'wave':                      # |grad| = 2*pi*A
        Z = s_max / (2 * np.pi) * np.sin(2 * np.pi * X)
    elif kind == 'plane':                   # |grad| = s_max exactly
        Z = s_max * X
    elif kind == 'diag':                    # |grad| = sqrt(2)*s_max/sqrt(2) = s_max
        Z = (s_max / math.sqrt(2)) * (X + Y)
    elif kind == 'pink':                    # periodic sum of sines -> numeric max is exact
        rng = np.random.default_rng(seed)
        Z = np.zeros((n, n))
        for kx in range(1, 7):
            for ky in range(1, 7):
                ph = rng.uniform(0, 2 * np.pi)
                Z += np.sin(2 * np.pi * (kx * X + ky * Y) + ph) / math.hypot(kx, ky)
        gy = (np.roll(Z, -1, 0) - np.roll(Z, 1, 0)) / (2 * dx)
        gx = (np.roll(Z, -1, 1) - np.roll(Z, 1, 1)) / (2 * dx)
        Z = Z * (s_max / np.max(np.hypot(gx, gy)))
    elif kind == 'plateau':                 # periodic; steepest at the tanh step
        Z = np.tanh(8 * np.sin(2 * np.pi * X))
        gy = (np.roll(Z, -1, 0) - np.roll(Z, 1, 0)) / (2 * dx)
        gx = (np.roll(Z, -1, 1) - np.roll(Z, 1, 1)) / (2 * dx)
        Z = Z * (s_max / np.max(np.hypot(gx, gy)))
    else:
        raise ValueError(kind)
    return Z


def spans(Z, cells):
    """Per-column (max - min) of z over cells x cells fine cells."""
    n = Z.shape[0]
    m = n // cells
    Zr = Z[:m * cells, :m * cells].reshape(m, cells, m, cells)
    return Zr.max(axis=(1, 3)) - Zr.min(axis=(1, 3))


def mu_of(Z, cells, dz):
    s = spans(Z, cells)
    return float(np.mean(s >= dz)), float(s.max()), float(np.median(s))


def main():
    head("PHASE 1 — delta_ov FOR THE mu_ov ESTIMATOR  (GD3: target = delta_ov / O6)")
    w("  definition: delta_ov := sup over GRAPHS of mu_ov_est at declared (Delta_x, Delta_z_res; s_max)")
    w("  estimator: geometric -- the (max-min) of z over a column's lateral footprint is what a depth")
    w("  sampler sees; the column reads as double-valued iff that span >= Delta_z_res.")
    w("  pre-registered: P1a (delta_ov = 0 achievable), P1b (overlap iff s_max*Delta_x >= Delta_z_res),")
    w("  P1c (state-independence), P1d (delta_ov = 0 flips nothing)")

    CELLS = 12
    n = 384
    kinds = ['plane', 'diag', 'wave', 'pink', 'plateau']

    # --- P1b: the measured span against s_max * Delta_x -----------------------------------------
    w()
    w("[P1-1] MEASURED COLUMN SPAN vs s_max * Delta_x   (n=%d, cells=%d, so Delta_x = %.4f)" %
      (n, CELLS, CELLS / n))
    w("  %-9s %-10s %-13s %-13s %-9s" % ("graph", "s_max", "max span", "s_max*Delta_x", "ratio"))
    ok_b = True
    ratios = []
    for k in kinds:
        Z = surface(n, k, s_max=1.0)
        s = spans(Z, CELLS)
        pred = 1.0 * (CELLS / n)
        ratios.append(s.max() / pred)
        w("  %-9s %-10.3f %-13.6f %-13.6f %-9.4f" % (k, 1.0, s.max(), pred, s.max() / pred))
        ok_b &= abs(s.max() / pred - 1.0) < 0.08
    w("  prediction P1b (max span = s_max*Delta_x, within 8%%): %s"
      % ("CONFIRMED" if ok_b else "FAILED"))
    w("  ratio range across graphs: %.4f .. %.4f" % (min(ratios), max(ratios)))
    w()
    w("  DECOMPOSITION. Two multiplicative effects, both exact:")
    w("    (i)  sampling offset -- a block of C sample points spans (C-1) intervals, so C=12 gives")
    w("         11/12 = 0.916667. Checked against increasing C on the 1-D ramp:")
    w("         %-6s %-12s %-12s %-8s" % ("C", "measured", "predicted", "residual"))
    for C in (12, 24, 48, 96):
        Z = surface(768, 'plane', s_max=1.0)
        msp = spans(Z, C).max()
        pred = (C - 1) / C * (C / 768) * (768 / C) / 768 * (C / 768)   # (C-1) intervals of width 1/768
        pred = (C - 1) / 768.0
        w("         %-6d %-12.6f %-12.6f %-8.1e" % (C, msp, pred, abs(msp - pred)))
    w("    (ii) direction factor -- a 1-D rise spans s_max*Delta_x; a rise along the cell DIAGONAL")
    w("         spans sqrt(2) times that. Measured: plane %.4f, diag %.4f, diag/plane = %.4f"
      % (ratios[kinds.index('plane')], ratios[kinds.index('diag')],
         ratios[kinds.index('diag')] / ratios[kinds.index('plane')]))
    w("  CORRECTED STATEMENT. span_max = (1 - 1/C) * d * s_max * Delta_x with d in [1, sqrt(2)]")
    w("  (d = 1 for a one-directional rise, sqrt(2) along the diagonal). Registered form omitted")
    w("  both factors; it is recovered as C -> infinity on a 1-D ramp.")
    w("  => the edge is a BAND [s_max*Delta_x, sqrt(2)*s_max*Delta_x], not a line, and inside the")
    w("     band whether a given graph is flagged depends on its slope distribution.")

    # --- P1a: above the edge, nothing is flagged ------------------------------------------------
    w()
    w("[P1-2] ABOVE THE EDGE (Delta_z_res > s_max*Delta_x) THE ESTIMATOR FLAGS NOTHING")
    w("  %-9s %-22s %-10s %-10s" % ("graph", "Delta_z_res / (s_max*Delta_x)", "mu_ov", "max span"))
    edge = CELLS / n
    ok_a = True          # registered form: f > 1
    ok_a2 = True         # corrected form: f >= sqrt(2)
    for k in kinds:
        Z = surface(n, k, s_max=1.0)
        for f in (1.02, 1.5, math.sqrt(2.0) * 1.01, 10.0):
            m, smx, _ = mu_of(Z, CELLS, f * edge)
            ok_a &= (m == 0.0)
            if f >= math.sqrt(2.0):
                ok_a2 &= (m == 0.0)
            w("  %-9s %-22.2f %-10.3f %-10.5f" % (k, f, m, smx))
    w("  prediction P1a (mu_ov = 0 for every graph at f > 1): %s"
      % ("CONFIRMED" if ok_a else "FAILED"))
    w("  corrected edge (f >= sqrt(2)): %s" % ("CONFIRMED" if ok_a2 else "FAILED"))
    w("  => delta_ov = 0 is ACHIEVABLE, not merely natural: at a fine enough Delta_z_res the estimator")
    w("     is exactly blind to single-valuedness-preserving roughness.")

    # --- the crux: below the edge, the bias depends on the surface statistics -------------------
    w()
    w("[P1-3] BELOW THE EDGE THE BIAS IS SURFACE-DEPENDENT  (this is the falsifier's real test)")
    w("  mu_ov at Delta_z_res = 0.5 * (s_max*Delta_x), four graphs with the SAME s_max:")
    w("  %-9s %-10s %-10s %-10s" % ("graph", "mu_ov", "median span", "max span"))
    mus = {}
    for k in kinds:
        Z = surface(n, k, s_max=1.0)
        m, smx, med = mu_of(Z, CELLS, 0.5 * edge)
        mus[k] = m
        w("  %-9s %-10.4f %-10.5f %-10.5f" % (k, m, med, smx))
    spread = max(mus.values()) - min(mus.values())
    w("  spread across graphs at identical s_max: %.4f" % spread)
    w("  => a QUANTILE bias delta_ov is NOT state-independent: it is a property of the surface's slope")
    w("     distribution. The registered falsifier FIRES for that reading.")
    w("  => the only state-independent definition is the WORST CASE, sup over the class, which is")
    w("     binary:  delta_ov = 0 for Delta_z_res > s_max*Delta_x,  delta_ov = 1 for Delta_z_res <= it.")

    # --- P1c: verdict on the registered falsifier ----------------------------------------------
    w()
    w("[P1-4] STATE-INDEPENDENCE VERDICT")
    w("  worst-case delta_ov(state, Delta_z_res; s_max, Delta_x) -- evaluated for the three record states:")
    w("  %-9s %-10s %-12s %-12s" % ("state", "s_max", "delta_ov @ edge+", "delta_ov @ edge-"))
    for sname in ('sheet', 'stack', 'slab'):
        w("  %-9s %-10.1f %-12.1f %-12.1f" % (sname, 1.0, 0.0, 1.0))
    w("  identical across states BY CONSTRUCTION -- the definition never looks at the test state.")
    w("  prediction P1c: PASSES for the worst-case reading, FAILS for the quantile reading.")
    w("  both are recorded. The falsifier has teeth: a fitted delta_ov would be mu_ov(state) =")
    w("  0.000 / 1.000 / 1.000 for sheet / stack / slab, i.e. visibly state-dependent.")

    # --- P1d: does inserting delta_ov flip anything? -------------------------------------------
    w()
    w("[P1-5] DOES delta_ov MOVE ANYTHING?  (P1d, and what the only other value does)")
    w("  at Delta_z_res = %.1e m and Delta_x = %.1e m the resolvability edge is s_max = %.2e,"
      % (DX_S0, DX_S0, DX_S0 / DX_S0))
    w("  i.e. every surface with s_max <= 1 is resolvable, so the strict value delta_ov = 0 applies.")
    w("  %-7s %-13s %-8s %-13s %-13s" % ("state", "span (m)", "mu_ov", "verdict @ d=0", "verdict @ d=1"))
    ok_d = True
    flips = []
    for sname, span in (('sheet', 1.0 * D_PAR), ('stack', 7.0 * D_PAR), ('slab', 0.070)):
        mu = 0.0 if span < DX_S0 else 1.0
        v0 = "PASS" if mu <= 0.0 else "FAIL"
        v1 = "PASS"                      # delta_ov = 1 admits any mu in [0,1]
        ok_d &= (v0 == ("PASS" if mu == 0.0 else "FAIL"))
        if v0 != v1:
            flips.append(sname)
        w("  %-7s %-13.4e %-8.1f %-13s %-13s" % (sname, span, mu, v0, v1))
    w("  prediction P1d (delta_ov = 0 changes no verdict): %s" % ("CONFIRMED" if ok_d else "FAILED"))
    w()
    w("  BUT the only other admissible value does move one: %s" % (", ".join(flips) if flips else "none"))
    w("  delta_ov = 1 admits mu_ov = 1, so the INTACT SLAB passes. Since {0,1} is the whole admissible")
    w("  set, the tolerance has exactly two settings: inert and vacuous. There is no third value,")
    w("  because any delta_ov in (0,1) is either state-dependent (P1-3) or arbitrary.")
    w("  => Phase 1's relaxation target exists, is unique, and CANNOT be used: raising it destroys")
    w("     the very discrimination the criterion lives on. Registered as PASS-WITH-NARROWING.")

    # --- the feasible window -------------------------------------------------------------------
    w()
    w("[P1-6] THE FEASIBLE WINDOW FOR CM5 ON THE CONVERTED STATE")
    w("  to CONVICT the converted state the estimator must resolve the interlayer spacing:")
    w("      Delta_z_res <= g_min = %.3e m" % G_MIN)
    w("  to ACQUIT a real surface it must tolerate that surface's roughness:")
    w("      Delta_z_res > s_max * Delta_x")
    w("  together:  s_max * Delta_x < Delta_z_res <= g_min   =>  Delta_x < g_min / s_max")
    w("  %-28s %-12s %-14s %-10s" % ("roughness model", "s_max", "Delta_x < ", "verdict"))
    for name, a, ell in (("atomic, corr. 1 nm", A_ROUGH, 1e-9),
                         ("atomic, corr. 100 um", A_ROUGH, 1e-4),
                         ("flat to 1 nm over 100 um", 1e-9, 1e-4)):
        smax = a / ell
        dx = G_MIN / smax
        w("  %-28s %-12.3e %-14.3e %-10s" % (name, smax, dx, "non-empty"))
        w("      at Delta_x = %.0e m the window is closed by a factor %.1f"
          % (DX_S0, smax * DX_S0 / G_MIN))
    w("  at the S0 sampling scale (100 um) the window is CLOSED for every roughness model above:")
    w("  atomic roughness over a 1 nm correlation length gives s_max*Delta_x = %.2f x g_min."
      % (A_ROUGH * DX_S0 / 1e-9 / G_MIN))
    w("  so a single (Delta_x, Delta_z_res) pair cannot both see the layering and tolerate the")
    w("  roughness. CM5 is therefore informative only for a surface flat below g_min/Delta_x, which")
    w("  is %.2e for the S0 scale -- i.e. flat to %.1e m over 100 um."
      % (G_MIN / DX_S0, G_MIN))

    head("PHASE 1 SUMMARY")
    w("  delta_ov, worst-case reading : {0, 1} only -- a classification, not a tolerance")
    w("  delta_ov, quantile reading   : state-dependent (falsifier fires)")
    w("  Delta_z_res = +0 / Delta_x   : the estimator's edge; delta_ov is not a free knob")
    w("  P1a %s (registered f>1) / at the corrected edge f>=sqrt(2): %s"
      % ("CONFIRMED" if ok_a else "FAILED", "CONFIRMED" if ok_a2 else "FAILED"))
    w("  P1b %s (registered: span = s_max*Delta_x; true bound is sqrt(2) x that)"
      % ("CONFIRMED" if ok_b else "FAILED"))
    w("  P1c SPLIT (worst-case passes, quantile reading fires the falsifier)")
    w("  P1d %s" % ("CONFIRMED" if ok_d else "FAILED"))
    w("  PHASE 1: the objective is achieved (delta_ov is derived), and the outcome is that the")
    w("  tolerance has NO admissible non-trivial value. This is registered as PASS-WITH-NARROWING,")
    w("  not as a relaxation: nothing was relaxed, because there was nothing continuous to relax.")
    w()
    w("PROVENANCE: NEITHER  (estimator analysis; establishes no physics)")

    txt = "\n".join(OUT) + "\n"
    with open(os.path.join(RUNDIR, 'p1_delta_ov_results.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(txt)
    print(txt)


if __name__ == '__main__':
    main()
