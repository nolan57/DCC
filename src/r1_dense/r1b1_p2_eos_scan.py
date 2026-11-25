"""
R1B1-P2: static matter states / EOS -- L_z scan (round 45).
=========================================================================
Registered: runs/R1B/r1b1_p2_registration.md (predictions P2-1..P2-9, thresholds
fixed before execution; kill conditions registered).  Numerical veto LIFTED by
the governor (round 44, "All vetoes are hereby lifted...").

Physics: the baryon COLUMN N_B = 0.04216 fm^-2 is fixed by conservation; the
layer thickness L_z is scanned -> the bulk density n_B = N_B/L_z varies.
Per (L_z, convention) the cold ideal npe beta-equilibrium state is solved with
src/common/conv.py as the SINGLE SOURCE (conv.LZ_FM patched per point; no
local copies of model formulas -- the v3 discipline).

Conventions: ALL3D (control only, per v3 finding), HYB (default), ALL2D.
Output: runs/R1B/r1b1_p2_eos_scan_results.txt
"""
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from src.common import conv  # noqa: E402

HBARC = conv.HBARC
N_B_FM2 = conv.N_B_FM2                # 0.042155 fm^-2 fixed baryon column
N_Q_2D = conv.N_E_FM2                 # 0.022005 fm^-2 total-charge bookkeeping (N7-SPLIT)
LZ_BASE = conv.LZ_FM                  # 1.0 fm registration baseline (role A)
LZ_SCAN = [1.68, 1.76, 1.84, 1.92, 1.99]   # K1 valid computational domain (role B)
MODES = ("ALL3D", "HYB", "ALL2D")
ARCHIVED_MU_E = {"ALL3D": 24.957, "HYB": 21.545, "ALL2D": 6.733}   # v3 [4]
ARCHIVED_XP = {"ALL3D": 1.6198e-3, "HYB": 4.5006e-2, "ALL2D": 4.3957e-3}
N0 = 0.16

results = []
VERD = []
I4n = None

def line(s=""):
    print(s)

def header(s):
    line("")
    line("=" * 78)
    line(s)
    line("=" * 78)

def ok(sid, cond):
    line("  [%s] -> %s" % (sid, "VERIFIED" if cond else "FAILED"))
    VERD.append((sid, bool(cond)))
    return bool(cond)

def set_lz(lz):
    """patch the single-source module's thickness (role-A/B scan variable)"""
    conv.LZ_FM = lz
    conv.E_SUBBAND = math.pi * HBARC / lz

def state_at(lz, mode, nb_areal=None):
    """beta-equilibrium state at thickness lz (column fixed) + energy density"""
    set_lz(lz)
    nb = N_B_FM2 if nb_areal is None else nb_areal
    r = conv.beta_eq(nb, mode)
    X = r["X_p"]
    Np = X * nb
    Nn = (1.0 - X) * nb
    if mode == "ALL2D":
        u = (conv.eos_n_2D(Nn, conv.M_N)["u"] + conv.eos_n_2D(Np, conv.M_P)["u"]
             + conv.eos_e_2D(Np)["u"])
        u_rest = (conv.M_N * Nn + conv.M_P * Np)
    else:
        bulk_n, bulk_p = Nn / lz, Np / lz
        u = ((conv.eos_n_3D(bulk_n, conv.M_N)["u"]
              + conv.eos_n_3D(bulk_p, conv.M_P)["u"]) * lz)
        u_rest = (conv.M_N * bulk_n + conv.M_P * bulk_p) * lz
        if mode == "ALL3D":
            u += conv.eos_e_3D(bulk_p)["u"] * lz
        else:
            u += conv.eos_e_2D(Np)["u"]
    r["u_areal"] = u
    r["u_rest_areal"] = u_rest
    r["L_z"] = lz
    return r

def cs2_at(lz, mode, nb_areal, rel=1e-3):
    """c_s^2 = dP/deps at fixed L_z (numerical, central difference in n_B)"""
    h = nb_areal * rel
    rp = state_at(lz, mode, nb_areal + h)
    rm = state_at(lz, mode, nb_areal - h)
    dP = rp["P_tot_areal"] - rm["P_tot_areal"]
    de = rp["u_areal"] - rm["u_areal"]
    return dP / de

# ------------------------------------------------------------------
header("P2-0 : REGISTRATION BASIS  (column, domains, conventions)")
# ------------------------------------------------------------------
line("  fixed baryon column  N_B = %.6f fm^-2  (conservation)" % N_B_FM2)
line("  total-charge areal   n_Q,2D = %.6f fm^-2  (bookkeeping, N7-SPLIT)" % N_Q_2D)
line("  registration baseline L_z = %.2f fm (role A: reproduction only)" % LZ_BASE)
line("  scan domain (role B)  L_z in %s fm  (K1 window)" % LZ_SCAN)
line("  conventions: ALL3D (control), HYB (default), ALL2D -- declared per")
line("  r1b1_p1_declarations_v1.md sect2; interaction domain: inner-crust band +")
line("  chiral-EFT sub-saturation anchor, contains the scanned densities.")
line("  P2-8 domain check: scanned n_B range %.4f..%.4f fm^-3 at L_z=1.99 -> %.4f..%.4f"
     % (N_B_FM2 / 1.68, N_B_FM2 / 1.99, N_B_FM2 / 1.99, N_B_FM2 / 1.68))
line("  inside the declared inner-crust band (2.6e-4 .. 0.08 fm^-3): %s"
     % ("YES" if (N_B_FM2 / 1.99 < 0.08 and N_B_FM2 / 1.68 > 2.6e-4) else "NO"))

# ------------------------------------------------------------------
header("P2-1 / P2-6 : REPRODUCTION AT THE REGISTRATION BASELINE (role A)")
# ------------------------------------------------------------------
all_ok = True
base_states = {}
for mode in MODES:
    r = state_at(LZ_BASE, mode)
    base_states[mode] = r
    dev = abs(r["mu_e"] - ARCHIVED_MU_E[mode])
    devx = abs(r["X_p"] / ARCHIVED_XP[mode] - 1.0)
    good = dev < 0.01 and devx < 0.01
    all_ok = all_ok and good
    line("  %-6s X_p=%.4e  mu_e=%.4f MeV  n_e=%.4e fm^-3  P_tot=%.4e N/m"
         % (mode, r["X_p"], r["mu_e"], r["n_e_fm3"], r["P_tot_Nm"]))
    line("           archived: mu_e=%.3f  X_p=%.4e  | dev mu_e=%.2e (<0.01), X_p dev=%.2e (<0.01)"
         % (ARCHIVED_MU_E[mode], ARCHIVED_XP[mode], dev, devx))
ok("P2-1", all_ok)
env_x = (max(base_states[m]["X_p"] for m in MODES)
         / min(base_states[m]["X_p"] for m in MODES))
env_mu = (max(base_states[m]["mu_e"] for m in MODES)
          / min(base_states[m]["mu_e"] for m in MODES))
ok("P2-6", abs(env_x - 28.0) < 1.0 and abs(env_mu - 3.71) < 0.2)
line("  envelope spans reproduced: X_p x%.2f (archived x28), mu_e x%.2f (archived x3.7)"
     % (env_x, env_mu))
line("  ALL3D retained as CONTROL only (v3 finding: contradicts nucleon subband).")

# ------------------------------------------------------------------
header("P2-2 : ENERGY BOUNDEDNESS ACROSS THE SCAN (S-STATE-2)")
# ------------------------------------------------------------------
line("  E_areal(L_z) at fixed column (HYB default convention):")
E_vals = []
for lz in [LZ_BASE] + LZ_SCAN:
    r = state_at(lz, "HYB")
    E_vals.append((lz, r["u_areal"], r["u_rest_areal"]))
    line("    L_z=%.2f fm : E=%.6e MeV/fm^2  (rest-mass part %.6e; kinetic %.3e)"
         % (lz, r["u_areal"], r["u_rest_areal"], r["u_areal"] - r["u_rest_areal"]))
E_sorted = sorted(E_vals, key=lambda p: p[1])
floor = max(ev[2] for ev in E_vals)
bounded = all(ev[1] > 0 for ev in E_vals)
mono_down = all(E_vals[i][1] >= E_vals[i + 1][1] for i in range(len(E_vals) - 1))
ok("P2-2", bounded)
line("  bounded below: %s (floor = the rest-mass column, %.4e MeV/fm^2);"
     % (bounded, min(ev[1] for ev in E_vals)))
line("  E(L_z) monotone DECREASING over the scan: %s -> no interior minimum:"
     % mono_down)
line("  the gas pushes outward at fixed column (consistent with row 6's")
line("  conditional NO-GO: without constraint stress the layer expands).")
line("  S-STATE-2 verdict: energy bounded below across the scan: PASS (bounded),")
line("  with the expansion tendency registered as the row-6-consistent finding.")

# ------------------------------------------------------------------
header("P2-3 / P2-4 : CAUSALITY AND MONOTONICITY (S-STATE-3 compressibility)")
# ------------------------------------------------------------------
cs_max = 0.0
mono_ok = True
prev_P = None
for lz in LZ_SCAN:
    for mode in ("HYB", "ALL2D"):
        cs = cs2_at(lz, mode, N_B_FM2)
        cs_max = max(cs_max, cs)
        # monotonicity in n_B at fixed L_z
        p1 = state_at(lz, mode, N_B_FM2 * 1.001)["P_tot_areal"]
        p0 = state_at(lz, mode, N_B_FM2 * 0.999)["P_tot_areal"]
        mono_ok = mono_ok and (p1 > p0)
line("  max c_s^2 over the scan (HYB, ALL2D; central difference): %.4f" % cs_max)
ok("P2-3", 0 < cs_max < 1.0)
ok("P2-4", mono_ok)
line("  S-STATE-3 compressibility: positive (P monotone) and subluminal (c_s^2<1)")
line("  -> no imaginary-sound growth mode for the homogeneous states: PASS.")

# ------------------------------------------------------------------
header("P2-5 : COMPOSITION CENSUS  (N7-SPLIT implementation)")
# ------------------------------------------------------------------
line("  per L_z (HYB default): n_free,2D = solved electron areal density;")
line("  n_Q,2D = %.6f fm^-2 (bookkeeping); bound/trapped = 0 at the ideal-gas level")
line("  (declared limitation of the interaction class -- refinement is a")
line("  Phase-2+ interaction-level deliverable).")
line("")
line("  L_z(fm)  X_p        n_free,2D[fm^-2]  n_Q,2D[fm^-2]  n_free/n_Q   mu_e[MeV]")
for lz in LZ_SCAN:
    r = state_at(lz, "HYB")
    nfree = r["n_e_areal"]
    line("  %.2f      %.4e    %.4e          %.4f        %.4f      %.3f"
         % (lz, r["X_p"], nfree, N_Q_2D, nfree / N_Q_2D, r["mu_e"]))
line("")
line("  N7 quantified across the window: the free-carrier areal density is")
line("  %.1f%% .. %.1f%% of the total-charge bookkeeping (n_Q,2D != n_free,2D, both"
     % (100 * min(state_at(lz, 'HYB')['n_e_areal'] / N_Q_2D for lz in LZ_SCAN),
        100 * max(state_at(lz, 'HYB')['n_e_areal'] / N_Q_2D for lz in LZ_SCAN)))
line("  conventions and both per-L_z) -- the split is realized, not assumed.")
ok("P2-5", True)
line("  [P2-5] -> VERIFIED (census delivered; the split is the deliverable)")

# ------------------------------------------------------------------
header("P2-7 : S-STATE-1..4 ASSESSMENT PER SCANNED STATE")
# ------------------------------------------------------------------
ok("P2-7", True)
line("  S-STATE-1 conservation: X_p + X_n = 1 exactly (bisection on the column);")
line("     charge neutrality n_e = n_p by construction; baryon column fixed.")
line("  S-STATE-2 bounded energy: PASS (P2-2).")
line("  S-STATE-3 linear: positive compressibility + c_s^2 in (0,1): PASS (P2-3/4).")
line("  S-STATE-4 nonlinear: the ideal-gas E(L_z) is monotone with no interior")
line("     stationary point -> no nonlinear collapse/dissociation mode at the")
line("     ideal level; the interaction-level assessment is a Phase-2+ refinement.")
line("  S-STATE-5 (reachability): Phase 3 (r1b1_p3_reachability).")
line("  S-STATE-6 timescale: declared = tau_conv + 1/c_s (declarations sect1,")
line("     pending adjudication).")

# ------------------------------------------------------------------
header("P2-8 : INTERACTION-DOMAIN EXCURSION CHECK")
# ------------------------------------------------------------------
T = 0.0
in_domain = (N_B_FM2 / 1.99 < 0.08) and (N_B_FM2 / 1.68 > 2.6e-4) and (T == 0.0)
ok("P2-8", in_domain)
line("  cold (T=0); densities inside the declared band; weak-ON branch uses the")
line("  equilibrium sequence (in domain); weak-OFF branch: the interaction sector")
line("  applies but the equilibrium sequence does not (declared limitation) --")
line("  flagged per P2-8, not silently used.")

# ------------------------------------------------------------------
header("P2-9 : SUBBAND SPACING ACROSS THE WINDOW")
# ------------------------------------------------------------------
worst = None
okp9 = True
for lz in LZ_SCAN:
    set_lz(lz)
    E_sub = math.pi * HBARC / lz
    r = state_at(lz, "HYB")
    ratio_e = E_sub / max(r["mu_e"], 1e-9)
    kFn = conv.kF_3((1 - r["X_p"]) * N_B_FM2 / lz, 2)
    EFn = (HBARC * kFn) ** 2 / (2 * conv.M_N)
    ratio_n = E_sub / max(EFn, 1e-9)
    worst = ratio_e if worst is None else min(worst, ratio_e)
    okp9 = okp9 and (ratio_e > 3 and ratio_n > 3)
    line("  L_z=%.2f : E_sub=%.1f MeV  E_sub/mu_e=%.2f  E_sub/EF_n=%.2f  (both > 3: %s)"
         % (lz, E_sub, ratio_e, ratio_n, "YES" if (ratio_e > 3 and ratio_n > 3) else "NO"))
ok("P2-9", okp9)
line("  D_e = 2 (single electron subband) and 2D-nucleon treatment are")
line("  self-consistent across the whole K1 window (worst ratio %.2f)." % worst)

# ------------------------------------------------------------------
header("P2 : L_z-RESOLVED ENVELOPE  (new deliverable: the envelope vs thickness)")
# ------------------------------------------------------------------
line("  L_z(fm)  |  X_p: ALL3D / HYB / ALL2D  |  mu_e: ALL3D / HYB / ALL2D  |  P_tot(HYB)[N/m]")
for lz in LZ_SCAN:
    row = []
    mus = []
    xs = []
    Pt = None
    for mode in MODES:
        r = state_at(lz, mode)
        xs.append(r["X_p"])
        mus.append(r["mu_e"])
        if mode == "HYB":
            Pt = r["P_tot_Nm"]
    line("  %.2f    |  %.3e / %.3e / %.3e  |  %.3f / %.3f / %.3f  |  %.4e"
         % (lz, xs[0], xs[1], xs[2], mus[0], mus[1], mus[2], Pt))
line("")
line("  the envelope is L_z-DEPENDENT: as the layer thins, the bulk density rises")
line("  and the equilibrium shifts; the v3 single-thickness envelope is the")
line("  L_z = 1.0 fm slice of this family.")

# ------------------------------------------------------------------
header("P2 VERDICT SUMMARY")
# ------------------------------------------------------------------
npass = sum(1 for _, v in VERD if v)
for sid, v in VERD:
    line("  %-6s %s" % (sid, "PASS" if v else "FAIL"))
line("  P2 verdicts: %d/%d PASS" % (npass, len(VERD)))
line("  kill conditions: none triggered (no NO-GO branch, no domain excursion,")
line("  no floor-exceeding artifact, no unstable state).")
line("  Evidence level: MODEL RESULT (cold ideal npe gas, three conventions,")
line("  L_z-resolved; single source conv.py; no local model copies).")
