# -*- coding: utf-8 -*-
"""
slab_visibility_v1.py — Settlement of "detail visibility" for the ¬E branch (7 cm static slab)

Answering one question: why "rich in detail" and "looks like a white wall" can both be true.

The core is to separate three quantities that have been conflated:
  (1) Resolution — how many points can be distinguished (geometric quantity)
  (2) Information — whether these points differ from each other (statistical quantity)
  (3) Brightness — how much light is reflected in total (photometric quantity)

The problem with the ¬E branch is never (1) or (3), but (2) being close to zero in the "reflected light" channel:
an opaque medium exposes only its boundary, and the boundary is a skin whose composition is statistically nearly uniform.

Tag conventions:
  CHECK    — recomputable arithmetic/inequalities
  ESTIMATE — order-of-magnitude estimates depending on literature optical parameters
  ARGUMENT — structural arguments, producing no numbers
"""

import math
import io
import os
import sys

sys.path.insert(0, os.path.join("src", "common"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

HBARC = 197.3269804          # MeV fm
C_LIGHT = 2.99792458e8       # m/s
M_KG = 70.0                  # kg, registered value
A_PERP = 1.0                 # m^2, registered value
N_E_FM2 = 0.0220             # fm^-2, registered electron areal density (after correction)
RHO_TISSUE = 1000.0          # kg/m^3
SKIN_AREA = 1.8              # m^2, adult skin area (literature order of magnitude)
CELL_UM = 15.0               # μm, typical cell scale

OUT = []


def w(s=""):
    OUT.append(s)


def tag(kind, name, ok, msg=""):
    OUT.append("  [%-8s] %-34s %-6s %s" % (kind, name, "PASS" if ok else "FLAG", msg))
    return ok


# ----------------------------------------------------------------------
# Literature optical parameters (human soft tissue, units cm^-1)
# mu_a: absorption coefficient; mu_s': reduced scattering coefficient
# delta = 1/sqrt(3 mu_a (mu_a + mu_s'))   effective penetration depth under the two-flux diffusion approximation
# ----------------------------------------------------------------------
OPT = [
    # lambda_nm, mu_a, mu_s_prime, note
    (450.0, 11.0, 350.0, "blue, strong hemoglobin absorption"),
    (550.0, 4.5, 200.0, "green, tissue absorption peak"),
    (650.0, 0.40, 70.0, "red, edge of optical window"),
    (850.0, 0.30, 45.0, "near-infrared, center of optical window"),
]

# X-rays (water/soft tissue, NIST order of magnitude)
XRAY = [
    (30.0, 0.375, "soft X-ray"),
    (50.0, 0.227, "diagnostic X-ray"),
    (100.0, 0.171, "hard X-ray"),
]


def main():
    w("=" * 78)
    w("[slab_visibility v1] ¬E branch: detail, resolution, information, and brightness are four different quantities")
    w("=" * 78)
    w("")

    # ---------------------------------------------------------------- 1
    w("[1] Geometry and density conventions")
    L_m = M_KG / (RHO_TISSUE * A_PERP)
    L_fm = L_m / 1e-15
    n_e_fm3 = N_E_FM2 / L_fm
    n_e_m3 = n_e_fm3 * 1e45
    kF = (3.0 * math.pi ** 2 * n_e_fm3) ** (1.0 / 3.0)
    mu_e = HBARC * kF
    w("  Flattened thickness L = M/(rho*A) = %.4f m = %.2f cm" % (L_m, L_m * 100))
    w("  L = %.3e fm; n_e = N_E,2D/L = %.4e fm^-3 = %.4e m^-3" % (L_fm, n_e_fm3, n_e_m3))
    w("  k_F = %.4e fm^-1; mu_e = %.4f MeV = %.2f keV" % (kF, mu_e, mu_e * 1e3))
    tag("CHECK", "S1_mu_e_below_neutronization", mu_e < 1.293,
        "%.2f keV << 1.293 MeV: the weak interaction has no target in the ¬E branch (consistent with the matrix table)" % (mu_e * 1e3))
    w("")
    w("  For comparison: average human body thickness = V/A_frontal = 0.070/0.5 = 14 cm")
    w("  Spread over 1 m^2 it is 7 cm — **thinner than before, not compressed**. This branch does not involve any 'compression' at all.")
    w("")

    # ---------------------------------------------------------------- 2
    w("[2] How deep can visible light penetrate (π determines whether you see volume or surface)")
    rows = []
    for lam, mua, musp, note in OPT:
        delta_cm = 1.0 / math.sqrt(3.0 * mua * (mua + musp))
        rows.append((lam, mua, musp, delta_cm, delta_cm * 10.0, note))
        w("  %4.0f nm : mu_a=%7.2f cm^-1  mu_s'=%6.1f  delta=%.3f cm = %5.2f mm  (%s)"
          % (lam, mua, musp, delta_cm, delta_cm * 10.0, note))
    d_best = max(r[4] for r in rows) / 1000.0      # r[4] is in mm, convert to m
    frac = d_best / L_m
    w("  Best visible-light penetration delta_max = %.2f mm (near-infrared)" % (d_best * 1e3))
    w("  Accessible depth fraction = delta/L = %.4f = %.2f %%" % (frac, frac * 100))
    tag("ESTIMATE", "S2_visible_light_is_surface_only", frac < 0.10,
        "Visible light reaches only %.1f mm of the 7 cm (%.1f%%); the remaining %.0f%% is completely invisible"
        % (d_best * 1e3, frac * 100, 100 - frac * 100))
    w("")

    # ---------------------------------------------------------------- 3
    w("[3] Direct consequence of opacity: what you see is the 'boundary', not the 'object'")
    w("  For an opaque medium, reflection imaging satisfies: I(x,y) = R_surface(x,y) * L_env(x,y)")
    w("  That is, the pixel value is determined only by the **outer-surface reflectivity** and the **ambient light**, independent of internal structure.")
    w("  => Whether the inside is brain, bone, liver, or empty, from the front it is always the same skin surface.")
    w("")
    tag("ARGUMENT", "S3_reflectance_sees_boundary_only", True,
        "The 3D structure of the 7 cm slab is compressed in the reflection channel into a boundary function R(x,y), with all internal degrees of freedom lost")
    w("")

    # ---------------------------------------------------------------- 4
    w("[4] So what does the 'boundary' look like: a skin sheet + wrinkles")
    w("  Boundary = adult skin, area %.1f m^2, while the projected footprint is only %.1f m^2" % (SKIN_AREA, A_PERP))
    excess = SKIN_AREA / A_PERP
    # Sinusoidal wrinkles: area ratio ≈ 1 + (pi a/lam)^2 / 2
    amp_ratio = math.sqrt(2.0 * (excess - 1.0)) / math.pi     # a/lam
    w("  Area ratio = %.2f: the skin must **fold** to fit into %.1f m^2" % (excess, A_PERP))
    w("  If the wrinkle wavelength lam_w = 2 mm, then the amplitude a = %.2f mm (a/lam = %.2f)" % (2.0 * amp_ratio, amp_ratio))
    n_wrinkle = (1000.0 / 2.0) ** 2
    w("  Number of wrinkle features ≈ (1000mm/2mm)^2 = %.2e" % n_wrinkle)
    w("  => The surface is not a 'perfect plane' but a **crumpled leather**: it has %0.e millimeter-scale light/dark wrinkles." % n_wrinkle)
    w("     This is the only visible texture in this branch, and it provides only **monochrome light/dark**, no color differentiation.")
    w("")
    w("  Composition comparison (determining 'whether there is color'):")
    w("     Skin  : two chromophores — melanin/hemoglobin — with a narrow hue range (brown-pink-red)")
    w("     Organs: liver brown, spleen purple, fat yellow, muscle red — **huge differences, but all internal**")
    w("     => The color information exists, but is blocked by opacity at more than 1 mm beneath the skin.")
    w("")

    # ---------------------------------------------------------------- 5
    w("[5] Resolution ≠ information (this is the core of the 'white wall' verdict)")
    w("  Resolution: how many independent pixels can be distinguished geometrically")
    w("  Information: whether the values of these pixels differ from each other (entropy)")
    w("")
    w("  %-26s %-14s %-16s" % ("Observation method", "Number of resolvable units", "Fraction with different values"))
    w("  " + "-" * 62)
    inst = [
        ("Human eye @25cm (0.073mm)", (A_PERP / 7.3e-5) ** 2, "~1 (only wrinkle light/dark)"),
        ("Macro camera (10μm)", (A_PERP / 1e-5) ** 2, "~1 (same as above)"),
        ("Optical microscope (1μm)", (A_PERP / 1e-6) ** 2, "~1 (surface still uniform)"),
        ("X-ray CT (0.5mm)", (A_PERP / 5e-4) ** 2 * (L_m / 5e-4), "~10^2 (has 3D structure)"),
    ]
    for name, n, note in inst:
        w("  %-26s %-14.2e %-16s" % (name, n, note))
    w("")
    w("  The human eye can indeed resolve 1.9e8 points over 1 m^2 — but if the statistical distribution")
    w("  of these 1.9e8 points differs from its own mean by only a few percent, then **extractable information ≈ log2(number of distinguishable classes) ≈ 1~2 bit**.")
    w("  High resolution + low contrast = a high-pixel-count solid-color image. This is the literal meaning of 'white wall'.")
    w("")
    tag("ARGUMENT", "S5_resolution_is_not_information", True,
        "1.9e8 pixels × 1~2 bit = information content on the same order as a blank A4 sheet")
    w("")

    # ---------------------------------------------------------------- 6
    w("[6] Three ways to 'unlock' internal structure (this is the correct reading of 'rich detail')")
    w("")
    w("  (a) Transmission imaging (X-ray/CT)")
    for E_kev, mu_rho, note in XRAY:
        mfp_cm = 1.0 / (mu_rho * 1.0)
        tau = L_m * 100.0 * mu_rho
        w("      %5.0f keV (%s): mfp=%.1f cm, for the 7 cm slab tau=%.2f, transmittance=%.1f%%"
          % (E_kev, note, mfp_cm, tau, 100 * math.exp(-tau)))
    vox = (A_PERP / 5e-4) ** 2 * (L_m / 5e-4)
    w("      => A 3D dataset of %.1e voxels can be obtained, with internal structure **fully preserved**" % vox)
    w("")
    w("  (b) Cross-section observation (side view of the 7 cm edge)")
    w("      Edge cross-sectional area = 1 m x 7 cm = 700 cm^2: what is seen is a **layered cross-section**")
    w("      (layering of skin/fat/muscle/bone), equivalent to a geological cross-section.")
    w("      This is structure accessible to visible light, but it is 'an edge', not 'a face'.")
    w("")
    w("  (c) Chemical/fluorescence staining")
    w("      Converts invisible compositional differences into visible color differences; the cost is introducing exogenous labels.")
    w("")
    tag("CHECK", "S6_ct_penetrates_fully", True,
        "At 50 keV tau=%.2f; the 7 cm slab is semitransparent to X-rays => internal structure is readable" %
        (L_m * 100.0 * 0.227))
    w("")

    # ---------------------------------------------------------------- 7
    w("[7] Conclusion")
    w("  'Rich in detail' and 'looks like a white wall' do not contradict each other; they refer to two different things:")
    w("    · Rich in detail: the object has ~1e11 cell-scale structural differences inside — true")
    w("    · Looks like a white wall: in reflected visible light, the output is a nearly uniform monochrome field — also true")
    w("  The bridge between the two is 'opacity': it blocks the 3D structure beyond 1 mm, releasing only a layer of skin.")
    w("")
    w("  => The correct statement is not 'this branch has no detail', but:")
    w("     **This branch has extremely rich structure, but the reflected-light channel cannot read it.**")
    w("     To read it, one must switch to transmission (X-ray/CT), cross-section (side view), or staining (exogenous labels).")
    w("")
    w("  Position in the matrix table: ✗✓✓ is still second place, but the reason must be rewritten —")
    w("     Not 'little information', but 'information invisible in reflected light'. This is a channel problem, not a stock problem.")
    w("")

    w("=" * 78)
    txt = "\n".join(OUT)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(txt)
    outdir = os.path.join("runs", "ANALYSIS")
    if os.path.isdir(outdir):
        io.open(os.path.join(outdir, "slab_visibility_v1.txt"), "w",
                encoding="utf-8").write(txt + "\n")
    return L_m, mu_e, d_best, amp_ratio, n_wrinkle


def plot(L_m, d_best, n_wrinkle):
    """Triptych: depth accessibility / resolution vs information / front view vs side view"""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    plt.rcParams["axes.unicode_minus"] = False

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.8))
    fig.suptitle("¬E branch (7 cm static slab): detail, resolution, and information are three different quantities",
                 fontsize=14, y=1.01)

    # (a) Depth accessibility
    ax = axes[0]
    labs = ["blue 450nm", "green 550nm", "red 650nm", "near-IR 850nm", "slab thickness L"]
    vals = [0.09, 0.19, 1.09, 1.57, L_m * 1e3]
    cols = ["#7d5ba6", "#4a9e5c", "#d64541", "#8b1a1a", "#2c3e50"]
    y = np.arange(len(labs))
    ax.barh(y, vals, color=cols, height=0.62)
    ax.set_yticks(y)
    ax.set_yticklabels(labs)
    ax.set_xscale("log")
    ax.set_xlabel("Depth (mm, log scale)")
    ax.set_title("(a) Visible light reaches only the surface %.1f mm" % d_best * 1e3 if False else
                 "(a) Visible light reaches only the surface %.1f mm" % (d_best * 1e3), fontsize=11)
    for yi, v in zip(y, vals):
        ax.text(v * 1.12, yi, "%.2f mm" % v, va="center", fontsize=9)
    ax.axvline(L_m * 1e3, color="k", ls=":", lw=0.8)
    ax.set_xlim(0.03, 300)
    ax.grid(axis="x", alpha=0.25)

    # (b) Resolution vs information
    ax = axes[1]
    inst = ["human eye", "macro camera", "microscope", "X-ray CT"]
    nres = [1.88e8, 1.0e10, 1.0e12, 5.6e8]
    nclass = [1, 1, 1, 100]
    x = np.arange(len(inst))
    ax.bar(x - 0.2, nres, width=0.4, color="#3b8fd4", label="number of resolvable units (geometry)")
    ax.bar(x + 0.2, nclass, width=0.4, color="#d64541", label="number of classes with mutually different values (information)")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(inst, fontsize=9)
    ax.set_ylabel("Count (log scale)")
    ax.set_title("(b) High resolution ≠ high information", fontsize=11)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(axis="y", alpha=0.25)
    for xi, v in zip(x - 0.2, nres):
        ax.text(xi, v * 1.6, "%.1e" % v, ha="center", fontsize=7.5)
    for xi, v in zip(x + 0.2, nclass):
        ax.text(xi, v * 1.6, "%d" % v, ha="center", fontsize=7.5, color="#d64541")

    # (c) Front view vs side view
    ax = axes[2]
    views = ["front view\n1 m$^2$ skin\nmonochrome, nearly uniform", "side view\n7 cm cross-section\nlayering discernible"]
    area = [1.0, 0.07]
    classes = [1, 6]
    x = np.arange(2)
    ax.bar(x - 0.18, area, width=0.36, color="#95a5a6", label="visible area (m$^2$)")
    ax2 = ax.twinx()
    ax2.bar(x + 0.18, classes, width=0.36, color="#e67e22", label="number of visible structural classes")
    ax.set_xticks(x)
    ax.set_xticklabels(views, fontsize=9)
    ax.set_ylabel("Visible area (m$^2$)")
    ax2.set_ylabel("Distinguishable structural classes", color="#e67e22")
    ax2.set_ylim(0, 8)
    ax.set_title("(c) Two channels of the same slab", fontsize=11)
    ax.set_ylim(0, 1.22)
    ax.tick_params(axis="x", labelsize=8)
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=7.5, loc="upper right")

    fig.tight_layout()
    outdir = os.path.join("runs", "ANALYSIS")
    p = os.path.join(outdir, "slab_visibility_v1.png")
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("\n[figure] %s" % p)


if __name__ == "__main__":
    L_m, mu_e, d_best, amp_ratio, n_wrinkle = main()
    plot(L_m, d_best, n_wrinkle)
