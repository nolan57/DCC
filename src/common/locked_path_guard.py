#!/usr/bin/env python
"""
LOCKED-PATH guard -- enforces S9(c): an unlocked rename must not change the computation path of a
locked quantity.

S9 has two scopes (docs/conventions/symbol_registry.md s5, S9):
  (a) symbols covered by a document's own sha256 are frozen; renaming them is not permitted;
  (b) every other symbol may be renamed freely;
  (c) but (b) must not move a locked number's computation path.

Clause (c) is a sentence until something measures it.  This does.  It records the pair

    (digest of src/route/structure_tiers.py, digest of runs/MATRIX/structure_tiers_results.txt)

and the admissible verdicts are:

    OK               source and numbers both unchanged -- nothing happened
    RENAME-ADMITTED  source moved, numbers identical   -- the signature of a rename or a comment edit
    DRIFT            source unchanged, numbers moved   -- the environment moved, not the code
    BLOCK            both moved                        -- a locked quantity's value changed; needs a new lock

`RENAME-ADMITTED` is deliberately not a free pass: it says the numbers must be re-baselined with a note,
so a rename cannot smuggle a value change through in two commits (rename now, tweak later).

Usage
    python src/common/locked_path_guard.py                 # check
    python src/common/locked_path_guard.py --record        # (re)baseline, prints why it is allowed
    python src/common/locked_path_guard.py --source P --results Q   # test on copies
"""
import argparse
import hashlib
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASELINE = os.path.join(ROOT, 'runs', 'MATRIX', 'locked_path_digest.json')
DEF_SRC = os.path.join(ROOT, 'src', 'route', 'structure_tiers.py')
DEF_RES = os.path.join(ROOT, 'runs', 'MATRIX', 'structure_tiers_results.txt')


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def check(src, res, base):
    if not base:
        return 'NO-BASELINE', 'no baseline recorded; run --record once, before any rename'
    s_ok = sha_file(src) == base['source_sha256']
    r_ok = sha_file(res) == base['results_sha256']
    if s_ok and r_ok:
        return 'OK', 'source and numbers unchanged'
    if (not s_ok) and r_ok:
        return 'RENAME-ADMITTED', 'source text moved, the 4x9 numbers did not -> permitted by S9(c); re-baseline with a note'
    if s_ok and (not r_ok):
        return 'DRIFT', 'numbers moved with the source unchanged -> environment/dependency, not a rename'
    return 'BLOCK', 'both moved -> a locked quantity changed value; S9(a) requires a new lock, not a commit'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--record', action='store_true')
    ap.add_argument('--source', default=DEF_SRC)
    ap.add_argument('--results', default=DEF_RES)
    a = ap.parse_args()

    src = os.path.abspath(a.source)
    res = os.path.abspath(a.results)
    for p in (src, res):
        if not os.path.exists(p):
            print('REFUSED: missing %s' % p)
            return 1

    base = None
    if os.path.exists(BASELINE):
        with open(BASELINE, encoding='utf-8') as f:
            base = json.load(f)

    if a.record:
        why = check(src, res, base)[0] if base else 'first baseline'
        rec = {
            'recorded_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'source_path': os.path.relpath(src, ROOT),
            'source_sha256': sha_file(src),
            'results_path': os.path.relpath(res, ROOT),
            'results_sha256': sha_file(res),
            'admission': why,
            'locked_symbols': ['Q0', 'Q1', 'Q2', 'Q3'],
            'rule': 'docs/conventions/symbol_registry.md S9(a)(b)(c)',
            'note': 'Numbers may be re-baselined only when RENAME-ADMITTED: source moved, numbers identical.',
        }
        with open(BASELINE, 'w', encoding='utf-8') as f:
            json.dump(rec, f, indent=2)
            f.write('\n')
        with open(BASELINE + '.sha256', 'w', encoding='utf-8') as f:
            f.write(sha_file(BASELINE) + '\n')
        print('recorded baseline: %s' % os.path.relpath(BASELINE, ROOT))
        print('  admission : %s' % why)
        print('  source    : %s' % rec['source_sha256'][:32] + '...')
        print('  results   : %s' % rec['results_sha256'][:32] + '...')
        return 0

    v, d = check(src, res, base)
    print('LOCKED-PATH guard -- S9(c)')
    print('  source    : %s' % os.path.relpath(src, ROOT))
    print('  results   : %s' % os.path.relpath(res, ROOT))
    if base:
        print('  baseline  : %s  (admission: %s)' % (base['recorded_at'], base['admission']))
        print('  source    : %s' % ('match' if sha_file(src) == base['source_sha256'] else 'MOVED'))
        print('  numbers   : %s' % ('match' if sha_file(res) == base['results_sha256'] else 'MOVED'))
    print('  verdict   : %s  -- %s' % (v, d))
    return 1 if v == 'BLOCK' else 0


if __name__ == '__main__':
    sys.exit(main())
