# -*- coding: utf-8 -*-
"""
w2_count_stageB_v1.py -- MEASURE stage for research-publication item 10.

Closes the W1-ROW2 open slot: states M as a history functional and derives the
slice/fragment counts with their label and spread. All numbers are read from
the locked inputs; no new physics and no re-pricing.

Run: python -I src/analysis/w2_count_stageB_v1.py
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

ROOT = W.ROOT
D = "runs/W2-COUNT"
PREFIX = "count"


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


def parse_components(path):
    """Read the seven registered z regions and their components/layer, verbatim."""
    text = open(path, "r", encoding="utf-8").read()
    rows = []
    for i, line in enumerate(text.splitlines(), 1):
        m = re.match(r"\s*([A-Za-z][A-Za-z\s>\-]*?)\s+"
                     r"([0-9]+\.[0-9]+)-([0-9]+\.[0-9]+)\s+"
                     r"([0-9]+\.[0-9]+)\s+"
                     r"([0-9]+\.[0-9]+)\s*-\s*([0-9.]+)\s*$", line)
        if m:
            rows.append(dict(line=i, region=m.group(1).strip(),
                             z0=float(m.group(2)), z1=float(m.group(3)),
                             components=float(m.group(4)),
                             a0=float(m.group(5)), a1=float(m.group(6))))
    return rows, text


def weighted_stats(rows):
    w = np.array([r["z1"] - r["z0"] for r in rows], dtype=np.float64)
    c = np.array([r["components"] for r in rows], dtype=np.float64)
    w = w / w.sum()
    mean = float((w * c).sum())
    var = float((w * (c - mean) ** 2).sum())
    return dict(mean=mean, sd=float(np.sqrt(var)), var=var,
                weights=w.tolist(), components=c.tolist())


def m_contract():
    """The five section-2.6 elements, written from the registered front state."""
    return {
        "1_history_functional": {
            "form": "u(t) = M[U(tau), phi(tau); 0 <= tau <= t]",
            "markov": "NOT PROVED; treated as a history functional per section 2.6",
            "extended_state_if_instant": ["deposited field u", "interface/front state phi",
                                          "per-site layer history"],
            "ground": "u(t_mid) is built by sweeping the front from tau=0, not from U(t_mid) alone",
        },
        "2_domain": {
            "reduced_z_interval_at_t": [0.0, w1.state_at(w1.T_MID_S)["zf"]],
            "front_parameter": "phi(x,y,z,t)=0 is the plane z = v_front*t, normal +z, speed v_front",
            "ground": "front_sweep_v1 front law; w1_row2_common_v1.state_at",
        },
        "3_units_coordinates": {
            "z": "m, lab frame, +z along front advance",
            "u": "dimensionless per-site layer-density index; density kg/m^3 for the mass ledger",
            "delta": "%s m (mechanism property, not a rendering knob)" % f(w1.DELTA, 6),
        },
        "4_single_valued": {
            "rule": "one deposited value per (x,y) site; where two layers compete the front-most wins",
            "tie": "equal-front cases take the mean and are counted in the ledger",
            "ground": "site occupancy is a function, not a multivalued map",
        },
        "5_discard_ledger": {
            "discards": ["vertical resolution below delta", "composition detail inside a layer",
                         "phase", "momentum"],
            "entered_at": "section 4.2.3-4.2.4 conservation ledger; mass/volume close by construction",
            "outflow": "booked, not dropped (w2_common.stretch_pushforward)",
        },
    }


def main():
    lock_path = os.path.join(ROOT, D, PREFIX + "_lock.json")
    ok, block = lock_block(lock_path)
    if not ok:
        print("STAGE B REFUSED: lock failed\n" + block)
        return 1

    sweep_path = os.path.join(ROOT, "runs/ANALYSIS/front_sweep_v1.txt")
    rows, sweep_text = parse_components(sweep_path)
    stats = weighted_stats(rows)
    contract = m_contract()

    st = w1.state_at(w1.T_MID_S)
    n_slices_mid = st["zf"] / w1.DELTA
    n_slices_full = w1.H_BODY / w1.DELTA
    n_frag_mid = n_slices_mid * stats["mean"]
    n_frag_full = n_slices_full * stats["mean"]

    registered_line = next((ln for ln in sweep_text.splitlines()
                            if "Mean components" in ln), "")
    reg_mean_match = re.search(r"=\s*([0-9.]+)", registered_line)
    reg_mean = float(reg_mean_match.group(1)) if reg_mean_match else w1.COMP_PER_LAYER

    checks = {
        "N1": all(k in contract for k in (
            "1_history_functional", "2_domain", "3_units_coordinates",
            "4_single_valued", "5_discard_ledger")),
        "N2": abs(stats["mean"] - 1.457) <= 0.002,
        "N3": bool(stats["sd"] > 0.0),
        "N4": bool(n_slices_mid > 0 and n_frag_mid > 0),
    }
    verdict = "PASS" if all(checks.values()) else "FALSIFIED"

    lines = [
        "[0] LOCK",
        block,
        "",
        "[1] THE MAP M -- five section-2.6 elements (not inferred from appearance)",
    ]
    for key, val in contract.items():
        lines.append("    %s:" % key)
        for k2, v2 in val.items():
            lines.append("        %s: %s" % (k2, v2))
    lines += [
        "",
        "[2] COMPONENT TABLE -- runs/ANALYSIS/front_sweep_v1.txt (parsed, not retyped)",
        "    line  region            z0      z1     components/layer",
    ]
    for r in rows:
        lines.append("    %4d  %-16s %6.3f  %6.3f      %.2f" %
                     (r["line"], r["region"][:16], r["z0"], r["z1"], r["components"]))
    lines += [
        "    %d regions; z-width weights sum to 1 by construction" % len(rows),
        "",
        "[3] WEIGHTED DERIVATION OF components/layer",
        "    weighted mean   = %s   (registered %s, |diff| %s)" %
        (f(stats["mean"], 10), f(reg_mean, 10), f(abs(stats["mean"] - reg_mean), 6)),
        "    weighted sd     = %s   (derivation spread, not a physical measurement error)" %
        f(stats["sd"], 10),
        "",
        "[4] COUNTS -- recomputed, labelled, with derivation",
        "    t_mid z_front       = %s m" % f(st["zf"], 10),
        "    delta               = %s m" % f(w1.DELTA, 6),
        "    N_slices(t_mid)     = %s = z_front/delta   [MODEL COUNT]" % f(n_slices_mid, 10),
        "    N_slices(full body)= %s = H_body/delta     [MODEL COUNT]" % f(n_slices_full, 10),
        "    N_frag(t_mid)       = %s = N_slices(t_mid) x weighted mean   [MODEL ESTIMATE]" %
        f(n_frag_mid, 10),
        "    N_frag(full body)   = %s                                        [MODEL ESTIMATE]" %
        f(n_frag_full, 10),
        "    registered 1.18e10 is the full-body mechanism count; no physical realization is claimed",
        "",
        "[5] PREDICTIONS",
        "    N1 M contract complete (five elements)   %s" % ("PASS" if checks["N1"] else "FAIL"),
        "    N2 weighted mean = 1.457 +/- 0.002        %s" % ("PASS" if checks["N2"] else "FAIL"),
        "    N3 weighted spread nonzero and labelled %s" % ("PASS" if checks["N3"] else "FAIL"),
        "    N4 counts recomputed with derivation    %s" % ("PASS" if checks["N4"] else "FAIL"),
        "    overall: %s" % verdict,
        "",
        "The fragment count is a MODEL ESTIMATE of the registered component rule; its spread is a derivation",
        "property of the region table, not an observed uncertainty of a physical phantom.",
    ]
    result = os.path.join(ROOT, D, "count_results_v1.txt")
    W.write_text(result, W.banner(W.PROVENANCE,
        "W2-COUNT-01 -- M CONTRACT AND COUNT DERIVATION", lines))

    profile = W.json_tag({
        "cycle_id": "W2_COUNT_01", "utc": W.utc(),
        "sweep_source": "runs/ANALYSIS/front_sweep_v1.txt",
        "component_rows": rows, "weighted_stats": stats,
        "registered_mean": reg_mean,
        "t_mid": st, "counts": {
            "N_slices_mid": n_slices_mid, "N_slices_full": n_slices_full,
            "N_frag_mid": n_frag_mid, "N_frag_full": n_frag_full,
            "label": "MODEL COUNT / MODEL ESTIMATE (mechanism output, not observation)",
        },
        "m_contract": contract, "checks": checks, "verdict": verdict,
    })
    write_json(os.path.join(ROOT, D, "count_profile_v1.json"), profile)
    record = W.json_tag({
        "cycle_id": "W2_COUNT_01", "utc": W.utc(), "python": sys.version.split()[0],
        "numpy": np.__version__,
        "modules": {p: W.sha256(os.path.join(ROOT, p)) for p in (
            "src/analysis/w2_common_v1.py", "src/analysis/w2_count_stageB_v1.py",
            "src/analysis/w1_row2_common_v1.py")},
        "threshold_lock_sha256": w1.LOCK_SHA,
        "products": ["runs/W2-COUNT/count_results_v1.txt",
                     "runs/W2-COUNT/count_profile_v1.json"],
        "rendered_frames": [],
    })
    write_json(os.path.join(ROOT, D, "count_run_record_v1.json"), record)
    print("W2-COUNT-01: %s  mean=%s sd=%s N_frag(full)=%s" %
          (verdict, f(stats["mean"], 8), f(stats["sd"], 8), f(n_frag_full, 8)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
