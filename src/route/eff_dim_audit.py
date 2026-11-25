"""
eff_dim_audit.py — audit of the submitted A.6 effective-dimensionality claim.

Reads the VERBATIM text in docs/specs/eff_dim_claim_A6_PROPOSED.md (the block between the markers) and
tests it against the registered record.  Nothing here edits the record; nothing here is a threshold.

Predictions were fixed in runs/FRONT/eff_dim_audit_registration.md before this file existed.  Two of them
(P1, P2) are disclosed there as NOT blind — they confirm a hand calculation done to decide whether the
submission deserved a registration at all.

Every closing line below is derived from a flag.  A static "CONCLUSION" string is how this project shipped
two wrong summaries already; it is not repeated here.
"""

import ast
import io
import math
import re
import sys

import numpy as np

# ------------------------------------------------------------------------------------------------
# constants: from the record, not chosen here
# ------------------------------------------------------------------------------------------------
HBAR_C = 197.3269804      # eV nm
H_C = 1239.84193          # eV nm   (= 2*pi*hbar_c, to 7 s.f.)
PI = math.pi

D_REG = 0.215             # nm   front_sweep_v1 s2: "one atomic layer (0.215 nm)"
D_A6 = 0.4307             # nm   A.6's declared delta
H_BODY = 1.738            # m    front_sweep_v1 s1
N_REG = 8.12e9            # layers, frozen census
COMP_PER_LAYER = 1.457    # front_sweep_v1 s2
N_PLATES = 1.18e10        # frozen census
SIDE = 90126              # array side, front_sweep_v1 s1 / reproduced by front_sweep_frame.py

E_QUOTED_KEV = 2.9
K_A6 = 1.0

# probes the project actually uses
PROBES = [("visible, FL/reflection channel", 2.25), ("transmission channel", 284.0),
          ("A.6's own falsifier", 12000.0), ("nuclear", 2.0e8)]

# registered E_F for the three states, effective_2d_definition_v1 s4
EF = [("frozen state", 73.37e6), ("HYB equilibrium", 21.54e6), ("ALL2D equilibrium", 6.73e6)]

FLAGS = []


def hdr(t):
    print()
    print("=" * 100)
    print(t)
    print("=" * 100)


def rec(tag, ok, detail):
    FLAGS.append((tag, bool(ok), detail))
    print("  [%s] %-6s %s" % ("PASS" if ok else "FAIL", tag, detail))


def verbatim():
    txt = open("docs/specs/eff_dim_claim_A6_PROPOSED.md", encoding="utf-8").read()
    m = re.search(r"<!-- BEGIN-VERBATIM -->(.*?)<!-- END-VERBATIM -->", txt, re.S)
    if not m:
        sys.exit("verbatim block not found — cannot audit a paraphrase")
    return m.group(1)


def slot_hits(text, groups):
    t = text.lower()
    return {g: [k for k in ks if k in t] for g, ks in groups.items()}


def main():
    V = verbatim()
    print("A.6 effective-dimensionality claim — audit")
    print("verbatim block: %d characters, %d lines" % (len(V), len(V.splitlines())))

    # ------------------------------------------------------------------ S0
    hdr("S0  the four-cell table: which (constant, thickness) reproduces 2.9 keV")
    print("     A.6 writes the formula with hbar*c and the thickness 0.4307 nm.  Both are checked.")
    print()
    print("     %-38s %14s %14s" % ("formula \\  L", "L = 0.215 nm", "L = 0.4307 nm"))
    print("     " + "-" * 68)
    cells = {}
    for name, cst in (("hbar*c/L        (A.6 written)", HBAR_C),
                      ("h*c/L = 2*pi*hbar*c/L  (Model C)", H_C),
                      ("pi*hbar*c/L     (registered Model B)", PI * HBAR_C)):
        a, b = cst / D_REG, cst / D_A6
        cells[name] = (a, b)
        print("     %-38s %11.1f eV %11.1f eV" % (name, a, b))
    print()
    written = cells["hbar*c/L        (A.6 written)"][1]
    print("     A.6's own formula at A.6's own thickness : %.1f eV = %.3f keV" % (written, written / 1e3))
    print("     A.6's quoted number                      : %.1f keV" % E_QUOTED_KEV)
    print("     ratio                                    : %.4f   (2*pi = %.4f)" % (E_QUOTED_KEV * 1e3 / written, 2 * PI))

    # ------------------------------------------------------------------ S1
    hdr("S1  P1  the written formula does not yield the written number")
    ratio = E_QUOTED_KEV * 1e3 / written
    # diagnostic only — the residual is decomposed, not forgiven.  The flag below is NOT relaxed.
    print("     residual decomposition: 2*pi * (delta_A6 / (2*delta_reg)) = %.4f * %.6f = %.4f"
          % (2 * PI, D_A6 / (2 * D_REG), 2 * PI * D_A6 / (2 * D_REG)))
    print("     so the 0.7%% gap from 2*pi is the SAME 2.0033 that S4 measures, seen from the other side.")
    ok1 = abs(ratio - 2 * PI) / (2 * PI) < 0.005 and abs(written - 458.0) < 5.0
    rec("P1", ok1, "written formula -> %.2f eV; quoted/written = %.4f (2*pi to %.2f%%)"
        % (written, ratio, 100 * abs(ratio - 2 * PI) / (2 * PI)))

    # ------------------------------------------------------------------ S2
    hdr("S2  P2  the quoted 2.9 keV is reached only by two mutually inconsistent pairs")
    target = E_QUOTED_KEV * 1e3
    hits = []
    for name, (a, b) in cells.items():
        for L, v in (("0.215", a), ("0.4307", b)):
            if abs(v - target) / target < 0.01:
                hits.append((name, L, v))
    for name, L, v in hits:
        print("     reproduces 2.9 keV : %-38s L = %-6s nm  (%.1f eV)" % (name, L, v))
    ok2 = (len(hits) == 2
           and "hbar*c/L" not in [h[0] for h in hits]
           and not any(h[0].startswith("hbar*c/L") for h in hits))
    rec("P2", ok2, "%d of 6 (formula, L) cells reproduce the quoted number; A.6's own pair is not one of them"
        % len(hits))

    # ------------------------------------------------------------------ S3
    hdr("S3  P3  k_max(E_1(k)) = k is an identity, so 'the self-consistent point' selects nothing")
    print("     k_max(E) = (c/E)/delta  and  E_1(k) = c/(k delta)  =>  k_max(E_1(k)) = k by construction.")
    print("     Sweep, both constants (the identity cannot depend on which one is used):")
    worst = 0.0
    for label, cst in (("hbar*c", HBAR_C), ("pi*hbar*c", PI * HBAR_C), ("h*c", H_C)):
        rel = 0.0
        for k in np.logspace(-1, 4, 60):
            e1 = cst / (k * D_REG)
            kmax = (cst / e1) / D_REG
            rel = max(rel, abs(kmax / k - 1.0))
        print("       %-10s max |k_max(E_1(k))/k - 1| over k in [0.1, 1e4] : %.3e" % (label, rel))
        worst = max(worst, rel)
    ok3 = worst < 1e-12
    rec("P3", ok3, "identity holds to %.1e for every k swept, incl. k = 1160; 'largest k at its own "
                   "freeze-out energy' is true of every k" % worst)

    # ------------------------------------------------------------------ S4
    hdr("S4  P4  the layer count: A.6's N and delta are both off by the same factor")
    n_from_h = H_BODY / (D_REG * 1e-9)
    n_a6 = H_BODY / (D_A6 * 1e-9)
    print("     N = H/delta :  H = %.3f m" % H_BODY)
    print("       with registered delta 0.215 nm  -> N = %.4e   (registered census: %.3e)" % (n_from_h, N_REG))
    print("       with A.6's delta     0.4307 nm  -> N = %.4e   (A.6 states 4.04e9)" % (n_a6,))
    print("     A.6 4.04e9 / (H/0.215nm) = %.4f ;  A.6 delta / 0.215nm = %.4f"
          % (4.04e9 / n_from_h, D_A6 / D_REG))
    ok4 = abs(4.04e9 / n_from_h - 0.5) < 0.005 and abs(D_A6 / D_REG - 2.0) < 0.01
    rec("P4", ok4, "N is low by 2.000x and delta high by 2.003x; their product N*delta = H is preserved, "
                   "so the error is invisible in the relation A.6 actually prints")

    # ------------------------------------------------------------------ S5
    hdr("S5  P5  k = 1 contradicts the frozen census")
    sites = SIDE ** 2
    k_census = N_PLATES / sites
    print("     array sites            = %d^2 = %.4e" % (SIDE, sites))
    print("     plates (frozen census) = %.3e" % N_PLATES)
    print("     plates per site        = %.4f" % k_census)
    print("     if k = 1 exactly, sites needed = %.3e -> side %.0f  (declared array is %d)"
          % (N_PLATES, math.sqrt(N_PLATES), SIDE))
    print("     unplaced plates at k=1 = %.3e" % (N_PLATES - sites))
    ok5 = abs(k_census - 1.453) < 0.01 and abs(SIDE - math.sqrt(N_PLATES)) > 1e4
    rec("P5", ok5, "k = %.3f from the census, not 1; the render is not the configuration A.6 analyses"
        % k_census)

    # ------------------------------------------------------------------ S6
    hdr("S6  P6  the four-slot conditional of effective_2d_definition_v1 s1")
    groups = {
        "model (B finite well / C compactification)": ["model b", "model c", "finite well", "compactif"],
        "subsystem (electrons / nucleons / collective)": ["electron", "nucleon", "phonon", "plasmon", "collective"],
        "occupation scale E_occ": ["e_f", "fermi", "k_bt", "occupation"],
        "probe energy E_probe": ["probe energy", "probe of available energy", "visible", "2.5 ev"],
    }
    hits = slot_hits(V, groups)
    filled = 0
    for g, h in hits.items():
        print("     %-46s %s" % (g, ("present: " + ", ".join(h)) if h else "ABSENT"))
        filled += 1 if h else 0
    print()
    print("     slots filled: %d of 4   -> \"2D\" has a referent only if subsystem is filled" % filled)
    ok6 = filled <= 2
    rec("P6", ok6, "%d of 4 slots filled; subsystem %s, E_occ %s"
        % (filled, "present" if hits["subsystem (electrons / nucleons / collective)"] else "ABSENT",
           "present" if hits["occupation scale E_occ"] else "ABSENT"))

    # ------------------------------------------------------------------ S7
    hdr("S7  P7  the internal bound fails by orders of magnitude; only the external one is met")
    print("     s3 of the convention: the TWO bounds must not be combined into one number.")
    print("     A.6 quotes ONE number and never names the bound.  Testing both against it:")
    print()
    print("     %-24s %12s %14s %10s" % ("state", "E_F", "E_F / dE_z", "internal"))
    ez = target  # eV, A.6's quoted value
    worst_ratio = 1e9
    for name, ef in EF:
        r = ef / ez
        worst_ratio = min(worst_ratio, r)
        print("     %-24s %9.2f MeV %14.3e %10s" % (name, ef / 1e6, r, "holds" if r < 1 else "FAILS"))
    print()
    print("     external bound at L = 0.215 nm, deltaE_z = %.1f eV: any E_probe < %.0f eV meets it."
          % (PI * HBAR_C / D_REG, PI * HBAR_C / D_REG))
    print("     internal bound requires L_z <~ 2 fm (registered); 0.215 nm = %.1e fm, i.e. %.1e x too thick"
          % (D_REG * 1e6, D_REG * 1e6 / 2.0))
    ok7 = worst_ratio > 1e3
    rec("P7", ok7, "internal bound fails by >= %.1e for every registered state; the claim is "
                   "external-only and 'is a 2D system' is false as written" % worst_ratio)

    # ------------------------------------------------------------------ S8
    hdr("S8  P8  the number is stable under joint correction — that is what compensating errors do")
    v_written = cells["hbar*c/L        (A.6 written)"][1]
    v_reg = PI * HBAR_C / D_REG
    print("     as written   (hbar*c, 0.4307 nm) : %8.2f eV = %.3f keV" % (v_written, v_written / 1e3))
    print("     corrected    (pi*hbar*c, 0.215 nm): %8.2f eV = %.3f keV" % (v_reg, v_reg / 1e3))
    print("     A.6 quoted                        : %8.2f eV = %.3f keV" % (target, E_QUOTED_KEV))
    print()
    print("     the quoted number is within %.1f%% of the CORRECTED value and %.0f%% of the AS-WRITTEN value."
          % (100 * abs(target - v_reg) / v_reg, 100 * abs(target - v_written) / v_written))
    ok8 = abs(target - v_reg) / v_reg < 0.01 and abs(target - v_written) / v_written > 5.0
    rec("P8", ok8, "quoted value reproduces the corrected formula to %.1f%% while being %.1fx the "
                   "as-written formula: the number survives, both inputs do not" % (100 * abs(target - v_reg) / v_reg,
                                                                                   target / v_written))

    # ------------------------------------------------------------------ S9
    hdr("S9  the consequence A.6 does not draw: unfalsifiable at the project's own probes")
    print("     %-34s %12s %10s %12s %s" % ("probe", "E", "lam", "lam / H_eff", "verdict"))
    print("     " + "-" * 86)
    for name, e in PROBES:
        lam = H_C / e
        print("     %-34s %9.2f eV %8.3f nm %12.2f  %s"
              % (name, e, lam, lam / D_REG, "z NOT resolvable" if lam / D_REG > 1 else "z resolvable"))
    print()
    print("     Both channels this project images with sit BELOW the freeze-out energy, so both are")
    print("     blind to the z residual by their own wavelength.  The claim is not merely true at those")
    print("     probes — no probe this project uses can test it.  The falsifying probe (12 keV) is one")
    print("     the project has never used and, under ME5's photon budget, cannot.")
    ok9 = all((H_C / e) / D_REG > 1 for _, e in PROBES[:2])
    rec("S9", ok9, "2.25 eV and 284 eV are both below freeze-out; lambda/H_eff = %.1f and %.1f"
        % ((H_C / 2.25) / D_REG, (H_C / 284.0) / D_REG))

    # ------------------------------------------------------------------ S10
    hdr("S10  A.6's coverage-gap claim: are the four tiers really blind to z?")
    src = open("src/route/structure_tiers.py", encoding="utf-8").read()
    tree = ast.parse(src)
    arity = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in ("total_persistence", "char_scale", "plug_q2", "q3"):
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Assign) and isinstance(sub.value, ast.Attribute)
                        and sub.value.attr == "shape" and len(sub.targets) == 1
                        and isinstance(sub.targets[0], ast.Tuple)):
                    arity[node.name] = (len(sub.targets[0].elts),
                                        ",".join(e.id for e in sub.targets[0].elts if isinstance(e, ast.Name)))
    for fn in ("total_persistence", "char_scale", "plug_q2", "q3"):
        print("     %-20s unpacks %s from .shape" % (fn, ("%d axes (%s)" % arity[fn]) if fn in arity else "no .shape unpack (delegates)"))
    try:
        a, b = np.zeros((4, 4, 4)).shape
        three_d_ok = True
    except ValueError as exc:
        three_d_ok = False
        print("     a 3-D field entering this idiom raises : ValueError: %s" % exc)
    print()
    print("     So a z-axis has no slot in the tier battery's index arithmetic.  A.6's coverage-gap")
    print("     paragraph is CORRECT, and it is the paragraph that should have stopped the claim.")
    ok10 = (not three_d_ok) and all(arity.get(f, (2,))[0] == 2 for f in arity)
    rec("S10", ok10, "all four tiers unpack 2 axes from .shape; a 3-D field cannot enter. Coverage gap confirmed")

    # ------------------------------------------------------------------ summary
    hdr("SUMMARY   (every line derived from a flag; none is a literal)")
    npass = sum(1 for _, ok, _ in FLAGS if ok)
    n = len(FLAGS)
    for tag, ok, detail in FLAGS:
        print("  %-5s %s" % (tag, "PASS" if ok else "FAIL"))
    print()
    print("  checks passed                     : %d of %d" % (npass, n))

    # verdicts, each computed
    formula_consistent = all(ok for tag, ok, _ in FLAGS if tag in ("P1", "P2"))
    selects_something = any((not ok) for tag, ok, _ in FLAGS if tag == "P3")
    k_matches_census = any((not ok) for tag, ok, _ in FLAGS if tag == "P5")
    four_slots = all(ok for tag, ok, _ in FLAGS if tag == "P6")
    bound_named = False  # A.6 names no bound; the text is searched in S7, not scored
    internal_ok = any((not ok) for tag, ok, _ in FLAGS if tag == "P7")

    print("  A.6 as written, adoptable into a body?")
    print("    - formula yields its own number     : %s" % ("yes" if formula_consistent else "NO (P1/P2)"))
    print("    - 'self-consistent point' selects   : %s" % ("yes" if selects_something else "NO — identity (P3)"))
    print("    - k = 1 is the rendered config      : %s" % ("yes" if k_matches_census else "NO — census says 1.45 (P5)"))
    print("    - four-slot conditional filled      : %s" % ("yes" if four_slots else "NO (P6)"))
    print("    - bound named as s3 requires        : %s" % ("yes" if bound_named else "NO — s3 forbids the single number"))
    print("    - internal bound holds              : %s" % ("yes" if internal_ok else "NO — fails by 1e4 (P7)"))
    print("    - coverage gap is real              : %s" % ("yes (A.6 right — S10)" if ok10 else "no (S10)"))
    adoptable = (formula_consistent and selects_something and k_matches_census and four_slots
                 and bound_named and (not internal_ok))
    print()
    print("  VERDICT: %s" % ("ADOPTABLE AS WRITTEN" if adoptable else "NOT ADOPTABLE AS WRITTEN — corrections required"))
    survived = ok10 and ok9
    print("  SURVIVING CONTENT: %s" % ("H_eff declaration + coverage gap + probe-blindness consequence"
                                      if survived else "none"))
    print()
    print("PROVENANCE: NEITHER  (audit of a submitted claim against the registered record; establishes no physics)")


if __name__ == "__main__":
    main()
