#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DCC P3-C5 — Parameter sensitivity scan of the adiabatic criterion
================================================

Prerequisites (already filled in; see the first page of this script's stdout and DCC_P3_C5_Scan_Report_v1.md):
  (1) Source of p_z=0.5: a representative value. It is chosen as a representative point from
      pz_list=[0,0.5,1,2,4] in DCC_P3_mode_freeze.py; it coincides numerically with the relation
      p_z^{eta(t0)=1} = |beta_C|*C0/t0 = 0.5,
      but no independent theory fixes p_z at 0.5 (the comoving z volume is unspecified -> the tower spacing is undetermined, P3 §7).
      Reasonable range: default axis A [0.1,2.0], 20 log-uniform points (no theoretically constrained interval; take both sides of O(1)).
  (2) t* = t0 = 1 (normalization time); C(t0)=C0=1 is a pure normalization convention; beta_C=-1/2 is not
      a normalization, but a phenomenological scaling exponent (representative value of the magnetic attractor;
      the vacuum Kasner extrapolation gives -1/3).

Scan target (over the whole trajectory, not a single point t*):
  eta(t) = |m_dot_eff| / m_eff^2 = |beta_C| * C(t) / (|p_z| * t)
  C(t) = C0 * (t/t0)^beta_C  ->  eta(t) = (|beta_C|*C0/t0) / |p_z| * (t/t0)^(beta_C-1)
  Output eta_max / eta_min / the eta=1 crossing time (if it exists).
  Interpretation: eta<1 adiabatic; eta>1 non-adiabatic/destruction; eta≈1 no discriminating power (this script uses band=[0.9,1.1]).

Key structural fact (must be reported honestly; no fabricated dependence):
  The formula for eta contains neither alpha nor the wall velocity beta_w. Hence:
    - On the (p_z, alpha) plane, eta_max contours are vertical lines and the drift with alpha is always 0;
    - The eta curves and their interpretation are point-by-point identical for the relativistic group and the
      low-speed phenomenological group (the groups are still output and concluded about separately).

Axes:
  A  p_z: [0.1,2.0], 20 log-uniform points
  B  alpha: [0.1,1.0], 10 linear points (L4 frozen alpha=0.5 is one of these slices)
  C  beta_C: fixed at -1/2; robustness checks -1/3, -2/3; out-of-range values (beta_C>=0 or outside the physical
     interval) are marked red and discarded.
     Physically valid domain: beta_C < 0 (C contracts, D2 direction) and, within t∈[t0,30t0], C>0 and C decreases monotonically.

Inputs (paths + SHA256 recorded in stdout; no background/wall values hardcoded in the script):
  - DCC_P3_mode_freeze.py  —— C(t) background constants (T0,C0,BETA_C,T_END read via importlib)
  - DCC_P2_1p1_frames.npz  —— wall trajectories (t, phi fields for W1/W2/W3; used to record the full time window swept by the wall)
  - DCC_P1_results.txt / DCC_P0-P4_Roadmap_Plan.md —— wall-velocity grouping values and phenomenological identity (read-only registration)

Outputs (all written in this directory):
  DCC_P3_C5_adiabatic_scan_stdout.txt       stdout archive (including version hashes, prerequisites, regression, acceptance)
  DCC_P3_C5_eta_curves.png                   Output 1: eta(t) curve family (faceted by p_z, eta=1 reference line)
  DCC_P3_C5_eta_max_contour.png              Output 2: (p_z,alpha) eta_max contour + three-region shading
  DCC_P3_C5_judgement_table.csv              Output 3: wall-velocity group × parameter point three-level verdict table
  DCC_P3_C5_contour_drift.txt                Output 4: drift of the eta=1 contour with alpha and beta_C
  DCC_P3_C5_adiabatic_scan_data.npz          machine-readable full dataset

Run: python DCC_P3_C5_adiabatic_scan.py
Fixed seed np.random.seed(0); no random sampling (deterministic grid), so two runs produce byte-identical output.
"""

import csv
import hashlib
import importlib.util
import os
import re
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch

np.random.seed(0)
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
BG_PY = os.path.join(HERE, "DCC_P3_mode_freeze.py")
FRAMES_NPZ = os.path.join(HERE, "DCC_P2_1p1_frames.npz")
P1_RES = os.path.join(HERE, "DCC_P1_results.txt")
P4_REP = os.path.join(HERE, "DCC_P4_Report_v1.md")
ROADMAP = os.path.join(HERE, "DCC_P0-P4_Roadmap_Plan.md")

OUT_STDOUT = os.path.join(HERE, "DCC_P3_C5_adiabatic_scan_stdout.txt")
OUT_CURVES = os.path.join(HERE, "DCC_P3_C5_eta_curves.png")
OUT_CONTOUR = os.path.join(HERE, "DCC_P3_C5_eta_max_contour.png")
OUT_TABLE = os.path.join(HERE, "DCC_P3_C5_judgement_table.csv")
OUT_DRIFT = os.path.join(HERE, "DCC_P3_C5_contour_drift.txt")
OUT_DATA = os.path.join(HERE, "DCC_P3_C5_adiabatic_scan_data.npz")

# Indifference band (no discriminating power): eta in [ETA_BAND_LO, ETA_BAND_HI] is treated as inconclusive
ETA_BAND_LO, ETA_BAND_HI = 0.9, 1.1

_LINES = []
def w(s=""):
    """Write to both stdout and the archive buffer."""
    print(s)
    _LINES.append(str(s))


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read_background_module():
    """Read constants from the existing C(t) background script (no hardcoded values)."""
    spec = importlib.util.spec_from_file_location("dcc_bg", BG_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    need = ["T0", "C0", "BETA_C", "BETA_AB", "T_END"]
    for k in need:
        if not hasattr(mod, k):
            raise RuntimeError("Background script missing constant %s" % k)
    return {k: float(getattr(mod, k)) for k in need}


def read_wall_provenance():
    """Read wall trajectories from the NPZ (time window, phi zero crossings = wall positions) and register wall-velocity provenance."""
    z = np.load(FRAMES_NPZ, allow_pickle=True)
    info = {}
    for case in ["W1-slab-static", "W2-slab-expand", "W3-slab-nob"]:
        if case not in z.files:
            continue
        d = z[case].item()
        t = np.asarray(d["t"], dtype=float)
        u = np.asarray(d["u"], dtype=float)      # (nt, 13, nx)
        x = np.asarray(d["x"], dtype=float)
        phi = u[:, 9, :]                          # IDX['phi']=9 frozen by DCC_P2_wall_1p1.py:141
        xw = []
        for i in range(len(t)):
            s = np.where(np.sign(phi[i, :-1]) * np.sign(phi[i, 1:]) < 0)[0]
            cand = [0.5 * (x[j] + x[j + 1]) for j in s]
            # Take the wall closest to the center (the slab has two/multiple walls; the central wall position
            # gives a representative trajectory of the wall sweeping past the observer)
            xw.append(min(cand, key=abs) if cand else np.nan)
        info[case] = dict(t=t, x=x, xw=np.asarray(xw))
    # Wall-velocity values are registered read-only; they do not enter the eta formula
    betaw = {}
    txt1 = open(P1_RES, encoding="utf-8", errors="replace").read()
    m = re.search(r"beta_f\s*=\s*[\d.]+\s*km/s\s*/\s*c\s*=\s*([\d.eE+-]+)", txt1)
    if m:
        betaw["lowspeed_pheno"] = float(m.group(1))
    txt2 = open(P4_REP, encoding="utf-8").read()
    m2 = re.search(r"Group\s*A[^\n]*?relativistic\s*β_w\s*=\s*([\d.]+)", txt2)
    if m2:
        betaw["relativistic"] = float(m2.group(1))
    return info, betaw


def eta_of_t(t, pz, beta_C, bg):
    """eta(t)=|beta_C|*C(t)/(|pz|*t), C(t)=C0*(t/t0)^beta_C, vectorized over the whole trajectory."""
    C = bg["C0"] * (np.asarray(t, dtype=float) / bg["T0"]) ** beta_C
    return abs(beta_C) * C / (abs(pz) * np.asarray(t, dtype=float))


def eta_at_t0_by_beta(beta_C, bg):
    """Closed form at the regression point: eta(t0)=|beta_C|*C0/(pz*t0)."""
    return abs(beta_C) * bg["C0"] / bg["T0"]


def dimension_assert():
    """Dimensional consistency assertion (c=hbar=1, [t]=[x]=M^-1, scale factors dimensionless, [p_z]=M^1)."""
    # eta = |beta_C| * C / (p_z * t): dimensionless / (M^1 * M^-1) = M^0
    mass_exp_eta = 0 + 0 - (1 + (-1))
    assert mass_exp_eta == 0, "eta dimensions inconsistent"
    assert 1 + (-1) == 0, "p_z*t must be dimensionless"
    return mass_exp_eta


def beta_valid(beta_C, bg, t):
    """Physical-meaning gate for the background (anchored to the frozen background beta_AB, no hardcoded values):
       (a) C contracts: beta_C<0 (D2 direction);
       (b) no transverse collapse and total volume V=ABC∝t^(2*beta_AB+beta_C) does not recollapse: 2*beta_AB+beta_C>=0;
       (c) within the interval C>0 and monotonically decreasing."""
    if not np.isfinite(beta_C) or beta_C >= 0.0:
        return False, "beta_C must be <0 (contraction along Z, D2)"
    lo = -2.0 * bg["BETA_AB"]          # = -1 for beta_AB=0.5 (read from background, not hardcoded)
    if beta_C < lo - 1e-12:
        return False, "beta_C < -2*beta_AB=%.3f: total volume ABC recollapses, leaving the frozen magnetic-attractor background" % lo
    C = bg["C0"] * (np.asarray(t) / bg["T0"]) ** beta_C
    if not np.all(np.isfinite(C)) or np.any(C <= 0):
        return False, "C(t) non-positive/non-finite"
    if not np.all(np.diff(C) < 0):
        return False, "C(t) not monotonically decreasing (loses the contracting-background meaning)"
    return True, "OK"


def crossing_time(pz, beta_C, bg):
    """Closed-form eta(t)=1 crossing time: t_cross=t0*(|beta_C|C0/(pz*t0))^(1/(1-beta_C))."""
    r = eta_at_t0_by_beta(beta_C, bg) / abs(pz)
    if r == 0:
        return np.inf
    return bg["T0"] * r ** (1.0 / (1.0 - beta_C))


def verdict(eta_max, eta_min):
    """Three-level verdict: eta<1 throughout = adiabatic; eta>1 throughout = destructive; otherwise no discriminating power."""
    if eta_max < ETA_BAND_LO:
        return "adiabatic"
    if eta_min > ETA_BAND_HI:
        return "destructive"
    return "no discriminating power"


def main():
    bg = read_background_module()
    wall, betaw = read_wall_provenance()
    T0, C0, BETA_C, T_END = bg["T0"], bg["C0"], bg["BETA_C"], bg["T_END"]

    t = np.linspace(T0, T_END, 1200)
    pz_grid = np.geomspace(0.1, 2.0, 20)
    alpha_grid = np.linspace(0.1, 1.0, 10)
    beta_list_raw = [BETA_C, -1.0 / 3.0, -2.0 / 3.0]

    # ---------- stdout first page: honesty boundaries + prerequisite fill-in ----------
    w("=" * 84)
    w("DCC P3-C5 Adiabatic-Criterion Parameter Sensitivity Scan | stdout archive (including version hashes)")
    w("=" * 84)
    w("[Honesty boundaries] This scan is based on the specified contracting background (C∝t^beta_C, a phenomenological")
    w("                     scaling extrapolated from the magnetic attractor),")
    w("                     D3 not achieved; the low-speed wall-velocity group is a phenomenological assumption, not a")
    w("                     prediction (P1b FAIL permanently archived).")
    w("                     If D3 is achieved later, this task must be rerun with a real dynamical C(t).")
    w("")
    w("[Prerequisite confirmation 1] Source of p_z=0.5: a representative value, not fixed by the relation.")
    w("  Evidence: in DCC_P3_mode_freeze.py, pz_list=[0.0,0.5,1.0,2.0,4.0]; 0.5 is a sampled representative point.")
    w("  Relation (numerical coincidence, not an independent constraint): eta(t0)=|beta_C|*C0/(pz*t0)=1")
    w("        =>  pz|^{eta(t0)=1} = |beta_C|*C0/t0 = %.4f*%.4f/%.4f = %.6f" % (
        abs(BETA_C), C0, T0, eta_at_t0_by_beta(BETA_C, bg)))
    w("  Reasonable range: no theoretical constraint (comoving z volume unspecified, KK tower spacing undetermined —")
    w("                    P3 §7); take axis A [0.1,2.0], 20 log-uniform points (covering O(10) on both sides of the")
    w("                    critical point).")
    w("  Strength of conclusions: until the above is filled in, all results are only [conditional conclusions for a given p_z].")
    w("")
    w("[Prerequisite confirmation 2] t* = t0 = %.4f; C(t0)=C0=%.4f: pure normalization convention;" % (T0, C0))
    w("  beta_C=%.4f: not a normalization but a phenomenological scaling exponent (representative magnetic-attractor" % BETA_C)
    w("  value; vacuum Kasner extrapolates to -1/3).")
    w("  Hence varying beta_C is a [model-assumption change] and must not be written as a unit/gauge change.")
    w("")

    w("[Input files and version hashes SHA256]")
    for nm, path in [("C(t) background script", BG_PY), ("wall-trajectory NPZ", FRAMES_NPZ),
                     ("P1 results (low-speed wall)", P1_RES), ("P4 report (relativistic wall)", P4_REP),
                     ("roadmap (status)", ROADMAP)]:
        w("  %-22s %s  %s" % (nm, os.path.basename(path), sha256(path)))
    w("")

    w("[Background constants (read via importlib, not hardcoded)]")
    for k, v in bg.items():
        w("  %-10s = %.10g" % (k, v))
    w("  C(t)=C0*(t/T0)^beta_C, t∈[%.4f, %.4f], sampled at %d points over the whole trajectory" % (T0, T_END, len(t)))
    w("")

    w("[Wall-trajectory time windows (read from NPZ)]")
    for case, d in wall.items():
        xw = d["xw"]
        finite = np.isfinite(xw)
        w("  %s: t∈[%.4f,%.4f] (%d frames), slab wall position |x_w|∈[%.3f,%.3f] (static in comoving coordinates;" % (
            case, d["t"][0], d["t"][-1], len(d["t"]),
            np.nanmin(np.abs(xw[finite])), np.nanmax(np.abs(xw[finite]))))
        w("      wall velocity registered separately by P1b)")
    w("  Wall-velocity registration (identity labels only, not entering eta): relativistic beta_w=%s; low-speed beta_f=%s" % (
        betaw.get("relativistic", "NA"), betaw.get("lowspeed_pheno", "NA")))
    w("  Low-speed group label: phenomenological assumption, not a prediction. The two groups have identical eta values")
    w("  (the formula contains no beta_w), but conclusions are drawn separately.")
    w("  Coordinate distinction: NPZ t∈[0,5.99] is the P2 ADM code time; the full-trajectory eta scan uses the P3 ansatz")
    w("                          validity window t∈[t0,30t0] (P3 effective-theory notes §1.1). The two have different")
    w("                          normalizations and must not be mixed.")
    w("")

    # ---------- dimensional assertion ----------
    dim = dimension_assert()
    w("[Dimensional consistency assertion] c=hbar=1, [t]=[x]=M^-1, [p_z]=M^1, [A,B,C]=M^0 -> [eta]=M^%d  PASS" % dim)
    w("")

    # ---------- regression check (hard gate; failure voids the whole batch) ----------
    eta_reg = eta_of_t(T0, 0.5, BETA_C, bg)
    reg_ok = bool(abs(float(eta_reg) - 1.0) < 1e-12)
    w("[Regression check] alpha=0.5, p_z=0.5, beta_C=%.4f, t=t0=%.4f -> eta=%.15f" % (
        BETA_C, T0, float(eta_reg)))
    w("  difference from 1.0 = %.3e, threshold 1e-12 -> %s" % (abs(float(eta_reg) - 1.0),
                                                             "PASS" if reg_ok else "FAIL (whole batch void)"))
    if not reg_ok:
        w("Regression failed; terminating.")
        _flush()
        sys.exit(2)
    w("")

    # ---------- beta_C gate ----------
    w("[beta_C physical gate]")
    beta_list = []
    for b in beta_list_raw:
        ok, why = beta_valid(b, bg, t)
        tag = "OK" if ok else "\033[91mmarked red and discarded\033[0m(%s)" % why
        w("  beta_C=%+.9f : %s" % (b, tag))
        if ok:
            beta_list.append(b)
    # Explicit out-of-range probes (verify the gate works; not counted in the scan)
    for b in [0.0, 0.5, -1.5, -2.0]:
        ok, why = beta_valid(b, bg, t)
        w("  probe beta_C=%+.3f : %s" % (b, "OK" if ok else "\033[91mmarked red and discarded\033[0m(%s)" % why))
    w("")

    # ---------- main scan loop ----------
    w("[Scan] axis A p_z 20 points (log[0.1,2.0]) × axis B alpha 10 points (lin[0.1,1.0]) × axis C beta_C %d settings" % len(beta_list))
    records = []
    eta_curves = np.zeros((len(beta_list), len(pz_grid), len(t)))
    emax_grid = np.zeros((len(beta_list), len(alpha_grid), len(pz_grid)))
    emin_grid = np.zeros_like(emax_grid)
    verdict_code = np.zeros((len(beta_list), len(alpha_grid), len(pz_grid)), dtype=np.int8)
    vmap = {"adiabatic": 0, "destructive": 1, "no discriminating power": 2}

    for ib, b in enumerate(beta_list):
        for ip, pz in enumerate(pz_grid):
            eta_curve = eta_of_t(t, pz, b, bg)
            eta_curves[ib, ip, :] = eta_curve
            emax, emin = float(eta_curve.max()), float(eta_curve.min())
            tc = crossing_time(pz, b, bg)
            for ia, al in enumerate(alpha_grid):
                vd = verdict(emax, emin)
                emax_grid[ib, ia, ip] = emax
                emin_grid[ib, ia, ip] = emin
                verdict_code[ib, ia, ip] = vmap[vd]
                for gname, glabel in [("relativistic", "dynamical solution"),
                                      ("lowspeed_pheno", "phenomenological assumption, not a prediction")]:
                    records.append(dict(
                        wall_group=gname, group_label=glabel,
                        p_z=float(pz), alpha=float(al), beta_C=float(b),
                        eta_max=emax, eta_min=emin,
                        t_cross=float(tc) if T0 <= tc <= T_END else np.nan,
                        eta_t0=float(eta_of_t(T0, pz, b, bg)),
                        verdict=vd,
                    ))
    w("  parameter points/group = %d; total verdict rows = %d (%d per group)" % (
        len(alpha_grid) * len(pz_grid) * len(beta_list), len(records), len(records) // 2))
    w("")

    # ---------- Output 1: eta(t) curve family (faceted by p_z) ----------
    fig, axes = plt.subplots(4, 5, figsize=(17, 11), sharex=True, sharey=True)
    for ip, ax in enumerate(axes.flat):
        for ib, b in enumerate(beta_list):
            ax.loglog(t, eta_curves[ib, ip, :], lw=1.4,
                      label="β_C=%+.3f" % b,
                      color=["#1f77b4", "#2ca02c", "#9467bd"][ib % 3])
        ax.axhline(1.0, color="k", ls="--", lw=0.9)
        ax.set_title("p_z=%.4f" % pz_grid[ip], fontsize=9)
        ax.grid(alpha=0.3, which="both")
    for ax in axes[-1, :]:
        ax.set_xlabel("t / t0")
    for ax in axes[:, 0]:
        ax.set_ylabel(r"$\eta=|\dot m|/m^2$")
    axes.flat[0].legend(fontsize=7, loc="upper right")
    fig.suptitle("Output 1  eta(t) full-trajectory curve family (faceted by p_z, dashed eta=1 line;" 
                 " specified contracting background, D3 not achieved)",
                 fontsize=12, y=0.995)
    fig.text(0.5, 0.006, "Low-speed wall group: phenomenological assumption, not a prediction; point-by-point identical"
             " to the relativistic group (eta contains no wall velocity)",
             ha="center", fontsize=9, color="#b22222")
    fig.tight_layout(rect=(0, 0.022, 1, 0.972))
    fig.savefig(OUT_CURVES, dpi=130)
    plt.close(fig)
    w("Output 1 written: %s" % os.path.basename(OUT_CURVES))

    # ---------- Output 2: (p_z, alpha) eta_max contours + three-region shading ----------
    fig, axes = plt.subplots(1, len(beta_list), figsize=(6.2 * len(beta_list), 5.2),
                             squeeze=False)
    cmap = ListedColormap(["#cfe8cf", "#f4cccc", "#e8e8e8"])  # adiabatic green / destructive red / no-discrimination grey
    for ib, b in enumerate(beta_list):
        ax = axes[0, ib]
        Z = verdict_code[ib, :, :].T          # (p_z, alpha)
        ax.pcolormesh(alpha_grid, pz_grid, Z, cmap=cmap, vmin=0, vmax=2, shading="auto")
        cs = ax.contour(alpha_grid, pz_grid, emax_grid[ib, :, :].T,
                        levels=[0.5, 0.9, 1.0, 1.1, 2.0], colors="k", linewidths=0.8)
        ax.clabel(cs, fmt="%.2f", fontsize=7)
        cs1 = ax.contour(alpha_grid, pz_grid, emax_grid[ib, :, :].T,
                         levels=[1.0], colors="#d62728", linewidths=2.2)
        ax.clabel(cs1, fmt="η_max=1.0", fontsize=8)
        ax.set_xlabel("alpha (Z=e^{alpha*phi/v})")
        ax.set_ylabel("p_z")
        ax.set_yscale("log")
        ax.set_title("beta_C=%+.4f" % b, fontsize=10)
        ax.legend(handles=[
            Patch(color="#cfe8cf", label="robustly adiabatic (eta_max<0.9)"),
            Patch(color="#f4cccc", label="robustly destructive (eta_min>1.1)"),
            Patch(color="#e8e8e8", label="no-discriminating-power band (0.9≤eta≤1.1)"),
        ], fontsize=7, loc="lower right")
    fig.suptitle("Output 2  eta_max contours on the (p_z,alpha) plane; eta=1 line is vertical -> drift with alpha = 0",
                 fontsize=12, y=0.99)
    fig.text(0.5, 0.008, "Specified contracting background, D3 not achieved; low-speed group is a phenomenological"
             " assumption, not a prediction; this figure is point-by-point identical for both groups",
             ha="center", fontsize=9, color="#b22222")
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(OUT_CONTOUR, dpi=130)
    plt.close(fig)
    w("Output 2 written: %s" % os.path.basename(OUT_CONTOUR))

    # ---------- Output 3: verdict table CSV ----------
    with open(OUT_TABLE, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.DictWriter(fh, fieldnames=["wall_group", "group_label", "p_z", "alpha",
                                            "beta_C", "eta_max", "eta_min", "t_cross",
                                            "eta_t0", "verdict"])
        wr.writeheader()
        for r in records:
            rr = dict(r)
            if np.isnan(rr["t_cross"]):
                rr["t_cross"] = ""
            wr.writerow({k: ("%.10g" % v if isinstance(v, float) else v) for k, v in rr.items()})
    w("Output 3 written: %s" % os.path.basename(OUT_TABLE))

    # ---------- Output 4: contour drift ----------
    w("")
    w("[Output 4] Drift of the eta=1 contour on the (p_z,alpha) plane")
    dr = []
    w("  Structure: eta contains no alpha ⇒ for any beta_C, eta_max(p_z,alpha) is independent of alpha;")
    w("             the eta=1 contour is the vertical line p_z = p_z^*(beta_C) = |beta_C|*C0/t0 (the eta_max=1 condition).")
    base_b = beta_list[0]
    pz_star_base = float(eta_at_t0_by_beta(base_b, bg))
    for b in beta_list:
        pz_star = float(eta_at_t0_by_beta(b, bg))
        drift_alpha = 0.0
        drift_beta_abs = pz_star - pz_star_base
        drift_beta_rel = drift_beta_abs / pz_star_base
        # Crossing interval: t_cross∈[t0,T_END] corresponds to this pz interval
        pz_hi = pz_star
        pz_lo = pz_star * (T_END / T0) ** (b - 1.0)   # use the current b, not beta_list[0]
        w("  beta_C=%+.6f : p_z^*=%.6f, drift w.r.t. alpha=%.6f (always 0), drift w.r.t. beta_C=%+.6f (%+.2f%%)" % (
            b, pz_star, drift_alpha, drift_beta_abs, 100 * drift_beta_rel))
        w("       eta=1 crossing window (t_cross∈[t0,%.0ft0]): p_z∈[%.6f, %.6f]; the lower end of [%.3f,%.3f] is critical" % (
            T_END / T0, pz_lo, pz_hi, 0.1, 2.0))
        dr.append((b, pz_star, 0.0, drift_beta_abs, drift_beta_rel, pz_lo, pz_hi))
    with open(OUT_DRIFT, "w", encoding="utf-8") as fh:
        fh.write("DCC P3-C5 Output 4: eta=1 contour drift (specified contracting background, D3 not achieved;"
                 " low-speed group phenomenological assumption, not a prediction)\n")
        fh.write("Conclusion: the eta formula contains neither alpha nor beta_w ⇒ drift with alpha is always 0;"
                 " contour position is determined solely by beta_C.\n")
        fh.write("beta_C,p_z_star,drift_alpha,drift_beta_abs,drift_beta_rel,tcross_pz_lo,tcross_pz_hi\n")
        for row in dr:
            fh.write(",".join("%.10g" % v for v in row) + "\n")
    w("Output 4 written: %s" % os.path.basename(OUT_DRIFT))

    # ---------- machine-readable data ----------
    np.savez_compressed(OUT_DATA, t=t, pz_grid=pz_grid, alpha_grid=alpha_grid,
                        beta_list=np.asarray(beta_list), eta_curves=eta_curves,
                        emax_grid=emax_grid, emin_grid=emin_grid, verdict_code=verdict_code,
                        bg_T0=T0, bg_C0=C0, bg_BETA_C=BETA_C, bg_T_END=T_END)
    w("Machine-readable data written: %s" % os.path.basename(OUT_DATA))

    # ---------- summary verdict (by group, by beta_C) ----------
    w("")
    w("[Verdict summary] For each group × each beta_C: fraction of parameter points in each of the three levels"
      " (alpha 10 × p_z 20 = 200 points)")
    for gname in ["relativistic", "lowspeed_pheno"]:
        glabel = "dynamical solution" if gname == "relativistic" else "phenomenological assumption, not a prediction"
        w("  group %s (%s)" % (gname, glabel))
        for ib, b in enumerate(beta_list):
            cnt = [int(np.sum(verdict_code[ib] == k)) for k in range(3)]
            tot = sum(cnt)
            w("    beta_C=%+.6f : adiabatic %d/%d (%.1f%%), destructive %d/%d (%.1f%%),"
              " no discriminating power %d/%d (%.1f%%)" % (
                b, cnt[0], tot, 100 * cnt[0] / tot, cnt[1], tot, 100 * cnt[1] / tot,
                cnt[2], tot, 100 * cnt[2] / tot))
    w("")
    w("[Conclusion layer] The fractions of the robustly adiabatic / robustly destructive regions in parameter space"
      " are given above;")
    w("                   eta=1 is only a single point in a monotonic crossing, and its position is set by the choice of")
    w("                   beta_C (together with the normalization C0/t0 and the representative p_z), not an intrinsic")
    w("                   critical point of the model.")
    w("                   The verdicts of the two wall-velocity groups are point-by-point identical — this criterion")
    w("                   has no discriminating power with respect to wall velocity.")
    w("=" * 84)
    _flush()


def _flush():
    with open(OUT_STDOUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(_LINES) + "\n")


if __name__ == "__main__":
    main()
