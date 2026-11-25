#!/usr/bin/env python3
"""
Numerical probe of the M_eff boundary draft v0.1 (S3->S4 branch specification).

Registered in runs/S45/meff_boundary_probe_registration.md BEFORE execution.
Every input is either an identity already established in the record, or a
definition taken from the draft itself.  No physical model is introduced.

Purpose: evaluate the draft's own formulas on the project's own registered
object, so that the audit can say "vacuous / unattainable / scale-free" with a
number instead of an opinion.

Evidence level: IDENTITY / ARITHMETIC (capped there).
"""
import math

# ---------------------------------------------------------------- registered inputs
A_PERP      = 0.040          # m^2   base area (painting_render_v1: A_c = V/H = 0.070/1.75)
H_OBJ       = 1.75           # m     object height
D_PAR       = 1.54e-14       # m     d_parallel = 15.4 fm  (roadmap 0.2 / 3.4)
N_S         = 4.22e27        # m^-2  column density
N_FRAG      = 1.18e10        # plates (front_sweep_v1: 1.457 comp/layer * 8.12e9 layers)
A0          = 5.29177210903e-11   # m  Bohr radius
LAM_OBS     = 550e-9         # m     visible-band centre, the draft's most favourable choice
C_LIGHT     = 2.99792458e8   # m/s

DELTA_INFO_SET = (1.0, 1e3, 1e6, 1e12)     # bit budgets to test


def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


# ---------------------------------------------------------------- P1 extensivity of dH
head("[Q1] Is Delta H extensive in base area?  (the draft defines it without normalising)")
dH_per_area = math.log2(H_OBJ / A0) / A0**2          # bits per m^2 at atomic resolution
for res_name, res in (("atomic (a0)", A0), ("molecular (0.3 nm)", 3e-10)):
    dpa = math.log2(H_OBJ / res) / res**2
    print("  resolution %-18s  dH/A = %.4e bits/m^2" % (res_name, dpa))
dH_1x  = dH_per_area * A_PERP
dH_10x = dH_per_area * (10.0 * A_PERP)
ratio  = dH_10x / dH_1x
print()
print("  registered object  A = %.3f m^2  ->  Delta H = %.4e bit" % (A_PERP, dH_1x))
print("  ten times wider    A = %.3f m^2  ->  Delta H = %.4e bit" % (10*A_PERP, dH_10x))
print("  ratio for A -> 10A : %.6f" % ratio)
q1 = 9.5 <= ratio <= 10.5
print("  criterion [9.5, 10.5] -> %s : Delta H is EXTENSIVE, so a size-independent"
      % ("MET" if q1 else "NOT MET"))
print("  delta_info is not a well-formed threshold across objects.")

# ---------------------------------------------------------------- P2 attainability of C_info
head("[Q2] Can C_info ever be met by the registered object?")
print("  shortfall = log10(Delta H / delta_info), Delta H = %.4e bit" % dH_1x)
for di in DELTA_INFO_SET:
    short = math.log10(dH_1x / di)
    a_crit = di / dH_per_area
    print("    delta_info = %8.0e bit -> shortfall %5.1f decades ; A_crit = %.3e m^2 (%.4f mm^2)"
          % (di, short, a_crit, a_crit * 1e6))
a_crit_ref = 1e12 / dH_per_area
q2 = a_crit_ref < 1e-4
print()
print("  with a one-terabit budget the constraint admits base areas <= %.3e m^2" % a_crit_ref)
print("  the registered object's base is %.3f m^2  ->  %.1fx too large"
      % (A_PERP, A_PERP / a_crit_ref))
print("  criterion A_crit(1e12) < 1e-4 m^2 -> %s : C_info is UNATTAINABLE as written"
      % ("MET" if q2 else "NOT MET"))

# ---------------------------------------------------------------- P3 is C_geo one statement or two?
head("[Q3] Are the draft's two statements of C_geo the same statement?")
print("  take z = a sin(kx); at the crest z'' = -a k^2 and R_perp = 1/(a k^2)")
a_amp, lam_pert = 1e-3, 2e-2
k_pert = 2.0 * math.pi / lam_pert
zpp_max  = a_amp * k_pert**2
R_perp   = 1.0 / (a_amp * k_pert**2)
lhs = LAM_OBS * zpp_max          # the draft's inequality
rhs = LAM_OBS / R_perp           # the draft's prose (R_perp vs lambda_obs)
rel = abs(lhs - rhs) / abs(rhs)
print("  lambda_obs * max|z''| = %.6e" % lhs)
print("  lambda_obs / R_perp   = %.6e" % rhs)
print("  relative difference   = %.3e" % rel)
q3 = rel < 1e-10
print("  criterion < 1e-10 -> %s : the two statements are IDENTICAL, so delta_geo is not an"
      % ("MET" if q3 else "NOT MET"))
print("  independent threshold but a restatement of R_perp > lambda_obs / delta_geo.")

# ---------------------------------------------------------------- P4 is C_geo ever non-vacuous?
head("[Q4] Is C_geo ever BOTH defined and non-vacuous?")
L_PLATE = 5e-2
zpp_plate = D_PAR / L_PLATE**2           # flattest curvature consistent with the plate thickness
dgeo_plate = LAM_OBS * zpp_plate
R_RIDGE = 5e-4
dgeo_ridge = LAM_OBS / R_RIDGE
print("  (a) converted plate, lateral %.0f cm, thickness d_par = %.2e m" % (L_PLATE*100, D_PAR))
print("      |z''| ~ d_par/L^2 = %.3e 1/m  ->  delta_geo = %.3e" % (zpp_plate, dgeo_plate))
print("  (b) surface ridge of radius %.1f mm (fingertip scale)" % (R_RIDGE*1e3))
print("      |z''| = 1/R       = %.3e 1/m  ->  delta_geo = %.3e" % (1/R_RIDGE, dgeo_ridge))
print()
print("  to make C_geo bite at delta_geo ~ 0.1 one needs R_perp ~ %.2e m = %.1f um"
      % (LAM_OBS/0.1, LAM_OBS/0.1*1e6))
q4 = (dgeo_plate < 1e-2) and (dgeo_ridge < 1e-2)
print("  criterion both < 1e-2 -> %s : C_geo is VACUOUS wherever z(x,y) is defined;"
      % ("MET" if q4 else "NOT MET"))
print("  it can only fail where z is NOT single-valued, i.e. on the un-converted bulk,")
print("  and there the constraint is undefined rather than violated.")

# ---------------------------------------------------------------- P5 C_top vs the fragment census
head("[Q5] Does chi(eps) = chi(0) survive the project's own fragment census?")
chi_3d = 2                                    # a body, topologically a ball (genus 0, 1 component)
chi_2d = N_FRAG * 1                           # each plate is contractible (disc, chi = 1)
phi_at_fail = 1.0 / N_FRAG
print("  chi_3D (intact body, ball)                = %d" % chi_3d)
print("  chi_2D (census: %.2e contractible plates) = %.3e" % (N_FRAG, chi_2d))
print("  ratio chi_2D/chi_3D                       = %.3e" % (chi_2d / chi_3d))
print("  converted fraction at which chi has already changed: phi_conv = 1/N_frag = %.3e"
      % phi_at_fail)
q5 = (chi_2d / chi_3d) > 1e6
print()
print("  criterion ratio > 1e6 -> %s : C_top holds only on phi_conv in [0, %.1e],"
      % ("MET" if q5 else "NOT MET", phi_at_fail))
print("  a set of measure ~1e-10 in the sweep variable. C_top is FALSE for essentially")
print("  the entire branch, and it is also directionally inverted (see audit F3).")

# ---------------------------------------------------------------- P6 the missing lifetime constraint
head("[Q6] Does any of the four constraints replace the established tearing bound?")
print("  t_rip = time for a signal at c_s = c/sqrt(2) to cross a length L")
print("  light round-trip time across the same L = 2L/c")
for L in (math.sqrt(A_PERP), 1.0, 7e-2):
    t_rip = math.sqrt(2.0) * L / C_LIGHT
    ratio_t = t_rip / (2.0 * L / C_LIGHT)
    print("    L = %8.4f m ->  t_rip = %.6e s ,  t_rip/(2L/c) = %.12f"
          % (L, t_rip, ratio_t))
r1 = math.sqrt(2.0) * 1.0 / C_LIGHT / (2.0 * 1.0 / C_LIGHT)
r2 = math.sqrt(2.0) * 7e-2 / C_LIGHT / (2.0 * 7e-2 / C_LIGHT)
q6 = abs(r1 / r2 - 1.0) < 1e-12
print()
print("  criterion ratio(L=1m)/ratio(L=7cm) = 1 to 1e-12 -> %s : the bound is SCALE-FREE"
      % ("MET" if q6 else "NOT MET"))
print("  (exactly 1/sqrt(2) = %.12f for every L)." % (1/math.sqrt(2.0)))
print("  No geometric, informational or topological tolerance can substitute for an")
print("  explicit lifetime constraint, which draft v0.1 does not contain.")

# ---------------------------------------------------------------- verdicts
head("[verdicts]")
rows = [
    ("Q1 Delta H extensive", q1, "size-independent delta_info is ill-formed"),
    ("Q2 C_info unattainable", q2, "shortfall 8.7 decades on the registered object"),
    ("Q3 C_geo single statement", q3, "delta_geo is not independent of R_perp"),
    ("Q4 C_geo vacuous", q4, "defined => loose by >=1e-2; tight => undefined"),
    ("Q5 C_top falsified by census", q5, "holds on measure ~1e-10 of the branch"),
    ("Q6 tearing bound scale-free", q6, "an explicit lifetime constraint is missing"),
]
for name, ok, note in rows:
    print("  %-30s %s  (%s)" % (name, "PASS" if ok else "FAIL", note))
print()
print("  All six are arithmetic on registered inputs. A PASS here means the DRAFT's")
print("  formulation is defective, not that the S3->S4 programme is unworkable.")
print()
print("Content generated by AI")
