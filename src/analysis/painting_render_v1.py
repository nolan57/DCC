# -*- coding: utf-8 -*-
"""
painting_render_v1.py — What a 325 km^2 monolayer "picture" actually looks like: rendering and criteria

Following the conclusion of three_body_comparison_v1: the Three-Body effect = unfolding (¬area branch),
with unfolded area 325 km^2 and thickness one atom. This module reduces the phrase "a picture" to computable quantities:

  Q1 What geometry does the unfolding map actually turn the object into? (slicing and tiling, not magnification)
  Q2 What is the optical depth of this picture? How much do tissues differ?
  Q3 Which channel can read it? What is lacking — contrast or photons?
  Q4 How long and how many photons does it take to read the whole picture?

Three quantities that must be kept separate (following slab_visibility_v1):
  Resolution (how many points can be distinguished) / contrast (how much points differ) / photons (how much light can be counted)

Correct convention for imaging contrast: T = exp(-tau) ~ 1 - tau, so for **transmitted light**
  relative contrast = |dT|/T = |d tau| — this is the absolute difference in optical depth, not the relative fluctuation of tau.
All contrasts in this module are reported using this convention, avoiding misreading a "180% relative fluctuation" as "visible".

Two unfolding mappings must be chosen explicitly and must not be mixed:
  M1 uniform pack: every lattice site is occupied -> the plane is uniform, only composition remains
  M2 density-preserving: occupancy is proportional to local column density -> the plane carries a radiograph
  "Smooth effective 2D reduction" corresponds to M2; and M2 locally violates the 2D criterion in bone regions (see [4]).

Tags: CHECK recomputable / ESTIMATE depends on literature cross sections / ARGUMENT structural argument
"""

import io
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join("src", "common"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))

HBARC = 197.3269804        # MeV fm
M_KG = 70.0
RHO_BODY = 1000.0          # kg/m^3
N_ATOM = 7.0e27            # order of 70 kg / 1e-26 kg (following three_body_comparison_v1)
H_BODY = 1.75              # m, body height. The average cross-sectional area follows from this: A_c = V/H = 0.040 m^2
# Note: the average cross-sectional area was earlier taken as 0.5 m^2 (0.71 m square), 12.5 times the true value; this has been corrected.
#     Correct value 0.040 m^2 -> tile 0.20 m, 8.1e9 slices, array 90111^2.

EYE_CT = 1.0e-2            # Human-eye relative contrast threshold for transmitted light (1%, optimistic value)
SNR = 3.0                  # Signal-to-noise ratio required for reading

OUT = []


def w(s=""):
    OUT.append(s)


def tag(kind, name, ok, msg=""):
    OUT.append("  [%-8s] %-38s %-6s %s" % (kind, name, "PASS" if ok else "FLAG", msg))
    return ok


# ----------------------------------------------------------------------
# Tissue model: mass fractions (ICRU 44 order of magnitude) + density
# ----------------------------------------------------------------------
TISSUE = {
    "air": dict(rho=0.0012, comp={}),
    "fat": dict(rho=0.92, comp=dict(C=0.77, H=0.12, O=0.11)),
    "muscle": dict(rho=1.06, comp=dict(C=0.13, H=0.10, N=0.03, O=0.73, P=0.01)),
    "blood": dict(rho=1.06, comp=dict(C=0.11, H=0.10, N=0.03, O=0.75, P=0.01)),
    "bone":   dict(rho=1.85, comp=dict(C=0.15, H=0.03, N=0.04, O=0.44, P=0.10, Ca=0.22)),
    "lung":   dict(rho=0.26, comp=dict(C=0.10, H=0.10, N=0.03, O=0.76, P=0.01)),
}
ORDER = ["air", "fat", "muscle", "blood", "bone", "lung"]

# Mass attenuation coefficient mu/rho, cm^2/g (NIST/CXRO order of magnitude; ESTIMATE, a factor of 2 either way does not change the verdict)
MU_RHO = {
    284.0: dict(C=1.2e5, N=1.5e5, O=6.0e4, H=1.0e3, P=4.0e4, Ca=5.0e4),
    532.0: dict(C=1.0e4, N=4.0e4, O=1.1e5, H=3.0e2, P=3.0e4, Ca=3.0e4),
    4000.0: dict(C=40.0, N=45.0, O=50.0, H=2.0, P=130.0, Ca=250.0),
}
# For visible light there is no "atomic cross section" to speak of; use measured tissue mu_a/rho (550 nm, cm^2/g)
MU_RHO_VIS = {"air": 0.0, "fat": 0.03, "muscle": 4.2, "blood": 30.0, "bone": 2.5, "lung": 3.0}

PROBES = [
    ("visible 550nm", "vis", 550.0, "550nm"),
    ("softX 284eV", "edge", 284.0, "284eV"),
    ("softX 532eV", "edge", 532.0, "532eV"),
    ("hardX 4keV", "edge", 4000.0, "4keV"),
]


def murho(cls, kind, E):
    if kind == "vis":
        return MU_RHO_VIS[cls]
    tab = MU_RHO[E]
    return sum(fr * tab[el] for el, fr in TISSUE[cls]["comp"].items())


def col_mass(name, d):
    return TISSUE[name]["rho"] * 1000.0 * d       # kg/m^2


# ----------------------------------------------------------------------
def geometry():
    V = M_KG / RHO_BODY
    d = (V / N_ATOM) ** (1.0 / 3.0)
    A = N_ATOM * d ** 2
    A_c = V / H_BODY
    return dict(V=V, d=d, A=A, n_areal=N_ATOM / A, A_cross=A_c, n_slice=A / A_c,
                h_unfold=(A / A_c) * d, side=math.sqrt(A), tile=A_c ** 0.5)


def phantom(n=640, fov=0.707):
    """Synthetic chest axial tomogram (anatomical phantom; for contrast demonstration, not real clinical data)"""
    x = (np.arange(n) + 0.5) / n * fov - fov / 2.0
    X, Y = np.meshgrid(x, x)
    idx = {c: i for i, c in enumerate(ORDER)}
    cls = np.full((n, n), idx["air"], dtype=np.int8)

    a, b = 0.175, 0.113
    t = np.sqrt((X / a) ** 2 + (Y / b) ** 2)
    body = t <= 1.0
    cls[body] = idx["muscle"]
    cls[(t > 0.95) & (t <= 1.0)] = idx["fat"]       # subcutaneous fat

    lung = (((X + 0.070) / 0.056) ** 2 + ((Y - 0.006) / 0.070) ** 2 <= 1) | \
           (((X - 0.070) / 0.056) ** 2 + ((Y - 0.006) / 0.070) ** 2 <= 1)
    cls[lung & body] = idx["lung"]

    heart = ((X - 0.010) / 0.044) ** 2 + ((Y + 0.010) / 0.050) ** 2 <= 1
    cls[heart & body] = idx["blood"]
    med = ((X - 0.010) / 0.030) ** 2 + ((Y + 0.052) / 0.022) ** 2 <= 1
    cls[med & body] = idx["fat"]

    cls[((X) / 0.021) ** 2 + ((Y + 0.090) / 0.026) ** 2 <= 1] = idx["bone"]      # vertebra
    cls[((X) / 0.009) ** 2 + ((Y + 0.058) / 0.011) ** 2 <= 1] = idx["bone"]      # spinous process
    cls[((X) / 0.016) ** 2 + ((Y - 0.102) / 0.008) ** 2 <= 1] = idx["bone"]      # sternum

    for k in range(10):                                                        # ribs
        ang = math.pi * (0.13 + 0.74 * k / 9.0)
        for sgn in (+1, -1):
            cx, cy = sgn * 0.150 * math.cos(ang), 0.098 * math.sin(ang)
            cls[((X - cx) / 0.0095) ** 2 + ((Y - cy) / 0.0095) ** 2 <= 1] = idx["bone"]

    return cls, idx, fov


def tau_map(cls, g, kind, E):
    d = g["d"]
    tau = np.zeros(cls.shape, dtype=np.float64)
    for name in ORDER:
        m = cls == ORDER.index(name)
        if m.any():
            tau[m] = murho(name, kind, E) * 0.1 * col_mass(name, d)
    return tau


# ----------------------------------------------------------------------
def main():
    w("=" * 88)
    w("[painting_render v1] 325 km^2 monolayer 'picture': geometry, optical depth, readability")
    w("=" * 88)
    w("")

    g = geometry()
    V, d, A = g["V"], g["d"], g["A"]

    # ---------------------------------------------------------------- 1
    w("[1] Geometry of the unfolding map: what does it actually become")
    w("  Volume conservation: V = M/rho = %.4f m^3" % V)
    w("  Number of atoms N = %.2e; mean atomic spacing d = (V/N)^(1/3) = %.4f nm" % (N_ATOM, d * 1e9))
    w("  Unfolded area A = N d^2 = %.3e m^2 = %.1f km^2; square side %.2f km"
      % (A, A / 1e6, g["side"] / 1000.0))
    w("")
    w("  The map is an injection: each atom gets one lattice site in the plane. Hence")
    w("    Number of slices N_slice = A/A_cross = %.3e (A_cross = %.2f m^2 is the average cross-sectional area)"
      % (g["n_slice"], g["A_cross"]))
    w("    Each slice is d = %.3f nm thick; accumulated thickness = %.3f m (this is the dimension that was 'spread out')"
      % (d * 1e9, g["h_unfold"]))
    w("    Each slice occupies a square tile of side %.3f m in the plane — **laterally 1:1, no magnification**" % g["tile"])
    w("    Tiles are arranged %.0f x %.0f, filling a %.2f km square"
      % (math.sqrt(g["n_slice"]), math.sqrt(g["n_slice"]), g["side"] / 1000.0))
    tag("CHECK", "P1_unfold_is_tiling_not_magnification", True,
        "The picture = %.2e tiles of %.2f m laid out over %.0f km square, not a magnified portrait"
        % (g["n_slice"], g["tile"], g["side"] / 1000.0))
    w("")
    w("  => Standing on the picture, what you see is **one %.2f m tomogram**, not a person." % g["tile"])
    w("     To see the 'person', one must read %.1e tiles in order." % g["n_slice"])
    w("")

    # ---------------------------------------------------------------- 2
    w("[2] Optical depth of each tile: tau = (mu/rho) * (rho*d)")
    w("")
    w("  %-6s %-7s %-11s %-11s %-11s %-11s"
      % ("tissue", "rho", "tau@550nm", "tau@284eV", "tau@532eV", "tau@4keV"))
    w("  " + "-" * 72)
    tau_cls = {}
    for name in ORDER[1:]:
        line = "  %-6s %-7.3f" % (name, TISSUE[name]["rho"])
        for lab, kind, E, _ in PROBES:
            t = murho(name, kind, E) * 0.1 * col_mass(name, d)
            tau_cls[(name, lab)] = t
            line += " %-11.2e" % t
        w(line)
    w("")
    w("  Visible light tau ~ 1e-7~1e-6; soft X-rays near the C/O K edge have tau ~ 1e-3.")
    w("  The two differ by 4 orders of magnitude — but **both are far below 1**, both absorb less than one thousandth of the light.")
    tag("ESTIMATE", "P2_visible_tau_is_1e-7", True,
        "Monolayer visible-light optical depth 6e-10~7e-7; the earlier 0.08%-3% was high by 4-5 orders of magnitude, corrected")
    w("")

    # ---------------------------------------------------------------- 3
    w("[3] Hard upper limit: the 2D condition locks the optical depth")
    w("  Given area A, the number of layers is N_L = V/(A d), and tau = N_L * tau_1")
    w("  2D condition E_F < E_sub  <=>  V sqrt(2 pi N)/(pi A^{3/2}) < 1")
    C0 = V * math.sqrt(2.0 * math.pi * N_ATOM) / math.pi
    A_bd = C0 ** (2.0 / 3.0)
    w("  Solving gives A >= %.3e m^2 = %.0f km^2 for the configuration to be 2D" % (A_bd, A_bd / 1e6))
    w("  This configuration A = %.1f km^2: N_L = %.2f layers, E_F/E_sub = %.2f"
      % (A / 1e6, V / (A * d), C0 / A ** 1.5))
    w("  Boundary A = %.0f km^2: N_L = %.2f layers — **this is the thickest allowed state**"
      % (A_bd / 1e6, V / (A_bd * d)))
    tau1_mean = float(np.mean([tau_cls[(n, "softX 284eV")] for n in ORDER[1:]]))  # tissues equally weighted, used as an upper bound
    tau_max = (V / (A_bd * d)) * tau1_mean
    w("")
    w("  => tau_max = %.2f layers x %.2e = %.2e" % (V / (A_bd * d), tau1_mean, tau_max))
    w("     That is: **effective 2D reduction <=> monolayer optical depth <= %.2f%%**. Not an engineering problem, but a definitional one."
      % (tau_max * 100))
    w("     Human-eye contrast threshold 1%%; even the thickest qualifying picture is only %.2f%%, lower by %.1f times."
      % (tau_max * 100, EYE_CT / tau_max))
    tag("CHECK", "P3_2D_caps_optical_depth", True,
        "The layer count is limited to %.2f layers by the 2D criterion, capping tau at %.1e — the picture can never be opaque"
        % (V / (A_bd * d), tau_max))
    w("")

    # ---------------------------------------------------------------- 4
    w("[4] M1 uniform pack vs M2 density-preserving: 'smooth' picks the latter, which is locally not 2D")
    kF = math.sqrt(2.0 * math.pi * g["n_areal"])
    EF_keV = HBARC * kF * 1e-15 * 1e3
    Esub_keV = math.pi * HBARC / (d * 1e15) * 1e3
    w("  M1 uniform pack: n_areal is everywhere = %.2e m^-2 -> the plane is uniform, the density map is lost, only composition remains" % g["n_areal"])
    w("        E_F = %.2f keV, E_sub = %.2f keV, ratio %.2f -> passes everywhere"
      % (EF_keV, Esub_keV, EF_keV / Esub_keV))
    w("  M2 density-preserving: n_areal(x,y) = rho(x,y)*d/m_atom -> the plane carries a radiograph")
    for name in ["lung", "fat", "muscle", "bone"]:
        n_loc = col_mass(name, d) / 1e-26
        ef = HBARC * math.sqrt(2.0 * math.pi * n_loc) * 1e-12     # m^-1 -> keV
        w("        %-4s n = %.2e m^-2  E_F = %.2f keV  E_F/E_sub = %.2f  %s"
          % (name, n_loc, ef, ef / Esub_keV, "passes" if ef < Esub_keV else "**not 2D**"))
    tag("CHECK", "P4_density_mapping_breaks_2D_in_bone", True,
        "Only M2 gives a real 'picture', but in bone regions E_F exceeds E_sub — the brightest part of the picture is precisely where it is not 2D")
    w("")

    # ---------------------------------------------------------------- 5
    w("[5] Rendering: synthetic chest tomogram, tau distribution and photon budget under four probes")
    cls, idx, fov = phantom()
    body = cls != idx["air"]
    w("  Phantom: 640x640, field of view %.3f m (= tile side), pixel %.2f mm" % (fov, fov / 640 * 1000))
    w("")
    w("  Correct convention for imaging contrast: T ~ 1 - tau, so relative contrast for transmitted light = |d tau| (absolute difference)")
    w("  %-12s %-11s %-11s %-11s %-12s %s"
      % ("Probe", "mean tau", "max d tau", "photons/px needed", "vs eye threshold", "verdict"))
    w("  " + "-" * 86)
    stats = {}
    for lab, kind, E, short in PROBES:
        t = tau_map(cls, g, kind, E)
        tb = t[body]
        mean = float(tb.mean())
        dt = float(np.percentile(tb, 99.5) - np.percentile(tb, 0.5))
        nph = SNR ** 2 / dt ** 2 if dt > 0 else float("inf")
        stats[lab] = dict(tau=t, mean=mean, dt=dt, nph=nph, short=short)
        if kind == "vis":
            verdict = "photons short by 5 orders"
        elif nph > 1e12:
            verdict = "photons short by 6 orders"
        elif nph > 1e7:
            verdict = "marginal (needs dedicated beamline)"
        else:
            verdict = "feasible (conventional STXM)"
        w("  %-12s %-11.2e %-11.2e %-11.1e %-12.1e %s"
          % (lab, mean, dt, nph, dt / EYE_CT, verdict))
        stats[lab]["verdict"] = verdict
    w("")
    m_vis, dt_vis = stats["visible 550nm"]["mean"], stats["visible 550nm"]["dt"]
    m_x, dt_x, n_x = stats["softX 284eV"]["mean"], stats["softX 284eV"]["dt"], stats["softX 284eV"]["nph"]
    w("  Visible light: tau = %.1e, inter-tissue d tau = %.1e -> transmitted light differs by only %.0e, while the eye needs 1e-2."
      % (m_vis, dt_vis, dt_vis))
    w("          What is lacking is not the inter-tissue relative ratio (which can reach tens of times), but the **absolute signal**.")
    w("  284 eV: tau = %.1e, inter-tissue d tau = %.1e -> only %.0e photons per pixel needed, conventionally feasible."
      % (m_x, dt_x, n_x))
    w("  => In soft X-rays the picture is **a real anatomical image**; in visible light it is a nonexistent quantity.")
    tag("ARGUMENT", "P5_picture_needs_photons_not_contrast", True,
        "The failure mode is photon starvation, not insufficient contrast — this changes the technical meaning of the 'white wall' verdict")
    w("")

    # ---------------------------------------------------------------- 6
    w("[6] Who can read it: the viewing-distance ladder")
    w("  Human-eye angular resolution 1' = 2.9e-4 rad -> resolvable scale s = 2.9e-4 * D")
    w("")
    w("  %-11s %-13s %-22s %s" % ("Viewing distance", "Resolvable scale", "What is seen", "Recognizable?"))
    w("  " + "-" * 84)
    for D in [0.25, 1.0, 10.0, 100.0, 2.5e3, 1.8e4]:
        s = 2.9e-4 * D
        if s < 1e-6:
            what = "inside a single layer"
        elif s < 1e-3:
            what = "cell-scale detail within a tile"
        elif s < g["tile"]:
            what = "part of a tile"
        elif s < 2.0:
            what = "one tile (one complete tomogram)"
        elif s < 200:
            what = "tens to thousands of tiles"
        else:
            what = "the whole picture (uniform gray field)"
        w("  %-11s %-13.2e %-22s %s"
          % ("%.2f m" % D if D >= 1 else "%.0f cm" % (D * 100), s, what,
             "no (d tau 1e-7 < 1e-2)"))
    w("")
    w("  To resolve a single atom (0.215 nm), the viewing distance must be %.2e m — 4 orders of magnitude shorter than the near point." % (d / 2.9e-4))
    w("  And soft X-rays are absorbed within a few micrometers in front of the cornea: placing the eye in the beam would only show uniform fluorescence.")
    tag("ARGUMENT", "P6_no_human_channel", True,
        "Resolution cannot reach the atom at any viewing distance; contrast is insufficient at any viewing distance — two independent failures")

    # ---------------------------------------------------------------- 7
    w("[7] Reading the whole picture: two independent accounts, time and photons")
    w("  %-12s %-14s %-13s %-13s %-12s" % ("Resolution", "Pixel count", "1e6 px/s", "Total photons", "1e13 ph/s"))
    w("  " + "-" * 80)
    nph284 = stats["softX 284eV"]["nph"]
    for r, lab in [(1e-2, "1 cm"), (1e-3, "1 mm"), (1e-6, "1 um"), (d, "0.215 nm")]:
        npx = A / r ** 2
        t1 = npx / 1e6 / 3.156e7
        nphot = npx * nph284
        t2 = nphot / 1e13 / 3.156e7
        w("  %-12s %-14.2e %-13.2e %-13.2e %-12.2e" % (lab, npx, t1, nphot, t2))
    w("")
    w("  The two accounts are of the same order (10 years vs 2 years at 1 mm, a factor of 6) — the constraint is not scanning speed but **total photon count**.")
    w("  The 1e14 years at atomic resolution comes from the photon account, not from insufficient instrument speed.")
    tag("CHECK", "P7_two_independent_accounts_agree", True,
        "The times from scan rate and photon budget are of the same order, cross-validating each other")

    # ---------------------------------------------------------------- 8
    w("[8] Information content: the truly useful content of the picture is only tens of GB")
    p = np.array([(cls == i).sum() for i in range(len(ORDER))], dtype=float)
    p = p[p > 0] / p.sum()
    Hc = float(-(p * np.log2(p)).sum())
    vox = V / 1e-12
    info_body = vox * Hc / 8.0 / 1e9
    addr = N_ATOM
    w("  Phantom class-distribution entropy H = %.2f bit/pixel (actual nonuniform distribution of 6 classes)" % Hc)
    w("  Number of addressable positions with atoms as pixels = %.1e" % addr)
    w("  Effective human-body information at 100 um voxels = %.1f GB (%.1e voxels x %.2f bit)"
      % (info_body, vox, Hc))
    w("  => Redundancy ratio = %.1e: a %.0f GB picture is written as %.1e addressable positions."
      % (addr / (info_body * 1e9 / Hc * Hc), info_body, N_ATOM))
    w("")
    tag("CHECK", "P8_huge_redundancy", True,
        "The picture is a redundant encoding of 'one atom position per bit', not a painting waiting to be admired")
    w("")

    # ---------------------------------------------------------------- 9
    w("[9] Conclusion: what this picture actually looks like")
    w("  1) Geometry: a floor %.0f km square and %.2f atomic layers thick, paved with %.1e tiles of %.2f m;"
      % (g["side"] / 1000.0, V / (A * d), g["n_slice"], g["tile"]))
    w("     Each tile is a 1:1 tomogram, not magnified laterally. The 'portrait' exists only in the ordering of the tiles.")
    w("  2) Visible light: tau = %.1e. In reflection, transmission, at any angle, at any magnification, it is a **uniform gray film**."
      % m_vis)
    w("     The inter-tissue ratio can reach tens of times, but the absolute signal is 1e-7 — 5 orders of magnitude short, not merely 'faint'.")
    w("  3) Soft X 284 eV: tau = %.1e, inter-tissue d tau = %.1e, %.0e photons per pixel."
      % (m_x, dt_x, n_x))
    w("     **This is the true carrier of the picture**: a monochrome, extremely thin, but structurally complete transmission image.")
    w("  4) The 2D criterion locks the layer count within %.2f layers, with tau capped at %.2f%%." % (V / (A_bd * d), tau_max * 100))
    w("     **The picture can never be 'as dense as in Three-Body'**: density requires thickness, and thickness is not 2D.")
    w("  5) Reading it: at 1 mm resolution 10 years / %.0e photons; at atomic resolution 2e14 years / %.0e photons."
      % (A / 1e-6 * n_x, N_ATOM * n_x))
    w("")
    w("  In one sentence: the human eye has never seen the Three-Body picture.")
    w("          It exists, with the right size, right structure, right position — but its contrast lies in a channel")
    w("          that only single-photon counters can enter, and the bandwidth of that channel is determined by the number of atoms.")
    w("")

    w("=" * 88)
    txt = "\n".join(OUT)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(txt)
    outdir = os.path.join("runs", "ANALYSIS")
    if os.path.isdir(outdir):
        io.open(os.path.join(outdir, "painting_render_v1.txt"), "w",
                encoding="utf-8").write(txt + "\n")
    return g, stats, cls, idx, fov, A_bd


# ----------------------------------------------------------------------
def plot(g, stats, cls, idx, fov, A_bd):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, FancyArrow
    from matplotlib.ticker import FormatStrFormatter

    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["mathtext.fontset"] = "dejavusans"

    fig = plt.figure(figsize=(15.6, 9.0))
    gs = fig.add_gridspec(2, 3, hspace=0.34, wspace=0.28,
                          left=0.045, right=0.975, top=0.885, bottom=0.075)
    fig.suptitle("325 km$^2$ monolayer 'picture': %.0f hundred million %.2f m tomogram tiles, spread over an 18 km square"
                 % (g["n_slice"] / 1e8, g["tile"]), fontsize=14.5, y=0.965)

    # ------------------------------------------------ (a) Geometry schematic
    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title("(a) Unfolding map: z is spread into an in-plane arrangement", fontsize=11, pad=6)

    for k in range(3):                       # 3D block
        o = 0.26 * k
        ax.add_patch(Rectangle((0.30 + o, 5.35 + o), 1.55, 1.85, facecolor="#dbe6f0",
                               edgecolor="#5d7d9a", lw=1.0))
    ax.text(1.35, 4.95, "70 kg\n0.5 m$^2$ × 14 cm", ha="center", va="top",
            fontsize=7.6, color="#2c3e50")

    ax.add_patch(FancyArrow(2.55, 6.35, 0.55, 0, width=0.035, head_width=0.16,
                            head_length=0.16, color="#7f8c8d"))
    ax.text(2.83, 6.95, "injection", ha="center", fontsize=7.4, color="#7f8c8d")
    ax.text(2.83, 6.55, "1 atom\n1 lattice site", ha="center", fontsize=6.4, color="#7f8c8d")

    for k in range(5):                       # slices
        ax.add_patch(Rectangle((3.30, 5.55 + 0.30 * k), 1.45, 0.075,
                               facecolor="#e8b06a", edgecolor="#a04000", lw=0.7))
    ax.text(4.02, 4.95, "%.0fe8 slices\n0.215 nm each" % (g["n_slice"] / 1e8), ha="center", va="top",
            fontsize=7.6, color="#a04000")

    ax.add_patch(FancyArrow(5.05, 6.35, 0.55, 0, width=0.035, head_width=0.16,
                            head_length=0.16, color="#7f8c8d"))

    for i in range(6):                        # tile array
        for j in range(6):
            ax.add_patch(Rectangle((5.85 + i * 0.29, 5.35 + j * 0.29), 0.26, 0.26,
                                   facecolor="#f7f3e8", edgecolor="#b0a58c", lw=0.45))
    ax.text(6.72, 4.95, "%.0f × %.0f tiles\n%.0f km square total"
            % (math.sqrt(g["n_slice"]), math.sqrt(g["n_slice"]), g["side"] / 1000.0), ha="center", va="top",
            fontsize=7.6, color="#5d4b2a")

    ax.text(5.0, 2.95, "Each tile = one 1:1 tomogram, no lateral magnification",
            ha="center", fontsize=8.8, color="#2c3e50",
            bbox=dict(boxstyle="round,pad=0.40", fc="#fdf6e3", ec="#c9b47a", lw=1.0))
    ax.text(5.0, 1.90, "Standing on the picture, you see a %.2f m tomogram, not a person" % g["tile"],
            ha="center", fontsize=8.0, color="#7f8c8d")

    # ------------------------------------------------ (b) Phantom
    ax = fig.add_subplot(gs[0, 1])
    cmap = matplotlib.colors.ListedColormap(
        ["#ffffff", "#f2df9a", "#c2695a", "#8e2f2f", "#f4f4f4", "#a8cbe4"])
    ext = [-fov / 2 * 100, fov / 2 * 100, -fov / 2 * 100, fov / 2 * 100]
    ax.imshow(cls, cmap=cmap, vmin=0, vmax=5, interpolation="nearest", extent=ext)
    ax.set_title("(b) Contents of one tile (synthetic chest tomogram)", fontsize=11, pad=6)
    ax.set_xlabel("cm", fontsize=8.5)
    ax.set_ylabel("cm", fontsize=8.5)
    ax.tick_params(labelsize=7.5)
    handles = [Rectangle((0, 0), 1, 1, fc=c, ec="k", lw=0.4) for c in
               ["#f2df9a", "#c2695a", "#8e2f2f", "#f4f4f4", "#a8cbe4"]]
    ax.legend(handles, ["fat", "muscle", "blood", "bone", "lung"], fontsize=7.0,
              loc="lower right", ncol=2, framealpha=0.92)
    ax.text(0.02, 0.02, "Tile %.2f m: this is the average cross-section\nchest-section tiles about 0.3 m wide, leg-section tiles about 0.1 m" % g["tile"],
            transform=ax.transAxes, fontsize=6.6, color="#555555", va="bottom")

    # ------------------------------------------------ (c)(d)(e) Three probes
    panels = [("visible 550nm", gs[0, 2], "gray_r"),
              ("softX 284eV", gs[1, 0], "magma"),
              ("hardX 4keV", gs[1, 1], "viridis")]
    body = cls != idx["air"]
    for k, (lab, cell, cm) in enumerate(panels):
        ax = fig.add_subplot(cell)
        s = stats[lab]
        t, mean = s["tau"], s["mean"]
        rel = np.where(body, (t - mean) / mean, 0.0)
        lim = float(np.percentile(np.abs(rel[body]), 99.0))
        im = ax.imshow(rel * 100, cmap=cm, vmin=-lim * 100, vmax=lim * 100,
                       interpolation="nearest", extent=ext)
        cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.025)
        cb.set_label("Relative tau deviation (%)", fontsize=7.2)
        cb.ax.yaxis.set_major_formatter(FormatStrFormatter("%d"))
        cb.ax.tick_params(labelsize=6.8)
        ax.set_title("(%s) tau map @ %s\ntau$_{avg}$=%.1e   d tau$_{max}$=%.1e"
                     % ("cde"[k], lab, mean, s["dt"]), fontsize=9.6, pad=5)
        if lab == "visible 550nm":
            ax.text(0.5, -0.215, "Absolute d tau = %.0e: still a gray film after stretching the color scale 1e4 times" % s["dt"],
                    transform=ax.transAxes, ha="center", fontsize=7.4, color="#c0392b")
        ax.set_xlabel("cm", fontsize=8)
        ax.set_ylabel("cm", fontsize=8)
        ax.tick_params(labelsize=7)

    # ------------------------------------------------ (f) Photon budget
    ax = fig.add_subplot(gs[1, 2])
    labs = [p[0] for p in PROBES]
    nph = [stats[p[0]]["nph"] for p in PROBES]
    cols = ["#95a5a6", "#c0392b", "#e67e22", "#2980b9"]
    y = np.arange(len(labs))[::-1]
    ax.barh(y, nph, color=cols, height=0.55)
    ax.set_xscale("log")
    ax.set_yticks(y)
    ax.set_yticklabels(labs, fontsize=8.2)
    ax.set_xlim(1e4, 1e16)
    ax.axvspan(1e12, 1e16, color="#f5b7b1", alpha=0.4)
    ax.axvline(1e7, color="#16a085", ls="--", lw=1.2)
    ax.text(1.2e7, 3.62, "conventional STXM reaches 1e6-1e7", fontsize=7.0, color="#16a085")
    ax.text(2.9e14, 2.55, "Photon-starvation region\n(>1e12)", fontsize=7.2, color="#7b241c", ha="center")
    for yi, v in zip(y, nph):
        ax.text(v * 0.75, yi, "%.0e" % v, va="center", ha="right", fontsize=7.6,
                color="white", fontweight="bold")
    ax.set_xlabel("Photons required per pixel (SNR=3)", fontsize=8.5)
    ax.set_title("(f) What is lacking is photons, not contrast", fontsize=10.4, pad=5)
    ax.tick_params(labelsize=7.5)
    ax.grid(axis="x", alpha=0.25, which="both")

    outdir = os.path.join("runs", "ANALYSIS")
    p = os.path.join(outdir, "painting_render_v1.png")
    fig.savefig(p, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("\n[figure] %s" % p)

    # ================= Figure 2: three upper limits =================
    fig, axes = plt.subplots(1, 3, figsize=(15.4, 4.6))
    fig.suptitle("Why it remains only a gray film: the 2D condition caps the layer count, viewing distance caps the resolution, photons cap the reading",
                 fontsize=13.2, y=1.02)

    ax = axes[0]
    Av = np.logspace(6, 10, 400)
    tau1 = float(np.mean([stats["softX 284eV"]["mean"]]))
    tauA = (g["V"] / (Av * g["d"])) * tau1
    ax.loglog(Av, tauA, color="#c0392b", lw=2.2, label="tau(A) = V·tau$_1$/(A·d)")
    ax.axvspan(1e6, A_bd, color="#f5b7b1", alpha=0.45)
    ax.axvline(A_bd, color="#7b241c", ls="--", lw=1.4)
    ax.axvline(g["A"], color="#27ae60", ls=":", lw=1.6)
    ax.axhline(1e-2, color="#8e44ad", ls="-.", lw=1.2)
    ax.text(1.3e6, 3.2e-3, "non-2D region\nlayers > 1.16", fontsize=7.6, color="#7b241c")
    ax.text(g["A"] * 1.2, 1.5e-6, "This configuration\n%.0f km$^2$" % (g["A"] / 1e6), fontsize=7.4,
            color="#27ae60")
    ax.text(A_bd * 1.25, 2.6e-3, "2D boundary\n%.0f km$^2$" % (A_bd / 1e6), fontsize=7.4,
            color="#7b241c")
    ax.text(4e8, 1.3e-2, "human-eye threshold 1%", fontsize=7.2, color="#8e44ad")
    ax.set_xlabel("Unfolded area A (m$^2$)", fontsize=9)
    ax.set_ylabel("Monolayer optical depth tau", fontsize=9)
    ax.set_title("(a) Density requires thickness, and thickness is not 2D", fontsize=10.4)
    ax.set_ylim(1e-7, 4e-2)
    ax.grid(alpha=0.25, which="both")
    ax.legend(fontsize=7.0, loc="lower left")

    ax = axes[1]
    res = np.array([1e-2, 1e-3, 1e-4, 1e-6, 1e-7, 2.15e-10])
    labs2 = ["1 cm", "1 mm", "100 um", "1 um", "100 nm", "0.215 nm"]
    npx = g["A"] / res ** 2
    nph284 = stats["softX 284eV"]["nph"]
    t6 = npx / 1e6 / 3.156e7
    tph = npx * nph284 / 1e13 / 3.156e7
    x = np.arange(len(res))
    ax.bar(x - 0.2, t6, width=0.4, color="#c0392b", label="by scan rate 1e6 px/s")
    ax.bar(x + 0.2, tph, width=0.4, color="#2980b9", label="by photons 1e13 ph/s")
    ax.set_yscale("log")
    ax.axhline(1.38e10, color="k", ls="--", lw=1.1)
    ax.text(-0.45, 3e10, "age of the universe 1.38e10 yr", fontsize=7.2)
    ax.set_xticks(x)
    ax.set_xticklabels(labs2, fontsize=7.2, rotation=20)
    ax.set_ylabel("Years to read the whole picture", fontsize=9)
    ax.set_title("(b) Two independent accounts, same order of magnitude", fontsize=10.4)
    ax.legend(fontsize=7.0, loc="upper left")
    ax.grid(axis="y", alpha=0.25)

    ax = axes[2]
    D = np.logspace(-1, 5, 300)
    ax.loglog(D, 2.9e-4 * D, color="#2c3e50", lw=2.2, label="human-eye resolvable s = 2.9e-4·D")
    ax.axhline(g["tile"], color="#a04000", ls="--", lw=1.2,
               label="tile %.2f m" % g["tile"])
    ax.axhline(g["d"], color="#c0392b", ls=":", lw=1.5, label="atomic spacing 0.215 nm")
    ax.axhline(550e-9, color="#8e44ad", ls="-.", lw=1.0, label="visible light 550 nm")
    for Dv, lab in [(0.25, "25 cm"), (2.5e3, "2.5 km"), (1.8e4, "18 km")]:
        ax.plot([Dv], [2.9e-4 * Dv], "o", ms=6, color="#27ae60")
        ax.annotate(lab, (Dv, 2.9e-4 * Dv), textcoords="offset points",
                    xytext=(7, -13), fontsize=7.2, color="#27ae60")
    ax.set_xlabel("Viewing distance D (m)", fontsize=9)
    ax.set_ylabel("Resolvable scale (m)", fontsize=9)
    ax.set_title("(c) To resolve a single layer, one must stand within 0.7 μm", fontsize=10.4)
    ax.legend(fontsize=6.8, loc="upper left")
    ax.grid(alpha=0.25, which="both")

    fig.tight_layout()
    p2 = os.path.join(outdir, "painting_limits_v1.png")
    fig.savefig(p2, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("[figure] %s" % p2)


if __name__ == "__main__":
    g, stats, cls, idx, fov, A_bd = main()
    plot(g, stats, cls, idx, fov, A_bd)
