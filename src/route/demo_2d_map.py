#!/usr/bin/env python
"""
DEMO-1 -- the declared demonstration object, mapped to the deposit plane by an exact Hilbert traversal.

Specification: docs/specs/demo_object_v1.md      (declares the geometry and sigma)
Predictions:   runs/FRONT/demo_obj_registration.md (P1-P14, fixed before this file existed)

What this file does NOT do:
  * it does not touch the body's census.  H = 1.74 m, 1.18e10 plates, array 90126^2 are untouched.
  * it does not close GD11 for the body.  sigma is declared HERE, for DEMO-1, and nowhere else.
  * it makes no readability claim (MR1.0) and no claim that the deposit is 2D (Annex B sB.3).
  * it is a presentation product: GEOMETRY PRESCRIBED (D2), FL1, false colour (EN2).

The map cannot be drawn 1:1: 4.295e9 sites against 512^2 = 262144 display pixels is a factor 16384, and a 4K
frame still shows 0.19% of the deposit.  The decimation is the reason sigma had to be chosen by measurement
rather than by taste (spec s4.1).

PROVENANCE: NEITHER  (declared geometry + a traversal; establishes no physics)
"""
import math
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_PNG = os.path.join(ROOT, 'runs', 'FRONT', 'demo_2d_map.png')
OUT_TXT = os.path.join(ROOT, 'runs', 'FRONT', 'demo_2d_map_results.txt')

# ---------------------------------------------------------------- registered constants
C_LIGHT = 2.99792458e8
DELTA = 0.215e-9          # m, atomic layer (front_sweep_v1)
PITCH = 0.4001            # m, registered lattice pitch (mid_sweep_frame_v1 s2)

# ---------------------------------------------------------------- declared (DEMO-1)
M_SHELL = 4
S_SIDE = 65536            # 2^16, so the Hilbert curve needs no padding
H_OBJ = 0.2300            # m
R1, R4 = 0.0200, 0.0900
R2_0, R2_A = 0.0450, 0.0060
R3_0, R3_A = 0.0700, 0.0080
RHO_A = (4.0e3, 1.2e3, 7.5e3, 2.0e3)   # kg/m^2, declared areal densities
ROLE = ('core, dense', 'shell, light', 'shell, heavy', 'jacket')
F_SWEEP = 0.5             # the front's position drawn in the figure

RES, FLAGS = [], {}


def out(s=""):
    print(s)
    RES.append(s)


def hdr(s):
    out()
    out("=" * 96)
    out(s)
    out("=" * 96)


def table(rows, cols):
    w = [len(str(c)) for c in cols]
    for r in rows:
        for i, c in enumerate(r):
            w[i] = max(w[i], len(str(c)))
    out("  " + "  ".join(str(c).ljust(w[i]) for i, c in enumerate(cols)))
    out("  " + "  ".join("-" * w[i] for i in range(len(cols))))
    for r in rows:
        out("  " + "  ".join(str(c).ljust(w[i]) for i, c in enumerate(r)))


def radii(z):
    """Outer radius of each shell at height z: returns (r1, r2, r3, r4)."""
    s = math.sin(2 * math.pi * z / H_OBJ)
    return R1, R2_0 - R2_A * s, R3_0 + R3_A * s, R4


def areas(z):
    """Cross-section area of each component at height z."""
    r1, r2, r3, r4 = radii(z)
    return np.array([math.pi * r1 ** 2,
                     math.pi * (r2 ** 2 - r1 ** 2),
                     math.pi * (r3 ** 2 - r2 ** 2),
                     math.pi * (r4 ** 2 - r3 ** 2)])


def d2xy(order, d):
    """Hilbert index -> (x, y) on a 2^order square (iterative standard form)."""
    n = 1 << order
    x = y = 0
    t = d
    s = 1
    while s < n:
        rx = 1 & (t >> 1)
        ry = 1 & (t ^ rx)
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        t >>= 2
        s <<= 1
    return x, y


# =================================================================================================
hdr("[A] CENSUS -- and the reason a new object could be declared at all")
# =================================================================================================
N_LAYER = int(math.floor(H_OBJ / DELTA))
PIECES = M_SHELL * N_LAYER
CELLS = S_SIDE ** 2
OCC = PIECES / CELLS
H_MAX = CELLS * DELTA / M_SHELL

out(f"  delta = {DELTA:.4e} m   H = {H_OBJ} m   M = {M_SHELL}   S = {S_SIDE} = 2^16")
out()
out(f"  N (layers)          = floor(H/delta) = {N_LAYER:,}")
out(f"  pieces = M*N        = {PIECES:,}")
out(f"  cells  = S^2        = {CELLS:,}")
out(f"  occupancy           = {OCC:.6f}   ->  {OCC:.4f} plates per cell")
FLAGS["P1"] = (PIECES == 4279069764 and CELLS == 4294967296 and abs(OCC - 0.99629) < 5e-6)
out(f"   => P1 (expected 4.279069764e9 / 4.294967296e9 / 0.99629): {'PASS' if FLAGS['P1'] else 'FAIL'}")
out()
out(f"  H_max = S^2*delta/M = {H_MAX:.6f} m     declared H = {H_OBJ} m  ->  {100*H_OBJ/H_MAX:.1f}% of cap")
FLAGS["P2"] = (abs(H_MAX - 0.230854) < 1e-6 and H_OBJ < H_MAX)
out(f"   => P2 (expected H_max = 0.230854, H below it): {'PASS' if FLAGS['P2'] else 'FAIL'}")
FLAGS["P3"] = OCC < 1.0
out(f"   => P3 (plates per cell < 1 so GD10 cannot arise): {'PASS' if FLAGS['P3'] else 'FAIL'}")
out()
out("  The body failed exactly here: 1.18e10 plates on 8.1227e9 cells = 1.4527 per cell (GD10). DEMO-1 is")
out("  declared so that pieces sit BELOW cells by construction; the 0.37% residue is vacuum, not a defect.")

# =================================================================================================
hdr("[B] ADMISSIBILITY OF THE PIECES")
# =================================================================================================
zs = np.linspace(0, H_OBJ, 20001)
A_of_z = np.array([areas(z) for z in zs])
A_max = A_of_z.max(axis=0)
A_min = A_of_z.min(axis=0)
SITE = PITCH ** 2

rows = []
for k in range(M_SHELL):
    rows.append([f"C{k+1}", ROLE[k], f"{RHO_A[k]:.1e}", f"{A_min[k]:.5e}", f"{A_max[k]:.5e}",
                 f"{A_max[k]/SITE:.4f}"])
table(rows, ["id", "role", "rho_A (kg/m^2)", "A_min (m^2)", "A_max (m^2)", "A_max / site"])

FLAGS["P4"] = (A_max.max() <= SITE) and (A_max.max() < 0.02)
out()
out(f"   largest piece A_3,max = {A_max[2]:.5e} m^2 on a {SITE:.4f} m^2 site = {100*A_max[2]/SITE:.1f}%"
    f"  ({SITE/A_max[2]:.2f}x clear)")
out(f"   => P4 (expected 1.4335e-2 vs 0.1601): {'PASS' if FLAGS['P4'] else 'FAIL'}")

extent = 2 * R4
FLAGS["P5"] = (extent <= PITCH)
out(f"   => P5 (expected 0.180 <= 0.4001): {'PASS' if FLAGS['P5'] else 'FAIL'}  ({extent:.3f} m vs {PITCH})")

gap = (R3_0 + R3_A * -1.0) - (R2_0 - R2_A * -1.0)   # worst case: r3 min, r2 max
gap = min(radii(z)[2] - radii(z)[1] for z in zs)
FLAGS["P6"] = (gap > 0)
out(f"   => P6 (expected min(r3-r2) > 0): {'PASS' if FLAGS['P6'] else 'FAIL'}  ({gap*1e3:.3f} mm)")

span3 = A_max[2] / A_min[2]
FLAGS["P7"] = (abs(span3 - 3.67) < 0.05)
out(f"   => P7 (expected C3 span 3.67): {'PASS' if FLAGS['P7'] else 'FAIL'}  ({span3:.3f})")
out()
out("   C2 and C3 are anti-phased: C3's cross-section swings by this factor along the axis while the TOTAL")
out(f"   area is constant at pi*r4^2 = {math.pi*R4**2:.5e} m^2 identically. That exchange is the structure.")
tot = A_of_z.sum(axis=1)
out(f"   check: total area span over z = {tot.min():.6e} .. {tot.max():.6e}  (flat to {1e6*(tot.max()/tot.min()-1):.3f} ppm)")

# =================================================================================================
hdr("[C] THE ORDERING -- measured, because the choice is not free")
# =================================================================================================
ORDER = int(round(math.log2(S_SIDE)))
SUB = int(round(math.log2(S_SIDE)))        # display grid: 2^9 = 512 sub-squares per side
SUB_SIDE = 512
LEVEL = 7                                   # each sub-square is 2^7 x 2^7 sites
PER_SUB = 4 ** LEVEL                        # 16384 sites per display pixel
assert SUB_SIDE * SUB_SIDE * PER_SUB >= 0

out(f"  display grid = {SUB_SIDE}^2 sub-squares, each covering {PER_SUB} sites")
out(f"  decimation   = {CELLS/SUB_SIDE**2:.0f} sites per display pixel   (a 4K frame still shows "
    f"{100*8294400/CELLS:.2f}% of the deposit)")
out()

# --- P8: layer-major is annihilated by this decimation
cnt = np.bincount(np.arange(PER_SUB) % M_SHELL, minlength=M_SHELL)
frac_layermajor = cnt / PER_SUB
out("  layer-major  p = 4n + k : component mix of ONE decimated block")
table([[f"C{k+1}", f"{100*frac_layermajor[k]:.2f}%"] for k in range(M_SHELL)],
      ["component", "share of a decimated block"])
FLAGS["P8"] = bool(np.all(np.abs(frac_layermajor - 0.25) < 0.01))
out(f"   => P8 (expected 25.0% each within 1%): {'PASS' if FLAGS['P8'] else 'FAIL'}")
out("     All four components in equal measure, exactly. The block resolves to their average, so under")
out("     layer-major NO decimated pixel can carry component identity. This is arithmetic, not a measurement.")

# --- P9/P10: component-major survives
shell_of = np.full((SUB_SIDE, SUB_SIDE), -1, dtype=np.int16)
area_of = np.zeros((SUB_SIDE, SUB_SIDE))
nfrac = np.zeros((SUB_SIDE, SUB_SIDE))
deposited = np.zeros((SUB_SIDE, SUB_SIDE), dtype=bool)

straddle_shell, straddle_empty = 0, 0
for q in range(SUB_SIDE * SUB_SIDE):
    d0 = q * PER_SUB
    d1 = d0 + PER_SUB - 1
    dc = d0 + PER_SUB // 2
    x, y = d2xy(SUB, q)
    s_mid = min(dc // N_LAYER, M_SHELL - 1) if dc < PIECES else -1
    shell_of[y, x] = s_mid
    if s_mid >= 0:
        n = dc % N_LAYER
        area_of[y, x] = areas((n + 0.5) * DELTA)[s_mid]
        nfrac[y, x] = n / N_LAYER
        deposited[y, x] = n < F_SWEEP * N_LAYER
    s0 = min(d0 // N_LAYER, M_SHELL - 1) if d0 < PIECES else -1
    s1 = min(d1 // N_LAYER, M_SHELL - 1) if d1 < PIECES else -1
    if s0 != s1:
        if s0 >= 0 and s1 >= 0:
            straddle_shell += 1
        else:
            straddle_empty += 1

single = float(np.mean(np.array([np.count_nonzero(shell_of[y:y + 1, x:x + 1]) for y in [0] for x in [0]]) >= 0))
sh_flat = shell_of.ravel()
nonempty = sh_flat[sh_flat >= 0]
n_single = 0
for s in range(M_SHELL):
    n_single += int(np.count_nonzero(sh_flat == s))
frac_single = 1.0 - (straddle_shell + straddle_empty) / (SUB_SIDE ** 2)

FLAGS["P9"] = (frac_single >= 0.99)
out()
out(f"  component-major  p = kN + n : single-shell blocks = {frac_single:.6f}")
out(f"   => P9 (expected >= 0.99): {'PASS' if FLAGS['P9'] else 'FAIL'}  ({frac_single:.6f})")
FLAGS["P10"] = (straddle_shell == 3)
out(f"   => P10 (expected exactly 3 shell-straddling blocks): {'PASS' if FLAGS['P10'] else 'FAIL'}"
    f"  ({straddle_shell} shell, {straddle_empty} at the empty boundary)")
out()
out(f"  distinct shells present in the map: {len(np.unique(nonempty))}  (expected 4)")
out(f"  empty sites: {100*(1-PIECES/CELLS):.3f}% -- vacuum, drawn as vacuum")

# =================================================================================================
hdr("[D] DEAD CONSTANTS AND THE CURVE")
# =================================================================================================
CANVAS = S_SIDE * PITCH
MEAN_PLACE = 0.3826 * CANVAS
MAX_PLACE = CANVAS / math.sqrt(2.0)
T_RIP = math.sqrt(2.0) * H_OBJ / C_LIGHT
V_MAX = 11.3e3
T_TRANSPORT = MEAN_PLACE / V_MAX
CUT_AREA = N_LAYER * math.pi * R4 ** 2

out(f"  canvas            = S*pitch = {CANVAS:.1f} m = {CANVAS/1e3:.2f} km")
out(f"  mean placement    = 0.3826*canvas = {MEAN_PLACE:.0f} m")
out(f"  max placement     = canvas/sqrt2 = {MAX_PLACE:.0f} m")
FLAGS["P11"] = (abs(CANVAS - 26218.6) < 1 and abs(MEAN_PLACE - 10032) < 5 and abs(MAX_PLACE - 18539) < 5)
out(f"   => P11 (expected 26218.6 / 10032 / 18539): {'PASS' if FLAGS['P11'] else 'FAIL'}")
out()
out(f"  t_rip             = sqrt2*H/c = {T_RIP:.4e} s")
out(f"  transport floor   = mean/v_max = {T_TRANSPORT:.4f} s")
out(f"  ratio             = {T_TRANSPORT/T_RIP:.3e}   (the deposit forms long after the conversion ends)")
FLAGS["P12"] = (abs(T_RIP - 1.0847e-9) / 1.0847e-9 < 5e-3 and abs(T_TRANSPORT - 0.888) < 0.01
                and abs(T_TRANSPORT/T_RIP - 8.2e8) / 8.2e8 < 0.05)
out(f"   => P12 (expected 1.0847e-9 / 0.888 / 8.2e8): {'PASS' if FLAGS['P12'] else 'FAIL'}")
out()
out(f"  total cut area    = N*pi*r4^2 = {CUT_AREA:.5e} m^2")
FLAGS["P13"] = (abs(CUT_AREA - 2.7222e7) / 2.7222e7 < 5e-3)
out(f"   => P13 (expected 2.7222e7): {'PASS' if FLAGS['P13'] else 'FAIL'}")

# contiguity: exhaustive at order 10, sampled at order 16
ORD_TEST = 10
g = np.array([d2xy(ORD_TEST, d) for d in range(4 ** ORD_TEST)])
dg = np.abs(np.diff(g, axis=0)).sum(axis=1)
contig10 = float(np.mean(dg == 1))
rng = np.random.default_rng(20261122)
ds = rng.integers(0, CELLS - 1, size=200000)
pairs = np.array([d2xy(ORDER, int(d)) for d in ds])
pairs1 = np.array([d2xy(ORDER, int(d) + 1) for d in ds])
sampled = float(np.mean(np.abs(pairs - pairs1).sum(axis=1) == 1))
out()
out(f"  contiguity, order {ORD_TEST} exhaustive ({4**ORD_TEST:,} sites) = {contig10:.6f}")
out(f"  contiguity, order {ORDER} sampled ({len(ds):,} of {CELLS:,})          = {sampled:.6f}")
FLAGS["P14"] = (contig10 == 1.0 and sampled == 1.0)
out(f"   => P14 (expected exactly 1.0000): {'PASS' if FLAGS['P14'] else 'FAIL'}")
out("      (P14 as registered said order 16 exhaustively; 4.295e9 indices are not enumerable here, so it is")
out("       evaluated at order 10 exhaustively plus a 2e5 sample at order 16. Substitution disclosed.)")

# =================================================================================================
hdr("[E] LEDGER")
# =================================================================================================
ids = sorted([k for k in FLAGS], key=lambda t: int(t[1:]))
npass = sum(1 for k in ids if FLAGS[k])
out(f"  {npass} / {len(ids)} predictions pass")
out("  " + "  ".join(f"{i}:{'P' if FLAGS[i] else 'F'}" for i in ids))
fails = [i for i in ids if not FLAGS[i]]
out()
if fails:
    out(f"  FAILED: {', '.join(fails)} -- inspect before drawing a verdict from its section.")
else:
    out("  none failed")

# =================================================================================================
# FIGURE
# =================================================================================================
BG = '#FBFAF7'
INK = '#3D3D3B'
MID = '#5F5E5A'
FAINT = '#9A968C'
SHELL_RGB = np.array([[0.541, 0.227, 0.204],    # C1  brick
                      [0.753, 0.541, 0.180],    # C2  ochre
                      [0.239, 0.420, 0.388],    # C3  teal
                      [0.431, 0.498, 0.588]])   # C4  slate
SHELL_HEX = ['#8A3A34', '#C08A2E', '#3D6B63', '#6E7F96']
EMPTY_RGB = np.array([0.929, 0.918, 0.886])

# brightness = normalised piece area within its own shell
img = np.zeros((SUB_SIDE, SUB_SIDE, 3))
for k in range(M_SHELL):
    m = shell_of == k
    if not m.any():
        continue
    lo, hi = A_min[k], A_max[k]
    anorm = np.clip((area_of[m] - lo) / max(hi - lo, 1e-18), 0, 1)
    shade = 0.62 + 0.38 * anorm
    rgb = SHELL_RGB[k] * shade[:, None]
    rgb[~deposited[m]] = 0.45 * SHELL_RGB[k] + 0.55 * np.array([1, 1, 1])   # not yet deposited: pale
    img[m] = rgb
img[shell_of < 0] = EMPTY_RGB

fig = plt.figure(figsize=(15.6, 6.3), facecolor=BG)
gs = fig.add_gridspec(1, 3, width_ratios=[0.95, 1.40, 0.92], wspace=0.30,
                      left=0.052, right=0.988, top=0.770, bottom=0.155)

# ---------------- A: the object, cutaway
ax0 = fig.add_subplot(gs[0, 0])
ax0.set_facecolor(BG)
zz = np.linspace(0, H_OBJ, 500)
r1v = np.full_like(zz, R1)
r2v = R2_0 - R2_A * np.sin(2 * np.pi * zz / H_OBJ)
r3v = R3_0 + R3_A * np.sin(2 * np.pi * zz / H_OBJ)
r4v = np.full_like(zz, R4)
edges = [np.zeros_like(zz), r1v, r2v, r3v, r4v]
handles = []
for k in range(M_SHELL):
    for sgn in (1, -1):
        ax0.fill_betweenx(zz, sgn * edges[k], sgn * edges[k + 1], color=SHELL_HEX[k],
                          lw=0, alpha=0.94)
ax0.axhline(F_SWEEP * H_OBJ, color='white', ls=(0, (6, 3)), lw=1.4, zorder=6)
ax0.axhline(F_SWEEP * H_OBJ, color=INK, ls=(0, (6, 3)), lw=0.7, zorder=7)
ax0.set_xlim(-0.101, 0.101)
ax0.set_ylim(0, H_OBJ * 1.05)
ax0.set_aspect('equal')
ax0.set_xticks([-0.1, -0.05, 0, 0.05, 0.1])
ax0.set_yticks([0, 0.05, 0.10, 0.15, 0.20])
ax0.set_xlabel('r  (m)', fontsize=8.5, color=MID)
ax0.set_ylabel('z  (m)', fontsize=8.5, color=MID)
ax0.tick_params(labelsize=7.5, colors=MID)
for sp in ax0.spines.values():
    sp.set_color('#D8D4CB')
ax0.set_title(f'DEMO-1, axial cross-section   ·   H = {H_OBJ*1e3:.0f} mm', fontsize=10.6, color=INK, pad=9)
ax0.text(-0.098, F_SWEEP * H_OBJ + 0.004, 'front  f = 0.50', fontsize=7.6, color=INK,
         va='bottom', ha='left',
         bbox=dict(fc='white', ec='none', alpha=0.85, pad=1.2))
# shell labels INSIDE the axes at each band's centre, just below the top edge (bands are identical
# at z = 0, H/2 and H, so this position is unambiguous at every height where the label could sit)
# NB the first attempt put these at axes-fraction 0.972, which is z = 0.2347 m -- ABOVE the material
# (ylim is 1.05*H, the fills stop at H), so white labels landed on the background and only the one
# dark label was visible. Data coordinates remove the failure mode.
LABEL_TXT = ('white', INK, 'white', 'white')
for k in range(M_SHELL):
    xc = 0.5 * (edges[k][0] + edges[k + 1][0])
    ax0.text(xc, H_OBJ * 0.952, f'C{k+1}', transform=ax0.transData,
             fontsize=7.8, color=LABEL_TXT[k], ha='center', va='center', weight='bold',
             zorder=8)


# ---------------- B: the Hilbert deposit map
ax1 = fig.add_subplot(gs[0, 1])
ax1.set_facecolor(BG)
ax1.imshow(img, origin='lower', interpolation='nearest',
           extent=[0, CANVAS / 1e3, 0, CANVAS / 1e3])
ax1.set_xlabel('km  on the deposit array  (true scale)', fontsize=8.5, color=MID)
ax1.set_ylabel('km', fontsize=8.5, color=MID)
ax1.tick_params(labelsize=7.5, colors=MID)
for sp in ax1.spines.values():
    sp.set_color('#D8D4CB')
ax1.set_title('the deposit plane under an exact Hilbert traversal', fontsize=10.6, color=INK, pad=9)
for (fx, fy, k) in [(0.13, 0.13, 0), (0.87, 0.13, 1), (0.87, 0.87, 2), (0.13, 0.87, 3)]:
    ax1.text(fx, fy, f'C{k+1}', transform=ax1.transAxes, fontsize=14, color='white',
             ha='center', va='center', weight='bold',
             bbox=dict(fc=INK, ec='none', alpha=0.62, pad=3.0))
ax1.text(0.5, 0.035, 'pale  =  not yet deposited at f = 0.50', transform=ax1.transAxes,
         fontsize=7.6, color=INK, ha='center', va='bottom',
         bbox=dict(fc='white', ec='none', alpha=0.88, pad=2.0))
ax1.text(0.5, 0.955, f'{CANVAS/1e3:.1f} km across   ·   {CELLS:,} sites   ·   shown at 1:{CELLS/SUB_SIDE**2:.0f}',
         transform=ax1.transAxes, fontsize=7.6, color=INK, ha='center', va='top',
         bbox=dict(fc='white', ec='none', alpha=0.88, pad=2.0))

# ---------------- C: one cross-section = four sites (2x2, matching the map's four scrolls)
ax2 = fig.add_subplot(gs[0, 2])
ax2.set_facecolor(BG)
ax2.set_xlim(-0.06, 2.24)
ax2.set_ylim(-0.30, 2.30)
ax2.set_aspect('equal')
ax2.axis('off')
z_mid = F_SWEEP * H_OBJ
rk = radii(z_mid)
edges_k = [0.0, rk[0], rk[1], rk[2], rk[3]]
POS = [(0.0, 1.20), (1.20, 1.20), (0.0, 0.0), (1.20, 0.0)]       # C1 C2 / C3 C4
for k in range(M_SHELL):
    x0, y0 = POS[k]
    ax2.add_patch(Rectangle((x0, y0), 1.0, 1.0, facecolor='#F2F0EA', edgecolor='#D8D4CB', lw=0.8))
    c = (x0 + 0.5, y0 + 0.5)
    ro = edges_k[k + 1] / PITCH
    ri = edges_k[k] / PITCH
    ax2.add_patch(Circle(c, ro, facecolor=SHELL_HEX[k], edgecolor='none'))
    if ri > 0:
        ax2.add_patch(Circle(c, ri, facecolor='#F2F0EA', edgecolor='none'))
    ax2.text(x0 + 0.5, y0 + 1.035, f'C{k+1}', fontsize=8.6, color=SHELL_HEX[k],
             ha='center', va='bottom')
ax2.set_title('what one site holds', fontsize=10.6, color=INK, pad=9)
ax2.text(0.5, -0.245, 'the four sites of one cross-section at z = 0.115 m\n'
                      'site 0.400 m square · the ring outside each piece is vacuum · areas in m²',
         fontsize=7.2, color=MID, ha='center', va='top', linespacing=1.5)
for k in range(M_SHELL):
    x0, y0 = POS[k]
    a = math.pi * (edges_k[k + 1] ** 2 - edges_k[k] ** 2)
    ax2.text(x0 + 0.5, y0 + 0.02, f'{a:.1e}', fontsize=6.4, color=FAINT, ha='center', va='bottom')

fig.text(0.052, 0.945, 'DEMO-1: a declared object mapped to the deposit plane by a space-filling curve',
         fontsize=12.6, color=INK)
fig.text(0.052, 0.885,
         'Declared geometry, not a measurement. The object is 0.230 m; the deposit is 26.2 km across — '
         'the two halves of the process differ by 1.1×10⁵.',
         fontsize=8.5, color=MID)
fig.text(0.052, 0.848,
         'σ :  p = k·N + n  →  Hilbert index   —   component-major, because layer-major is annihilated by '
         'the 1:16384 decimation any renderable frame imposes.',
         fontsize=8.5, color=MID)
fig.text(0.052, 0.032,
         'FL1 · false colour (EN2) · GEOMETRY PRESCRIBED (D2) · no readability claim (MR1.0) · '
         'no claim that the deposit is two-dimensional (Annex B §B.3) · DECLARED OBJECT',
         fontsize=7.2, color=FAINT)

fig.savefig(OUT_PNG, dpi=190, facecolor=BG)
plt.close(fig)
out()
out(f"  figure written: {os.path.relpath(OUT_PNG, ROOT)}")

out()
out("=" * 96)
out("PROVENANCE: NEITHER  (declared geometry + a traversal; establishes no physics)")
with open(OUT_TXT, 'w', encoding='utf-8') as f:
    f.write("\n".join(RES) + "\n")
print("\nwritten to", os.path.relpath(OUT_TXT, ROOT))
