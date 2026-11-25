# -*- coding: utf-8 -*-
"""
front_sweep_v1.py -- How exactly does the "unfolding" process happen when the
2D-reduction front sweeps through the human body?

Building on the four-question verdict of unfold_is_real_v1 (area is arithmetic,
the inside of each sheet is unchanged, the order is encoded, the process is a
cut), this module answers two questions:

  A. After the cut, is it "8.1 billion sheets" or "more fragments"? (connected
     components)
  B. During the time the front sweeps through, what does each layer of matter
     undergo in turn? Can it physically be completed continuously?

B breaks down into four ledgers:
  B1 microscopic sequence: cut -> spread -> land; each layer is an SE(2) rigid
     motion (intra-sheet strain identically 0)
  B2 time ledger: layer emission rate, transport distance, atomic speed, shortest
     duration of the whole process
  B3 heat ledger: cut energy -> temperature rise -> atomic diffusion -> blurring
     scale vs legible scale
  B4 order ledger: placement order constrained by transport time; "one long film
     strip" is vetoed by the speed of light

Labels: CHECK recomputable / ESTIMATE depends on literature values / ARGUMENT structural reasoning
"""

import io
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "common"))

import unfold_appearance_v1 as ua          # reuse the phantom; that module's main has a __name__ guard

HBARC = 197.3269804
M_KG = 70.0
RHO = 1000.0
V = M_KG / RHO
N = 7.0e27
H_BODY = 1.75
D = (V / N) ** (1.0 / 3.0)                 # atomic spacing
A = N * D * D                              # unfolded area
A_C = V / H_BODY                           # mean cross-sectional area
TILE = math.sqrt(A_C)
N_SLICE = A / A_C
NT = int(round(math.sqrt(N_SLICE)))
C_LIGHT = 2.99792458e8
K_B = 1.380649e-23
EV_J = 1.602176634e-19

OUT = []


def w(s=""):
    OUT.append(s)


def tag(kind, name, ok, msg=""):
    OUT.append("  [%-8s] %-40s %-6s %s" % (kind, name, "PASS" if ok else "FLAG", msg))
    return ok


# ======================================================================
# A. How many fragments are there after the cut
# ======================================================================
def frag_count():
    from scipy import ndimage
    w("[A] After the cut: 8.1 billion sheets, or more fragments?")
    w("  Criterion: take a cross-section at each layer and count 4-connected components. Both legs/arms split a layer into several pieces.")
    w("")
    nz = 700
    zs = np.linspace(0.012, 1.738, nz)
    ncomp = np.zeros(nz)
    areas_raw = []
    perim = np.zeros(nz)
    for i, z in enumerate(zs):
        c = ua.slice_at(z, 200, 0.55)
        m = c > 0
        lab, k = ndimage.label(m)
        ncomp[i] = k
        px = (0.55 / 200.0) ** 2
        for j in range(1, k + 1):
            a = float((lab == j).sum()) * px
            if a > 1e-6:
                areas_raw.append((z, a))
        # perimeter: number of boundary pixels x pixel edge length
        er = m & ~np.roll(m, 1, 0)
        d2 = m & ~np.roll(m, 1, 1)
        perim[i] = float((er | d2).sum()) * (0.55 / 200.0)

    n_mean = float(np.trapezoid(ncomp, zs) / (zs[-1] - zs[0]))
    prof = np.zeros(nz)
    for z, a in areas_raw:
        prof[int(np.argmin(np.abs(zs - z)))] += a
    vol = float(np.trapezoid(prof, zs))
    N_FRAG = n_mean * N_SLICE
    areas = np.array([a for _, a in areas_raw])

    w("  region          z range       connected components    area per piece (m^2)")
    for lo, hi, lab in [(0.012, 0.80, "calf→thigh"), (0.80, 0.96, "pelvis"),
                        (0.96, 1.17, "abdomen"), (1.17, 1.38, "thorax"),
                        (1.38, 1.47, "shoulder"), (1.47, 1.56, "neck"),
                        (1.56, 1.738, "head")]:
        mk = (zs >= lo) & (zs < hi)
        ncm = float(ncomp[mk].mean())
        aa = np.array([a for z, a in areas_raw if lo <= z < hi])
        w("  %-14s %.3f-%.3f     %.2f          %.4f - %.4f"
          % (lab, lo, hi, ncm, aa.min() if aa.size else 0, aa.max() if aa.size else 0))
    w("")
    w("  mean connected components = %.3f  ->  total fragments = %.3f x %.3e = %.2e pieces" % (n_mean, n_mean, N_SLICE, N_FRAG))
    w("  fragment area: min %.2e m^2, max %.4f m^2, median %.4f m^2"
      % (areas.min(), areas.max(), float(np.median(areas))))
    w("  Note: each piece is not a single atom but a whole plate 0.215 nm thick, with area from mm^2 to 5e-2 m^2.")
    w("")
    side = float(np.trapezoid(perim, zs))
    w("  phantom self-check: int A_c(z) dz = %.4f m^3 (nominal 0.070; phantom is %.0f%% slimmer, area slightly smaller by the same ratio)"
      % (vol, (1 - vol / V) * 100))
    w("  side area: int P(z) dz = %.2f m^2 (negligible vs the 325 km^2 frontal area)" % side)
    w("  => fragments are essentially thin plates, not 3D crumbs; the side area is only %.1e" % (side / A))
    tag("CHECK", "A_phantom_volume", abs(vol / V - 1) < 0.25,
        "int A_c dz = %.4f m^3 vs 0.0700" % vol)
    tag("CHECK", "A_fragment_count", 1.0 < n_mean < 2.0,
        "%.2e pieces (not 8.1e9 sheets; the excess comes from the double-leg segments)" % N_FRAG)
    return dict(N_FRAG=N_FRAG, n_mean=n_mean, areas=areas, side=side)


# ======================================================================
# B1. Microscopic sequence
# ======================================================================
def micro_sequence():
    w("")
    w("[B1] What matter undergoes in turn as the front sweeps through a layer")
    w("  Step 1 cut: all interlayer bonds to the layers above and below lose their domain in one dimensionality reduction.")
    w("             They are not pulled apart (stretching takes time); the z direction simply ceases to exist -- the bonds' domain vanishes.")
    w("             cut area = the layer's cross-sectional area, across the whole layer at once.")
    w("  Step 2 spread: the whole layer translates to its lattice site as a 2D rigid body.")
    w("             **In-layer (x,y) is the identity -> in-layer strain = 0; all displacement is borne between layers.**")
    w("  Step 3 land: enter the lattice site and join neighbors edge-to-edge only, with no in-plane bonding.")
    w("")
    w("  Key implication: the whole unfolding = %.2e SE(2) rigid translations, none of them a deformation." % N_SLICE)
    w("  So 'smoothness' holds for the advance of the front (zero strain inside each layer),")
    w("  but fails everywhere between layers (all %.2e interfaces are severed)." % N_SLICE)
    tag("ARGUMENT", "B1_zero_strain_inside_layer", True,
        "in-layer strain 0; all displacement borne by interlayer interfaces")
    tag("ARGUMENT", "B1_front_is_delamination", True,
        "front = layer-by-layer delamination surface, neither a compression plane nor a tear surface")


# ======================================================================
# B2. Time and speed
# ======================================================================
def time_budget():
    w("")
    w("[B2] Time ledger: how fast the front moves, how fast the atoms must move")
    # Placement distance: lattice sites (0.2*i, 0.2*j), source near the body center
    m = 900
    ii, jj = np.meshgrid(np.arange(m), np.arange(m))
    r = TILE * np.sqrt(ii ** 2 + jj ** 2) * (NT / float(m))
    r_mean, r_max = float(r.mean()), float(r.max())
    w("  placement distance (origin at body center, square array %d x %d):" % (NT, NT))
    w("    mean %.2f km   max %.2f km (diagonal)" % (r_mean / 1e3, r_max / 1e3))
    w("")
    for T in (2.2, 10.0, 100.0, 1750.0):
        v = r_max / T
        KE = 0.5 * (M_KG / N) * v * v
        w("  total duration %8.1f s -> farthest atom speed %8.2f km/s, kinetic energy %6.2f eV/atom" %
          (T, v / 1e3, KE / EV_J))
    w("")
    w("  Criterion: transport kinetic energy < bond energy (~4 eV) to avoid scrambling the matter")
    v_lim = math.sqrt(2.0 * 4.0 * EV_J / (M_KG / N))
    T_min = r_max / v_lim
    w("    v_lim = %.2f km/s  ->  minimum total duration = r_max/v_lim = %.2f s" % (v_lim / 1e3, T_min))
    w("  That is: the 3D-to-2D conversion **cannot be completed in under a second**, otherwise atoms are flung into place rather than placed there.")
    tag("CHECK", "B2_min_duration", 1.0 < T_min < 10.0,
        "T >= %.1f s (set by transport kinetic energy < 4 eV)" % T_min)
    return dict(r_max=r_max, r_mean=r_mean, T_min=T_min)


# ======================================================================
# B3. Heat ledger
# ======================================================================
def heat_budget():
    w("")
    w("[B3] Heat ledger: cutting releases heat -- will the image burn itself away?")
    w("  cut energy per unit area = 2*gamma_eff; total cut area = %.3e m^2" % A)
    w("")
    w("  gamma_eff (J/m^2)    total heat (J)    dT (K)    diffusion length (legible at mm scale?)")
    w("  " + "-" * 74)
    CP = 4200.0
    for gam in (0.07, 0.3, 1.0):
        E = 2.0 * gam * A
        dT = E / (M_KG * CP)
        # 2D film melting point: Lindemann, k_spring=20 N/m, u=0.1 d
        T_melt = 20.0 * (0.1 * D) ** 2 / K_B
        # diffusion: liquid D ~ 1e-9 * exp(-Ea/kT), crudely taken as 1e-9*(T/1000)
        Dcoef = 1e-9 * max(dT, 300.0) / 1000.0
        # radiative cooling time
        T_abs = 300.0 + dT
        sig = 5.670374e-8
        t_cool = E / (sig * T_abs ** 4 * 2.0 * A)
        L = math.sqrt(2.0 * Dcoef * t_cool)
        w("  %-20.2f %-13.2e %-13.0f %.0e m  %s"
          % (gam, E, dT, L, "legible" if L < 1e-3 else "blurred"))
    w("")
    w("  How to read this:")
    w("    · Soft-tissue cutting gamma ~ 0.07 J/m^2 -> 4.5e7 J released, 150 K rise; the film is warm.")
    w("    · If the cut passes through many covalent bonds (gamma -> 1) -> 2000 K rise; the film melts.")
    w("    · In both cases atomic diffusion **before cooling completes** (10-30 us) is on the 10-100 nm scale.")
    w("  Conclusion: atomic-scale detail is lost over 10-100 nm, but the image's legible scale is 1 mm -- **a gap of 4-5 orders of magnitude**.")
    w("        So: the picture is blurred at the atomic level but clear at the anatomical level.")
    tag("ESTIMATE", "B3_heat_keeps_picture", True,
        "diffusion 1e-8 m << legible scale 1e-3 m")
    tag("ESTIMATE", "B3_sheet_is_hot", True,
        "the freshly cut film carries 10^2-10^3 K residual heat and must cool before it sets")


# ======================================================================
# B4. Order ledger
# ======================================================================
def order_budget(tb):
    w("")
    w("[B4] Order ledger: placement order is not entirely free")
    w("  If the picture must be fully placed when the front finishes sweeping, the farthest site must be filled first -- 'far first, near last'.")
    w("  If one insists on placing in head-to-toe order, the last batch of sheets has sites %.1f km away, requiring a transport tail:"
      % (tb["r_max"] / 1e3))
    tail = tb["r_max"] / math.sqrt(2.0 * 4.0 * EV_J / (M_KG / N))
    w("    tail ~ %.1f s (at the speed corresponding to the 4 eV limit)" % tail)
    w("  Both are possible; only 'front finished sweeping' and 'picture formed' are two distinct moments.")
    w("")
    w("  Counterexample (why it cannot be laid out as one long film strip):")
    for wid in (0.20, 0.49, 1.0):
        length = A / wid
        v = length / tb["T_min"]
        w("    strip width %.2f m -> strip length %.2e km; at minimum duration %.1f s it needs %.2f c  %s"
          % (wid, length / 1e3, tb["T_min"], v / C_LIGHT,
             "vetoed" if v > C_LIGHT else "feasible"))
    w("  That is: a 'film' layout 0.2 m wide cannot pass the speed-of-light gate; the strip width must be > %.2f m."
      % (A / (C_LIGHT * tb["T_min"])))
    tag("CHECK", "B4_strip_layout_forbidden", A / 0.2 / tb["T_min"] > C_LIGHT,
        "0.2 m width requires %.1f c" % (A / 0.2 / tb["T_min"] / C_LIGHT))
    tag("ARGUMENT", "B4_order_needs_tail", True,
        "order is free, but one pays a transport tail (~%.0f s)" % tail)


# ======================================================================
def conclusion(fg, tb):
    w("")
    w("=" * 80)
    w("[Conclusion] The complete process as the front sweeps through")
    w("=" * 80)
    w("  1. Morphology: a planar delamination front advancing along the body-height direction, peeling off one atomic layer (0.215 nm) at a time.")
    w("  2. Three steps per layer: cut (dimensionality reduction removes the domain of interlayer bonds) -> spread (whole-layer rigid translation) -> land (edge-to-edge joining).")
    w("     In-layer strain is always 0; all %.1e interfaces are severed, fracture area %.0f km^2." % (N_SLICE, A / 1e6))
    w("  3. Fragments: not 8.1e9 whole sheets but %.1e pieces (the double-leg segments split each layer in two), area 6e-3~5e-2 m^2."
      % fg["N_FRAG"])
    w("  4. Time: minimum %.1f s (any faster and the atoms are flung apart) -> front speed ceiling %.2f m/s;"
      % (tb["T_min"], H_BODY / tb["T_min"]))
    w("     if relaxed to the minute scale, the front is a slow sweep of order %.0f mm/s." % (H_BODY / 1750.0 * 1e3))
    w("  5. Heat: cutting releases heat, bringing the film to 300-2000 K; atoms diffuse 10-100 nm before cooling;")
    w("     atomic-level detail is lost while the 1 mm-scale anatomical image remains intact -- 'blurred at the atomic level, clear at the anatomical level'.")
    w("  6. Order: free, but either 'far first, near last' or with a transport tail; the long-film-strip layout is vetoed by the speed of light.")
    w("")
    w("  In one sentence: this is not 'compressing a person into a picture' but 'peeling the person layer by layer, flattening each layer, and filing them in order'.")
    w("  The front is more like a layer-peeler plus a placement machine, with a microsecond-scale heat flash in between.")


def main():
    w("=" * 80)
    w("[front_sweep v1] What the unfolding process looks like as the 2D-reduction front sweeps through the human body")
    w("=" * 80)
    w("")
    w("  geometric ledger: d=%.4f nm  A=%.1f km^2  A_c=%.4f m^2  N_slice=%.3e  NT=%d"
      % (D * 1e9, A / 1e6, A_C, N_SLICE, NT))
    w("")
    fg = frag_count()
    micro_sequence()
    tb = time_budget()
    heat_budget()
    order_budget(tb)
    conclusion(fg, tb)

    txt = "\n".join(OUT)
    print(txt)
    os.makedirs(os.path.join("runs", "ANALYSIS"), exist_ok=True)
    p = os.path.join("runs", "ANALYSIS", "front_sweep_v1.txt")
    io.open(p, "w", encoding="utf-8").write(txt + "\n")
    print("\n[out] %s" % p)


if __name__ == "__main__":
    main()
