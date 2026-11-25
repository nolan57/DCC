#!/usr/bin/env python
"""
FL1 figure for RQ-16 -- the declared scene, its shuffle control, and the three measured laws.

Draws only what runs/MATRIX2/plate_array_results.txt contains: the declared arrays and the measured numbers.
The label on the figure says so. This is a chart (FL1 per D-3/G1), not a measurement column, and not a
depiction of the deposit (DEPOSIT-BLIND: six objects, one digest, I(canvas;r4) = 0).

Usage:  python src/route/plate_array_figure.py
"""
import contextlib
import importlib.util
import io
import os

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'runs', 'MATRIX2', 'plate_array_figure_v1.png')

_spec = importlib.util.spec_from_file_location(
    'structure_tiers', os.path.join(ROOT, 'src', 'route', 'structure_tiers.py'))
ST = importlib.util.module_from_spec(_spec)
with contextlib.redirect_stdout(io.StringIO()):
    _spec.loader.exec_module(ST)

GRID = ST.GRID
P0_NULL, Q2_NULL = ST.P0_NULL, ST.Q2_NULL


def plates(p, s):
    return ((np.arange(GRID) % p)[:, None] < s).astype(float) * \
           ((np.arange(GRID) % p)[None, :] < s).astype(float)


def m(u):
    p0 = ST.total_persistence(u)
    q2p, _ = ST.plug_q2(u)
    xi, _ = ST.char_scale(u)
    return 1.0 - p0 / P0_NULL, xi, (q2p - Q2_NULL) / (1.0 - Q2_NULL)


u = plates(16, 12)
us = u.ravel()[np.random.default_rng(9999).permutation(GRID * GRID)].reshape(GRID, GRID)
q0, xi, q2 = m(u)
q0s, xis, q2s = m(us)

ps = (8, 16, 32)
curves = [(m(plates(p, int(0.75 * p)))) for p in ps]

fig = plt.figure(figsize=(11.6, 4.5), dpi=200)
fig.subplots_adjust(left=0.045, right=0.955, top=0.86, bottom=0.235, wspace=0.22)
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.45], wspace=0.30)

ax = fig.add_subplot(gs[0, 0])
ax.imshow(u, cmap='gray', interpolation='nearest')
ax.set_title('declared array   p=16, s=12, f=0.5625\nQ0 %.4f   xi/h %.2f   Q2 %.4f' % (q0, xi, q2),
             fontsize=8, linespacing=1.5)
ax.set_xticks([]); ax.set_yticks([])

ax = fig.add_subplot(gs[0, 1])
ax.imshow(us, cmap='gray', interpolation='nearest')
ax.set_title('same pixels, permuted (seed 9999)\nQ0 %.4f   xi/h %.2f   Q2 %.4f' % (q0s, xis, q2s),
             fontsize=8, linespacing=1.5)
ax.set_xticks([]); ax.set_yticks([])

ax = fig.add_subplot(gs[0, 2])
ax.plot(ps, [c[0] for c in curves], 'o-', color='#1d4ed8', lw=1.4, ms=4, label='Q0   (left)')
ax.plot(ps, [c[2] for c in curves], '^-', color='#0f766e', lw=1.4, ms=4, label='Q2   (left)')
h_thr1 = ax.axhline(0.5, color='#555', lw=0.9, ls='--', label='threshold 0.5 (L0, L2)')
ax.plot(ps, [q0s] * 3, 'x', color='#a00', ms=8, mew=1.4, label='shuffled Q0 (left)')
ax.set_ylim(-0.1, 1.08)
ax.set_ylabel('Q0 , Q2', fontsize=8)
ax.tick_params(labelsize=7)

ax2 = ax.twinx()
ax2.plot(ps, [c[1] for c in curves], 's--', color='#b45309', lw=1.4, ms=4, label='xi/h  (right)')
h_thr2 = ax2.axhline(4.0, color='#b45309', lw=0.9, ls=':', label='threshold 4.0 (L1)')
ax2.set_ylim(-0.4, 7.6)
ax2.set_ylabel('xi/h  (cells)', fontsize=8, color='#b45309')
ax2.tick_params(labelsize=7, colors='#b45309')

ax.set_xscale('log', base=2)
ax.set_xticks(ps); ax.set_xticklabels(['8', '16', '32'])
ax.set_xlabel('lattice pitch p (cells), h = 1 cell', fontsize=8)
ax.set_title('measured:  Q0 = 1 - 1/(p^2 P0null)     xi/h = 0.207 p', fontsize=8.5)

h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2,
          fontsize=6.4, frameon=False, loc='lower left', ncol=2, handlelength=1.8, columnspacing=1.4)

fig.text(0.045, 0.055,
         'FL1 -- declared chart drawn from runs/MATRIX2/plate_array_results.txt.  Not a measurement of the deposit:'
         '\nDEPOSIT-BLIND -- six physically distinct objects share one digest, I(canvas; r4) = 0.  Panels 1-2 are'
         '\ndeclared synthetic fields, not photographs and not reconstructions.',
         fontsize=6.6, color='#444', linespacing=1.6)

fig.savefig(OUT, facecolor='white')
print('wrote %s' % OUT)
