# -*- coding: utf-8 -*-
"""
w1_row2_cycle_v1.py -- STAGE B of the W1 / row-2 artifact cycle: verify, render, publish.

Stage A (src/analysis/w1_row2_scene_v1.py) wrote and lock-hashed the scene card, the
manifest, the solver spec and the predicted profile. This stage:

  1. verifies every locked hash -- and stops if the card no longer matches the lock;
  2. renders the three keyframes and a time-compressed sequence (declared compression);
  3. measures T0-T3 on the same fields the prediction used, and reports the difference;
  4. publishes the profile CSV, the effective-2D record, the DISPLAY-DECLARATIONS,
     the results text and the run record.

Programme: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1, sections 2.5, 4.3, 4.5, 4.7, 5.3.

Run: python -I src/analysis/w1_row2_cycle_v1.py
"""

import csv
import io
import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)

import w1_row2_common_v1 as C

OUTDIR = os.path.join(ROOT, "runs", "W1-ROW2")
CYCLE_ID = "W1-ROW2-ARTIFACT-01"
UTC = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------------------------------------------------------------------------
# 1. verify the pre-registration lock
# ---------------------------------------------------------------------------
lock_path = os.path.join(OUTDIR, "row2_lock_v1.json")
with open(lock_path, "r", encoding="utf-8") as f:
    LOCK = json.load(f)
with open(lock_path + ".sha256", "r", encoding="utf-8") as f:
    LOCK_SHA_RECORDED = f.read().split()[0]
LOCK_SHA_OBSERVED = C.sha256(lock_path)

bad = []
for k, v in LOCK["files"].items():
    p = os.path.join(ROOT, v["path"])
    if not os.path.exists(p):
        bad.append((k, "MISSING", v["path"]))
        continue
    h = C.sha256(p)
    if h != v["sha256"]:
        bad.append((k, "CHANGED", v["path"]))

if bad or LOCK_SHA_OBSERVED != LOCK_SHA_RECORDED:
    print("REFUSING TO RENDER: the pre-registration lock does not verify.")
    for k, why, p in bad:
        print("  %-16s %-8s %s" % (k, why, p))
    if LOCK_SHA_OBSERVED != LOCK_SHA_RECORDED:
        print("  lock file itself: %s != %s" % (LOCK_SHA_OBSERVED[:16], LOCK_SHA_RECORDED[:16]))
    print("  stage A must be re-run and re-locked; a frame drawn against an edited card is an illustration.")
    sys.exit(1)

with open(os.path.join(OUTDIR, "row2_prediction_v1.json"), "r", encoding="utf-8") as f:
    PRED = json.load(f)
with open(os.path.join(OUTDIR, "row2_manifest_v1.json"), "r", encoding="utf-8") as f:
    MAN = json.load(f)

STATES = [
    ("t0", C.T0_S, C.state_at(C.T0_S)),
    ("t_mid", C.T_MID_S, C.state_at(C.T_MID_S)),
    ("t_end", C.T_END_S, C.state_at(C.T_END_S)),
]

# ---------------------------------------------------------------------------
# 2. drawing
# ---------------------------------------------------------------------------
def object_panel(ax, st, compact=False):
    z = np.arange(0.0, C.H_BODY + 1e-9, 0.002)
    A = np.array([C.total_area(v) for v in z])
    two = z < 0.800
    r_leg = np.sqrt(np.where(two, A / (2.0 * math.pi), 0.0))
    r_one = np.sqrt(np.where(two, 0.0, A / math.pi))
    groups = ((-C.LEG_HALF_SEP, r_leg), (C.LEG_HALF_SEP, r_leg), (0.0, r_one))

    kept = z >= st["zf"]
    for cx, rr in groups:
        ax.fill_betweenx(z, cx - rr, cx + rr, where=kept, color=C.INTACT, lw=0, zorder=2)
    live = (z >= st["z_decayed"]) & (z < st["zf"])
    for cx, rr in groups:
        ax.fill_betweenx(z, cx - rr, cx + rr, where=live, color=C.CONVERTED, lw=0, zorder=3)
    dead = z < st["z_decayed"]
    for cx, rr in groups:
        ax.fill_betweenx(z, cx - rr, cx + rr, where=dead, color=C.DECAYED, alpha=0.32, lw=0, zorder=4)

    ft = 7.6 if compact else 9.5
    fl = 6.4 if compact else 8.0
    if st["zf"] > 0:
        ax.axhline(st["zf"], color=C.DECAYED, lw=2.0, zorder=6)
        if st["zf"] > 1.62:
            ax.text(-0.385, st["zf"] - 0.022, "front %.3f m" % st["zf"], color=C.DECAYED,
                    fontsize=fl, ha="left", va="top")
        else:
            ax.text(-0.385, st["zf"] + 0.022, "front %.3f m" % st["zf"], color=C.DECAYED,
                    fontsize=fl, ha="left", va="bottom")
    if st["z_decayed"] > 0:
        ax.axhline(st["z_decayed"], color=C.DECAYED, lw=1.0, ls=(0, (3, 2)), zorder=6)
        ax.text(-0.385, st["z_decayed"] + 0.025, "decayed (τ = 3 ns)", color=C.DECAYED,
                fontsize=fl - 0.5, ha="left", va="bottom")

    ax.set_xlim(-0.40, 0.46)
    ax.set_ylim(0.0, 1.90)
    ax.set_ylabel("z  (m, true)", fontsize=fl)
    ax.set_yticks([0.0, 0.5, 1.0, 1.5])
    ax.set_xticks([])
    ax.set_title("A · the object" if compact else "A · the object: intact / converted / decayed",
                 fontsize=ft, pad=5, loc="left")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=fl - 0.5, pad=1)
    ax.text(-0.385, 1.845, "x: equal-area circle   z: true",
            fontsize=fl - 1.4, color=C.MUTED, va="top")
    # legend below the panel: never collides with the moving front/decay labels
    from matplotlib.patches import Patch
    handles = [Patch(facecolor=C.INTACT, edgecolor="none", label="intact"),
               Patch(facecolor=C.CONVERTED, edgecolor="none", label="converted, live"),
               Patch(facecolor=C.DECAYED, alpha=0.32, edgecolor="none", label="converted, decayed")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.015),
              ncol=3, frameon=False, fontsize=fl - 1.0, handlelength=1.1,
              handleheight=0.8, columnspacing=1.0, borderaxespad=0.0)
    return ax


def canvas_panel(ax, st, compact=False):
    n = 256
    u = C.canvas_field(st, n=n)
    m = np.ma.masked_where(u <= 0.0, u)
    cmap = plt.get_cmap("Purples").copy()
    cmap.set_bad("#EFECE3")
    vmax = float(u.max()) if u.max() > 0 else 1.0
    ax.imshow(m, origin="lower", extent=[0.0, C.CANVAS / 1e3, 0.0, C.CANVAS / 1e3],
              cmap=cmap, interpolation="nearest", aspect="equal", vmin=0.0, vmax=vmax)
    ax.set_xlabel("km", fontsize=7.6 if compact else 8, labelpad=1)
    ax.set_ylabel("km", fontsize=7.6 if compact else 8, labelpad=1)
    ax.tick_params(labelsize=6.8 if compact else 7, pad=1)
    ax.set_title("B · the array, 36.1 km" if compact else "B · the assembled array, 36.1 km",
                 fontsize=7.6 if compact else 9.5, pad=5, loc="left")
    ax.text(1.2, C.CANVAS / 1e3 - 1.4,
            "%.1f%% of sites hold a sheet" % (100.0 * st["sites"]),
            fontsize=6.4 if compact else 7.0, color=C.INK, va="top")
    ax.text(1.2, 1.2,
            "%.1f%% decayed  ·  darkness = mean layer density"
            % (100.0 * ((st["V_decayed"] / st["V_swept"]) if st["V_swept"] > 0 else 0.0)),
            fontsize=5.8 if compact else 6.4, color=C.DECAYED, va="bottom")
    for s in ax.spines.values():
        s.set_color("#C9C6BD")
    return ax


def plate_panel(ax, st, compact=False):
    ft = 7.6 if compact else 9.5
    if st["t"] == 0.0:
        ax.set_facecolor("#F4F2EC")
        ax.text(0.5, 0.5, "no sheet yet\nthe front has not arrived", ha="center", va="center",
                fontsize=7.5 if compact else 9.5, color=C.MUTED, transform=ax.transAxes)
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_title("C · one sheet" if compact else "C · one deposited sheet", fontsize=ft, pad=5, loc="left")
        return ax
    zrep = min(st["zf"], 1.700)
    u = C.plate_field(st["zf"])
    ax.imshow(u, origin="lower", extent=[-0.275, 0.275, -0.275, 0.275],
              cmap="gray", vmin=0.0, vmax=1.0, interpolation="nearest")
    ax.set_xlim(-0.275, 0.275); ax.set_ylim(-0.275, 0.275)
    ax.set_xticks([]); ax.set_yticks([])
    title = "C · one sheet, z = %.3f m" % zrep if compact else "C · one deposited sheet: slice at z = %.3f m" % zrep
    ax.set_title(title, fontsize=ft, pad=5, loc="left")
    ax.plot([-0.24, -0.14], [-0.245, -0.245], color="white", lw=3.0, solid_capstyle="butt")
    ax.text(-0.19, -0.225, "0.10 m", color="white", fontsize=6.2 if compact else 6.5,
            ha="center", va="bottom")
    ax.text(0.245, 0.245, "density channel", color="white",
            fontsize=6.0 if compact else 6.5, ha="right", va="top")
    for s in ax.spines.values():
        s.set_color("#C9C6BD")
    return ax


def timeline_panel(ax, t, compact=False):
    span = C.T_RIP / 1e-9
    ax.set_xlim(-0.30, span + 0.30)
    ax.set_ylim(-1.0, 1.0)
    ax.axhline(0.0, color="#C9C6BD", lw=1.0)
    ax.axvspan(0.0, C.TAU_C3 / 1e-9, color=C.DECAYED, alpha=0.10, lw=0)
    ax.text(C.TAU_C3 / 2e-9, 0.55, "τ = 3 ns", color=C.DECAYED, fontsize=6.4 if compact else 7, ha="center")
    for lab, tt in (("t0", 0.0), ("t_mid", C.T_MID_S / 1e-9), ("t_end", C.T_END_S / 1e-9)):
        ax.plot([tt], [0.0], marker="o", ms=4.0 if compact else 4.5, color=C.INK)
        ax.text(tt, -0.50, lab, fontsize=6.4 if compact else 7, ha="center", va="top", color=C.INK)
    ax.plot([t / 1e-9], [0.0], marker="|", ms=10 if compact else 12, color=C.CONVERTED, mew=2)
    ax.set_yticks([])
    if not compact:
        ax.set_xlabel("t  (ns, true scale)", fontsize=7.2, labelpad=1)
    ax.tick_params(labelsize=6.6 if compact else 7, pad=1)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    return ax


def make_figure(t, compact=False):
    st = C.state_at(t)
    if compact:
        figsize = (10.0, 5.6)
        layout = dict(left=0.060, right=0.980, top=0.865, bottom=0.205,
                      wspace=0.22, hspace=0.62)
    else:
        figsize = (13.0, 6.4)
        layout = dict(left=0.055, right=0.978, top=0.870, bottom=0.135,
                      wspace=0.20, hspace=0.40)
    fig = plt.figure(figsize=figsize, facecolor=C.BG)
    g = fig.add_gridspec(2, 3, height_ratios=[1.0, 0.14], width_ratios=[1.0, 1.0, 0.92],
                         **layout)
    axA = fig.add_subplot(g[0, 0])
    axB = fig.add_subplot(g[0, 1])
    axC = fig.add_subplot(g[0, 2])
    axT = fig.add_subplot(g[1, :])
    for ax in (axA, axB, axC, axT):
        ax.set_facecolor(C.BG)

    object_panel(axA, st, compact)
    canvas_panel(axB, st, compact)
    plate_panel(axC, st, compact)
    timeline_panel(axT, t, compact)

    fs = 9.0 if compact else 12.0
    fig.suptitle("Row 2  (C1 C2 ¬C3)   ·   t = %.3f ns   ·   prescribed geometry, 3 ns transient"
                 % (t / 1e-9), fontsize=fs, color=C.INK, y=0.975)
    f1 = 6.6 if compact else 7.3
    f2 = 6.0 if compact else 6.9
    dec = 100.0 * ((st["V_decayed"] / st["V_swept"]) if st["V_swept"] > 0 else 0.0)
    fy = (0.095, 0.058, 0.024) if compact else (0.072, 0.040, 0.014)
    fig.text(0.060, fy[0],
             "C1 HELD (layer→site bijection, deposit = swept)   ·   C2 HELD (no map, det J = 1)   ·   "
             "C3 VIOLATED (τ = 3 ns imported; %.1f%% decayed)" % dec,
             fontsize=f1, color=C.INK)
    fig.text(0.060, fy[1],
             "z_front = %.4f m   ·   %.4e sheets   ·   %.4e fragments (model estimate)   ·   "
             "live %.4f of %.4f m³ swept"
             % (st["zf"], st["layers"], st["plates"], st["V_live"], st["V_swept"]),
             fontsize=f1, color=C.MUTED)
    fig.text(0.060, fy[2],
             "FL1 · false colour · GEOMETRY PRESCRIBED (D2), not solved · no enhancement · "
             "effective-2D label NOT-MEASURED · no visibility claim",
             fontsize=f2, color=C.MUTED)
    return fig


def save_png(fig, path, dpi=170):
    fig.savefig(path, dpi=dpi, facecolor=C.BG)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. measure and compare with the frozen prediction
# ---------------------------------------------------------------------------
measured_rows = []
measured_meta = {}
for tag, t, st in STATES:
    if tag == "t0":
        for field in ("plate", "canvas"):
            for tier in ("T0", "T1", "T2", "T3"):
                measured_rows.append(dict(row=2, keyframe=tag, field=field, tier=tier,
                                          value=None, threshold=C.THR["L" + tier[1]],
                                          verdict="NOT-APPLICABLE", status="NOT-APPLICABLE",
                                          note="no 2D output before the front arrives"))
        measured_meta[tag] = {}
        continue
    fields = {"plate": C.plate_field(st["zf"]), "canvas": C.canvas_field(st)}
    measured_meta[tag] = {}
    for field, u in fields.items():
        rows, meta = C.measure(u, "%s@%s" % (field, tag))
        measured_meta[tag][field] = meta
        for r in rows:
            measured_rows.append(dict(row=2, keyframe=tag, field=field, tier=r["tier"],
                                      value=r["value"], threshold=C.THR["L" + r["tier"][1]],
                                      verdict=r["verdict"], status=r["status"], note=r["note"]))

pred_index = {(r["keyframe"], r["field"], r["tier"]): r for r in PRED["profile"]}
mism = []
for r in measured_rows:
    p = pred_index[(r["keyframe"], r["field"], r["tier"])]
    if p["verdict"] != r["verdict"]:
        mism.append((r, p, "verdict"))
        continue
    a, b = p["value"], r["value"]
    if (a is None) != (b is None):
        mism.append((r, p, "value-presence"))
    elif a is not None and abs(a - b) > 1e-12 * max(1.0, abs(a)):
        mism.append((r, p, "value"))

# ---------------------------------------------------------------------------
# 4. render
# ---------------------------------------------------------------------------
PNGS = ["row2_t0.png", "row2_tmid.png", "row2_tend.png"]
for (tag, _t, _st), name in zip(STATES, PNGS):
    save_png(make_figure(_t), os.path.join(OUTDIR, name))

N_GIF = 36
frames = []
for i in range(N_GIF):
    t = C.T_RIP * i / (N_GIF - 1)
    fig = make_figure(t, compact=True)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=80, facecolor=C.BG)
    plt.close(fig)
    buf.seek(0)
    frames.append(Image.open(buf).convert("RGB"))
GIF = "row2_sequence.gif"
frames[0].save(os.path.join(OUTDIR, GIF), save_all=True, append_images=frames[1:],
               duration=90, loop=0, optimize=True)

# ---------------------------------------------------------------------------
# 5. DISPLAY-DECLARATION sidecars
# ---------------------------------------------------------------------------
for name, tag, t, st in zip(PNGS, [s[0] for s in STATES], [s[1] for s in STATES], [s[2] for s in STATES]):
    tspan = 0.0
    side = (
        "DISPLAY-DECLARATION v1\n"
        "FRAME:            %s\n"
        "PROVENANCE:       NEITHER\n"
        "STAGE:            S0\n"
        "FIDELITY:         FL1\n"
        "BAND:             NONE (declared density channel; no spectral measurement)\n"
        "COLOUR:           DECLARED-CONVENTION\n"
        "COLOUR-BASIS:     panel A: hue separates intact / converted-live / converted-decayed matter; "
        "panel B: a sequential violet ramp encodes the per-site mean layer density and pale beige marks "
        "sites the front has not reached; panel C: greyscale is the declared tissue-density index. "
        "No wavelength information is carried at any stage\n"
        "SCALAR:           tissue-density index (dimensionless); z (m); per-site mean layer density "
        "(dimensionless); time (ns)\n"
        "TIME:             t_span = %.1f s (single snapshot) ; compression = 1 ; t_rip = %.6e s ; ratio = 0\n"
        "GEOMETRY:         PRESCRIBED (D2)\n"
        "ENHANCEMENT:      none\n"
        "ME5-COROLLARY:    PRESENT\n"
        % (name, tspan, C.T_RIP)
    )
    with open(os.path.join(OUTDIR, name.replace(".png", ".display.txt")), "w",
              encoding="utf-8", newline="\n") as f:
        f.write(side)

gif_side = (
    "DISPLAY-DECLARATION v1\n"
    "FRAME:            %s\n"
    "PROVENANCE:       NEITHER\n"
    "STAGE:            S0\n"
    "FIDELITY:         FL1\n"
    "BAND:             NONE (declared density channel; no spectral measurement)\n"
    "COLOUR:           DECLARED-CONVENTION\n"
    "COLOUR-BASIS:     as the keyframes: hue separates matter states and array occupancy, no wavelength "
    "information is carried\n"
    "SCALAR:           tissue-density index (dimensionless); z (m); per-site mean layer density; time (ns)\n"
    "TIME:             t_span = %.6e s ; compression = %.6e x ; t_rip = %.6e s ; ratio = 1.000\n"
    "GEOMETRY:         PRESCRIBED (D2)\n"
    "ENHANCEMENT:      none\n"
    "ME5-COROLLARY:    PRESENT (the sequence spans t_rip; the 3 ns transient is shorter and is declared)\n"
    % (GIF, C.T_RIP, C.T_RIP / (N_GIF * 90e-3), C.T_RIP)
)
with open(os.path.join(OUTDIR, GIF.replace(".gif", ".display.txt")), "w",
          encoding="utf-8", newline="\n") as f:
    f.write(gif_side)

# ---------------------------------------------------------------------------
# 6. profile CSV and effective-2D record
# ---------------------------------------------------------------------------
CSV = "row2_profile_v1.csv"
with open(os.path.join(OUTDIR, CSV), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["row", "keyframe", "field", "tier", "value", "threshold",
                                      "verdict", "status", "note"])
    w.writeheader()
    for r in measured_rows:
        w.writerow({**r, "value": "" if r["value"] is None else "%.10g" % r["value"]})

E2D = C.effective2d()
E2D_PATH = "row2_effective2d_v1.json"
with open(os.path.join(OUTDIR, E2D_PATH), "w", encoding="utf-8", newline="\n") as f:
    json.dump(E2D, f, indent=2, ensure_ascii=False)
    f.write("\n")

# ---------------------------------------------------------------------------
# 7. results text
# ---------------------------------------------------------------------------
def fnum(v, nd=6):
    if v is None:
        return "-"
    if isinstance(v, str):
        return v
    return ("%%.%de" % nd) % v if (abs(v) >= 1e5 or (v != 0 and abs(v) < 1e-3)) else ("%%.%df" % nd) % v


R = []
A = R.append
A("=" * 100)
A("W1 / ROW 2 -- ARTIFACT CYCLE (C1 C2 not-C3)  ·  %s" % CYCLE_ID)
A("=" * 100)
A("  programme : docs/program/RESEARCH_PROGRAM_v1.md v1.1.1")
A("  stage A   : %s (locked)" % LOCK["locked_utc"])
A("  stage B   : %s" % UTC)
A("  lock      : row2_lock_v1.json sha256 %s  (verified: %d/%d files)"
  % (LOCK_SHA_OBSERVED, len(LOCK["files"]) - len(bad), len(LOCK["files"])))
A("  verdict   : %s  -- %s" % (MAN["acceptance"]["verdict"], MAN["acceptance"]["verdict_reason"]))
A("")
A("1. DERIVED SCALARS (from the stipulated geometry; no free parameter)")
A("-" * 100)
A("  t_rip              = %.10e s  = %.4f ns" % (C.T_RIP, C.T_RIP / 1e-9))
A("  v_front            = c/sqrt(2) = %.6e m/s" % C.V_FRONT)
A("  delta              = %.3e m     components/layer = %.3f" % (C.DELTA, C.COMP_PER_LAYER))
A("  N_slices           = H/delta = %.4e     plate census = %.4e (MODEL ESTIMATE)" %
  (C.H_BODY / C.DELTA, C.N_PLATE))
A("  V_reconstructed    = %.6f m^3     V_registered = %.4f m^3     ratio = %.4f"
  % (C.V_RECON, C.V_REG, C.V_RECON / C.V_REG))
A("  tau_C3 / t_rip     = %.4f     a 3 ns state cannot span the sweep" % (C.TAU_C3 / C.T_RIP))
A("")
A("2. PER-FRAME STATE AND LEDGER (programme 2.6 and 4.2.3)")
A("-" * 100)
A("  %-6s %8s %10s %11s %11s %11s %11s %8s" %
  ("frame", "t (ns)", "z_front", "V_depos", "V_swept", "V_decayed", "V_live", "decayed"))
for tag, t, st in STATES:
    dec = st["V_decayed"] / st["V_swept"] if st["V_swept"] > 0 else 0.0
    A("  %-6s %8.3f %10.4f %11.5f %11.5f %11.5f %11.5f %7.1f%%" %
      (tag, t / 1e-9, st["zf"], st["V_swept"], st["V_swept"], st["V_decayed"], st["V_live"], 100 * dec))
A("")
A("  residual V_deposited - V_swept = 0.0 for every frame: C1 is HELD by the bijection")
A("  layer k -> site k, so the deposit equals the swept volume by construction, not by measurement.")
A("  The decayed volume is a boundary TERMINATION of the 2D domain, not a leak inside it.")
A("")
A("3. TIER PROFILE -- measured, with the frozen prediction beside it")
A("-" * 100)
A("  %-6s %-7s %-3s %-13s %-13s %-10s %s" %
  ("frame", "field", "tier", "measured", "predicted", "verdict", "note"))
for r in measured_rows:
    p = pred_index[(r["keyframe"], r["field"], r["tier"])]
    A("  %-6s %-7s %-3s %-13s %-13s %-10s %s" %
      (r["keyframe"], r["field"], r["tier"], fnum(r["value"]), fnum(p["value"]),
       r["verdict"], r["note"]))
A("")
A("  prediction check: %s  (%d cell(s) differ)" %
  ("PASS -- measured profile reproduces the locked prediction" if not mism else "FAIL", len(mism)))
for r, p, why in mism:
    A("    MISMATCH %s/%s/%s %s: predicted %s, measured %s" %
      (r["keyframe"], r["field"], r["tier"], why, p["value"], r["value"]))
A("")
A("  estimator : %s" % C.ESTIMATOR["identity"])
A("  null      : %s" % C.ESTIMATOR["null_ensemble"])
A("  null means: P0 = %.6e (sd %.2e) ; Q2 = %.6f (sd %.2e)"
  % (C.NULL_RECORD["P0_mean"], C.NULL_RECORD["P0_sd"],
     C.NULL_RECORD["Q2_mean"], C.NULL_RECORD["Q2_sd"]))
A("  rng       : seeds %d..%d, %d realisations, no other stochastic element"
  % (C.tc.NULL_SEED0, C.tc.NULL_SEED0 + C.tc.NULL_M - 1, C.tc.NULL_M))
A("  lock      : %s sha256 %s" % (C.ESTIMATOR["threshold_lock"], C.LOCK_SHA))
A("")
A("  Note on the canvas field: at t_end the array is fully covered, so its structure is the")
A("  layer-density profile along the raster; its T0 measures that profile's topology, not the")
A("  array's uniformity. The two fields answer different questions and are not ranked against")
A("  each other.")
A("")
A("4. EFFECTIVE-2D RECORD (programme 4.7; label = NOT-MEASURED)")
A("-" * 100)
for k in ("model", "model_status", "subsystem", "Delta_E_z_eV", "E_F_eV", "E_occ_eV",
          "eps_z", "E_probe_eV", "probe_resolution_nm", "internal_bound",
          "external_excitation", "external_resolution", "coupling", "label", "missing_slot",
          "geometric_thinning", "visual_flatness"):
    A("  %-24s %s" % (k, E2D[k]))
A("")
A("  The three external checks are separate and are not merged into a label:")
A("    excitation : %.3f eV < Delta_E_z = %.3f eV -> the probe cannot excite z" %
  (E2D["E_probe_eV"], E2D["Delta_E_z_eV"]))
A("    resolution : probe point-spread %.1f nm vs layer spacing %.3f nm -> z is unresolved" %
  (E2D["probe_resolution_nm"], C.DELTA_NM))
A("    coupling   : NOT-MEASURED (no selection rule is registered)")
A("  Geometric thinning is THIN and visual flatness is NOT-ASSESSED. Neither substitutes for the")
A("  four-slot conditional, which is NOT-MEASURED because no confining potential is registered.")
A("")
A("5. FINDINGS")
A("-" * 100)
A("  F1  The 16.9% volume shortfall recorded in runs/FRONT/mid_sweep_frame_results.txt (N9') is")
A("      the missing factor of two on the two-leg region, not a defect of the area table.")
A("      Counting calf->thigh as per-piece areas and doubling gives V = %.5f m^3," % C.V_RECON)
A("      %.2f%% above the registered 0.0601 m^3. The residual is the declared piecewise-linear" %
  (100 * (C.V_RECON / C.V_REG - 1)))
A("      interpolation of the per-region ranges, not a second error. N9' is not edited; this cycle")
A("      records the reconciliation. N9's conclusion is retained, for the correct reason: the")
A("      continuous volume fraction is a declared linear interpolation, not a registered profile.")
A("")
A("  F2  The 3 ns transient is shorter than the %.4f ns sweep by a factor %.2f. At t_end," %
  (C.T_RIP / 1e-9, C.T_RIP / C.TAU_C3))
A("      %.1f%% of the deposited volume has already left the 2D state. Row 2 therefore cannot"
  % (100 * STATES[2][2]["V_decayed"] / STATES[2][2]["V_swept"]))
A("      present a completed deposit: the 'after the sweep' frame is mostly decayed matter, and")
A("      only the last 3 ns of swept material is still converted. This is a property of the")
A("      declared transient, not a derivation of it (tau is imported).")
A("")
A("  F3  The declared optical probe can neither excite nor resolve z (layer spacing %.3f nm," % C.DELTA_NM)
A("      probe point-spread %.1f nm), yet the cell is still NOT-MEASURED: 'cannot see z' and" % E2D["probe_resolution_nm"])
A("      'is 2D' are different claims, and the missing slot is the confining potential, not the probe.")
A("")
A("  F4  The profile does not rank the two fields, and the tiers move in opposite directions:")
A("      the canvas field is smoother than the sheet field (xi = %.1f vs %.1f cells) yet has" %
  (measured_meta["t_end"]["canvas"]["xi"], measured_meta["t_end"]["plate"]["xi"]))
A("      lower legibility (Q3 = %.2f vs %.2f at the same q = 1). A single 'structure score' would" %
  (measured_meta["t_end"]["canvas"]["Q3"], measured_meta["t_end"]["plate"]["Q3"]))
A("      have to choose between them. Every cell also PASSes its threshold, so the tiers separate")
A("      these scenes from the null ensemble (Q0 ~ 0, Q2 ~ 0, xi < 1) but do not discriminate")
A("      between structured scenes. That is a property of the tiers, not of the scene.")
A("")
A("6. O0 ACCEPTANCE (programme 2.5)")
A("-" * 100)
for k, v in MAN["acceptance"]["o0_minimum_items"].items():
    A("  %-48s %s" % (k, v))
A("")
A("  publication items:")
for k, v in MAN["acceptance"]["publication_items"].items():
    A("  %-48s %s" % (k, v))
A("")
A("  => %s. The frame set is citable as an artifact; it is not a RESULT." % MAN["acceptance"]["verdict"])
A("")
A("7. REPRODUCTION")
A("-" * 100)
A("  R2 only: the physical quantities (counts, volumes, profile) are reproducible from the card,")
A("  manifest and solver spec. Frame reproduction (R3) is NOT claimed.")
A("  commands: python -I src/analysis/w1_row2_scene_v1.py")
A("            python -I src/analysis/w1_row2_cycle_v1.py")
A("")

RESULTS = "row2_results_v1.txt"
with open(os.path.join(OUTDIR, RESULTS), "w", encoding="utf-8", newline="\n") as f:
    f.write("\n".join(R) + "\n")

# ---------------------------------------------------------------------------
# 8. run record
# ---------------------------------------------------------------------------
script = os.path.abspath(__file__)
outputs = {}
for name in PNGS + [GIF, "row2_t0.display.txt", "row2_tmid.display.txt", "row2_tend.display.txt",
                    "row2_sequence.display.txt", CSV, E2D_PATH, RESULTS]:
    p = os.path.join(OUTDIR, name)
    if os.path.exists(p):
        outputs[name] = dict(path="runs/W1-ROW2/" + name, sha256=C.sha256(p))

RECORD = dict(
    cycle_id=CYCLE_ID,
    utc=UTC,
    python=sys.version.split()[0],
    numpy=np.__version__,
    matplotlib=matplotlib.__version__,
    pillow=Image.__version__ if hasattr(Image, "__version__") else "n/a",
    inputs=dict(
        stage_a=dict(path="src/analysis/w1_row2_scene_v1.py",
                     sha256=C.sha256(os.path.join(ROOT, "src/analysis/w1_row2_scene_v1.py"))),
        shared_module=dict(path="src/analysis/w1_row2_common_v1.py",
                           sha256=C.sha256(os.path.join(ROOT, "src/analysis/w1_row2_common_v1.py"))),
        tiers_core=dict(path="src/analysis/tiers_core_v1.py",
                        sha256=C.sha256(os.path.join(ROOT, "src/analysis/tiers_core_v1.py"))),
        phantom=dict(path="src/analysis/unfold_appearance_v1.py",
                     sha256=C.sha256(os.path.join(ROOT, "src/analysis/unfold_appearance_v1.py"))),
        threshold_lock=dict(path="runs/MATRIX/threshold_lock.json", sha256=C.LOCK_SHA),
    ),
    preregistration=dict(lock="runs/W1-ROW2/row2_lock_v1.json", sha256=LOCK_SHA_OBSERVED,
                         lock_sha256_file=LOCK_SHA_RECORDED, verified=True,
                         files=LOCK["files"]),
    prediction_check=dict(n_cells=len(measured_rows), n_mismatch=len(mism),
                          status="PASS" if not mism else "FAIL"),
    outputs=outputs,
    reproduction_level="R2 (physical quantities); frame reproduction not claimed (R3)",
    notes=("artifact cycle; geometry PRESCRIBED (D2); C3 is a declared imported transient; "
           "no reduction equation is solved; no visibility, readability or realizability claim"),
)
REC_PATH = "row2_run_record_v1.json"
with open(os.path.join(OUTDIR, REC_PATH), "w", encoding="utf-8", newline="\n") as f:
    json.dump(RECORD, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("\n".join(R))
print("  outputs:")
for k, v in outputs.items():
    print("    %-28s %s" % (v["sha256"][:16], k))
print("  run record: %s" % REC_PATH)
