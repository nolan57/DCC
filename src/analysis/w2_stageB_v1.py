# -*- coding: utf-8 -*-
"""
w2_stageB_v1.py -- MEASURE stage for the four W2 continuation cycles.

Every product is emitted by this script; no number is hand-transcribed. Stage B
refuses to write a result if a stage-A lock fails.

Run: python -I src/analysis/w2_stageB_v1.py
"""
import json
import math
import os
import struct
import sys
import zlib
from copy import deepcopy

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w2_common_v1 as W
import w1_row2_common_v1 as w1

ROOT = W.ROOT
CYCLES = [
    ("runs/W2-DISC", "disc", "W2_DISC_01"),
    ("runs/W2-C2", "c2", "W2_C2VIOL_01"),
    ("runs/W2-C3", "c3", "W2_C3TEST_01"),
    ("runs/W2-XCHECK", "xcheck", "W2_XCHECK_01"),
]


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
    if x is None:
        return None
    return str(x)


def write_json(path, obj):
    text = json.dumps(jsonable(obj), indent=2, ensure_ascii=False) + "\n"
    W.write_text(path, text)
    return path


def rel(path):
    return os.path.relpath(path, ROOT)


def f(x, n=12):
    if x is None:
        return "n/a"
    return ("%%.%dg" % n) % float(x)


def tier_table(rows, indent="    "):
    out = []
    for r in rows:
        out.append("%s%-3s %-10s %-16s %-12s %s" %
                   (indent, r["tier"], f(r["value"], 10), r["verdict"], r["status"], r["note"]))
    return "\n".join(out)


def not_applicable_rows(field, note="no 2D output before the front arrives"):
    return [dict(tier=t, value=None, verdict="NOT-APPLICABLE", status="NOT-APPLICABLE",
                 note=note, field=field) for t in ("T0", "T1", "T2", "T3")]


def lock_block(lock_path, ok, lines):
    return "\n".join(["LOCK: %s" % rel(lock_path),
                      "  status: %s" % ("VERIFIED" if ok else "FAILED"),
                      *["  " + ln for ln in lines]])


def guard(cycles=CYCLES):
    ok_all = True
    blocks = []
    for d, prefix, _ in cycles:
        p = os.path.join(ROOT, d, prefix + "_lock.json")
        ok, lines = W.verify_lock(p)
        ok_all = ok_all and ok
        blocks.append(lock_block(p, ok, lines))
    return ok_all, blocks


# ---------------------------------------------------------------------------
# W2-DISC-01 -- discretization control
# ---------------------------------------------------------------------------
def run_disc(lock_ok):
    st1 = w1.state_at(w1.T_MID_S)
    st10 = deepcopy(st1)
    st10["delta_m"] = w1.DELTA * W.DELTA_FACTOR
    st10["layers"] = st1["zf"] / st10["delta_m"]
    st10["plates"] = st10["layers"] * w1.COMP_PER_LAYER
    st10["fill"] = st10["plates"] / w1.N_PLATE
    st10["sites"] = min(1.0, st10["layers"] / w1.N_SLICE_REG)

    plate1 = w1.plate_field(st1["zf"])
    plate10 = w1.plate_field(st10["zf"])
    canvas1 = w1.canvas_field(st1)
    canvas10 = w1.canvas_field(st10)
    rp1, mp1 = w1.measure(plate1, "plate")
    rp10, mp10 = w1.measure(plate10, "plate-delta10")
    rpf, mpf = w1.measure(plate1.copy(), "plate-floor-repeat")
    rc1, mc1 = w1.measure(canvas1, "canvas")
    rc10, mc10 = w1.measure(canvas10, "canvas-delta10")

    plate_sha1 = W.sha_bytes(plate1.tobytes())
    plate_sha10 = W.sha_bytes(plate10.tobytes())
    floor_sha = W.sha_bytes(plate1.copy().tobytes())

    counts = {
        "layers": (st1["layers"], st10["layers"]),
        "plates": (st1["plates"], st10["plates"]),
        "fragments": (st1["plates"], st10["plates"]),
        "sites": (st1["sites"], st10["sites"]),
        "fill": (st1["fill"], st10["fill"]),
    }
    count_ratios = {k: v[1] / v[0] for k, v in counts.items()}
    count_ok = all(abs(r - 0.1) <= 1e-12 for r in count_ratios.values())

    tier_ratios = {}
    for a, b in zip(rp1, rp10):
        tier_ratios[a["tier"]] = (None if a["value"] in (None, 0.0) or b["value"] is None
                                  else b["value"] / a["value"])
    floor_ratios = {}
    for a, b in zip(rp1, rpf):
        floor_ratios[a["tier"]] = (None if a["value"] in (None, 0.0) or b["value"] is None
                                   else b["value"] / a["value"])
    flips = [a["tier"] for a, b in zip(rp1, rp10) if a["verdict"] != b["verdict"]]
    d1 = plate_sha1 == plate_sha10 == floor_sha and not flips and all(
        abs(v - 1.0) <= 1e-15 for v in floor_ratios.values() if v is not None)

    mass1 = st1["m_swept"]
    mass10 = st10["m_swept"]
    vol1 = st1["V_swept"]
    vol10 = st10["V_swept"]
    inv1 = abs(st1["m_decayed"] + st1["m_live"] - mass1) / mass1
    inv10 = abs(st10["m_decayed"] + st10["m_live"] - mass10) / mass10
    d4 = (mass1 == mass10 and vol1 == vol10 and st1["zf"] == st10["zf"]
          and inv1 == 0.0 and inv10 == 0.0)

    xi1 = mc1["xi"]
    xi10 = mc10["xi"]
    xi_gain = xi10 / xi1 - 1.0
    d3 = (abs(count_ratios["fill"] - 0.1) <= 1e-12 and xi_gain >= 0.20)
    checks = {"D1": d1, "D2": count_ok, "D3": d3, "D4": d4}
    verdict = "PASS" if all(checks.values()) else "FALSIFIED"

    lines = [
        "CYCLE: W2-DISC-01  (programme section 6.1 item 3)",
        "TYPE: TECHNICAL closure; not an O0 artifact and not a rendered scene",
        "LOCK INPUTS: threshold lock %s" % w1.LOCK_SHA,
        lock_block(os.path.join(ROOT, "runs/W2-DISC", "disc_lock.json"), lock_ok,
                   W.verify_lock(os.path.join(ROOT, "runs/W2-DISC", "disc_lock.json"))[1]),
        "",
        "[1] MECHANISMS",
        "    baseline id atomic-layer-slice-v1   delta = %s m" % f(w1.DELTA),
        "    control  id atomic-layer-slice-v1-delta10 delta = %s m" % f(st10["delta_m"]),
        "    ratio control/baseline = %s ; front law and map M unchanged" % f(W.DELTA_FACTOR),
        "",
        "[2] PLATE FIELD AT t_mid (identical geometry, different z-window census)",
        "    sha256 baseline  %s" % plate_sha1,
        "    sha256 control   %s" % plate_sha10,
        "    sha256 repeat    %s  (deterministic floor)" % floor_sha,
        "    baseline tiers:", tier_table(rp1),
        "    control tiers:", tier_table(rp10),
        "    repeat tiers:", tier_table(rpf),
        "    tier value ratios control/baseline: " +
        ", ".join("%s=%s" % (k, f(v)) for k, v in tier_ratios.items()),
        "    tier value ratios repeat/baseline:  " +
        ", ".join("%s=%s" % (k, f(v)) for k, v in floor_ratios.items()),
        "    verdict flips: %s" % (", ".join(flips) if flips else "none"),
        "",
        "[3] CANVAS FIELD / CENSUS",
        "    baseline tiers:", tier_table(rc1),
        "    control tiers:", tier_table(rc10),
        "    xi cells baseline=%s control=%s gain=%s" % (f(xi1), f(xi10), f(xi_gain)),
        "    count ratios control/baseline: " +
        ", ".join("%s=%s" % (k, f(v)) for k, v in count_ratios.items()),
        "",
        "[4] CONSERVED INTEGRALS AND FRONT",
        "    m_swept baseline=%s control=%s kg" % (f(mass1), f(mass10)),
        "    V_swept baseline=%s control=%s m^3" % (f(vol1), f(vol10)),
        "    z_front both=%s m" % f(st1["zf"]),
        "    conservation residual baseline=%s control=%s" % (f(inv1), f(inv10)),
        "",
        "[5] PREDICTIONS AGAINST FLOOR",
        "    D1 plate invariance          %s" % ("PASS" if d1 else "FAIL"),
        "    D2 census scaling            %s" % ("PASS" if count_ok else "FAIL"),
        "    D3 canvas fill / xi increase %s" % ("PASS" if d3 else "FAIL"),
        "    D4 mass/volume/front         %s" % ("PASS" if d4 else "FAIL"),
        "    overall: %s" % verdict,
        "",
        "No frame is claimed. No result-labelled claim is made. A control difference at or below",
        "the deterministic floor would be NO-OBSERVED-EFFECT; this cycle uses that floor, not a",
        "new threshold chosen after seeing the values.",
    ]
    result = os.path.join(ROOT, "runs/W2-DISC/disc_results_v1.txt")
    W.write_text(result, W.banner(
        W.PROVENANCE,
        "W2-DISC-01 -- DISCRETIZATION CONTROL (delta x 10), TECHNICAL CLOSURE", lines))

    profile = {
        "provenance_tag": "PROVENANCE: %s" % W.PROVENANCE,
        "cycle_id": "W2_DISC_01",
        "front_s": w1.T_MID_S,
        "baseline": {"delta_m": w1.DELTA, "plate": rp1, "canvas": rc1, "state": jsonable(st1)},
        "control": {"delta_m": st10["delta_m"], "plate": rp10, "canvas": rc10, "state": jsonable(st10)},
        "floor": {"plate": rpf, "sha256": floor_sha},
        "sha256": {"plate_baseline": plate_sha1, "plate_control": plate_sha10},
        "ratios": {"counts": jsonable(count_ratios), "tiers": jsonable(tier_ratios),
                   "floor": jsonable(floor_ratios), "canvas_xi_gain": xi_gain},
        "conservation_residual": {"baseline": inv1, "control": inv10},
        "checks": checks, "verdict": verdict,
    }
    write_json(os.path.join(ROOT, "runs/W2-DISC/disc_profile_v1.json"), profile)

    record = {
        "provenance_tag": "PROVENANCE: %s" % W.PROVENANCE,
        "cycle_id": "W2_DISC_01",
        "utc": W.utc(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "modules": {p: W.sha256(os.path.join(ROOT, p)) for p in (
            "src/analysis/w2_common_v1.py", "src/analysis/w2_stageB_v1.py",
            "src/analysis/w1_row2_common_v1.py", "src/analysis/tiers_core_v1.py")},
        "thresholds": w1.THR,
        "threshold_lock_sha256": w1.LOCK_SHA,
        "products": [rel(result), "runs/W2-DISC/disc_profile_v1.json"],
        "rendered_frames": [],
    }
    write_json(os.path.join(ROOT, "runs/W2-DISC/disc_run_record_v1.json"), record)
    return result, verdict, checks


# ---------------------------------------------------------------------------
# W2-C2VIOL-01 -- not-C2 stretch branch
# ---------------------------------------------------------------------------
def _png_chunk(kind, data):
    return (struct.pack(">I", len(data)) + kind + data +
            struct.pack(">I", zlib.crc32(kind + data) & 0xffffffff))


def write_png(path, rgb):
    """Minimal PNG writer (stdlib only), so the instrument stays runnable under -I."""
    rgb = np.ascontiguousarray(rgb, dtype=np.uint8)
    h, w, _ = rgb.shape
    raw = b"".join(b"\x00" + row.tobytes() for row in rgb)
    png = (b"\x89PNG\r\n\x1a\n" +
           _png_chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) +
           _png_chunk(b"IDAT", zlib.compress(raw, 9)) +
           _png_chunk(b"IEND", b""))
    with open(path, "wb") as f:
        f.write(png)
    return path


def _nearest(arr, size):
    a = np.asarray(arr, dtype=np.float64)
    idx = (np.arange(size) * a.shape[0] // size).astype(int)
    return a[np.ix_(idx, idx)]


def _ramp(v):
    """Declared sequential violet ramp; v in [0,1], pale beige -> violet."""
    v = np.clip(np.asarray(v, dtype=np.float64), 0.0, 1.0)
    lo = np.array([251.0, 250.0, 247.0])
    hi = np.array([83.0, 74.0, 183.0])
    return (lo[None, None, :] + v[:, :, None] * (hi - lo)[None, None, :]).astype(np.uint8)


def _grey(v):
    v = np.clip(np.asarray(v, dtype=np.float64), 0.0, 1.0)
    return np.repeat((255.0 * v).astype(np.uint8)[:, :, None], 3, axis=2)


def _montage(panels, size=256, gap=8):
    cells = [_nearest(p, size) for p in panels]
    w = size * len(cells) + gap * (len(cells) + 1)
    out = np.full((size + 2 * gap, w, 3), 251, dtype=np.uint8)
    for i, c in enumerate(cells):
        x0 = gap + i * (size + gap)
        rgb = _ramp(c) if c.shape[2:] == () else c
        out[gap:gap + size, x0:x0 + size, :] = rgb
    return out


def display_sidecar(path, frame, cols, time_line, basis, scalar):
    text = (
        "DISPLAY-DECLARATION v1\n"
        "FRAME:            %s\n"
        "PROVENANCE:       NEITHER\n"
        "STAGE:            S0\n"
        "FIDELITY:         FL1\n"
        "BAND:             NONE (declared density channel; no spectral measurement)\n"
        "COLOUR:           DECLARED-CONVENTION\n"
        "COLOUR-BASIS:     %s\n"
        "SCALAR:           %s\n"
        "TIME:             %s\n"
        "GEOMETRY:         PRESCRIBED (D2)\n"
        "ENHANCEMENT:      none\n"
        "ME5-COROLLARY:    PRESENT\n"
        % (frame, basis, scalar, time_line)
    )
    W.write_text(path, text)
    return text


def frame_sidecar(t_span, ratio, sequence=False):
    time_line = ("t_span = %s s (single snapshot) ; compression = 1 ; t_rip = %s s ; ratio = %s"
                 % (f(t_span, 8), f(w1.T_RIP, 8), f(ratio, 8))) if not sequence else (
                 "t_span = %s s (three-frame plate array) ; compression = 1 ; t_rip = %s s ; ratio = %s"
                 % (f(t_span, 8), f(w1.T_RIP, 8), f(ratio, 8)))
    if sequence:
        basis = ("three panels left-to-right: t0, t_mid, t_end; each is the pushed-forward tissue-density "
                 "index in the declared violet sequential ramp; pale marks sites the front has not reached. "
                 "No wavelength information is carried at any stage")
    else:
        basis = ("panel A: violet sequential ramp encodes the pushed-forward tissue-density index and pale "
                 "marks sites the front has not reached; panel B: violet sequential ramp encodes per-site "
                 "mean layer density; panel C: greyscale is the absolute difference between the stretched "
                 "and row-2 plate fields at the same time slot. No wavelength information is carried")
    scalar = ("tissue-density index (dimensionless); per-site mean layer density (dimensionless); "
              "absolute density difference (dimensionless); time (ns); area factor det J (dimensionless)")
    return time_line, basis, scalar


def render_c2_frame(out, plate, canvas, base, t_span, ratio):
    diff = np.abs(plate - base)
    panels = [plate, canvas, _grey(diff / max(float(diff.max()), 1e-300))]
    write_png(out, _montage(panels))
    time_line, basis, scalar = frame_sidecar(t_span, ratio)
    display_sidecar(out + ".display.txt", os.path.basename(out), None, time_line, basis, scalar)


def render_c2_sequence(out, frames):
    write_png(out, _montage(frames))
    time_line, basis, scalar = frame_sidecar(w1.T_RIP, 1.0, True)
    display_sidecar(out + ".display.txt", os.path.basename(out), None, time_line, basis, scalar)


def run_c2(lock_ok):
    keys = [("t0", w1.T0_S), ("t_mid", w1.T_MID_S), ("t_end", w1.T_END_S)]
    measurements = {}
    stretched_frames = {}
    base_frames = {}
    for name, t in keys:
        st = w1.state_at(t)
        if name == "t0":
            base = np.zeros((128, 128), dtype=np.float64)
            canvas = np.zeros((128, 128), dtype=np.float64)
            moved, cons = W.stretch_pushforward(base, W.S_STRETCH)
            rb = not_applicable_rows("row2-plate-t0")
            rs = not_applicable_rows("stretched-plate-t0")
            rc = not_applicable_rows("canvas-t0")
            mb = ms = mc = dict(field=name, Q0=None, xi=None, Q2=None, Q3=None,
                                Q3_reflection=None, C_xi=None, sigma_over_du=0.0,
                                H_bits=0.0, P0=0.0)
        else:
            base = w1.plate_field(st["zf"])
            canvas = w1.canvas_field(st)
            moved, cons = W.stretch_pushforward(base, W.S_STRETCH)
            rb, mb = w1.measure(base, "row2-plate-" + name)
            rs, ms = w1.measure(moved, "stretched-plate-" + name)
            rc, mc = w1.measure(canvas, "canvas-" + name)
        stretched_frames[name] = moved
        base_frames[name] = base
        measurements[name] = dict(t=t, state=jsonable(st), base_rows=rb, base_meta=mb,
                                  stretch_rows=rs, stretch_meta=ms, canvas_rows=rc,
                                  canvas_meta=mc, conservation=jsonable(cons),
                                  sha_base=W.sha_bytes(base.tobytes()),
                                  sha_stretch=W.sha_bytes(moved.tobytes()))

    mid = measurements["t_mid"]
    cons = mid["conservation"]
    s1 = (abs(cons["detJ"] - W.S_STRETCH ** 2) <= 1e-15 and
          abs(cons["area_change_fraction"] - (W.S_STRETCH ** 2 - 1.0)) <= 1e-15)
    s2 = cons["conservation_residual"] < 1e-12 and cons["mass_outflow"] > 0
    xi_ratio = mid["stretch_meta"]["xi"] / mid["base_meta"]["xi"]
    s3 = 0.99 <= xi_ratio <= 1.03
    pass_tiers = {"T0", "T2", "T3"}
    s4 = all(r["verdict"] == "PASS" for r in mid["stretch_rows"] if r["tier"] in pass_tiers) and \
        [r["value"] for r in mid["stretch_rows"] if r["tier"] == "T3"] and \
        all(a["value"] == b["value"] and a["verdict"] == b["verdict"]
            for a, b in zip(mid["canvas_rows"], measurements["t_mid"]["canvas_rows"]))
    # canvas self-comparison above is trivially true; the substantive check is against the row-2 field.
    st_mid = w1.state_at(w1.T_MID_S)
    row2_canvas_rows, _ = w1.measure(w1.canvas_field(st_mid), "row2-canvas-reference")
    s4_canvas = all(a["value"] == b["value"] and a["verdict"] == b["verdict"]
                    for a, b in zip(mid["canvas_rows"], row2_canvas_rows))
    s4 = s4 and s4_canvas
    checks = {"S1": s1, "S2": s2, "S3": s3, "S4": s4}
    verdict = "PASS" if all(checks.values()) else "FALSIFIED"

    # render: three keyframes + sequence
    img_dir = os.path.join(ROOT, "runs/W2-C2")
    for name, t in keys:
        m = measurements[name]
        st = w1.state_at(t)
        render_c2_frame(
            os.path.join(img_dir, "c2_%s.png" % name),
            stretched_frames[name], w1.canvas_field(st) if name != "t0"
            else np.zeros((128, 128)), base_frames[name],
            t, t / w1.T_RIP)
    render_c2_sequence(os.path.join(img_dir, "c2_sequence.png"),
                       [stretched_frames[n] for n, _ in keys])

    lines = [
        "CYCLE: W2-C2VIOL-01  (programme section 6.1 item 4)",
        "TYPE: artifact cycle, row 4 = C1 HELD / C2 VIOLATED / C3 VIOLATED",
        "LOCK INPUTS: threshold lock %s" % w1.LOCK_SHA,
        lock_block(os.path.join(ROOT, "runs/W2-C2", "c2_lock.json"), lock_ok,
                   W.verify_lock(os.path.join(ROOT, "runs/W2-C2", "c2_lock.json"))[1]),
        "",
        "[1] DECLARED MAP AND PRICE",
        "    (x,y) -> (%s x, %s y) about the registered 128x128 window origin" %
        (f(W.S_STRETCH, 4), f(W.S_STRETCH, 4)),
        "    Jacobian det J = %s ; area change = %s" %
        (f(cons["detJ"], 8), f(cons["area_change_fraction"], 8)),
        "    C1 kept by pushforward Sigma'(x') = Sigma(x'/s)/s^2 (area-overlap interpolation)",
        "    conservation ledger: mass before=%s, inside window=%s, outflow=%s, residual=%s" %
        (f(cons["mass_before"], 10), f(cons["mass_in_window"], 10),
         f(cons["mass_outflow"], 10), f(cons["conservation_residual"], 4)),
        "    boundary: %s" % cons["boundary_rule"],
        "    detection observable: conservation ledger and T1 scale shift",
        "",
        "[2] TIER PROFILES (q=1 declared instrumented channel)",
    ]
    for name, t in keys:
        m = measurements[name]
        lines += ["    %s t=%s s" % (name, f(t, 8)),
                  "      row-2 plate:", tier_table(m["base_rows"], "        "),
                  "      stretched  :", tier_table(m["stretch_rows"], "        "),
                  "      canvas     :", tier_table(m["canvas_rows"], "        "),
                  "      sha256 row2=%s stretched=%s" % (m["sha_base"], m["sha_stretch"])]
    lines += [
        "",
        "[3] EFFECTIVE 2D (not merged into a scene verdict)",
        "    subsystem: %s" % w1.effective2d()["subsystem"],
        "    label: %s ; missing slot: %s" %
        (w1.effective2d()["label"], w1.effective2d()["missing_slot"]),
        "    scope note: %s" % w1.effective2d()["subsystem_scope_note"],
        "",
        "[4] t_mid COMPARISON AGAINST ROW 2",
        "    xi row2=%s cells ; xi stretched=%s ; ratio=%s" %
        (f(mid["base_meta"]["xi"], 10), f(mid["stretch_meta"]["xi"], 10), f(xi_ratio, 10)),
        "    Q3 row2=%s ; stretched=%s ; q=0 channel=%s" %
        (f(mid["base_meta"]["Q3"], 8), f(mid["stretch_meta"]["Q3"], 8),
         f(mid["stretch_meta"]["Q3_reflection"], 8)),
        "    canvas profile identical to row 2 at t_mid: %s" % s4_canvas,
        "",
        "[5] PREDICTIONS",
        "    S1 Jacobian / area factor  %s" % ("PASS" if s1 else "FAIL"),
        "    S2 conservation ledger    %s" % ("PASS" if s2 else "FAIL"),
        "    S3 xi scales with s       %s" % ("PASS" if s3 else "FAIL"),
        "    S4 tier / canvas profile  %s" % ("PASS" if s4 else "FAIL"),
        "    overall: %s" % verdict,
        "",
        "The q=0 reflected channel is reported separately; it is not used as a scene verdict.",
        "No visibility, readability, realizability or COUNTERFACTUAL(C3) claim is made. C3 is violated here.",
        "The frames are citable only together with their DISPLAY-DECLARATION sidecars.",
    ]
    result = os.path.join(ROOT, "runs/W2-C2/c2_results_v1.txt")
    W.write_text(result, W.banner(
        W.PROVENANCE,
        "W2-C2VIOL-01 -- NOT-C2 UNIFORM DILATION s=1.01 (ROW 4)", lines))

    profile = {
        "provenance_tag": "PROVENANCE: %s" % W.PROVENANCE,
        "cycle_id": "W2_C2VIOL_01", "map": {"s": W.S_STRETCH, "detJ": W.S_STRETCH ** 2},
        "keyframes": {k: jsonable(v) for k, v in measurements.items()},
        "t_mid_comparison": {"xi_ratio": xi_ratio, "canvas_identical": s4_canvas},
        "effective_2d": w1.effective2d(),
        "checks": checks, "verdict": verdict,
        "q_reflection": mid["stretch_meta"]["Q3_reflection"],
    }
    write_json(os.path.join(ROOT, "runs/W2-C2/c2_profile_v1.json"), profile)

    record = {
        "provenance_tag": "PROVENANCE: %s" % W.PROVENANCE,
        "cycle_id": "W2_C2VIOL_01", "utc": W.utc(),
        "python": sys.version.split()[0], "numpy": np.__version__,
        "modules": {p: W.sha256(os.path.join(ROOT, p)) for p in (
            "src/analysis/w2_common_v1.py", "src/analysis/w2_stageB_v1.py",
            "src/analysis/w1_row2_common_v1.py", "src/analysis/tiers_core_v1.py")},
        "thresholds": w1.THR, "threshold_lock_sha256": w1.LOCK_SHA,
        "products": [rel(result), "runs/W2-C2/c2_profile_v1.json"],
        "rendered_frames": ["runs/W2-C2/c2_%s.png" % n for n, _ in keys] +
                           ["runs/W2-C2/c2_sequence.png"],
        "display_sidecars": [p + ".display.txt" for p in
                             ["runs/W2-C2/c2_%s.png" % n for n, _ in keys] +
                             ["runs/W2-C2/c2_sequence.png"]],
        "reproduction": "R2 (physical quantities); frame reproduction R3 not claimed",
    }
    write_json(os.path.join(ROOT, "runs/W2-C2/c2_run_record_v1.json"), record)
    return result, verdict, checks


# ---------------------------------------------------------------------------
# W2-C3TEST-01 -- C3 consumption test
# ---------------------------------------------------------------------------
def run_c3(lock_ok):
    states = W.c3_states()
    graph = W.generator_graph_check()
    frozen = states["HELDC3_counterfactual"]
    neut = {k: v for k, v in states.items() if k.startswith("NEUTRONIZED_")}
    c1_rows = []
    ratios = {}
    for name, st in sorted(neut.items()):
        ye_ok = st["Y_e"] < frozen["Y_e"]
        ne_ok = st["n_e_fm3"] < frozen["n_e_fm3"]
        n_ratio = st["n_e_fm3"] / frozen["n_e_fm3"]
        kin = st["mu_kin_MeV"]
        k_ratio = kin / frozen["E_F_MeV"]
        power_ratio = n_ratio ** (2.0 / 3.0)
        ratios[name] = dict(n_e_ratio=n_ratio, mu_kin_ratio=k_ratio,
                            n_e_power_2_3=power_ratio,
                            relative_difference=abs(k_ratio - power_ratio) / k_ratio)
        c1_rows.append((name, ye_ok and ne_ok, ye_ok, ne_ok))
    c1 = all(r[1] for r in c1_rows)
    c2 = all(r["relative_difference"] <= 0.02 for r in ratios.values())
    st = w1.state_at(w1.T_MID_S)
    # The branch label changes the C3 state passed to the observer scope; the registered
    # field generators do not read it, so both branches are built and byte-compared here.
    branch_fields = {}
    for branch in ["HELDC3_counterfactual"] + sorted(neut):
        u_p = w1.plate_field(st["zf"])
        u_c = w1.canvas_field(st)
        branch_fields[branch] = {
            "plate_sha256": W.sha_bytes(u_p.tobytes()),
            "canvas_sha256": W.sha_bytes(u_c.tobytes()),
        }
    sha = {b: v for b, v in branch_fields.items()}
    held_sha = branch_fields["HELDC3_counterfactual"]
    c3 = all(v["plate_sha256"] == held_sha["plate_sha256"] and
             v["canvas_sha256"] == held_sha["canvas_sha256"]
             for b, v in branch_fields.items() if b != "HELDC3_counterfactual")
    c4 = graph["verdict"] == "ABSENT-FROM-GRAPH"
    checks = {"C1": c1, "C2": c2, "C3": c3, "C4": c4}
    verdict = "PASS" if all(checks.values()) else "PARTIAL-FALSIFIED"

    lines = [
        "CYCLE: W2-C3TEST-01  (programme section 6.1 item 5)",
        "TYPE: TECHNICAL closure; held C3 is a counterfactual, not a realizability claim",
        "LOCK INPUTS: threshold lock %s" % w1.LOCK_SHA,
        lock_block(os.path.join(ROOT, "runs/W2-C3", "c3_lock.json"), lock_ok,
                   W.verify_lock(os.path.join(ROOT, "runs/W2-C3", "c3_lock.json"))[1]),
        "",
        "[1] C3 STATE VECTOR AT t_mid",
        "    held (counterfactual): Y_e=%s n_e=%s fm^-3 E_F=%s MeV (%s)" %
        (f(frozen["Y_e"], 8), f(frozen["n_e_fm3"], 8), f(frozen["E_F_MeV"], 8),
         frozen["E_F_kind"]),
    ]
    for name, stt in sorted(neut.items()):
        lines.append("    %s: Y_e=%s n_e=%s fm^-3 mu_e=%s MeV mu_kin=%s MeV reduction=%s beta_res=%s" %
                     (name, f(stt["Y_e"], 8), f(stt["n_e_fm3"], 8), f(stt["mu_e_MeV"], 8),
                      f(stt["mu_kin_MeV"], 8), f(stt["reduction"], 8), f(stt["beta_residual"], 4)))
    lines += [
        "",
        "[2] Y_e / n_e / E_F COMPARISON",
        "    all neutronized branches have lower Y_e and n_e: %s" % c1,
        "    mu_kin ratio vs n_e^(2/3) scaling (2D kinetic comparison):",
    ]
    for name, r in sorted(ratios.items()):
        lines.append("      %s: mu_kin/frozen=%s ; n_e_ratio^(2/3)=%s ; rel. diff=%s" %
                     (name, f(r["mu_kin_ratio"], 8), f(r["n_e_power_2_3"], 8),
                      f(r["relative_difference"], 8)))
    lines += [
        "    registered 2/3-power scaling within 2%% in every convention: %s" % c2,
        "    NOTE: the 2/3 power is the prediction fixed in stage A; its failure is recorded,",
        "    not repaired here. A different exponent would be a new claim requiring a new round.",
        "",
        "[3] DOES u CONSUME THE C3 STATE?",
    ]
    for branch, v in sorted(sha.items()):
        lines.append("    %s: plate=%s canvas=%s" %
                     (branch, v["plate_sha256"], v["canvas_sha256"]))
    lines += [
        "    byte identity between held and neutronized branches: %s" % c3,
        "    generator graph: %s ; tokens checked=%s ; hits=%s" %
        (graph["verdict"], ", ".join(graph["tokens"]), json.dumps(graph["hits"])),
        "    verdict: %s" % ("GENERATOR-DOES-NOT-CONSUME" if c4 else "NO-OBSERVED-EFFECT"),
        "    byte identity alone is not used as proof; the graph check is required.",
        "",
        "[4] OTHER C3 SLOTS (kept separate)",
        "    sigma_s(omega): NOT-MEASURED -- no compliant sigma_s exists (G6 / DC2)",
        "    t_life: IMPORTED %s s (scifi_boundary_v1); not derived by this cycle" % f(w1.TAU_C3, 4),
        "    neutrino luminosity ledger: OUT-OF-SCOPE of the declared closure (section 4.2.6)",
        "",
        "[5] PREDICTIONS",
        "    C1 Y_e / n_e fall            %s" % ("PASS" if c1 else "FAIL"),
        "    C2 mu_kin / n_e scaling      %s" % ("PASS" if c2 else "FAIL"),
        "    C3 u byte identity           %s" % ("PASS" if c3 else "FAIL"),
        "    C4 generator graph absence   %s" % ("PASS" if c4 else "FAIL"),
        "    overall: %s" % verdict,
        "",
        "No optical, visibility, effective-2D, or realizability claim follows from this test.",
    ]
    result = os.path.join(ROOT, "runs/W2-C3/c3_results_v1.txt")
    W.write_text(result, W.banner(
        W.PROVENANCE,
        "W2-C3TEST-01 -- C3 CONSUMPTION TEST (HELD VS NEUTRONIZED)", lines))

    profile = {
        "provenance_tag": "PROVENANCE: %s" % W.PROVENANCE,
        "cycle_id": "W2_C3TEST_01", "states": states, "ratios": ratios,
        "generator_graph": graph, "sha256_u": sha, "checks": checks, "verdict": verdict,
        "slots": {"sigma_s": "NOT-MEASURED", "t_life": "IMPORTED", "L_nu": "OUT-OF-SCOPE"},
    }
    write_json(os.path.join(ROOT, "runs/W2-C3/c3_profile_v1.json"), profile)
    record = {
        "provenance_tag": "PROVENANCE: %s" % W.PROVENANCE,
        "cycle_id": "W2_C3TEST_01", "utc": W.utc(),
        "python": sys.version.split()[0], "numpy": np.__version__,
        "modules": {p: W.sha256(os.path.join(ROOT, p)) for p in (
            "src/analysis/w2_common_v1.py", "src/analysis/w2_stageB_v1.py",
            "src/common/conv.py", "src/analysis/w1_row2_common_v1.py")},
        "products": [rel(result), "runs/W2-C3/c3_profile_v1.json"], "rendered_frames": [],
    }
    write_json(os.path.join(ROOT, "runs/W2-C3/c3_run_record_v1.json"), record)
    return result, verdict, checks


# ---------------------------------------------------------------------------
# W2-XCHECK-01 -- cross-check the four unsuspended authorities
# ---------------------------------------------------------------------------
def run_xcheck(lock_ok):
    files = {
        "crosswalk": "docs/conventions/constraint_crosswalk_v1.md",
        "tiers": "docs/specs/intrinsic_structure_tiers_v1.md",
        "ladder": "docs/specs/relaxation_ladder_v1.md",
        "protocol": "docs/program/COMPLETION_PROTOCOL_v1.md",
        "programme": "docs/program/RESEARCH_PROGRAM_v1.md",
    }
    text = {k: open(os.path.join(ROOT, v), "r", encoding="utf-8").read() for k, v in files.items()}
    ids = {c: ("`%s`" % c in text["crosswalk"]) for c in ("C1", "C2", "C3")}
    x1 = all(ids.values())
    lock = json.load(open(W.LOCK, "r", encoding="utf-8"))
    thr_lock = {k: float(v["threshold_c"]) for k, v in lock["tiers"].items()}
    thr_spec = {}
    for tier, pattern in (("L0", r"Q0\s*≥\s*([0-9.]+)"),
                          ("L1", r"Q1\s*≥\s*([0-9.]+)"),
                          ("L2", r"Q2\s*≥\s*([0-9.]+)"),
                          ("L3", r"Q3\s*≥\s*([0-9.]+)")):
        import re
        m = re.search(pattern, text["tiers"])
        thr_spec[tier] = float(m.group(1)) if m else None
    x2 = all(thr_spec[k] is not None and abs(thr_spec[k] - thr_lock[k]) <= 1e-12
             for k in thr_lock)
    import re
    rungs = {}
    for n in range(1, 7):
        m = re.search(r"^\|\s*\*{0,2}`RL-%d`\*{0,2}\s*\|(.*)$" % n, text["ladder"], re.M)
        rungs["RL-%d" % n] = bool(m and m.group(1).strip())
    x3 = all(rungs.values())
    wip = "`WIP = 1`" in text["protocol"]
    report_phrases = [p for p in ("report-only", "report only", "exit 0", "exit code")
                      if p in text["protocol"].lower()]
    programme_report = [p for p in ("report-only", "report only") if p in text["programme"].lower()]
    x4 = wip and bool(report_phrases)
    checks = {"X1": x1, "X2": x2, "X3": x3, "X4": x4}
    verdict = "PASS" if all(checks.values()) else "CITATION-DEFECT"

    lines = [
        "CYCLE: W2-XCHECK-01  (Appendix D declared TECHNICAL cross-check)",
        "TYPE: structural read only; no authority is edited",
        lock_block(os.path.join(ROOT, "runs/W2-XCHECK", "xcheck_lock.json"), lock_ok,
                   W.verify_lock(os.path.join(ROOT, "runs/W2-XCHECK", "xcheck_lock.json"))[1]),
        "",
        "[1] AUTHORITY FILES READ",
    ]
    for k, v in files.items():
        lines.append("    %-10s %s sha256=%s" % (k, v, W.sha256(os.path.join(ROOT, v))))
    lines += [
        "",
        "[2] CROSSWALK IDENTIFIERS",
        "    " + ", ".join("%s=%s" % (k, v) for k, v in ids.items()),
        "    X1: %s" % ("PASS" if x1 else "FAIL"),
        "",
        "[3] TIER THRESHOLDS (spec vs lock)",
    ]
    for k in sorted(thr_lock):
        lines.append("    %s spec=%s lock=%s diff=%s" %
                     (k, f(thr_spec[k], 8), f(thr_lock[k], 8),
                      f(abs(thr_spec[k] - thr_lock[k]) if thr_spec[k] is not None else float("nan"), 4)))
    lines += ["    X2: %s" % ("PASS" if x2 else "FAIL"), "",
              "[4] LADDER RUNGS",
              "    " + ", ".join("%s=%s" % (k, v) for k, v in rungs.items()),
              "    X3: %s" % ("PASS" if x3 else "FAIL"), "",
              "[5] PROTOCOL",
              "    WIP = 1 token found: %s" % wip,
              "    report-only / exit-code phrases in protocol: %s" %
              (", ".join(report_phrases) if report_phrases else "NONE"),
              "    report-only phrases in programme: %s" %
              (", ".join(programme_report) if programme_report else "NONE"),
              "    X4: %s" % ("PASS" if x4 else "FAIL"),
              "    REGISTRATION DEFECT: stage A asked the protocol to contain a report-only statement.",
              "    The protocol does not make that statement, and the programme does not cite it as",
              "    protocol text. This is an over-specified check in the pre-registration, not a change",
              "    to any authority; it is recorded rather than silently re-priced.", "",
              "[6] CONCLUSION",
              "    overall: %s" % verdict,
              "    X1-X3 confirm the clauses this programme relies on; X4 is a citation defect in the",
              "    pre-registered check. No authority was edited and no gate mark was changed.",
    ]
    result = os.path.join(ROOT, "runs/W2-XCHECK/xcheck_results_v1.txt")
    W.write_text(result, W.banner(
        W.PROVENANCE,
        "W2-XCHECK-01 -- FOUR-AUTHORITY CONSISTENCY CROSS-CHECK", lines))

    profile = {
        "provenance_tag": "PROVENANCE: %s" % W.PROVENANCE,
        "cycle_id": "W2_XCHECK_01", "files": {k: {"path": v, "sha256": W.sha256(os.path.join(ROOT, v))}
                                            for k, v in files.items()},
        "ids": ids, "thresholds": {"lock": thr_lock, "spec": thr_spec},
        "rungs": rungs, "protocol": {"wip": wip, "report_phrases": report_phrases,
                                     "programme_report_phrases": programme_report},
        "checks": checks, "verdict": verdict,
    }
    write_json(os.path.join(ROOT, "runs/W2-XCHECK/xcheck_profile_v1.json"), profile)
    record = {
        "provenance_tag": "PROVENANCE: %s" % W.PROVENANCE,
        "cycle_id": "W2_XCHECK_01", "utc": W.utc(),
        "modules": {p: W.sha256(os.path.join(ROOT, p)) for p in (
            "src/analysis/w2_common_v1.py", "src/analysis/w2_stageB_v1.py")},
        "products": [rel(result), "runs/W2-XCHECK/xcheck_profile_v1.json"],
        "rendered_frames": [],
    }
    write_json(os.path.join(ROOT, "runs/W2-XCHECK/xcheck_run_record_v1.json"), record)
    return result, verdict, checks


def main():
    ok, blocks = guard()
    if not ok:
        print("STAGE B REFUSED: one or more stage-A locks failed")
        print("\n\n".join(blocks))
        return 1
    outcomes = []
    outcomes.append(("W2-DISC-01",) + run_disc(ok)[1:])
    outcomes.append(("W2-C2VIOL-01",) + run_c2(ok)[1:])
    outcomes.append(("W2-C3TEST-01",) + run_c3(ok)[1:])
    outcomes.append(("W2-XCHECK-01",) + run_xcheck(ok)[1:])
    print("stage B verdicts:")
    for name, verdict, checks in outcomes:
        print("  %-16s %-18s %s" % (name, verdict, json.dumps(jsonable(checks))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
