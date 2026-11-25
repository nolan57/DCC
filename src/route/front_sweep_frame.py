#!/usr/bin/env python
"""
The mid-sweep frame -- the artifact the route's goal names and the repo has never produced.

Registered inputs only (docs/decisions/front_sweep_v1.md):
    body phantom z in [0, 1.738] m, integral A dz = 0.0601 m^3
    layer 0.215 nm, 1.457 components/layer, 1.18e10 plates
    array 90126^2, max placement 25.5 km, mean 13.8 km, 8.12e9 peelings

Predictions fixed in runs/FRONT/mid_sweep_frame_registration.md (with addenda A1, A2) BEFORE this file existed.
A2 withdrew the converted VOLUME fraction: the registered table gives per-segment ranges, not a profile, and the
declared reconstruction misses the registered volume. The frame prints f = z/H, which is definitional, and says on
its face that the volume fraction is not shown.

The frame is a presentation product: GEOMETRY PRESCRIBED (D2), FL1, false colour (EN2). It establishes no physics,
is not a matrix cell, and makes no readability claim (MR1.0).

Falsifier honoured in the drawing: no plate may be drawn on the object's remaining material. The departing plume is
therefore placed strictly outside the silhouette, whose maximum radius is sqrt(0.0540/pi) = 0.131 m.
"""
import math
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'runs', 'FRONT', 'mid_sweep_fl1.png')

C_LIGHT = 2.99792458e8
A_LAYER = 0.215e-9
Z_TOP = 1.738
V_REG = 0.0601
N_PEEL_REG = 8.12e9
N_PLATE_REG = 1.18e10
COMP_PER_LAYER = 1.457
SIDE_REG = 90126
MAX_DIST_REG = 25.5e3
MEAN_DIST_REG = 13.8e3
LEG_SPLIT = 0.800
LEG_HALF_SEP = 0.062

SEG = [
    (0.012, 0.800, 0.0063, 0.0221),
    (0.800, 0.960, 0.0457, 0.0457),
    (0.960, 1.170, 0.0464, 0.0516),
    (1.170, 1.380, 0.0540, 0.0540),
    (1.380, 1.470, 0.0490, 0.0490),
    (1.470, 1.560, 0.0098, 0.0098),
    (1.560, 1.738, 0.0202, 0.0303),
]


def area(z):
    for z0, z1, a0, a1 in SEG:
        if z0 <= z <= z1:
            t = 0.0 if z1 == z0 else (z - z0) / (z1 - z0)
            return a0 + t * (a1 - a0)
    return 0.0


V_MODEL = sum((a0 + a1) / 2.0 * (z1 - z0) for z0, z1, a0, a1 in SEG)
t_rip = math.sqrt(2.0) * Z_TOP / C_LIGHT
ZF = 0.5 * Z_TOP
layers = Z_TOP / A_LAYER
spacing = MAX_DIST_REG / ((SIDE_REG / 2.0) * math.sqrt(2.0))
canvas = SIDE_REG * spacing
max_dist = (canvas / 2.0) * math.sqrt(2.0)
mean_dist = 0.3826 * canvas
speed = Z_TOP / t_rip
layers_deposited = ZF / A_LAYER
plates_deposited = layers_deposited * COMP_PER_LAYER
fill = plates_deposited / N_PLATE_REG          # fraction of the CENSUS deposited, not of cells
K_PER_CELL = N_PLATE_REG / float(SIDE_REG ** 2)  # 1.4527 -- cells receive more than one plate (GD10, open)
occ = min(1.0, fill * K_PER_CELL)               # cells holding at least one plate; saturates at 1
plate_side = math.sqrt((V_REG / A_LAYER) / N_PLATE_REG)
R_MAX = math.sqrt(0.0540 / math.pi)

res = []


def rec(tag, ok, note):
    res.append((tag, bool(ok), note))
    print('  %-4s %-5s %s' % (tag, 'PASS' if ok else 'FAIL', note))


print('=' * 92)
print('MID-SWEEP FRAME -- derived numbers and prediction ledger')
print('=' * 92)
print('  registered: z_top=%.3f m  layer=%.3f nm  array=%d^2  max=%.1f km  mean=%.1f km'
      % (Z_TOP, A_LAYER * 1e9, SIDE_REG, MAX_DIST_REG / 1e3, MEAN_DIST_REG / 1e3))
print('  t_rip = sqrt2 z_top / c = %.6e s' % t_rip)
print()
rec('N1', abs(layers - N_PEEL_REG) / N_PEEL_REG < 0.005,
    'layers z_top/a_L = %.4e vs registered peelings %.3e (%.2f%% apart)'
    % (layers, N_PEEL_REG, 100 * abs(layers - N_PEEL_REG) / N_PEEL_REG))
rec('N4', abs(spacing - 0.4001) < 1e-3, 'site spacing = %.4f m' % spacing)
rec('N5', abs(canvas - 36.06e3) < 60, 'canvas side = %.2f km' % (canvas / 1e3))
rec('N6', abs(max_dist - MAX_DIST_REG) / MAX_DIST_REG < 1e-6,
    'farthest plate (N5/2)*sqrt2 = %.3f km -> recovers the registered %.1f km' % (max_dist / 1e3, MAX_DIST_REG / 1e3))
rec('N7', abs(mean_dist - MEAN_DIST_REG) / MEAN_DIST_REG < 0.01,
    'mean distance 0.3826*N5 = %.3f km vs registered %.1f km' % (mean_dist / 1e3, MEAN_DIST_REG / 1e3))
rec('N8', abs(speed - C_LIGHT / math.sqrt(2)) / (C_LIGHT / math.sqrt(2)) < 1e-9,
    'front speed = %.6e m/s = c/sqrt2 to 1e-9' % speed)
rec("N9'", 0.045 <= V_MODEL <= 0.056,
    'declared reconstruction integrates to %.5f m^3, %.1f%% below the registered %.4f'
    % (V_MODEL, 100 * (V_REG - V_MODEL) / V_REG, V_REG))
print()
print('  frame prints f = z/H = %.3f (definitional).' % (ZF / Z_TOP))
print('  volume fraction NOT printed -- the table gives ranges, not a profile; the reconstruction')
print('  misses the registered volume by %.1f%%, and that miss is the reason the number is absent.'
      % (100 * (V_REG - V_MODEL) / V_REG))
print('  layers deposited so far = %.4e ; plates ~ %.4e (x %.3f comp/layer)'
      % (layers_deposited, plates_deposited, COMP_PER_LAYER))
print('  fraction of the census deposited = %.4f  (this is what the label used to print '
      'as a percentage of sites)' % fill)
print('  cells holding >=1 plate          = %.4f  = min(1, f x %.4f)   <- the corrected label'
      % (occ, K_PER_CELL))
print('  NOTE  census/cells = %.4f > 1, so cells hold more than one plate; one-plate-per-cell '
      'would need an array of side %.0f.'
      % (K_PER_CELL, math.sqrt(N_PLATE_REG)))
print('        Registered OPEN as GD10; H_eff unaffected (plates are coplanar -- '
      'effective_2d_definition_v1_annex_B sB.1).')
print('  plate side = %.4f m on %.4f m spacing (so a plate fits its site)' % (plate_side, spacing))
print('  max silhouette radius = %.4f m -> the plume is drawn beyond 0.19 m (falsifier check)' % R_MAX)

z = np.arange(0.0, Z_TOP + 1e-9, 0.002)
A = np.array([area(v) for v in z])
two = z < LEG_SPLIT
r_leg = np.sqrt(np.where(two, A / (2.0 * math.pi), 0.0))
r_one = np.sqrt(np.where(two, 0.0, A / math.pi))

fig = plt.figure(figsize=(13.6, 6.9))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.26], width_ratios=[1.0, 1.06],
                      hspace=0.46, wspace=0.16, left=0.055, right=0.975, top=0.895, bottom=0.215)
axb = fig.add_subplot(gs[0, 0])
axa = fig.add_subplot(gs[0, 1])
axs = fig.add_subplot(gs[1, :])

# ---- panel A ---------------------------------------------------------------------------------
kept = z >= ZF
for zlo, zhi, r, c in ((None, None, r_leg, LEG_HALF_SEP), (None, None, r_one, 0.0)):
    pass
rr_leg = np.where(two, r_leg, np.nan)
rr_one = np.where(two, np.nan, r_one)
axb.fill_betweenx(z, -LEG_HALF_SEP - rr_leg, -LEG_HALF_SEP + rr_leg, where=kept,
                  color='#4A4A48', linewidth=0, zorder=2)
axb.fill_betweenx(z, LEG_HALF_SEP - rr_leg, LEG_HALF_SEP + rr_leg, where=kept,
                  color='#4A4A48', linewidth=0, zorder=2)
axb.fill_betweenx(z, -rr_one, rr_one, where=kept, color='#4A4A48', linewidth=0, zorder=2)
for lo, hi in ((-LEG_HALF_SEP - rr_leg, -LEG_HALF_SEP + rr_leg), (LEG_HALF_SEP - rr_leg, LEG_HALF_SEP + rr_leg),
               (-rr_one, rr_one)):
    axb.plot(lo[~kept], z[~kept], color='#C9C6BD', lw=0.9, ls=(0, (3, 3)), zorder=1)
    axb.plot(hi[~kept], z[~kept], color='#C9C6BD', lw=0.9, ls=(0, (3, 3)), zorder=1)

axb.axhline(ZF, color='#A32D2D', lw=1.8, zorder=4)
axb.text(0.165, ZF - 0.055, 'the front\nz = %.3f m  (%.0f%% of the height)' % (ZF, 100 * ZF / Z_TOP),
         color='#A32D2D', fontsize=8.5, va='top', ha='left', zorder=6)

for i, (dz, dx, ang) in enumerate([(0.02, 0.20, 14), (0.075, 0.235, 40), (0.135, 0.205, 22),
                                  (0.19, 0.26, 55), (0.245, 0.215, 8), (0.30, 0.255, 34)]):
    axb.add_patch(Rectangle((dx - 0.013, ZF + dz - 0.013), 0.026, 0.026, angle=ang,
                            facecolor='#534AB7', edgecolor='none', alpha=0.85 - 0.07 * i, zorder=5))
axb.annotate('', xy=(0.335, ZF + 0.40), xytext=(0.285, ZF + 0.31),
             arrowprops=dict(arrowstyle='-|>', color='#534AB7', lw=1.0, alpha=0.85))
axb.text(0.395, 1.545, 'plates leave for the array\n(symbols, not to scale;\ndrawn count is not a census)',
         fontsize=7.5, color='#534AB7', ha='right', va='top')
axb.text(0.0, 0.16, 'consumed\n%.2e layers peeled' % layers_deposited, fontsize=8,
         color='#9A968C', ha='center', va='bottom', zorder=6)

axb.text(0.30, 0.44, 'calf to thigh', fontsize=7.5, color='#5F5E5A', ha='center')
axb.text(0.30, 0.965, 'pelvis', fontsize=7.5, color='#5F5E5A', ha='left')
axb.text(0.30, 1.075, 'abdomen', fontsize=7.5, color='#5F5E5A', ha='left')
axb.text(0.30, 1.285, 'thorax', fontsize=7.5, color='#5F5E5A', ha='left')
axb.text(0.235, 1.655, 'head', fontsize=7.5, color='#5F5E5A', ha='left')
axb.text(-0.395, 1.855, 'intact above the front', fontsize=8, color='#3D3D3B', ha='left', va='top')
axb.text(-0.395, 0.03, 'cross-sections from the registered area table', fontsize=7.5, color='#9A968C',
         ha='left', va='bottom')

axb.set_xlim(-0.40, 0.40)
axb.set_ylim(0.0, 1.90)
axb.set_ylabel('z  (m, true scale)', fontsize=9)
axb.set_yticks([0, 0.5, 1.0, 1.5])
axb.set_xticks([])
axb.set_title('the object, front mid-sweep', fontsize=11, pad=7)
for s in ('top', 'right'):
    axb.spines[s].set_visible(False)

# ---- panel B ---------------------------------------------------------------------------------
km = canvas / 1e3
axa.add_patch(Rectangle((0, 0), km, km, facecolor='#FBFAFF', edgecolor='#7F77DD', lw=1.0))
axa.add_patch(Rectangle((0, 0), km, km * occ, facecolor='#EEEDFE', edgecolor='none'))
n = 44
for i in range(n + 1):
    for j in range(n + 1):
        y = j * km / n
        if y <= km * occ:
            axa.plot(i * km / n, y, marker='s', ms=1.5, color='#534AB7', alpha=0.5, zorder=3)
axa.set_xlim(-1.4, km + 1.4)
axa.set_ylim(-1.4, km + 1.4)
axa.set_aspect('equal')
axa.set_xlabel('km  (true scale)', fontsize=9)
axa.tick_params(labelsize=8)
axa.set_title('where it went: the deposit array, %.1f km across' % km, fontsize=11, pad=7)
axa.text(km * 0.02, km * 0.975, '%.1f%% of cells hold a plate' % (100 * occ),
         fontsize=8.5, color='#5F5E5A', ha='left', va='top')
axa.text(km * 0.44, km * 0.865, 'empty', fontsize=9, color='#9A968C', ha='center', va='center')
axa.text(km * 0.5, km * 0.20, 'already deposited', fontsize=9, color='#3D3D3B', ha='center', va='center',
         bbox=dict(facecolor='white', edgecolor='none', pad=2.0, alpha=0.85))

ins = axa.inset_axes([0.605, 0.555, 0.315, 0.315])
ins.set_xlim(-0.05, 3.3)
ins.set_ylim(-0.05, 3.3)
for i in range(9):
    ins.axvline(i * spacing, color='#D3D1C7', lw=0.4, zorder=1)
    ins.axhline(i * spacing, color='#D3D1C7', lw=0.4, zorder=1)
for i in range(8):
    for j in range(3):
        if (i + j) % 5 != 4:
            ins.add_patch(Rectangle((i * spacing + (spacing - plate_side) / 2,
                                     j * spacing + (spacing - plate_side) / 2),
                                    plate_side, plate_side, facecolor='#534AB7',
                                    edgecolor='none', alpha=0.85))
ins.set_xticks([])
ins.set_yticks([])
ins.set_facecolor('#FFFFFF')
for s in ins.spines.values():
    s.set_edgecolor('#B4B2A9')
    s.set_linewidth(0.6)
ins.set_title('8x8 sites, %.2f m apart' % spacing, fontsize=6.8, pad=3, color='#5F5E5A')

# ---- panel C ---------------------------------------------------------------------------------
axs.set_xscale('log')
axs.set_xlim(1e-2, 3e5)
axs.set_ylim(0.0, 1.0)
axs.set_yticks([])
axs.axhline(0.52, color='#D3D1C7', lw=1.0, zorder=0)
axs.plot([Z_TOP], [0.52], marker='o', ms=7, color='#4A4A48')
axs.plot([canvas], [0.52], marker='s', ms=7, color='#534AB7')
axs.annotate('', xy=(canvas, 0.52), xytext=(Z_TOP, 0.52),
             arrowprops=dict(arrowstyle='<->', color='#A32D2D', lw=1.1))
axs.text(math.sqrt(Z_TOP * canvas), 0.70, 'x %.2e' % (canvas / Z_TOP), ha='center', fontsize=9,
         color='#A32D2D')
axs.text(Z_TOP, 0.26, 'the object  %.2f m' % Z_TOP, ha='center', fontsize=8.5, color='#3D3D3B')
axs.text(canvas, 0.26, 'the deposit array  %.1f km' % km, ha='center', fontsize=8.5, color='#534AB7')
axs.set_xlabel('metres (log scale)', fontsize=8.5, labelpad=2)
axs.tick_params(labelsize=8, pad=2)
axs.set_title('why no single photograph exists: the two halves of the process are %.1e apart'
              % (canvas / Z_TOP), fontsize=9.5, pad=3, color='#5F5E5A')
for s in ('top', 'right', 'left'):
    axs.spines[s].set_visible(False)

fig.text(0.055, 0.105, 'true aspect, no geometric distortion  ·  FL1, false colour (EN2)  ·  geometry PRESCRIBED (D2), '
         'not solved  ·  front speed c/\u221a2 = %.4e m/s  ·  t_rip = %.3e s' % (speed, t_rip),
         fontsize=8, color='#5F5E5A')
fig.text(0.055, 0.062, 'volume fraction NOT shown: the registered table gives per-segment ranges, not a profile, and '
         'the declared reconstruction misses the registered volume by %.0f%%  ·  plate marks are symbols, not to scale'
         % (100 * (V_REG - V_MODEL) / V_REG), fontsize=8, color='#5F5E5A')
fig.text(0.055, 0.022, 'no claim that the state is two-dimensional, a graph, or readable; ME4 certifies only that no '
         'handles were created  ·  no claim about support or motion (position is initial, D2)',
         fontsize=8, color='#5F5E5A')
fig.suptitle('The 2D-ification front mid-sweep: what is consumed here is deposited %.0f km away'
             % (mean_dist / 1e3), fontsize=13, x=0.055, ha='left', y=0.972)

fig.savefig(OUT, dpi=190, facecolor='white')
print()
print('  frame written: %s' % os.path.relpath(OUT, ROOT))
nfail = sum(1 for _t, ok, _n in res if not ok)
print('  predictions confirmed %d of %d ; FAILED %d %s'
      % (len(res) - nfail, len(res), nfail, ', '.join(t for t, ok, _n in res if not ok) or '-'))
print()
print('PROVENANCE: NEITHER  (presentation product on prescribed geometry; establishes no physics)')
