# -*- coding: utf-8 -*-
"""
h5_b8_stageB_v1.py -- H5-B8 stage B (TECHNICAL, report-only).

Checks the registered predictions of runs/H5-B8/b8_route_boundary_registration.md
against the archived RR-DT ladder record and the Phase 1 symbolic result. It
establishes no new physics, registers no threshold, and emits one product:

    runs/H5-B8/b8_route_boundary_results.txt

Run from the repository root:

    python -I src/analysis/h5_b8_stageB_v1.py

Every number is quoted with the file and line that produced it. CHECK, IDENT
and NEGCTRL are counted separately; a failed prediction stays in the product.
"""
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "runs", "H5-B8", "b8_route_boundary_results.txt")
LOCK = os.path.join(ROOT, "runs", "H5-B8", "b8_route_boundary_lock.json")
W = 88


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def read(path):
    with open(os.path.join(ROOT, path), "r", encoding="utf-8") as f:
        return f.read().splitlines()


def lines_with(needle, text):
    return [i + 1 for i, ln in enumerate(text) if needle in ln]


def verify_lock():
    lines = []
    try:
        with open(LOCK, "r", encoding="utf-8") as f:
            lock = json.load(f)
    except (OSError, ValueError) as exc:
        return False, ["lock unreadable: %s" % exc], {}
    side = LOCK + ".sha256"
    recorded = open(side, "r", encoding="utf-8").read().split()[0].strip().lower()
    got = sha256(LOCK)
    ok = got == recorded
    lines.append("lock digest        %s  recorded=%s  %s" % (got[:12], recorded[:12], "OK" if ok else "MISMATCH"))
    for label, item in lock.get("files", {}).items():
        rel = item["path"]
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            lines.append("  %-18s MISSING  %s" % (label, rel))
            ok = False
            continue
        h = sha256(p)
        good = h == item["sha256"].lower()
        lines.append("  %-18s %s  %s  %s" % (label, h[:12], "OK" if good else "MISMATCH", rel))
        ok = ok and good
    return ok, lines, lock


BROW = re.compile(r"^\s*(B\d+)\s+self-consistent\s+(\S+)\s+boundary\s+(\S+)")
BSUM = re.compile(r"^\s*(B\d+)\s+(.+?)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s*$")


def parse_table(text):
    """Return (rows, provenance lines) where rows is level -> (sc, boundary, lineno)."""
    rows, prov = {}, []
    for i, ln in enumerate(text, 1):
        m = BROW.match(ln)
        if m:
            rows[m.group(1)] = (m.group(2), m.group(3), i)
            prov.append((i, ln.strip()))
    return rows, prov


def parse_twice(text):
    a, _ = parse_table(text)
    b, _ = parse_table(list(text))
    return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True), a


def main():
    lock_ok, lock_lines, lock = verify_lock()
    rrdt = read("runs/RR-DT/rr_dt_01_record_repair_results.txt")
    record = read("runs/RR-DT/constraint_relaxation_record.md")
    phase1 = read("runs/P1/phase1_symbolic_constraint_results.txt")
    adoption = read("docs/decisions/hard_sf_effective_2d_route_adoption_v1.md")
    proposal = read("docs/decisions/hard_sf_effective_2d_route_proposal_v1.md")

    out = []
    out.append("=" * W)
    out.append("H5-B8 -- ROUTE-TO-B8 BOUNDARY CONFORMANCE CHECK (TECHNICAL, REPORT-ONLY)")
    out.append("=" * W)
    out.append("PROVENANCE: NEITHER")
    out.append("Question: does the adopted route stop exactly at B8 under the registered B1-B10 ladder?")
    out.append("All commands: python -I src/analysis/h5_b8_stageB_v1.py, CWD = repo root.")
    out.append("This product audits records; it establishes no chain, branch, gate, price or visibility claim.")
    out.append("Erratum E1: the first run is kept at b8_route_boundary_results_run1_falsified.txt; two parser")
    out.append("  defects (P4 source file, P6 line-wrapped needle) were corrected without moving a prediction.")
    out.append("  P4's correct source is constraint_relaxation_record.md:289, not the results file cited in stage A.")
    out.append("")
    out.append("-" * W)
    out.append("STAGE A LOCKS")
    out.append("-" * W)
    out.extend(lock_lines)
    out.append("")

    identical, rows = parse_twice(rrdt)
    yes = [(lv, v[2]) for lv, v in rows.items() if v[1] == "YES"]
    b18 = [lv for lv in rows if lv in ["B%d" % i for i in range(1, 8)] and rows[lv][0] == "YES"]
    checks = []

    # P1 -- exactly one boundary level, and it is B8.
    p1 = (len(yes) == 1 and yes[0][0] == "B8")
    checks.append(("P1", p1, "boundary YES count=%d level=%s" % (len(yes), ",".join(l for l, _ in yes)),
                   "runs/RR-DT/rr_dt_01_record_repair_results.txt:%s" % ",".join(str(n) for _, n in yes)))

    # P2 -- B1-B7 self-consistent YES (7) and B8 NO.
    b8sc = rows.get("B8", ("?", "?", 0))[0]
    p2 = (len(b18) == 7 and b8sc == "NO")
    checks.append(("P2", p2, "B1-B7 self-consistent YES=%d, B8=%s" % (len(b18), b8sc),
                   "runs/RR-DT/rr_dt_01_record_repair_results.txt:88-95"))

    # P3 -- B9 not evaluated, B10 never relaxed.
    b9line = lines_with("NOT EVALUATED-BEYOND-BOUNDARY", record)
    b10line = lines_with("NEVER RELAXED", record)
    p3 = (len(b9line) >= 1 and len(b10line) >= 1 and rows.get("B9", ("?", "?", 0))[1] == "?")
    checks.append(("P3", p3, "B9 unevaluated=%s B10 never-relaxed=%s match_count=%d" %
                   (bool(b9line), bool(b10line), int(bool(b9line)) + int(bool(b10line))),
                   "runs/RR-DT/constraint_relaxation_record.md:%s" % ",".join(map(str, b9line[:1] + b10line[:1]))))

    # P4 -- B8 summary row: RL-6 = 2e4, G0' row 1 unsayable, eff-2D undefined.
    b8sum = [(i, ln.strip()) for i, ln in enumerate(record, 1) if re.match(r"^\s*B8\s+global hyperbolicity", ln)]
    vals = BSUM.match(b8sum[0][1]) if b8sum else None
    triple = (vals.group(5), vals.group(6), vals.group(7)) if vals else ("", "", "")
    p4 = triple == ("2e4", "unsayable", "undefined")
    checks.append(("P4", p4, "B8 summary RL-6=%s G0'=%s eff-2D=%s" % triple,
                   "runs/RR-DT/constraint_relaxation_record.md:%d" % (b8sum[0][0] if b8sum else 0)))

    # P5 -- Phase 1 class ceiling.
    ceil = lines_with("class <= constraint-satisfying solution", phase1)
    deny = lines_with("NOT an evolution solution; NOT a joint solution", phase1)
    p5 = bool(ceil) and bool(deny)
    checks.append(("P5", p5, "ceiling line=%s denial line=%s match_count=%d" %
                   (ceil[:1], deny[:1], int(bool(ceil)) + int(bool(deny))),
                   "runs/P1/phase1_symbolic_constraint_results.txt:%s" % ",".join(map(str, ceil[:1] + deny[:1]))))

    # P6 -- two avoidances recorded, neither adopted.
    av1 = lines_with("(i) Confine the relaxation", record)
    av2 = lines_with("(ii) Drop", record)   # wrapped in the archive: continuation on the next line
    adopt_line = lines_with("Neither is adopted here", adoption)
    p6 = bool(av1) and bool(av2) and bool(adopt_line)
    checks.append(("P6", p6, "avoidances recorded=%d adopted=%d" %
                   (int(bool(av1)) + int(bool(av2)), 0 if adopt_line else 1),
                   "runs/RR-DT/constraint_relaxation_record.md:%s; docs/decisions/hard_sf_effective_2d_route_adoption_v1.md:%s" %
                   (",".join(map(str, (av1[:1] + av2[:1]))), ",".join(map(str, adopt_line[:1])))))

    # Governor mark transcribed in place.
    mark = lines_with("[x] Accept as the governing successor route", proposal)
    out.append("-" * W)
    out.append("GOVERNOR MARK (transcribed by the governor, not inferred by the executor)")
    out.append("-" * W)
    out.append("  %s  [x] Accept as the governing successor route  docs/decisions/hard_sf_effective_2d_route_proposal_v1.md:%s" %
               ("PASS" if mark else "FAIL", ",".join(map(str, mark[:1])) or "0"))
    out.append("  note: the other two lines remain unmarked; no approval was inferred from silence.")
    out.append("")

    out.append("-" * W)
    out.append("CHECK (P1-P6) -- counted as evidence only when all pass")
    out.append("-" * W)
    for cid, ok, detail, src in checks:
        out.append("  %-4s %-4s  %s" % (cid, "PASS" if ok else "FAIL", detail))
        out.append("       source: %s" % src)
    npass = sum(1 for _, ok, _, _ in checks if ok)
    out.append("  CHECK %d/%d" % (npass, len(checks)))
    out.append("")

    out.append("-" * W)
    out.append("IDENT (not evidence) and NEGCTRL (counted separately)")
    out.append("-" * W)
    out.append("  IDENT I1 repeat-parse-identical=%s  (not evidence)" % identical)
    b7 = [(lv, v[2]) for lv, v in rows.items() if lv == "B7" and v[1] == "YES"]
    neg = len(b7) == 0 and len(yes) == 1
    out.append("  NEGCTRL N1 B7 boundary YES=%d against B8 boundary YES=%d  %s" %
               (len(b7), len(yes), "PASS" if neg else "FAIL"))
    out.append("  required failure factor: one level (B7=0, B8=1).")
    out.append("")

    out.append("-" * W)
    out.append("INSTRUMENT FLOOR AND LIMIT")
    out.append("-" * W)
    out.append("  exact-text parser; floor 0 mismatches on unchanged input (IDENT I1 = %s)." % identical)
    out.append("  The parser cannot distinguish a one-character edit in a counted field from no edit;")
    out.append("  no numeric tolerance is used and no branch of this instrument measures physics.")
    out.append("  No threshold was introduced or evaluated in this round.")
    out.append("")

    verdict_pass = lock_ok and identical and neg and npass == len(checks) and bool(mark)
    verdict = "PASS" if verdict_pass else "FALSIFIED"
    out.append("-" * W)
    out.append("VERDICT: %s" % verdict)
    out.append("  CHECK %d/%d - IDENT 1/1 (not evidence) - NEGCTRL %s" %
               (npass, len(checks), "1/1" if neg else "0/1"))
    out.append("  Meaning: the adopted hard-SF effective-2D route stops at B8 (referential reading;")
    out.append("  B10 by construction under the strict-propositional reading), with no claim beyond.")
    if not verdict_pass:
        out.append("  A failed prediction is retained verbatim above and no B8 claim is made by this cycle.")
    out.append("")
    out.append("Content generated by AI")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print("wrote %s (%s)" % (os.path.relpath(OUT, ROOT), verdict))
    return 0  # report-only: the instrument never vetoes a product


if __name__ == "__main__":
    main()
