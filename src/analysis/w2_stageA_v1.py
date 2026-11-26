# -*- coding: utf-8 -*-
"""
w2_stageA_v1.py -- DECLARE stage for the four W2 continuation cycles.

Writes one page cards, machine manifests, solver specs, numeric predictions,
registrations with kill conditions, and hash locks. Nothing is measured here.
Stage B refuses to emit a product if any lock fails.

Run: python -I src/analysis/w2_stageA_v1.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w2_common_v1 as W

ROOT = W.ROOT
DISC = "runs/W2-DISC"
C2 = "runs/W2-C2"
C3 = "runs/W2-C3"
XC = "runs/W2-XCHECK"

HEAD = ("PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 4.2.3, 4.2.6, 4.8, "
        "5.1, 6.1, Appendix D).\nPROVENANCE: NEITHER\n")


def card(cycle, kind, body):
    return ("# Scene / closure card -- %s\n\n%s\n%s\n" % (cycle, HEAD, body))


def manifest(cycle, kind, body):
    obj = {
        "cycle_id": cycle,
        "cycle_type": kind,
        "programme": "docs/program/RESEARCH_PROGRAM_v1.md v1.1.1",
        "utc": W.utc(),
    }
    obj.update(body)
    return W.json_tag(obj)


def registration(cycle, kind, product, predictions, kill, scope):
    rows = "\n".join("| %s | %s | %s |" % (a, b, c) for a, b, c in predictions)
    return ("# Pre-registration -- %s\n\n%s\n**Cycle type**: %s  \n**Product owed**: `%s`\n\n"
            "## Numeric predictions (fixed before any stage-B run)\n\n"
            "| id | prediction | falsified if |\n|---|---|---|\n%s\n\n"
            "## Kill condition\n\n%s\n\n## Scope and barred claims\n\n%s\n"
            % (cycle, HEAD, kind, product, rows, kill, scope))


def write_set(d, prefix, kind, card_body, man_body, spec, prediction, pred_rows, kill, scope, extra=None):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    paths = {}
    paths["card"] = W.write_text(os.path.join(ROOT, d, prefix + "_card.md"),
                                 card(d.split("/")[-1].replace("-", "_"), kind, card_body))
    paths["manifest"] = W.write_json(os.path.join(ROOT, d, prefix + "_manifest.json"),
                                     manifest(d.split("/")[-1].replace("-", "_"), kind, man_body))
    paths["spec"] = W.write_text(os.path.join(ROOT, d, prefix + "_solver_spec.md"), spec)
    paths["prediction"] = W.write_json(os.path.join(ROOT, d, prefix + "_prediction.json"),
                                       W.json_tag(prediction))
    paths["registration"] = W.write_text(
        os.path.join(ROOT, d, prefix + "_registration.md"),
        registration(d.split("/")[-1].replace("-", "_"), kind,
                     "runs/%s/%s_results.txt" % (d, prefix), pred_rows, kill, scope))
    paths["shared_module"] = os.path.join(ROOT, "src", "analysis", "w2_common_v1.py")
    files = {k: os.path.relpath(v, ROOT) for k, v in paths.items()}
    files["threshold_lock"] = os.path.relpath(W.LOCK, ROOT)
    if extra:
        files.update(extra)
    lock = os.path.join(ROOT, d, prefix + "_lock.json")
    return W.make_lock(d.split("/")[-1].replace("-", "_"), lock, files)


def main():
    w1 = "src/analysis/w1_row2_common_v1.py"
    conv = "src/common/conv.py"
    tl = "runs/MATRIX/threshold_lock.json"

    # ---------------------------------------------------------------- W2-DISC-01
    disc_body = """**Item**: 6.1(3) discretization control. **Type**: TECHNICAL closure, not an O0 artifact.

- baseline mechanism: one atomic layer per slice, delta = 0.215 nm (front_sweep_v1; a mechanism property, not a rendering knob).
- control mechanism: delta x 10 = 2.150 nm, same front law and same map M; registered as a DIFFERENT mechanism id, not a parameter edit (section 4.8).
- scene: row 2 (`C1 C2 not-C3`) at `t_mid` = 4.0993412373e-09 s; z_front = 0.869 m.
- constraints: C1 HELD, C2 HELD, C3 VIOLATED (imported 3 ns transient, unchanged by the control).
- observer: the declared instrumented channel q = 1; tiers T0-T3 from the locked estimators and thresholds.
- seed: none (deterministic phantom and null ensemble seeds 4000..4015).
- predicted direction: plate-scale tiers invariant; array-scale census and its tiers change because site count scales as 1/delta.
"""
    disc_man = {
        "row": 2,
        "keyframe": "t_mid",
        "mechanism_baseline": {"id": "atomic-layer-slice-v1", "delta_m": 0.215e-9},
        "mechanism_control": {"id": "atomic-layer-slice-v1-delta10", "delta_m": 2.150e-9},
        "front_law": "z_f = min(H, c t / sqrt(2))",
        "map": "M assigns layer k to site k in raster order (bijection); unchanged",
        "constraints": {"C1": "HELD", "C2": "HELD", "C3": "VIOLATED (IMPORTED tau_life)"},
        "theta": {"q": 1.0, "band": "declared density channel, no spectral measurement",
                  "gate": "none", "aperture": "none", "distance": "none",
                  "E": "not applicable to a density channel", "G": "not applicable"},
        "estimator": W.w1.ESTIMATOR,
        "null": W.w1.NULL_RECORD,
        "deterministic_seed": "phantom fixed; null seeds 4000..4015",
    }
    disc_spec = HEAD + """# Solver spec -- W2-DISC-01

1. **What is solved.** No equation of motion. The registered phantom is sampled; the control replaces one layer by a ten-layer z-window average at the same front position. Counts are recomputed from N = z_f / delta and N_frag = N x 1.457.
2. **Fields.** `plate`: tissue-density index of the axial slice at z_f. `canvas`: per-site mean layer density downsampled to 128^2; its fill is z_f/(H) in the baseline and 10x smaller in the control because the site census is 10x smaller.
3. **Estimators.** `src/analysis/tiers_core_v1.py` verbatim, thresholds and constants read from runs/MATRIX/threshold_lock.json; grid 128^2, bins 64, context 16, DoG sigma = xi/2 and 2 xi.
4. **Floor.** The deterministic repeat of the baseline field is the instrument floor (byte-identical, tier ratios exactly 1). A control difference at or below that floor is NO-OBSERVED-EFFECT, not a pass awarded after seeing the number.
5. **Judged quantities.** deposited mass/volume, front position, sheet/plate/fragment census, conserved-integral residual, and both fields' T0-T3 profiles. Appearance is not evidence.
6. **Status vocabulary.** PASS / FAIL / REFUSED / NOT-APPLICABLE / NOT-MEASURED stay distinct; a NO-VERDICT tier is not a FAIL.
"""
    disc_pred = {
        "cycle_id": "W2_DISC_01",
        "utc": W.utc(),
        "delta_ratio_control_over_baseline": 10.0,
        "predictions": {
            "D1": "plate field byte-identical; all four plate tier values equal to the baseline within the deterministic floor (ratio 1.0)",
            "D2": "layer, sheet and fragment counts scale by exactly 0.1 +/- 1e-12 relative",
            "D3": "canvas fill at t_mid scales by 0.1 +/- 1e-12; canvas correlation length increases by at least 20 percent",
            "D4": "deposited mass/volume and front position unchanged to 1e-12 relative; conserved residual 0",
        },
        "kill": "any plate tier verdict flip, any nonzero conservation residual, or a census ratio outside 0.1 +/- 1e-12",
    }
    disc_rows = [
        ("D1", "plate sha256 equal; tier ratios = 1.0 +/- floor", "any plate byte difference or verdict flip"),
        ("D2", "N_slices, plates and fragments x 0.1 (rel. err < 1e-12)", "ratio outside 0.1 +/- 1e-12"),
        ("D3", "canvas fill x 0.1; xi_canvas rises >= 20%", "fill ratio wrong or xi not increased"),
        ("D4", "mass, volume, z_front unchanged (< 1e-12); residual 0", "any drift or nonzero residual"),
    ]
    write_set(DISC, "disc", "technical closure", disc_body, disc_man, disc_spec, disc_pred,
              disc_rows,
              "If the kill condition fires, the cycle closes with the NEGATIVE result 'the plate result is discretization-dependent'; it is not re-labelled a pass and no threshold is re-priced.",
              "No frame is claimed, no O0 artifact is claimed, no visibility or realizability claim is made. The control is a different mechanism id (delta x 10), not a rendering of the baseline.",
              extra={"scene_module": w1})

    # ---------------------------------------------------------------- W2-C2VIOL-01
    c2_body = """**Item**: 6.1(4) `¬C2` branch. **Type**: artifact cycle for row 4 (`C1 not-C2 not-C3`).

- scene: the row-2 phantom and front law, with the declared non-isometric map `(x,y) -> (1.01 x, 1.01 y)` applied to the deposit plane.
- constraints: C1 HELD via the pushforward `Sigma'(x') = Sigma(x'/s)/s^2`; C2 VIOLATED by s = 1.01; C3 VIOLATED by the same imported 3 ns transient as row 2.
- price record (section 3.5): clause = C2 injectivity/isometry of the intralayer map; Pi_raw = det J = 1.0201 (area factor); Pi = 0.0201; O_detect = conservation ledger and autocorrelation scale; F = shift of xi relative to row 2 at t_mid.
- observer: declared instrumented channel q = 1; q = 0 reflected channel reported separately and not used as a scene verdict.
- keyframes: t0, t_mid, t_end (the row-2 slots), plus a three-frame sequence with a declared compression.
- seed: none (deterministic).
"""
    c2_man = {
        "row": 4,
        "row_label": "C1 not-C2 not-C3",
        "scene_class": "VIOLATION(C2)",
        "constraints": {"C1": "HELD (pushforward)", "C2": "VIOLATED (s=1.01)",
                        "C3": "VIOLATED (IMPORTED tau_life)"},
        "map": {"id": "uniform-dilation-v1", "s": 1.01, "detJ": 1.0201,
                "domain": "deposit plane, registered 128x128 window",
                "multi_valued": False,
                "boundary_rule": "zero-width window; image outside it is booked as OUTFLOW",
                "discarded": "mass leaving the registered window (booked, not silently dropped)"},
        "price_record": {"clause_relaxed": "C2 intralayer isometry",
                         "Pi_raw": 1.0201, "Pi": 0.0201,
                         "O_detect": "conservation ledger and T1 autocorrelation scale",
                         "F": "xi shift against row 2 at t_mid"},
        "theta": {"q": 1.0, "q_reflection": 0.0,
                  "band": "declared density channel; no spectral measurement",
                  "gate": "none", "aperture": "none", "distance": "none",
                  "E": "not applicable to a density channel", "G": "not applicable"},
        "keyframes": {"t0": 0.0, "t_mid": 4.0993412372709514e-09, "t_end": 8.198682474541903e-09},
        "estimator": W.w1.ESTIMATOR,
        "null": W.w1.NULL_RECORD,
    }
    c2_spec = HEAD + """# Solver spec -- W2-C2VIOL-01

1. **What is solved.** No PDE. The row-2 field at each keyframe is pushed forward by the declared dilation; conservation is exact on the finite window by area-overlap apportionment plus an explicit OUTFLOW ledger.
2. **Grid / boundary.** 128^2 cells, unit cell in the registered window; dilation about the origin; cells whose image crosses x>=128 or y>=128 contribute OUTFLOW.
3. **Estimators.** `src/analysis/tiers_core_v1.py`, thresholds from runs/MATRIX/threshold_lock.json. Each cell records estimator id, threshold, q, seed, and source hashes.
4. **Profiles.** T0-T3 on `plate` (stretched) and `canvas` (unchanged, declared out of scope of the dilation) at t0 / t_mid / t_end; t0 cells stay NOT-APPLICABLE because no 2D output exists before the front.
5. **Effective 2D.** Three labels recorded separately; the missing model slot is named, so the label is NOT-MEASURED and no IS_2D / LOOKS_2D claim follows.
6. **Reproduction.** R2 for physical quantities; frame reproduction (R3) not claimed.
"""
    c2_pred = {
        "cycle_id": "W2_C2VIOL_01",
        "utc": W.utc(),
        "s": W.S_STRETCH,
        "detJ": W.S_STRETCH ** 2,
        "predictions": {
            "S1": "det J = 1.0201 and area change = +2.01% exactly",
            "S2": "conservation residual on the full (window + outflow) ledger < 1e-12; within-window deficit about 2%",
            "S3": "plate autocorrelation length xi scales by s within [0.99, 1.03] of the row-2 value",
            "S4": "T0, T2, T3 verdicts at t_mid remain PASS; canvas profile unchanged",
        },
        "row2_tmid_reference": "runs/W1-ROW2/row2_prediction_v1.json (plate xi = 21.85984947 cells)",
    }
    c2_rows = [
        ("S1", "det J = 1.0201, area change +2.01%", "any other value"),
        ("S2", "full-ledger residual < 1e-12; window deficit about 2%", "residual >= 1e-12 or missing outflow"),
        ("S3", "xi ratio in [0.99, 1.03]", "ratio outside the interval"),
        ("S4", "T0/T2/T3 PASS at t_mid; canvas profile identical", "verdict flip or canvas change"),
    ]
    write_set(C2, "c2", "artifact cycle", c2_body, c2_man, c2_spec, c2_pred, c2_rows,
              "If the conservation ledger fails or xi does not scale with s, the branch is recorded as FALSIFIED; the row is not withdrawn and no threshold is re-priced.",
              "COUNTERFACTUAL(C3) is not claimed: C3 is VIOLATED here. The stretch is a hard-SF priced violation, not a visibility, readability, realizability or identity claim. Frames without their sidecars are not citable.",
              extra={"scene_module": w1})

    # ---------------------------------------------------------------- W2-C3TEST-01
    c3_body = """**Item**: 6.1(5) C3 consumption test. **Type**: TECHNICAL closure.

- question: for held vs neutronized C3 at t_mid, which state variables change, and does u encode them?
- held branch: frozen Z/A = 0.522 (counterfactual, since C3 is in-action NO-GO); neutronized branch: beta equilibrium in the three registered conventions (ALL3D, HYB, ALL2D).
- closure scope (section 4.2.6): composition and occupation scale only. sigma_s(omega) is NOT-MEASURED (no compliant sigma_s exists: G6/DC2); t_life is IMPORTED 3 ns, not derived; the neutrino luminosity ledger is OUT-OF-SCOPE. No optical or shutdown claim follows.
- u: the row-2 plate and canvas fields at t_mid, byte-compared across branches.
- seed: none (deterministic).
"""
    c3_man = {
        "question": "which C3 variables change and are they consumed by the row-2 u generator?",
        "branches": {"HELDC3_counterfactual": "frozen Z/A",
                     "NEUTRONIZED": "conv.beta_envelope over ALL3D, HYB, ALL2D"},
        "state_vector": ["Y_e", "n_e", "E_F", "sigma_s", "t_life", "L_nu"],
        "closure_scope": {
            "in_scope": ["Y_e", "n_e", "E_F / mu_e", "u byte identity", "generator graph"],
            "out_of_scope": ["sigma_s(omega) (G6/DC2 blocker)", "derived t_life", "L_nu energy ledger"],
        },
        "t_life_s_imported": 3.0e-9,
        "theta": {"q": 1.0, "band": "declared density channel", "E": "not applicable", "G": "not applicable"},
        "keyframe": "t_mid",
        "sources": {"conv": conv, "scene": w1},
    }
    c3_spec = HEAD + """# Solver spec -- W2-C3TEST-01

1. **What is solved.** No dynamics. `conv.frozen_state()` and `conv.beta_envelope()` supply the registered electron states; no EOS is written here and no tau is scanned.
2. **Convention envelope.** All three MODES are reported; a single-convention number is never used as the answer (conv.py module header; dimensional_conventions_v1.md section 5).
3. **Graph evidence.** The source of `plate_field` and `canvas_field` is scanned for composition tokens. Byte identity of u alone is NOT accepted as proof of non-consumption (section 1.1 / 4.6).
4. **C3 slots.** sigma_s is NOT-MEASURED; t_life is IMPORTED; L_nu is OUT-OF-SCOPE. These are recorded as separate slots, not merged into a PASS.
5. **Verdict vocabulary.** GENERATOR-DOES-NOT-CONSUME requires graph absence; otherwise NO-OBSERVED-EFFECT is recorded.
"""
    c3_pred = {
        "cycle_id": "W2_C3TEST_01",
        "utc": W.utc(),
        "predictions": {
            "C1": "Y_e and n_e decrease under neutronization in all three conventions",
            "C2": "mu_kin decreases; the ratio follows (n_e_neut / n_e_frozen)^(2/3) in the 2D kinetic convention",
            "C3": "u fields are byte-identical across branches (same sha256)",
            "C4": "composition tokens are absent from both field generators -> GENERATOR-DOES-NOT-CONSUME",
        },
        "kill": "any composition token found in a field generator, or any byte difference in u with no declared mechanism",
    }
    c3_rows = [
        ("C1", "Y_e and n_e fall in ALL3D / HYB / ALL2D", "any convention with n_e >= frozen"),
        ("C2", "mu_kin falls; 2D kinetic ratio follows n_e^(2/3)", "ratio disagrees beyond rounding"),
        ("C3", "plate and canvas sha256 identical across branches", "any byte difference"),
        ("C4", "graph check ABSENT-FROM-GRAPH", "any token hit -> NO-OBSERVED-EFFECT instead"),
    ]
    write_set(C3, "c3", "technical closure", c3_body, c3_man, c3_spec, c3_pred, c3_rows,
              "If a composition token is found in u's generator, GENERATOR-DOES-NOT-CONSUME is refused and NO-OBSERVED-EFFECT is recorded with the missing encoding named.",
              "No visibility, optical, effective-2D or realizability claim. C3 held is a counterfactual branch; the neutronized branch is not a prediction of a realizable process.",
              extra={"conv": conv, "scene": w1})

    # ---------------------------------------------------------------- W2-XCHECK-01
    xc_body = """**Item**: Appendix D evidence-boundary cross-check (declared TECHNICAL under section 5.1).

- four authoritative objects that this programme does not supersede: constraint_crosswalk_v1, intrinsic_structure_tiers_v1, relaxation_ladder_v1, COMPLETION_PROTOCOL_v1.
- question: do the contracts this programme cites actually match the objects, without editing any of them?
- the check is structural: identifiers, threshold values, rung count, price fields, WIP and gate mode. No physics is re-derived.
"""
    xc_man = {
        "question": "do the four unsuspended authorities satisfy the contracts cited by RESEARCH_PROGRAM_v1?",
        "authorities": [
            "docs/conventions/constraint_crosswalk_v1.md",
            "docs/specs/intrinsic_structure_tiers_v1.md",
            "docs/specs/relaxation_ladder_v1.md",
            "docs/program/COMPLETION_PROTOCOL_v1.md",
        ],
        "mode": "structural read only; no authority is edited",
    }
    xc_spec = HEAD + """# Solver spec -- W2-XCHECK-01

1. Each authority is read byte-wise; only presence and consistency of named fields are checked.
2. Tier thresholds in the spec are compared with runs/MATRIX/threshold_lock.json to 1e-12.
3. Ladder rung identifiers RL-1..RL-6 and the four price-record fields are counted; a missing price is reported as UNSPECIFIED, never invented.
4. The protocol's WIP and report-only gate statements are located as text; no gate mark is changed.
5. A mismatch is a finding about the programme's citation, not a redefinition of an authority.
"""
    xc_pred = {
        "cycle_id": "W2_XCHECK_01",
        "utc": W.utc(),
        "predictions": {
            "X1": "C1/C2/C3 are present as constraint identifiers in the crosswalk",
            "X2": "T0..T3 threshold values in the spec match the lock (0.5, 4.0, 0.5, 2.0) to 1e-12",
            "X3": "the ladder declares six rungs RL-1..RL-6 and each has a price field",
            "X4": "the protocol declares WIP = 1 and the instruments are report-only",
        },
        "kill": "a missing identifier, a threshold mismatch, or a rung with no price field",
    }
    xc_rows = [
        ("X1", "C1, C2, C3 all found in crosswalk", "any identifier absent"),
        ("X2", "four thresholds match the lock", "any mismatch > 1e-12"),
        ("X3", "six rungs, each with a price", "missing rung or price"),
        ("X4", "WIP = 1 and report-only statement found", "either absent"),
    ]
    write_set(XC, "xcheck", "technical closure", xc_body, xc_man, xc_spec, xc_pred, xc_rows,
              "A mismatch closes the cycle with a citation defect recorded against this programme; it does not license editing an authority.",
              "No new definition, no threshold change, no gate mark, no visibility claim.",
              extra={"lock": tl})

    print("w2 stage A: four cycles declared")
    for d, prefix in ((DISC, "disc"), (C2, "c2"), (C3, "c3"), (XC, "xcheck")):
        ok, lines = W.verify_lock(os.path.join(ROOT, d, prefix + "_lock.json"))
        print("%s lock %s" % (d, "VERIFIED" if ok else "FAILED"))
        for line in lines:
            print("   " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
