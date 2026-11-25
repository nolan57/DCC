#!/usr/bin/env python3
"""
Disposition checks for the M_eff boundary draft (S3->S4 branch).

Registered in runs/S45/meff_disposition_checks_registration.md BEFORE execution.
Decides whether dissolving C_info is CONTENT-PRESERVING, i.e. whether its only
injectivity content is already carried by ME1, and sizes the defect in terms the
record can quote (a resolution-conditional shortfall, an exact area cut).

Evidence level: IDENTITY / ARITHMETIC. No physics verdict.
"""
import itertools
import math

# ---------------------------------------------------------------- registered inputs
A_PERP = 0.040                 # m^2  base area (painting_render_v1)
H_OBJ = 1.75                   # m    object height
A0 = 5.29177210903e-11         # m    Bohr radius
RES_SET = (("molecular (0.3 nm)", 3e-10), ("atomic (a0)", A0))
DELTA_INFO_SET = (1.0, 1e3, 1e6, 1e12)      # bit budgets, draft v0.1 s2
C_LIGHT = 2.99792458e8         # m/s
L_SET = (0.200, 1.000, 0.070)  # m    Q6 length ladder
DELTA_REF = 1e12               # bit  the budget the earlier headline used

BAR = "=" * 78


def head(title):
    print()
    print(BAR)
    print(title)
    print(BAR)


def dh_per_area(res):
    """Description length per unit base area at lateral/depth resolution `res`."""
    return math.log2(H_OBJ / res) / res ** 2


# ---------------------------------------------------------------- D1 resolution sensitivity
head("[D1] Is the '8.7 decades' shortfall resolution-independent?")
rows = []
for name, res in RES_SET:
    dpa = dh_per_area(res)
    dh = dpa * A_PERP
    short = math.log10(dh / DELTA_REF)
    rows.append((name, res, dpa, dh, short))
    print("  res %-18s = %.3e m" % (name, res))
    print("      dH/A = %.4e bits/m^2 ; dH(obj) = %.4e bit ; shortfall @1Tbit = %5.2f decades"
          % (dpa, dh, short))
shorts = [r[4] for r in rows]
span = max(shorts) - min(shorts)
d1 = all(7.0 <= s <= 8.8 for s in shorts) and span > 1.0
print()
print("  span across the declared resolutions = %.2f decades" % span)
print("  criterion all in [7.0, 8.8] and span > 1.0 -> %s" % ("MET" if d1 else "NOT MET"))
print("  => the headline 8.7 decades is RESOLUTION-CONDITIONAL. The order of magnitude is robust;")
print("     the digit is not. Any record quoting it must state (res, delta_info, A_PERP).")


# ---------------------------------------------------------------- D2 extensivity
head("[D2] Is the shortfall linear in log10(area)?  (i.e. is there a size-independent budget?)")
a_list = [A_PERP, 10 * A_PERP, 1.0, 10.0, 100.0]
dpa_ref = dh_per_area(A0)
pts = [(math.log10(a), math.log10(dpa_ref * a / DELTA_REF)) for a in a_list]
slope_d2 = (pts[-1][1] - pts[0][1]) / (pts[-1][0] - pts[0][0])
for a, (_x, y) in zip(a_list, pts):
    print("  A = %10.4f m^2  ->  shortfall %6.2f decades" % (a, y))
print()
print("  log-log slope = %.12f" % slope_d2)
d2 = abs(slope_d2 - 1.0) < 1e-12
print("  criterion |slope - 1| < 1e-12 -> %s" % ("MET" if d2 else "NOT MET"))
print("  => the shortfall grows without bound in area, so NO size-independent delta_info")
print("     can hold for all objects. C_info is not a fidelity threshold.")


# ---------------------------------------------------------------- D3 area cut
head("[D3] Is A_crit = delta_info / (dH/A) exactly linear in delta_info?")
pts3 = []
for di in DELTA_INFO_SET:
    a_crit = di / dpa_ref
    pts3.append((math.log10(di), math.log10(a_crit)))
    print("  delta_info = %8.0e bit  ->  A_crit = %.6e m^2  = %.6e mm^2" % (di, a_crit, a_crit * 1e6))
slope_d3 = (pts3[-1][1] - pts3[0][1]) / (pts3[-1][0] - pts3[0][0])
print()
print("  log-log slope = %.12f" % slope_d3)
d3 = abs(slope_d3 - 1.0) < 1e-12
print("  criterion |slope - 1| < 1e-12 -> %s" % ("MET" if d3 else "NOT MET"))
print("  => C_info, as written, is EXACTLY the statement  A_perp <= delta_info * (A/dH) ,")
print("     i.e. an upper bound on the object's base AREA. It contains no statement about")
print("     fidelity that is not already a statement about how small the object is.")


# ---------------------------------------------------------------- D4 ME5 identity
head("[D4] Is the ME5 gate a crossing-time inequality?  t_rip = sqrt(2) L/c  vs  L/c_s , c_s = c/sqrt(2)")
c_s = C_LIGHT / math.sqrt(2.0)
d4_ok = True
for L in L_SET:
    t_rip = math.sqrt(2.0) * L / C_LIGHT
    t_cross = L / c_s
    rel = abs(t_rip - t_cross) / t_cross
    ratio = t_rip / (2.0 * L / C_LIGHT)
    d4_ok = d4_ok and rel < 1e-15
    print("  L = %.3f m : t_rip = %.6e s ; L/c_s = %.6e s ; rel.diff = %.2e ; t_rip/(2L/c) = %.12f"
          % (L, t_rip, t_cross, rel, ratio))
print()
print("  criterion rel.diff < 1e-15 for every L -> %s" % ("MET" if d4_ok else "NOT MET"))
print("  => ME5's inequality  tau_exp <= sqrt(2) L/c  is identically  tau_exp <= L/c_s :")
print("     a light-crossing bound, exact and scale-free, hence registerable as a gate.")
d4 = d4_ok


# ---------------------------------------------------------------- D5 zero set == injectivity
head("[D5] Is the budget's ZERO SET exactly injectivity?  (exhaustive, 2x2x2 lattice)")
NX = NY = NZ = 2
V = NX * NY * NZ
cells = list(itertools.product(range(NX), range(NY), range(NZ)))
bits_per_point = math.log2(V)
print("  lattice %dx%dx%d  ->  V = %d cells, naive code cost per point = log2 V = %.6f bit"
      % (NX, NY, NZ, V, bits_per_point))

worst_err = 0.0
n_cfg = 0
bad_zero = []
bad_sign = []
for r in range(V + 1):
    for subset in itertools.combinations(cells, r):
        n_cfg += 1
        cols = set((x, y) for (x, y, z) in subset)
        n_ov = len(subset) - len(cols)
        # naive fixed-length code: each occupied cell costs log2(V); a column stores one value
        dh = n_ov * bits_per_point
        injective = (n_ov == 0)
        if not injective and abs(dh) < 1e-12:
            bad_zero.append(subset)
        if injective and abs(dh) > 1e-12:
            bad_zero.append(subset)
        if dh < -1e-12:
            bad_sign.append(subset)
        # identity check against the direct count
        direct = len(subset) * bits_per_point - len(cols) * bits_per_point
        worst_err = max(worst_err, abs(dh - direct))

print("  configurations enumerated = %d  (expected 2^%d = %d)" % (n_cfg, V, 2 ** V))
print("  max |dH - (N_points - N_columns)*log2 V| = %.2e" % worst_err)
print("  configurations violating  dH = 0 <=> injective : %d" % len(bad_zero))
print("  configurations with dH < 0                     : %d" % len(bad_sign))
d5 = (n_cfg == 2 ** V) and worst_err < 1e-12 and not bad_zero and not bad_sign
print()
print("  criterion identity to 1e-12 and zero-set == injectivity on all %d -> %s"
      % (n_cfg, "MET" if d5 else "NOT MET"))
print("  => the budget's zero set IS injectivity (ME1). Dissolving C_info therefore removes")
print("     no content that ME1 does not carry; what is discarded is the choice of code")
print("     (log2 V per overlap) and the choice of resolution, neither of which is physical.")


# ---------------------------------------------------------------- verdicts
head("[verdicts]")
checks = [
    ("D1 shortfall resolution-conditional", d1,
     "8.7 dec is one point on a %.1f-decade spread; quote (res, delta_info, A)" % span),
    ("D2 no size-independent budget", d2,
     "shortfall slope in log A = %.12f" % slope_d2),
    ("D3 C_info is an area cut", d3,
     "A_crit slope in log delta_info = %.12f" % slope_d3),
    ("D4 ME5 is a crossing-time gate", d4,
     "t_rip = sqrt(2)L/c = L/c_s to 1e-15"),
    ("D5 zero set == injectivity", d5,
     "exhaustive on 2x2x2; dH = N_overlap * log2 V exactly"),
]
for name, ok, note in checks:
    print("  %-38s %s  (%s)" % (name, "PASS" if ok else "FAIL", note))

all_ok = all(c[1] for c in checks)
print()
print("  OVERALL: %s" % ("PASS" if all_ok else "FAIL"))
print("  A PASS means: dissolving C_info into ME1 + a reportable budget loses no content,")
print("  and the three quantitative claims in the disposition record are arithmetic.")
print()
print("PROVENANCE: NEITHER  (definitional audit of a draft; boundary data and evidence both excluded)")
print()
print("Content generated by AI")
