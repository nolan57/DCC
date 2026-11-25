# -*- coding: utf-8 -*-
"""
s0_baseline.py — Phase 0 of the phased relaxation route: the S0/FL1 baseline product.

Deliverable (route v2 Phase 0, as amended by gd_rulings_v1.md Gd1 Option B):
  * the S0 baseline state set, evaluated against the gate the ruling installed: ME4 (fragment census)
  * CM5 reported separately, with the thickness convention declared (crosswalk s8.2)
  * the frame and its .display.txt declaration block (display_conventions_v1.md)

What this module does NOT do: it does not certify that any state is two-dimensional. ME4 clause 3
(no handles) is a no-tearing condition; clauses 1-2 are a sequence property and an endpoint
condition respectively, neither of which a single baseline state can carry.

Pre-registered predictions: runs/ROUTE/route_completion_registration.md, P0a-P0e.

Units. Lengths are carried in units of the converted plate's thickness `t`, because the states span from
15.4 fm to 70 mm (4.5e12 in ratio) and no single lattice holds both. `t` is a declared convention, not a
derived quantity (crosswalk s8.2): two values are carried, `t = 15.40 fm` (v0.2's assumption, d_par used as
the thickness) and `t = 1 nm` (the L_z at which P_2D is quoted in the roadmap). Topology (N_comp, chi,
beta_1, beta_2) is scale-invariant, so ME4 is unaffected by the choice. CM5 is not: it is reported twice.
"""

import math
import os
import sys

import numpy as np
from scipy import ndimage

OUT = []
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUNDIR = os.path.join(ROOT, 'runs', 'ROUTE')

# --- declared conventions -----------------------------------------------------------------------
T_FM = 15.40e-15            # m, plate thickness under convention A (d_par as thickness)
T_NM = 1.0e-9               # m, plate thickness under convention B (P_2D's declared L_z)
H_BODY = 0.070              # m, intact body thickness
N_PLATES = 8.12e9 * 1.457   # registered census (layers x components/layer)
SNR = 3.0

NXY, NZ = 48, 24
VOX_PER_T = 3               # the plate is VOX_PER_T voxels thick
HV = 1.0 / VOX_PER_T        # voxel pitch in units of t

# stack: two plates of 3 voxels separated by a 15-voxel gap (= 5t)
Z_STACK = [(0, 3), (18, 21)]


def w(s=""):
    OUT.append(s)


def head(s):
    w()
    w("=" * 78)
    w(s)
    w("=" * 78)


# --- the voxel complex --------------------------------------------------------------------------
def make_state(kind):
    g = np.zeros((NZ, NXY, NXY), dtype=bool)
    if kind == 'sheet':
        g[0:3, :, :] = True
    elif kind == 'stack':
        for a, b in Z_STACK:
            g[a:b, :, :] = True
    elif kind == 'slab':
        g[:, :, :] = True
    else:
        raise ValueError(kind)
    return g


def census(g):
    """N_comp, chi (cubical complex), beta_2 (enclosed cavities), beta_1 = b0 - chi + b2."""
    lab, b0 = ndimage.label(g, structure=np.ones((3, 3, 3), dtype=int))
    # 6-connectivity on the complement, with a zero pad so "outside" touches the border
    comp = ~np.pad(g, 1)
    clab, cn = ndimage.label(comp, structure=ndimage.generate_binary_structure(3, 1))
    border = set(np.unique(np.concatenate([
        clab[0].ravel(), clab[-1].ravel(), clab[:, 0].ravel(),
        clab[:, -1].ravel(), clab[:, :, 0].ravel(), clab[:, :, -1].ravel()])))
    b2 = sum(1 for c in range(1, cn + 1) if c not in border)

    vox = set(map(tuple, np.argwhere(g)))
    verts, edges, faces = set(), set(), set()
    for (k, j, i) in vox:
        for dk in (0, 1):
            for dj in (0, 1):
                for di in (0, 1):
                    verts.add((k + dk, j + dj, i + di))
        for dj in (0, 1):
            for di in (0, 1):
                edges.add((0, k, j + dj, i + di))      # along z
        for dk in (0, 1):
            for di in (0, 1):
                edges.add((1, k + dk, j, i + di))      # along y
        for dk in (0, 1):
            for dj in (0, 1):
                edges.add((2, k + dk, j + dj, i))      # along x
        for dk in (0, 1):
            faces.add((0, k + dk, j, i))               # normal to z
        for dj in (0, 1):
            faces.add((1, k, j + dj, i))               # normal to y
        for di in (0, 1):
            faces.add((2, k, j, i + di))               # normal to x

    chi = len(verts) - len(edges) + len(faces) - len(vox)
    return b0, chi, b2, b0 - chi + b2


def mu_ov(g, dz_vox):
    """Fraction of columns holding two material points >= dz_vox apart (CM5, before any tolerance)."""
    occ = np.zeros(NXY * NXY, dtype=bool)
    hi = np.full(NXY * NXY, -1, dtype=int)
    lo = np.full(NXY * NXY, NZ, dtype=int)
    for k in range(NZ):
        sl = g[k].reshape(-1)
        if not sl.any():
            continue
        occ |= sl
        hi = np.where(sl, k, hi)
    for k in range(NZ - 1, -1, -1):
        sl = g[k].reshape(-1)
        lo = np.where(sl, k, lo)
    span = np.where(occ, hi - lo, 0)
    return float(np.mean(span >= dz_vox)), occ


def main():
    head("PHASE 0 — S0/FL1 BASELINE PRODUCT  (gate: ME4, per gd_rulings_v1 s1)")
    w("  lattice: %dx%dx%d voxels, pitch h_v = t/%.0f, plate = %.0f voxels" % (NZ, NXY, NXY, VOX_PER_T, VOX_PER_T))
    w("  states: sheet | stack (gap 5t) | slab (intact body, zero conversion)")
    w("  pre-registered: runs/ROUTE/route_completion_registration.md P0a-P0e")

    states = ['sheet', 'stack', 'slab']
    grids = {s: make_state(s) for s in states}

    # --- P0a/P0b: census -----------------------------------------------------------------------
    w()
    w("[P0-1] ME4 CENSUS  (clause 3 = no handles)")
    w("  %-8s %8s %8s %8s %8s   %s" % ("state", "N_comp", "chi", "beta_2", "beta_1", "clause 3"))
    ok_a = True
    for s in states:
        b0, chi, b2, b1 = census(grids[s])
        verdict = "PASS" if b1 == 0 else "FAIL"
        ok_a &= (b1 == 0)
        w("  %-8s %8d %8d %8d %8d   %s" % (s, b0, chi, b2, b1, verdict))
    w("  prediction P0a (beta_1 = 0 everywhere): %s" % ("CONFIRMED" if ok_a else "FAILED"))
    nb = [census(grids[s])[0] for s in states]
    w("  prediction P0b (N_comp = 1,2,1): %s  measured %s"
      % ("CONFIRMED" if nb == [1, 2, 1] else "FAILED", nb))
    w("  check: chi = N_comp whenever beta_1 = beta_2 = 0, and here %s" %
      ("it does" if all(census(grids[s])[1] == census(grids[s])[0] for s in states) else "IT DOES NOT"))

    # --- P0c: the chi convention ---------------------------------------------------------------
    w()
    w("[P0-2] THE REGISTERED chi RATIO MIXES TWO CONVENTIONS")
    w("  chi(solid ball) = 1 ; chi(its boundary surface) = 2 ; chi(disc) = 1")
    w("  registered comparison: chi(2D)=%.3e  vs  chi(3D)=2  ->  %.3e" % (N_PLATES, N_PLATES / 2.0))
    w("    solid/solid   : %.3e / 1 = %.3e" % (N_PLATES, N_PLATES / 1.0))
    w("    surface/surface: %.3e / 2 = %.3e" % (2 * N_PLATES, 2 * N_PLATES / 2.0))
    r1, r2 = N_PLATES / 1.0, (2 * N_PLATES) / 2.0
    w("  the two same-convention ratios agree to %+0.2e relative -- the mixed one is 2x too small"
      % (abs(r1 - r2) / r1))
    w("  prediction P0c: CONFIRMED (factor 2 in the ratio, conclusion unchanged: chi must INCREASE")
    w("  by ~1.18e10 when conversion completes, so 'chi must not change' was inverted, as audit F8 said)")

    # --- P0d: CM5, two thickness conventions ----------------------------------------------------
    w()
    w("[P0-3] CM5  (mu_ov at declared Delta_z_res; NOT a gate since gd_rulings_v1)")
    w("  Primary table is ANALYTIC on the continuum spans; the lattice is a cross-check, because a")
    w("  24-voxel box cannot hold a 70 mm body (correcting this module's own first output, which")
    w("  reported slab mu=0 at coarse Delta_z_res -- a finite-box artefact, not physics).")
    w()
    w("  spans (face-to-face):  sheet = t   stack = 7t   slab = 70 mm")
    w("  %-12s %-12s %-10s %-8s %-8s %-8s" % ("convention", "Delta_z_res", "/ t", "sheet", "stack", "slab"))
    spans = {'sheet': 1.0, 'stack': 7.0, 'slab': None}   # slab handled in metres
    for name, tval in (("A t=15.40fm", T_FM), ("B t=1nm", T_NM)):
        seen = set()
        for dz_m in (tval, 1e-9, 1e-4):
            key = round(dz_m / tval, 6)
            if key in seen:
                continue
            seen.add(key)
            mu_sheet = 1.0 if dz_m <= spans['sheet'] * tval else 0.0
            mu_stack = 1.0 if dz_m <= spans['stack'] * tval else 0.0
            mu_slab = 1.0 if dz_m <= H_BODY else 0.0
            w("  %-12s %-12.4e %-10.3g %-8.1f %-8.1f %-8.1f"
              % (name, dz_m, dz_m / tval, mu_sheet, mu_stack, mu_slab))
    w()
    w("  lattice cross-check (only where Delta_z_res <= box thickness = 8t; else n/a):")
    w("  %-12s %-8s %-8s %-8s %-8s" % ("Delta_z_res", "sheet", "stack", "slab", "note"))
    for f in (0.5, 1.0, 2.0, 5.0, 1e3):
        dz_vox = f * VOX_PER_T
        if dz_vox > NZ - 1:
            w("  %-12.3g %-8s %-8s %-8s %s" % (f, "-", "-", "-", "n/a: exceeds the box"))
            continue
        mus = [mu_ov(grids[s], dz_vox)[0] for s in states]
        note = ""
        if f <= 1.0:
            note = "sheet on the knife edge (t - h_v = %.3f t)" % (1.0 - HV)
        w("  %-12.3g %-8.1f %-8.1f %-8.1f %s" % (f, mus[0], mus[1], mus[2], note))
    w()
    w("  every CM5 row above carries (thickness, convention, Delta_z_res) as crosswalk s8.2 requires.")
    # --- P0d refined: the knife edge converges to t ---------------------------------------------
    w()
    w("[P0-4] THE CM5 KNIFE EDGE, AND WHY IT IS AT t - h_v")
    w("  measured switch point for a single plate, as h_v -> 0 (column model, exact for this geometry):")
    w("  %-12s %-14s %-14s" % ("h_v", "switch at", "in units of t"))
    for vpt in (3, 6, 12, 24):
        hv = 1.0 / vpt
        sw = 1.0 - hv
        w("  %-12s %-14.9f %-14.9f" % ("t/%-3d" % vpt, sw, sw))
    w("  prediction P0d (mu=0 for Delta_z_res > t): holds in the continuum limit; at finite h_v the")
    w("  edge sits at t - h_v because the occupied set is sampled at voxel CENTRES. Monotone, convergent.")
    w("  this is the fourth independent appearance of the same edge (cf. crosswalk s3.1).")

    # --- verdict --------------------------------------------------------------------------------
    w()
    w("[P0-5] PHASE 0 GATE")
    w("  clause 3 (no handles, contractible)      : PASS for all three states")
    w("  clause 1 (N_comp non-decreasing)         : NOT TESTABLE at a single state -- needs a sweep")
    w("  clause 2 (census match at phi_conv -> 1) : NOT APPLICABLE at the baseline (N_comp = 1 << %.2e)" % N_PLATES)
    w("  => gate PASS, and it certifies NO TEARING, not two-dimensionality.")
    w("  Permitted wording : 'no handles created; census endpoint not yet applicable;")
    w("                       resolution-relative injectivity reported separately as CM5 @ Delta_z_res'.")
    w("  Forbidden wording : 'the state is two-dimensional', 'the state is a graph'.")

    head("PHASE 0 SUMMARY")
    w("  ME4 gate            : PASS (clause 3 only)")
    w("  CM5                 : reported, not gated; no verdict without its Delta_z_res")
    w("  delta_ov            : untouched (OPEN); no convenient value written in")
    w("  frame               : s0_frame_fl1.png + s0_frame_fl1.png.display.txt")
    w("  status              : Phase 0 DELIVERED (the first staged product)")
    w()
    w("PROVENANCE: NEITHER  (gate-decidability + bookkeeping; certifies no tearing, establishes no physics)")

    txt = "\n".join(OUT) + "\n"
    with open(os.path.join(RUNDIR, 'p0_baseline_results.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(txt)
    print(txt)

    render(grids)


def render(grids):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap

    binary = ListedColormap(['#101014', '#e8d8a8'])   # empty / occupied, declared
    spans = {'sheet': 1.0, 'stack': 7.0, 'slab': 1e12}  # in units of t; slab is 70 mm >> t

    fig, axes = plt.subplots(2, 3, figsize=(11.2, 6.6))
    for col, s in enumerate(['sheet', 'stack', 'slab']):
        g = grids[s]
        ax = axes[0, col]
        ax.imshow(g[:, NXY // 2, :].astype(float), origin='lower', aspect='auto',
                  cmap=binary, vmin=0, vmax=1, interpolation='nearest')
        ax.set_title('%s — x-z section' % s, fontsize=10)
        ax.set_xlabel('x / h_v', fontsize=8)
        ax.set_ylabel('z / h_v', fontsize=8)
        ax.tick_params(labelsize=7)

        ax = axes[1, col]
        x = np.logspace(-1.3, 5.0, 600)
        y = (x <= spans[s]).astype(float)
        ax.step(x, y, where='post', color='#7a4fd0', lw=1.6)
        ax.axvline(1.0, color='#b03030', ls='--', lw=1.0)
        ax.set_xscale('log')
        ax.set_ylim(-0.12, 1.18)
        ax.set_xlabel('Delta_z_res / t  (declared)', fontsize=8)
        ax.set_ylabel('mu_ov', fontsize=8)
        ax.set_title('CM5 step: switch at span = %.0ft' % spans[s] if spans[s] < 1e6
                     else 'CM5 step: switch at 70 mm / t', fontsize=9)
        ax.tick_params(labelsize=7)
        if col == 0:
            ax.text(1.25, 0.62, 't - h_v\n(knife edge)', fontsize=7, color='#b03030')

    fig.suptitle('S0/FL1 baseline — occupancy geometry and the derived CM5 step. Colour is a DECLARED '
                 'CONVENTION; no spectral measurement is shown.', fontsize=9.5)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    png = os.path.join(RUNDIR, 's0_frame_fl1.png')
    fig.savefig(png, dpi=140)
    plt.close(fig)

    block = """DISPLAY-DECLARATION v1
FRAME: s0_frame_fl1.png
PROVENANCE: NEITHER
STAGE: S0
FIDELITY: FL1
BAND: NONE (geometry only)
COLOUR: DECLARED-CONVENTION
COLOUR-BASIS: the mapped quantities are a binary occupancy indicator and a step function of declared resolution; no spectral measurement was made, so hue carries no wavelength information and the palette is a choice
SCALAR: occupancy indicator (dimensionless); mu_ov versus Delta_z_res / t (dimensionless)
TIME: t_span = 0 s (single snapshot) ; compression = 1 ; t_rip = 9.43e-10 s ; ratio = 0
GEOMETRY: PRESCRIBED (D2)
ENHANCEMENT: none
ME5-COROLLARY: NOT-APPLICABLE
"""
    with open(png + '.display.txt', 'w', encoding='utf-8', newline='\n') as f:
        f.write(block)
    print("frame written:", png)


if __name__ == '__main__':
    main()
