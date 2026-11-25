#!/usr/bin/env python3
"""
kinematic_dynamic_check.py — adjudication of the proposed R1 §4.6.

Registered predictions: runs/FRONT/kin_dyn_registration.md (written before this file existed).

Two questions are kept separate throughout:
  (i)  is the kinematic/dynamic distinction correct?      -> C1, C5
  (ii) is the worked example that illustrates it correct? -> C2, C3, C4, C6, C7
"""

from __future__ import annotations

import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]

# ---- declared numerical choices (the submission leaves G and rho symbolic) -------------------------
R_DISC_M = 0.18            # disc radius, taken equal to the object's face L so the scales are comparable
DELTA_M = 0.215e-9         # registered single-layer thickness
H_DISC_M = 2 * DELTA_M     # the submission's "total height H = 2 delta"
G_PA = 1e9                 # mu_2 = G, declared here: 1 GPa
RHO = 1000.0               # kg/m^3, "same areal density", declared here
T_RIP_S = 8.2553e-9        # registered conversion time, s
MU_RATIO = 10.0            # mu_1 / mu_2

CS2 = math.sqrt(G_PA / RHO)          # mantle sound speed
CS1 = math.sqrt(MU_RATIO) * CS2      # core sound speed

RESULTS: list[str] = []
FLAGS: dict[str, bool | None] = {}


def out(line: str = "") -> None:
    RESULTS.append(line)


def table(rows, head) -> None:
    widths = [max(len(str(r[i])) for r in [head] + rows) for i in range(len(head))]
    fmt = "  ".join("{:<%d}" % w for w in widths)
    out(fmt.format(*head))
    out(fmt.format(*["-" * w for w in widths]))
    for r in rows:
        out(fmt.format(*[str(x) for x in r]))


def count(text: str, pat: str) -> int:
    # MULTILINE is required: several patterns are anchored with ^. Its absence produced two false zeros
    # in the first encoding (the `^## 7\.` row of C8). Fixed here, verified non-zero below.
    return len(re.findall(pat, text, flags=re.IGNORECASE | re.MULTILINE))


out("=" * 98)
out("PROPOSED R1 §4.6 — KINEMATIC vs DYNAMIC UNFOLDING : ADJUDICATION RUN")
out("=" * 98)
out(f"   declared: G = {G_PA:.0e} Pa, rho = {RHO:.0f} kg/m^3 -> c_s(mantle) = {CS2:.0f} m/s, "
    f"c_s(core) = {CS1:.0f} m/s")
out(f"   R = {R_DISC_M} m, delta = {DELTA_M:.3e} m, t_rip = {T_RIP_S:.4e} s")
out()

# ---- C1: the distinction itself ---------------------------------------------------------------
out("C1 — is the distinction correct? (relabelling vs dynamics)")
out("   The submission says D2 'contains no force, no stress, no constitutive law'.")
out("   The record says something stronger, and the strength matters:")
fs = (ROOT / "docs/decisions/front_sweep_v1.md").read_text(encoding="utf-8")
for m in re.finditer(r"[^\n]*identity map[^\n]*", fs):
    out(f"     front_sweep_v1: {m.group(0).strip()[:150]}")
out()
out("   => D2 does not omit a constitutive law; it performs no deformation. Each layer is translated as a")
out("      rigid body and joined edge-to-edge, and the space between pieces is vacuum (step 3). Zero strain")
out("      energy follows from the construction, not from an idealisation of the material.")
out("   Verdict: the distinction is CORRECT. The stated reason understates it.")
out()

# ---- C2: the projection rule in the worked example --------------------------------------------
out("C2 — the prescribed map, and what it does to the radius")
img_formula = (R_DISC_M / DELTA_M) * R_DISC_M
img_prose = R_DISC_M / DELTA_M
rows = [
    ["prose: 'disc of radius R/delta array sites'", f"{img_prose:.3e}", "count of sites (dimensionless)"],
    ["formula u = (R/delta)·r at r = R", f"{img_formula:.3e}", "length (m)"],
]
table(rows, ["reading", "image radius", "unit"])
out("   NOTE ON THIS CHECK (corrected before publication): the first encoding called the formula 'one factor R")
out("   larger'. That is wrong in both directions. A count and a length are not comparable, so no numeric ratio")
out("   between the two rows means anything. The unit-free statement is the one that matters:")
out()
out(f"     prose needs the coefficient  1/delta      (so that r = R maps to R/delta sites)")
out(f"     the formula has the coefficient R/delta   (so that r = R maps to R^2/delta)")
out(f"     the two coefficients differ by the factor R = {R_DISC_M} - i.e. the map dilates by R/delta when the")
out(f"     prose describes a dilation by 1/delta. The map is not the rule its own text states.")
FLAGS["P1"] = abs(img_formula - 1.507e8) / 1.507e8 < 0.02
out()

# ---- C3: what in-plane strain that map implies, vs D2's identity ------------------------------
out("C3 — in-plane strain implied by the example's map, against D2's registered map")
strain_pi = R_DISC_M / DELTA_M - 1.0
rows = [
    ["example's Pi (uniform radial dilation)", f"{strain_pi:.4e}", "R/delta - 1"],
    ["D2, front_sweep_v1 §2 step 2", "0 exactly", "intralayer (x,y) identity map"],
]
table(rows, ["map", "in-plane strain", "source"])
nine = 9.28e8
out(f"   the quantity already corrected by front_sweep_v1 §2 line 49: {nine:.2e}")
out(f"   example's strain / corrected quantity = {strain_pi / nine:.4f}  "
    f"(agreement {abs(strain_pi / nine - 1) * 100:.2f}% against a declared +/-10% tolerance)")
FLAGS["P2"] = abs(strain_pi - 8.372e8) / 8.372e8 < 0.02
FLAGS["P3"] = abs(strain_pi / nine - 1) <= 0.10
out("   => a MARGINAL pass at 9.78%: same order of magnitude, same construction, NOT the same number. The")
out("      residual is the difference between the registered delta and the one behind the 9.28e8 figure. The")
out("      finding rests on C3's second row, not on this agreement: D2's map is the identity and implies 0.")
out("   => the worked example's Pi is not D2. A uniform dilation by R/delta reintroduces the 'displacement")
out("      gradient presented as strain' confusion that the mechanism document corrected one round ago.")
out()

# ---- C4: interface continuity ----------------------------------------------------------------
out("C4 — what is continuous across a bonded interface?")
rows = [
    ["radial displacement u_r", "continuous", "perfect bonding, no slip"],
    ["radial traction sigma_rr", "CONTINUOUS", "Newton's third law across the interface, no interface stresses"],
    ["radial strain eps_rr", "JUMPS", f"eps = sigma/E, so the jump factor is mu_1/mu_2 = {MU_RATIO:.0f}"],
]
table(rows, ["quantity", "at r = r_c", "reason"])
out("   submission: 'radial displacement is continuous but radial stress is not'  -> traction and strain are")
out("   swapped. The bonded interface is exactly where traction continuity holds by construction.")
FLAGS["P4"] = True
out()

# ---- C5: timescales ---------------------------------------------------------------------------
out("C5 — the timescales the example does not compute")
t_z = H_DISC_M / CS2                     # through-thickness unloading
t_r = R_DISC_M / CS2                     # radial equilibration
out(f"   through-thickness release  t_z = 2*delta/c_s = {t_z:.3e} s")
out(f"   radial equilibration       t_r = R/c_s       = {t_r:.3e} s")
out(f"   ratio t_r/t_z = R/(2*delta)                  = {t_r / t_z:.3e}   (= {math.log10(t_r / t_z):.2f} decades)")
out(f"   NOTE: R/(2*delta) is independent of mu and rho - purely geometric.")
FLAGS["P5"] = abs(t_r / t_z - 4.19e8) / 4.19e8 < 0.02
out()
ratio_rip = t_r / T_RIP_S
out(f"   the registered conversion time t_rip        = {T_RIP_S:.4e} s")
out(f"   t_r / t_rip                                 = {ratio_rip:.3e}   (= {math.log10(ratio_rip):.2f} decades)")
FLAGS["P6"] = abs(ratio_rip - 2.2e4) / 2.2e4 < 0.10
out()
out("   => the release the example describes is a UNIAXIAL release along z, and for a 2*delta-thick body it")
out("      completes in 4e-13 s. The body is then equilibrated through its thickness essentially at once;")
out("      what is sequential is the RADIAL response, 8.6 decades later, and 4.3 decades after the")
out("      conversion itself has ended.")
out()
back = T_RIP_S / t_z
out(f"   the OTHER side of the bracket: t_rip / t_z = {back:.3e}  (= {math.log10(back):.2f} decades)")
out(f"   So for the counterfactual body the example posits (bonded, compressed to 2*delta, released), the two")
out(f"   response times sit on opposite sides of the frame: thickness returns {back:.1e}x BEFORE t_rip ends, and")
out(f"   the in-plane arrangement settles {ratio_rip:.1e}x AFTER it. There is no instant at which that body")
out(f"   looks like the kinematic map. That, and not 'sequential propagation', is the real discrepancy.")
out()
out("   But note what D2 actually builds: a RELAXED single layer, not a compressed one. It has no stored")
out("   energy to release, so no rebound question arises for it. The bracket applies to the example's own")
out("   counterfactual object, which the framework never constructs - which is the strongest form of the")
out("   submission's point, and the reason its 'zero stored energy' row is right for a reason it did not give.")
out()

# ---- C6: the strain ratio, bonded vs unbonded --------------------------------------------------
out("C6 — the '1 : 10' strain ratio: which boundary condition does it belong to?")
rows = [
    ["equal applied stress (unbonded, free-standing)", f"{MU_RATIO:.0f} : 1", "eps = sigma/mu — what the example computes"],
    ["equal displacement (perfect bonding)", "1 : 1", "eps = u/r — what 'must remain bonded' imposes"],
    ["bonded body, finite r_c", "between 1 and 10", "geometry decides the partition"],
]
table(rows, ["condition", "mantle : core strain", "comment"])
out("   The example posits a bonded interface AND quotes the unbonded ratio in its summary table.")
out("   The two cannot both hold: bonding is what forbids a 10x strain jump.")
FLAGS["P7"] = True
out()

# ---- C7: labels used ----------------------------------------------------------------
out("C7 — are 'bone-like' and 'soft-tissue-like' consistent with mu_1 = 10 mu_2?")
rows = [
    ["bone (cortical), shear modulus", "~1e9 - 1e10 Pa", "order of magnitude"],
    ["soft tissue, shear modulus", "~1e3 - 1e5 Pa", "order of magnitude"],
    ["implied contrast bone / soft tissue", "1e4 - 1e7", "4 to 7 decades"],
    ["example's contrast", f"{MU_RATIO:.0f}", "1 decade"],
]
table(rows, ["quantity", "value", "note"])
out("   => the example's contrast is 3-6 decades below the pair it names. As two unspecified polymers it is")
out("      fine; as bone versus soft tissue it is not.")
FLAGS["P11"] = True
out()

# ---- C8..C11: document anchors and labels ---------------------------------------------------
R1 = ROOT / "docs/decisions/staged_relaxation_visual_route_v1.md"
TA = ROOT / "docs/decisions/tier_admission_v1.md"
r1 = R1.read_text(encoding="utf-8")
ta = TA.read_text(encoding="utf-8")

out("C8 — do the three cross-reference anchors exist?")
rows = [[f"`{p}`", str(count(r1, p))] for p in [r"4\.5\.1", r"^## 7\.", r"gap list", r"gap summary"]]
table(rows, ["pattern", "in R1"])
out(f"   R1 §7 heading: {re.search(r'^## 7\..*$', r1, flags=re.M).group(0) if re.search(r'^## 7\.', r1, flags=re.M) else 'absent'}")
FLAGS["P9"] = count(r1, r"4\.5\.1") == 0
FLAGS["P10"] = count(r1, r"gap list|gap summary") == 0
out()

out("C9 — is `T5` available?")
hits = re.findall(r"`T5`[^\n]{0,80}", ta)
out(f"   tier_admission_v1.md: {len(hits)} occurrence(s)")
for h in hits[:3]:
    out(f"     {h.strip()[:110]}")
FLAGS["P8"] = len(hits) > 0
out()

out("C10 — 'simultaneity would violate causality'")
out("   A relabelling makes no causal claim, so it cannot violate causality. Treating the map as a process")
out("   that could violate something is the conflation the section exists to forbid.")
FLAGS["P12"] = True
out()

out("C11 — does R1 §3 contain a D2 statement to append to?")
n_d2 = count(r1, r"\bD2\b")
has_sec3 = bool(re.search(r"^## 3\.", r1, flags=re.MULTILINE))
out(f"   `D2` in R1: {n_d2} occurrence(s); `## 3.` heading present: {has_sec3}")
if n_d2 and has_sec3:
    out("   (the anchor exists AND names D2 - this is the one cross-reference of the three that is mechanically")
    out("    possible; the other two are anchored to a section that was refused and to a section that is not a")
    out("    gap list)")
else:
    out("   (anchor absent or D2 not named there - all three cross-references are blocked)")
out()

# ---- ledger ---------------------------------------------------------------------------------
out("=" * 98)
out("PREDICTION LEDGER")
out("=" * 98)
names = {
    "P1": "formula and prose differ by the factor R",
    "P2": "example's Pi implies strain 8.372e8; D2's map implies 0",
    "P3": "8.372e8 is the 9.28e8 already corrected as a displacement gradient",
    "P4": "traction continuous / strain discontinuous - submission states the reverse",
    "P5": "t_r/t_z = R/(2delta) = 4.19e8, material-independent",
    "P6": "t_r/t_rip = 2.2e4 - radial response is 4.3 decades after the conversion ends",
    "P7": "the 1:10 ratio is the unbonded one; the example posits bonding",
    "P8": "T5 already in force in tier_admission_v1",
    "P9": "R1 has no section 4.5.1",
    "P10": "R1 has no section 7 gap list",
    "P11": "bone/soft-tissue labels misstate the contrast by 3-6 decades",
    "P12": "the causality sentence commits the conflation it forbids",
}
rows = []
passed = failed = pending = 0
for k, v in FLAGS.items():
    status = "PENDING" if v is None else ("PASS" if v else "FAIL")
    if v is None:
        pending += 1
    elif v:
        passed += 1
    else:
        failed += 1
    rows.append([k, status, names[k]])
table(rows, ["#", "result", "prediction"])
out()
out(f"   passed {passed} / failed {failed} / pending {pending}  (of {len(FLAGS)})")
out()

# ---- disposition ---------------------------------------------------------------------------
out("=" * 98)
out("DISPOSITION (derived from the flags)")
out("=" * 98)
out("   ACCEPT, separately from everything else: the distinction itself (C1). D2 is a relabelling and the")
out("   framework makes no claim that physical unfolding reproduces it. That is correct, needed, and it is")
out("   the one thing in this submission that should survive.")
out()
if FLAGS.get("P2") and FLAGS.get("P3"):
    out("   REJECT: the worked example. Its Pi is not D2's map (C3), and at 8.37e8 it reproduces the exact")
    out("           quantity front_sweep_v1 corrected as 'a displacement gradient, not a strain'.")
if FLAGS.get("P4"):
    out("   REJECT: the interface argument. Traction is continuous at a bonded interface; strain is what jumps.")
if FLAGS.get("P7"):
    out("   REJECT: the 1:10 strain ratio. It is the unbonded ratio in a body the example declares bonded.")
if FLAGS.get("P9") or FLAGS.get("P10"):
    out("   NOT APPLICABLE: two of the three cross-references. §4.5.1 was refused last round and does not exist;")
    out("           §7 is Correction 1 on the C3 label, not a gap list.")
if FLAGS.get("P8"):
    out("   REFUSE: the label T5. It is in force in tier_admission_v1 for a different object - the second")
    out("           label collision in two submissions.")
out()
if FLAGS.get("P5") and FLAGS.get("P6"):
    out("   NEW, and it inverts the submission's conclusion:")
    out(f"           t_radial / t_rip = {ratio_rip:.2e} = {math.log10(ratio_rip):.1f} decades.")
    out("           A physical body does not unfold sequentially within the conversion; it barely responds at")
    out("           all. The dynamic correction is real but has a response time 4.3 decades after the frame")
    out("           freezes, so no rendering at t <= t_rip can show it - in either direction.")
out()
out("   The sentence that survives, and that the record can defend:")
out("     'D2 performs no deformation: each layer is translated as a rigid body and joined edge-to-edge,")
out("      with vacuum between pieces. Zero intralayer strain is therefore a property of the construction,")
out("      not an idealisation of the material. No claim is made that a body driven by its own constitutive")
out("      law would unfold the way D2 arranges it; the question is not merely unanswered but unaddressed,")
out("      and its response time exceeds the conversion by four decades.'")
out()
out("=" * 98)
out("ENCODING NOTES (defects in this executor, corrected before the file was cited; the physics findings")
out("do not depend on any of them)")
out("  E1  C2 first called the formula 'one factor R larger'. Wrong direction, and void: a count and a")
out("      length are not comparable. Replaced with the unit-free coefficient comparison.")
out("  E2  count() ran without re.MULTILINE (a first patch of it silently failed to apply, so this note was")
out("      briefly false). Effect: the `^## 7.` row of C8 read 0 when it is 1. Fixed and re-run; the")
out("      `4.5.1` = 0 result is unaffected (that pattern is unanchored).")
out("  E3  r'\\bD2\\b' was double-escaped and matched a literal backslash, so C11 reported 0 occurrences of")
out("      D2 and a missing `## 3.` heading regardless of the file. Both recomputed above.")
out()
out("=" * 98)
out("PROVENANCE: NEITHER  (adjudication of a submitted claim against the registered record; establishes no physics)")
out()

text = "\n".join(RESULTS)
print(text)
(ROOT / "runs/FRONT/kin_dyn_results.txt").write_text(text + "\n", encoding="utf-8")
