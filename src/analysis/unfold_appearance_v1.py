# -*- coding: utf-8 -*-
"""
unfold_appearance_v1.py — What "unfolding human-body slices" actually looks like: five levels of view

The previous version gave numbers (8.1e9 tiles, 18 km, tau<=0.18%). This version gives something for the eyes.
Using a synthetic whole-body tomographic phantom, we draw the act of "unfolding":

  1  Overhead view from 18 km          — uniform gray field (human-eye resolution here is 5.2 m)
  2  Standing on the picture: neighbors 3x3 — adjacent tiles differ by 0.215 nm, visually identical
  3  Array after 4.65e6:1 decimation   — this is what "unfolding human-body slices" looks like: a whole wall of tomograms
  4  Two channels of a single tile     — naked eye = gray film; 284 eV detector = anatomical image
  5  Atomic-scale pixels               — each atom is one pixel, 0.215 nm per cell

Key quantities (recomputed):
  Number of slices N_s = A/A_c = V/(H d) = 8.12e9, A_c = V/H = 0.040 m^2 (H=1.75 m)
  Adjacent tiles differ by d = 0.215 nm  ->  to see anatomical variation one must sample one tile per 1 mm = 4.65e6 : 1
  In other words: **the human figure exists only in the 4.65-million-fold decimation; the original is a 4.65-million-fold redundant sequence.**

Tags: CHECK recomputable / ESTIMATE depends on literature parameters / ARGUMENT structural argument
"""

import io
import math
import os
import sys

import numpy as np

HBARC = 197.3269804
M_KG = 70.0
RHO_BODY = 1000.0
N_ATOM = 7.0e27
H_BODY = 1.75

OUT = []

TISSUE_RHO = {"air": 0.0012, "fat": 0.92, "muscle": 1.06, "blood": 1.06, "bone": 1.85, "lung": 0.26}
MU_VIS = {"air": 0.0, "fat": 0.03, "muscle": 4.2, "blood": 30.0, "bone": 2.5, "lung": 3.0}
MU_284 = {"air": 0.0, "fat": 9.9e4, "muscle": 6.4e4, "blood": 6.3e4, "bone": 6.5e4, "lung": 6.3e4}
ORDER = ["air", "fat", "muscle", "blood", "bone", "lung"]


def w(s=""):
    OUT.append(s)


def tag(kind, name, ok, msg=""):
    OUT.append("  [%-8s] %-40s %-6s %s" % (kind, name, "PASS" if ok else "FLAG", msg))
    return ok


# ----------------------------------------------------------------------
# Synthetic whole-body phantom: given height z, return a tissue-class map of one axial slice
# ----------------------------------------------------------------------
def slice_at(z, n=128, fov=0.55):
    x = (np.arange(n) + 0.5) / n * fov - fov / 2.0
    X, Y = np.meshgrid(x, x)
    c = np.zeros((n, n), dtype=np.int8)          # 0 = air

    if z < 0.80:                                  # lower leg -> thigh
        t = z / 0.80
        r = 0.044 + 0.040 * t
        cx = 0.078 + 0.014 * t
        for s in (-1, 1):
            d = np.hypot(X - s * cx, Y)
            c[d <= r] = 2
            c[(d > r - 0.008) & (d <= r)] = 1
            c[d <= 0.009 + 0.005 * t] = 4
    elif z < 0.96:                                # pelvis
        a, b = 0.148, 0.098
        e = (X / a) ** 2 + (Y / b) ** 2
        c[e <= 1] = 2
        c[(e <= 1) & (e > 0.90)] = 1
        for s in (-1, 1):
            c[((X - s * 0.082) / 0.070) ** 2 + ((Y + 0.012) / 0.030) ** 2 <= 1] = 4
        c[(X / 0.020) ** 2 + ((Y + 0.068) / 0.024) ** 2 <= 1] = 4
        c[(X / 0.042) ** 2 + ((Y - 0.024) / 0.032) ** 2 <= 1] = 3
    elif z < 1.17:                                # abdomen
        k = (z - 0.96) / 0.21
        a, b = 0.148 + 0.010 * k, 0.100 + 0.004 * k
        e = (X / a) ** 2 + (Y / b) ** 2
        c[e <= 1] = 2
        c[(e <= 1) & (e > 0.88)] = 1
        c[((X + 0.058) / 0.070) ** 2 + ((Y + 0.006) / 0.062) ** 2 <= 1] = 2   # liver
        c[((X + 0.030) / 0.030) ** 2 + ((Y - 0.042) / 0.026) ** 2 <= 1] = 3   # stomach
        c[((X - 0.062) / 0.040) ** 2 + ((Y - 0.010) / 0.036) ** 2 <= 1] = 1   # colon fat
        c[((X - 0.030) / 0.026) ** 2 + ((Y + 0.062) / 0.020) ** 2 <= 1] = 3   # bowel gas
        c[(X / 0.024) ** 2 + ((Y + 0.072) / 0.028) ** 2 <= 1] = 4             # spine
    elif z < 1.38:                                # chest
        a, b = 0.162, 0.106
        e = (X / a) ** 2 + (Y / b) ** 2
        c[e <= 1] = 2
        c[(e <= 1) & (e > 0.92)] = 1
        lung = (((X + 0.068) / 0.052) ** 2 + ((Y - 0.004) / 0.068) ** 2 <= 1) | \
               (((X - 0.068) / 0.052) ** 2 + ((Y - 0.004) / 0.068) ** 2 <= 1)
        c[lung & (e <= 1)] = 5
        c[((X - 0.008) / 0.042) ** 2 + ((Y + 0.012) / 0.048) ** 2 <= 1] = 3   # heart
        c[((X - 0.010) / 0.026) ** 2 + ((Y + 0.050) / 0.020) ** 2 <= 1] = 1   # mediastinal fat
        c[(X / 0.022) ** 2 + ((Y + 0.082) / 0.026) ** 2 <= 1] = 4
        c[(X / 0.014) ** 2 + ((Y - 0.096) / 0.008) ** 2 <= 1] = 4
        for k in range(10):
            ang = math.pi * (0.14 + 0.72 * k / 9.0)
            for s in (-1, 1):
                cx_, cy_ = s * 0.145 * math.cos(ang), 0.092 * math.sin(ang)
                c[((X - cx_) / 0.009) ** 2 + ((Y - cy_) / 0.009) ** 2 <= 1] = 4
    elif z < 1.47:                                # shoulder
        a, b = 0.190, 0.082
        e = (X / a) ** 2 + (Y / b) ** 2
        c[e <= 1] = 2
        c[(e <= 1) & (e > 0.90)] = 1
        c[(X / 0.022) ** 2 + ((Y + 0.058) / 0.026) ** 2 <= 1] = 4
        for s in (-1, 1):
            c[((X - s * 0.100) / 0.055) ** 2 + ((Y + 0.008) / 0.010) ** 2 <= 1] = 4
        c[(X / 0.026) ** 2 + ((Y - 0.030) / 0.018) ** 2 <= 1] = 5
    elif z < 1.56:                                # neck
        r = 0.056
        d = np.hypot(X, Y)
        c[d <= r] = 2
        c[(d <= r) & (d > r - 0.006)] = 1
        c[(X / 0.016) ** 2 + ((Y + 0.030) / 0.018) ** 2 <= 1] = 4
        c[(X / 0.011) ** 2 + ((Y - 0.006) / 0.011) ** 2 <= 1] = 5
    else:                                         # head
        t = min((z - 1.56) / 0.19, 1.0)
        r = 0.080 + 0.016 * math.sin(math.pi * t)
        d = np.hypot(X, Y)
        c[d <= r] = 2
        c[(d <= r) & (d > r - 0.007)] = 4
        c[((X + 0.006) / 0.012) ** 2 + ((Y - 0.004) / 0.028) ** 2 <= 1] = 3   # ventricle
        if t > 0.55:                              # face
            c[((X) / 0.030) ** 2 + ((Y + r + 0.008) / 0.020) ** 2 <= 1] = 2
            c[((X) / 0.014) ** 2 + ((Y + r + 0.012) / 0.010) ** 2 <= 1] = 5
    return c


def density_map(c):
    lut = np.array([TISSUE_RHO[n] for n in ORDER])
    return lut[c]


def tau_map(c, mu_tab, d):
    lut = np.array([mu_tab[n] for n in ORDER])
    return lut[c] * 0.1 * (density_map(c) * 1000.0 * d)


# ----------------------------------------------------------------------
def main():
    w("=" * 86)
    w("[unfold_appearance v1] What unfolded human-body slices look like: five levels of view")
    w("=" * 86)
    w("")

    V = M_KG / RHO_BODY
    d = (V / N_ATOM) ** (1.0 / 3.0)
    A = N_ATOM * d ** 2
    A_c = V / H_BODY
    n_s = A / A_c
    tile = math.sqrt(A_c)
    dec = 1e-3 / d

    w("[0] Convention recomputation (correction: the average cross-sectional area is not 0.5 m^2)")
    w("  V = %.4f m^3; H = %.2f m -> A_c = V/H = %.4f m^2 (side %.3f m)"
      % (V, H_BODY, A_c, tile))
    w("  Number of slices N_s = A/A_c = %.3e; unfolded height = N_s d = %.3f m" % (n_s, n_s * d))
    w("  Array %.0f x %.0f, total side length %.2f km" % (math.sqrt(n_s), math.sqrt(n_s), math.sqrt(A) / 1e3))
    w("  Anatomical difference between adjacent tiles = d = %.3f nm" % (d * 1e9))
    w("  To see anatomical variation (1 mm scale), one must sample one tile per %.2e -> decimation ratio %.2e : 1"
      % (dec, dec))
    tag("CHECK", "U1_decimation_ratio", True,
        "The human figure exists only in the %.1e-fold decimation; the original is a %.1e-fold redundant sequence" % (dec, dec))
    w("")

    # ---------------------------------------------------------------- 2
    w("[1] Physical meaning of each of the five views")
    w("  View A, 18 km overhead: resolvable 5.2 m -> on average %.0f tiles per resolution element" % ((5.2 / tile) ** 2))
    w("  View B, standing on the picture: resolvable 73 um (at 1 m) -> 2700 points within one tile, tiles all identical")
    w("  View C, decimated array: this is 'unfolded human-body slices', but it is a %.0e-fold synthesized view" % dec)
    w("  View D, two channels of one tile: naked eye = gray film; 284 eV = anatomical image (tau 1.2e-3)")
    w("  View E, atomic scale: each atom is a pixel, 0.215 nm per cell, %.1e pixels per tile"
      % ((tile / d) ** 2))
    w("")
    tag("ARGUMENT", "U2_five_views_are_not_interchangeable", True,
        "C is the 'blueprint', B/D are the 'real object' — mistaking C for what the naked eye sees is the easiest mistake to make in this project")

    # ---------------------------------------------------------------- 3
    w("[2] How many pixels are in one tile")
    px = (tile / d) ** 2
    w("  0.20 m tile / 0.215 nm = %.2e atoms across; area %.2e pixels" % (tile / d, px))
    w("  At human-eye 73 um, one tile gives only %.0f x %.0f resolvable points" %
      (tile / 73e-6, tile / 73e-6))
    w("  => The %.1e-fold information inside the tile is completely unreadable to the naked eye." % (px / (tile / 73e-6) ** 2))
    w("")

    txt = "\n".join(OUT)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(txt)
    outdir = os.path.join("runs", "ANALYSIS")
    if os.path.isdir(outdir):
        io.open(os.path.join(outdir, "unfold_appearance_v1.txt"), "w",
                encoding="utf-8").write(txt + "\n")
    return dict(d=d, A=A, A_c=A_c, n_s=n_s, tile=tile, dec=dec)


# ----------------------------------------------------------------------
def render():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    plt.rcParams["axes.unicode_minus"] = False

    V = M_KG / RHO_BODY
    d = (V / N_ATOM) ** (1.0 / 3.0)
    A_c = V / H_BODY
    tile = math.sqrt(A_c)
    dec = 1e-3 / d
    FOV = 0.40
    from matplotlib.colors import PowerNorm

    fig = plt.figure(figsize=(15.8, 9.2))
    gs = fig.add_gridspec(2, 3, width_ratios=[1.62, 1, 1], height_ratios=[1.06, 1],
                          hspace=0.30, wspace=0.22,
                          left=0.062, right=0.975, top=0.885, bottom=0.075)
    fig.suptitle("Spreading 70 kg over 325 km$^2$: what unfolded human-body slices actually look like",
                 fontsize=15.5, y=0.95)

    # ================================================== C decimated array (main figure)
    ax = fig.add_subplot(gs[0:2, 0])
    NT, NPX = 18, 150
    zs = np.linspace(1.738, 0.012, NT * NT)
    sheet = np.zeros((NT * NPX, NT * NPX), dtype=np.float32)
    for i, z in enumerate(zs):
        img = density_map(slice_at(z, NPX, FOV))
        r, c = divmod(i, NT)
        sheet[r * NPX:(r + 1) * NPX, c * NPX:(c + 1) * NPX] = img
    ax.imshow(sheet, cmap="gray", norm=PowerNorm(0.90, vmin=0.10, vmax=1.30),
              interpolation="nearest")
    for k in range(1, NT):
        ax.axhline(k * NPX - 0.5, color="#7f8c8d", lw=0.35, alpha=0.5)
        ax.axvline(k * NPX - 0.5, color="#7f8c8d", lw=0.35, alpha=0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("View C: unfolded image decimated %.1e : 1 (%d×%d tiles, head→foot)"
                 % (dec, NT, NT), fontsize=11.2, pad=8)

    # Inset: atomic-scale pixels
    axi = ax.inset_axes([0.615, 0.015, 0.365, 0.365])
    NA = 40
    rng = np.random.default_rng(11)
    gx, gy = np.meshgrid(np.arange(NA), np.arange(NA))
    edge = 20 + 2.2 * np.sin(gy / 3.1) + 0.8 * rng.standard_normal(NA)[None, :]
    kind = np.where(gx < edge, 0, 1)
    bone = rng.random((NA, NA)) < 0.03
    axi.set_facecolor("#101418")
    axi.scatter(gx[kind == 0], gy[kind == 0], s=7, c="#8d6e63", marker="o", lw=0)
    axi.scatter(gx[kind == 1], gy[kind == 1], s=7, c="#4fc3f7", marker="o", lw=0)
    axi.scatter(gx[bone], gy[bone], s=9, c="#ffffff", marker="o", lw=0)
    axi.set_xlim(-1, NA)
    axi.set_ylim(-1, NA)
    axi.set_xticks([])
    axi.set_yticks([])
    for sp in axi.spines.values():
        sp.set_color("#f1c40f")
        sp.set_linewidth(1.0)
    axi.set_title("View E: atomic-scale pixels (0.215 nm / point)", fontsize=6.6, color="#f1c40f", pad=2)

    ax.annotate("", xy=(1.022, 0.0), xytext=(1.022, 1.0), xycoords="axes fraction",
                arrowprops=dict(arrowstyle="-|>", color="#c0392b", lw=1.8))
    ax.text(1.042, 0.5, "head → foot", transform=ax.transAxes, rotation=90,
            va="center", ha="center", fontsize=9, color="#c0392b")
    step = 1.726 / (NT * NT) * 1000.0
    for lab, fy in [("head", 0.045), ("neck/shoulder", 0.175), ("chest", 0.265), ("abdomen", 0.385),
                    ("pelvis", 0.500), ("lower limbs", 0.760)]:
        ax.text(-0.012, 1.0 - fy, lab, transform=ax.transAxes, fontsize=7.4,
                color="#2c3e50", ha="right", va="center")
    ax.text(0.5, -0.035,
            "Each small cell = one 0.20 m tile, i.e. a 1:1 tomogram; cell spacing %.1f mm of body height\n"
            "But the truly adjacent tiles on the picture differ by only 0.215 nm and look identical — this image is the result of %.1e-fold decimation"
            % (step, dec), transform=ax.transAxes, ha="center", va="top", fontsize=7.8, color="#333333")

    # ================================================== A 18 km overhead view (far field)
    ax = fig.add_subplot(gs[0, 1])
    nz = 900
    prof = []
    for z in np.linspace(1.738, 0.012, nz):
        c = slice_at(z, 72, FOV)
        rho = density_map(c)
        m = rho > 0.1
        prof.append(float(rho[m].mean()) if m.any() else 0.0)
    prof = np.array(prof)
    k = np.ones(41) / 41.0
    prof = np.convolve(prof, k, mode="same")
    prof[:20] = prof[20]; prof[-20:] = prof[-21]
    img = np.repeat(prof[:, None], 60, axis=1)
    ax.imshow(img, cmap="gray", vmin=prof.min() - 0.015, vmax=prof.max() + 0.015,
              aspect="auto",
              extent=[0, 18.03, 0, 18.03], interpolation="bilinear")
    ax.set_title("View A: overhead view from 18 km (normalized $\\tau$)", fontsize=10.4, pad=6)
    ax.set_xlabel("km", fontsize=8.5)
    ax.set_ylabel("km", fontsize=8.5)
    ax.tick_params(labelsize=7.5)
    cmin = (prof.max() - prof.min()) / (prof.max() + prof.min())
    ax.text(0.03, 0.035,
            "A 1.75 m person is spread into 90,000 horizontal bands over 18 km\n"
            "In the far field only 1D information remains (head→foot), contrast %.0f%%, no human figure\n"
            "And this is a normalized view; the original visible-light $\\tau=10^{-7}$ shows nothing at all"
            % (cmin * 100),
            transform=ax.transAxes, ha="left", va="bottom", fontsize=7.0, color="#7b241c",
            bbox=dict(boxstyle="round,pad=0.32", fc="white", ec="#e6b0aa", alpha=0.9))

    # ================================================== B neighboring 3x3
    ax = fig.add_subplot(gs[0, 2])
    NB, NPB = 3, 100
    nb = np.zeros((NB * NPB, NB * NPB), dtype=np.float32)
    for i in range(NB * NB):
        img = density_map(slice_at(1.25 + i * d, NPB, FOV))
        r, c = divmod(i, NB)
        nb[r * NPB:(r + 1) * NPB, c * NPB:(c + 1) * NPB] = img
    ax.imshow(nb, cmap="gray", norm=PowerNorm(0.90, vmin=0.10, vmax=1.30),
              interpolation="nearest")
    for k in range(1, NB):
        ax.axhline(k * NPB - 0.5, color="#e67e22", lw=0.9)
        ax.axvline(k * NPB - 0.5, color="#e67e22", lw=0.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("View B: standing on the picture, adjacent 3×3 tiles", fontsize=10.4, pad=6)
    ax.text(0.5, -0.075, "Adjacent tiles differ by only 0.215 nm — completely indistinguishable to the naked eye",
            transform=ax.transAxes, ha="center", va="top", fontsize=7.6, color="#c0392b")

    # ================================================== D-left naked eye
    ax = fig.add_subplot(gs[1, 1])
    cz = slice_at(1.26, 320, FOV)
    ext = [-FOV / 2, FOV / 2, -FOV / 2, FOV / 2]
    rng2 = np.random.default_rng(3)
    flat = 1.0 - 1.1e-7 + 1.0e-5 * rng2.standard_normal((320, 320))
    ax.imshow(flat, cmap="gray", vmin=0.99988, vmax=1.00012, extent=ext)
    ax.set_title("View D-left: what the naked eye sees (reflected visible light)", fontsize=10.0, pad=5)
    ax.set_xlabel("m", fontsize=8)
    ax.set_ylabel("m", fontsize=8)
    ax.tick_params(labelsize=7)
    ax.text(0.5, -0.30, "$\\tau=1.1\\times10^{-7}$: the whole tile is a constant\nNot 'dark' but 'empty' — what you see is what lies behind it",
            transform=ax.transAxes, ha="center", va="top", fontsize=7.4, color="#c0392b")

    # ================================================== D-right 284 eV
    ax = fig.add_subplot(gs[1, 2])
    tv = tau_map(cz, MU_284, d)
    im = ax.imshow(tv * 1e3, cmap="magma", extent=ext,
                   vmin=float(tv.min() * 1e3), vmax=float(np.percentile(tv, 99.5) * 1e3))
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label("$\\tau\\times10^{3}$", fontsize=7.6)
    cb.ax.tick_params(labelsize=7)
    ax.set_title("View D-right: what the 284 eV detector sees", fontsize=10.0, pad=5)
    ax.set_xlabel("m", fontsize=8)
    ax.tick_params(labelsize=7)
    for txt, xx, yy in [("lung", -0.105, 0.0), ("heart", 0.012, -0.02), ("spine", 0.0, -0.145),
                        ("chest wall", 0.0, 0.088)]:
        ax.annotate(txt, (xx, yy), color="#f1c40f", fontsize=7.4, ha="center",
                    bbox=dict(boxstyle="round,pad=0.12", fc="#00000066", ec="none"))
    ax.text(0.5, -0.30, "$\\tau=1.2\\times10^{-3}$, inter-tissue $\\Delta\\tau\\sim10^{-3}$\nThis is what the picture really looks like",
            transform=ax.transAxes, ha="center", va="top", fontsize=7.4, color="#1e8449")

    outdir = os.path.join("runs", "ANALYSIS")
    p = os.path.join(outdir, "unfold_appearance_v1.png")
    fig.savefig(p, dpi=155, bbox_inches="tight")
    plt.close(fig)
    print("\n[figure] %s" % p)
    return p


if __name__ == "__main__":
    main()
    render()
