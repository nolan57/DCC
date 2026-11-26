# -*- coding: utf-8 -*-
"""
w2_common_v1.py -- shared machinery for the W2 continuation cycles.

Cycles served (docs/program/RESEARCH_PROGRAM_v1.md v1.1.1, section 6.1):
  W2-DISC-01    item 3, discretization control (delta x 10)      TECHNICAL
  W2-C2VIOL-01  item 4, not-C2 stretch branch (s = 1.01)         artifact
  W2-C3TEST-01  item 5, C3 multi-variable consumption test        TECHNICAL
  W2-XCHECK-01  Appendix D cross-check of the four authorities    TECHNICAL

This module establishes no physics. It verifies stage-A locks, implements the
declared pushforward on a sampled field, reads the registered electron states,
and formats products. Thresholds are read from runs/MATRIX/threshold_lock.json,
never written here. Run from the repo root with python -I.
"""
import hashlib
import inspect
import json
import os
import re
import sys
from datetime import datetime, timezone

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "src", "common"))

import conv                      # noqa: E402  registered constants and beta equilibrium
import tiers_core_v1 as tc       # noqa: E402  locked tier estimators
import w1_row2_common_v1 as w1    # noqa: E402  the row-2 scene this continuation extends

PROVENANCE = "NEITHER"           # convention/audit products establish no chain or branch claim
LOCK = os.path.join(ROOT, "runs", "MATRIX", "threshold_lock.json")
S_STRETCH = 1.01                 # W2 item 4, stipulated in stage A
DELTA_FACTOR = 10.0              # W2 item 3, stipulated in stage A


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def write_json(path, obj):
    return write_text(path, json.dumps(obj, indent=2, sort_keys=False, ensure_ascii=False) + "\n")


def make_lock(cycle_id, lock_path, files, extra=None):
    """Write the stage-A lock and its digest sidecar. files: label -> relative path."""
    rec = {
        "cycle_id": cycle_id,
        "locked_utc": utc(),
        "purpose": "pre-registration: stage B must verify these hashes before emitting products",
        "files": {k: {"path": v, "sha256": sha256(os.path.join(ROOT, v))}
                  for k, v in files.items()},
        "rendered_artifacts": [],
    }
    if extra:
        rec.update(extra)
    write_json(lock_path, rec)
    write_text(lock_path + ".sha256", sha256(lock_path) + "\n")
    return rec


def verify_lock(lock_path):
    """Return (ok, lines). Checks the lock's own sidecar and every named file."""
    lines = []
    try:
        with open(lock_path, "r", encoding="utf-8") as f:
            lock = json.load(f)
    except (OSError, ValueError) as exc:
        return False, ["lock unreadable: %s" % exc]
    side = lock_path + ".sha256"
    if not os.path.exists(side):
        return False, ["lock has no .sha256 sidecar"]
    with open(side, "r", encoding="utf-8") as f:
        recorded = f.read().split()[0].strip().lower()
    got = sha256(lock_path)
    lines.append("lock digest %s  recorded=%s  %s" %
                 (got[:12], recorded[:12], "OK" if got == recorded else "MISMATCH"))
    ok = got == recorded
    for label, item in lock.get("files", {}).items():
        rel = item["path"]
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            lines.append("  %-16s MISSING %s" % (label, rel))
            ok = False
            continue
        h = sha256(p)
        good = h == item["sha256"].lower()
        lines.append("  %-16s %s  %s" % (label, h[:12], "OK" if good else "MISMATCH"))
        ok = ok and good
    return ok, lines


def banner(tag, title, lines):
    """One and only one provenance declaration per text product."""
    width = 88
    out = ["=" * width, title, "=" * width, "PROVENANCE: %s" % tag]
    out.extend(lines)
    return "\n".join(out) + "\n"


def json_tag(obj):
    """A JSON-safe string whose content is an inline provenance declaration."""
    obj["provenance_tag"] = "PROVENANCE: %s" % PROVENANCE
    return obj


# ---------------------------------------------------------------------------
# The declared not-C2 map: (x,y) -> (s x, s y), s > 1.
# Discrete pushforward with exact mass accounting on the finite sampled window.
# A cell of unit input area maps to output area s^2; its density is divided by
# s^2. Overlap with output cells is apportioned by area; mass whose image falls
# outside the registered window is recorded as OUTFLOW, not silently dropped.
# ---------------------------------------------------------------------------
def stretch_pushforward(u, s=S_STRETCH):
    u = np.asarray(u, dtype=np.float64)
    n = u.shape[0]
    out = np.zeros_like(u, dtype=np.float64)
    m_in = float(u.sum())
    m_out = 0.0
    for i in range(n):
        x0, x1 = s * i, s * (i + 1)
        k0, k1 = int(np.floor(x0)), int(np.ceil(x1))
        fx = []
        for k in range(k0, k1):
            ov = min(x1, k + 1) - max(x0, k)
            if ov > 0 and 0 <= k < n:
                fx.append((k, ov))
        for j in range(n):
            y0, y1 = s * j, s * (j + 1)
            l0, l1 = int(np.floor(y0)), int(np.ceil(y1))
            fy = []
            for l in range(l0, l1):
                ov = min(y1, l + 1) - max(y0, l)
                if ov > 0 and 0 <= l < n:
                    fy.append((l, ov))
            val = float(u[i, j])
            if not fx or not fy:
                m_out += val
                continue
            kept = 0.0
            for k, ovx in fx:
                for l, ovy in fy:
                    contrib = val * ovx * ovy / (s * s)
                    out[k, l] += contrib
                    kept += contrib
            m_out += val - kept
    m_window = float(out.sum())
    return out, dict(
        s=s, detJ=s * s, area_change_fraction=s * s - 1.0,
        mass_in_window=m_window, mass_outflow=m_out,
        mass_before=m_in,
        conservation_residual=abs(m_window + m_out - m_in) / m_in if m_in else 0.0,
        window_deficit_fraction=m_out / m_in if m_in else 0.0,
        boundary_rule="zero-width registered window; image outside it is booked as OUTFLOW",
        interpolation="area-overlap (box) pushforward, no smoothing kernel",
    )


# ---------------------------------------------------------------------------
# C3 state vector (section 4.2.6).  All numbers come from conv.py; no new EOS.
# ---------------------------------------------------------------------------
def c3_states():
    frozen = conv.frozen_state()
    env = conv.beta_envelope()
    out = {
        "HELDC3_counterfactual": {
            "Y_e": float(conv.ZA),
            "n_e_fm3": float(conv.N_E_FM2 / conv.LZ_FM),
            "E_F_MeV": float(frozen["EF_2D"]),
            "E_F_kind": "2D kinetic hbar*c*kF (frozen state)",
            "state": "frozen Z/A=0.522; counterfactual because C3 is in-action NO-GO",
        }
    }
    for mode in conv.MODES:
        st = env[mode]
        out["NEUTRONIZED_" + mode] = {
            "Y_e": float(st["X_p"]),
            "n_e_fm3": float(st["n_e_fm3"]),
            "mu_e_MeV": float(st["mu_e"]),
            "mu_kin_MeV": float(st["mu_e"] - conv.M_E),
            "E_F_kind": "beta-equilibrium total mu_e; mu_kin = mu_e - m_e for kinetic comparison",
            "reduction": float(st["reduction"]),
            "beta_residual": float(st["beta_res"]),
            "state": "beta-equilibrated %s convention" % mode,
        }
    return out


def generator_graph_check():
    """Evidence for/against GENERATOR-DOES-NOT-CONSUME, beyond byte identity."""
    src = os.path.join(HERE, "w1_row2_common_v1.py")
    with open(src, "r", encoding="utf-8") as f:
        text = f.read()
    forbidden = ("Y_e", "n_e", "E_F", "sigma_s", "TAU_C3", "tau_life")
    found = {}
    for fn in ("plate_field", "canvas_field"):
        m = re.search(r"^def %s\(.*?(?=^def |\Z)" % fn, text, re.M | re.S)
        body = m.group(0) if m else ""
        found[fn] = [tok for tok in forbidden if re.search(r"\b%s\b" % re.escape(tok), body)]
    return dict(
        source="src/analysis/w1_row2_common_v1.py",
        functions_checked=sorted(found),
        tokens=list(forbidden),
        hits=found,
        verdict="ABSENT-FROM-GRAPH" if not any(found.values()) else "PRESENT-IN-GRAPH",
        note="absence of composition tokens in both field generators; byte identity alone is not used",
    )


def dependency_versions():
    import matplotlib
    import PIL
    return dict(
        python="%d.%d.%d" % sys.version_info[:3],
        numpy=np.__version__,
        scipy=__import__("scipy").__version__,
        matplotlib=matplotlib.__version__,
        pillow=PIL.__version__,
    )
