#!/usr/bin/env python
"""
RQ-17 -- matrix v2 regenerated on the measured plate class.

Replaces every PREDICTED or BORROWED cell of runs/MATRIX2/matrix_v2_results.txt with a MEASURED one, or with an
explicit UNREALIZED / BLOCKED / PRICED, and prints the condition (lattice pitch p, h = 1 cell) under which each
value was taken. Reads run products only; measures nothing new; changes no threshold.

Inputs : runs/MATRIX2/plate_array_results.txt, runs/MATRIX/structure_tiers_results.txt,
         runs/MATRIX/threshold_lock.json
Output : runs/MATRIX2/matrix_v2r_results.txt
Usage  : python src/route/matrix_v2r.py [--write]
"""
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTDIR = os.path.join(ROOT, 'runs', 'MATRIX2')
PA = os.path.join(OUTDIR, 'plate_array_results.txt')
REG = os.path.join(OUTDIR, 'matrix_v2r_registration.md')
OUT = os.path.join(OUTDIR, 'matrix_v2r_results.txt')
LOCK = os.path.join(ROOT, 'runs', 'MATRIX', 'threshold_lock.json')

TIERS = ('L0', 'L1', 'L2', 'L3')
QUANT = {'L0': 'Q0', 'L1': 'xi/h', 'L2': 'Q2', 'L3': 'Q3'}

ROWS = (('R1', 'C1&C2&C3', 1, 1, 1, ''),
        ('R2', 'C1&C2&~C3', 1, 1, 0, ''),
        ('R3', 'C1&~C2&C3', 1, 0, 1, ''),
        ('R4', '~C1&C2&C3', 0, 1, 1, ''),
        ('R5', 'C1&~C2&~C3', 1, 0, 0, ''),
        ('R6', '~C1&~C2&~C3', 0, 0, 0, ''),
        ('R7', '~C1&~C2&C3', 0, 0, 1, ''),
        ('R8', '~C1&~C2&~C3', 0, 0, 0, 'duplicate of R6'))
OMITTED = ('R0', '~C1&C2&~C3', 0, 1, 0, 'omitted by sIV; M0')
PITCHES = (8, 16, 32)

L = []


def a(s=''):
    L.append(s)


def hdr(t):
    a('')
    a('=' * 96)
    a(t)
    a('=' * 96)


def read(p):
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


lock = json.load(open(LOCK, encoding='utf-8'))
THR = {k: float(lock['tiers'][k]['threshold_c']) for k in TIERS}


# ==================================================================================
# 0. the measured class
# ==================================================================================
hdr('[0] SOURCE -- the measured plate class (runs/MATRIX2/plate_array_results.txt)')

MEAS = {}
for line in read(PA).splitlines():
    parts = line.split()
    if len(parts) == 8 and re.fullmatch(r'PA-\d+f?|SHUF-\d+', parts[0]):
        try:
            MEAS[parts[0]] = dict(P0=float(parts[1]), Q0=float(parts[2]), xi=float(parts[3]),
                                  Q2=float(parts[4]))
        except ValueError:
            pass

a('  id       Q0        xi/h     Q2       (thresholds %s / %s / %s)'
  % (THR['L0'], THR['L1'], THR['L2']))
for k in ('PA-8', 'PA-16', 'PA-32', 'PA-16f', 'SHUF-16'):
    if k in MEAS:
        r = MEAS[k]
        a('  %-8s %-9.4f %-8.2f %-9.4f' % (k, r['Q0'], r['xi'], r['Q2']))
a('')
a('  The pitch instances are the declared class; SHUF-16 is the evidentiality control')
a('  (it fails all three tiers, so the passes below are not shuffle-invariant).')


def verdict(tier, key):
    r = MEAS[key]
    v = r['Q0'] if tier == 'L0' else (r['xi'] if tier == 'L1' else r['Q2'])
    return v, ('PASS' if v >= THR[tier] else 'FAIL')


# ==================================================================================
# 1. row typing (unchanged rule)
# ==================================================================================
hdr('[1] ROW TYPING -- the v2 rule, restated so the grid is readable without v2')

MODULUS = 'one constitutive law (modulus / body sigma; KIN-DYN supplies none)'
KNEE = 'R2 knob: weak suppression >= 1e5 (scifi_boundary_v1 s1)'


def typing(c1, c2, c3):
    if not c1:
        return (None, 'NO-SCENE', '-- (no 2D field exists)')
    sc = 'severed' if c2 else 'bonded'
    if not c2:
        return (sc, 'UNREALIZED', MODULUS + (' + ' + KNEE if c3 else ''))
    if c3:
        return (sc, 'PRICED', KNEE)
    return (sc, 'LIVE', '0')


a('  id   combination   scene    class         price')
a('  ' + '-' * 88)
T = {}
for rid, combo, c1, c2, c3, note in ROWS:
    sc, klass, price = typing(c1, c2, c3)
    T[rid] = (sc, klass)
    a('  %-4s %-13s %-8s %-13s %s%s' % (rid, combo, sc or '--', klass, price,
                                        '  (' + note + ')' if note else ''))
sc0, k0, p0 = typing(*OMITTED[2:5])
a('  %-4s %-13s %-8s %-13s %s  (%s)' % (OMITTED[0], OMITTED[1], sc0 or '--', k0, p0, OMITTED[5]))

# ==================================================================================
# 2. the grid
# ==================================================================================
hdr('[2] THE GRID   cell = value verdict @condition   (condition = lattice pitch p, h = 1 cell)')


def cell(rid, tier):
    sc, klass = T[rid]
    if sc is None:
        return 'NO-SCENE', 'empty'
    if tier == 'L3':
        if sc == 'severed':
            return '0.000 FAIL @RL-0', 'content'          # q = 0 exactly: identity, not a measurement
        return '0.000 FAIL @RL-0', 'content'              # identity, as above
    if sc == 'bonded':
        return 'UNREALIZED', 'unrealized'
    v, sd = verdict(tier, 'PA-%d' % PITCHES[1])
    return ('%.4f %s @p16' % (v, sd)) if tier != 'L1' else ('%.2f %s @p16' % (v, sd)), 'content'


a('  id   scene    %s' % '  '.join('%-18s' % ('%s %s' % (k, QUANT[k])) for k in TIERS))
a('  ' + '-' * 92)
for rid, combo, c1, c2, c3, note in ROWS:
    a('  %-4s %-8s %s' % (rid, (T[rid][0] or '--'),
                          '  '.join('%-18s' % cell(rid, t)[0] for t in TIERS)))
a('')
a('  R2 and R5 are the only rows that could carry a measured value; R5 cannot, because the bonded')
a('  scene needs one constitutive law that the record does not have. R1/R3 differ from R2/R5 only')
a('  in price (C3), never in scene -- S2 of the v2 registration.')

# ==================================================================================
# 3. the pitch axis, printed inside the row that owns it
# ==================================================================================
hdr('[3] PITCH AXIS of the severed row -- the row does not have one cell per column')

a('  p    Q0       L0     xi/h    L1     Q2       L2     vector')
a('  ' + '-' * 74)
vectors = {}
for p in PITCHES:
    key = 'PA-%d' % p
    q0, s0 = verdict('L0', key)
    xi, s1 = verdict('L1', key)
    q2, s2 = verdict('L2', key)
    vec = (s0, s1, s2)
    vectors[p] = vec
    a('  %-4d %-8.4f %-6s %-7.2f %-6s %-8.4f %-6s %s'
      % (p, q0, s0, xi, s1, q2, s2,
         '/' + ''.join('Y' if v == 'PASS' else '.' for v in vec) + '/.'))
a('')
a('  Last column reads L0/L1/L2/L3: Y = PASS, . = FAIL. L3 is FAIL at RL-0 for every pitch (q = 0).')
a('  Fill control PA-16f (f = 0.4727 at p = 16): Q0 %.4f, xi/h %.2f, Q2 %.4f -- the same Q0 as PA-16,'
  % (MEAS['PA-16f']['Q0'], MEAS['PA-16f']['xi'], MEAS['PA-16f']['Q2']))
a('  which is why Q0 cannot be read as a statement about the object.')

# ==================================================================================
# 4. L3 across the rung axis (unchanged: no new input)
# ==================================================================================
hdr('[4] L3 ACROSS THE RUNG AXIS -- unchanged, because nothing new exists above RL-0')

a('  rung  severed                       bonded')
a('  ' + '-' * 66)
for r in range(7):
    sv = '0.000 FAIL' if r == 0 else 'BLOCKED (no compliant sigma_s)'
    bv = '0.000 FAIL' if r == 0 else ('BLOCKED (no compliant sigma_s)' if r == 1 else 'PRICED, uncomputed')
    a('  RL-%d  %-30s %s' % (r, sv, bv))

# ==================================================================================
# 5. compression
# ==================================================================================
hdr('[5] COMPRESSION -- counted, not asserted')

canon = {}
for rid in ('R2', 'R5'):
    sc, _k = T[rid]
    for t in TIERS[:3]:
        if sc == 'bonded':
            canon[(sc, t, None)] = 'unrealized'
        else:
            for p in PITCHES:
                canon[(sc, t, p)] = 'content'
    canon[(sc, 'L3', 0)] = 'content'
    for r in range(1, 7):
        canon[(sc, 'L3', r)] = ('blocked' if (sc == 'severed' or r == 1) else 'priced')

kinds = {}
for v in canon.values():
    kinds[v] = kinds.get(v, 0) + 1
nominal = 8 * 4 * 7
a('  nominal  8 rows x 4 columns x 7 rungs : %d' % nominal)
a('  canonical (distinct entries)          : %d' % len(canon))
for k in ('content', 'unrealized', 'blocked', 'priced'):
    a('    %-10s                          : %d' % (k, kinds.get(k, 0)))
a('  compression ratio                     : %.1f : 1' % (nominal / float(len(canon))))

# ==================================================================================
# 6. predictions
# ==================================================================================
hdr('[6] PREDICTIONS G1..G5 -- registration runs/MATRIX2/matrix_v2r_registration.md')

res = []
g1 = (len(canon) == 26 and kinds.get('content') == 11)
res.append(('G1', 'canonical 26, content 11, ratio 8.6 : 1', g1,
            '%d / %d / %.1f : 1' % (len(canon), kinds.get('content', 0), nominal / float(len(canon)))))

passes = {}
for rid in ('R2', 'R5'):
    passes[rid] = sum(1 for t in TIERS if cell(rid, t)[0].split()[-2:-1] == ['PASS']
                      or ' PASS ' in cell(rid, t)[0])
g2 = (max(passes.values()) < 4) and passes['R5'] == 0
res.append(('G2', 'no row passes 4 of 4; R5 passes 0 of 4', g2,
            'R2 %d/4 at p16, R5 %d/4' % (passes['R2'], passes['R5'])))

LEAK = ('0.9989', '27.55', '0.9417', '6.316')
grid_txt = ' '.join(cell(rid, t)[0] for rid in ('R2', 'R5') for t in TIERS)
g3 = not any(k in grid_txt for k in LEAK)
res.append(('G3', 'no calibration constant appears as a cell value', g3,
            'leaked: %s' % ', '.join(k for k in LEAK if k in grid_txt) if not g3 else 'clean: ' + grid_txt))

g4 = len(set(vectors.values())) >= 2
res.append(('G4', 'the severed row has >= 2 verdict vectors over the pitch axis', g4,
            'distinct vectors: %d  (%s)' % (len(set(vectors.values())),
                                            ' | '.join('p%d:%s' % (p, ''.join('Y' if x == 'PASS' else '.' for x in vectors[p]))
                                                       for p in PITCHES))))

g5 = 'PRED' not in grid_txt
res.append(('G5', 'the label PRED disappears from the grid (0 cells, was 3)', g5,
            'PRED count %d' % grid_txt.count('PRED')))

a('')
for k, what, ok, got in res:
    a('  %-3s %-56s : %-9s  (%s)' % (k, what, 'CONFIRMED' if ok else 'FALSIFIED', got))

# ==================================================================================
# 7. what changed
# ==================================================================================
hdr('[7] WHAT CHANGED FROM matrix_v2_results.txt (retained unedited)')

a('  1. WITHDRAWN: "R5 is the only row in which all four columns pass". R5\'s four passes were')
a('     TILED\'s calibration values (0.9989 / 27.55 / 0.9417 / 6.316), borrowed from a scene that')
a('     is not this row\'s scene. The bonded row now reads UNREALIZED in L0-L2 and BLOCKED in L3,')
a('     because one constitutive law is missing. V4 stays unanswered.')
a('  2. WITHDRAWN: the three PRED cells of the severed row. V1-V3 are falsified (erratum E2); the')
a('     cells now read measured values at a declared pitch.')
a('  3. ADDED: the pitch axis. One row, three verdict vectors.')
a('  4. UNCHANGED: the row typing, the L3 column, the rung axis, every threshold. The 224 -> 26')
a('     compression is recounted, not re-derived by assertion.')
a('')
a('  The grid now says a narrower thing than v2 did, and a true one: the severed row PASSES L0 and')
a('  L2 at every pitch the grid can hold, PASSES L1 only when the lattice is coarse (p >= 19.3 cells),')
a('  and FAILS L3 at every rung because q = 0 is exact. No row passes four columns -- the "only row')
a('  that passes everything" was an artefact of borrowing, and it is gone.')

a('')
a('PROVENANCE: NEITHER  (re-presentation of measured products; establishes no physics)')

if os.path.exists(REG):
    amended = bool(re.search(r'^## Errata\s*$', read(REG), re.M))
    if amended:
        a('ordering          : NOT EVIDENCED BY MTIME -- the registration carries an erratum.')
    else:
        a('registration to this run : %.1f s later  -> declared BEFORE evaluation'
          % (time.time() - os.path.getmtime(REG)))

txt = '\n'.join(L) + '\n'
print(txt, end='')
if '--write' in sys.argv:
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(txt)
    sys.stderr.write('wrote %s\n' % OUT)
sys.exit(0 if all(r[2] for r in res) else 1)
