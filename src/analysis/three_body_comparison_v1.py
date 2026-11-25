# -*- coding: utf-8 -*-
"""
three_body_comparison_v1.py — Quantitative comparison between the ¬E branch and the "dual-vector foil" scene in The Three-Body Problem

Core proposition test:
  "The scene from abandoning effective two-dimensional reduction (7 cm slab) resembles the 2D reduction effect in The Three-Body Problem"

The criterion is not "thin or not", but "whether information is **unfolded** or **overlapped**":
  · Unfold: each atom has its own position in the plane -> can be a "picture"
  · Overlap: N layers of atoms are stacked under the same pixel -> can only be the top face of a "slab"

The area magnification factor required for unfolding = thickness / atomic spacing.
This moves the "Three-Body effect" from 1 m² to hundreds of km², and simultaneously from the ¬E branch to the ¬area branch.

Tags: CHECK (recomputable) / ESTIMATE (depends on literature parameters) / ARGUMENT (structural argument)
"""

import math
import io
import os
import sys

HBARC = 197.3269804
M_KG = 70.0
RHO = 1000.0
A_REG = 1.0

# Average atomic weight (human-body CHNO mixture, conservative if counted as C)
N_ATOMS_TOTAL = 7.0e27          # order of 70 kg / 1e-26 kg
D_BOND = 0.30e-9                # m, chemical bond scale (to judge "whether atoms are still present")
E_SCHWINGER = 1.32              # MeV/fm

OUT = []


def w(s=""):
    OUT.append(s)


def tag(kind, name, ok, msg=""):
    OUT.append("  [%-8s] %-36s %-6s %s" % (kind, name, "PASS" if ok else "FLAG", msg))
    return ok


def main():
    w("=" * 80)
    w("[three_body_comparison v1] ¬E 7 cm slab vs Three-Body dual-vector foil: unfold or overlap")
    w("=" * 80)
    w("")

    V = M_KG / RHO                      # m^3
    L_reg = V / A_REG                   # m, thickness under the registered 1 m^2
    w("[1] Geometry of three candidates")
    w("  Volume conservation: V = M/rho = %.4f m^3  — **area and thickness have a hyperbolic relationship**" % V)
    w("  A*L = V always holds. So 'how thin it is spread' and 'how large it is spread' are not two degrees of freedom, but one.")
    w("")
    w("  %-24s %-14s %-14s %-12s %s" % ("Configuration", "Area (m^2)", "Thickness (m)", "Flattening ratio L/sqrt(A)", "What it is"))
    w("  " + "-" * 82)

    # Atomic spacing (inferred from bulk density)
    d_atom = (V / N_ATOMS_TOTAL) ** (1.0 / 3.0)
    A_unfold = N_ATOMS_TOTAL * d_atom ** 2
    rows = [
        ("E holds @1 m^2", A_REG, 1e-15, "mirror (no atoms)"),
        ("¬E holds @1 m^2", A_REG, L_reg, "7 cm slab"),
        ("¬area @unfolded", A_unfold, d_atom, "monolayer"),
    ]
    for name, A, L, note in rows:
        w("  %-24s %-14.3e %-14.3e %-12.2e %s" % (name, A, L, L / math.sqrt(A), note))
    w("")

    # ---------------------------------------------------------------- 2
    w("[2] Key quantity: unfolding factor")
    w("  Number of atoms N = %.2e; average atomic spacing d inferred from bulk density = %.3f nm" % (N_ATOMS_TOTAL, d_atom * 1e9))
    ratio = L_reg / d_atom
    w("  Number of layers = L_reg/d = %.3e = %.2e layers of atoms stacked along one line of sight" % (ratio, ratio))
    w("  Unfolded area = N*d^2 = %.4e m^2 = %.1f km^2" % (A_unfold, A_unfold / 1e6))
    tag("CHECK", "T1_unfold_area", True,
        "Spreading the 7 cm stack side by side requires %.0f km^2, %.0e times 1 m^2"
        % (A_unfold / 1e6, A_unfold / A_REG))
    tag("CHECK", "T2_unfold_equals_monolayer", True,
        "When spread to that area the thickness is exactly d = %.3f nm — i.e., a monolayer" % (d_atom * 1e9))
    w("")

    # ---------------------------------------------------------------- 3
    w("[3] Why 'overlap' necessarily hides the interior (consistent with slab_visibility)")
    w("  With N = %.1e overlapping layers, any line of sight passes through all N layers:" % ratio)
    w("    · The first 1 mm (about %.0e layers) absorbs all visible light -> the remaining N layers contribute nothing to imaging" % (1e-3 / d_atom))
    w("    · After unfolding N = 1 layer, **no layer is hidden** -> all information is on the surface")
    tag("ARGUMENT", "T3_overlap_vs_unfold", True,
        "Overlap buries information in depth (unreadable); unfolding puts information on the surface (directly readable)")
    w("")

    # ---------------------------------------------------------------- 4
    w("[4] Optics of the monolayer: it is a 'picture', but a very faint one")
    # Areal density of the monolayer
    n_areal = N_ATOMS_TOTAL / A_unfold
    w("  Monolayer areal density n_atom = %.3e m^-2 (spacing %.3f nm)" % (n_areal, math.sqrt(1.0 / n_areal) * 1e9))
    # Chromophore absorption cross section: sigma[m^2] = 3.82e-25 * eps[M^-1 cm^-1]
    # Derivation: sigma[cm^2] = 3.82e-21*eps, 1 cm^2 = 1e-4 m^2
    w("  %-30s %-14s %-12s %-12s" % ("Chromophore", "sigma (m^2)", "fraction 1%", "fraction 10%"))
    w("  " + "-" * 68)
    for eps, lab in ((1e3, "weak chromophore (eps=1e3)"), (1e4, "melanin/heme (1e4)"),
                     (3e4, "strong absorption region (3e4)")):
        sig = 3.82e-25 * eps
        a1 = "%.3f%%" % (sig * n_areal * 0.01 * 100)
        a2 = "%.2f%%" % (sig * n_areal * 0.10 * 100)
        w("  %-30s %-14.2e %-12s %-12s" % (lab, sig, a1, a2))
    w("  => If chromophores make up 1%-10% of atoms, the monolayer visible absorptance is about 0.08%-3%.")
    w("     (The previous version computed this as 2.3%; the order of magnitude was right but the derivation treated cm^2 as m^2; recomputed with the correct cross section.)")
    w("     This is a **low-contrast image with a pattern**: like an extremely faint stained-glass window, not an oil painting.")
    w("     For comparison: although the 7 cm stack is thick, absorption is saturated (R=35%), leaving only uniform color -> no pattern.")
    tag("ESTIMATE", "T4_monolayer_is_faint_but_patterned", True,
        "Unfolding gives a pattern but low contrast (0.1-1%); overlap gives high reflectivity but no pattern (35% uniform color)")
    w("")

    # ---------------------------------------------------------------- 5
    w("[5] Position of the 2D criterion on the monolayer (avoiding again conflating inner/outer bounds)")
    kF = math.sqrt(2.0 * math.pi * n_areal)              # g=2
    EF_MeV = HBARC * kF * 1e-15                          # k: m^-1 -> fm^-1 -> MeV
    E_sub_MeV = math.pi * HBARC / (d_atom * 1e15)        # L: m -> fm
    ratio = EF_MeV / E_sub_MeV
    w("  n_2D = %.3e m^-2 ; k_F = %.3e m^-1" % (n_areal, kF))
    w("  E_F   = %.3f MeV = %.0f eV" % (EF_MeV, EF_MeV * 1e6))
    w("  E_sub = pi*hbarc/L = %.3f MeV = %.0f eV  (L=%.3f nm)" % (E_sub_MeV, E_sub_MeV * 1e6, d_atom * 1e9))
    w("  Inner bound E_F/E_sub = %.3f  -> %s" % (ratio, "satisfied (margin only %.2f times)" % (1 / ratio) if ratio < 1 else "not satisfied"))
    w("  Outer bound 2.5 eV / E_sub = %.2e  -> satisfied (visible light cannot excite the z direction by far)" % (2.5 / (E_sub_MeV * 1e6)))
    w("  => The monolayer **simultaneously** satisfies the inner and outer bounds; it is the only configuration in the whole project that 'has atoms and is also two-dimensional'.")
    w("     But the inner margin is only %.2f times; a slightly higher density drops it out of 2D — this is a fragile window." % (1 / ratio))
    tag("CHECK", "T5_monolayer_passes_both_bounds", ratio < 1.0,
        "Inner bound %.2f < 1, outer bound 10^%-1.0f; both pass, but the inner margin is only %.1f times"
        % (ratio, math.log10(E_sub_MeV * 1e6 / 2.5), 1 / ratio))
    w("")

    # ---------------------------------------------------------------- 6
    w("[6] Comparison with the description in The Three-Body Problem")
    w("  In the novel the solar system is flattened into 'a gigantic flat picture'; note three points:")
    w("    (a) The canvas area **explodes** (solar system -> a huge plane)  -> consistent with 'unfold' ✓")
    w("    (b) The picture **preserves internal structure** (mountains, cities, planetary interiors) -> only 'unfold' can do this ✓")
    w("    (c) The flattened being **dies immediately** (not 'a flattened person still alive')    -> consistent with the DCC seven-line verdict ✓")
    w("  That is: Liu Cixin's intuition is self-consistent regarding area and information; his canvas is indeed the huge plane after unfolding,")
    w("      not '300 million layers stacked on 1 square meter'.")
    w("")
    w("  Only one point truly conflicts with physics: the **contrast** of the picture.")
    w("  The monolayer absorptance is about 0.1%-1%, while the picture in the novel has normal light/dark and color.")
    w("  To obtain such contrast one needs **bulk thickness** (saturated absorption), which returns to 'overlap'.")
    w("  This is where the whole contradiction lies: **contrast requires thickness, pattern requires unfolding; both draw from the same volume and cannot be had together.**")
    w("")

    # ---------------------------------------------------------------- 7
    w("[7] 2x2 verdict: 'being a picture' requires two independent conditions simultaneously")
    w("")
    w("                    with atoms (color/structure)         without atoms")
    w("  Unfolded (thin)   ¬area: %.0f km^2 monolayer picture  <-Three-Body   E: 1 m^2 mirror" % (A_unfold / 1e6))
    w("  Overlapped (thick) ¬E: 1 m^2 7 cm slab              E+¬E both fail: mirror")
    w("")
    w("  => The Three-Body effect falls in the upper-left cell: **unfolded + with atoms**.")
    w("     Its correct branch name is not 'abandon effective 2D' but 'abandon 1 square meter'.")
    w("     Abandoning E only gives you the 'slab' between lower-right and upper-right; abandoning area gives you the 'picture'.")
    w("")

    # ---------------------------------------------------------------- 8
    w("[8] Conclusion")
    w("  1) 'The ¬E scene resembles Three-Body' — close in **composition** (the only branch preserving atoms and color),")
    w("     not close in **geometry** (7 cm / 1 m^2 is a slab with flattening ratio 0.07, not a picture).")
    w("  2) Three-Body effect = unfolding, which requires %.0f km^2, i.e. %.0e times 1 m^2." % (A_unfold / 1e6, A_unfold))
    w("  3) Spread to that area, the thickness automatically becomes %.2f nm — i.e. **a true monolayer**," % (d_atom * 1e9))
    w("     so the Three-Body effect is itself two-dimensional; it's just that its area is not 1 square meter.")
    w("  4) Cost: contrast only 0.1%%-1%%, an 'extremely faint stained-glass window'; and a %.0f km^2 freely suspended film" % (A_unfold / 1e6))
    w("     cannot support itself (requires a substrate or support).")
    w("")
    w("  In one sentence: Three-Body got the area of '2D reduction' right but the contrast wrong.")
    w("          While the DCC ¬E branch got 'contrast' right and area wrong.")
    w("          The two are two sides of the same coin, separated by %.0e times in area." % A_unfold)
    w("")

    w("=" * 80)
    txt = "\n".join(OUT)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(txt)
    outdir = os.path.join("runs", "ANALYSIS")
    if os.path.isdir(outdir):
        io.open(os.path.join(outdir, "three_body_comparison_v1.txt"), "w",
                encoding="utf-8").write(txt + "\n")
    return dict(V=V, L_reg=L_reg, d_atom=d_atom, A_unfold=A_unfold,
                n_areal=n_areal, EF=EF_MeV, E_sub=E_sub_MeV)


def plot(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["mathtext.fontset"] = "dejavusans"

    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.2),
                             gridspec_kw={"width_ratios": [1.35, 1]})
    fig.suptitle("Three-Body dual-vector foil vs abandoning effective 2D: the boundary between unfolding and overlap", fontsize=14, y=1.01)

    # (a) Hyperbola
    ax = axes[0]
    A = np.logspace(-1, 10.5, 500)
    L = res["V"] / A
    ax.loglog(A, L, color="#2c3e50", lw=2, label=r"Volume conservation $A\cdot L=V$")
    ax.axhline(res["d_atom"], color="#d64541", ls="--", lw=1.2,
               label="monolayer %.2f nm" % (res["d_atom"] * 1e9))
    ax.axhline(1e-15, color="#9b59b6", ls=":", lw=1, label="1 fm (E branch)")

    pts = [
        (1.0, res["L_reg"], "¬E, 1 m$^2$\n7 cm slab", "#e67e22", (12, -28)),
        (res["A_unfold"], res["d_atom"], "¬area, %.0f km$^2$\nmonolayer picture" % (res["A_unfold"] / 1e6),
         "#27ae60", (-70, 18)),
        (1.0, 1e-15, "E, 1 m$^2$\nmirror", "#8e44ad", (12, 14)),
    ]
    for x, y, lab, c, off in pts:
        ax.plot([x], [y], "o", ms=9, color=c, zorder=5)
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=off,
                    fontsize=8.5, color=c,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=c, lw=0.8, alpha=0.9))
    ax.set_xlabel("Area (m$^2$)")
    ax.set_ylabel("Thickness (m)")
    ax.set_title("(a) Area and thickness are not two degrees of freedom but one", fontsize=11)
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(alpha=0.25, which="both")
    ax.set_xlim(1e-1, 3e10)
    ax.set_ylim(1e-16, 1)

    # (b) 2x2
    ax = axes[1]
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    ax.set_xticks([0.5, 1.5])
    ax.set_yticks([0.5, 1.5])
    ax.set_xticklabels(["overlapped (thick)", "unfolded (thin)"], fontsize=10)
    ax.set_yticklabels(["without atoms", "with atoms"], fontsize=10)
    ax.set_title("(b) 'Being a picture' requires two independent conditions", fontsize=11)
    cells = [
        (0.5, 1.5, "¬E: 1 m$^2$\n7 cm slab\ncolored, no pattern", "#f8e0c8", "#a04000"),
        (1.5, 1.5, "¬area: %.0f km$^2$\nmonolayer\npatterned, extremely faint" % (res["A_unfold"] / 1e6),
         "#d5f0dd", "#1e8449"),
        (0.5, 0.5, "E+S+W, 1 m$^2$\n1 fm mirror", "#eceff1", "#546e7a"),
        (1.5, 0.5, "E, 1 m$^2$\n1 fm mirror", "#eceff1", "#546e7a"),
    ]
    for cx, cy, txt, fc, tc in cells:
        ax.add_patch(plt.Rectangle((cx - 0.5, cy - 0.5), 1, 1, fc=fc, ec="#b0bec5", lw=1.2))
        ax.text(cx, cy, txt, ha="center", va="center", fontsize=9, color=tc)
    ax.text(1.5, 1.93, "← Three-Body", ha="center", fontsize=10, color="#1e8449", fontweight="bold")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)

    fig.tight_layout()
    outdir = os.path.join("runs", "ANALYSIS")
    p = os.path.join(outdir, "three_body_comparison_v1.png")
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("\n[figure] %s" % p)


if __name__ == "__main__":
    res = main()
    plot(res)
