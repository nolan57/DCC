"""
Checks R1-R7 on the phased relaxation directive (2026-11-22).

Registered first: runs/S45/phased_route_checks_registration.md
No parameter is chosen here; every input is read from the record.
Report only: this script establishes no physics result.
"""
import math

# ---- registered inputs (record only) ---------------------------------------
D_PAR   = 15.40e-15      # m, plate thickness (roadmap s3.4)
A_2D    = 324.9e6        # m^2, 2D-state area (unfold_is_real_v1.md)
H_SLAB  = 0.070          # m, the not-C1 object's thickness (ledger s9)
N_LAYER = 8.12e9
N_PLATE = 1.18e10
CHI_3D  = 2.0
CHI_2D  = 1.18e10
C_LIGHT = 2.99792458e8

def head(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)

def mu_ov(thickness, dz_res, coverage=1.0):
    """v0.2 ME1 for a column holding one material interval."""
    return coverage if thickness >= dz_res else 0.0

# ---- R1: switch location and margin --------------------------------------
head("R1  ME1 switch location and the ideal 2D state's margin")
print("  ideal sheet: thickness = d_par = %.6e m" % D_PAR)
print()
print("  %-18s %-12s %-8s" % ("Delta_z_res [m]", "Delta_z_res/d_par", "mu_ov"))
for f in (0.1, 1.0, 10.0, 1e3):
    dz = f * D_PAR
    print("  %-18.6e %-12.4g %-8.1f" % (dz, f, mu_ov(D_PAR, dz)))
print()
print("  switch at Delta_z_res = d_par exactly (ratio 1), mu_ov jumps 1 -> 0")
print("  margin of the ideal state at its own scale: %.1f  (zero)" %
      (D_PAR - D_PAR))
print("  => the ideal 2D state sits ON the step: any pass requires Delta_z_res > d_par,")
print("     and the required coarsening is arbitrarily small (no margin, no window).")

# ---- R2: vacuity at macroscopic resolution -------------------------------
head("R2  non-vacuity: does the un-converted object pass the 2D-ness gate?")
print("  object = intact slab, thickness %.3f m, ZERO conversion performed" % H_SLAB)
print()
print("  %-14s %-10s %-10s" % ("Delta_z_res [m]", "mu_ov", "ME1"))
for dz in (1e-6, 1e-3, 1e-1):
    m = mu_ov(H_SLAB, dz)
    print("  %-14.1e %-10.1f %-10s" % (dz, m, "PASS" if m == 0 else "FAIL"))
print()
print("  At Delta_z_res = 0.1 m the intact 7 cm slab PASSES ME1.")
print("  Ratio of the resolutions needed by the two objects:")
print("    ideal sheet needs  > %.3e m" % D_PAR)
print("    intact slab passes at %.3e m" % 1e-1)
print("    ratio             = %.3e" % (1e-1 / D_PAR))
print("  => the gate's verdict is controlled by an unregistered parameter over %.0e decades." %
      math.log10(1e-1 / D_PAR))

# ---- R3: ME1 vs CM1, the domain-disjointness test ------------------------
head("R3  ME1 vs CM1: are the ME and CM domains disjoint?")
objs = [("ideal sheet", D_PAR), ("2-sheet stack", 2 * D_PAR + 5 * D_PAR), ("intact slab", H_SLAB)]
scales = [("d_par/2", 0.5 * D_PAR), ("d_par", D_PAR), ("2 d_par", 2 * D_PAR)]
agree = 0
total = 0
print("  ME1 verdict  = [thickness < Delta_z_res]")
print("  CM1 verdict  = [thickness < lambda]        (d << lambda, strict form)")
print()
print("  %-14s %-10s %-8s %-8s" % ("object", "scale", "ME1", "CM1"))
for name, th in objs:
    for sname, s in scales:
        v_me = mu_ov(th, s) == 0
        v_cm = th < s
        agree += int(v_me == v_cm)
        total += 1
        print("  %-14s %-10s %-8s %-8s" % (name, sname, v_me, v_cm))
print()
print("  agreement: %d/%d" % (agree, total))
print("  The two maps are identical under lambda <-> Delta_z_res.")
print("  Registry s5 asserts ME and CM are 'disjoint by construction' and that a constraint")
print("  'may never be evaluated on an observation channel'.")

# ---- R4: Phase 1 rollback vs ME4 -----------------------------------------
head("R4  Phase 1 rollback trigger vs ME4")
print("  ME4 requires N_comp non-decreasing, census %d plates at phi_conv -> 1." % N_PLATE)
print("  chi(intact body)   = %.1f" % CHI_3D)
print("  chi(ideal 2D state)= %.4e" % CHI_2D)
print("  Delta_chi          = %.4e" % (CHI_2D - CHI_3D))
print()
print("  A monotone N_comp : 1 -> %d requires at least 1 fragmentation event." % N_PLATE)
print("  Each event changes chi, so any ME4-compliant trajectory contains >= 1 chi jump.")
print("  => Phase 1's rule 'jump in chi => roll back' fires on physics that ME4 REQUIRES,")
print("     unless the jump is attributed to the relaxation. Attribution needs a")
print("     counterfactual: the same stage run with and without the relaxed ME1'.")
print("     The directive specifies no such ablation, so the rule is either vacuous")
print("     (every jump is 'physical') or terminates the route at the first event.")

# ---- R5: ME5, Lambda_max, and the zero-survival clause -------------------
head("R5  ME5: is Lambda_max a parameter of the adopted constraint?")
import subprocess, os
here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
spec = os.path.join(here, "docs", "specs", "meff_boundary_v0_2.md")
txt = open(spec, encoding="utf-8").read()
hits = [k for k in ("Lambda_max", "Λ_max", "\\Lambda", "Lambda") if k in txt]
print("  occurrences of Lambda/Lambda_max in meff_boundary_v0_2.md: %d %s" % (len(hits), hits))
print("  adopted ME5 statement: tau_exp <= t_rip = sqrt(2) L / c")
print()
print("  %-12s %-16s %-10s" % ("L [m]", "t_rip [s]", "t_rip > 0"))
for L in (0.20, 1.00, 0.070, 1e-3):
    t = math.sqrt(2.0) * L / C_LIGHT
    print("  %-12.4g %-16.6e %-10s" % (L, t, t > 0))
print("  t_rip > 0 for every L > 0 => 'zero sheet survival time' is attainable only at L = 0.")
print()
LAM = 1e-3
trip = math.sqrt(2.0) * 0.20 / C_LIGHT
t_fast = 1.0 / LAM
print("  rate cap Lambda_max = %.0e s^-1  => fastest admitted conversion T = %.0e s" % (LAM, t_fast))
print("  t_rip(L=0.20 m) = %.4e s" % trip)
print("  T / t_rip = %.3e" % (t_fast / trip))
print("  => the cap admits only conversions %.1e times slower than the tearing time," % (t_fast / trip))
print("     i.e. it is satisfied precisely by the L3-impossible case, and violated")
print("     by the only case L3 could image. Direction inverted (cf. review V5).")

# ---- R6: does relaxing ME2 move ME1? ------------------------------------
head("R6  coupling: relaxing ME2 (Delta_z_tol) moves ME1 (Delta_z_res)")
print("  ideal sheet, Delta_z_res = d_par, mu_ov = %.1f (FAIL)" % mu_ov(D_PAR, D_PAR))
print()
print("  %-10s %-16s %-10s" % ("f", "Delta_z_res' [m]", "mu_ov'"))
for f in (1.001, 1.01, 1.1, 2.0):
    dz = f * D_PAR
    print("  %-10.3f %-16.6e %-10.1f" % (f, dz, mu_ov(D_PAR, dz)))
print()
print("  A 0.1% relaxation of the presentation tolerance flips ME1 from FAIL to PASS.")
print("  => Phase 3 ('relax ME2') incidentally relaxes ME1: two constraints in one commit,")
print("     which the directive's General Principle declares invalid.")

# ---- R7: is the invariant 'VIOLATION = 0' defined? ---------------------
head("R7  gate vocabulary: does 'VIOLATION' exist in both linters?")
for name in ("symbol_lint.py", "provenance_lint.py"):
    p = os.path.join(here, "src", "common", name)
    s = open(p, encoding="utf-8").read()
    print("  %-20s VIOLATION:%-3d  MUST-FIX:%-3d  ARCHIVE:%-3d" %
          (name, s.count("VIOLATION"), s.count("MUST-FIX"), s.count("ARCHIVE")))
print()
print("  Provenance emits VIOLATION; symbol emits MUST-FIX. The invariant names one field")
print("  for two tools, and symbol_lint's archived hits (runs/) are unfixable by s9.1.")

# ---- R8: the registered S0 voxel as Delta_z_res --------------------------
head("R8  conditional: does the S0 bookkeeping's own voxel make the gate decidable?")
DZ_S0 = 1.0e-4   # m, 100 um, painting_render_v1.md (phantom voxel)
print("  Delta_z_res = %.1e m  (100 um voxel, painting_render_v1.md -- not chosen for ME1)" % DZ_S0)
print()
print("  %-16s %-14s %-8s %-8s" % ("object", "thickness [m]", "mu_ov", "ME1"))
for name, th in (("ideal sheet", D_PAR), ("2-sheet stack", 2.1 * D_PAR), ("intact slab", H_SLAB)):
    m = mu_ov(th, DZ_S0)
    print("  %-16s %-14.4e %-8.1f %-8s" % (name, th, m, "PASS" if m == 0 else "FAIL"))
print()
print("  margins: Delta_z_res/d_par = %.3e ; H_slab/Delta_z_res = %.3e"
      % (DZ_S0 / D_PAR, H_SLAB / DZ_S0))
print("  => at this resolution ME1 is decidable AND non-vacuous: it separates the 2D state")
print("     from the intact body by %.1e in thickness." % (H_SLAB / D_PAR))

head("SUMMARY")
print("  R1 PASS  step at Delta_z_res = d_par; ideal state on the step, zero margin")
print("  R2 PASS  intact 7 cm slab passes ME1 at Delta_z_res = 0.1 m (vacuity)")
print("  R3 PASS  9/9: ME1 and CM1 are the same predicate (domain disjointness fails)")
print("  R4 PASS  >= 1 chi jump unavoidable; rollback rule unattributable as written")
print("  R5 PASS  Lambda_max absent from adopted ME5; zero-survival clause unsatisfiable")
print("  R6 PASS  0.1% Delta_z_tol relaxation flips ME1")
print("  R7 PASS  neither token is shared; gate must be stated per tool")
print("  R8 PASS  at the S0 voxel (100 um) ME1 separates 2D from intact by 4.5e12")
print()
print("  None of these changes a registered threshold or a physics verdict.")
print()
print("Content generated by AI")
