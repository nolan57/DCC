# -*- coding: utf-8 -*-
"""
w2_rl1_stageA_v1.py -- DECLARE stage for programme section 6.1 item 6.

RL-1 is re-run here on the row-2 deposit scene (not the stand-in plate scene used
by round 48). No measurement is performed in this stage.

Run: python -I src/analysis/w2_rl1_stageA_v1.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w2_common_v1 as W

ROOT = W.ROOT
D = "runs/W2-RL1"
PREFIX = "rl1"
HEAD = ("PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (section 6.1 item 6, "
        "sections 4.3/4.4/4.7/5.1).\nPROVENANCE: NEITHER\n")


def main():
    os.makedirs(os.path.join(ROOT, D), exist_ok=True)
    card = """# Scene card -- W2-RL1-01

%s
**Item**: 6.1(6) `RL-1` measurement: `Q3` at `θ_fast` on the deposit's own 2D-ified scene.

## Stipulated inputs
- object: row 2 (`C1 C2 ¬C3`) at `t_mid` = 4.0993412372709514e-09 s; front z = 0.869 m.
- field: `plate`: tissue-density index of the axial slice at the front; `canvas`: per-site mean layer density.
- mechanism: one atomic-layer slice (`δ = 0.215 nm`); same map `M` as W1-ROW2.
- constraints: `C1` HELD, `C2` HELD, `C3` VIOLATED (imported 3 ns transient).
- observer `θ`: `q` is the declared channel factor; band = declared density channel (no spectral measurement);
  gate = none; aperture = none; distance = none.
- `E`: declared density field; no radiance environment is substituted, and no `E1` zero-contrast default is used.
- `G`: `G_A` specular-coupled, local normal at zero incidence in the surface frame, `δ_v = 0.01` rad. The
  registered `Q3` estimator has no angular variable, so this pose is declared but integrated out; the result is
  a channel contrast, not evidence that the scene is legible from any particular geometry.
- seed: none (deterministic phantom; null seeds 4000..4015).
- effective 2D: NOT-MEASURED; missing slot = registered confining-potential model; no `IS_2D`/`LOOKS_2D` claim.

## Derived outputs owed
`C_xi` on the row-2 plate, `C*` from the registered flux chain, `q(θ_fast)`, `Q3` at `θ_eye`, `θ_ideal` and
`θ_fast`, the full T0-T3 profile against W1-ROW2, and the kill-condition verdict.
""" % HEAD
    manifest = W.json_tag({
        "cycle_id": "W2_RL1_01", "cycle_type": "technical closure",
        "programme": "docs/program/RESEARCH_PROGRAM_v1.md v1.1.1", "utc": W.utc(),
        "row": 2, "keyframe": "t_mid",
        "scene": "runs/W1-ROW2/row2_tmid.png and its two declared fields",
        "scene_class": "HELD C1 / HELD C2 / VIOLATED C3",
        "q_definition": {
            "theta_eye": 0.0, "theta_ideal": 1.0,
            "theta_fast": "min(1, (C_xi / C*)^2)",
            "source": "runs/LADDER/r1_observer_registration.md section 1",
            "C_star_source": "runs/LADDER/r1_observer_results.txt section 4",
        },
        "theta": {"band": "declared density channel; no spectral measurement",
                  "gate": "none", "aperture": "none", "distance": "none",
                  "E": "declared density field; no radiance substitution",
                  "G": {"id": "G_A", "n_v": "local normal, zero incidence", "delta_v_rad": 0.01,
                        "note": "declared pose integrated out by the registered scalar estimator"}},
        "estimator": W.w1.ESTIMATOR, "null": W.w1.NULL_RECORD,
        "reproduction": "R2 physical quantities; frame reproduction not claimed",
    })
    spec = HEAD + """# Solver spec -- W2-RL1-01

1. `C*` is not re-derived from a new model. It is recovered from the registered shortfall at contrast 1e-7:
   `C* = 1e-7 sqrt(S)`, with `S` read from `runs/LADDER/r1_observer_results.txt`.
2. The row-2 plate field at `t_mid` is regenerated from `src/analysis/w1_row2_common_v1.py`. `xi` and `C_xi`
   come from the locked `src/analysis/tiers_core_v1.py` estimators; no threshold is changed.
3. `q(θ_fast) = min(1, (C_xi/C*)^2)`; `Q3 = log2(1 + C_xi q / C_eye)` with `C_eye = 0.01` from the lock.
4. `T0-T3` at `q=1` are compared with `runs/W1-ROW2/row2_prediction_v1.json`; a verdict flip is a kill.
5. No new frame is rendered. No viewing-geometry claim is made because the estimator has no angular variable.
"""
    prediction = W.json_tag({
        "cycle_id": "W2_RL1_01", "utc": W.utc(),
        "predictions": {
            "R1": "C_xi on the row-2 plate at t_mid exceeds C*, so q(theta_fast) saturates at 1",
            "R2": "Q3(theta_fast) equals Q3(theta_ideal) to 1e-12 and Q3(theta_eye) = 0 exactly",
            "R3": "the T0-T3 profile at q=1 matches the registered W1-ROW2 t_mid profile with no verdict flip",
            "R4": "the shortfall evaluated at C_xi is < 1, i.e. the registered flux gate is already open",
        },
        "kill": "q(theta_fast) < 1, Q3_fast != Q3_ideal within 1e-12, or any tier verdict flip",
    })
    registration = """# Pre-registration -- W2-RL1-01

%s
**Cycle type**: TECHNICAL closure
**Product owed**: `runs/W2-RL1/rl1_results_v1.txt`

| id | prediction | falsified if |
|---|---|---|
| R1 | `q(theta_fast)` saturates at 1 because `C_xi > C*` | `C_xi <= C*`, giving q < 1 |
| R2 | `Q3_fast = Q3_ideal` to 1e-12; `Q3_eye = 0` exactly | either equality fails |
| R3 | T0-T3 at q=1 reproduce the W1-ROW2 t_mid profile; no verdict flip | any value or verdict differs |
| R4 | shortfall at the measured `C_xi` is < 1 | shortfall >= 1 |

## Kill condition

If the kill condition fires, the cycle records RL-1 as FALSIFIED on this scene; no threshold is re-priced and
the old stand-in result is not substituted.

## Scope and barred claims

This is a channel measurement on the deposit's declared field. It is not a new physics result, not an
effective-2D label, not evidence of legibility from a particular viewing geometry, and not an O0 artifact.
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
        "estimator": "src/analysis/tiers_core_v1.py",
        "threshold_lock": "runs/MATRIX/threshold_lock.json",
        "q_registration": "runs/LADDER/r1_observer_registration.md",
        "flux_chain": "runs/LADDER/r1_observer_results.txt",
        "w1_prediction": "runs/W1-ROW2/row2_prediction_v1.json",
    })
    lock_path = os.path.join(ROOT, D, PREFIX + "_lock.json")
    W.make_lock("W2_RL1_01", lock_path, files)
    ok, lines = W.verify_lock(lock_path)
    print("W2-RL1-01 stage A: %s" % ("LOCK VERIFIED" if ok else "LOCK FAILED"))
    for line in lines:
        print("  " + line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
