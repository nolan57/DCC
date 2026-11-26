# -*- coding: utf-8 -*-
"""
w2_count_stageA_v1.py -- DECLARE stage for research-publication item 10.

Closes the W1-ROW2 open slot: state M as a history functional and register the
derivation/error of the modelled slice/fragment counts. No measurement here.

Run: python -I src/analysis/w2_count_stageA_v1.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w2_common_v1 as W

ROOT = W.ROOT
D = "runs/W2-COUNT"
PREFIX = "count"
HEAD = ("PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 2.5 item 10, "
        "2.6, 4.8).\nPROVENANCE: NEITHER\n")


def main():
    os.makedirs(os.path.join(ROOT, D), exist_ok=True)
    card = """# Closure card -- W2-COUNT-01

%s
**Question**: are `M` and every slice/fragment count stated at the publication bar (§2.5 item 10)?

## Stipulated inputs
- `M` source: W1-ROW2 manifest line 153 records `M` as a history functional; the full contract is written below.
- count source: `runs/ANALYSIS/front_sweep_v1.txt` lines 10-19 (seven registered z regions and component counts).
- slice count: `N_slices = z_front/delta`, `delta = 0.215 nm`, mechanism property not a rendering knob.
- fragment count: `N_frag = N_slices * <components/layer>`, labelled MODEL ESTIMATE.
- no new physics, no new EOS, no threshold change.

## Derived outputs owed
A five-element `M` contract; weighted mean components/layer; weighted spread; slice/fragment count derivation;
count label and error; verdict against the stage-A predictions.
""" % HEAD
    manifest = W.json_tag({
        "cycle_id": "W2_COUNT_01", "cycle_type": "technical closure",
        "utc": W.utc(), "programme_item": "2.5 item 10",
        "sources": {
            "front_sweep": "runs/ANALYSIS/front_sweep_v1.txt",
            "w1_manifest": "runs/W1-ROW2/row2_manifest_v1.json",
            "programme": "docs/program/RESEARCH_PROGRAM_v1.md",
        },
        "contract_elements": ["history functional", "domain", "units/coordinates",
                              "single-valued", "discarded quantities and ledger"],
        "count_rule": "N_frag = (z_front/delta) * <components/layer>",
    })
    spec = HEAD + """# Solver spec -- W2-COUNT-01

1. The `M` contract is written from §2.6 and the W1 front law; it is not inferred from appearance.
2. The component table is parsed from `runs/ANALYSIS/front_sweep_v1.txt` lines 11-17; no count is retyped.
3. The mean is weighted by each region's z-width, the only registered layer-density weight.
4. The spread is the same weighted standard deviation; it is reported as derivation spread, not promoted to a
   measurement error of the physical phantom.
5. `N_slices` and `N_frag` are recomputed at t_mid from `src/analysis/w1_row2_common_v1.py`; both remain
   MODEL/MECHANISM counts with their derivation attached.
"""
    prediction = W.json_tag({
        "cycle_id": "W2_COUNT_01", "utc": W.utc(),
        "predictions": {
            "N1": "the M contract contains all five elements required by section 2.6",
            "N2": "z-width-weighted mean components/layer reproduces the registered 1.457 to within 0.002",
            "N3": "the weighted spread is nonzero and reported as derivation spread",
            "N4": "N_slices and N_frag are recomputed, labelled, and carry derivation and spread",
        },
        "kill": "any missing M element, or a weighted mean outside 1.457 +/- 0.002",
    })
    registration = """# Pre-registration -- W2-COUNT-01

%s
**Cycle type**: TECHNICAL closure
**Product owed**: `runs/W2-COUNT/count_results_v1.txt`

| id | prediction | falsified if |
|---|---|---|
| N1 | M contract has history functional, domain, units/coordinates, single-valuedness, discard ledger | any element absent |
| N2 | weighted mean components/layer = 1.457 +/- 0.002 | outside the interval |
| N3 | weighted spread is nonzero and labelled derivation spread | spread = 0 or mislabelled |
| N4 | counts are recomputed with derivation and label | any count lacks derivation or label |

## Kill condition

If the weighted mean misses 1.457 +/- 0.002, the cycle records a count-derivation defect against front_sweep_v1;
it does not silently reprice the component rule.

## Scope and barred claims

No claim that the phantom is a real body, that the fragment count is observed, or that the count error is a
physical measurement uncertainty. The spread is a derivation property of the registered region table.
""" % HEAD

    paths = {
        "card": os.path.join(ROOT, D, PREFIX + "_card.md"),
        "manifest": os.path.join(ROOT, D, PREFIX + "_manifest.json"),
        "spec": os.path.join(ROOT, D, PREFIX + "_solver_spec.md"),
        "prediction": os.path.join(ROOT, D, PREFIX + "_prediction.json"),
        "registration": os.path.join(ROOT, D, PREFIX + "_registration.md"),
    }
    W.write_text(paths["card"], card)
    W.write_json(paths["manifest"], manifest)
    W.write_text(paths["spec"], spec)
    W.write_json(paths["prediction"], prediction)
    W.write_text(paths["registration"], registration)
    files = {k: os.path.relpath(v, ROOT) for k, v in paths.items()}
    files.update({
        "shared_module": "src/analysis/w2_common_v1.py",
        "scene_module": "src/analysis/w1_row2_common_v1.py",
        "front_sweep": "runs/ANALYSIS/front_sweep_v1.txt",
        "w1_manifest": "runs/W1-ROW2/row2_manifest_v1.json",
        "programme": "docs/program/RESEARCH_PROGRAM_v1.md",
    })
    lock_path = os.path.join(ROOT, D, PREFIX + "_lock.json")
    W.make_lock("W2_COUNT_01", lock_path, files)
    ok, lines = W.verify_lock(lock_path)
    print("W2-COUNT-01 stage A: %s" % ("LOCK VERIFIED" if ok else "LOCK FAILED"))
    for line in lines:
        print("  " + line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
