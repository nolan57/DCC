#!/usr/bin/env python3
"""
t4_floor_check.py — adjudication of the proposed R1 §4.5.1 / T4 insertion.

Registered predictions: runs/FRONT/t4_floor_registration.md (written before this file existed).

Every number here is recomputed from constants; nothing is carried over from A6 or from the submission.
Document checks read the record and count literal occurrences; they are reported as integers, not paraphrases.
"""

from __future__ import annotations

import math
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]

# ---- constants -------------------------------------------------------------------------------------
HBARC_EV_NM = 197.3269804      # eV * nm
HC_EV_NM = 1239.841984         # eV * nm
PLANCK_L_M = 1.6159e-35        # m
H_OBJ_M = 1.74                 # object height, m  (registered)
L_FACE_M = 0.18                # object face, m   (L = 0.18 -> A = 0.0324 m^2)
N_CENSUS_CELLS = 90126 ** 2    # 8.1227e9, frozen census array
N_CENSUS_PLATES = 1.18e10      # frozen census plate count
A_LATTICE_M = 1e-10            # lattice scale for the atom-count estimate

DELTA_REG_NM = 0.215           # registered single-layer thickness (Annex B)
DELTA_A6_NM = 0.4307           # submission's delta (A6 lineage)
E_QUOTED_EV = 2.9e3            # the submission's quoted number

RESULTS: list[str] = []
FLAGS: dict[str, bool] = {}


def out(line: str = "") -> None:
    RESULTS.append(line)


def table(rows: list[list[str]], head: list[str]) -> None:
    widths = [max(len(str(r[i])) for r in [head] + rows) for i in range(len(head))]
    fmt = "  ".join("{:<%d}" % w for w in widths)
    out(fmt.format(*head))
    out(fmt.format(*["-" * w for w in widths]))
    for r in rows:
        out(fmt.format(*[str(x) for x in r]))


# ===================================================================================================
out("=" * 96)
out("T4 / §4.5.1 INSERTION — ADJUDICATION RUN")
out("=" * 96)
out()

# ---- C1: the four formulas against the three candidate thicknesses ---------------------------------
out("C1 — E = (constant) / L for every plausible constant and thickness  [eV]")
Ls = [("0.215 nm (registered)", DELTA_REG_NM),
      ("0.2142 nm (H / census cells)", 1.74 / N_CENSUS_CELLS * 1e9),
      ("0.4307 nm (submission)", DELTA_A6_NM)]
rows = []
for const_name, const in [("hbarc   (what A6 writes)", HBARC_EV_NM),
                          ("hc = 2*pi*hbarc (Model C)", HC_EV_NM),
                          ("pi*hbarc (Model B, registered)", math.pi * HBARC_EV_NM)]:
    rows.append([const_name] + [f"{const / L:9.1f}" for _, L in Ls])
table(rows, ["formula \\ L"] + [n for n, _ in Ls])
out()
out(f"   quoted by the submission: {E_QUOTED_EV:.0f} eV")
out()

# ---- C2: the ratio --------------------------------------------------------------------------------
r = E_QUOTED_EV / (HBARC_EV_NM / DELTA_A6_NM)
out("C2 — is the written formula's value the quoted value?")
out(f"   hbarc / delta_A6           = {HBARC_EV_NM / DELTA_A6_NM:8.2f} eV")
out(f"   quoted / written           = {r:8.4f}")
out(f"   2*pi                       = {2 * math.pi:8.4f}      deviation {abs(r / (2 * math.pi) - 1) * 100:.2f}%")
FLAGS["P1"] = abs(HBARC_EV_NM / DELTA_A6_NM - 458.2) <= 0.5
FLAGS["P2"] = abs(r - 6.33) <= 0.02
r_reg = E_QUOTED_EV / (HBARC_EV_NM / DELTA_REG_NM)
out(f"   with the registered delta  = {HBARC_EV_NM / DELTA_REG_NM:8.2f} eV  -> quoted/written = {r_reg:.3f} (pi = {math.pi:.3f})")
out(f"   pi*hbarc / delta_reg       = {math.pi * HBARC_EV_NM / DELTA_REG_NM:8.2f} eV   <- this is the quoted number")
out()

# ---- C3: is there any delta consistent with N*delta = H that gives 2.9 keV from hbarc/delta? -------
d_need_nm = HBARC_EV_NM / E_QUOTED_EV
N_need = H_OBJ_M / (d_need_nm * 1e-9)
N_layers_census = H_OBJ_M / (DELTA_REG_NM * 1e-9)
out("C3 — solve hbarc/delta = 2.9 keV, then test it against the stripping prescription N*delta = H")
out(f"   delta required             = {d_need_nm * 1e3:8.3f} pm")
out(f"   N = H/delta                = {N_need:.3e}")
out(f"   census layer count H/delta = {N_layers_census:.3e}")
out(f"   ratio                      = {N_need / N_layers_census:8.3f}x")
out("   => the single value that makes hbarc/delta = 2.9 keV needs 3.16x the layers the census has,")
out("      so NO thickness compatible with N*delta = H yields 2.9 keV from hbarc/delta.")
FLAGS["P3"] = (abs(d_need_nm * 1e3 - 68.0) <= 0.2 and abs(N_need - 2.56e10) <= 0.02e10)
out()

# ---- C4/C5: the Planck regime ----------------------------------------------------------------
out("C4 — k_max = l_P / delta, and delta / l_P")
rows = []
for name, d in [("delta_A6 = 0.4307 nm", DELTA_A6_NM * 1e-9), ("delta_reg = 0.215 nm", DELTA_REG_NM * 1e-9)]:
    rows.append([name, f"{d / PLANCK_L_M:.3e}", f"{PLANCK_L_M / d:.3e}", "no valid integer" if PLANCK_L_M / d < 1 else "valid"])
table(rows, ["thickness", "delta / l_P", "k_max(l_P) = l_P/delta", "verdict"])
FLAGS["P4"] = (abs(PLANCK_L_M / (DELTA_A6_NM * 1e-9) - 3.75e-26) / 3.75e-26 < 0.02
               and abs(PLANCK_L_M / (DELTA_REG_NM * 1e-9) - 7.51e-26) / 7.51e-26 < 0.02
               and PLANCK_L_M / (DELTA_A6_NM * 1e-9) < 1 and PLANCK_L_M / (DELTA_REG_NM * 1e-9) < 1)
out()
out("C5 — the submission's Planck-regime arithmetic, recomputed")
A_face = L_FACE_M ** 2
V_p = PLANCK_L_M * A_face
V0 = A_face * H_OBJ_M
n_atoms = V_p / A_LATTICE_M ** 3
out(f"   A = L^2                    = {A_face:.4f} m^2")
out(f"   V = l_P * A                = {V_p:.3e} m^3      (submission: 5.2e-37)")
out(f"   V / V_0                    = {V_p / V0:.3e}      (submission: 9.3e-36)")
out(f"   n = V / a^3, a = 1e-10 m   = {n_atoms:.3e} atoms (submission: 5.2e-7)")
FLAGS["P6"] = (abs(V_p - 5.24e-37) / 5.24e-37 < 0.02
               and abs(V_p / V0 - 9.3e-36) / 9.3e-36 < 0.02
               and abs(n_atoms - 5.2e-7) / 5.2e-7 < 0.02)
decades = math.log10(DELTA_REG_NM * 1e-9 / PLANCK_L_M)
out(f"   delta_reg / l_P            = 10^{decades:.2f}   (submission: '25 orders')")
FLAGS["P5"] = abs(decades - 25) <= 0.1
out()

# ---- C6..C10: document anchors ------------------------------------------------------------------
R1 = ROOT / "docs/decisions/staged_relaxation_visual_route_v1.md"
ANNEX_A = ROOT / "docs/specs/intrinsic_structure_tiers_v1_annex_A.md"
ANNEX_B = ROOT / "docs/specs/effective_2d_definition_v1_annex_B.md"
A6 = ROOT / "docs/specs/eff_dim_claim_A6_PROPOSED.md"
MR = ROOT / "docs/decisions/matrix_reading_rules_v1.md"

r1 = R1.read_text(encoding="utf-8")


def count(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE))


out("C6 — do the two insertion anchors exist in R1?")
rows = [[f"`{pat}`", str(count(r1, pat))] for pat in [r"k_max", r"H_eff", r"4\.5\.1", r"\bT4\b", r"self-consistent point"]]
table(rows, ["pattern", "occurrences in R1"])
FLAGS["P7"] = all(int(r[1]) == 0 for r in rows)
out(f"   R1 sections: {len(re.findall(r'^## ', r1, flags=re.M))} (max numbered: "
    f"{max(int(m) for m in re.findall(r'^## (\d+)\.', r1, flags=re.M))})")
out()

sec4 = r1.split("## 4. Floor and discipline")[1].split("## 5.")[0]
nums4 = re.findall(r"\d+(?:\.\d+)?(?:e-?\d+)?", sec4)
out("C7 — is R1 §4 a quantitative section?")
out(f"   numeric constants in §4    = {len(nums4)}  {nums4}")
out(f"   length                     = {len(sec4.split())} words")
FLAGS["P8"] = len(nums4) == 0
out()

a = ANNEX_A.read_text(encoding="utf-8")
secs = re.findall(r"^## (A\.\d+)", a, flags=re.M)
out("C8 — is there an 'annex_A §A.6' to cross-reference?")
out(f"   Annex A sections           = {secs}")
FLAGS["P9"] = "A.6" not in secs
b = ANNEX_B.read_text(encoding="utf-8")
out(f"   Annex B sections           = {re.findall(r'^## (B\.\d+)', b, flags=re.M)}")
out()

# Insertion A / B text, as registered
INS_A = (ROOT / "runs/FRONT/t4_submission_verbatim.md")
text_a = INS_A.read_text(encoding="utf-8") if INS_A.exists() else ""
ins_a_block = text_a.split("<!-- BEGIN-INSERTION-A -->")[1].split("<!-- END-INSERTION-A -->")[0] if "BEGIN-INSERTION-A" in text_a else ""
ins_b_block = text_a.split("<!-- BEGIN-INSERTION-B -->")[1].split("<!-- END-INSERTION-B -->")[0] if "BEGIN-INSERTION-B" in text_a else ""

out("C9 — does Insertion A name which bound its single number belongs to?")
if ins_a_block:
    rows = [[f"`{p}`", str(count(ins_a_block, p))] for p in ["external", "internal", r"Model B", "subsystem"]]
    table(rows, ["required token", "occurrences"])
    FLAGS["P10"] = all(int(r[1]) == 0 for r in rows)
else:
    out("   (Insertion A block not yet registered — see §1 of the ruling)")
    FLAGS["P10"] = None
out()

out("C10 — does Insertion B supply the three admission requirements?")
req = [
    ("(a) formal definition referencing only the scene", ["definition", "define", r"\bD\(s\)|statistic|score|quantity"]),
    ("(b) a quantity between unstructured and structured", ["unstructured", "structured", "between", "scale", "range"]),
    ("(c) threshold declared and hash-locked before the run", ["threshold", "lock", "pre-registered", "pre-register"]),
]
if ins_b_block:
    rows = []
    supplied = 0
    for name, toks in req:
        n = sum(count(ins_b_block, t) for t in toks)
        hit = n > 0
        supplied += int(hit)
        rows.append([name, str(n), "supplied" if hit else "absent"])
    table(rows, ["requirement", "token hits", "status"])
    out(f"   supplied: {supplied} of 3")
    FLAGS["P11"] = supplied == 0
else:
    out("   (Insertion B block not yet registered — see §1 of the ruling)")
    FLAGS["P11"] = None
out()

out("C11 — symbol: what does `k` already mean in the record?")
kB = re.findall(r"`k`[^\n]{0,160}", b)
out(f"   Annex B, {len(kB)} statement(s) about `k`:")
for line in kB[:4]:
    out(f"     - {line.strip()[:150]}")
FLAGS["P12"] = any("1.4527" in line for line in kB)
out()

out("C12 — does the mechanism contain a stacking step?")
docs = [ROOT / "docs/decisions/front_sweep_v1.md", ROOT / "docs/decisions/mid_sweep_frame_v1.md", ANNEX_B, A6]
tot = 0
for d in docs:
    if not d.exists():
        continue
    t = d.read_text(encoding="utf-8")
    hits = count(t, r"\bstack|stacked|stacking|on top of|superposed|one per site")
    out(f"   {d.name:<44} {hits}")
    tot += hits
out(f"   total stacking vocabulary in mechanism/annex documents = {tot}")
FLAGS["P13"] = tot == 0
out()

out("C13 — is `T4` already in force under another meaning?")
mr = MR.read_text(encoding="utf-8")
out(f"   `matrix_reading_rules_v1.md` cites ruling T4: {'T4' in mr}")
out(f"   `MR1` present: {'MR1' in mr}")
FLAGS["P14"] = ("T4" in mr) and ("MR1" in mr)
out()

# ---- ledger ---------------------------------------------------------------------------------------
out("=" * 96)
out("PREDICTION LEDGER")
out("=" * 96)
names = {
    "P1": "hbarc/delta_A6 = 458.2 eV (the printed equality is false)",
    "P2": "quoted/written = 6.33 ~ 2*pi",
    "P3": "no delta with N*delta = H gives 2.9 keV from hbarc/delta",
    "P4": "k_max(l_P) = 3.75e-26 and 7.51e-26, both < 1",
    "P5": "delta/l_P = 1e25",
    "P6": "Planck-regime arithmetic is correct (credit to the submission)",
    "P7": "R1 contains no anchor (k_max / H_eff / 4.5.1 / T4 = 0)",
    "P8": "R1 section 4 has zero numeric constants",
    "P9": "Annex A has no section A.6",
    "P10": "Insertion A names no bound (external/internal/Model B = 0)",
    "P11": "Insertion B supplies 0 of 3 admission requirements",
    "P12": "k already means plates-per-cell = 1.4527",
    "P13": "zero stacking vocabulary in the mechanism",
    "P14": "T4 already in force as MR1",
}
passed = failed = pending = 0
rows = []
for k, v in FLAGS.items():
    if v is None:
        status = "PENDING"
        pending += 1
    elif v:
        status = "PASS"
        passed += 1
    else:
        status = "FAIL"
        failed += 1
    rows.append([k, status, names[k]])
table(rows, ["#", "result", "prediction"])
out()
out(f"   passed {passed} / failed {failed} / pending {pending}  (of {len(FLAGS)})")
out()
if pending:
    out("   PENDING means the verbatim insertion text had not been registered when this ran; re-run after §1 of")
    out("   the ruling exists. A pending check is not a pass.")
    out()

# ---- disposition, derived from the flags -------------------------------------------------------
out("=" * 96)
out("DISPOSITION (derived from the flags above, not written in advance)")
out("=" * 96)
blockers = []
if FLAGS.get("P7"):
    blockers.append("B1  both insertion anchors are absent from R1 (P7) — there is no §4.5 and no §7 tier list")
if FLAGS.get("P14"):
    blockers.append("B2  T4 is already in force as MR1 with a different meaning (P14) — one label, two objects")
if FLAGS.get("P11"):
    blockers.append("B3  Insertion B supplies 0 of 3 admission requirements (P11) — it cannot enter as a tier")
if FLAGS.get("P1") and FLAGS.get("P2"):
    blockers.append("B4  the printed equality hbarc/delta = 2.9 keV is false by 6.33x = 2*pi (P1, P2)")
if FLAGS.get("P10"):
    blockers.append("B5  Insertion A names no bound, repeating the §3 prohibition (P10)")
if FLAGS.get("P12"):
    blockers.append("B6  `k` is already 1.4527 plates-per-cell; the submission's k = 1 is a collision (P12)")
for bl in blockers:
    out("   " + bl)
out()
if not blockers:
    out("   no blockers — the insertion may proceed")
else:
    out(f"   => {len(blockers)} independent blockers. The insertion cannot be applied as written.")
out()
out("   What survives and is NOT a blocker:")
if FLAGS.get("P4") and FLAGS.get("P6"):
    out("   S1  k_max(l_P) < 1 is correct and is a *derivation* that l_P is outside the model's image —")
    out("       stronger than the previous '25 orders of magnitude away' remark (P4, P6)")
if FLAGS.get("P5"):
    out("   S2  the 25-decade separation is confirmed (P5)")
out()
out("   The correct sentence, which no blocker touches:")
out('   "H_eff takes the value delta and no other: delta = H/N is fixed by the stripping, and a')
out('    configuration thinner than one atomic layer has no solution. l_P is 25 decades below delta,')
out('    so it is not a thickness this model fails to reach; it is a thickness this model cannot denote."')
out()
out("=" * 96)
out("PROVENANCE: NEITHER  (adjudication of a submitted claim against the registered record; establishes no physics)")
ou()

text = "\n".join(RESULTS)
print(text)
(ROOT / "runs/FRONT/t4_floor_results.txt").write_text(text + "\n", encoding="utf-8")
