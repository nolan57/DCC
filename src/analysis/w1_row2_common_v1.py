# -*- coding: utf-8 -*-
"""
w1_row2_common_v1.py -- shared machinery for the W1 / row-2 artifact cycle.

One module so the pre-registration stage and the render stage cannot diverge:
the scene card, the prediction, and the published frame are all computed from
this file.

Authority:
  docs/program/RESEARCH_PROGRAM_v1.md v1.1.1  (2.5, 2.6, 4.2-4.8, 6.1)
  docs/decisions/front_sweep_v1.md            (delta, 1.457 components/layer, 8.12e9)
  docs/decisions/mid_sweep_frame_v1.md        (the t_mid slot)
  docs/specs/intrinsic_structure_tiers_v1.md  (T0-T3 definitions)
  runs/MATRIX/threshold_lock.json             (thresholds, read, never written)

This module establishes no physics. It computes the declared mechanism's
outputs for a stipulated geometry, so that a frame can be regenerated from the
scene card. It is not a solver of the reduction and makes no realizability claim.
"""

import hashlib
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

import sys
sys.path.insert(0, HERE)
import tiers_core_v1 as tc
import unfold_appearance_v1 as ua

# ---------------------------------------------------------------------------
# 1. stipulated inputs (registered geometry of front_sweep_v1; no free knobs)
# ---------------------------------------------------------------------------
C_LIGHT = 2.99792458e8
H_BODY = 1.738                 # m, phantom height  (front_sweep_v1 table)
DELTA = 0.215e-9               # m, one atomic layer (mechanism property, not a knob)
COMP_PER_LAYER = 1.457         # measured 4-connected components per layer
N_PLATE = 1.18e10              # plate census = 8.12e9 x 1.457
N_SLICE_REG = 8.12e9           # registered peelings
SIDE_REG = 90126               # sites per side
SPACING = 0.4001               # m, site spacing
CANVAS = 36.06e3               # m, array side
V_REG = 0.0601                 # m^3, registered phantom volume
RHO_DECL = 1.0e3               # kg/m^3, declared uniform density for the mass ledger

T_RIP = math.sqrt(2.0) * H_BODY / C_LIGHT     # 8.198682e-9 s
V_FRONT = H_BODY / T_RIP                      # c/sqrt(2)
TAU_C3 = 3.0e-9                               # s, IMPORTED transient (scifi_boundary_v1)
Z_MID = 0.5 * H_BODY

T0_S = 0.0
T_MID_S = 0.5 * T_RIP
T_END_S = T_RIP

# per-piece cross-section table (front_sweep_v1 section 1)
SEG = [
    (0.012, 0.800, 0.0063, 0.0221, 2.00),   # calf -> thigh: TWO legs, 2 components
    (0.800, 0.960, 0.0457, 0.0457, 1.00),
    (0.960, 1.170, 0.0464, 0.0516, 1.00),
    (1.170, 1.380, 0.0540, 0.0540, 1.00),
    (1.380, 1.470, 0.0490, 0.0490, 1.00),
    (1.470, 1.560, 0.0098, 0.0098, 1.00),
    (1.560, 1.738, 0.0202, 0.0303, 1.00),
]
LEG_HALF_SEP = 0.062
TISSUE_RHO = np.array([0.0012, 0.92, 1.06, 1.06, 1.85, 0.26])  # air, fat, muscle, blood, bone, lung


def piece_area(z):
    """single-piece cross-section area at height z (m^2); 0 outside the phantom."""
    for z0, z1, a0, a1, _n in SEG:
        if z0 <= z <= z1:
            t = 0.0 if z1 == z0 else (z - z0) / (z1 - z0)
            return a0 + t * (a1 - a0)
    return 0.0


def total_area(z):
    """total material area at height z: piece area x component count (legs counted twice)."""
    for z0, z1, a0, a1, n in SEG:
        if z0 <= z <= z1:
            t = 0.0 if z1 == z0 else (z - z0) / (z1 - z0)
            return n * (a0 + t * (a1 - a0))
    return 0.0


_ZZ = np.arange(0.0, H_BODY + 1e-9, 2e-4)
_AT = np.array([total_area(v) for v in _ZZ])
_CUM = np.concatenate([[0.0], np.cumsum(0.5 * (_AT[1:] + _AT[:-1]) * np.diff(_ZZ))])


def volume_to(z):
    """integral of the total cross-section from 0 to z (m^3), trapezoid on a 0.2 mm grid."""
    if z <= 0:
        return 0.0
    if z >= H_BODY:
        return float(_CUM[-1])
    return float(np.interp(z, _ZZ, _CUM))


V_RECON = volume_to(H_BODY)


# ---------------------------------------------------------------------------
# 2. the map M and the process state
# ---------------------------------------------------------------------------
def state_at(t):
    """Front state phi(t) and the derived counts. z_f(t) = min(H, v t), v = c/sqrt(2)."""
    zf = min(H_BODY, V_FRONT * t)
    layers = zf / DELTA
    plates = layers * COMP_PER_LAYER
    fill = plates / N_PLATE
    z_dec = max(0.0, zf - V_FRONT * TAU_C3)
    v_swept = volume_to(zf)
    v_dec = volume_to(z_dec)
    return dict(
        t=t, zf=zf, layers=layers, plates=plates, fill=fill,
        z_decayed=z_dec,
        sites=min(1.0, layers / N_SLICE_REG),
        V_swept=v_swept, V_decayed=v_dec, V_live=v_swept - v_dec,
        m_swept=RHO_DECL * v_swept, m_decayed=RHO_DECL * v_dec,
        m_live=RHO_DECL * (v_swept - v_dec),
        z_frac=zf / H_BODY,
    )


# ---------------------------------------------------------------------------
# 3. the two 2D fields the observer samples
# ---------------------------------------------------------------------------
_ZP = np.linspace(0.012, 1.738, 400)
_MEAN = []
for _z in _ZP:
    _cls = ua.slice_at(float(_z), 128, 0.55)
    _MEAN.append(float(TISSUE_RHO[_cls].mean()))
_MEAN = np.array(_MEAN) / TISSUE_RHO.max()


def plate_field(zf, n=128):
    """u(x,y) on one plate: the tissue-density channel of the axial slice the front has reached."""
    zz = float(min(zf, 1.700))
    cls = ua.slice_at(zz, n, 0.55)
    return TISSUE_RHO[cls] / TISSUE_RHO.max()


def canvas_field(st, n=128):
    """u(x,y) at array scale: per-site mean density of the layer that site received.

    M assigns layer k to site k in raster order (a bijection), so site s carries the
    layer swept at z = s H / N_sites.  Downsampled to n^2 blocks, a block is filled
    iff the front has passed it; the value is the block's mean layer density.
    """
    idx = np.arange(n * n).astype(np.float64)
    pos = (idx + 0.5) / (n * n)                       # block position in raster order, 0..1
    z = 0.012 + pos * (H_BODY - 0.012)
    u = np.interp(z, _ZP, _MEAN)
    mask = pos <= st["sites"]
    return np.where(mask, u, 0.0).reshape(n, n)


# ---------------------------------------------------------------------------
# 4. thresholds (read from the lock, never written here)
# ---------------------------------------------------------------------------
LOCK = os.path.join(ROOT, "runs", "MATRIX", "threshold_lock.json")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


with open(LOCK, "r", encoding="utf-8") as f:
    _LOCKJ = json.load(f)
THR = {k: float(v["threshold_c"]) for k, v in _LOCKJ["tiers"].items()}
PRE_CONTRAST = float(_LOCKJ["declared_constants"]["precondition_contrast_min"])
LOCK_SHA = sha256(LOCK)
LOCK_RECORDED = ""
if os.path.exists(LOCK + ".sha256"):
    with open(LOCK + ".sha256", "r", encoding="utf-8") as f:
        LOCK_RECORDED = f.read().strip()

ESTIMATOR = dict(
    identity="intrinsic_structure_tiers_v1 v1 (T0 sec.2, T1 sec.3, T2 sec.4, T3 sec.5)",
    implementation="src/analysis/tiers_core_v1.py (verbatim extraction of src/route/structure_tiers.py)",
    grid=[tc.GRID, tc.GRID], bins=tc.BINS, context_levels=tc.CTX,
    smoothing="T3: DoG, sigma = xi/2 and 2*xi (cells)",
    null_ensemble="uniform iid, %d realisations, seeds %d..%d"
                  % (tc.NULL_M, tc.NULL_SEED0, tc.NULL_SEED0 + tc.NULL_M - 1),
    threshold_lock=LOCK, threshold_lock_sha256=LOCK_SHA,
    threshold_lock_recorded=LOCK_RECORDED,
)


def measure(u, tag):
    """Return (rows, meta). One row per tier, each with value, threshold, verdict, status, note."""
    p0 = tc.total_persistence(u)
    xi, acf = tc.char_scale(u)
    q2p, hm = tc.plug_q2(u)
    Q0 = 1.0 - p0 / _P0_NULL if _P0_NULL > 0 else None
    Q2 = (q2p - _Q2_NULL) / (1.0 - _Q2_NULL) if q2p is not None else None
    r1 = tc.q3(u, xi, tc.Q_INSTR)
    r0 = tc.q3(u, xi, tc.Q_REFL)
    span = float(u.max() - u.min())
    cv = float(u.std() / span) if span > 0 else 0.0
    rows = []

    if span <= 0 or cv < PRE_CONTRAST:
        rows.append(dict(tier="T0", value=None, verdict="NO-VERDICT", status="NO-VERDICT",
                         note="precondition sigma_u/du = %.4f < %.3f (constant or near-constant field)"
                              % (cv, PRE_CONTRAST)))
    else:
        rows.append(dict(tier="T0", value=Q0, verdict="PASS" if Q0 >= THR["L0"] else "FAIL",
                         status="MEASURED", note="Q0 = 1 - P0/P0(null)"))

    if span <= 0:
        rows.append(dict(tier="T1", value=None, verdict="NO-VERDICT", status="NO-VERDICT",
                         note="constant field: autocorrelation undefined"))
    else:
        rows.append(dict(tier="T1", value=xi, verdict="PASS" if xi >= THR["L1"] else "FAIL",
                         status="MEASURED", note="xi in cells (h = 1 cell), w(1/e) = %.4f" % acf))

    if Q2 is None:
        rows.append(dict(tier="T2", value=None, verdict="NO-VERDICT", status="NO-VERDICT",
                         note="H(u) = 0: no levels to predict"))
    else:
        rows.append(dict(tier="T2", value=Q2, verdict="PASS" if Q2 >= THR["L2"] else "FAIL",
                         status="MEASURED", note="Q2 renormalised conditional entropy, H = %.4f bits" % hm))

    if r1 is None:
        rows.append(dict(tier="T3", value=None, verdict="NO-VERDICT", status="NO-VERDICT",
                         note="xi/h = %.3f < 2 or mean = 0: no band-limited contrast" % xi))
    else:
        rows.append(dict(tier="T3", value=r1[0], verdict="PASS" if r1[0] >= THR["L3"] else "FAIL",
                         status="MEASURED",
                         note="q = 1.0 (declared instrument); C_xi = %.6f; q = 0 channel gives Q3 = %.3f"
                              % (r1[1], (r0[0] if r0 else 0.0))))

    for r in rows:
        r["field"] = tag
    meta = dict(field=tag, Q0=Q0, xi=xi, Q2=Q2, Q3=(r1[0] if r1 else None),
                Q3_reflection=(r0[0] if r0 else None),
                C_xi=(r1[1] if r1 else None), sigma_over_du=cv, H_bits=hm, P0=p0)
    return rows, meta


# null statistics are deterministic: same seeds, same ensemble, both stages
_P0_NULL, _Q2_NULL, _P0_SD, _Q2_SD = tc.null_statistics()
NULL_RECORD = dict(P0_mean=_P0_NULL, P0_sd=_P0_SD, Q2_mean=_Q2_NULL, Q2_sd=_Q2_SD,
                   realisations=tc.NULL_M, seed_start=tc.NULL_SEED0)


# ---------------------------------------------------------------------------
# 5. effective-2D record (section 4.7) -- three checks, never merged
# ---------------------------------------------------------------------------
HBAR = 1.054571817e-34
M_E = 9.1093837015e-31
E_CHARGE = 1.602176634e-19
K_B_EV = 8.617333262e-5
N_E_DECL = 1.0e28              # m^-3, declared conduction-electron density of the sheet
T_SHEET = 300.0                # K, declared
E_PROBE = 2.5                  # eV, declared optical channel
LAMBDA_PROBE_NM = 1239.841984 / E_PROBE

kF = (3.0 * math.pi ** 2 * N_E_DECL) ** (1.0 / 3.0)
E_F = (HBAR * kF) ** 2 / (2.0 * M_E) / E_CHARGE                 # eV
DELTA_E_Z = 3.0 * math.pi ** 2 * HBAR ** 2 / (2.0 * M_E * DELTA ** 2) / E_CHARGE
E_OCC = max(E_F, K_B_EV * T_SHEET)
_ratio = DELTA_E_Z / (K_B_EV * T_SHEET)
EPS_Z = math.exp(-_ratio) if _ratio < 700.0 else 0.0
RES_PROBE_NM = 0.5 * LAMBDA_PROBE_NM
DELTA_NM = DELTA * 1e9


def effective2d():
    internal = "PASS" if E_OCC < DELTA_E_Z else "FAIL"
    ext_exc = "PASS" if E_PROBE < DELTA_E_Z else "FAIL"
    ext_res = "PASS" if RES_PROBE_NM <= DELTA_NM else "FAIL"
    return dict(
        subsystem="conduction electrons of the deposited sheet only (declared n_e = 1.0e28 m^-3)",
        subsystem_scope_note=("ionic, lattice, collective and non-degenerate modes are NOT assessed; "
                              "per RESEARCH_PROGRAM_v1 section 4.7 the label must not be extended to them"),
        model="Model B surrogate: infinite square well of width L_z = delta, electron mass",
        model_status=("SURROGATE -- the registered mechanism supplies no confining potential, so this "
                      "Delta_E_z is a bound on a declared model, not the system's own level spacing"),
        L_z_m=DELTA,
        Delta_E_z_eV=DELTA_E_Z,
        Delta_E_z_formula="3 pi^2 hbar^2 / (2 m_e L_z^2)  (infinite square well, first excitation)",
        E_F_eV=E_F,
        T_K=T_SHEET,
        E_occ_eV=E_OCC,
        E_occ_source="max(E_F, k_B T) per effective_2d_definition_v1 section 1",
        eps_z=EPS_Z,
        eps_z_definition="exp(-Delta_E_z / k_B T): Boltzmann occupation of the first z excitation",
        probe="declared optical channel at 2.5 eV, diffraction-limited",
        E_probe_eV=E_PROBE,
        probe_wavelength_nm=LAMBDA_PROBE_NM,
        probe_resolution_nm=RES_PROBE_NM,
        internal_bound=internal,
        external_excitation=ext_exc,
        external_resolution=ext_res,
        external_resolution_note=("layer spacing %.3f nm vs probe point-spread %.1f nm: the declared "
                                  "optical probe cannot resolve z" % (DELTA_NM, RES_PROBE_NM)),
        coupling="NOT-MEASURED (no selection rule or matrix element is registered for this state)",
        label="NOT-MEASURED",
        label_rule="RESEARCH_PROGRAM_v1 section 4.7: NOT-MEASURED when model, subsystem, E_occ, E_probe or eps_z is undeclared",
        missing_slot="model -- no registered Model B/C confining potential for a free-standing atomic layer",
        geometric_thinning="THIN (L_z = 0.215 nm vs body scale 1.7 m)",
        visual_flatness="NOT-ASSESSED (no observer image is rendered in this cycle)",
        claim_barred=("the three checks are recorded separately; this record does not license IS_2D, "
                      "LOOKS_2D, or any readability claim"),
    )


# ---------------------------------------------------------------------------
# 6. palette
# ---------------------------------------------------------------------------
BG = "#FBFAF7"
INK = "#2E2E2C"
MUTED = "#8A877E"
INTACT = "#D8D5CC"
CONVERTED = "#534AB7"
DECAYED = "#A32D2D"
LIVE = "#6B62C9"
