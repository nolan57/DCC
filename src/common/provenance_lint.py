#!/usr/bin/env python3
"""
Provenance linter for the DCC repository.

Implements rules P1-P6 of docs/conventions/provenance_tags_v1.md, which encodes
governor ruling D-A: boundary data (S3->S4 branch) is admissible into the S0->S2
solve but never into the S0->S2 validation ledger.

This is a REPORT: it emits no physics verdict, licenses no visibility conclusion,
and always exits 0. G-64-01 removed the last veto: even VIOLATION rows are recorded facts,
not a "do not commit". The surviving hard constraint is result-class honesty, which is
checked against the product's own registration, not by this linter.

Verdict classes
  OK               tag present and consistent with location
  MISSING          no PROVENANCE line (post-cutoff product)  -> must be added
  VIOLATION        branch file claiming CHAIN-EVIDENCE (P2); or an exempt file that was edited (P9)
  DRIFT-OBSERVED   P8 lock digest changed but a registered *drift*.json explains the exact
                   recorded->observed pair (G-64-01): a fact, not a violation; never re-sealed
  INCOMPLETE       BOUNDARY-INPUT without TYPE / OVERDETERMINATION / DERIVATION (P4)
  RECONSTRUCTION   BOUNDARY-INPUT whose surplus <= 0 -- legal, but may not be
                   reported as validation (P4)
  LEGACY-UNTAGGED  product dated before the cutoff (P6) -- not edited, not a defect
  LOCKED-ARTIFACT  hash-locked declaration (P8) -- digest verified, cannot be annotated
  EXEMPT-LEGACY    named in provenance_exemption_bn04.txt with a matching digest (P9) --
                   non-blocking, and deliberately NOT "OK": no tag exists
  N/A              documentation file, not a run product

Grandfathering is by MANIFEST, not by date: runs/CONVENTIONS/provenance_baseline.txt
freezes the inventory at the moment the convention was adopted. A file in the
baseline is grandfathered byte-identical (s9.1); a file outside it must be tagged.
Dates are unreliable here because the whole repository was written within two days.

BN-04 (2026-11-23) added a SECOND, closed manifest for twelve products that were written
around adoption but are absent from the frozen baseline, and that cannot be tagged without
being edited. P9 honours it only while its own digest verifies: the exemption cannot be
extended, because extending it breaks the sidecar and voids the whole list.
"""
import hashlib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUNS = os.path.join(ROOT, 'runs')
BASELINE = os.path.join(RUNS, 'CONVENTIONS', 'provenance_baseline.txt')
EXEMPT = os.path.join(RUNS, 'CONVENTIONS', 'provenance_exemption_bn04.txt')
BRANCH_DIRS = ('S45',)          # + any dir starting with 'S4'
TAGS = ('CHAIN-EVIDENCE', 'BOUNDARY-INPUT', 'NEITHER')
REQUIRED_BOUNDARY_FIELDS = ('TYPE', 'OVERDETERMINATION', 'DERIVATION')
SKIP_DIRS = ('.mimosa', '__pycache__', '.git')

# Files that are registrations or conventions rather than run products.
DOC_PATTERNS = (r'_registration\.md$', r'\.md$')
PRODUCT_EXT = ('.txt', '.log', '.csv', '.json', '.npz', '.png')

TAG_RE = re.compile(r'PROVENANCE:\s*([A-Z\-]+)')
TYPE_RE = re.compile(r'^\s*TYPE:', re.M)
OVER_RE = re.compile(r'OVERDETERMINATION:.*?surplus\s*=\s*(-?\d+)', re.S)
DERIV_RE = re.compile(r'^\s*DERIVATION:', re.M)
DATE_RE = re.compile(r'20\d\d-\d\d-\d\d')


def load_baseline():
    if not os.path.exists(BASELINE):
        return set()
    out = set()
    with open(BASELINE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                out.add(line.replace('\\', '/'))
    return out


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for ch in iter(lambda: f.read(65536), b''):
            h.update(ch)
    return h.hexdigest()


def load_exemption(path=None):
    """P9. Returns (dict path->digest, valid_flag, detail).

    The manifest is honoured ONLY while its own digest matches its sidecar. That is the
    closure property: adding a thirteenth line changes the manifest, breaks the sidecar,
    and voids every line in it. An exemption that can be extended is not an exemption.
    """
    path = path or EXEMPT
    if not os.path.exists(path):
        return {}, False, 'no exemption manifest'
    side = path + '.sha256'
    if not os.path.exists(side):
        return {}, False, 'exemption manifest has no .sha256 sidecar -> NOT honoured'
    rec = (read(side).split() or [''])[0].strip().lower()
    got = sha256_file(path)
    if not rec or rec != got:
        return {}, False, ('exemption manifest digest mismatch %s != %s -> list VOID (P9)'
                           % (rec[:12], got[:12]))
    out = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if len(parts) >= 2:
                out[parts[-1].replace('\\', '/')] = parts[0].lower()
    return out, True, '%d entries, digest verified' % len(out)


def is_branch(rel):
    parts = rel.replace('\\', '/').split('/')
    for p in parts:
        if p in BRANCH_DIRS or p.startswith('S4'):
            return True
    return False


def load_drifts(root=None):
    """G-64-01: registered drift observations keyed by target path.

    A *drift*.json is a parallel observation object. It explains a P8 lock digest change
    without re-sealing the locked original; the matched pair reads as DRIFT-OBSERVED.
    """
    root = root or ROOT
    out = {}
    for dirpath, dirnames, filenames in os.walk(os.path.join(root, 'runs')):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        for fn in sorted(filenames):
            if 'drift' not in fn.lower() or not fn.lower().endswith('.json'):
                continue
            try:
                d = json.loads(read(os.path.join(dirpath, fn)))
            except (ValueError, OSError):
                continue
            if not isinstance(d, dict) or not d.get('target'):
                continue
            out.setdefault(d['target'].replace('\\', '/'), []).append({
                'recorded': (d.get('recorded_digest') or '').lower(),
                'observed': (d.get('observed_digest') or '').lower(),
                'id': d.get('drift_id', fn),
            })
    return out


def read(path):
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except OSError:
        return ''


def classify(path, rel, baseline, exempt=None, exempt_ok=False, root=None):
    """Return (verdict, detail)."""
    root = root or ROOT
    exempt = exempt or {}
    if os.path.basename(path) in ('provenance_baseline.txt', 'provenance_lint_results.txt'):
        return 'N/A', 'linter machinery (manifest / this report)'
    if not path.lower().endswith(PRODUCT_EXT):
        return 'N/A', 'not a run product'

    txt = read(path)
    # P8: a hash-locked declaration cannot be annotated. Any PROVENANCE comment would change the
    # digest, and the digest is the only thing that proves the declaration preceded the data. So a
    # sidecar digest stands in for the tag -- but ONLY when it matches the file, which is strictly
    # stronger evidence than a comment (a comment proves nothing about whether the file was edited;
    # a matching digest proves it was not). A mismatch is a VIOLATION.
    side = path + '.sha256'
    if os.path.exists(side):
        rec = (read(side).split() or [''])[0].strip().lower()
        h = hashlib.sha256()
        with open(path, 'rb') as fh:
            for ch in iter(lambda: fh.read(65536), b''):
                h.update(ch)
        if rec and rec == h.hexdigest():
            return 'LOCKED-ARTIFACT', 'hash-locked (P8); digest verified, cannot be annotated'
        for d in load_drifts(root).get(rel.replace('\\', '/'), []):
            if (d['recorded'] and rec.startswith(d['recorded']) and
                    d['observed'] and h.hexdigest().startswith(d['observed'])):
                return ('DRIFT-OBSERVED',
                        'P8 digest drift %s -> %s explained by [%s]; fact, not a violation (G-64-01)'
                        % (rec[:12], h.hexdigest()[:12], d['id']))
        return 'VIOLATION', 'lock digest mismatch %s != %s (P8)' % (rec[:12], h.hexdigest()[:12])
    # P7: a binary product cannot carry a text line. Its declaration lives in the sidecar
    # `<file>.display.txt` written by display_conventions_v1, which already has a PROVENANCE field.
    if path.lower().endswith(('.png', '.jpg', '.jpeg', '.npz', '.npy', '.pdf', '.mp4')):
        side = path + '.display.txt'
        if os.path.exists(side):
            return _classify_text(read(side), rel, baseline, via='sidecar',
                                  exempt=exempt, exempt_ok=exempt_ok, root=root)
        if rel.replace('\\', '/') in baseline:
            return 'LEGACY-UNTAGGED', 'pre-convention binary in baseline; not edited (P6)'
        return 'MISSING', 'binary product without a .display.txt sidecar (P7)'
    # tags may sit in the banner or in a closing block; scan the whole file, but
    # only on a line of their own (a mention inside prose is not a declaration).
    return _classify_text(txt, rel, baseline, via='inline', exempt=exempt, exempt_ok=exempt_ok,
                          root=root)


def _classify_text(txt, rel, baseline, via='inline', exempt=None, exempt_ok=False, root=None):
    root = root or ROOT
    m = TAG_RE.search(txt)
    branch = is_branch(rel)
    key = rel.replace('\\', '/')
    exempt = exempt or {}

    if not m:
        if key in baseline:
            return 'LEGACY-UNTAGGED', 'in baseline manifest; not edited (P6)'
        # P9: a named exemption is honoured only while the manifest's own digest verifies AND
        # the file still matches the digest recorded for it. An edited "exempt" file is the one
        # thing this mechanism must not tolerate -- that would launder new text under an old name.
        if key in exempt:
            if not exempt_ok:
                return 'MISSING', 'listed in the P9 exemption, but the list is VOID (digest)'
            got = sha256_file(os.path.join(root, key))
            if got == exempt[key]:
                return 'EXEMPT-LEGACY', 'named exemption BN-04; digest verified, cannot be tagged (P9)'
            return 'VIOLATION', ('exempt file edited after exemption %s != %s (P9)'
                                 % (exempt[key][:12], got[:12]))
        return 'MISSING', 'no PROVENANCE line anywhere (%s) (P1)' % via

    tag = m.group(1)
    if tag not in TAGS:
        return 'VIOLATION', 'unknown tag %r' % tag

    if branch and tag == 'CHAIN-EVIDENCE':
        return 'VIOLATION', 'branch product claims CHAIN-EVIDENCE (P2)'

    if tag == 'BOUNDARY-INPUT':
        missing = [f for f in REQUIRED_BOUNDARY_FIELDS
                   if not {'TYPE': TYPE_RE, 'OVERDETERMINATION': OVER_RE,
                           'DERIVATION': DERIV_RE}[f].search(txt)]
        if missing:
            return 'INCOMPLETE', 'BOUNDARY-INPUT lacks %s (P4)' % ', '.join(missing)
        mo = OVER_RE.search(txt)
        if mo and int(mo.group(1)) <= 0:
            return 'RECONSTRUCTION', 'surplus <= 0: report as reconstruction, not validation'
    return 'OK', tag


def main():
    baseline = load_baseline()
    exempt, exempt_ok, exempt_detail = load_exemption()
    rows = []
    for dirpath, dirnames, filenames in os.walk(RUNS):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith('.')]
        for fn in sorted(filenames):
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT)
            verdict, detail = classify(path, rel, baseline, exempt, exempt_ok)
            rows.append((verdict, rel, detail))

    order = ['VIOLATION', 'MISSING', 'INCOMPLETE', 'DRIFT-OBSERVED', 'RECONSTRUCTION',
             'EXEMPT-LEGACY', 'OK', 'LOCKED-ARTIFACT', 'LEGACY-UNTAGGED', 'N/A']
    rows.sort(key=lambda r: (order.index(r[0]), r[1]))

    print("=" * 78)
    print("PROVENANCE LINT  (rules P1-P9, docs/conventions/provenance_tags_v1.md)")
    print("=" * 78)
    print("  scope: runs/  ;  grandfathering: manifest (%d entries)  ;  branch dirs: %s"
          % (len(baseline), ', '.join(BRANCH_DIRS)))
    print("  exemption (P9, BN-04): %s" % exempt_detail)
    print("  report only (G-64-01): no physics verdict, no veto, exit code always 0")
    print()

    tally = {k: 0 for k in order}
    for verdict, rel, detail in rows:
        tally[verdict] += 1

    for verdict in order:
        sel = [r for r in rows if r[0] == verdict]
        if not sel:
            continue
        print("-" * 78)
        print("[%s]  %d file(s)" % (verdict, len(sel)))
        print("-" * 78)
        if verdict == 'N/A':
            print("  (documentation; not itemised)")
            print()
            continue
        for _v, rel, detail in sel:
            print("  %-58s %s" % (rel.replace('\\', '/'), detail))
        print()

    print("=" * 78)
    print("[tally]")
    for k in order:
        if tally[k]:
            print("  %-18s %d" % (k, tally[k]))
    print()
    flagged = tally['VIOLATION'] + tally['MISSING'] + tally['INCOMPLETE']
    print("  flagged (VIOLATION + MISSING + INCOMPLETE) = %d  [facts; no veto since G-64-01]" % flagged)
    print("  drift observations (DRIFT-OBSERVED)        = %d" % tally['DRIFT-OBSERVED'])
    print("  informational (RECONSTRUCTION)             = %d" % tally['RECONSTRUCTION'])
    print("  grandfathered (LEGACY-UNTAGGED)            = %d" % tally['LEGACY-UNTAGGED'])
    print("  exempted      (EXEMPT-LEGACY, P9)          = %d" % tally['EXEMPT-LEGACY'])
    print()
    print("  Since G-64-01 no tally here blocks emission or registration. A VIOLATION still")
    print("  flags a branch product promoted to chain evidence (ruling D-A) as a FACT to record.")
    print()
    print("PROVENANCE: NEITHER  (convention enforcement report; establishes nothing)")
    print()
    print("Content generated by AI")


def selftest():
    """P9 negative tests. An exemption must be unobtainable by editing, extending or omitting.

    Five cases, run on a throwaway tree: the exemption is honoured only for a byte-identical
    file, only while the manifest's own digest verifies, and it never shadows a real tag.
    """
    import shutil
    import tempfile

    tmp = tempfile.mkdtemp(prefix='prov9_')
    fails = []
    try:
        os.makedirs(os.path.join(tmp, 'runs', 'X'))
        a = os.path.join(tmp, 'runs', 'X', 'a.txt')
        b = os.path.join(tmp, 'runs', 'X', 'b.txt')
        for p, s in ((a, 'alpha\n'), (b, 'beta\n')):
            with open(p, 'w', encoding='utf-8') as f:
                f.write(s)
        man = os.path.join(tmp, 'runs', 'X', 'exempt.txt')
        with open(man, 'w', encoding='utf-8') as f:
            for p in (a, b):
                f.write('%s  %s\n' % (sha256_file(p), os.path.relpath(p, tmp).replace('\\', '/')))
        with open(man + '.sha256', 'w', encoding='utf-8') as f:
            f.write(sha256_file(man) + '\n')

        def run(label, want_a, mutate=None, drop_side=False):
            if mutate:
                mutate()
            ex, ok, _d = load_exemption(man)
            got_a = _classify_text(read(a), os.path.relpath(a, tmp), set(), exempt=ex,
                                   exempt_ok=ok, root=tmp)[0]
            got_b = _classify_text(read(b), os.path.relpath(b, tmp), set(), exempt=ex,
                                   exempt_ok=ok, root=tmp)[0]
            good = (got_a == want_a)
            print("  %-46s a=%-14s b=%-14s %s" % (label, got_a, got_b, 'PASS' if good else 'FAIL'))
            if not good:
                fails.append(label)

        run('clean manifest, untouched files', 'EXEMPT-LEGACY')
        run('one file edited by one byte', 'VIOLATION',
            mutate=lambda: open(a, 'a', encoding='utf-8').write('x'))
        run('a thirteenth line appended to the manifest', 'MISSING',
            mutate=lambda: open(man, 'a', encoding='utf-8').write(
                '%s  runs/X/c.txt\n' % ('0' * 64)))
        run('sidecar deleted', 'MISSING',
            mutate=lambda: os.remove(man + '.sha256'))
        # precedence: a real tag is never shadowed by an exemption
        got = _classify_text(read(a) + 'PROVENANCE: NEITHER\n', os.path.relpath(a, tmp), set(),
                             exempt={os.path.relpath(a, tmp): 'x'}, exempt_ok=True, root=tmp)[0]
        print("  %-46s a=%-14s %s" % ('a tagged exempt file reads as its tag', got,
                                      'PASS' if got == 'OK' else 'FAIL'))
        if got != 'OK':
            fails.append('tag precedence')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    print("  P9 SELFTEST: %s" % ('PASS -- 5/5' if not fails else 'FAIL on %s' % fails))
    return 0 if not fails else 1


if __name__ == '__main__':
    if '--selftest' in os.sys.argv:
        os.sys.exit(selftest())
    main()
