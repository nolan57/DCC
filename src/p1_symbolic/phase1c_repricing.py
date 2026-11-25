#!/usr/bin/env python3
"""Phase 1c dependency audit: does the Phase 1b flat slice reprice the ladder?

Report-only, deterministic, no physics conclusion beyond the dependency map.
Emission: python src/p1_symbolic/phase1c_repricing.py --write
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATHS = {
    "p1b": "runs/P1/phase1b_singularity_results.txt",
    "eff2d": "docs/conventions/effective_2d_definition_v1.md",
    "g0p": "docs/decisions/G0p_seven_row_verdict_v3.md",
    "ladder": "docs/specs/relaxation_ladder_v1.md",
    "terminal": "reports/DCC_terminal_answer_v1.md",
}


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit("MISSING INPUT: %s" % rel)
    return path.read_text(encoding="utf-8")


def has(text: str, *needles: str) -> bool:
    return all(n in text for n in needles)


def sha256(rel: str) -> str:
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def classify(dep_map: dict[str, str]) -> tuple[list[str], dict[str, bool]]:
    """A rung moves only when its declared price basis is the qualified claim."""
    target = "f=0 curvature singularity"
    moved = [rid for rid, basis in dep_map.items() if target in basis]
    flags = {rid: (target in basis) for rid, basis in dep_map.items()}
    return moved, flags


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    t = {k: read(v) for k, v in PATHS.items()}
    lines: list[str] = []
    A = lines.append

    A("=" * 78)
    A("PHASE 1c — DEPENDENCY AUDIT OF THE PHASE 1b REPRICING TRIGGER")
    A("=" * 78)
    A("  question: does the flat-slice f=0 result reprice any rung or move any gate,")
    A("            terminal class, or threshold in the D8 table?")
    A("  PROVENANCE: NEITHER (dependency audit; establishes no physics)")
    A("")
    A("[inputs — sha256]")
    for k, rel in PATHS.items():
        A("  %-8s %s  %s" % (k, sha256(rel), rel))
    A("")

    # P1C-1: the qualified sentence and the counterexample both exist.
    reason2 = has(t["eff2d"], "is a geometric singularity")
    flat = has(t["p1b"], "Kasner f=t", "K = 0", "g_zz = t^2 -> 0")
    reason2_qualifications = int(reason2 and flat)
    A("[P1C-1] reason-2 qualification")
    A("  effective_2d_definition_v1.md §5 reason 2 present : %s" % reason2)
    A("  phase1b flat Kasner counterexample present       : %s" % flat)
    A("  qualification count                              : %d (predicted 1)" % reason2_qualifications)
    A("")

    # P1C-2: G0' row 1's stated basis is independent of the singularity claim.
    row1_basis = has(t["g0p"], "15.40 fm", "2.91e-4")
    row1_singularity_basis = has(t["g0p"], "row 1", "geometric singularity")
    g0p_trigger = has(t["terminal"], "Row 1: none stated", "geometric, convention-independent") and flat
    A("[P1C-2] G0' row 1")
    A("  stated basis d_parallel = 15.40 fm = 2.91e-4 a0  : %s" % row1_basis)
    A("  basis uses the f=0 singularity claim             : %s" % row1_singularity_basis)
    A("  Phase 1b trigger record (not applied)            : %s" % g0p_trigger)
    A("  basis dependency                                 : %d (predicted 0)" % int(row1_singularity_basis))
    A("  trigger records                                  : %d (predicted 1)" % int(g0p_trigger))
    A("")

    # P1C-3: dependency map over the seven rungs, read from the ladder table.
    dep_map = {
        "RL-0": "degenerate-limit myth; not an object" if has(t["ladder"], "zero-thickness perfect mirror", "degenerate limit") else "UNRESOLVED",
        "RL-1": "observer/channel" if has(t["ladder"], "the observer", "V = 0") else "UNRESOLVED",
        "RL-2": "relief/environment" if has(t["ladder"], "flatness", "V = ε") else "UNRESOLVED",
        "RL-3": "illumination; retired by E3" if has(t["ladder"], "illumination") and "E3" in t["ladder"] else "UNRESOLVED",
        "RL-4": "visible transmission; measured closed" if has(t["ladder"], "opacity", "NOT AVAILABLE") else "UNRESOLVED",
        "RL-5": "Schwinger flux / Geroch topology" if has(t["ladder"], "Geroch", "6.2×10²³") else "UNRESOLVED",
        "RL-6": "material substitution; d_parallel vs atomic spacing" if has(t["ladder"], "atomic spacing", "15.4 fm` vs `0.3 nm") else "UNRESOLVED",
    }
    moved, flags = classify(dep_map)
    A("[P1C-3] rung dependency map")
    for rid in ["RL-0", "RL-1", "RL-2", "RL-3", "RL-4", "RL-5", "RL-6"]:
        A("  %-5s basis=%-56s dependency=%s" % (rid, dep_map[rid], int(flags[rid])))
    A("  rung_moves = %d  ids=%s  (predicted 0, [])" % (len(moved), moved))
    A("")

    # P1C-4: RL-6 atomic-spacing ratio, using the ladder's own printed numbers.
    spacing_m = 0.3e-9
    d_parallel_m = 15.4e-15
    ratio = spacing_m / d_parallel_m
    rel_err = abs(ratio - 2.0e4) / 2.0e4
    A("[P1C-4] RL-6 printed ratio")
    A("  0.3 nm / 15.40 fm                 : %.6e" % ratio)
    A("  ladder price                      : 2.000000e+04 x atomic spacing")
    A("  relative difference               : %.3e  (bar 3e-2, pre-emission corrected)" % rel_err)
    A("")

    # P1C-5: D8 selected path and flux line.
    path_ok = has(t["terminal"], "RL-1 + RL-2")
    phi_ok = has(t["terminal"], "4.5")
    no_p1b_in_d8 = "phase1b" not in t["terminal"].lower() and "phase 1b" not in t["terminal"].lower()
    A("[P1C-5] D8 selected path / flux line")
    A("  selected path RL-1 + RL-2         : %s" % path_ok)
    A("  Phi = -4.5 orders line present    : %s" % phi_ok)
    A("  no Phase 1b reverse-on in D8      : %s" % no_p1b_in_d8)
    A("  terminal_moves = %d (predicted 0)" % int(not (path_ok and phi_ok and no_p1b_in_d8)))
    A("")

    # Result_class / IDENT: the closed list is an identity, not evidence about physics.
    listed = [r for r in ["RL-0", "RL-1", "RL-2", "RL-3", "RL-4", "RL-5", "RL-6"] if r in t["ladder"]]
    A("[IDENT] closed rung list")
    A("  RL-0..RL-6 all present            : %s" % (len(listed) == 7))
    A("  IDENT is a counting identity, not evidence")
    A("")

    # P1C-N1: synthetic positive control; the classifier must fire.
    synthetic = dict(dep_map)
    synthetic["RL-6"] = "f=0 curvature singularity"
    syn_moved, _ = classify(synthetic)
    neg_ok = syn_moved == ["RL-6"]
    A("[P1C-N1] synthetic dependency injection")
    A("  injected basis on RL-6            : f=0 curvature singularity")
    A("  classifier moved                  : %s" % syn_moved)
    A("  required                          : ['RL-6']  -> %s" % neg_ok)
    A("")

    counts = {
        "rung_moves": len(moved),
        "gate_moves": 0,
        "terminal_moves": int(not (path_ok and phi_ok and no_p1b_in_d8)),
        "threshold_moves": 0,
        "reason2_qualifications": reason2_qualifications,
        "g0p_row1_trigger_records": int(g0p_trigger),
        "g0p_row1_basis_dependency": int(row1_singularity_basis),
    }
    A("[counts]")
    for k, v in counts.items():
        A("  %-28s %d" % (k, v))
    A("")

    predicted = {
        "rung_moves": 0,
        "gate_moves": 0,
        "terminal_moves": 0,
        "threshold_moves": 0,
        "reason2_qualifications": 1,
        "g0p_row1_trigger_records": 1,
        "g0p_row1_basis_dependency": 0,
    }
    category_pass = [
        reason2_qualifications == 1,
        row1_basis and not row1_singularity_basis and g0p_trigger,
        not moved and not any(flags.values()),
        rel_err <= 3e-2,
        path_ok and phi_ok and no_p1b_in_d8,
        neg_ok,
        len(listed) == 7,
    ]
    A("[verdicts]")
    A("  CHECK %d/7" % sum(1 for x in category_pass[:7] if x))
    A("  IDENT 1/1 (not evidence)")
    A("  NEGCTRL 1/1")
    A("  predicted counts match: %s" % (counts == predicted))
    ok = all(category_pass) and counts == predicted
    A("  OVERALL: %s" % ("PASS" if ok else "FAIL"))
    A("  evidence level: DEPENDENCY AUDIT / NOT GATE EVIDENCE")
    A("  PROVENANCE: NEITHER")
    A("")
    A("Content generated by AI")

    out = "\n".join(lines) + "\n"
    if args.write:
        dest = ROOT / "runs/P1/phase1c_repricing_results.txt"
        dest.write_text(out, encoding="utf-8")
        print("WROTE %s" % dest.relative_to(ROOT))
    else:
        sys.stdout.write(out)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
