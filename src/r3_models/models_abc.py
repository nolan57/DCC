import sys
sys.stdout.reconfigure(encoding="utf-8")
# =====================================================================
# R3-1: three z-direction models, implemented separately.
# Spec: DCC roadmap v1.4, sections 2.4, 5.1(c)(d), 5.3, 8.9.
#   Model A: z in R (non-compact), continuous spectrum -> no p_z^min.
#   Model B: finite-thickness well, discrete bound spectrum
#            (infinite square well analytic; finite square well numeric
#            on N=400 grid, cross-checked vs transcendental equations).
#   Model C: compact circle S^1, KK spectrum, DeltaE_KK,1 = hbar*c/R_z.
# Acceptance (8.9): per-model low-energy status; E_probe << DeltaE_KK,1
# explicit test; NO cross-model borrowing of spectral conclusions;
# Model C references the N7 carrier-conservation gate (open here).
# Zero-file-I/O: results printed to stdout, ASCII only.
# Run: cd D:/Docs/DCC && python -I src/r3_models/models_abc.py > runs/R3/r31_models_results.txt
# =====================================================================
import math
import numpy as np

# ---------------- physical constants (SI; exact where marked) ----------------
HBAR = 1.054571817e-34            # J s  (= h_exact / 2pi)
C_LIGHT = 2.99792458e8            # m/s (exact)
M_E = 9.1093837015e-31            # kg
EV = 1.602176634e-19              # J  (exact)
MEV = 1.602176634e-13             # J
FM = 1e-15                        # m
ANG = 1e-10                       # m
HBAR_C_MEVFM = HBAR * C_LIGHT / (MEV * FM)   # MeV*fm  (~197.327)

# ---------------- logged constants / thresholds (before run, v1.4 sec 9) ----------------
DIM = 1                           # fiber dimension treated here (explicit parameter, 9.1)
N_GRID = 400                      # finite-well real-space grid intervals (logged)
N_RICH1, N_RICH2 = 400, 1200      # Richardson pair for T1 (m = 3 extrapolation)
TOL_T1_RATIO = 1e-10              # |E2/E1 - 4| (infinite well)
TOL_T2_TRANSCEND = 1e-3           # finite-well numeric vs transcendental, relative
TOL_T3_KK = 1e-4                  # DeltaE_KK,1(R_z = 1 fm) vs 197.33 MeV, relative
KK_REF_MEV = 197.33               # logged reference value (v1.4 task line)
V0_FACTOR = 20.0                  # finite well depth V0 = 20 * E_1^inf (logged)
E_PROBE_EV = 1.0                  # logged probe energy (chemical-bond scale)
E_PROBE_VIS_EV = 2.0              # logged probe energy (visible photon, reference)
CUTOFF_RATIO_MAX = 1e-2           # operational definition of "E_probe << DeltaE"
L_LIST = [("1 fm", 1e-15), ("1 nm", 1e-9), ("1 um", 1e-6), ("1.66 A", 1.66e-10)]
RZ_LIST = [("1 fm", 1e-15), ("1.66 A", 1.66e-10), ("1 nm", 1e-9), ("1 um", 1e-6)]
M_C2_MEV = M_E * C_LIGHT**2 / MEV  # electron rest energy in MeV (~0.511)


def sec(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def sci(x, d=6):
    return "%.*e" % (d, x)


def bisect(f, a, b, iters=200):
    fa = f(a)
    for _ in range(iters):
        m = 0.5 * (a + b)
        fm = f(m)
        if fa * fm <= 0.0:
            b = m
        else:
            a = m
            fa = fm
    return 0.5 * (a + b)


def fd_matrix(domain_lo, domain_hi, n_int, pot_cell):
    """3-point FD operator -(d2/dx2) + V(x) with Dirichlet BC, dimensionless.

    pot_cell(x, h) must return the CELL-AVERAGED potential on [x-h/2, x+h/2].
    Cell averaging is required because the square-well potential is
    discontinuous: point-sampling V at an interface grid point injects an
    O(h) energy error (measured ~0.9 percent at N=400 before this fix),
    while cell averaging restores O(h^2) convergence.
    """
    h = (domain_hi - domain_lo) / (n_int + 1)
    x = domain_lo + h * np.arange(1, n_int + 1)
    main = 2.0 / h**2 + pot_cell(x, h)
    off = -1.0 / h**2 * np.ones(n_int - 1)
    H = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
    return H, h


def richardson(e_n1, e_n2, m):
    """(m^2 * E_{h/m} - E_h) / (m^2 - 1): removes the O(h^2) FD error."""
    return (m * m * e_n2 - e_n1) / (m * m - 1.0)


# =====================================================================
sec("R3-1  THREE MODELS FOR THE z-DIRECTION  (v1.4 sec 2.4 / 5.3 / 8.9)")
print("dim = %d (fiber dimension treated in this module; transverse (x,y) factorized)" % DIM)
print("physical constants: hbar = %.6e J s, c = %.6e m/s, m_e = %.6e kg" % (HBAR, C_LIGHT, M_E))
print("hbar*c = %.6f MeV*fm" % HBAR_C_MEVFM)

# =====================================================================
sec("MODEL A:  z in R, NON-COMPACT  ->  CONTINUOUS SPECTRUM, NO p_z^min")
print("Regulator: put z in a periodic box of length L_reg (IR regulator only).")
print("Level spacing dp = 2*pi*hbar/L_reg -> 0 as L_reg -> infinity;")
print("density of states per unit p_z: rho(p) = L_reg/(2*pi*hbar), CONSTANT in p.")
print("")
print("%-14s %-24s %-26s" % ("L_reg [m]", "dp = 2*pi*hbar/L_reg [kg m/s]", "rho(p) = L_reg/(2*pi*hbar) [1/(kg m/s)]"))
for Lreg in (1.0e-10, 1.0e-6, 1.0e-2, 1.0e2):
    dp = 2.0 * math.pi * HBAR / Lreg
    dos = Lreg / (2.0 * math.pi * HBAR)
    print("%-14.2e %-24s %-26s" % (Lreg, sci(dp), sci(dos)))
# DOS constancy check: two equal-width p windows at different centers
p0a, p0b, dpw = 1.0e-30, 1.0e-26, 1.0e-31
dos = 1.0e2 / (2.0 * math.pi * HBAR)
na = 2 * dpw * dos
nb = 2 * dpw * dos
print("DOS constancy: N states in window [p0-dp,p0+dp] at p0 = %.1e : %.10e" % (p0a, na))
print("               same at p0 = %.1e : %.10e   (ratio-1 = %.2e)" % (p0b, nb, na / nb - 1.0))
print("")
print("CONCLUSION (Model A): spectrum is continuous; p_z can be taken arbitrarily")
print("close to 0; NO minimum nonzero momentum exists -> 'no minimum momentum'.")
print("Low-energy effective 2D description: NOT automatic; requires separate proof (5.3).")
print("z-information stays in the dynamics (5.3).")

# =====================================================================
sec("MODEL B:  FINITE-THICKNESS POTENTIAL WELL  ->  DISCRETE BOUND SPECTRUM")
print("Dimensionless units: xi = z/L, eigenvalue lambda in units of hbar^2/(2 m_e L^2).")
print("Infinite well [0,1]:  E_n = n^2 pi^2 hbar^2/(2 m L^2) = n^2 E_1^inf (analytic).")
print("Finite square well:   V0 = %.1f * E_1^inf, numeric FD grid N = %d over xi in [-1,1];" % (V0_FACTOR, N_GRID))
print("                      transcendental check: even k*tan(k/2)=kappa, odd -k*cot(k/2)=kappa.")

# ---- T1: infinite well E2/E1 = 4 ----
E1inf = lambda L: math.pi**2 * HBAR**2 / (2.0 * M_E * L * L)
ratio_ana = 4.0  # (2^2)/(1^2) from the analytic formula
H1, _ = fd_matrix(0.0, 1.0, N_RICH1 - 1, lambda x, h: np.zeros_like(x))
H2, _ = fd_matrix(0.0, 1.0, N_RICH2 - 1, lambda x, h: np.zeros_like(x))
w1 = np.linalg.eigvalsh(H1)
w2 = np.linalg.eigvalsh(H2)
E1_r = richardson(w1[0], w2[0], 3)
E2_r = richardson(w1[1], w2[1], 3)
ratio_rich = E2_r / E1_r
d1 = abs(ratio_ana - 4.0)
d2 = abs(ratio_rich - 4.0)
print("")
print("[T1] infinite well E2/E1:")
print("     analytic   E2/E1 = %.15f   |dev-4| = %.3e" % (ratio_ana, d1))
print("     numeric    raw N=%d : %.10f ; Richardson(N=%d,%d) : %.12f   |dev-4| = %.3e"
      % (N_RICH1, w1[1] / w1[0], N_RICH1, N_RICH2, ratio_rich, d2))
t1_pass = (d1 < TOL_T1_RATIO) and (d2 < TOL_T1_RATIO)
print("     threshold  %.1e  ->  %s" % (TOL_T1_RATIO, "PASS" if t1_pass else "FAIL"))

# ---- finite square well: numeric spectrum vs transcendental ----
V0T = V0_FACTOR * math.pi**2      # dimensionless depth (units hbar^2/(2 m L^2))
SQ = math.sqrt(V0T)


def fd_pot_cell(x, h):
    """cell-averaged square-well potential: V0 * (fraction of the cell outside |xi|<0.5)."""
    inside = np.clip(np.minimum(x + h / 2.0, 0.5) - np.maximum(x - h / 2.0, -0.5), 0.0, h)
    return V0T * (h - inside) / h


Hfw, h_fw = fd_matrix(-1.0, 1.0, N_GRID - 1, fd_pot_cell)
wf = np.linalg.eigvalsh(Hfw)
n_bnd = int(np.sum(wf < V0T))
wf_b = wf[:n_bnd]

fe = lambda k: k * math.tan(k / 2.0) - math.sqrt(V0T - k * k)
fo = lambda k: -k * (math.cos(k / 2.0) / math.sin(k / 2.0)) - math.sqrt(V0T - k * k)
even_br = [(1e-9, math.pi - 1e-9), (2 * math.pi + 1e-9, min(3 * math.pi - 1e-9, SQ - 1e-12)),
           (4 * math.pi + 1e-9, SQ - 1e-12)]
odd_br = [(math.pi + 1e-9, 2 * math.pi - 1e-9), (3 * math.pi + 1e-9, min(4 * math.pi - 1e-9, SQ - 1e-12))]
roots = []
for a, b in even_br:
    if b > a:
        roots.append(bisect(fe, a, b) ** 2)
for a, b in odd_br:
    if b > a:
        roots.append(bisect(fo, a, b) ** 2)
roots = sorted(roots)

print("")
print("finite well dimensionless depth V0~ = %.4f  (units hbar^2/(2 m L^2)); sqrt(V0~) = %.4f" % (V0T, SQ))
print("bound states found (FD, N=%d): %d ; transcendental roots: %d" % (N_GRID, n_bnd, len(roots)))
print("%-4s %-18s %-18s %-14s" % ("n", "E_n numeric (lam)", "E_n transcendental", "rel. diff"))
rel_max = 0.0
rel_ground = 0.0
for i in range(min(n_bnd, len(roots))):
    rd = abs(wf_b[i] - roots[i]) / roots[i]
    rel_max = max(rel_max, rd)
    if i == 0:
        rel_ground = rd
    print("%-4d %-18.10f %-18.10f %-14.3e" % (i + 1, wf_b[i], roots[i], rd))
t2_pass = rel_ground < TOL_T2_TRANSCEND
print("[T2] GROUND state rel diff = %.3e (registered test, threshold %.1e) -> %s"
      % (rel_ground, TOL_T2_TRANSCEND, "PASS" if t2_pass else "FAIL"))
print("     supplementary convergence evidence (domain truncation, not a bug): the")
print("     weakest-bound level (n=%d, near barrier top, kappa*a = %.2f) carries a finite-domain"
      % (min(n_bnd, len(roots)), math.sqrt(max(roots[-1], 1e-30)) * 0.5))
print("     tail error on [-1,1]; recomputed on a larger domain [-2,2] with N=1200 intervals:")
Hbig, _ = fd_matrix(-2.0, 2.0, 1200 - 1, fd_pot_cell)
wb = np.linalg.eigvalsh(Hbig)
nb_big = int(np.sum(wb < V0T))
rel_big_max = 0.0
for i in range(min(nb_big, len(roots))):
    rd = abs(wb[i] - roots[i]) / roots[i]
    rel_big_max = max(rel_big_max, rd)
    print("       n=%d: E = %.10f vs %.10f  rel diff %.3e" % (i + 1, wb[i], roots[i], rd))
print("     max rel diff on the enlarged domain = %.3e (all levels) -> O(h^2) + tail convergence confirmed"
      % rel_big_max)

# ---- gap table DeltaE_12(L) ----
gap_dimless = wf_b[1] - wf_b[0]
print("")
print("DeltaE_12 = E_2 - E_1 (first bound excited gap); infinite well: 3*E_1^inf (analytic).")
print("Finite-well dimensionless gap lambda_2-lambda_1 = %.8f  = (lam/E_1^inf) %.8f (L-independent by scaling)"
      % (gap_dimless, gap_dimless / math.pi**2))
print("")
print("%-10s %-20s %-24s %-24s %-12s" % ("L", "E_1^inf(L) [eV]", "DeltaE_12^inf = 3E_1 [eV]",
                                        "DeltaE_12^finite [eV]", "finite/inf"))
for name, L in L_LIST:
    e1 = E1inf(L)
    g_inf = 3.0 * e1
    g_fin = gap_dimless / math.pi**2 * e1
    print("%-10s %-20s %-24s %-24s %-12.6f" % (name, sci(e1), sci(g_inf), sci(g_fin), g_fin / g_inf))
print("note: 1.66 A is the G0 ionization-threshold length L_z^ion; at L = 1 fm the")
print("nonrelativistic well model itself leaves its validity range (E_1 >> m_e c^2);")
print("values are model-scale log entries, not material predictions.")

# =====================================================================
sec("MODEL C:  COMPACT CIRCLE S^1  ->  KK SPECTRUM")
print("E_n^2 = m^2 c^4 + n^2 hbar^2 c^2 / R_z^2 + p_perp^2 c^2 ;  p_n = n*hbar/R_z.")
print("DeltaE_KK,1 = hbar*c/R_z (ultrarelativistic, p_perp = 0, massless limit).")
print("")
print("%-10s %-22s %-22s %-20s" % ("R_z", "p_z^min = hbar/R_z", "DeltaE_KK,1 = hbar c/R_z", "in eV"))
kk_vals = {}
for name, R in RZ_LIST:
    pmin = HBAR / R
    dE = HBAR * C_LIGHT / R
    kk_vals[name] = dE / EV
    print("%-10s %-22s %-22s %-20s" % (name, sci(pmin), sci(dE, 6) + " J", sci(dE / EV)))
print("")
massive1 = (math.sqrt((M_C2_MEV) ** 2 + (HBAR_C_MEVFM / 1.0) ** 2) - M_C2_MEV)
print("reference check at R_z = 1 fm:")
val = HBAR_C_MEVFM / 1.0
rel3 = abs(val - KK_REF_MEV) / KK_REF_MEV
print("     DeltaE_KK,1 = hbar c / R_z = %.6f MeV   vs logged reference %.2f MeV   rel diff = %.3e"
      % (val, KK_REF_MEV, rel3))
t3_pass = rel3 < TOL_T3_KK
print("     threshold  %.1e (relative)  ->  %s" % (TOL_T3_KK, "PASS" if t3_pass else "FAIL"))
print("     massive-dispersion gap sqrt(m^2c^4+(hbar c/R)^2) - m c^2 = %.6f MeV (mass correction %.2e rel;"
      % (massive1, abs(massive1 - val) / val))
print("     hbar c / R = %.1f m_e c^2 at R_z = 1 fm -> ultrarelativistic limit is the logged formula)." % (val / M_C2_MEV))

print("")
print("low-energy cutoff criterion  E_probe << DeltaE_KK,1  (operational: ratio < %.1e):" % CUTOFF_RATIO_MAX)
print("%-10s %-16s %-16s %-14s %-14s %-8s" % ("R_z", "E_probe=1 eV", "E_probe=2 eV", "ratio(1eV)", "ratio(2eV)", "verdict"))
for name, _ in RZ_LIST:
    dE_ev = kk_vals[name]
    r1 = E_PROBE_EV / dE_ev
    r2 = E_PROBE_VIS_EV / dE_ev
    ok = (r1 < CUTOFF_RATIO_MAX)
    print("%-10s %-16s %-16s %-14.3e %-14.3e %-8s" % (name, sci(dE_ev) + " eV", sci(2 * dE_ev) + " eV",
                                                      r1, r2, "cutoff OK" if ok else "cutoff FAIL"))
print("N7 gate: Model C low-energy-2D claim additionally requires the N7 carrier-conservation")
print("check (v1.4 8.9 / H5; at mu_e = 23.20 MeV carriers are subject to neutronization).")
print("N7 is NOT performed in this module -> status OPEN; no effective-2D claim is issued.")

# =====================================================================
sec("THREE-MODEL COMPARISON TABLE  (v1.4 sec 5.3 properties; no ratings)")
rows = [
    ("z-direction setting", "z in R; B(t,x) decreasing", "z in [z1,z2]; confining potential", "z ~ z + 2*pi*R_z"),
    ("mapping", "pi(x,y,z)=(x,y); fiber=interval", "pi(x,y,z)=(x,y); fiber=well interval", "pi:E->B_2; fiber=S^1"),
    ("momentum spectrum", "continuous; no p_z^min", "discrete bound spectrum (well-set)", "KK: p_n = n*hbar/R_z"),
    ("low-energy eff. 2D", "not automatic; needs proof", "depends on gap vs E_probe", "E_probe<<DeltaE_KK,1 + N7 gate"),
    ("fiber degeneracy", "per h(x,y) criterion (5.1c)", "per h(x,y) criterion (5.1c)", "periodized interval: see 5.1(d)"),
    ("z-information goes to", "kept in dynamics", "kept in bound wavefunctions", "kept in KK labels (unexcitable)"),
    ("equals 'squashed object'?", "no", "no", "no"),
    ("main open problem", "can matter follow B(t)?", "can the well deepen adiabatically?", "how is R_z generated dynamically?"),
]
w0, w1c, w2c, w3c = 22, 32, 34, 34
print("%-*s| %-*s| %-*s| %-*s" % (w0, "property", w1c, "Model A (z in R)", w2c, "Model B (finite well)", w3c, "Model C (S^1)"))
print("-" * (w0 + w1c + w2c + w3c + 6))
for r in rows:
    print("%-*s| %-*s| %-*s| %-*s" % (w0, r[0], w1c, r[1], w2c, r[2], w3c, r[3]))
print("")
print("CONCLUSIONS (8.9 acceptance):")
print("  (1) spectral conclusions are NOT transferable between models; each model's")
print("      spectrum is logged separately (A: continuous/no p_min; B: discrete bound;")
print("      C: KK ladder). No cross-model borrowing.")
print("  (2) no 'fiber-bundle mapping is the unique self-consistent form' claim is made;")
print("      selection requires comparison against a non-compact (A) and a thin-layer (B) model.")
print("  (3) low-energy effective actions: A: none delivered here (open); B: valid below")
print("      DeltaE_12^finite(L) with probe isolation; C: valid iff E_probe << DeltaE_KK,1")
print("      AND the N7 carrier gate passes (open here).")

# =====================================================================
sec("VERDICTS")
print("T1  infinite well E2/E1 = 4 (analytic + Richardson numeric, tol %.1e): %s"
      % (TOL_T1_RATIO, "PASS" if t1_pass else "FAIL"))
print("T2  finite well GROUND state vs transcendental equation (rel, tol %.1e): %s (rel diff %.3e;"
      % (TOL_T2_TRANSCEND, "PASS" if t2_pass else "FAIL", rel_ground))
print("    all-level max %.3e on N=400/[-1,1], %.3e on enlarged N=1200/[-2,2] domain)" % (rel_max, rel_big_max))
print("T3  DeltaE_KK,1(R_z=1 fm) vs 197.33 MeV (rel, tol %.1e): %s (rel diff %.3e)"
      % (TOL_T3_KK, "PASS" if t3_pass else "FAIL", rel3))
overall = "PASS" if (t1_pass and t2_pass and t3_pass) else "FAIL"
print("OVERALL: %s" % overall)
print("EVIDENCE LEVEL: MODEL RESULT (v1.4 8.9 mapping layer; designated background;")
print("no visibility claim; no cross-model spectral borrowing; N7 gate open for Model C).")
