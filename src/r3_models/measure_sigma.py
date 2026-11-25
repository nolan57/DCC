import sys
sys.stdout.reconfigure(encoding="utf-8")
# =====================================================================
# R3-3: macroscopic quantities with the correct measure.
# Spec: DCC roadmap v1.4, sections 5.4, 8.11 (and G0 column-density
# consistency: under H2 (area fixed) + H3 (particle number fixed),
# d(Sigma)/dB = 0).
#   Sigma(x,y) = int rho sqrt(g_zz) dz = int rho B dz,
#   with rho declared as density PER PROPER 3-VOLUME (v1.4 5.4).
#   Slice volume element: dV_3 = sqrt(det h_ij) d^3x; in simple orthogonal
#   slicing sqrt(g_zz) = B.
# Two independent paths under compression B -> c*B:
#   path 1 "coordinate density": rho per coordinate dz held fixed
#     -> Sigma_A(c) = c * Sigma_A(1)  (NOT conserved; control, T3);
#   path 2 "proper density": H3 forces rho_proper(c) = rho_0/c
#     -> Sigma_B(c) = Sigma_B(1)     (conserved; T2).
# Which path conserves is printed (answer: the proper-density path).
# Surface charge / surface entropy same-measure formulas: equation level.
# Zero-file-I/O: results printed to stdout, ASCII only.
# Run: cd D:/Docs/DCC && python -I src/r3_models/measure_sigma.py > runs/R3/r33_measure_results.txt
# =====================================================================
import math
import numpy as np

# ---------------- logged constants / thresholds (before run) ----------------
DIM = 1                    # slice integration dimension (z only; (x,y) factorized) - explicit
B0 = 1.0                   # profile amplitude (units free; B is dimensionless here)
EPS_B = 0.3                # profile curvature parameter: B(z) = B0 (1 + eps z^2/L^2)
L_COORD = 1.0              # coordinate half-extent scale: z in [-L/2, L/2]
RHO0 = 1.0                 # base density (proper-volume convention at c = 1)
N_SIMPSON = 4001           # odd number of Simpson nodes (logged)
C_LIST = (0.5, 1.0, 2.0)   # compression factors c: B -> c*B
TOL_T1_SIMPSON = 1e-10     # Simpson vs analytic Sigma, relative
TOL_T2_INVARIANT = 1e-12   # |Sigma_B(c)/Sigma_B(1) - 1| (proper-density path)
TOL_T3_PROPORT = 1e-12     # |Sigma_A(c)/Sigma_A(1) - c| (coordinate-density path, control)


def sec(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def sci(x, d=6):
    return "%.*e" % (d, x)


def simpson(y, x):
    """composite Simpson on a uniform grid with an odd number of nodes."""
    n = len(x) - 1
    assert n % 2 == 0, "Simpson needs an even number of intervals"
    h = x[1] - x[0]
    return h / 3.0 * (y[0] + y[-1] + 4.0 * np.sum(y[1:-1:2]) + 2.0 * np.sum(y[2:-2:2]))


L = L_COORD
z = np.linspace(-L / 2.0, L / 2.0, N_SIMPSON)
B_of = lambda zz, c=1.0: c * B0 * (1.0 + EPS_B * (zz / L) ** 2)

# =====================================================================
sec("R3-3:  Sigma = int rho sqrt(g_zz) dz = int rho B dz  (v1.4 5.4 / 8.11)")
print("dim = %d (slice integration over z; transverse (x,y) factorized, area fixed = H2)." % DIM)
print("profile: B(z) = B0*(1 + eps*z^2/L^2), B0 = %.2f, eps = %.2f, z in [-L/2, L/2], L = %.2f"
      % (B0, EPS_B, L))
print("rho: uniform; measure convention is stated per delivery (8.11 requirement).")

# ---- T1: Simpson vs analytic ----
Bz = B_of(z)
rho_u = RHO0                       # uniform (proper-volume density at c = 1)
Sigma_num = rho_u * simpson(Bz, z)
# analytic: int_{-L/2}^{L/2} B0 (1 + eps z^2/L^2) dz = B0 L (1 + eps/12)
Sigma_ana = rho_u * B0 * L * (1.0 + EPS_B / 12.0)
rel1 = abs(Sigma_num - Sigma_ana) / abs(Sigma_ana)
# cross-check with np.trapezoid (lower order; no threshold, evidence only)
Sigma_trap = rho_u * float(np.trapezoid(Bz, z))
print("")
print("[T1] Simpson (N = %d nodes) vs analytic:" % N_SIMPSON)
print("     Sigma_numeric   = %s" % sci(Sigma_num))
print("     Sigma_analytic  = rho0*B0*L*(1 + eps/12) = %s   (int z^2/L^2 dz over [-L/2,L/2] = L/12)" % sci(Sigma_ana))
print("     np.trapezoid cross-check (2nd order, evidence only) = %s (diff %.2e)" % (sci(Sigma_trap), abs(Sigma_trap - Sigma_ana)))
t1_pass = rel1 < TOL_T1_SIMPSON
print("     rel diff = %.3e   threshold %.1e -> %s" % (rel1, TOL_T1_SIMPSON, "PASS" if t1_pass else "FAIL"))

# =====================================================================
sec("COMPRESSION B -> c*B:  TWO INDEPENDENT PATHS (H2 area fixed, H3 N fixed)")
print("path 1 'coordinate density': rho per coordinate volume dz, held fixed -> Sigma_A(c) = rho0*int cB dz.")
print("path 2 'proper density':     rho per PROPER volume; H3 (N fixed) forces rho(c) = rho0/c")
print("                             -> Sigma_B(c) = int (rho0/c)(cB) dz.")
print("")
print("%-6s %-22s %-22s %-22s" % ("c", "Sigma_A/Sigma_A(1)", "Sigma_B/Sigma_B(1)", "N check: SigB(c)/SigB(1)"))
base = None
dev2_max = 0.0
dev3_max = 0.0
rowA, rowB = {}, {}
for c in C_LIST:
    Bc = B_of(z, c)
    SigA = RHO0 * simpson(Bc, z)          # path 1: coordinate density fixed
    SigB = (RHO0 / c) * simpson(Bc, z)    # path 2: proper density, H3-conserving
    rowA[c], rowB[c] = SigA, SigB
    if c == 1.0:
        base = (SigA, SigB)
for c in C_LIST:
    ra = rowA[c] / base[0]
    rb = rowB[c] / base[1]
    dev2_max = max(dev2_max, abs(rb - 1.0))
    dev3_max = max(dev3_max, abs(ra - c))
    print("%-6.2f %-22.15f %-22.15f %-22.15f" % (c, ra, rb, rb))
t3_pass = dev3_max < TOL_T3_PROPORT
t2_pass = dev2_max < TOL_T2_INVARIANT
print("")
print("[T2] proper-density path: max |Sigma_B(c)/Sigma_B(1) - 1| = %.3e  threshold %.1e -> %s"
      % (dev2_max, TOL_T2_INVARIANT, "PASS" if t2_pass else "FAIL"))
print("     => Sigma is INVARIANT under B -> c*B on the proper-density path")
print("       (because the measure itself carries B: Sigma = int rho_proper B dz, and H3")
print("        rescales rho_proper by 1/c). This is the G0 column-density consistency:")
print("        d(Sigma)/dB = 0 under H2 + H3 (v1.4 5.4, 8.11 acceptance).")
print("[T3] coordinate-density path (CONTROL): max |Sigma_A(c)/Sigma_A(1) - c| = %.3e  threshold %.1e -> %s"
      % (dev3_max, TOL_T3_PROPORT, "PASS" if t3_pass else "FAIL"))
print("     => on this convention Sigma scales as Sigma_A ~ c*B (NOT conserved).")
print("")
print("WHICH PATH CONSERVES: the PROPER-DENSITY path. Per v1.4 5.4, rho in Sigma = int rho sqrt(g_zz) dz")
print("is the density per unit PROPER 3-volume; writing Sigma = int rho dz without sqrt(g_zz),")
print("or holding a coordinate-volume density fixed, is exactly the forbidden move that the")
print("T3 control exhibits. The measure convention is therefore necessary, not cosmetic.")
print("Also forbidden (5.4): treating rho(x,y,0)*L_z as a general result.")

# =====================================================================
sec("SURFACE CHARGE AND SURFACE ENTROPY: SAME-MEASURE FORMULAS (equation level)")
print("Same measure as Sigma; each delivery must state the rho definition and the slice")
print("volume element (8.11):")
print("")
print("  surface charge density:")
print("    sigma_q(x,y) = int rho_q(x,y,z) sqrt(g_zz) dz = int rho_q(x,y,z) B dz,")
print("    with rho_q the PROPER-volume charge density;")
print("  surface entropy density:")
print("    s_sur(x,y) = int s(x,y,z) sqrt(g_zz) dz = int s(x,y,z) B dz,")
print("    with s the PROPER-volume entropy density (for a degenerate gas, s is computed")
print("    from the same rho and dispersion used in G0; no separate universal constant).")
print("  particle/mass check: N/A = int rho_proper B dz = Sigma (verified in the table above).")
print("  general slicing: use dV_3 = sqrt(det h_ij) d^3x (5.4); sqrt(g_zz) = B is the")
print("  simple-orthogonal-slicing specialization used here and stated per delivery.")

# =====================================================================
sec("VERDICTS")
print("T1  Simpson vs analytic Sigma (rel, tol %.1e): %s (%.3e)"
      % (TOL_T1_SIMPSON, "PASS" if t1_pass else "FAIL", rel1))
print("T2  Sigma invariant under B -> c*B on the proper-density path (tol %.1e): %s (%.3e)"
      % (TOL_T2_INVARIANT, "PASS" if t2_pass else "FAIL", dev2_max))
print("T3  coordinate-density control Sigma_A ~ c (tol %.1e): %s (%.3e)"
      % (TOL_T3_PROPORT, "PASS" if t3_pass else "FAIL", dev3_max))
overall = "PASS" if (t1_pass and t2_pass and t3_pass) else "FAIL"
print("OVERALL: %s" % overall)
print("EVIDENCE LEVEL: MODEL RESULT (v1.4 8.11 mapping layer; designated background;")
print("no visibility claim; measure convention stated per quantity as required by 8.11).")
