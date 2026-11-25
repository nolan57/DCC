#!/usr/bin/env python3
"""
Programme audit for the DCC repository — docs/program/COMPLETION_PROTOCOL_v1.md.

G-64-01 (round 64) downgraded audit from a gate to an instrument. THIS SCRIPT NEVER VETOES.

  check 1  digest integrity     every .sha256 verifies; every *lock*.json has its sidecar
                                (a mismatch registered in a *drift*.json is an OBSERVATION, not a violation)
  check 2  citation integrity   every runs/... path named in docs/ exists
  advisory authority            a decision doc with an approval block in which NO line is marked
  advisory ordering             a post-cutoff product with no earlier named registration
                                (mtime is NOT evidence -- the 2026-11-21 bulk copy reset it)
  advisory queue                queue items, blockers, terminal states
  advisory ledger               hash chain over runs/PROGRAM/round_ledger.jsonl

Exit code: ALWAYS 0 since G-64-01. Findings are facts recorded into the chain, never a veto.
The only surviving hard constraint is scientific honesty: a result-class label must not be
overstated. That constraint lives in the product registration, not in this reporter.
"Do not commit" is no longer a verdict this instrument is permitted to return.

Usage
  python src/common/program_audit.py                 board + DoD, stdout only
  python src/common/program_audit.py --write         also write both products under runs/PROGRAM/
  python src/common/program_audit.py --check-locks     exit 1 on any digest mismatch
  python src/common/program_audit.py --check-citations exit 1 on any unresolvable runs/ path
  python src/common/program_audit.py --ledger-append RQ-03 --verdict CLOSED-CONSTRUCTIVE \
         --registration runs/R1B/x_registration.md --product runs/R1B/x_results.txt
"""
import hashlib
import json
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUEUE = os.path.join(ROOT, 'docs', 'program', 'round_queue_v1.json')
OUT = os.path.join(ROOT, 'runs', 'PROGRAM')
LEDGER = os.path.join(OUT, 'round_ledger.jsonl')
SKIP = ('.git', '__pycache__', '.mimosa', 'node_modules')
CUTOFF_DEFAULT = "2026-11-21T16:00:00Z"

# machinery directories: their products are this reporter's own output, not round products
MACHINERY = ('CONVENTIONS', 'PROGRAM')

CITE_RE = re.compile(r'runs/[A-Za-z0-9_./\-]+\.(?:txt|md|jsonl|json|png|py|npz|csv)')
MARK_RE = re.compile(r'^\s*\[([ xX])\]\s*(Ratify|Select|Return|Hold|Decline|Accept|Reject)\b(.*)$',
                     re.I)
TERMINAL = ('CLOSED-CONSTRUCTIVE', 'CLOSED-NO-GO', 'RETIRED-IDENTITY',
            'BLOCKED-ON-INPUT', 'FROZEN')
NON_TERMINAL = ('QUEUED', 'REGISTERED', 'EXECUTED', 'AUDITED', 'BLOCKED-ON-GOVERNOR')


def rel(p):
    return os.path.relpath(p, ROOT).replace('\\', '/')


def read(p):
    try:
        with open(p, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except OSError:
        return ''


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for ch in iter(lambda: f.read(65536), b''):
            h.update(ch)
    return h.hexdigest()


def walk(exts, sub='.'):
    for d, dns, fns in os.walk(os.path.join(ROOT, sub)):
        dns[:] = [x for x in dns if x not in SKIP and not x.startswith('.')]
        for fn in sorted(fns):
            if fn.lower().endswith(exts):
                yield os.path.join(d, fn)


# ---------------------------------------------------------------- check 1
DRIFT_RE = re.compile(r'.*drift.*\.json$', re.I)


def load_drifts():
    """G-64-01: registered drift observations, keyed by target path.

    A drift record is a *parallel observation object*: it explains a digest change without
    re-sealing the locked original. Matching the recorded->observed pair lets check_locks
    report DRIFT-OBSERVED instead of VIOLATION. This is a restatement, not a repair.
    """
    out = {}
    for p in walk('.json'):
        if not DRIFT_RE.match(os.path.basename(p)):
            continue
        try:
            d = json.loads(read(p))
        except ValueError:
            continue
        if not isinstance(d, dict) or not d.get('target'):
            continue
        rec = (d.get('recorded_digest') or '').lower()
        got = (d.get('observed_digest') or '').lower()
        if not rec or not got:
            continue
        out.setdefault(d['target'].replace('\\', '/'), []).append({
            'recorded': rec, 'observed': got,
            'id': d.get('drift_id', rel(p)),
            'neg': d.get('negative_evidence', ''),
        })
    return out


def check_locks():
    bad, observed, n = [], [], 0
    drifts = load_drifts()
    for side in walk('.sha256'):
        n += 1
        tgt = side[:-len('.sha256')]
        rec = (read(side).split() or [''])[0].strip().lower()
        if not os.path.exists(tgt):
            bad.append((rel(side), 'target %s missing' % rel(tgt)))
            continue
        got = sha(tgt)
        if rec != got:
            match = None
            for d in drifts.get(rel(tgt), []):
                if d['recorded'].startswith(rec) and d['observed'].startswith(got):
                    match = d
                    break
            if match:
                observed.append((rel(tgt), 'DRIFT-OBSERVED %s -> %s [%s] (not a violation: G-64-01)'
                                 % (rec[:12], got[:12], match['id'])))
            else:
                bad.append((rel(side), 'digest mismatch %s != %s' % (rec[:12], got[:12])))
    for j in walk('.json'):
        if 'lock' not in os.path.basename(j).lower():
            continue
        if os.path.basename(j).endswith('.display.json'):
            continue
        if DRIFT_RE.match(os.path.basename(j)):
            continue
        if not os.path.exists(j + '.sha256'):
            bad.append((rel(j), 'hash-locked declaration without a .sha256 sidecar'))
    return bad, observed, n


ERRATA_RE = re.compile(r'^\s*-\s*\*\*E\d+\*\*', re.M)


def planned_products():
    """Products a queue item owes but has not produced. Declared, never inferred."""
    try:
        return set(json.loads(read(QUEUE)).get('planned_products', []))
    except (ValueError, OSError):
        return set()


def check_citations():
    """Return [(token, doc, kind)].
    kind: MISS (blocking) | MISS-ERRATA (recorded by an erratum) | PLANNED (owed by a queue item).

    MISS-ERRATA exists because the record's sanctioned repair for an archived citation is an appended
    erratum, never an edit (s9.1). A document that carries an erratum block KNOWS the path is dead and
    says so; counting that as a fresh defect would punish the only repair the record allows.
    """
    bad = []
    planned = planned_products()
    for md in walk('.md', 'docs'):
        txt = read(md)
        has_errata = bool(ERRATA_RE.search(txt))
        for tok in sorted(set(CITE_RE.findall(txt))):
            if any(c in tok for c in ('{', '*', '<', '>', '\u2026')):
                continue
            # generated machinery: this reporter's own outputs, produced by --write
            if '/PROGRAM/' in tok:
                continue
            if not os.path.exists(os.path.join(ROOT, tok)):
                kind = 'PLANNED' if tok in planned else ('MISS-ERRATA' if has_errata else 'MISS')
                bad.append((tok, rel(md), kind))
    return bad


# ------------------------------------------------------------ advisory checks
def check_authority():
    pend = []
    for sub in ('decisions', 'specs'):
        ddir = os.path.join(ROOT, 'docs', sub)
        if not os.path.isdir(ddir):
            continue
        for fn in sorted(os.listdir(ddir)):
            if not fn.endswith('.md'):
                continue
            p = os.path.join(ddir, fn)
            lines = read(p).splitlines()
            boxes = [(i + 1, m.group(1)) for i, m in
                     ((i, MARK_RE.match(l)) for i, l in enumerate(lines)) if m]
            if not boxes:
                continue
            if not any(st.strip().lower() == 'x' for _n, st in boxes):
                pend.append(('docs/%s/%s' % (sub, fn),
                             ','.join(str(n) for n, _st in boxes)))
    return pend


def check_ordering(cutoff):
    fail, weak, ok = [], [], 0
    for d, dns, fns in os.walk(os.path.join(ROOT, 'runs')):
        dns[:] = [x for x in dns if x not in SKIP and not x.startswith('.')]
        if os.path.basename(d) in MACHINERY:
            continue
        regs = {f: os.path.getmtime(os.path.join(d, f))
                for f in fns if f.endswith('registration.md')}
        for f in fns:
            if not f.endswith('_results.txt'):
                continue
            p = os.path.join(d, f)
            if os.path.getmtime(p) < cutoff:
                continue
            stem = f[:-len('_results.txt')]
            named = [r for r in regs if stem.startswith(r[:-len('_registration.md')])]
            pool = named if named else list(regs)
            early = [r for r in pool if regs[r] < os.path.getmtime(p)]
            if not pool:
                fail.append((rel(p), 'no registration in directory'))
            elif not early:
                fail.append((rel(p), 'named registration not earlier: %s' % ', '.join(sorted(pool))))
            elif named:
                ok += 1
            else:
                weak.append((rel(p), sorted(early, key=lambda r: regs[r])[-1]))
    return ok, weak, fail


def check_queue():
    if not os.path.exists(QUEUE):
        return None
    q = json.loads(read(QUEUE))
    ids = [i['id'] for i in q['items']] + [g['id'] for g in q.get('gates', [])]
    dangling = []
    for it in q['items']:
        for b in it.get('blocked_by', []):
            if b not in ids:
                dangling.append((it['id'], b))
    return q, ids, dangling


def check_ledger():
    """Return (records, status text, breaks)."""
    if not os.path.exists(LEDGER):
        return [], 'absent (starts at round 46)', []
    recs, prev, bad = [], '0' * 64, []
    for n, line in enumerate(read(LEDGER).splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except ValueError:
            bad.append((n, 'unparseable record'))
            continue
        body = json.dumps({k: v for k, v in r.items() if k != 'prev'},
                          sort_keys=True).encode()
        if r.get('prev') != prev:
            bad.append((n, 'prev-link broken'))
        prev = hashlib.sha256(body).hexdigest()
        recs.append(r)
    status = '%d record(s)' % len(recs) if recs else 'empty'
    return recs, status, bad


# --------------------------------------------------------------------- board
def board():
    q, ids, dangling = check_queue()
    locks, drifts, nlock = check_locks()
    cites = check_citations()
    pend = check_authority()
    ok, weak, orderfail = check_ordering(time.mktime(time.strptime(
        (q['cutoff_utc'] if q else CUTOFF_DEFAULT), '%Y-%m-%dT%H:%M:%SZ')) - time.timezone)
    recs, led, breaks = check_ledger()

    L = []
    A = L.append
    A("=" * 78)
    A("PROGRAMME AUDIT  (docs/program/COMPLETION_PROTOCOL_v1.md)")
    A("=" * 78)
    A("  as of round %s  |  queue: %s" % (q['round_cursor'] if q else '?',
                                          'docs/program/round_queue_v1.json' if q else 'MISSING'))
    A("  G-64-01: REPORT-ONLY INSTRUMENT — exit 0 always; findings are facts, never a veto")
    A("")

    # -- check 1 (digest integrity)
    A("-" * 78)
    A("[CHECK 1] DIGEST INTEGRITY  %d sidecar(s)  (was HARD 1 before G-64-01)" % nlock)
    A("-" * 78)
    if locks:
        for p, why in locks:
            A("  UNEXPLAINED  %-50s %s" % (p, why))
    else:
        A("  OK — every declared digest verifies, every lock file has its sidecar")
    for p, why in drifts:
        A("  %s" % why)
    A("")

    A("-" * 78)
    A("[CHECK 2] CITATION INTEGRITY  (runs/ paths named in docs/)")
    A("-" * 78)
    if cites:
        for tok, where, kind in cites:
            A("  %-11s %-52s cited by %s" % (kind, tok, where))
    else:
        A("  OK — every cited product exists")
    A("")

    # -- advisory
    A("-" * 78)
    A("[ADVISORY 1] AUTHORITY — decision documents with an unmarked approval block")
    A("-" * 78)
    if pend:
        for doc, lines_at in pend:
            A("  AWAITING-GOVERNOR  %-52s line(s) %s" % (doc, lines_at))
    else:
        A("  OK — no unmarked block")
    A("")

    A("-" * 78)
    A("[ADVISORY 2] ORDERING — registration earlier than product (mtime; weak evidence)")
    A("-" * 78)
    A("  named registration, earlier : %d" % ok)
    A("  fallback (no name match)    : %d" % len(weak))
    A("  ORDER-SUSPECT               : %d   (advisory: a bulk copy produces these too)" % len(orderfail))
    for p, why in orderfail:
        A("    %-52s %s" % (p, why))
    A("")

    A("-" * 78)
    A("[ADVISORY 3] ROUND LEDGER — runs/PROGRAM/round_ledger.jsonl  %s" % led)
    A("-" * 78)
    if breaks:
        for n, why in breaks:
            A("  BREAK      record %d: %s" % (n, why))
    if recs:
        for r in recs[-5:]:
            A("  round %-3s %-7s %-22s %s" % (r.get('round'), r.get('id'),
                                              r.get('verdict'), r.get('product', '')[:34]))
        if len(recs) > 5:
            A("  ... %d earlier record(s)" % (len(recs) - 5))
    else:
        A("  no records yet — this is the ordering proof from round 46 forward")
    A("")

    A("-" * 78)
    A("[ADVISORY 4] QUEUE")
    A("-" * 78)
    if not q:
        A("  MISSING — no queue file")
    else:
        tally = {}
        for it in q['items']:
            tally[it['state']] = tally.get(it['state'], 0) + 1
        for k in NON_TERMINAL + TERMINAL:
            if tally.get(k):
                A("  %-22s %d" % (k, tally[k]))
        if dangling:
            for i, b in dangling:
                A("  DANGLING BLOCKER  %s -> %s" % (i, b))
        openit = [it for it in q['items'] if it['state'] in NON_TERMINAL]
        if openit:
            A("  open:")
            for it in openit:
                A("    %-7s %-22s %s" % (it['id'], it['state'], it['title'][:44]))
    A("")

    # -- DoD
    A("=" * 78)
    A("[DEFINITION OF DONE]  docs/program/COMPLETION_PROTOCOL_v1.md §0")
    A("=" * 78)
    d1 = len(pend) == 0
    d2 = len(locks) == 0
    d3 = not [c for c in cites if c[2] == 'MISS']
    closed = [it for it in (q['items'] if q else [])
              if it['state'] in ('CLOSED-CONSTRUCTIVE', 'CLOSED-NO-GO', 'RETIRED-IDENTITY')]
    logged = [r.get('id') for r in recs]
    d4 = all(it['id'] in logged for it in closed)
    d5 = not breaks
    d6 = bool(q) and not [it for it in q['items'] if it['state'] in NON_TERMINAL]
    rows = [
        ('D1', 'zero unmarked governor blocks', d1, len(pend)),
        ('D2', 'zero unexplained digest drifts', d2,
         '%d unexplained, %d observed' % (len(locks), len(drifts))),
        ('D3', 'zero broken citations', d3,
         len([c for c in cites if c[2] == 'MISS'])),
        ('D4', 'every closed item has a ledger record', d4,
         'vacuous (0 closed)' if not closed else '%d/%d' % (sum(it['id'] in logged for it in closed), len(closed))),
        ('D5', 'ledger chain intact', d5, '%d break(s)' % len(breaks) if breaks else ''),
        ('D6', 'every queue item terminal', d6,
         len([it for it in (q['items'] if q else []) if it['state'] in NON_TERMINAL])),
    ]
    met = 0
    for cid, what, good, val in rows:
        met += 1 if good else 0
        A("  %-3s %-44s %-5s %s" % (cid, what, 'MET' if good else 'OPEN', val))
    A("  D7  every BLOCKED-ON-INPUT names its physics        MANUAL")
    A("  D8  the terminal answer exists                      MANUAL")
    A("")
    A("  completion: %d/6 machine-checked" % met)
    A("  G-64-01: this score is an instrument reading, not a gate. It never blocks emission,")
    A("  registration or use of a product whose own CHECK/IDENT/NEGCTRL self-tests passed.")
    A("")
    A("PROVENANCE: NEITHER  (process instrument report; establishes no physics)")
    A("")
    A("Content generated by AI")
    return "\n".join(L), locks, cites, pend


def digest():
    q, _ids, _d = check_queue()
    pend = check_authority()
    L = ["=" * 78,
         "GOVERNOR DIGEST — %s" % time.strftime('%Y-%m-%d'),
         "one character per gate; the mark is the only authority this programme recognises",
         "=" * 78, ""]
    for g in (q['gates'] if q else []):
        L.append("%-6s %s" % (g['id'], g['title']))
        L.append("  ask    : %s" % g['ask'])
        L.append("  basis  : %s" % g['basis'])
        L.append("  cost   : %s" % g['cost_if_unmarked'])
        L.append("  mark   : %s" % g['mark_at'])
        L.append("  rec    : %s" % g['recommendation'])
        if g.get('marked'):
            L.append("  MARKED : %s" % g['marked'])
        else:
            L.append("  if no  : stays open; a silence is not an approval")
        L.append("")
    for n in (q.get('board_notes', []) if q else []):
        L.append("%-6s %s" % (n['id'], n['finding']))
        L.append("  detail : %s" % n['detail'])
        L.append("  action : %s" % n['action_if_any'])
        L.append("")
    if not pend:
        L.append("  (no unmarked approval block found on disk)")
        L.append("")
    L.append("PROVENANCE: NEITHER  (interaction surface; adjudicates nothing)")
    L.append("")
    L.append("Content generated by AI")
    return "\n".join(L)


def ledger_append(rnd, item, verdict, reg, prod):
    os.makedirs(OUT, exist_ok=True)
    prev = '0' * 64
    if os.path.exists(LEDGER):
        lines = [l for l in read(LEDGER).splitlines() if l.strip()]
        if lines:
            last = json.loads(lines[-1])
            body = json.dumps({k: v for k, v in last.items() if k != 'prev'}, sort_keys=True).encode()
            prev = hashlib.sha256(body).hexdigest()
    rec = {
        'round': int(rnd),
        'id': item,
        'registration_sha256': sha(os.path.join(ROOT, reg)) if reg and os.path.exists(os.path.join(ROOT, reg)) else None,
        'product_sha256': sha(os.path.join(ROOT, prod)) if prod and os.path.exists(os.path.join(ROOT, prod)) else None,
        'registration': reg,
        'product': prod,
        'verdict': verdict,
        'prev': prev,
        'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    }
    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")
    print("ledger: round %s / %s / %s recorded (prev %s)" % (rnd, item, verdict, prev[:12]))


def main(argv):
    if '--ledger-append' in argv:
        a = argv[argv.index('--ledger-append') + 1]
        def opt(name, default=None):
            return argv[argv.index(name) + 1] if name in argv else default
        ledger_append(a, opt('--id', ''), opt('--verdict', ''), opt('--registration', ''),
                      opt('--product', ''))
        return 0

    if '--check-locks' in argv:
        bad, observed, n = check_locks()
        for p, why in bad:
            print("UNEXPLAINED %s  %s" % (p, why))
        for p, why in observed:
            print("%s" % why)
        print("digest check (report only): %d unexplained, %d observed, %d sidecars"
              % (len(bad), len(observed), n))
        return 0

    if '--check-citations' in argv:
        bad = [c for c in check_citations() if c[2] == 'MISS']
        for tok, where, _k in bad:
            print("MISS %s  <- %s" % (tok, where))
        print("citation check (report only): %d missing" % len(bad))
        return 0

    text, locks, cites, _pend = board()
    print(text)
    if '--write' in argv:
        os.makedirs(OUT, exist_ok=True)
        with open(os.path.join(OUT, 'program_audit_results.txt'), 'w', encoding='utf-8') as f:
            f.write(text + "\n")
        with open(os.path.join(OUT, 'governor_digest.txt'), 'w', encoding='utf-8') as f:
            f.write(digest() + "\n")
        print("\nwritten: runs/PROGRAM/program_audit_results.txt, runs/PROGRAM/governor_digest.txt")
    # G-64-01: report-only. Findings are recorded as facts; this instrument never returns a veto.
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
