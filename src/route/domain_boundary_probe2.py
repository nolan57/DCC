#!/usr/bin/env python
"""
Probe 2 -- is Q2's failure about the FIELD or about the ESTIMATOR?

Main run result: Q2 < 0 across the whole sparse-excursion family.  A near-constant field is genuinely
predictable, so a negative Q2 for it is a false negative, not a property of the field.  Deterministic
fact to test: plug_q2's joint table is CTX*CTX*BINS = 16384 cells estimated from 16129 samples.

Prediction A1-P3 is the causal test: shrink the table (CTX 16 -> 4, BINS 64 -> 16 = 256 cells, ~63
samples per cell) and the SAME field should show the structure it actually has.

CTX and BINS are locked at 16 and 64.  Numbers taken at other values are DIAGNOSTIC ONLY and may not be
cited as tier verdicts.
"""
import ast
import hashlib
import json
import math
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCK = os.path.join(ROOT, 'runs', 'MATRIX', 'threshold_lock.json')
SRC = os.path.join(ROOT, 'src', 'route', 'structure_tiers.py')


def hdr(t):
    print('\n' + '=' * 96)
    print(t)
    print('=' * 96)


with open(LOCK, encoding='utf-8') as f:
    lock = json.load(f)
C = lock['declared_constants']
GRID, BINS, CTX = C['grid'][0], C['bins'], C['context_levels']
NULL_M, NULL_SEED0 = C['null_realisations'], C['null_seed_start']

text = open(SRC, encoding='utf-8').read()
tree = ast.parse(text)
WANT = ('quant', 'plug_q2')
BODY = '\n\n'.join(ast.get_source_segment(text, n) for n in tree.body
                   if isinstance(n, ast.FunctionDef) and n.name in WANT)
G = {'np': np, 'BINS': BINS, 'CTX': CTX}
exec(compile(BODY, '<extracted>', 'exec'), G)
plug_q2 = G['plug_q2']

hdr('[0] THE ARITHMETIC THAT MOTIVATES THE PROBE')
n_samples = (GRID - 1) * (GRID - 1)
n_cells = CTX * CTX * BINS
print('  joint table cells      : CTX*CTX*BINS = %d*%d*%d = %d' % (CTX, CTX, BINS, n_cells))
print('  samples available      : (GRID-1)^2 = %d' % n_samples)
print('  samples per cell       : %.4f' % (n_samples / n_cells))
print('  -> at the locked configuration the plug-in conditional entropy has about ONE sample')
print('     per parameter.  That is a bias source independent of any field.')

hdr('[1] THE FIELD: near-constant with a BLOCK-STRUCTURED excursion')
# 8x8 blocks: 3% of blocks are "up" by +0.3, 3% "down" by -0.3, rest at 0.5.  Modal mass ~0.94, and the
# field is trivially predictable: a cell's value equals its block's value, so any neighbour tells you.
rng = np.random.default_rng(9100)
nb = GRID // 8
blk = rng.random((nb, nb))
up = blk < 0.03
dn = blk > 0.97
u = np.full((GRID, GRID), 0.5)
val = np.where(up, 0.5 + 0.3, np.where(dn, 0.5 - 0.3, 0.5))
u = np.repeat(np.repeat(val, 8, axis=0), 8, axis=1)
q, _ = G['quant'](u)
modal = float(np.bincount(q.ravel(), minlength=BINS).max() / q.size)
print('  grid %dx%d, 8x8 blocks, modal mass = %.4f' % (GRID, GRID, modal))
print('  a neighbour agrees with its cell in %.2f%% of pairs (by construction ~100%%)'
      % (100.0 * float((u[1:, 1:] == u[:-1, 1:]).mean())))


def null_q2(ctx, bins):
    G['CTX'], G['BINS'] = ctx, bins
    vals = []
    for k in range(NULL_M):
        w = np.random.default_rng(NULL_SEED0 + k).random((GRID, GRID))
        vals.append(plug_q2(w)[0])
    return float(np.mean(vals))


hdr('[2] MEASUREMENT AT THE LOCKED ALPHABET (CTX = 16, BINS = 64)')
q2_locked = plug_q2(u)[0]
null_locked = null_q2(CTX, BINS)
Q2_locked = (q2_locked - null_locked) / (1.0 - null_locked)
print('  raw q2     = %.6f' % q2_locked)
print('  q2(null)   = %.6f' % null_locked)
print('  Q2         = %.6f   (locked threshold 0.50)' % Q2_locked)

hdr('[3] SAME FIELD, SMALLER TABLE (diagnostic only -- CTX and BINS are locked)')
G['CTX'], G['BINS'] = CTX, BINS
q2_small = plug_q2(u)[0] if False else None
G['CTX'], G['BINS'] = 4, 16
q2_small = plug_q2(u)[0]
null_small = null_q2(4, 16)
Q2_small = (q2_small - null_small) / (1.0 - null_small)
print('  CTX=4, BINS=16 -> 256 cells, %.1f samples per cell' % (n_samples / 256.0))
print('  raw q2     = %.6f' % q2_small)
print('  q2(null)   = %.6f' % null_small)
print('  Q2         = %.6f' % Q2_small)
G['CTX'], G['BINS'] = CTX, BINS

hdr('[4] PREDICTION LEDGER')
res = []


def rec(tag, ok, note):
    res.append((tag, bool(ok), note))
    print('  %-6s %-5s %s' % (tag, 'PASS' if ok else 'FAIL', note))


rec('A1-P1', Q2_locked < 0.5, 'Q2 on the block-structured near-constant field = %.4f (< 0.50)' % Q2_locked)
rec('A1-P2', q2_locked < 0.05, 'raw q2 at the locked alphabet = %.4f (< 0.05)' % q2_locked)
rec('A1-P3', q2_small > 0.30, 'raw q2 on the SAME field with a 256-cell table = %.4f (> 0.30)' % q2_small)

hdr('SUMMARY')
nfail = sum(1 for _t, ok, _n in res if not ok)
print('  predictions confirmed  : %d of %d' % (len(res) - nfail, len(res)))
print('  predictions FAILED     : %d  %s' % (nfail, ', '.join(t for t, ok, _n in res if not ok) or '-'))
print()
if res[2][1]:
    print('  CAUSE ESTABLISHED: the same field reads q2 = %.3f with a 256-cell table and %.3f with the'
          % (q2_small, q2_locked))
    print('  locked 16384-cell table.  Q2\'s failure is the parameter/sample ratio of the estimator,')
    print('  not the geometry of the field.  T2\'s stated mechanism (alphabet bias) is therefore WRONG;')
    print('  the prohibition must be stated in terms of the estimator, not of the alphabet.')
else:
    print('  CAUSE NOT ESTABLISHED: shrinking the table did not recover the structure, so the')
    print('  undersampling account is also wrong and the annex must leave the mechanism unexplained.')
print()
print('PROVENANCE: NEITHER  (estimator characterisation; establishes no physics)')
