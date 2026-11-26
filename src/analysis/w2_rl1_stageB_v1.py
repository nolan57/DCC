# -*- coding: utf-8 -*-
"""
w2_rl1_stageB_v1.py -- MEASURE stage for programme section 6.1 item 6.

Re-runs RL-1 on the row-2 deposit scene at theta_fast. The flux chain and the
q definition are read from the locked registrations; no new threshold is made.

Run: python -I src/analysis/w2_rl1_stageB_v1.py
"""
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w2_common_v1 as W
import w1_row2_common_v1 as w1
import tiers_core_v1 as tc

ROOT = W.ROOT
D = "runs/W2-RL1"
PREFIX = "rl1"


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return float(x)
    if isinstance(x, (np.integer, int)):
        return int(x)
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    return x if x is None else str(x)


def write_json(path, obj):
    W.write_text(path, json.dumps(jsonable(obj), indent=2, ensure_ascii=False) + "\n")
    return path


def f(x, n=12):
    return "n/a" if x is None else ("%%.%dg" % n) % float(x)


def lock_block(path):
    ok, lines = W.verify_lock(path)
    return ok, "\n".join(["LOCK: %s" % os.path.relpath(path, ROOT),
                          "  status: %s" % ("VERIFIED" if ok else "FAILED"),
                          *["  " + ln for ln in lines]])


def parse_shortfall(path):
    text = open(path, "r", encoding="utf-8").read()
    m = re.search(r"shortfall at 1e-7\s*=.*?=\s*([0-9.eE+-]+)", text)
    if not m:
        raise ValueError("shortfall at 1e-7 not found in %s" % path)
    for i, line in enumerate(text.splitlines(), 1):
        if "shortfall at 1e-7" in line:
            return float(m.group(1)), i
    raise ValueError("shortfall line not located")


def main():
    lock_path = os.path.join(ROOT, D, PREFIX + "_lock.json")
    ok, block = lock_block(lock_path)
    if not ok:
        print("STAGE B REFUSED: lock failed\n" + block)
        return 1

    flux_path = os.path.join(ROOT, "runs/LADDER/r1_observer_results.txt")
    shortfall, flux_line = parse_shortfall(flux_path)
    c_star = 1e-7 * np.sqrt(shortfall)

    st = w1.state_at(w1.T_MID_S)
    u = w1.plate_field(st["zf"])
    rows, meta = w1.measure(u, "plate")
    xi = meta["xi"]
    c_xi = meta["C_xi"]
    q_fast = min(1.0, (c_xi / c_star) ** 2)
    eye = tc.q3(u, xi, 0.0)
    ideal = tc.q3(u, xi, 1.0)
    fast = tc.q3(u, xi, q_fast)
    shortfall_at_cxi = shortfall * (1e-7 / c_xi) ** 2

    ref_path = os.path.join(ROOT, "runs/W1-ROW2/row2_prediction_v1.json")
    ref = json.load(open(ref_path, "r", encoding="utf-8"))
    ref_rows = {(r["field"], r["tier"]): r for r in ref["profile"]
                if r["keyframe"] == "t_mid" and r["field"] == "plate"}
    profile_check = []
    for r in rows:
        q = ref_rows[("plate", r["tier"])]
        profile_check.append(dict(
            tier=r["tier"], measured=f(r["value"], 12), reference=f(q["value"], 12),
            verdict=r["verdict"], reference_verdict=q["verdict"],
            ok=(r["verdict"] == q["verdict"] and
                ((r["value"] is None and q["value"] is None) or
                 abs(r["value"] - q["value"]) <= 1e-12))))

    checks = {
        "R1": bool(c_xi > c_star and q_fast == 1.0),
        "R2": bool(fast is not None and ideal is not None and eye is not None and
                   abs(fast[0] - ideal[0]) <= 1e-12 and eye[0] == 0.0),
        "R3": all(r["ok"] for r in profile_check),
        "R4": bool(shortfall_at_cxi < 1.0),
    }
    verdict = "PASS" if all(checks.values()) else "FALSIFIED"

    lines = [
        "CYCLE: W2-RL1-01  (programme section 6.1 item 6)",
        "TYPE: TECHNICAL closure; RL-1 on the deposit's own 2D-ified field",
        block,
        "",
        "[1] REGISTERED CHARGE CHAIN (not re-priced)",
        "    source: runs/LADDER/r1_observer_results.txt line %d" % flux_line,
        "    shortfall at contrast 1e-7 = %s" % f(shortfall, 8),
        "    C* = 1e-7 sqrt(shortfall) = %s" % f(c_star, 10),
        "    q(theta_fast) = min(1, (C_xi/C*)^2)  [runs/LADDER/r1_observer_registration.md line 23]",
        "",
        "[2] ROW-2 SCENE AT t_mid",
        "    t = %s s ; z_front = %s m" % (f(st["t"], 10), f(st["zf"], 10)),
        "    delta = %s m ; constraints C1 HELD / C2 HELD / C3 VIOLATED" % f(w1.DELTA, 6),
        "    theta: band = declared density channel; gate/aperture/distance = none",
        "    E = declared density field (no radiance substitution)",
        "    G = G_A, local normal at zero incidence, delta_v = 0.01 rad (integrated out by the estimator)",
        "    effective 2D: %s ; missing slot: %s" %
        (w1.effective2d()["label"], w1.effective2d()["missing_slot"]),
        "",
        "[3] MEASURED CONTRAST AND CHANNEL FACTORS",
        "    xi = %s cells ; C_xi = %s ; C_xi/C* = %s" %
        (f(xi, 10), f(c_xi, 10), f(c_xi / c_star, 10)),
        "    q(theta_eye)=%s ; q(theta_ideal)=%s ; q(theta_fast)=%s" %
        (f(0.0, 1), f(1.0, 1), f(q_fast, 12)),
        "    Q3(theta_eye)=%s ; Q3(theta_ideal)=%s ; Q3(theta_fast)=%s" %
        (f(eye[0], 12), f(ideal[0], 12), f(fast[0], 12)),
        "    shortfall at the measured C_xi = %s" % f(shortfall_at_cxi, 12),
        "",
        "[4] TIER PROFILE AGAINST W1-ROW2 t_mid PLATE",
    ]
    for chk in profile_check:
        note = next(r["note"] for r in rows if r["tier"] == chk["tier"])
        lines.append("    %s measured=%s reference=%s verdict=%s reference_verdict=%s ok=%s" %
                     (chk["tier"], chk["measured"], chk["reference"], chk["verdict"],
                      chk["reference_verdict"], chk["ok"]))
        lines.append("      %s" % note)
    lines += [
        "",
        "[5] PREDICTIONS",
        "    R1 q_fast saturation        %s" % ("PASS" if checks["R1"] else "FAIL"),
        "    R2 Q3 channel identity      %s" % ("PASS" if checks["R2"] else "FAIL"),
        "    R3 tier profile identity    %s" % ("PASS" if checks["R3"] else "FAIL"),
        "    R4 flux gate open           %s" % ("PASS" if checks["R4"] else "FAIL"),
        "    overall: %s" % verdict,
        "",
        "This is a channel contrast measurement. It does not claim effective two-dimensionality, physical",
        "realizability, or legibility from the declared viewing geometry: the estimator has no angular variable.",
        "The old stand-in result in runs/LADDER is not substituted for this scene measurement.",
    ]
    result = os.path.join(ROOT, D, "rl1_results_v1.txt")
    W.write_text(result, W.banner(W.PROVENANCE,
        "W2-RL1-01 -- RL-1 q(theta_fast) ON THE ROW-2 DEPOSIT SCENE", lines))

    profile = W.json_tag({
        "cycle_id": "W2_RL1_01", "t_s": st["t"], "z_front_m": st["zf"],
        "flux_chain": {"source": "runs/LADDER/r1_observer_results.txt", "line": flux_line,
                       "shortfall_at_1e-7": shortfall, "C_star": c_star,
                       "shortfall_at_C_xi": shortfall_at_cxi},
        "channel": {"C_xi": c_xi, "xi_cells": xi, "q_eye": 0.0, "q_ideal": 1.0,
                    "q_fast": q_fast, "Q3_eye": eye[0], "Q3_ideal": ideal[0],
                    "Q3_fast": fast[0]},
        "theta": {"G": "G_A local normal, delta_v=0.01 rad; integrated out",
                  "E": "declared density field", "band": "declared density channel"},
        "effective_2d": w1.effective2d(),
        "tier_profile": rows, "w1_reference_check": profile_check,
        "checks": checks, "verdict": verdict,
    })
    write_json(os.path.join(ROOT, D, "rl1_profile_v1.json"), profile)
    record = W.json_tag({
        "cycle_id": "W2_RL1_01", "utc": W.utc(), "python": sys.version.split()[0],
        "numpy": np.__version__,
        "modules": {p: W.sha256(os.path.join(ROOT, p)) for p in (
            "src/analysis/w2_common_v1.py", "src/analysis/w2_rl1_stageB_v1.py",
            "src/analysis/w1_row2_common_v1.py", "src/analysis/tiers_core_v1.py")},
        "threshold_lock_sha256": w1.LOCK_SHA,
        "products": ["runs/W2-RL1/rl1_results_v1.txt", "runs/W2-RL1/rl1_profile_v1.json"],
        "rendered_frames": [],
    })
    write_json(os.path.join(ROOT, D, "rl1_run_record_v1.json"), record)
    print("W2-RL1-01: %s  q_fast=%s Q3_fast=%s" %
          (verdict, f(q_fast, 10), f(fast[0], 10)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
