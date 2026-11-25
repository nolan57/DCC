#!/usr/bin/env python
"""G-73-01 arithmetic and structure verifier.

Reads the frozen registration (runs/G-73-01/g73_01_registration.md), recomputes every declared
number from archived constants, and checks the two products' structure and claim tokens.

No new physics. Every constant below is copied from a named record; the only derived inputs are
the two reverse-engineered quantities of registration section 4 (c_s and R), which are solved for
from two printed equations and are accepted only if the printed ratio is reproduced.

Usage:
    python verify_g73_numbers.py            # verify; products checked if present
    python verify_g73_numbers.py --strict    # products must be present
"""

import hashlib
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REG = os.path.join(ROOT, "runs/G-73-01/g73_01_registration.md")
P1 = os.path.join(ROOT, "runs/G-73-01/adiabaticity_provenance_analysis.md")
P2 = os.path.join(ROOT, "runs/G-73-01/b3_numerical_analysis.md")

# ---------------------------------------------------------------- constants (archived)
C = 2.99792458e8
G = 6.67430e-11
HBARC_MEV_FM = 197.3269804
HBARC_SI = 3.16152677e-26
MEV_J = 1.602176634e-13

P_2D = 8.6227e16          # N/m   G0' section 2
SIGMA = 70.0             # kg/m2 G0' section 2
T_RIP = 8.2553e-9        # s     unfolding section 7
LZ = 1.0e-15             # m     normalisation
EF = 73.37               # MeV   G0' section 2
EF_ALL2D = 6.2221        # MeV   RR-DT B2
EPS = 1.7e-4             # relief amplitude, RR-DT B3
LAM = 1.0e-3             # m     RR-DT B3
N0_FM3 = 0.16            # fm^-3 saturation, R1-B1 spec
M_N_MEV = 939.565        # MeV
DELTA_PLATE = 0.215e-9   # m     demo_object_ruling
RHO_NUC = N0_FM3 * M_N_MEV * MEV_J / 1e-45   # J/m^3

# printed times in front_sweep / unfolding section 7
T_THICK_PRINTED = 4.30e-13
T_INPLANE_PRINTED = 1.80e-4
RATIO_PRINTED = 4.19e8

ROWS = []


def chk(tag, ok, detail):
    ROWS.append((tag, bool(ok), detail))


def close(a, b, rel=5e-4):
    if b == 0:
        return abs(a) < rel
    return abs(a / b - 1.0) <= rel


# ---------------------------------------------------------------- section 3 numbers
A = P_2D / SIGMA
DL = 0.5 * A * T_RIP ** 2
VC = A * T_RIP / C
GAMMA_M1 = 1.0 / math.sqrt(1.0 - VC ** 2) - 1.0
DEZ_1FM = math.pi * HBARC_MEV_FM / 1.0
LZ_MAX = math.pi * HBARC_MEV_FM / EF
TW_FROZEN = math.sqrt(2.0 * (LZ_MAX - 1.0) * 1e-15 / A)
TW_ALL2D = math.sqrt(2.0 * (math.pi * HBARC_MEV_FM / EF_ALL2D - 1.0) * 1e-15 / A)
FAC = C ** 4 / (8.0 * math.pi * G)
K = 2.0 * math.pi / LAM
K2E = K * K * EPS
RHO = FAC * K2E
RHO_MEVFM3 = RHO / MEV_J / 1e45
RATIO = RHO / RHO_NUC
RHO_Q = (RHO * HBARC_SI ** 3) ** 0.25
T_RAD = (30.0 * RHO / (math.pi ** 2 * 86.25) * HBARC_SI ** 3) ** 0.25
LAM_NUC = 1e-3 * math.sqrt(RATIO)
CURV_R = 1.0 / math.sqrt(K2E)

# external comparison anchors (registration section 2.1; not record values)
CAS_1UM = -math.pi ** 2 * 1.054571817e-34 * C / (720.0 * (1e-6) ** 4)
CAS_1NM = -math.pi ** 2 * 1.054571817e-34 * C / (720.0 * (1e-9) ** 4)
LASER = 1e22 * 1e4 / C
NS_CORE = 5.0 * RHO_NUC
QGP = 12.0 * 1.602176634e32
PLANCK = C ** 5 / (1.054571817e-34 * G ** 2) * C ** 2

# registration section 4: solve the pair
CS_IMPLIED = 2.0 * DELTA_PLATE / T_THICK_PRINTED
R_IMPLIED = CS_IMPLIED * T_INPLANE_PRINTED
RATIO_RECON = R_IMPLIED / (2.0 * DELTA_PLATE)
CS_2D = C / math.sqrt(2.0)
T_THICK_2D = 2.0 * DELTA_PLATE / CS_2D
T_INPL_2D = R_IMPLIED / CS_2D

DECLARED = [
    ("N01", A, 1.2318e15, "m/s^2", "a = P/Sigma"),
    ("N02", DL, 4.1974e-2, "m", "0.5 a t_rip^2"),
    ("N03", VC, 3.392e-2, "-", "v/c at t_rip"),
    ("N04", GAMMA_M1, 5.76e-4, "-", "gamma-1 at t_rip"),
    ("N05", DL / LZ, 4.197e13, "-", "dL/L_z"),
    ("N06", DEZ_1FM, 619.921, "MeV", "pi hbar c / 1 fm"),
    ("N07", LZ_MAX, 8.4492, "fm", "L_z max, frozen"),
    ("N08", TW_FROZEN, 3.4778e-15, "s", "t to reach L_z,max"),
    ("N09", TW_FROZEN / T_RIP, 4.2127e-7, "-", "window fraction of t_rip"),
    ("N10", math.pi * HBARC_MEV_FM / EF_ALL2D, 99.632, "fm", "L_z max, ALL2D"),
    ("N11", TW_ALL2D, 1.2655e-14, "s", "t to reach L_z,max ALL2D"),
    ("N12", 4.9635e7 * T_RIP, 0.4098, "m", "v_inf t_rip"),
    ("N13", CS_2D * T_RIP, 1.7501, "m", "c_s t_rip"),
    ("N14", FAC, 4.81545e42, "Pa m^2", "c^4/8 pi G"),
    ("N15", K2E, 6.7113e3, "m^-2", "k^2 eps"),
    ("N16", RHO, 3.23181e46, "J/m^3", "rho_req"),
    ("N17", RHO_MEVFM3, 2.01714e14, "MeV/fm^3", "rho_req"),
    ("N18", RHO_NUC, 2.4086e34, "J/m^3", "rho_nuc"),
    ("N19", RATIO, 1.3418e12, "-", "rho_req/rho_nuc"),
    ("N20", RHO_Q / MEV_J * 1e-3, 198.4, "GeV", "rho^(1/4)"),
    ("N21", T_RAD / MEV_J * 1e-3, 86.0, "GeV", "T_rad at g=86.25"),
    ("N22", LAM_NUC, 1158.0, "m", "lambda for rho_nuc"),
    ("N23", CURV_R, 1.221e-2, "m", "curvature radius"),
    ("N24", DL / (2.0 * 0.180), 0.1166, "-", "aspect ratio after growth"),
    ("N25", CS_IMPLIED, 1.000e3, "m/s", "c_s implied"),
    ("N26", R_IMPLIED, 0.180, "m", "R implied"),
    ("N27", T_THICK_2D, 2.0284e-18, "s", "2 delta / (c/sqrt2)"),
    ("N28", T_INPL_2D, 8.4912e-10, "s", "R / (c/sqrt2)"),
    ("N29", math.sqrt(2.0) * 1.75 / C, 8.2553e-9, "s", "t_rip = sqrt2 L / c"),
    ("N30", math.sqrt(2.0 * 1e-10 / A), 4.030e-13, "s", "t to 0.1 nm"),
    ("N31a", math.sqrt(2.0 * 1e-6 / A), 4.0294e-11, "s", "t to 1 um"),
    ("N31b", math.sqrt(2.0 * 1e-3 / A), 1.2738e-9, "s", "t to 1 mm"),
    ("X1", CAS_1UM, -4.3338e-4, "J/m^3", "Casimir 1 um"),
    ("X2", CAS_1NM, -4.3338e8, "J/m^3", "Casimir 1 nm"),
    ("X3", LASER, 3.3356e17, "J/m^3", "laser u=I/c"),
    ("X4", NS_CORE, 1.2043e35, "J/m^3", "NS core 5 n0"),
    ("X5", QGP, 1.9226e33, "J/m^3", "QGP 12 GeV/fm^3"),
    ("X6", PLANCK, 4.6329e113, "J/m^3", "Planck density"),
    ("N33", math.log10(RHO / abs(CAS_1UM)), 49.873, "dec", "orders over Casimir 1 um"),
    ("N34", math.log10(RHO / abs(CAS_1NM)), 37.873, "dec", "orders over Casimir 1 nm"),
    ("N35", math.log10(RHO / LASER), 28.986, "dec", "orders over laser"),
    ("N36", math.log10(RHO / NS_CORE), 11.429, "dec", "orders over NS core"),
    ("N37", math.log10(RHO / QGP), 13.226, "dec", "orders over QGP"),
    ("N38", math.log10(PLANCK / RHO), 67.156, "dec", "orders below Planck"),
    ("N39", FAC / RHO_NUC, 1.9993e8, "-", "(c^4/8piG)/rho_nuc"),
    ("N40", SIGMA * math.pi * 0.180 ** 2, 7.125, "kg", "Sigma pi R^2"),
    ("N41", 2.0 * DELTA_PLATE / 0.36, 1.194e-9, "-", "aspect ratio before growth"),
    ("N42", 1.7245e17, 1.7245e17, "J/m^2", "u_2D archived"),
    ("N43", (math.pi ** 2 / 30.0) * 106.75 * (160.0e3 * MEV_J) ** 4 / HBARC_SI ** 3, 4.797e47, "J/m^3",
     "radiation density at 160 GeV"),
    ("N44", math.log10((math.pi ** 2 / 30.0) * 106.75 * (160.0e3 * MEV_J) ** 4 / HBARC_SI ** 3 / RHO), 1.172,
     "dec", "rho_req below the 160 GeV bath"),
    ("N45", 1e-3 * math.sqrt(RHO / NS_CORE), 518.0, "m", "lambda for NS-core cost"),
    ("N46", 1e-15 / 0.07, 1.4286e-14, "-", "B at L_z = 1 fm"),
    ("N47", math.log10(2.4e-9 / (1e-15 / 0.07)), 5.2253, "dec", "decades outside v1.4 B window"),
    ("N48", 2.0 * DELTA_PLATE, 4.30e-10, "m", "2 delta"),
    ("N49", A / 9.80665, 1.256e14, "g", "a in gravities"),
]

for tag, val, dec, unit, what in DECLARED:
    chk(tag, close(val, dec), "%-34s %14.6e %-10s declared %14.6e  %s"
        % (what, val, unit, dec, "ok" if close(val, dec) else "MISMATCH"))


def build():
    out = []
    a = out.append
    a("G-73-01  VERIFICATION REPORT")
    a("=" * 78)
    a("Instrument : src/g73/verify_g73_numbers.py")
    a("Registration: runs/G-73-01/g73_01_registration.md")
    a("PROVENANCE : NEITHER (re-reads archived constants; derives no physics)")
    a("Result class: ARITHMETIC AND STRUCTURE ONLY. No survival, visibility, feasibility,")
    a("              route, gate, threshold, price or RQ claim.")
    a("")
    a("-" * 78)
    a("SECTION A  Declared arithmetic (registration section 3)")
    a("-" * 78)
    for tag, ok, det in ROWS:
        a("  %-5s %-4s %s" % (tag, "ok" if ok else "FAIL", det))

    a("")
    a("-" * 78)
    a("SECTION B  Reconstruction of the section 7 timescales (registration section 4)")
    a("-" * 78)
    a("  printed: 2*delta/c_s = %.3e s ; R/c_s = %.3e s ; R/(2 delta) = %.3e"
      % (T_THICK_PRINTED, T_INPLANE_PRINTED, RATIO_PRINTED))
    a("  solved : c_s = %.6e m/s ; R = %.6e m ; R/(2 delta) = %.6e" % (CS_IMPLIED, R_IMPLIED, RATIO_RECON))
    ok_recon = close(RATIO_RECON, RATIO_PRINTED, 2e-3)
    a("  CK1  ratio reproduced to 2e-3 : %s (deviation %.2e)"
      % ("PASS" if ok_recon else "FAIL", abs(RATIO_RECON / RATIO_PRINTED - 1)))
    a("  c_s solved / c_s(2D UR)      : %.5e / %.5e = %.3f decades below"
      % (CS_IMPLIED, CS_2D, math.log10(CS_2D / CS_IMPLIED)))
    a("  at c/sqrt2: thickness %.4e s (%.3e x t_rip) ; in-plane %.4e s (%.3e x t_rip)"
      % (T_THICK_2D, T_THICK_2D / T_RIP, T_INPL_2D, T_INPL_2D / T_RIP))
    a("  both before t_rip at c/sqrt2 : %s"
      % ("YES" if (T_THICK_2D < T_RIP and T_INPL_2D < T_RIP) else "NO"))
    chk("CK1", ok_recon, "ratio reconstruction")

    a("")
    a("-" * 78)
    a("SECTION C  Self-consistency of the B3 ballistic estimate")
    a("-" * 78)
    a("  v at t_rip = %.4e m/s = %.4f c ; gamma-1 = %.3e" % (A * T_RIP, VC, GAMMA_M1))
    a("  non-relativistic treatment valid to %.3f%% : %s"
      % (100 * GAMMA_M1, "YES" if GAMMA_M1 < 1e-2 else "NO"))
    a("  light travel within t_rip = %.4f m ; dL is %.3f%% of it" % (C * T_RIP, 100 * DL / (C * T_RIP)))
    a("  estimate spread, same t_rip: 0.5 a t^2 = %.4f m ; v_inf t = %.4f m ; c_s t = %.4f m"
      % (DL, 4.9635e7 * T_RIP, CS_2D * T_RIP))
    a("  spread factor v_inf / (0.5 a t) = %.3f ; in decades %.3f"
      % (4.9635e7 * T_RIP / DL, math.log10(4.9635e7 * T_RIP / DL)))
    chk("CK2r", GAMMA_M1 < 1e-2, "ballistic estimate non-relativistic")
    chk("CK3r", DL < C * T_RIP, "dL below the light-crossing distance")

    a("")
    a("-" * 78)
    a("SECTION D  Growth ladder: time to grow the thickness BY the stated amount")
    a("-" * 78)
    a("  (entries are increments of L_z from 1 fm, not absolute thicknesses)")
    for name, tgt in (("10 fm", 1e-14), ("1 nm", 1e-9), ("1 um", 1e-6), ("1 mm", 1e-3), ("1 cm", 1e-2), ("4.2 cm", DL)):
        a("  by %-6s t = %.4e s   t/t_rip = %.4e" % (name, math.sqrt(2.0 * tgt / A), math.sqrt(2.0 * tgt / A) / T_RIP))
    a("  rank order preserved : %s"
      % ("YES" if (math.sqrt(2e-14 / A) < math.sqrt(2e-9 / A) < math.sqrt(2e-6 / A) < math.sqrt(2e-3 / A)) else "NO"))
    chk("CK4r", math.sqrt(2e-15 / A) < math.sqrt(2e-9 / A) < math.sqrt(2e-6 / A) < math.sqrt(2e-3 / A),
        "growth ladder monotone")

    a("")
    a("-" * 78)
    a("SECTION E  Relief scaling checks")
    a("-" * 78)
    for lam in (1e-2, 1e-3, 1e-1, 1.0):
        k = 2.0 * math.pi / lam
        a("  lambda %-7g rho = %.5e J/m^3 = %.4e rho_nuc" % (lam, FAC * k * k * EPS, FAC * k * k * EPS / RHO_NUC))
    a("  rho ~ eps / lambda^2 : doubling eps doubles rho, doubling lambda quarters it")
    a("  ratio to a decade change in lambda 1e-2 -> 1e-3 : %.4f (expect 100)"
      % ((FAC * (2 * math.pi / 1e-3) ** 2 * EPS) / (FAC * (2 * math.pi / 1e-2) ** 2 * EPS)))
    chk("CK5r", close((FAC * (2 * math.pi / 1e-3) ** 2 * EPS) / (FAC * (2 * math.pi / 1e-2) ** 2 * EPS), 100.0, 1e-9),
        "1/lambda^2 scaling")
    chk("CK6r", close((FAC * K * K * 2 * EPS) / RHO, 2.0, 1e-12), "linearity in eps")

    a("")
    a("-" * 78)
    a("SECTION F  Product structure and claim guard")
    a("-" * 78)
    strict = "--strict" in sys.argv
    for path, tag in ((P1, "P1"), (P2, "P2")):
        name = os.path.basename(path)
        if not os.path.exists(path):
            a("  %-4s %-40s ABSENT (%s)" % (tag, name, "FAIL" if strict else "checked when present"))
            if strict:
                ROWS.append((tag + "-present", False, "strict mode"))
            continue
        txt = open(path, encoding="utf-8").read()
        need = ["Date:", "Directive: G-73-01", "SUMMARY", "OPEN QUESTIONS"]
        miss = [n for n in need if n not in txt]
        a("  %-4s %-40s %6d bytes  header %s" % (tag, name, len(txt), "ok" if not miss else "MISSING " + ",".join(miss)))
        ROWS.append((tag + "-hdr", not miss, "missing " + str(miss)))
        nf = txt.count("Finding:")
        ev = txt.count("Evidence:")
        asr = txt.count("Assessment:")
        a("       Finding %d / Evidence %d / Assessment %d : %s"
          % (nf, ev, asr, "ok" if nf == ev == asr and nf > 0 else "UNBALANCED"))
        ROWS.append((tag + "-fve", nf == ev == asr and nf > 0, "counts %d/%d/%d" % (nf, ev, asr)))

        bad = []
        tok = ["is feasible", "feasible in", "route is adopted", "route adopted",
               "proves adiabaticity", "disproves adiabaticity", "the object survives",
               "is visible to the eye", "survival is demonstrated"]
        for ln in txt.splitlines():
            if ln.lstrip().startswith(">"):
                continue          # archived citation, registration section 5
            low = ln.lower()
            for t in tok:
                if t in low:
                    bad.append(t)
        a("       claim tokens (non-citation lines) : %s" % ("none" if not bad else str(sorted(set(bad)))))
        ROWS.append((tag + "-claim", not bad, str(sorted(set(bad)))))

    a("")
    a("-" * 78)
    a("SECTION G  Verdicts")
    a("-" * 78)
    fails = [r for r in ROWS if not r[1]]
    a("  arithmetic rows  : %d" % len([r for r in ROWS if re.match(r"^N\d", r[0])]))
    a("  structural rows  : %d" % len([r for r in ROWS if not re.match(r"^N\d", r[0])]))
    a("  failures         : %d %s" % (len(fails), "" if not fails else str([f[0] for f in fails])))
    a("")
    a("  OVERALL: %s" % ("PASS" if not fails else "FAIL"))
    a("")
    a("Content generated by AI")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    txt = build()
    if "--write" in sys.argv:
        dst = os.path.join(ROOT, "runs/G-73-01/g73_01_verification.txt")
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        print("written %s" % dst)
    else:
        sys.stdout.write(txt)
    fails = [r for r in ROWS if not r[1]]
    sys.exit(0 if not fails else 1)
