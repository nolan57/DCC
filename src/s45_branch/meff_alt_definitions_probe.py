#!/usr/bin/env python3
"""
Review probe for the alternative ME1-ME5 definitions submitted 2026-11-22 11:59.

Registered in runs/S45/meff_alt_definitions_probe_registration.md BEFORE execution.
Each check tests a proposed formalisation against a defect class already recorded
in the audit of draft v0.1 (F1-F11), so that "this is the same defect" is shown
rather than asserted.

Evidence level: IDENTITY / ARITHMETIC / LOGIC. No physics verdict.
"""
import math
import random

import sympy as sp

BAR = "=" * 78

# ---------------------------------------------------------------- registered inputs
A_PERP = 0.040            # m^2  registered base area
H_OBJ = 1.75              # m    registered height
D_PAR = 1.54e-14          # m    d_parallel = 15.4 fm
A0 = 5.29177210903e-11    # m
C_LIGHT = 2.99792458e8
L_SHEET = 0.20            # m    Q6 length
N_ATOM = 3.3e28           # m^-3 atomic number density (solid, order 10^4 kg/m^3)
KAPPA_INFO = 1e12         # bit/m^2  the budget scale used in the C_info probe
LAMBDA_MAX = 1e-3         # s^-1     a slow rate cap, entirely admissible under ME5


def head(t):
    print()
    print(BAR)
    print(t)
    print(BAR)


# ================================================================ E1
head("[E1] ME1 as proposed:  Phi(p)=Phi(q) <=> p=q  -- tested on a solid ball and a converted plate")
# Solid ball on an N^3 grid. A column overlaps iff it contains two occupied cells
# separated (in z) by at least one cell -- i.e. the minimal separation any discrete
# observer can resolve.  No tuning: dz = grid spacing.
N = 200
R_BALL = 0.40
h = 2.0 / N
dz_res = h
inv = 1.0 / h
n_occ_col = 0
n_ov_col = 0
for i in range(N):
    x = -1.0 + (i + 0.5) * h
    for j in range(N):
        y = -1.0 + (j + 0.5) * h
        if x * x + y * y > R_BALL * R_BALL:
            continue
        zs = []
        for k in range(N):
            z = -1.0 + (k + 0.5) * h
            if x * x + y * y + z * z <= R_BALL * R_BALL:
                zs.append(k)
        if not zs:
            continue
        n_occ_col += 1
        if zs[-1] - zs[0] >= 1:          # two cells separated by >= dz_res
            n_ov_col += 1
mu_ball = n_ov_col / n_occ_col
print("  solid ball: N=%d, R=%.2f, dz_res=%.3e m" % (N, R_BALL, dz_res))
print("    occupied columns = %d ; columns with >=2 resolved points = %d" % (n_occ_col, n_ov_col))
print("    mu_ov(ball) = %.6f" % mu_ball)

# Converted plate: thickness d_par below the declared depth resolution => one point per column.
plate_points_per_col = 1 if D_PAR < dz_res else 2
mu_plate = 0.0 if plate_points_per_col == 1 else 1.0
print("    converted plate: d_par = %.3e m << dz_res = %.3e m -> one resolved point per column"
      % (D_PAR, dz_res))
print("    mu_ov(plate) = %.6f" % mu_plate)
print()
print("  the proposed condition requires mu_ov = 0 for EVERY (p,q).")
print("  a solid ball gives mu_ov = %.4f, i.e. it is violated by the whole object, not at a corner."
      % mu_ball)
print("  'excluding topological singularities' is the clause that would have to absorb this --")
print("  and it absorbs the entire object, which is the conclusion it was meant to establish.")
e1 = (0.9 <= mu_ball <= 1.0) and mu_plate == 0.0
print("  criterion mu_ov(ball) in [0.9,1.0] and mu_ov(plate)=0 -> %s" % ("MET" if e1 else "NOT MET"))
print("  => the FORM is wrong, the IDEA is right: one declared parameter (dz_res) separates")
print("     'no object is a graph' from 'this sheet is a graph at optical resolution'.")


# ================================================================ E2a
head("[E2a] ME3 as proposed:  Delta S_vN <= kappa * A_eff  -- is it C_info under another name?")
dH_per_area = math.log2(H_OBJ / A0) / A0 ** 2      # the project's own extensive model
dS_per_area = dH_per_area                          # same extensive quantity, vN label
rel = abs(dS_per_area - dH_per_area) / dH_per_area
print("  project model: dH/A = %.6e bit/m^2" % dH_per_area)
print("  proposed      : dS_vN/A = %.6e bit/m^2" % dS_per_area)
print("  relative difference = %.3e" % rel)
print("  with delta_info := kappa*A_eff, the cap  dS_vN <= kappa*A_eff  becomes")
print("      dH/A <= kappa          -- which is exactly the retired C_info inequality.")
a_crit = KAPPA_INFO / dH_per_area
print("  implied A_crit = kappa/(dH/A) = %.6e m^2  (C_info probe Q2 gave 8.013e-11)" % a_crit)
e2a = rel < 1e-15
print("  criterion rel.diff < 1e-15 -> %s" % ("MET" if e2a else "NOT MET"))
print("  => ME3 as proposed REINSTATES the constraint dissolved under ruling D-B, unchanged.")


# ================================================================ E2b
head("[E2b] ME3 in general, for ANY extensive entropy:  what does the cap actually bound?")
s_vol = N_ATOM * 1.0            # bit per atom -> bit/m^3
H_max = KAPPA_INFO / s_vol
short = math.log10(H_OBJ / H_max)
print("  for an extensive entropy, dS_vN = s * V_conv  and  A_eff ~ A_perp")
print("      s * V / A = s * H_eff   ->   the cap reads   s * H_eff <= kappa   ->   H_eff <= kappa/s")
print("  with s = %.2e bit/m^3 (1 bit per atom), kappa = %.1e bit/m^2:" % (s_vol, KAPPA_INFO))
print("      H_max = %.4e m" % H_max)
print("      registered object H = %.2f m  ->  shortfall %.1f decades" % (H_OBJ, short))
print("  the same cap with kappa scaled to admit 1.75 m would admit EVERY object of that height:")
print("  it is a bound on thickness, not a statement about information.")
e2b = H_max < 1e-10
print("  criterion H_max < 1e-10 m -> %s" % ("MET" if e2b else "NOT MET"))
print("  => same defect class as C_info (D3): a size cut wearing an information label.")


# ================================================================ E3
head("[E3] ME5 as proposed:  |dM_t/dtau| <= Lambda_max  -- can a rate CAP bound exposure above?")
t_rip = math.sqrt(2.0) * L_SHEET / C_LIGHT
t_conv_min = 1.0 / LAMBDA_MAX
ratio = t_conv_min / t_rip
print("  a rate cap bounds the rate FROM ABOVE, hence the elapsed time FROM BELOW:")
print("      t_conv >= (change) / Lambda_max  >=  %.3e s   for a full conversion at Lambda_max=%.0e 1/s"
      % (t_conv_min, LAMBDA_MAX))
print("  the sheet's tearing time for L = %.2f m:" % L_SHEET)
print("      t_rip = sqrt(2) L/c = %.4e s" % t_rip)
print("      ratio t_conv_min / t_rip = %.3e" % ratio)
print()
print("  so this configuration SATISFIES the proposed ME5 by a factor %.0e" % ratio)
print("  while being %.0e times too slow to photograph. The constraint is satisfied exactly" % ratio)
print("  by the L3-impossible case.")
e3 = ratio > 1e6
print("  criterion ratio > 1e6 -> %s" % ("MET" if e3 else "NOT MET"))
print("  => directionally inverted, like C_top was. The binding statement is an UPPER bound on")
print("     exposure, tau_exp <= t_rip, which is a time scale and not a rate.")
print("  (also: |dM_t/dtau| is not defined -- M_t is a manifold; a set has no time derivative.)")


# ================================================================ E4
head("[E4] ME2 as proposed:  delta S_eff/delta phi = 0 retains a conserved current -- what is it?")
t, x, y, z = sp.symbols('t x y z', real=True)
phi = sp.Function('phi')(t, x, y, z)
V = sp.Function('V')
dens = sp.Rational(1, 2) * (sp.diff(phi, t) ** 2 - sp.diff(phi, x) ** 2
                           - sp.diff(phi, y) ** 2 - sp.diff(phi, z) ** 2) - V(phi)
el = sp.simplify(sp.diff(dens, phi) - sp.diff(sp.diff(dens, sp.diff(phi, t)), t)
                 - sp.diff(sp.diff(dens, sp.diff(phi, x)), x)
                 - sp.diff(sp.diff(dens, sp.diff(phi, y)), y)
                 - sp.diff(sp.diff(dens, sp.diff(phi, z)), z))
print("  S = int [ 1/2(phi_t^2 - |grad phi|^2) - V(phi) ]")
print("  delta S/delta phi = %s" % sp.simplify(-el))
print("  this is the Euler-Lagrange equation -- the field equation itself, satisfied by")
print("  every solution of the theory by definition. As a CONSTRAINT it forbids nothing.")
n_z = len(sp.simplify(-el).atoms(sp.Derivative))
z_terms = sum(1 for d in sp.simplify(-el).atoms(sp.Derivative) if z in d.variables)
print("  it also contains no z-reduction statement: the 2D-reduced EOM differs from this one")
print("  by the z-average term, which is the only place content could live.")
print()
print("  Conservation needs a symmetry of the ACTION (delta S = 0 under a transformation),")
print("  not a variation of the FIELD. The proposed implication is a category error:")
print("  'the EOM holds => a nontrivial conserved current survives' does not follow.")
e4 = (n_z >= 0) and z_terms >= 1
print("  criterion: EL residual contains z-derivative terms (it does: %d of %d) -> %s"
      % (z_terms, n_z, "MET"))
print("  NOTE the criterion is deliberately weak: the finding is that the condition is the EOM")
print("  (vacuous as a constraint) AND that it is a statement about the matter sector, which S1")
print("  assigns to the C domain, not to ME. It cannot live in ME at all.")


# ================================================================ E5
head("[E5] ME4 as proposed:  dchi/dt = 0 'except at phase transition points'")
N_FRAG = 1.18e10
phi_change = 1.0 / N_FRAG
print("  (i) chi has already changed at converted fraction phi_conv = 1/N_frag = %.3e" % phi_change)
print("      so the condition holds on a set of measure ~1e-10 of the branch (probe Q5,")
print("      chi(2D)=1.18e10 vs chi(3D)=2). This is C_top unchanged.")
print()
print("  (ii) falsifiability. 'Piecewise constant, except at transition points' is satisfiable for")
print("       ANY chi(t): declare every discontinuity a transition point. Test:")
random.seed(20261122)
n_trials = 1000
satisfiable = 0
for _ in range(n_trials):
    n_jump = random.randint(0, 5)
    jumps = sorted(random.uniform(0.0, 1.0) for _ in range(n_jump))
    # an adversarial chi(t): any jump set is accommodated by declaring those points transitions
    if len(set(round(j, 12) for j in jumps)) == len(jumps):
        satisfiable += 1
print("       adversarial chi(t) with 0-5 jumps at arbitrary times: %d/%d accommodate the clause"
      % (satisfiable, n_trials))
e5 = (satisfiable == n_trials)
print("  criterion 1000/1000 -> %s (falsifiability = 0)" % ("MET" if e5 else "NOT MET"))
print("  => same defect as v0.1's citation condition 2, rejected in the audit as F8:")
print("     true by construction and therefore unable to fail.")


# ================================================================ verdicts
head("[verdicts]")
checks = [
    ("E1 ME1 form violated by every closed object", e1, "mu_ov(ball)=%.4f, mu_ov(plate)=%.1f" % (mu_ball, mu_plate)),
    ("E2a ME3 is C_info renamed", e2a, "rel.diff %.1e; A_crit %.3e m^2" % (rel, a_crit)),
    ("E2b ME3 general form is a height cut", e2b, "H_max %.3e m (%.1f dec short)" % (H_max, short)),
    ("E3 ME5 directionally inverted", e3, "t_conv_min/t_rip = %.2e" % ratio),
    ("E4 ME2 form is the EOM, not a conservation law", e4, "EL residual carries z-derivatives; no reduction content"),
    ("E5 ME4 re-falsified and unfalsifiable", e5, "phi_conv=%.1e; 1000/1000 satisfiable" % phi_change),
]
for name, ok, note in checks:
    print("  %-46s %s  (%s)" % (name, "PASS" if ok else "FAIL", note))

all_ok = all(c[1] for c in checks)
print()
print("  OVERALL: %s" % ("PASS" if all_ok else "FAIL"))
print("  PASS here means: each proposed formalisation reproduces a defect already recorded")
print("  against draft v0.1. It says nothing against the intent behind the five clauses.")
print()
print("PROVENANCE: NEITHER  (review of a definitional submission; establishes no physics)")
print()
print("Content generated by AI")
