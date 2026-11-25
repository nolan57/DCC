# -*- coding: utf-8 -*-
"""
w1_row2_scene_v1.py -- STAGE A of the W1 / row-2 artifact cycle: pre-registration.

Writes, and then hash-locks, everything the frame is allowed to show:

    row2_scene_card_v1.md      one page: object, mechanism, constraints, theta, M, ledger
    row2_manifest_v1.json      every parameter with units and domain; theta expanded
    row2_solver_spec_v1.md     what is solved, what is interpolated, what is OUT-OF-SCOPE
    row2_prediction_v1.json    the predicted T0-T3 profile and the derived scalars
    row2_lock_v1.json          sha256 of the four above plus the shared module
    row2_lock_v1.sha256        sha256 of the lock file itself

Nothing is rendered here. RESEARCH_PROGRAM_v1 v1.1.1 section 2.5(1) requires the
card and manifest to be complete and hash-locked *before* rendering; stage B
(src/analysis/w1_row2_cycle_v1.py) refuses to draw if the hash does not match.

Run: python -I src/analysis/w1_row2_scene_v1.py
"""

import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import w1_row2_common_v1 as C

OUTDIR = os.path.join(ROOT, "runs", "W1-ROW2")
os.makedirs(OUTDIR, exist_ok=True)

UTC = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
CYCLE_ID = "W1-ROW2-ARTIFACT-01"

STATES = [
    ("t0", C.T0_S, C.state_at(C.T0_S)),
    ("t_mid", C.T_MID_S, C.state_at(C.T_MID_S)),
    ("t_end", C.T_END_S, C.state_at(C.T_END_S)),
]

# ---------------------------------------------------------------------------
# predicted profile (no rendering)
# ---------------------------------------------------------------------------
pred_rows = []
pred_meta = {}
for tag, t, st in STATES:
    if tag == "t0":
        for field in ("plate", "canvas"):
            for tier in ("T0", "T1", "T2", "T3"):
                pred_rows.append(dict(keyframe=tag, field=field, tier=tier, value=None,
                                      threshold=C.THR["L" + tier[1]],
                                      verdict="NOT-APPLICABLE", status="NOT-APPLICABLE",
                                      note="no 2D output before the front arrives"))
        pred_meta[tag] = {}
        continue
    zrep = min(st["zf"], 1.700)
    fields = {
        "plate": C.plate_field(st["zf"]),
        "canvas": C.canvas_field(st),
    }
    pred_meta[tag] = {}
    for field, u in fields.items():
        rows, meta = C.measure(u, "%s@%s" % (field, tag))
        pred_meta[tag][field] = meta
        for r in rows:
            pred_rows.append(dict(keyframe=tag, field=field, tier=r["tier"],
                                  value=r["value"], threshold=C.THR["L" + r["tier"][1]],
                                  verdict=r["verdict"], status=r["status"], note=r["note"]))

# ---------------------------------------------------------------------------
# ledger
# ---------------------------------------------------------------------------
def ledger(st):
    """Volume/mass ledger; C1 held means deposit = swept exactly, decay is a boundary termination."""
    return dict(
        t_s=st["t"], z_front_m=st["zf"],
        V_swept_m3=st["V_swept"], m_swept_kg=st["m_swept"],
        V_deposited_m3=st["V_swept"], m_deposited_kg=st["m_swept"],
        V_decayed_m3=st["V_decayed"], m_decayed_kg=st["m_decayed"],
        V_live_m3=st["V_live"], m_live_kg=st["m_live"],
        sheet_count=st["layers"], fragment_count=st["plates"],
        residual_m3=st["V_swept"] - st["V_swept"],
        closure="deposited == swept (identity, residual 0 by construction; C1 HELD)",
        decay_route=("decayed mass terminates the 2D domain and leaves to a 3D reservoir; the reservoir "
                     "budget is OUT-OF-SCOPE for this cycle because the 3 ns lifetime is IMPORTED"),
    )

LEDGER = {tag: ledger(st) for tag, _t, st in STATES}

# ---------------------------------------------------------------------------
# manifest
# ---------------------------------------------------------------------------
THETA = dict(
    q=dict(value=1.0, unit="dimensionless photon budget", domain="[0, inf); 0 = naked-eye reflected channel",
           source="intrinsic_structure_tiers_v1 section 5; declared instrument"),
    band=dict(value="declared density channel", unit="none", domain="no spectral band is claimed",
              source="the field is a tissue-density index, not a radiance"),
    gate=dict(value=3.0e-9, unit="s", domain="(0, inf)",
              source="scifi_boundary_v1 3 ns transient gate (IMPORTED)"),
    aperture=dict(value=0.10, unit="m", domain="(0, inf)", source="declared instrument (not solved)"),
    distance=dict(value=1.0, unit="m", domain="(0, inf)", source="declared viewing distance (not solved)"),
    E=dict(value="flat, dark, room temperature", unit="none", domain="declared environment",
           source="no illumination model is used: the frame is not a radiance render"),
    G=dict(value="linear greyscale/violet density transfer, no tone curve",
           unit="none", domain="declared camera/transfer model",
           source="declared; differs from theta_camera_v1's specular/fixed geometries because no "
                  "reflection is computed"),
)

MANIFEST = dict(
    cycle_id=CYCLE_ID,
    cycle_type="artifact",
    programme=dict(path="docs/program/RESEARCH_PROGRAM_v1.md", version="v1.1.1",
                   sections="2.5, 2.6, 4.2-4.8, 5.3, 6.1"),
    utc=UTC,
    row=dict(index=2, label="C1 C2 not-C3", scene_class="CONSTRUCTIVE",
             constraints=dict(C1="HELD", C2="HELD", C3="VIOLATED"),
             c3_note=("C3 is violated by a declared 3 ns transient, not by a computed decay: the "
                      "lifetime is IMPORTED from scifi_boundary_v1's npe branch and is not derived "
                      "from this state's energy ledger (RESEARCH_PROGRAM_v1 section 4.2.6 marks that "
                      "derivation OUT-OF-SCOPE here)")),
    object=dict(height_m=C.H_BODY, registered_volume_m3=C.V_REG,
                reconstructed_volume_m3=C.V_RECON,
                reconstruction_ratio=C.V_RECON / C.V_REG,
                shape="synthetic whole-body phantom (src/analysis/unfold_appearance_v1.py slice_at)",
                density_kg_m3=C.RHO_DECL,
                density_note="declared uniform; the phantom's tissue classes are used for the field, not for the mass"),
    mechanism=dict(
        id="front_sweep_v1", version="v1 (unchanged)",
        front_law="z_f(t) = min(H, v t), v = c/sqrt(2) = %.6e m/s" % C.V_FRONT,
        layer_thickness_m=C.DELTA,
        components_per_layer=C.COMP_PER_LAYER,
        plate_census=C.N_PLATE,
        registered_peelings=C.N_SLICE_REG,
        array=dict(sites_per_side=C.SIDE_REG, spacing_m=C.SPACING, canvas_m=C.CANVAS,
                   sites_total=float(C.SIDE_REG ** 2)),
        t_rip_s=C.T_RIP,
        transient=dict(tau_s=C.TAU_C3, status="IMPORTED",
                       source="docs/decisions/scifi_boundary_v1.md (3-5 ns), lower bound taken"),
    ),
    map_M=dict(
        form="u(t) = M[U(tau), phi(tau); 0 <= tau <= t]",
        domain="the swept slab z in [0, z_f(t)] of U; z outside it is untouched and absent from u",
        coordinates="u on the body cross-section uses (x,y) in m centred on the slice; u on the array uses raster site index",
        single_valued="YES, by a declared bijection: layer k -> site k in raster order. One layer occupies one site.",
        competition_rule=("no layer competes for a site: the 1.457 components are the pieces of ONE layer "
                          "sharing that layer's single site, so the site holds 1 or 2 fragments of the same slice"),
        markov="NO as written. History enters through the accumulated deposit and the interface position. "
               "With the extended state (deposited field, z_f, decayed front z_f - v tau) the map is "
               "instantaneous; that extended state is declared, not proved minimal.",
        discards=["mass (ledger row m_decayed)", "particle number (tied to mass)",
                  "energy (OUT-OF-SCOPE: no energy equation is solved)",
                  "momentum (OUT-OF-SCOPE)", "phase (OUT-OF-SCOPE)",
                  "per-site fragment multiplicity beyond the mean 1.457 (recorded as a count, not a field)"],
    ),
    theta=THETA,
    estimator=C.ESTIMATOR,
    null_ensemble=C.NULL_RECORD,
    discretization=dict(
        declaration="one atomic layer per slice (the registered mechanism)",
        control="NOT RUN in this cycle (delta x 10 control is programme item 6.1(3), OPEN)",
        slice_count_note="8.12e9 is derived as H/delta for this mechanism, not chosen",
        fragment_count_note=("1.18e10 = 8.12e9 x 1.457 is a MODEL ESTIMATE: 1.457 is measured on the "
                             "200^2 phantom but its sample size, per-region variance and the weighting of "
                             "the leg/neck/head regions are NOT in the registered record"),
    ),
    acceptance=dict(
        o0_minimum_items={
            "1_card_and_manifest_locked_before_rendering": "PASS (this lock)",
            "2_three_keyframes": "PASS (t0, t_mid, t_end)",
            "3_display_declaration_label_profile_slot": "PASS (measured profile; stage B emits the sidecars)",
            "4_constraint_state_and_consequence_visible": "PASS (caption line on every frame)",
            "5_third_party_reproduction": "R2 only; no frame reproduction is claimed",
        },
        publication_items={
            "6_profile_with_estimator_identity": "PASS",
            "7_discretization_error_or_convergence": "FAIL -- the delta x 10 control is not run",
            "8_conservation_ledger": "PASS (volume/mass ledger closes by construction)",
            "9_price_ledger": "NOT APPLICABLE -- this row uses no relaxation rung",
            "10_M_and_count_error": "PARTIAL -- M is stated as a history functional; the fragment count is "
                                    "labelled MODEL ESTIMATE and its sampling error is unregistered",
        },
        verdict="O0-ARTIFACT",
        verdict_reason="items 7 and 10 are not satisfied, so the cycle may not be labelled RESULT",
    ),
)

# ---------------------------------------------------------------------------
# scene card
# ---------------------------------------------------------------------------
def fmt(v, nd=6):
    if v is None:
        return "-"
    if isinstance(v, str):
        return v
    return ("%%.%de" % nd) % v if (abs(v) >= 1e5 or (v != 0 and abs(v) < 1e-3)) else ("%%.%df" % nd) % v


card = []
A = card.append
A("# Scene card — W1 / row 2 (`C1 C2 ¬C3`), %s" % CYCLE_ID)
A("")
A("**Status**: O0-ARTIFACT (pre-registration, stage A). Nothing is rendered yet; the hashes below")
A("are the lock that stage B verifies before drawing.")
A("**Programme**: `docs/program/RESEARCH_PROGRAM_v1.md` v1.1.1, sections 2.5, 2.6, 4.2–4.8, 6.1.")
A("**Created (UTC)**: %s" % UTC)
A("")
A("---")
A("")
A("## 1. Row and scene class")
A("")
A("| field | value |")
A("|---|---|")
A("| row | 2 — `C1 C2 ¬C3` |")
A("| scene class | `CONSTRUCTIVE` (no counterfactual is used; `C3` is violated, not held) |")
A("| `C1` | **HELD** — layer→site is a declared bijection; deposit volume = swept volume, residual 0 |")
A("| `C2` | **HELD** — no map is applied; the intralayer (x,y) identity is used, det J = 1 |")
A("| `C3` | **VIOLATED** — a 3 ns transient ends the 2D state; the lifetime is IMPORTED, not derived |")
A("")
A("`C3` consequence at each keyframe (the state is fixed; only the consequence moves):")
A("")
A("| keyframe | t (ns) | z front (m) | sheets | fragments | decayed fraction of deposit |")
A("|---|---|---|---|---|---|")
for tag, t, st in STATES:
    dec = st["V_decayed"] / st["V_swept"] if st["V_swept"] > 0 else 0.0
    A("| `%s` | %.3f | %.4f | %.4e | %.4e | %.3f |"
      % (tag, t / 1e-9, st["zf"], st["layers"], st["plates"], dec))
A("")
A("The 3 ns transient is shorter than the 8.1987 ns sweep, so the last frame cannot show a surviving")
A("deposit: everything swept earlier than `t_end − τ` has already left the 2D state. That is the")
A("`¬C3` consequence, and it is why this row is published as an artifact rather than as a process")
A("that completes.")
A("")
A("## 2. Object")
A("")
A("- height `H = %.3f m`; registered volume `%.4f m^3` (`front_sweep_v1` section 1 self-check)." % (C.H_BODY, C.V_REG))
A("- cross-section: the registered per-region table, **with the two-leg region counted twice**.")
A("  The reconstruction integrates to `%.5f m^3` = `%.4f ×` the registered volume." % (C.V_RECON, C.V_RECON / C.V_REG))
A("- density: declared uniform `%.1e kg/m^3` for the mass ledger only; the field uses the phantom's" % C.RHO_DECL)
A("  tissue classes.")
A("")
A("> **Reconciliation note (new).** `runs/FRONT/mid_sweep_frame_results.txt` N9′ reports the")
A("> reconstruction as `0.04992 m^3`, 16.9% below the registered `0.0601`, and withholds the volume")
A("> fraction for that reason. Counting the calf→thigh table as *per-piece* area (two legs) gives")
A("> `%.5f m^3`, i.e. `%.1f%%` above the registered value. The 16.9%% gap is the missing factor of two," % (C.V_RECON, 100.0 * (C.V_RECON / C.V_REG - 1.0)))
A("> not a defect of the table. N9′ is not edited here (retirement rules: append, do not delete);")
A("> this card records the explanation and stage B carries it into the results text.")
A("")
A("## 3. Mechanism")
A("")
A("| parameter | value | source |")
A("|---|---|---|")
A("| layer thickness `δ` | `0.215 nm` | `front_sweep_v1` §2 (mechanism property, not a knob) |")
A("| components per layer | `1.457` | `front_sweep_v1` §1, 200² phantom |")
A("| plate census | `1.18e10` | derived: `8.12e9 × 1.457` |")
A("| front law | `z_f = min(H, v t)`, `v = c/√2` | `front_sweep_v1` §2 |")
A("| `t_rip` | `%.6e s` | derived |" % C.T_RIP)
A("| transient `τ` | `3.0e-9 s` | **IMPORTED** `scifi_boundary_v1` (3–5 ns, lower bound) |")
A("")
A("## 4. The map `M` (programme §2.6)")
A("")
A("```")
A("u(t) = M[ U(τ), φ(τ); 0 ≤ τ ≤ t ]")
A("```")
A("")
A("- **domain**: the swept slab `z ∈ [0, z_f(t)]`; material above the front is absent from `u`.")
A("- **coordinates**: body cross-section `(x,y)` in m about the slice centre; array field in raster site index.")
A("- **single-valued**: yes, by a declared bijection `layer k ↦ site k` (raster order).")
A("- **competition**: none across layers. The `1.457` components are pieces of *one* layer sharing its")
A("  single site, so a site holds 1 or 2 fragments of the same slice.")
A("- **Markov**: no. History enters through the accumulated deposit and the decayed front. With the")
A("  extended state `(deposited field, z_f, z_f − vτ)` the map is instantaneous; minimality is not proved.")
A("- **discards**: mass (ledger), particle number (via mass), energy / momentum / phase (`OUT-OF-SCOPE`),")
A("  per-site fragment multiplicity beyond the mean (recorded as a count, not a field).")
A("")
A("## 5. Conservation ledger (programme §4.2.3)")
A("")
A("| keyframe | `V_swept` (m³) | `V_deposited` (m³) | `V_decayed` (m³) | `V_live` (m³) | residual |")
A("|---|---|---|---|---|---|")
for tag, _t, st in STATES:
    L = LEDGER[tag]
    A("| `%s` | %s | %s | %s | %s | %.1e |"
      % (tag, fmt(L["V_swept_m3"]), fmt(L["V_deposited_m3"]), fmt(L["V_decayed_m3"]),
         fmt(L["V_live_m3"]), L["residual_m3"]))
A("")
A("`C1` is held, so `V_deposited = V_swept` exactly and the residual is 0 by construction, not by")
A("measurement. The decayed volume leaves the 2D domain as a boundary termination; the receiving 3D")
A("reservoir's budget is `OUT-OF-SCOPE` because `τ` is imported. Energy, momentum and phase are not")
A("modelled and are entered here as `OUT-OF-SCOPE` rather than omitted.")
A("")
A("## 6. Observer `θ`")
A("")
A("| slot | value | unit / domain |")
A("|---|---|---|")
for k, v in THETA.items():
    A("| `%s` | %s | %s |" % (k, v["value"], v["unit"]))
A("")
A("`q = 1` is a declared instrument. `q = 0` (naked-eye reflected channel) is a different cell and is")
A("reported in the profile as `Q3 = 0` by the authority's registration, not by this cycle.")
A("")
A("## 7. Predicted profile (frozen before rendering)")
A("")
A("| keyframe | field | tier | value | threshold | verdict |")
A("|---|---|---|---|---|---|")
for r in pred_rows:
    A("| `%s` | %s | %s | %s | %.2f | %s |"
      % (r["keyframe"], r["field"], r["tier"], fmt(r["value"]), r["threshold"], r["verdict"]))
A("")
A("Estimator: %s. Reference ensemble: %s." % (C.ESTIMATOR["identity"], C.ESTIMATOR["null_ensemble"]))
A("Threshold lock `sha256 = %s…`." % C.LOCK_SHA[:16])
A("")
A("The prediction is a **freeze, not an independent forecast**: it is the same deterministic computation")
A("run before any image is drawn. Its function is to stop the card being adjusted after the frame is")
A("seen (programme §2.5(1)), not to forecast a measurement. Stage B must report any difference.")
A("")
A("## 8. Effective-2D slots (programme §4.7)")
A("")
E = C.effective2d()
A("| slot | value |")
A("|---|---|")
A("| model | %s |" % E["model"])
A("| model status | %s |" % E["model_status"])
A("| subsystem | %s |" % E["subsystem"])
A("| `ΔE_z` | `%.3f eV` = %s |" % (E["Delta_E_z_eV"], E["Delta_E_z_formula"]))
A("| `E_occ` | `max(E_F, k_BT) = %.4f eV` |" % E["E_occ_eV"])
A("| `ε_z` | `%.3e` = %s |" % (E["eps_z"], E["eps_z_definition"]))
A("| internal bound | **%s** |" % E["internal_bound"])
A("| external excitation | **%s** (`E_probe = %.3f eV`) |" % (E["external_excitation"], E["E_probe_eV"]))
A("| external resolution | **%s** (`%.3f nm` vs probe `%.1f nm`) |" % (E["external_resolution"], C.DELTA_NM, E["probe_resolution_nm"]))
A("| coupling | %s |" % E["coupling"])
A("| **label** | **`%s`** |" % E["label"])
A("| missing slot | %s |" % E["missing_slot"])
A("")
A("The label is `NOT-MEASURED` because the confining potential is not registered. The three external")
A("checks are reported separately and are not merged: the declared optical probe cannot excite `z`")
A("(`2.5 eV ≪ ΔE_z`) and cannot resolve it (`%.1f nm ≫ %.3f nm`). Neither fact is turned into" % (E["probe_resolution_nm"], C.DELTA_NM))
A("`IS_2D` or `LOOKS_2D`.")
A("")
A("## 9. Solver spec")
A("")
A("See `row2_solver_spec_v1.md`. In one line: the geometry is **prescribed** (`D2`), the counts are")
A("derived, the tiers are **measured** on the resulting fields, and no reduction equation is solved.")
A("")
A("## 10. What this card does not claim")
A("")
A("- not a solution of the reduction, and not a matrix cell;")
A("- not a visibility or readability claim (`Q3` is a legibility index in levels, not identity bits);")
A("- not a survival claim: at `t_end` %.1f%% of the deposit has decayed;" % (100.0 * STATES[2][2]["V_decayed"] / STATES[2][2]["V_swept"]))
A("- not a derivation of the 3 ns lifetime; it is imported and marked as such everywhere;")
A("- not a fragment count with an error bar: `1.18e10` is a model estimate (programme §4.8).")
A("")
A("---")
A("")
A("*If Stage B's measured profile differs from section 7, Stage B must publish the difference and the")
A("card stands as the falsified prediction. The card is not edited after the lock.*")
A("")

# ---------------------------------------------------------------------------
# solver spec
# ---------------------------------------------------------------------------
spec = []
S = spec.append
S("# Solver spec — W1 / row 2, %s" % CYCLE_ID)
S("")
S("**Status**: pre-registration, stage A. `docs/program/RESEARCH_PROGRAM_v1.md` v1.1.1 §5.3 splits")
S("card / manifest / solver spec / run record; this is the third.")
S("")
S("## 1. What is solved, and what is not")
S("")
S("| object | treatment |")
S("|---|---|")
S("| 3D body state `U` | **prescribed**: the registered synthetic phantom; no equation of motion |")
S("| front `φ` | **prescribed law** `z_f = min(H, v t)`, `v = c/√2`; no front equation solved |")
S("| 2D output `u` | **derived** by the map `M` of the card §4 |")
S("| tiers `T0–T3` | **measured** on `u` with the locked estimators |")
S("| effective-2D label | **computed** on a declared surrogate potential, then withheld (`NOT-MEASURED`) |")
S("| `C3` decay | **declared overlay** with an imported `τ`; not solved |")
S("")
S("No PDE is integrated. No conservation law is enforced beyond the identity `V_deposited = V_swept`.")
S("The frame is a presentation of this computation (`GEOMETRY: PRESCRIBED (D2)`), and `R3` frame")
S("reproduction is **not** claimed.")
S("")
S("## 2. Fields handed to the estimators")
S("")
S("| field | grid | definition |")
S("|---|---|---|")
S("| `plate` | 128×128 | tissue-density channel `ρ_class/ρ_max` of the axial slice at `min(z_f, 1.70 m)` |")
S("| `canvas` | 128×128 | per-site mean layer density over the array raster; a block is filled iff the front has passed it |")
S("")
S("The two fields answer different questions: `plate` is what one deposited sheet carries; `canvas` is")
S("what the assembled array carries at 36 km scale. They are not two renderings of one quantity.")
S("")
S("## 3. Estimator identity (programme §4.3)")
S("")
S("| item | value |")
S("|---|---|")
S("| authority | `docs/specs/intrinsic_structure_tiers_v1.md` v1 (T0 §2, T1 §3, T2 §4, T3 §5) |")
S("| implementation | `src/analysis/tiers_core_v1.py`, a verbatim extraction of `src/route/structure_tiers.py` |")
S("| grid / bins | 128×128 / 64 |")
S("| T2 context | %d levels |" % C.tc.CTX)
S("| T3 smoothing | DoG with `σ = ξ/2` and `2ξ`, `C_eye = 0.01` |")
S("| null ensemble | %d uniform realisations, seeds %d…%d |"
  % (C.tc.NULL_M, C.tc.NULL_SEED0, C.tc.NULL_SEED0 + C.tc.NULL_M - 1))
S("| null means | `P0 = %.6e` (sd `%.2e`), `Q2 = %.6f` (sd `%.2e`) |"
  % (C.NULL_RECORD["P0_mean"], C.NULL_RECORD["P0_sd"], C.NULL_RECORD["Q2_mean"], C.NULL_RECORD["Q2_sd"]))
S("| threshold lock | `runs/MATRIX/threshold_lock.json`, sha256 `%s` |" % C.LOCK_SHA)
S("| lock's own record | `%s` |" % (C.LOCK_RECORDED or "ABSENT"))
S("")
S("## 4. Fragment-count provenance (programme §4.8)")
S("")
S("| required item | value | status |")
S("|---|---|---|")
S("| phantom coverage | `z ∈ [0.012, 1.738] m`, full body | REGISTERED |")
S("| pixels per layer | 200×200 | REGISTERED |")
S("| sample size (layers counted) | not stated in the registered record | **UNREGISTERED** |")
S("| per-region mean | 2.00 (calf→thigh), 1.00 elsewhere | REGISTERED |")
S("| per-region variance | not stated | **UNREGISTERED** |")
S("| weighting of leg / neck / head | thickness-weighted mean over the table → 1.457 | DERIVED here |")
S("| boundary rule (4-connected, slice plane) | 4-connected components in the axial section | REGISTERED |")
S("")
S("Because sample size and variance are unregistered, `1.18e10` is labelled a **MODEL ESTIMATE**, not a")
S("counted total, and no error bar is claimed. Stage B prints this label next to every occurrence.")
S("")
S("## 5. Discretization declaration (programme §4.8)")
S("")
S("- baseline: one atomic layer per slice, `δ = 0.215 nm`, `N_slices = H/δ = %.4e`." % (C.H_BODY / C.DELTA))
S("- control: `δ × 10` or a continuous front — **not run** in this cycle; programme item 6.1(3) remains OPEN.")
S("- consequence: publication item 7 fails, so the cycle is `O0-ARTIFACT`.")
S("")
S("## 6. Determinism and seeds")
S("")
S("- the phantom is analytic (no RNG);")
S("- the null ensemble is seeded (`%d + k`, `k = 0…%d`);" % (C.tc.NULL_SEED0, C.tc.NULL_M - 1))
S("- the figure has no stochastic element; identical inputs must give byte-identical PNGs at a fixed")
S("  matplotlib version (recorded in the run record).")
S("")

# ---------------------------------------------------------------------------
# write, then lock
# ---------------------------------------------------------------------------
card_path = os.path.join(OUTDIR, "row2_scene_card_v1.md")
man_path = os.path.join(OUTDIR, "row2_manifest_v1.json")
spec_path = os.path.join(OUTDIR, "row2_solver_spec_v1.md")
pred_path = os.path.join(OUTDIR, "row2_prediction_v1.json")

with open(card_path, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(card) + "\n")
with open(man_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(MANIFEST, f, indent=2, ensure_ascii=False)
    f.write("\n")
with open(spec_path, "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(spec) + "\n")

PREDICTION = dict(
    cycle_id=CYCLE_ID,
    utc=UTC,
    derived=dict(
        t_rip_s=C.T_RIP, v_front_m_s=C.V_FRONT, tau_s=C.TAU_C3,
        tau_over_t_rip=C.TAU_C3 / C.T_RIP,
        n_slices=C.H_BODY / C.DELTA, plate_census=C.N_PLATE,
        V_recon_m3=C.V_RECON, V_registered_m3=C.V_REG, V_ratio=C.V_RECON / C.V_REG,
        keyframes={tag: dict(t_s=t, z_front_m=st["zf"], sheets=st["layers"], fragments=st["plates"],
                             fill=st["fill"], V_swept_m3=st["V_swept"],
                             V_decayed_m3=st["V_decayed"], V_live_m3=st["V_live"],
                             decayed_fraction=(st["V_decayed"] / st["V_swept"]) if st["V_swept"] > 0 else 0.0)
                  for tag, t, st in STATES},
    ),
    estimator=C.ESTIMATOR,
    null_ensemble=C.NULL_RECORD,
    profile=pred_rows,
    meta=pred_meta,
    ledger=LEDGER,
)
with open(pred_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(PREDICTION, f, indent=2, ensure_ascii=False)
    f.write("\n")

files = dict(
    scene_card="runs/W1-ROW2/row2_scene_card_v1.md",
    manifest="runs/W1-ROW2/row2_manifest_v1.json",
    solver_spec="runs/W1-ROW2/row2_solver_spec_v1.md",
    prediction="runs/W1-ROW2/row2_prediction_v1.json",
    shared_module="src/analysis/w1_row2_common_v1.py",
    tiers_core="src/analysis/tiers_core_v1.py",
    phantom="src/analysis/unfold_appearance_v1.py",
    threshold_lock="runs/MATRIX/threshold_lock.json",
)
lock = dict(
    cycle_id=CYCLE_ID,
    locked_utc=UTC,
    purpose="pre-registration: stage B must verify these hashes before rendering",
    files={k: dict(path=v, sha256=C.sha256(os.path.join(ROOT, v))) for k, v in files.items()},
    rendered_artifacts=[],
)
lock_path = os.path.join(OUTDIR, "row2_lock_v1.json")
with open(lock_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(lock, f, indent=2, ensure_ascii=False)
    f.write("\n")
lock_sha = C.sha256(lock_path)
with open(lock_path + ".sha256", "w", encoding="utf-8", newline="\n") as f:
    f.write(lock_sha + "  row2_lock_v1.json\n")

print("STAGE A -- pre-registration")
print("  cycle        : %s" % CYCLE_ID)
print("  V_recon      : %.6f m^3   (registered %.4f ; ratio %.4f)" % (C.V_RECON, C.V_REG, C.V_RECON / C.V_REG))
print("  t_rip        : %.10e s   v_front %.6e m/s" % (C.T_RIP, C.V_FRONT))
print("  tau/t_rip    : %.4f" % (C.TAU_C3 / C.T_RIP))
print("  O0 verdict   : %s  (%s)" % (MANIFEST["acceptance"]["verdict"], MANIFEST["acceptance"]["verdict_reason"]))
print("  locked files :")
for k, v in lock["files"].items():
    print("    %-16s %s  %s" % (k, v["sha256"][:16], v["path"]))
print("  lock sha256  : %s" % lock_sha)
print("")
print("  predicted profile:")
for r in pred_rows:
    print("    %-6s %-7s %-3s %-12s thr %.2f  %s" %
          (r["keyframe"], r["field"], r["tier"],
           "-" if r["value"] is None else "%.6g" % r["value"], r["threshold"], r["verdict"]))
print("")
print("  next: python -I src/analysis/w1_row2_cycle_v1.py")
