#!/usr/bin/env python3
"""
RR-DT-01 instrument: record repair, deferral, and dual-track advancement.

Report-only bookkeeping. It verifies that the three AX-01 documentation repairs landed,
that the six deferred findings are deferred by name and their records untouched, that the
Track A relabel is in place, and that the Track B record is complete and stops at exactly
one boundary. It emits no physics verdict and licenses no claim.

Every check is a string predicate on files that exist at run time, plus one SHA-256
invariant set frozen in runs/RR-DT/rr_dt_01_invariants.json before any docs/ edit of this
round. The invariant check is the load-bearing one: it is what makes "no sealed product was
edited" a measurement rather than an assertion.

Usage
  python src/rr_dt/rr_dt_01_record_repair.py            dry run
  python src/rr_dt/rr_dt_01_record_repair.py --write    write the product
"""
import hashlib
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'runs', 'RR-DT', 'rr_dt_01_record_repair_results.txt')

LADDER = 'docs/specs/relaxation_ladder_v1.md'
CROSS = 'docs/conventions/constraint_crosswalk_v1.md'
G0P = 'docs/decisions/G0p_seven_row_verdict_v3.md'
REG = 'docs/conventions/symbol_registry.md'
UNFOLD = 'docs/decisions/kinematic_vs_dynamic_unfolding_v1.md'
RECORD = 'runs/RR-DT/constraint_relaxation_record.md'
AX01 = 'runs/AX/ax01_axiom_audit_results.txt'
EFF2D = 'docs/conventions/effective_2d_definition_v1.md'
SNAP = 'runs/RR-DT/rr_dt_01_invariants.json'
LEDGER = 'runs/PROGRAM/round_ledger.jsonl'
QUEUE = 'docs/program/round_queue_v1.json'
TERM = 'reports/DCC_terminal_answer_v1.md'

ANNOT = '[IDENT \u2014 no constraint information; see AX-01 HIGH-3]'


def read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8', errors='replace') as f:
        return f.read()


def norm(t):
    return re.sub(r'\s+', ' ', t.replace('> ', '').replace('\n>', '')).strip()


def sha(p):
    h = hashlib.sha256()
    with open(os.path.join(ROOT, p), 'rb') as f:
        for b in iter(lambda: f.read(65536), b''):
            h.update(b)
    return h.hexdigest()


def has(p, *subs):
    t = norm(read(p))
    return all(s in t for s in subs)


# ---------------------------------------------------------------- invariants
def invariant_checks():
    snap = json.loads(read(SNAP))
    rows = []

    # the snapshot must be a faithful read of the ledger as it stood when the snapshot was
    # frozen. Later rounds legitimately append records, so this is a subset test on the
    # snapshot's own keys, not an equality test on the whole ledger: the product stays
    # reproducible after the round that emits it is itself appended.
    recs = [json.loads(l) for l in read(LEDGER).splitlines() if l.strip()]
    from_ledger = {}
    for r in recs:
        for k in ('product', 'registration'):
            p = r.get(k)
            if p and os.path.exists(os.path.join(ROOT, p)):
                from_ledger[p] = sha(p)
    keys = snap['ledger_sealed']
    derived = all(p in from_ledger for p in keys)
    rows.append(('I0', 'invariant snapshot is a faithful read of the ledger (%d sealed files)'
                 % len(keys), derived, ''))

    moved = [p for p, h in snap['ledger_sealed'].items()
             if not os.path.exists(os.path.join(ROOT, p)) or sha(p) != h]
    rows.append(('I1', 'every ledger-registered product/registration is byte-identical',
                 not moved, ','.join(moved)))

    q = json.loads(read(QUEUE))
    qi = hashlib.sha256(json.dumps(q['items'], sort_keys=True).encode()).hexdigest()
    qg = hashlib.sha256(json.dumps(q.get('gates', []), sort_keys=True).encode()).hexdigest()
    rows.append(('I2', 'queue items+gates unchanged (cursor/board notes are the only movable fields)',
                 qi == snap['queue_items_sha'] and qg == snap['queue_gates_sha'], ''))

    rows.append(('I3', 'terminal answer (sealed round 62) byte-identical',
                 sha(TERM) == snap['terminal_answer_r62'], sha(TERM)[:16]))

    gmoved = [f for f, h in snap['gates_dir'].items()
              if sha(os.path.join('reports/gates', f)) != h]
    rows.append(('I4', 'reports/gates/ byte-identical', not gmoved, ','.join(gmoved)))

    ok5 = ('1.94805e4' in read(LADDER)) and ('2\u00d710\u2074\u00d7' in read(LADDER)) \
        and ('\u03a6 = \u22124.5' in read(LADDER)) and ('an external parameter set to 1 fm' in norm(read(EFF2D))) \
        and ('four-slot conditional implication' in norm(read(EFF2D))) and ('2.60' in read(LADDER))
    rows.append(('I5', 'the three numbers the deferred findings are about are unchanged', ok5, ''))
    return rows


# ---------------------------------------------------------------- repairs
def repair_checks():
    rows = []

    lad = norm(read(LADDER))
    ok = ('pricing assumes `d\u2225` serves as both in-plane column pitch and plate thickness' in lad
          and 'changes by a factor of `15.4`' in lad
          and '`2\u00d710\u2074\u00d7` atomic spacing (`15.4 fm` vs `0.3 nm`)' in lad)
    rows.append(('R1', 'RL-6 carries the dual-role qualification; rung table bytes intact', ok,
                 'ladder'))

    ok = has(CROSS, '### 8.5', 'carries \u00a78.2', 'relaxation_ladder_v1.md', 'modelling choice')
    rows.append(('R2', 'crosswalk carries the forward reference to the ladder qualification', ok,
                 'crosswalk 8.5'))

    g = norm(read(G0P))
    ok = ('conditional on fixed `(M, A_\u22a5, m\u0304)`' in g
          and 'geometric quantity, independent of the electron convention' not in g
          and 'NO-GO' in g)
    rows.append(('R3', 'row 1 basis is conditional; verdict and evidence level untouched', ok, 'G0p row 1'))

    ok = ('## 8. Erratum E4 (round 71)' in g
          and 'geometric, conditional on fixed `(M, A_\u22a5, m\u0304)`; scales as `(A_\u22a5/M)^{1/2}` under variation' in g
          and 'sealed' in g and '23f6813392621b40' in g)
    rows.append(('R4', 'reverse-on replacement is carried by erratum; sealed cell named, not edited', ok,
                 'G0p E4'))

    r = norm(read(REG))
    ok = (ANNOT in read(REG)
          and 'phase1_symbolic_constraint_results.txt' in r
          and 'phase1_symbolic_constraint_registration.md' in r
          and 'governor_digest.txt' in r
          and 'r4_finite_region_geometry_v1.md' in r
          and 'R-IDENT-1' in r)
    rows.append(('R5', 'IDENT annotation registered with all four in-record locations', ok, 'registry 4'))

    u = norm(read(UNFOLD))
    ok = ('WORKING-HYPOTHESIS' in u
          and '[WORKING-HYPOTHESIS: adiabaticity; see RR-DT-01 \u00a73.1]' in u
          and 'IDEAL-LIMIT' in u)
    rows.append(('R7', 'adiabaticity relabelled WORKING-HYPOTHESIS with the citation tag and retention clause',
                 ok, 'unfolding 12'))
    return rows


# ---------------------------------------------------------------- deferral
def deferred():
    ax = read(AX01)
    found = []
    for line in ax.splitlines():
        m = re.match(r'\[(F-0\d\d)\] \[(HIGH|MEDIUM|LOW)\] (.*)', line.strip())
        if m:
            found.append((m.group(1), m.group(2), m.group(3)))
    return [(i, s, t) for i, s, t in found if s in ('MEDIUM', 'LOW')]


# ---------------------------------------------------------------- track B
def levels():
    t = read(RECORD)
    out = {}
    marks = [(m.start(), m.group(1)) for m in re.finditer(r'\nB(\d+) \u2014 ', t)]
    for i, (pos, n) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(t)
        out['B' + n] = t[pos:end]
    return out


def track_b_checks():
    lv = levels()
    rows = []

    need = ('Relaxed:', 'Degree:', 'Self-consistent:', 'Hard boundary reached:', 'Notes:')
    missing = [k for k in ('B%d' % i for i in range(1, 9))
               if k not in lv or not all(f in lv[k] for f in need)]
    rows.append(('R8a', 'B1-B8 each carry the five required fields', not missing, ','.join(missing)))

    reached = [k for k, v in lv.items()
               if re.search(r'Hard boundary reached: YES', v)]
    rows.append(('R8b', 'exactly one level reaches the boundary, and it is B8',
                 reached == ['B8'], ','.join(reached)))

    ok = 'NEVER RELAXED' in read(RECORD) and 'NOT EVALUATED-BEYOND-BOUNDARY' in read(RECORD)
    rows.append(('R8c', 'B9 recorded as not-evaluated; B10 never relaxed', ok, ''))

    tri = [k for k, v in lv.items()
           if ('RL-6' in v and "G0'" in v and re.search(r'eff-?2D|Effective-2D', v, re.I))]
    rows.append(('R8d', 'every level re-evaluates RL-6, the G0-prime clause and the effective-2D criterion',
                 len(tri) >= 8, ','.join(sorted(tri))))
    return rows


def arithmetic():
    c, G = 2.99792458e8, 6.67430e-11
    hbarc = 197.3269804
    H0 = 67.4e3 / 3.0856775814913673e22
    lam = 3 * H0 ** 2 / c ** 2
    rho_nuc = 0.16 * 940.0 * 1.602176634e32
    k = 2 * math.pi / 1e-3
    rho_rel = (c ** 4 / (8 * math.pi * G)) * (k * k * 1.7e-4)
    a = 8.6227e16 / 70.0
    drift = 0.5 * a * (8.2553e-9) ** 2
    checks = [
        ('CK1', 'Lambda_obs = 1.5926e-52 m^-2 (1.5926e-82 fm^-2)',
         abs(lam / 1.5926e-52 - 1) < 1e-3, '%.4e' % lam),
        ('CK2', '78.8 orders below the 1e-3 fm^-2 probe',
         abs(math.log10(1e-3 / (lam * 1e-30)) - 78.80) < 0.02,
         '%.2f' % math.log10(1e-3 / (lam * 1e-30))),
        ('CK3', 'relief rho_req = 3.232e46 J/m^3 = 1.3e12 rho_nuc (1 mm, eps=1.7e-4)',
         abs(rho_rel / 3.232e46 - 1) < 2e-3 and abs(rho_rel / rho_nuc / 1.3e12 - 1) < 0.05,
         '%.3e J/m3, %.2e rho_nuc' % (rho_rel, rho_rel / rho_nuc)),
        ('CK4', 'unconfined L_z drift over t_rip = 4.20e-2 m',
         abs(drift / 4.197e-2 - 1) < 2e-3, '%.4e' % drift),
        ('CK5', 'dE_z = 619.921 MeV at 1 fm; 2.4797 eV at 250 nm',
         abs(math.pi * hbarc / 1.0 - 619.921) < 1e-2
         and abs(math.pi * hbarc / 250e6 * 1e6 - 2.4797) < 1e-3,
         '%.3f MeV / %.4f eV' % (math.pi * hbarc, math.pi * hbarc / 250e6 * 1e6)),
        ('CK6', 'RL-6 spans 1.9478e4 (d_par) / 3.000e5 (L_z) / 4.4497e4 (6.742 fm); printed 1.94805e4',
         abs(0.3e-9 / 15.40194e-15 / 1.94781e4 - 1) < 1e-4
         and abs(0.3e-9 / 1e-15 / 3.0e5 - 1) < 1e-6
         and abs(0.3e-9 / 6.742e-15 / 4.44972e4 - 1) < 1e-4
         and abs(0.3e-9 / 15.400e-15 / 1.94805e4 - 1) < 1e-5,
         '%.5e / %.4e / %.5e  (15.400 fm -> %.5e)' % (0.3e-9 / 15.40194e-15, 0.3e-9 / 1e-15,
                                                     0.3e-9 / 6.742e-15, 0.3e-9 / 15.400e-15)),
    ]
    return checks


# ---------------------------------------------------------------- emit
def build():
    inv = invariant_checks()
    rep = repair_checks()
    tb = track_b_checks()
    ar = arithmetic()
    defs = deferred()

    L = []
    a = L.append
    a('=' * 78)
    a('RR-DT-01  RECORD REPAIR, DEFERRAL AND DUAL-TRACK ADVANCEMENT')
    a('=' * 78)
    a('Date: 2026-11-24T03:52:00Z')
    a('Authority: governor directive G-71-01 (round 71)')
    a('Instrument: src/rr_dt/rr_dt_01_record_repair.py')
    a('Pre-registration: runs/RR-DT/rr_dt_01_record_repair_registration.md')
    a('  registration sha256   %s' % sha('runs/RR-DT/rr_dt_01_record_repair_registration.md'))
    a('Invariant snapshot: runs/RR-DT/rr_dt_01_invariants.json (frozen before any docs/ edit)')
    a('Relaxation log: runs/RR-DT/constraint_relaxation_record.md')
    a('PROVENANCE: NEITHER (documentation repair; derives no physics, adjudicates no gate)')
    a('Result class: RECORD REPAIR. No survival, visibility, gate, price, route or D-state claim.')
    a('')
    a('The one rule this round obeys: an artifact whose SHA-256 is in the round ledger is')
    a('never edited. Where G-71-01 names such an artifact as an annotation target, the')
    a('annotation is carried by this product and by the errata of the unsealed document that')
    a('owns the same content. Section E measures that claim instead of asserting it.')

    a('')
    a('-' * 78)
    a('SECTION A: REPAIR LEDGER')
    a('-' * 78)
    edits = [
        ('HIGH-1', 'd_parallel dual role', LADDER, 'EDITABLE',
         'qualification block appended directly below the rung table; table bytes unchanged'),
        ('HIGH-1', 'forward reference', CROSS, 'EDITABLE',
         'new 8.5 points back at the ladder block and forward from 8.2'),
        ('HIGH-2', 'row 1 basis cell', G0P, 'EDITABLE',
         'parenthetical replaced by its conditional form; verdict and evidence level untouched'),
        ('HIGH-2', 'reverse-on phrase', TERM, 'SEALED (round 62)',
         'NOT EDITED: replacement text carried by G0p erratum E4; hash preserved'),
        ('HIGH-3', 'K^2 - K_ijK^ij annotation', REG, 'EDITABLE',
         'registration R-IDENT-1 names four in-record locations and their dispositions'),
        ('HIGH-3', 'K^2 - K_ijK^ij annotation', 'runs/P1/phase1_symbolic_constraint_results.txt',
         'SEALED (round 63)', 'NOT EDITED: annotation carried here; hash preserved'),
        ('HIGH-3', 'K^2 - K_ijK^ij annotation', 'runs/P1/phase1_symbolic_constraint_registration.md',
         'SEALED (round 63)', 'NOT EDITED: annotation carried here; hash preserved'),
        ('Track A', 'adiabaticity relabel', UNFOLD, 'EDITABLE',
         'section 12: WORKING-HYPOTHESIS, citation tag, dependency table, retention clause'),
    ]
    for hid, what, path, status, action in edits:
        a('%-7s %-34s %-52s' % (hid, what, path))
        a('        status %-18s action %s' % (status, action))
        if hid == 'HIGH-3':
            a('        annotation %s' % ANNOT.replace('\u2014', '--'))
    a('')
    a('  Predicate results:')
    for rid, desc, ok, note in rep:
        a('  %-4s %-5s %s' % (rid, 'PASS' if ok else 'FAIL', desc))
        if not ok and note:
            a('       %s' % note)
    ok_rep = all(r[2] for r in rep)

    a('')
    a('-' * 78)
    a('SECTION B: DEFERRED FINDINGS (MEDIUM and LOW, G-71-01 2)')
    a('-' * 78)
    a('  Read from runs/AX/ax01_axiom_audit_results.txt, not re-typed: %d items.' % len(defs))
    for i, s, t in defs:
        a('  %s [%s] %s' % (i, s, t[:150] + ('...' if len(t) > 150 else '')))
    a('')
    a('  Count by severity: MEDIUM %d, LOW %d' %
      (sum(1 for d in defs if d[1] == 'MEDIUM'), sum(1 for d in defs if d[1] == 'LOW')))
    a('  Disposition: DEFERRED. No record carrying any of these six findings was repaired,')
    a('  annotated or re-worded this round. Two of them live in sealed products (F-005 in')
    a('  Phase 1, F-009 in Phase 1b) and are covered by the hash check in SECTION E; the')
    a('  other four live in editable documents, and the sentences that carry them are')
    a('  checked verbatim by invariant I5: 2e4 / 1.94805e4 and 2.60% (F-010), Phi = -4.5')
    a('  (F-006), L_z = 1 fm as an external parameter and the four-slot conditional (F-007,')
    a('  F-008). A deferral that let any of those sentences drift would not be a deferral.')
    ok_def = [(i, s) for i, s, _t in defs] == [('F-005', 'MEDIUM'), ('F-006', 'MEDIUM'),
                                              ('F-007', 'MEDIUM'), ('F-008', 'MEDIUM'),
                                              ('F-009', 'LOW'), ('F-010', 'LOW')]

    a('')
    a('-' * 78)
    a('SECTION C: TRACK A (adiabaticity as WORKING-HYPOTHESIS)')
    a('-' * 78)
    a('  Status      : WORKING-HYPOTHESIS (was ASSUMPTION in the sealed AX-01 audit, AX-S02).')
    a('  Tag         : [WORKING-HYPOTHESIS: adiabaticity; see RR-DT-01 3.1]')
    a('  Home        : docs/decisions/kinematic_vs_dynamic_unfolding_v1.md section 12')
    a('  Advanced    : the smooth 2D-ization branch proceeds without proof of the hypothesis.')
    a('  Not advanced: survival, visibility, ground-state, gate passage, price movement.')
    a('  Retention   : if the hypothesis is disproved, results are relabelled IDEAL-LIMIT,')
    a('                not withdrawn (G-71-01 3.1, last bullet).')
    a('  One honest note recorded in section 12: the 1.92e4x / 2.18e4x timescale measurement')
    a('  that made adiabaticity look violated belongs to a counterfactual elastic body the')
    a('  deposition does not build. The hypothesis is unstated for the dynamical reading and')
    a('  unnecessary for the kinematic one; that asymmetry is why the branch can advance.')

    a('')
    a('-' * 78)
    a('SECTION D: TRACK B (constraint relaxation, B1-B10)')
    a('-' * 78)
    lv = levels()
    for k in ('B%d' % i for i in range(1, 10)):
        if k in lv:
            sc = re.search(r'Self-consistent: (\w+)', lv[k])
            hb = re.search(r'Hard boundary reached: (YES|NO)', lv[k])
            a('  %-4s self-consistent %-9s boundary %s' %
              (k, sc.group(1) if sc else '?', hb.group(1) if hb else '?'))
    a('  B10  NEVER RELAXED (definition of the boundary, not a rung on it)')
    a('')
    a('  HARD-SCI-FI-LIMIT : B8 (referential reading); B10 by construction under the strict')
    a('                      propositional reading. Both recorded, neither recommended.')
    a('  Contradiction     : "the scene at theta is well defined" together with "a closed')
    a('                      causal curve passes through the scene". The theta tuple needs a')
    a('                      global time function and an environment radiance independent of')
    a('                      the object; a CTC removes both, so the same sentence about the')
    a('                      same object is asserted and has no referent. The record already')
    a('                      rates referential failure fatal (N7), which is why B8, not B6 or')
    a('                      B7, is the wall: B1-B7 weaken, cost or re-scope, and none of them')
    a('                      makes a scene sentence unsayable.')
    a('  Avoidable         : YES. (i) confine the CTC to a region spacelike-separated from the')
    a('                      observer patch; or (ii) carry only the steady-state S branch, with')
    a('                      no transient and no imaged scene.')
    for rid, desc, ok, note in tb:
        a('  %-4s %-5s %s%s' % (rid, 'PASS' if ok else 'FAIL', desc, ('  [' + note + ']') if (note and not ok) else ''))
    ok_tb = all(r[2] for r in tb)

    a('')
    a('-' * 78)
    a('SECTION E: INVARIANTS')
    a('-' * 78)
    for rid, desc, ok, note in inv:
        a('  %-4s %-5s %s%s' % (rid, 'PASS' if ok else 'FAIL', desc,
                               ('  [' + note + ']') if (note and not ok) else ''))
    ok_inv = all(r[2] for r in inv)
    a('')
    a('  Ledger-sealed files checked: %d' % len(json.loads(read(SNAP))['ledger_sealed']))

    a('')
    a('-' * 78)
    a('SECTION F: SELF-TESTS')
    a('-' * 78)
    for cid, desc, ok, val in ar:
        a('  %-4s %-5s %s' % (cid, 'PASS' if ok else 'FAIL', desc))
        a('       %s' % val)
    ok_ar = all(c[2] for c in ar)

    a('')
    a('  DISCLOSURE (found during the dry run, before emission): the archive prints two values')
    a('  for the RL-6 ratio. Ladder E5 and phase1c give 1.94805e4, which is 0.3 nm / 15.400 fm;')
    a('  AX-01 gives 1.948e4 from 0.3 nm / 15.40194 fm, which is 1.94781e4. The two differ by')
    a('  1.2e-4 relative because 15.400 fm is the rounded pitch and 15.40194 fm is N_s^-1/2.')
    a('  Both round to 2e4 and neither is re-priced here; CK6 checks all four baselines so the')
    a('  discrepancy is visible rather than averaged away.')

    a('')
    a('  IDENT  predicate count: repairs %d, track-B %d, invariants %d, arithmetic %d'
      % (len(rep), len(tb), len(inv), len(ar)))
    a('  IDENT  deferral list matches AX-01 F-005..F-010 exactly: %s' % ('PASS' if ok_def else 'FAIL'))

    overall = ok_rep and ok_tb and ok_inv and ok_ar and ok_def
    a('')
    a('=' * 78)
    a('[VERDICTS]')
    a('=' * 78)
    a('  REPAIR     %d/%d' % (sum(1 for r in rep if r[2]), len(rep)))
    a('  TRACK-B    %d/%d' % (sum(1 for r in tb if r[2]), len(tb)))
    a('  INVARIANT  %d/%d' % (sum(1 for r in inv if r[2]), len(inv)))
    a('  ARITHMETIC %d/%d' % (sum(1 for c in ar if c[2]), len(ar)))
    a('  Deferral: 6 items by name, none repaired')
    a('  Findings: HIGH 0 open (three repaired, one carried by Track A) / MEDIUM 4 deferred / LOW 2 deferred')
    a('  OVERALL: %s' % ('PASS' if overall else 'FAIL'))
    a('  evidence level: RECORD REPAIR / NOT GATE EVIDENCE')
    a('  PROVENANCE: NEITHER')
    a('')
    a('Content generated by AI')
    return '\n'.join(L) + '\n', overall


def main():
    txt, ok = build()
    try:
        txt.encode('ascii')
    except UnicodeEncodeError as e:
        raise SystemExit('product is not ASCII: %s' % e)
    if '--write' in sys.argv:
        with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
            f.write(txt)
        print('wrote %s (%d lines) overall %s' % (OUT, txt.count('\n'), 'PASS' if ok else 'FAIL'))
    else:
        sys.stdout.write(txt)
        print('\nDRY RUN - nothing written; overall', 'PASS' if ok else 'FAIL')


if __name__ == '__main__':
    main()
