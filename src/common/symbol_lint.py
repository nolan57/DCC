#!/usr/bin/env python3
"""
Symbol-namespace linter for the DCC repository.

Implements rule S3 of docs/conventions/symbol_registry.md: symbol conflict is a
HARD audit item, not an aspiration.  This is a REPORT: it emits no physics
verdict, licenses no visibility conclusion, and always exits 0.

Verdict classes
  MUST-FIX     active prose where the label is cheap to change and the collision
               is real (docs/, reports/, roadmap)
  ERRATA       source module whose printed labels are baked into an ARCHIVED run
               output. s9.1 forbids rewriting archived stdout, so the fix is a
               registry entry, not an edit.
  ARCHIVE      file under runs/ — never edited
  DEFINITION   the registry itself, which necessarily names what it defines
  (dropped)    token inside a Markdown code span — a MENTION, not a use

Checks
  A  bracket test IDs [C#] [B#] [P#] outside the module that defines them
  B  bare L1..L4 — ADVISORY only, because L is three-way overloaded and the
     R2-D labels are embedded in file paths (see registry s3 item 3)
  C  K1..K4 (K is the trace of the extrinsic curvature)
  D  C_geo / C_phys / C_info / C_top (rule R4)
  E  bare C1..C4 — report only, since C is sole owner after the s6.1 rename
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCAN_DIRS = ['docs', 'reports', 'src', 'runs']
SCAN_FILES = ['Macro3D_to_2D_Smooth_Reduction_Roadmap_v1.4.md']
REGISTRY = os.path.join('docs', 'conventions', 'symbol_registry.md')
SELF = os.path.join('src', 'common', 'symbol_lint.py')   # defines the patterns: DEFINITION
TEST_OWNERS = ('instability_localization.py', 'instability_localization_detail.py',
               'axisym_2p1_evolution.py', 'meff_boundary_probe.py')
# Chain directories: products here are CHAIN-EVIDENCE. An ME label appearing in one
# is an S1 scope bleed (registry S1: the branch may not legislate in the C domain).
CHAIN_DIRS = ('R1A', 'R1B', 'R2', 'R3', 'R4', 'R5', 'G0', 'P1')
# Active texts that must QUOTE rejected labels in order to reject them.
QUOTING = {
    'docs/conventions/symbol_registry.md',
    'src/common/symbol_lint.py',
    'docs/specs/meff_boundary_v0_2_alt_definitions_DECLINED.md',
    'docs/decisions/phased_relaxation_route_v2.md',   # invariant 1 must NAME the retired labels to forbid them
    'reports/reviews/meff_boundary_alt_definitions_review.md',
}
# Roadmap section 6 owns the optics-layer reading of L1..L4.
OPTICS_SECTION = (691, 798)


def masked(line):
    """Blank out inline code spans so quoted labels count as mentions."""
    out, depth = [], 0
    for ch in line:
        if ch == '`':
            depth = 1 - depth
            out.append(' ')
            continue
        out.append(' ' if depth else ch)
    return ''.join(out)


def files():
    for f in SCAN_FILES:
        p = os.path.join(ROOT, f)
        if os.path.isfile(p):
            yield f, p
    for d in SCAN_DIRS:
        for dp, dn, fn in os.walk(os.path.join(ROOT, d)):
            dn[:] = [x for x in dn if x not in ('__pycache__', '.git')]
            for f in fn:
                if f.endswith(('.md', '.py', '.txt')):
                    full = os.path.join(dp, f)
                    yield os.path.relpath(full, ROOT), full


def verdict(rel, is_arch):
    if is_arch:
        return 'ARCHIVE'
    if rel in (REGISTRY, SELF):
        return 'DEFINITION'
    if rel.startswith('src' + os.sep):
        return 'ERRATA'
    return 'MUST-FIX'


def main():
    hits = {k: {} for k in 'ABCDFGH'}
    c_counts = {}
    n = n_arch = 0

    for rel, full in files():
        n += 1
        is_arch = rel.startswith('runs' + os.sep)
        n_arch += is_arch
        try:
            text = open(full, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        base = os.path.basename(rel)
        for ln, line in enumerate(text.split('\n'), 1):
            m = masked(line)
            v = verdict(rel, is_arch)
            rk = rel.replace(os.sep, '/')
            quoting = rk in QUOTING

            if base not in TEST_OWNERS:
                for g in re.finditer(r'\[([CBP])(\d)\]', m):
                    hits['A'].setdefault(v, []).append((rel, ln, g.group(0)))
            # C: a SECOND meaning for K. K1-K4 are legitimate where the sci-fi
            # boundary owns them; the hazard is a rendering/contrast reading.
            if re.search(r'band|pseudo|colou?r|stretch|shadow|contrast', line, re.I):
                for g in re.finditer(r'(?<![A-Za-z_])K([1-9])(?![0-9_])', m):
                    hits['C'].setdefault(v, []).append((rel, ln, g.group(0)))
            if not quoting:
                for g in re.finditer(r'C_(geo|phys|info|top)\b', m):
                    hits['D'].setdefault(v, []).append((rel, ln, g.group(0)))
            # F: the ME namespace (adopted 2026-11-22, ruling D-B).
            #  F1  bare M1..M9 in active text -- ADVISORY only: M1-M4 already have
            #      four pre-existing owners (mass, gate M4, painting modes, metrics)
            #  F2  an ME label inside a CHAIN directory -- S1 scope bleed
            if not quoting:
                for g in re.finditer(r'(?<![A-Za-z_])M([1-9])(?![0-9_])', m):
                    hits['F'].setdefault(v, []).append((rel, ln, g.group(0)))
            # H: ME1 is a DEPRECATED ALIAS of CM5 since 2026-11-22 (GD1 Option B).
            #  Advisory: an obsolete label kept for provenance, not an error in arithmetic.
            #  Archived products are exempt -- their stdout is the record of what was run.
            if not quoting and not is_arch:
                for g in re.finditer(r'(?<![A-Za-z_])ME1(?![0-9\u2032\'])', m):
                    hits['H'].setdefault('ERRATA', []).append((rel, ln, g.group(0)))
            if is_arch and rel.replace(os.sep, '/').split('/')[1] in CHAIN_DIRS:
                for g in re.finditer(r'(?<![A-Za-z_])ME([1-9])(?![0-9])', m):
                    hits['G'].setdefault('SCOPE-BLEED', []).append((rel, ln, g.group(0)))
            if not (rel == SCAN_FILES[0] and OPTICS_SECTION[0] <= ln <= OPTICS_SECTION[1]):
                lhits = re.findall(r'(?<![A-Za-z_])L([1-4])(?![0-9_])', m)
                if lhits:
                    hits['B'].setdefault(v, []).append((rel, ln, len(lhits)))
            if re.search(r'(?<![A-Za-z_])C([1-4])(?![0-9_])', m):
                c_counts[rel] = c_counts.get(rel, 0) + 1

    print("=" * 78)
    print("SYMBOL NAMESPACE LINT  —  rule S3 of docs/conventions/symbol_registry.md")
    print("=" * 78)
    print("files scanned: %d   archived under runs/: %d" % (n, n_arch))
    print("(a label inside backticks is a MENTION and is not counted)")
    print("(the registry file is DEFINITION and is not counted)")

    order = ['MUST-FIX', 'ERRATA', 'ARCHIVE', 'DEFINITION']
    titles = {
        'A': 'bracket test IDs [C#]/[B#]/[P#] outside the defining module',
        'C': 'a SECOND meaning for K in a rendering/contrast context (K1-K4 are owned by the sci-fi boundary)',
        'D': 'C_geo / C_phys / C_info / C_top  (rule R4: subscripts do not rescue a letter)',
        'F': 'bare M1..M9 — ADVISORY: M1-M4 already have FOUR owners (mass, gate M4, painting modes, '
             'abandon-assumption metrics); the ME prefix is mandatory (registry S2/R3, and §2a)',
        'H': 'ME1 — ADVISORY: reconstructed alias of CM5 since GD1 Option B (2026-11-22); '
             'new text writes CM5. Not an arithmetic error; provenance banner only',
    }
    must_total = 0
    for key in 'ACDFH':
        print()
        print("-" * 78)
        print("[%s] %s" % (key, titles[key]))
        for v in order:
            rows = hits[key].get(v, [])
            if not rows:
                continue
            if v == 'MUST-FIX' and key in 'ACD':
                must_total += len(rows)
            print("     %-11s %3d" % (v, len(rows)))
            if v in ('MUST-FIX', 'ERRATA'):
                for rel, ln, tok in rows[:12]:
                    print("        %s:%d  %s" % (rel, ln, tok))
                if len(rows) > 12:
                    print("        ... %d more" % (len(rows) - 12))

    print()
    print("-" * 78)
    print("[B] bare L1..L4 — ADVISORY (L is three-way overloaded; staged, not renamed)")
    tot = sum(len(r) for r in hits['B'].values())
    print("     total line-hits: %d  (optics §6 range excluded as DECLARED)" % tot)
    for v in order:
        rows = hits['B'].get(v, [])
        if not rows:
            continue
        agg = {}
        for rel, ln, k in rows:
            agg[rel] = agg.get(rel, 0) + k
        print("     %-11s %3d line-hits across %d files" % (v, len(rows), len(agg)))
        for rel in sorted(agg, key=lambda r: -agg[r])[:8]:
            print("        %-56s %4d" % (rel[:56], agg[rel]))
    print("     Three meanings: optics layers L1-L4 (§6.2) | R2-D redshift layers")
    print("     L1-L3 (§4, embedded in file paths r2d_l1/l2/l3) | fidelity levels")
    print("     (decision statement, now FL1-FL3). Qualify in all new text.")

    print()
    print("-" * 78)
    print("[E] bare C1..C4 — REPORT ONLY (legal: C is sole owner after the §6.1 rename)")
    for rel in sorted(c_counts, key=lambda r: -c_counts[r])[:10]:
        tag = "  (ARCHIVE)" if rel.startswith('runs') else ""
        print("     %-56s %4d%s" % (rel[:56], c_counts[rel], tag))

    print()
    print("=" * 78)
    print("-" * 78)
    print("[G] S1 scope bleed: an ME label inside a CHAIN directory (advisory)")
    print("-" * 78)
    bleeds = hits['G'].get('SCOPE-BLEED', [])
    if not bleeds:
        print("     none  — no ME predicate appears in a chain product")
    else:
        for rel, ln, tok in bleeds[:12]:
            print("        %s:%d  %s" % (rel, ln, tok))
        print("     %d hit(s): a branch predicate is being used in the C domain" % len(bleeds))

    print()
    print("MUST-FIX total (A, C, D): %d   [F is advisory: M1-M4 are pre-existing owners]" % must_total)
    print("Exit code 0 by design — report, not gate.")
    print()
    print("Content generated by AI")


if __name__ == '__main__':
    main()
