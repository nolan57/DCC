#!/usr/bin/env python
"""
matrix_audit.py -- audit of the PROPOSED "exhaustive constraint enumeration" route.

Establishes no physics. Every number below is either
  (a) a registered constant carried in from an archive, or
  (b) arithmetic on (a).
No fitting, no new mechanism, no threshold that was not in the pre-registration.

Pre-registration: runs/MATRIX/matrix_audit_registration.md  (P1..P7, fixed before this file existed)
Inputs: front_sweep_v1.md s2 (census, placement distances); unfold_is_real_v1.md s3-s5;
        p2_clock_results.txt (t_rip, flux); G0p_seven_row_verdict_v3.md row 1 (d_parallel);
        constraint_crosswalk_v1.md (C3 in-action NO-GO, parameter-independent).
"""

import math
import itertools

# ----------------------------------------------------------------------------------
# registered constants
# ----------------------------------------------------------------------------------
C_LIGHT = 2.99792458e8            # m/s
SQ2 = math.sqrt(2.0)

# object (unfold_is_real_v1 s3: A_c = V/H = 0.070/1.75; front_sweep_v1: square array)
V_OBJ = 0.070                     # m^3
H_OBJ = 1.75                      # m
A_COL = V_OBJ / H_OBJ             # m^2 column cross-section
TILE = 0.200                      # m, tile side (unfold_is_real_v1 s3)
A_TILE = TILE * TILE              # 0.0400 m^2

# census (FROZEN, gd_rulings_v1)
N_LAYERS = 8.12e9
COMP_PER_LAYER = 1.457
N_PLATES = N_LAYERS * COMP_PER_LAYER      # 1.183e10

# layout (front_sweep_v1 s3, registered)
D_PLACE_MEAN = 13.8e3             # m, average placement distance from body centre
D_PLACE_MAX = 25.5e3              # m, maximum (diagonal)

# Phase 2 visible-channel detection requirement (p2_clock_results P2-3/P2-4)
FLUX_VIS = 9.539e31               # m^-2 s^-1 at 2 eV, dtau = 1e-7, N = 9.0e14
E_VIS = 2.25 * 1.602176634e-19    # J, 2.25 eV
SUN_IRR = 1000.0                  # W m^-2, full sun / bright-day equivalent

# FL coordinate (fl_coordinate_results)
FL3 = 0.0

flags = {}
detail = []


def rec(key, verdict, note=""):
    flags[key] = verdict
    detail.append((key, verdict, note))


def hdr(t):
    print("\n" + "=" * 94)
    print(t)
    print("=" * 94)


def fmt(x, n=4):
    return ("%.*e" % (n, x)) if (abs(x) >= 1e5 or (abs(x) < 1e-2 and x != 0)) else ("%.*f" % (n, x))


print("=" * 94)
print("MATRIX ROUTE AUDIT -- 'exhaustive constraint enumeration and distinguishability mapping'")
print("=" * 94)
print("object audited : docs/decisions/exhaustive_matrix_route_v1.md  (PROPOSED, not ratified)")
print("pre-registered : runs/MATRIX/matrix_audit_registration.md  P1..P7")
print("mode           : arithmetic on registered constants only; establishes no physics")
print("t_rip(L) = sqrt(2) L / c ;  check t_rip(1.0 m) = %.6e s against registered 4.717309e-09"
      % (SQ2 * 1.0 / C_LIGHT))

# ==================================================================================
# M-0  ENUMERATION INTEGRITY
# ==================================================================================
hdr("[M-0] ENUMERATION INTEGRITY: the table does not list 8 distinct combinations")

# the table exactly as submitted (rows 1..8), transcribed verbatim, NOT repaired
SUBMITTED = [
    (1, (+1, +1, +1), "Full"),
    (2, (+1, +1, -1), ""),
    (3, (+1, -1, +1), ""),
    (4, (-1, +1, +1), ""),
    (5, (+1, -1, -1), ""),
    (6, (-1, -1, -1), ""),
    (7, (-1, -1, +1), ""),
    (8, (-1, -1, -1), "Zero"),
]

ALL8 = set(itertools.product((+1, -1), repeat=3))
present = [r[1] for r in SUBMITTED]
distinct = set(present)
missing = sorted(ALL8 - distinct)
dupes = sorted({p for p in present if present.count(p) > 1})


def sgn(t):
    return "(%s,%s,%s)" % tuple("C%d" % (i + 1) if v > 0 else "!C%d" % (i + 1) for i, v in enumerate(t))


print("  row  combination        label")
for n, t, lab in SUBMITTED:
    print("   %d   %-18s %s" % (n, sgn(t), lab))
print("\n  claimed in sIV : 2^3 = 8 combinations, 'complete coverage' (sV)")
print("  rows printed   : %d" % len(SUBMITTED))
print("  distinct       : %d" % len(distinct))
for d in dupes:
    rows = [r[0] for r in SUBMITTED if r[1] == d]
    print("  DUPLICATE      : %s appears as rows %s" % (sgn(d), rows))
for m in missing:
    print("  MISSING        : %s is not in the table" % sgn(m))

enum_ok = (len(distinct) == 8) and not missing and not dupes
rec("M0", "COMPLETE" if enum_ok else "INCOMPLETE",
    "7 distinct of 8; rows 6 and 8 identical; %s absent" % (", ".join(sgn(m) for m in missing) if missing else "none"))

# ==================================================================================
# M-1  ROW ADMISSIBILITY
# ==================================================================================
hdr("[M-1] ROW ADMISSIBILITY: how many of the 8 rows can be instantiated at all")

print("  C3 : in-action NO-GO, PARAMETER-INDEPENDENT -- kappa(rho+p_x) = -gamma(gamma+h) < 0")
print("       for all h, gamma > 0 (constraint_crosswalk_v1).  A NO-GO constraint cannot be")
print("       SATISFIED, so any row containing C3 has no physical instantiation.")
print("  C2 : 'zero intralayer strain' is NOT a switchable property.  The registered mechanism")
print("       (front_sweep_v1 s2 step 2) is an (x,y) IDENTITY map per layer, so intralayer")
print("       strain is IDENTICALLY zero.  '!C2' therefore has no registered realization.")
print("  C1 : a genuine binary -- the object is or is not dimensionally reduced.")
print()
print("  #  combination          C3 ?   C2 ?   status")
print("  " + "-" * 72)
rows = []
for n, t, lab in SUBMITTED:
    c1, c2, c3 = t
    if c3 > 0:
        st = "VOID  (C3 is NO-GO)"
    elif c2 < 0:
        st = "UNREALIZED  (no construction)"
    else:
        st = "ADMISSIBLE"
    rows.append((n, t, st))
    print("  %d  %-18s %-6s %-6s %s" % (n, sgn(t), "+" if c3 > 0 else "-", "+" if c2 > 0 else "-", st))

n_void_print = sum(1 for _, _, s in rows if s.startswith("VOID"))
n_unreal_print = sum(1 for _, _, s in rows if s.startswith("UNREAL"))
n_adm_print = sum(1 for _, _, s in rows if s.startswith("ADMISS"))

# admissibility over the FULL 2^3 (not just the printed table)
adm_all, void_all, unreal_all = [], [], []
for t in sorted(ALL8):
    c1, c2, c3 = t
    if c3 > 0:
        void_all.append(t)
    elif c2 < 0:
        unreal_all.append(t)
    else:
        adm_all.append(t)

print("\n  over the printed table (8 rows, %d distinct):" % len(distinct))
print("    VOID = %d   UNREALIZED = %d   ADMISSIBLE = %d"
      % (n_void_print, n_unreal_print, n_adm_print))
print("  over the full 2^3 = 8 distinct combinations:")
print("    VOID = %d   UNREALIZED = %d   ADMISSIBLE = %d"
      % (len(void_all), len(unreal_all), len(adm_all)))
print("    admissible: %s" % ", ".join(sgn(t) for t in adm_all))

lost = [t for t in adm_all if t not in distinct]
print("\n  The two admissible combinations differ ONLY in C1 -- a one-bit comparison,")
print("  C1 vs !C1 with C2 and !C3 held.  But one of the two (%s) is the row the"
      % (", ".join(sgn(t) for t in lost) if lost else "-"))
print("  table omits.  So the table as printed contains exactly ONE admissible row and no")
print("  comparison at all: the single comparison the matrix could make is the one it drops.")

print("\n  NOTE  both rows the submission singles out are dead: 'Full' (row 1) is VOID, and")
print("        'Zero / minimal constraint baseline' (row 8) is UNREALIZED.  sVII.1 asks to")
print("        populate row 1 first -- it cannot be populated.")
print("  NOTE  C2 is not a free binary, so 'relaxing C2' -- one of the two axes of the")
print("        proposed matrix -- has no meaning: there is nothing to relax.")

rec("M1", "NARROWED" if len(adm_all) < 8 else "FULL",
    "%d admissible of 8 distinct (%d VOID by C3 NO-GO, %d UNREALIZED by !C2); table prints 1"
    % (len(adm_all), len(void_all), len(unreal_all)))
rec("M1B", "NO-PAIR", "printed table has one admissible row; its comparison partner is omitted")

# ==================================================================================
# M-2  L0  TOPOLOGICAL DISTINGUISHABILITY
# ==================================================================================
hdr("[M-2] L0 -- 'preserves the topological invariants (genus, connectivity) of the original'")

# original: solid column, contractible
chi_orig, b0_orig = 1.0, 1
print("  original object : V = %.3f m^3, H = %.2f m, A_c = %.4f m^2 -- one solid, contractible"
      % (V_OBJ, H_OBJ, A_COL))
print("                    beta_0 = %d, chi = %.0f" % (b0_orig, chi_orig))

# 2D scene under C1: N_PLATES disconnected contractible plates, vacuum between
chi_2d, b0_2d = N_PLATES * 1.0, int(round(N_PLATES))
print("  2D scene under C1: %.4e plates, mutually disconnected with vacuum between" % N_PLATES)
print("                    (front_sweep_v1 step 3: 'no in-plane bonding is performed')")
print("                    beta_0 = %.4e, chi = %.4e" % (b0_2d, chi_2d))
ratio = chi_2d / chi_orig
print("\n  chi ratio 2D/original = %.4e   (log10 = %.3f)" % (ratio, math.log10(ratio)))
print("  L0 verdict at C1  : %s -- connectivity is destroyed by a factor %.2e"
      % ("FAIL", ratio))
print("  L0 verdict at !C1 : PASS trivially (chi ratio = 1.0000e+00)")

print("\n  can L0 be rescued at C1?  Only by fixing the layout permutation pi:")
print("    unfold_is_real_v1 s4 -- the physical list is 'N plates + 0.04 m^2 each + 324.9 km^2'.")
print("    Any adjacency is a CHOICE of pi, and 'being a painting' is there called")
print("    'a measure-zero encoding choice, not a physical conclusion'.")
print("    So L0 at C1 passes only on an object that physics does not supply.")

rec("M2", "REVERSED", "L0 fails at C1 by 1.18e10, exact at !C1; rescue requires unphysical pi")

# ==================================================================================
# M-3  L1  METRIC DISTINGUISHABILITY
# ==================================================================================
hdr("[M-3] L1 -- 'close under an optimized metric (Hausdorff or Wasserstein)'")

dH_C1 = D_PLACE_MAX
W1_C1 = D_PLACE_MEAN
bits = N_PLATES * math.log2(N_PLATES / math.e)      # Stirling, log2(N!); scope note only
print("  both candidate metrics, both embedded in the ambient space:")
print("    Hausdorff  d_H(original, 2D layout) = registered MAX placement  = %.3e m" % dH_C1)
print("    Wasserstein W_1                      = registered MEAN placement = %.3e m" % W1_C1)
print("  normalised by the object height H = %.2f m:" % H_OBJ)
print("    d_H / H   = %.4e     W_1 / H   = %.4e" % (dH_C1 / H_OBJ, W1_C1 / H_OBJ))
print("  at !C1  (object not reduced): d_H = 0 exactly, W_1 = 0 exactly.")
print("\n  => L1 is LARGEST where 2D-ification is complete and ZERO where it never happened.")
print("     The tier's optimum is the failure of the experiment.")

print("\n  the 'metric selected individually to best fit' clause, taken literally:")
print("    for ANY layout map f, the pullback metric g* = f^*(delta) makes f an ISOMETRY,")
print("    so d(original, scene) = 0 identically -- for every layout, including a failed one.")
print("    A tier whose metric and threshold may be chosen per cell AFTER seeing the cell is")
print("    therefore satisfied by EVERY cell, failed cells included.  So L1 under sIII is not")
print("    merely non-discriminating: it is IDENTICALLY SATISFIED.  VACUOUS.")
print("    This is precisely what sVI exists to forbid, and the submission contains both")
print("    clauses.  Only one can survive (M-8).")

print("\n  scope note, so a later reader does not inherit a wrong reason for a right conclusion:")
print("    the layout permutation lives in a space of log2(N!) = %.2e bits (N = %.4e)." % (bits, N_PLATES))
print("    But the experimenter does not SPEND that: one RULE ('row-major, 90126 wide')")
print("    describes the layout in ~34 bits.  So pi is NOT an information cost and L1 does")
print("    not fail for that reason.  It fails because a per-cell metric is unfalsifiable.")
print("    The permutation matters elsewhere: presenting the arranged picture AS the physical")
print("    scene is what unfold_is_real_v1 s4 calls 'a measure-zero encoding choice, not a")
print("    physical conclusion' -- a sV 'no falsified imagery' question, not an L1 question.")
print("    [This paragraph is a correction of the audit's own first reading, which charged L1")
print("     the %.2e bits.  The number is real; the charge was misplaced.]" % bits)

rec("M3", "VACUOUS+REVERSED",
    "positional metric: max at !C1 (d=0); fitting clause: pullback metric -> L1 = 0 everywhere")

# ==================================================================================
# M-4  L2  INFORMATION-THEORETIC DISTINGUISHABILITY
# ==================================================================================
hdr("[M-4] L2 -- 'I(Scene; Structure) exceeds I_min'")

print("  I(S;T) = H(S) - H(S|T).  The scene is a deterministic function of the structure")
print("  (one object, one conversion law), so H(S|T) = 0 identically and")
print("      I(S;T) = H(S).")
print()
print("  case (i) no ensemble over structures declared:")
print("      mutual information is defined on a JOINT DISTRIBUTION.  The project has one")
print("      object.  Without an ensemble I is UNDEFINED -- not small, not zero.  This is the")
print("      ME3-F1 class (an undefined argument), not a tolerance question.")
print("  case (ii) the single registered realization:")
print("      H(S) = 0 bits (discrete, one outcome) => I = 0 at EVERY cell.")
print("      Any I_min > 0 therefore fails every cell identically.  Non-discriminating.")
print("  case (iii) over any reachable scene alphabet:")
print("      max I = max H(S), attained by a UNIFORM NOISE FIELD.")
print("      sV of the submission lists that very object as a NEGATIVE entry:")
print("        'A \"null image\" or \"structureless noise\" result is a valid matrix entry.'")
print("      So L2's argmax is the submission's own declared failure mode.")

noise_wins = True
rec("M4", "UNDEFINED-OR-NOISE", "I = H(S); argmax is structureless noise = declared failure entry")

# ==================================================================================
# M-5  L3  VISUAL DISTINGUISHABILITY
# ==================================================================================
hdr("[M-5] L3 -- 'recognizable as a structured image by a naked-eye observer, no enhancement'")

t_rip = SQ2 * H_OBJ / C_LIGHT
print("  object height H = %.2f m  ->  t_rip = sqrt(2) H / c = %.6e s" % (H_OBJ, t_rip))
print("  cross-check: t_rip(1.0 m) = %.6e s vs registered 4.717309e-09 s  -> ratio %.6f"
      % (SQ2 * 1.0 / C_LIGHT, (SQ2 * H_OBJ / C_LIGHT) / (SQ2 * 1.0 / C_LIGHT)))

print("\n  ground 1 -- TIMING (frozen corollary, ME5):")
print("    reflection needs a round trip 2H/c = %.6e s," % (2 * H_OBJ / C_LIGHT))
print("    available is t_rip = %.6e s.  Excess %.6e s = factor %.6f."
      % (t_rip, 2 * H_OBJ / C_LIGHT - t_rip, (2 * H_OBJ / C_LIGHT) / t_rip))
print("    => ZERO exposure budget in reflection.  No frame exists, naked-eye or instrumented.")

print("\n  ground 2 -- FLUX:")
req_frame = FLUX_VIS * t_rip
sun_flux = SUN_IRR / E_VIS
sun_frame = sun_flux * t_rip
print("    detection requirement (registered)  %.4e m^-2 s^-1" % FLUX_VIS)
print("      x t_rip                           = %.4e photons m^-2 per frame" % req_frame)
print("    full sun at 2.25 eV                 %.4e m^-2 s^-1" % sun_flux)
print("      x t_rip                           = %.4e photons m^-2 per frame" % sun_frame)
print("    shortfall                           = %.4e  (%.1f orders)"
      % (req_frame / sun_frame, math.log10(req_frame / sun_frame)))
print("    and this is the DETECTOR threshold, before the eye's own ~90-photon requirement,")
print("    and it is at the end L3 forbids (the only channel that fits inside t_rip is 284 eV")
print("    transmission, which is band migration, i.e. exactly what L3 excludes).")

print("\n  => L3 at C1: empty on two independent grounds (timing, then flux).")
print("     L3 at !C1: trivially satisfied by the intact object -- a scene in which the")
print("     phenomenon under study did not occur.")
print("     Charitable reading (L3 presupposes a 2D scene, so !C1 rows are unscorable):")
print("     L3 is then unreachable OUTRIGHT, and Phase 2 is entered with no bound (M-7).")

rec("M5", "EMPTY-AT-C1", "zero exposure budget + %.1f orders flux short; only !C1 passes"
    % math.log10(req_frame / sun_frame))

# ==================================================================================
# M-6  TIER MONOTONICITY
# ==================================================================================
hdr("[M-6] DOES ANY TIER INCREASE WITH 2D-IFICATION?")

print("  tier   score at !C1        score at C1                  direction")
print("  " + "-" * 74)
tab = [
    ("L0", "PASS  (chi ratio 1)", "FAIL  (chi ratio %.2e)" % ratio, "DECREASING"),
    ("L1", "0.0000 (exact)", "%.2e H (d_H)" % (dH_C1 / H_OBJ), "DECREASING"),
    ("L2", "0 (single realization)", "0 (single realization)", "CONSTANT"),
    ("L3", "PASS  (intact object)", "FAIL  (two grounds)", "DECREASING"),
]
for t, a, b, d in tab:
    print("   %s   %-22s %-28s %s" % (t, a, b, d))
n_inc = sum(1 for _, _, _, d in tab if d.startswith("INCREAS"))
print("\n  tiers increasing with 2D-ification: %d of 4" % n_inc)
print("  The matrix's cell value is 'Max Distinguishability', which needs a total order")
print("  L0 < L1 < L2 < L3.  Three columns run the other way and one is flat, so no such")
print("  order exists on the measured signs.  The matrix cannot be filled as specified --")
print("  not for lack of physics, but because every column measures what 2D-ification DESTROYS.")

rec("M6", "NONE" if n_inc == 0 else "SOME", "%d of 4 tiers increase with 2D-ification" % n_inc)

# ==================================================================================
# M-7  PHASE 2 TERMINATION
# ==================================================================================
hdr("[M-7] PHASE 2 -- 'unlimited' constraint extension, terminate on first L3")

print("  sIV Phase 2 sets: unlimited number and type; 'not pre-defined'; 'determined")
print("  dynamically'; terminate when a set yields L3.")
print()
print("  (a) no falsifier.  The search space is unbounded and unparameterised, so the")
print("      statement 'this constraint set cannot reach L3' has no test.  Same class as the")
print("      withdrawn ME4 clause 'except at phase transitions', which accommodated")
print("      1000/1000 adversarial cases and was declined for that reason.")
print("  (b) and it terminates anyway, at zero cost.  From M-5, L3 is reached at !C1.")
print("      Adding no constraint at all, the route reaches its own terminal condition on a")
print("      row where the frontier never sweeps.  sIV's trigger -- 'if and only if all 8")
print("      combinations fail to reach L3' -- is false, so Phase 2 never runs, and the route")
print("      concludes: do not perform the experiment.")
print()
print("  (c) the two branches are both unacceptable and they are simultaneous:")
print("      strict reading  -> Phase 2 entered, no termination proof  (a)")
print("      literal reading -> Phase 2 never entered, route self-defeating  (b)")

rec("M7", "UNFALSIFIABLE", "unbounded search, and literal termination is self-defeating")

# ==================================================================================
# M-8  INTERNAL CONTRADICTION: sIII vs sVI
# ==================================================================================
hdr("[M-8] sIII vs sVI -- the same threshold, two incompatible rules")

print("  sIII L1 : 'The specific metric and its threshold are selected individually for each")
print("             constraint combination to best fit its physical characteristics.'")
print("  sIII L2 : 'This threshold is dynamic and declared independently for each constraint")
print("             combination.'")
print("  sVI     : 'Thresholds for L1 and L2 must be declared before the evaluation of the")
print("             scene to prevent post-hoc fitting.'")
print()
print("  These cannot both hold.  A threshold chosen per cell, to best fit that cell, IS")
print("  post-hoc fitting; that is what the phrase forbids.  And from M-3 the fitting has a")
print("  price: at C1 the fitting metric must carry %.2e bits of pi." % bits)
print()
print("  Adjudication (executor's, for the governor): keep sVI, delete both 'selected")
print("  individually' / 'dynamic' clauses.  Reason: sVI is the invariant that makes a matrix")
print("  cell mean anything, and sV independently forbids the information the fitting injects.")
print("  Consequence, stated so it is not a surprise: with sVI alone, the fixed metric must be")
print("  chosen once, globally -- and then M-3 says which way it scores.")

rec("M8", "CONTRADICTION", "sIII per-cell threshold selection vs sVI pre-declaration")

# ==================================================================================
# SUMMARY -- derived from flags, never hand-written
# ==================================================================================
hdr("SUMMARY  (derived from the flags above)")

print("  %-6s %-20s %s" % ("id", "verdict", "note"))
print("  " + "-" * 88)
for k, v, n in detail:
    print("  %-6s %-20s %s" % (k, v, n))

NON_BLOCKING = {"COMPLETE", "FULL", "NARROWED", "SOME"}
blocking = [k for k, v, _ in detail if v not in NON_BLOCKING]
print()
print("  rows claimed / distinct          : 8 / %d" % len(distinct))
print("  rows admissible (distinct)       : %d of 8" % len(adm_all))
print("  tiers increasing with 2D-ification: %d of 4" % n_inc)
print("  cells that can be filled as specified: 0")

ok = (len(distinct) == 8) and (len(adm_all) == 8) and (n_inc > 0) and not blocking
print()
print("  ROUTE AS SPECIFIED: %s" % ("VIABLE" if ok else "NOT VIABLE AS WRITTEN"))
print("  findings that block ratification: %s" % (", ".join(blocking) if blocking else "none"))

# ----------------------------------------------------------------------------------
# registration vs outcome
# ----------------------------------------------------------------------------------
hdr("PRE-REGISTRATION vs OUTCOME")

pred = [
    ("P1", "rows reduce to 2 admissible; 4 VOID, 2 UNREALIZED (of 8 distinct)",
     "2 admissible; 4 VOID, 2 UNREALIZED",
     len(adm_all) == 2 and len(void_all) == 4 and len(unreal_all) == 2),
    ("P2", "L0 fails at C1 by factor 1.18e10; anti-monotone",
     "ratio %.4e (log10 %.3f); fails at C1, exact at !C1" % (ratio, math.log10(ratio)),
     abs(math.log10(ratio) - 10.073) < 0.01),
    ("P3", "L1 ~1.46e4 H (Hausdorff) at C1, 0 at !C1; log2(N!) = 3.79e11 bits",
     "d_H/H = %.4e, W_1/H = %.4e; pi = %.4e bits"
     % (dH_C1 / H_OBJ, W1_C1 / H_OBJ, bits),
     abs(dH_C1 / H_OBJ - 1.4571e4) < 10.0 and abs(bits / 3.788e11 - 1.0) < 1e-2),
    ("P4", "I undefined without ensemble; =0 on one realization; noise maximises",
     "all three hold; I = H(S) follows from determinism", True),
    ("P5", "L3 empty at C1 on two grounds; shortfall ~3.44e10",
     "zero exposure budget; shortfall %.4e (%.1f orders)"
     % (req_frame / sun_frame, math.log10(req_frame / sun_frame)),
     abs((req_frame / sun_frame) / 3.4387e10 - 1.0) < 1e-3),
    ("P6", "0 of 4 tiers increase with 2D-ification",
     "%d of 4" % n_inc, n_inc == 0),
    ("P7", "Phase 2 has no falsifier; literal termination is self-defeating",
     "both established by construction of the clause", True),
]

print("  %-4s %-9s %s" % ("id", "result", "outcome"))
print("  " + "-" * 92)
n_conf = 0
for pid, p, o, okp in pred:
    n_conf += 1 if okp else 0
    print("  %-4s %-9s %s" % (pid, "CONFIRMED" if okp else "FAILED", o))

print()
print("  predictions confirmed: %d of %d" % (n_conf, len(pred)))
print("  P5 is checked against its PRE-RUN-CORRECTED value 3.4387e10.  The value first written")
print("  into the pre-registration was 3.4e9, derived from t_rip = 3.893e-9 s, which was wrong")
print("  (correct: 8.2553e-9 s).  Corrected before this file existed and recorded in the")
print("  pre-registration as a disclosed correction, not silently repaired.")

if n_conf != len(pred):
    print("\n  WARNING: a prediction FAILED.  The failure is a result and may not be absorbed.")

print()
print("PROVENANCE: NEITHER  (audit arithmetic on registered inputs; establishes no physics)")
