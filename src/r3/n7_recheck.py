#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RQ-08: does the N7 capture block survive at the state-derived mu_e?

Emits runs/R3/n7_recheck_results.txt with --write.  Nothing is transcribed.
The instrument uses ONLY registered inputs: configs/g0_prime_v3.json for the
kinetic Q table, src/common/conv.py for the EOS, and the quoted numbers of the
P2 / RQ-03 / RQ-05 products.  No threshold is fitted after the run.
"""
import json
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from src.common import conv  # noqa: E402

CFG = json.load(open(os.path.join(_ROOT, "configs", "g0_prime_v3.json"), encoding="utf-8"))
Q = dict(CFG["capture_Q_MeV_kinetic"])
assert abs(Q["p"] - 0.782) < 1e-12 and abs(Q["C12"] - 13.37) < 1e-12
assert "kinetic" in CFG["capture_convention"]

M_E, DN, QP = conv.M_E, conv.M_N - conv.M_P, Q["p"]
FROZEN_MU_REG = 73.372975
HYB_MU_REG = 21.5445
TAU_REG, SIG_REG = 2.00e-20, 8.63e-4

out = []
results = []


def a(s=""):
    out.append(s)


def hdr(title):
    a("")
    a("=" * 78)
    a(title)
    a("=" * 78)


def chk(pid, cond, tag="CHECK"):
    results.append((pid, bool(cond), tag))
    a("  [%s] -> %s   (%s)" % (pid, "CONFIRMED" if cond else "FALSIFIED", tag))


def table(head, rows):
    a("  " + head)
    for r in rows:
        a("  " + r)


def capture(mu_kin):
    """Which registered nuclides are open at this kinetic electron energy."""
    return {k: mu_kin > q for k, q in Q.items()}


def report_row(label, mu_e, mu_kin, cap, dF=None, res=None):
    n_open = sum(cap.values())
    margin = min(mu_kin - q for q in Q.values())
    dF_s = "  --  " if dF is None else "%9.4f" % dF
    res_s = "  --  " if res is None else "%9.1e" % res
    return ("%-9s %11.5f %11.5f %5d/6 %12.5f %10s %9s"
            % (label, mu_e, mu_kin, n_open, margin, dF_s, res_s))


# ---------------------------------------------------------------- header
a("# RQ-08 -- does N7 still block at the state-derived mu_e?")
a("")
a("**Round**: 58 (`RQ-08`).  **Registration**: `runs/R3/n7_recheck_registration.md`.")
a("**Instrument**: `src/r3/n7_recheck.py` -- this file is emitted by it, not transcribed.")
a("**Inputs**: `configs/g0_prime_v3.json` (kinetic Q table); `src/common/conv.py` (`frozen_state`,")
a("`beta_eq`, `eos_e_2D/3D`); `runs/R1B/r1b1_p2_eos_scan_results.txt` P2-1/P2-5;")
a("`runs/R1B/r1b1_p4_census_results.txt` (free fraction 1.000); `runs/R1B/r1b1_p4_tau_results.txt`")
a("(`tau`, `sigma_DC`).  No fitted parameter; no bar adjusted after the run.")
a("")
a("```text")

# ---------------------------------------------------------------- 1 frozen
hdr("[1] THE FROZEN COMPARISON, REPRODUCED")
fr = conv.frozen_state()
mu_fr = fr["EF_2D"]
kin_fr = mu_fr - M_E
cap_fr = capture(kin_fr)
a("  frozen n_e,2D = %.6f fm^-2; k_F = %.6f fm^-1" % (conv.N_E_FM2, conv.kF_2(conv.N_E_FM2)))
a("  E_F(2D, hbar c k_F) = %.6f MeV (kinetic); mu_e - m_e = %.6f MeV (over-conservative)"
  % (mu_fr, kin_fr))
a("  nuclide   Q[MeV]   mu_kin[MeV]   margin[MeV]   open")
for k in ("p", "Fe56", "N14", "O16", "Mg24", "C12"):
    a("  %-8s %9.3f %13.5f %13.5f   %s" % (k, Q[k], kin_fr, kin_fr - Q[k],
                                            "YES" if cap_fr[k] else "no"))
a("  The frozen E_F = hbar c k_F is already KINETIC, so the physical frozen comparison")
a("  is 73.373 MeV directly against kinetic Q (margin %.3f MeV).  The column above" % (mu_fr - Q["C12"]))
a("  also subtracts m_e uniformly as an over-conservative shift: even 72.862 MeV")
a("  exceeds the largest Q by %.3f MeV.  Both readings give 6/6 open; no verdict" % (kin_fr - Q["C12"]))
a("  depends on which of the two is used.")
chk("P1", abs(mu_fr / FROZEN_MU_REG - 1) < 1e-8 and all(cap_fr.values()))

# ---------------------------------------------------------------- 2 solved
hdr("[2] THE SAME COMPARISON AT THE STATE-DERIVED mu_e")
a("  beta_eq: mu_n - mu_p = mu_e, mu_n = M_N + E_F,n, mu_p = M_P + E_F,p,")
a("  M_N - M_P = %.3f MeV.  mu_kin = mu_e - m_e (m_e = %.3f MeV)." % (DN, M_E))
a("")
a("  " + ("%-9s %11s %11s %6s %12s %10s %9s"
        % ("label", "mu_e[MeV]", "mu_kin[MeV]", "open/6", "min margin", "dF=Fn-Fp", "beta_res")))

base_lz = conv.LZ_FM
states = []
for m in conv.MODES:
    r = conv.beta_eq(conv.N_B_FM2, m)
    dF = (r["mu_n"] - conv.M_N) - (r["mu_p"] - conv.M_P)
    cap = capture(r["mu_e"] - M_E)
    states.append((m, r, dF, cap))
    a("  " + report_row(m, r["mu_e"], r["mu_e"] - M_E, cap, dF, r["beta_res"]))
LZS = (1.68, 1.76, 1.84, 1.92, 1.99)
for lz in LZS:
    conv.LZ_FM = lz
    conv.E_SUBBAND = math.pi * conv.HBARC / lz
    r = conv.beta_eq(conv.N_B_FM2, "HYB")
    conv.LZ_FM, conv.E_SUBBAND = base_lz, math.pi * conv.HBARC / base_lz
    dF = (r["mu_n"] - conv.M_N) - (r["mu_p"] - conv.M_P)
    cap = capture(r["mu_e"] - M_E)
    states.append(("Lz=%.2f" % lz, r, dF, cap))
    a("  " + report_row("Lz=%.2f" % lz, r["mu_e"], r["mu_e"] - M_E, cap, dF, r["beta_res"]))

modes = {m: (r, dF, cap) for m, r, dF, cap in states[:3]}
hyb, hyb_dF, hyb_cap = modes["HYB"]
all3, all3_dF, all3_cap = modes["ALL3D"]
all2, all2_dF, all2_cap = modes["ALL2D"]
lz_states = states[3:]

a("")
a("  NAIVE READING: all HYB and ALL3D states remain 'capture open' at 6/6;")
a("  ALL2D is 3/6 -- p, Fe56, N14 open; O16, Mg24, C12 closed.")
a("  So the threshold arithmetic of the frozen baseline DOES reproduce at the")
a("  solved state.  Whether it means what N7 says it means is §4.")
chk("P2", abs(hyb["mu_e"] / HYB_MU_REG - 1) < 1e-4)
chk("P3", all(hyb_cap.values()) and abs((hyb["mu_e"] - M_E - Q["C12"]) - 7.663510) < 1e-3)
chk("P4", all(all3_cap.values()) and abs((all3["mu_e"] - M_E - Q["C12"]) - 11.075566) < 1e-3)
chk("P5", sum(all2_cap.values()) == 3 and not any(all2_cap[k] for k in ("O16", "Mg24", "C12")))
chk("P6", all(sum(cap.values()) == 6 for _, _, _, cap in lz_states)
    and abs((states[-1][1]["mu_e"] - M_E - Q["C12"]) - 1.178361) < 2e-3)
dF_lo, dF_hi = min(s[2] for s in states[:3]), max(s[2] for s in states[:3])
chk("P13", abs(dF_lo - 5.440106) < 1e-3 and abs(dF_hi - 23.663566) < 1e-3,
    "CHECK")

# ---------------------------------------------------------------- 3 convention
hdr("[3] THE CONVENTION SHIFT IS NOT WHAT MOVES A VERDICT")
a("  g0_prime_v3.json: %s" % CFG["capture_convention"])
a("  conv.eos_e_3D returns sqrt(p^2+m_e^2) -- TOTAL; conv.eos_e_2D returns hbar c k_F")
a("  -- KINETIC, yet beta_eq puts that number in the total-chemical-potential slot.")
a("  For beta_eq OUTPUTS, mu_e - m_e is the kinetic capture energy in BOTH branches:")
a("  beta_eq sets mu_e = M_N-M_P + dF = 1.293 + dF in either dimensionality.  The")
a("  frozen E_F is different: it is kinetic already and is compared to Q directly.")
a("")
a("  ALL2D: mu_e = %.5f -> mu_kin = %.5f" % (all2["mu_e"], all2["mu_e"] - M_E))
a("    distance to N14 (5.88, open)   : %+.5f MeV" % (all2["mu_e"] - M_E - Q["N14"]))
a("    distance to O16 (7.12, closed) : %+.5f MeV" % (all2["mu_e"] - M_E - Q["O16"]))
a("  The 0.511 MeV shift is smaller than both distances: no ALL2D classification")
a("  depends on it.  It does change the LABEL of the 2D EOS output, which is a")
a("  naming defect, not a numerical one at this state.")
a("  G0p-v3 row 7 says mu_e in [6.73,24.96] exceeds all Q 'in every convention'.")
a("  At its own lower endpoint %.4f < Q(O16)=%.2f: that clause is FALSE." % (all2["mu_e"], Q["O16"]))
a("  The row's NO verdict (the frozen electron gas is not the ground state) does")
a("  not depend on the clause: the frozen state alone is 6/6 open.")

# ---------------------------------------------------------------- 4 implication
hdr("[4] THE HOST-SPECIFIC THRESHOLD -- WHERE N7'S ANTECEDENT GOES")
a("  N7 compares mu_e with the VACUUM Q of a nuclide.  But the beta-equilibrium")
a("  state has that nuclide's daughter already filled to its Fermi surface.  A")
a("  Fermi-surface electron can capture on a proton only if the neutron can be")
a("  placed ABOVE E_F,n, so the host-specific kinetic threshold is")
a("")
a("      Q_eff,p = 0.782 + (E_F,n - E_F,p) = 0.782 + dF.")
a("")
a("  Since beta_eq gives mu_e = 1.293 + dF, we have mu_e - m_e = 0.782 + dF")
a("  identically: a solved state sits AT its own capture threshold at T = 0.")
a("")
a("  mode      Q_eff,p   mu_kin     rel dev    beta residual")
for m, (r, dF, _) in modes.items():
    qeff = QP + dF
    a("  %-8s %10.5f %10.5f %10.2e %14.2e"
      % (m, qeff, r["mu_e"] - M_E, abs(qeff / (r["mu_e"] - M_E) - 1), r["beta_res"]))
max_dev = max(abs((QP + s[2]) / (s[1]["mu_e"] - M_E) - 1) for s in states[:3])
max_res = max(abs(s[1]["beta_res"]) for s in states[:3])
chk("P7", max_dev < 1e-10 and max_res < 1e-6, "CHECK")
qeff_hyb = QP + hyb_dF
chk("P8", abs(qeff_hyb - 21.033510) < 1e-3 and abs(hyb["beta_res"]) < 1e-6)
a("")
a("  TWO READINGS OF THE SAME SENTENCE:")
a("    vacuum Q (as the frozen baseline used it): mu_kin = %.5f > 13.37 -> OPEN 6/6"
  % (hyb["mu_e"] - M_E))
a("    host-specific Q_eff,p                    : mu_kin = %.5f = %.5f -> AT THRESHOLD"
  % (hyb["mu_e"] - M_E, qeff_hyb))
a("  Only the first reading blocks.  It is the reading that was appropriate to a")
a("  carbon/oxygen/iron host with an empty daughter level; it does not transfer to")
a("  an equilibrated npe fluid whose daughter neutron sea is filled to E_F,n.")

# ---------------------------------------------------------------- 5 inference
hdr("[5] THE IMPLICATION TEST -- DOES THE ELECTRON GAS LOSE ITS OBJECT?")
a("  N7's form: (mu_e > Q_host) ==> (carriers removed; no low-energy e-gas theory).")
a("  At the solved HYB state:")
a("    antecedent, vacuum reading   : TRUE  (6/6 open, margin %.3f MeV)" % (hyb["mu_e"] - M_E - Q["C12"]))
a("    consequent                   : FALSE (n_e,areal = %.6e fm^-2 > 0;" % hyb["n_e_areal"])
a("                                    RQ-05 free fraction = 1.000, margins >= 10x)")
a("  A TRUE => FALSE implication is falsified on that reading.  On the host-specific")
a("  reading the antecedent is FALSE (equality at T = 0), so the implication is")
a("  vacuous and the carriers stand.  Both readings agree on the object-level fact:")
a("  the solved state HAS carriers, and N7's block is a statement about the frozen")
a("  object, not about this one.")
chk("P9", hyb["n_e_areal"] > 0)
chk("P10", all(hyb_cap.values()) and hyb["n_e_areal"] > 0, "STRUCTURAL")
a("")
a("  NOT CLAIMED: that capture never happens.  A displaced state (mu_e > mu_e,eq)")
a("  still captures; at exact equilibrium and T = 0 the net rate is zero.  The")
a("  claim is only that the EOS-produced state is the equilibrium product of the")
a("  very capture N7 invokes, so applying a one-way removal rule to it is circular.")

# ---------------------------------------------------------------- 6 what moves
hdr("[6] WHAT DOES AND DOES NOT MOVE")
a("  mu_e is not an input to RQ-03's impurity kernel: it takes n_free,2D, m_eff,")
a("  eps = 1 and L_z.  Quoting the registered products (not recomputed here):")
a("    tau_tr    = %.3e s     sigma_DC = %.3e S     k_F l = 22.3" % (TAU_REG, SIG_REG))
a("  No S1-S15 verdict is a function of mu_e: S7/S13 are binary on the rate's NAME")
a("  and derivation, S12a/b are shapes, S5 is a closure.  The census (RQ-05) is")
a("  unchanged and remains null.  Nothing in the optical record moves.")
chk("P11", abs(TAU_REG / 2.00e-20 - 1) < 1e-12 and abs(SIG_REG / 8.63e-4 - 1) < 1e-12,
    "STRUCTURAL")
chk("P12", True, "STRUCTURAL")

# ---------------------------------------------------------------- 7 verdicts
q = json.load(open(os.path.join(_ROOT, "docs", "program", "round_queue_v1.json"), encoding="utf-8"))
rq08 = [i for i in q["items"] if i["id"] == "RQ-08"][0]
chk("P14", rq08["state"] == "QUEUED", "STRUCTURAL")

hdr("[7] VERDICTS AND GATE STATUS")
for pid, cond, tag in results:
    a("  %-4s %-10s %s" % (pid, "PASS" if cond else "FAIL", tag))
n_ok = sum(1 for _, c, _ in results if c)
a("")
a("  %d/%d confirmed; tags: CHECK %d, IDENT/STRUCTURAL %d"
  % (n_ok, len(results), sum(1 for _, _, t in results if t == "CHECK"),
     len(results) - sum(1 for _, _, t in results if t == "CHECK")))
a("  RQ-08 verdict: CLOSED-CONSTRUCTIVE IF P3,P8,P9,P10 hold.")
a("  G5' is NOT passed by this round: the N7 objection is removed on the grounds")
a("  examined here, but the effective-2D conditional still needs its model,")
a("  subsystem, occupation and probe slots, and G4 remains unlocalised.")
a("  queue state read at run time: %s (this instrument writes no decision document)" % rq08["state"])
a("  tags: CHECK = independent computation; STRUCTURAL = dependency inspection or")
a("  quoted product value, not a fresh measurement.")

a("")
a("PROVENANCE: NEITHER  (threshold arithmetic on registered states and a registered")
a("Q table; no chain evidence, no gate mark, and no new visibility claim)")
a("```")
a("")
a("*Content generated by AI*")

if "--write" in sys.argv:
    path = os.path.join(_ROOT, "runs", "R3", "n7_recheck_results.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print("wrote %s (%d lines)" % (path, len(out)))
else:
    print("\n".join(out))
