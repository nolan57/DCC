#!/usr/bin/env python3
"""
Matrix v2 -- the 8x4 reconstructed as (row = physics budget) x (column = admitted tier) x (rung = measurement budget).

Emits the grid, the compression count, and the structural predictions of runs/MATRIX2/matrix_v2_registration.md.
Reads the declared-scene calibration table for the bonded reference values; establishes no physics.

Usage:  python src/route/matrix_v2.py [--write]
"""
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CAL = os.path.join(ROOT, 'runs', 'MATRIX', 'structure_tiers_results.txt')
REG = os.path.join(ROOT, 'runs', 'MATRIX2', 'matrix_v2_registration.md')
OUTDIR = os.path.join(ROOT, 'runs', 'MATRIX2')
OUT = os.path.join(OUTDIR, 'matrix_v2_results.txt')

TIERS = (('L0', 'Q0', '>= 0.50'), ('L1', 'xi/h', '>= 4.0'),
         ('L2', 'Q2', '>= 0.50'), ('L3', 'Q3', '>= 2.0'))
NRUNG = 7                      # RL-0 .. RL-6
KNEE = 'R2 knob: weak suppression >= 1e5 (hard, scifi_boundary_v1 s1)'
MODULUS = 'one constitutive law (modulus / body sigma; KIN-DYN supplies none)'

# id, combination, C1, C2, C3, note   -- the eight printed rows, verbatim (M0's duplicate kept)
ROWS = (
    ('R1', 'C1&C2&C3', 1, 1, 1, ''),
    ('R2', 'C1&C2&~C3', 1, 1, 0, ''),
    ('R3', 'C1&~C2&C3', 1, 0, 1, ''),
    ('R4', '~C1&C2&C3', 0, 1, 1, ''),
    ('R5', 'C1&~C2&~C3', 1, 0, 0, ''),
    ('R6', '~C1&~C2&~C3', 0, 0, 0, ''),
    ('R7', '~C1&~C2&C3', 0, 0, 1, ''),
    ('R8', '~C1&~C2&~C3', 0, 0, 0, 'duplicate of R6'),
)
OMITTED = ('R0', '~C1&C2&~C3', 0, 1, 0, 'omitted by sIV; M0')

L = []


def a(s=''):
    L.append(s)


def read(p):
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def calibration():
    """Parse the [2] CALIBRATION block: scene Q0 xi/h Q2 C_xi Q3(q=1) Q3(q=0)."""
    out = {}
    for line in read(CAL).splitlines():
        parts = line.split()
        if len(parts) == 7 and re.fullmatch(r'[A-Z][A-Z0-9\-]*', parts[0]):
            name = parts[0]
            try:
                q3_1 = None if parts[5] == 'n/v' else float(parts[5])
                q3_0 = None if parts[6] == 'n/v' else float(parts[6])
                out[name] = {'Q0': float(parts[1]), 'xi': float(parts[2]),
                             'Q2': float(parts[3]), 'q3_1': q3_1, 'q3_0': q3_0}
            except ValueError:
                continue
    return out


def typing(c1, c2, c3):
    """Rule, not editorial. Returns (field, scene, obstacle, price, klass)."""
    if not c1:
        return (False, None, 'NO-FIELD', '-- (no 2D field exists)',
                'NO-SCENE' + (' + C3' if c3 else ''))
    scene = 'severed' if c2 else 'bonded'
    obs, prices, klass = [], [], 'STRICT'
    if not c2:
        obs.append('MISSING MODEL')
        prices.append(MODULUS)
        klass = 'LIVE'
    if c3:
        obs.append('HARD KNOB')
        prices.append(KNEE)
        klass = 'PRICED'
    if not obs:
        obs, prices = ['--'], ['0']
    return (True, scene, ' + '.join(obs), ' + '.join(prices), klass)


def cells(c1, scene, cal):
    """One (text, kind) per tier. kind: content | priced | blocked | empty."""
    t = cal.get('TILED')
    ref = (t['Q0'], t['xi'], t['Q2'], t['q3_1']) if t else (0.9989, 27.55, 0.9417, 6.316)
    if not c1:
        return [('NO-SCENE', 'empty')] * 4
    if scene == 'severed':
        return [('PRED FAIL @--', 'content'),
                ('PRED FAIL @--', 'content'),
                ('PRED PASS* @0', 'content'),
                ('FAIL@0 BLK@1', 'content')]
    return [('%.4f PASS* @0' % ref[0], 'content'),
            ('%.2f PASS* @0' % ref[1], 'content'),
            ('%.4f PASS* @0' % ref[2], 'content'),
            ('%.3f PASS @1' % ref[3], 'content')]


def l3_at(scene, rung, cal):
    """L3 across the rung axis. Only Q3 depends on the rung; the other three are rung-invariant."""
    t = cal.get('TILED')
    q1 = t['q3_1'] if t else 6.316
    if scene == 'severed':
        return ('FAIL 0.000' if rung == 0 else 'BLOCKED', 'content' if rung == 0 else 'blocked')
    if rung == 0:
        return ('FAIL 0.000', 'content')
    if rung == 1:
        return ('%.3f PASS' % q1, 'content')
    return ('PRICED, uncomputed', 'priced')


def main():
    cal = calibration()
    a('=' * 96)
    a('MATRIX v2 -- reconstructed 8x4  (design proposal; establishes no physics)')
    a('=' * 96)
    a('spec        : docs/specs/matrix_v2_spec_v1.md')
    a('registered  : runs/MATRIX2/matrix_v2_registration.md')
    a('columns     : ' + ' | '.join('%s %s %s' % (k, q, th) for k, q, th in TIERS))
    a('rungs       : RL-0 .. RL-%d  (only L3 moves; Q0,Q1,Q2 are rung-invariant)' % (NRUNG - 1))
    a('calibration : %d declared scenes parsed from runs/MATRIX/structure_tiers_results.txt' % len(cal))
    if not cal:
        a('  !! calibration parse produced nothing -- values below are the fallback constants')
    a('')

    a('=' * 96)
    a('[1] ROW TYPING  (rule, not bookkeeping: three obstacle classes, three prices)')
    a('=' * 96)
    a('  id   combination   field scene    obstacle                 class')
    a('  ' + '-' * 92)
    typed = {}
    for rid, combo, c1, c2, c3, note in ROWS:
        f, sc, obs, price, klass = typing(c1, c2, c3)
        typed[rid] = (c1, sc)
        a('  %-4s %-13s %-5s %-8s %-24s %s%s' % (rid, combo, 'yes' if f else 'no',
                                                 sc or '--', obs, klass,
                                                 '  (' + note + ')' if note else ''))
        a('       price : %s' % price)
    rid, combo, c1, c2, c3, note = OMITTED
    f, sc, obs, price, klass = typing(c1, c2, c3)
    a('  %-4s %-13s %-5s %-8s %-24s %s  (%s)' % (rid, combo, 'yes' if f else 'no',
                                                 sc or '--', obs, klass, note))
    a('')

    a('=' * 96)
    a('[2] THE GRID   cell = value verdict @rung*   (* = passes, not evidential, MR1.1)')
    a('=' * 96)
    a('  id   scene     %s' % ' '.join('%-16s' % k for k, _q, _t in TIERS))
    a('  ' + '-' * 92)
    for rid, combo, c1, c2, c3, note in ROWS:
        _f, sc, _o, _p, _k = typing(c1, c2, c3)
        cs = cells(c1, sc, cal)
        a('  %-4s %-9s %s' % (rid, sc or '--', ' '.join('%-16s' % c[0] for c in cs)))
    a('')
    a('  NOTE  R1/R2 and R3/R5 agree column by column: C3 is column-invisible (S2).')
    a('        It changes the price, not the scene -- which is why 8 rows are rank 2.')
    a('  NOTE  R5\'s L3 value is the TILED reference. MR1.3 forbids inheriting a Q3 measured on an')
    a('        abstract field; it is recorded here as a PREDICTION TARGET, not as a cell value.')
    a('')

    a('=' * 96)
    a('[3] L3 ACROSS THE RUNG AXIS  (the strict -> hard-SF dial; only this column moves)')
    a('=' * 96)
    a('  rung  severed            bonded')
    a('  ' + '-' * 60)
    for r in range(NRUNG):
        sv = l3_at('severed', r, cal)[0]
        bv = l3_at('bonded', r, cal)[0]
        a('  RL-%d  %-18s %s' % (r, sv, bv))
    a('')
    a('  RL-0 deposit as measured | RL-1 declared instrumented observer (q=1, gate <= 3 ns)')
    a('  RL-2 relief geometry | RL-3 oblique illumination | RL-4 visible transmission CLOSED')
    a('  RL-5 persistence to steady state (>= 6.2e23 V/m, or a 2D pocket) | RL-6 picture CLOSED (2^14)')
    a('')

    a('=' * 96)
    a('[4] COMPRESSION  (computed, not asserted)')
    a('=' * 96)
    nominal = len(ROWS) * len(TIERS) * NRUNG
    canon = {}
    for rid, combo, c1, c2, c3, note in ROWS:
        _f, sc, _o, _p, _k = typing(c1, c2, c3)
        if not c1:
            continue
        for k, _q, _t in TIERS[:3]:
            canon[(sc, k, 0)] = cells(c1, sc, cal)[TIERS.index((k, _q, _t))][1]
        for r in range(NRUNG):
            canon[(sc, 'L3', r)] = l3_at(sc, r, cal)[1]
    kinds = {}
    for v in canon.values():
        kinds[v] = kinds.get(v, 0) + 1
    a('  nominal  8 x 4 x %d        : %d' % (NRUNG, nominal))
    a('  canonical (distinct)       : %d' % len(canon))
    for k in ('content', 'priced', 'blocked', 'empty'):
        if k in kinds:
            a('    %-8s               : %d' % (k, kinds[k]))
    a('  compression ratio         : %.1f : 1' % (nominal / float(len(canon))))
    a('')

    a('=' * 96)
    a('[5] STRUCTURAL PREDICTIONS  (registration S1..S4)')
    a('=' * 96)
    with_field = [r[0] for r in ROWS if r[2]]
    s1 = with_field == ['R1', 'R2', 'R3', 'R5']
    a('  S1 4 of 8 rows carry a field   : %s  %s' % ('CONFIRMED' if s1 else 'FAILED', with_field))
    g = dict((r[0], r) for r in ROWS)
    same = lambda x, y: typing(*g[x][2:5])[1] == typing(*g[y][2:5])[1]
    s2 = same('R1', 'R2') and same('R3', 'R5')
    a('  S2 C3 is column-invisible      : %s  (R1=R2, R3=R5)' % ('CONFIRMED' if s2 else 'FAILED'))
    f0, sc0, _o, _p, _k = typing(*OMITTED[2:5])
    s3 = (not f0) and sc0 is None
    a('  S3 the omitted row adds 0 cells: %s  (NO-SCENE)' % ('CONFIRMED' if s3 else 'FAILED'))
    s4 = len(canon) == 20 and kinds.get('content') == 8
    a('  S4 224 -> 20, 8 with content   : %s  (%d canonical, %d content)'
      % ('CONFIRMED' if s4 else 'FAILED', len(canon), kinds.get('content', 0)))
    if not s4:
        a('       -- the registered count omitted the severed scene\'s L3 at RL-0 (0.000 FAIL),')
        a('          which is a value and not a blocked entry. Correction recorded as E1 in the')
        a('          registration; the prediction above is left standing as written.')
    a('')

    a('=' * 96)
    a('[6] WHAT THE GRID SAYS')
    a('=' * 96)
    a('  R5 is the only row in which all four columns pass, and it passes at RL-1 -- the cheapest')
    a('  rung, priced as a CONVENTION (a declared observer) rather than a field. R2, the row that')
    a('  costs nothing, fails three of four and its single pass is non-evidential. The matrix,')
    a('  typed correctly, reaches the ladder\'s conclusion from the row side.')
    a('')
    a('  Ceiling, unchanged: R2\'s scene is the deposit, and the deposit reads only (M, N)')
    a('  (DEPOSIT-BLIND: six objects, one digest, I(canvas;r4) = 0). MR1.6 stands.')
    a('')
    a('PROVENANCE: NEITHER  (row typing by rule; values from the declared-scene calibration)')

    txt = '\n'.join(L) + '\n'
    dt = time.time() - os.path.getmtime(REG) if os.path.exists(REG) else None
    amended = '## Errata' in read(REG) if os.path.exists(REG) else False
    if amended:
        txt += ('ordering          : NOT EVIDENCED BY MTIME -- the registration carries an appended\n'
                '                    erratum, so its mtime is the append time. Declaration order is\n'
                '                    asserted by the erratum text, not by this number (%.1f s).\n' % (dt or 0))
    else:
        txt += 'registration mtime to this run : %s\n' % (
            ('%.1f s earlier  -> declared BEFORE evaluation' % dt) if dt is not None and dt > 0
            else 'NOT EARLIER -- ordering violated')
    if '--write' in sys.argv:
        if not os.path.isdir(OUTDIR):
            os.makedirs(OUTDIR)
        with open(OUT, 'w', encoding='utf-8') as f:
            f.write(txt)
    sys.stdout.write(txt)
    return 0 if (s1 and s2 and s3) else 1


if __name__ == '__main__':
    sys.exit(main())
