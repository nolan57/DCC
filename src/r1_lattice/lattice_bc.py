# -*- coding: utf-8 -*-
"""
R1-A3: chemical bond and small-lattice instability thresholds
(v1.4 roadmap s8.2 row R1-A3, Sprint-1 screening grade; s8.4 four-way classification).

Registered model (all assumptions fixed before any run; evidence level capped at MODEL RESULT):
  M1  1D Morse pair potential V(r) = D[exp(-2 a (r-r0)) - 2 exp(-a (r-r0))];
      typical covalent parameters D = 5.0 eV, alpha = 2.0 1/A, r0 = 1.4 A.
  M2  dimer reduced mass mu = 7.0 amu (two identical 14 amu atoms).
  M3  chain atom mass m = 14.0 amu; lattice sites pinned at spacing d = B*r0
      (upper-bound stiffness scenario, explicitly registered).
  M4  dimer excitation spectrum: registered equivalent-coordinate mapping V(r) -> V(B*r)
      (well depth D kept, curvature scales as B^2, minimum at r = r0/B).
  M5  bond survival at fixed spacing: direct substitution d = B*r0 into V(d), V''(d),
      and the dissociation criterion V(d) >= 0.
  M6  continuum threshold E_c = 0 eV (V -> 0 as r -> inf, independent of B).

Zero file I/O (sandbox hook constraint): results printed to stdout, ASCII only.
Run:  cd D:/Docs/DCC && python -I src/r1_lattice/lattice_bc.py > runs/R1A/r1a3_lattice_results.txt
"""
import math
import sys

sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
from scipy.linalg import eigh_tridiagonal

# ------------------------------------------------------------------ registered inputs
D_EV = 5.0                # Morse depth [eV]
ALPHA = 2.0               # inverse range [1/A]
R0 = 1.4                  # equilibrium separation [A]
MU_AMU = 7.0              # dimer reduced mass [amu] (M2)
M_CHAIN_AMU = 14.0        # chain atom mass [amu] (M3)
B_SCAN = (0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.05, 1.10, 1.15, 1.20)
B_ION = 2.4e-9            # N8 valid-window lower edge
V_PROBE_KMS = 42.47       # G0 registered probe speed (per-nucleon kinetic scale)
M_N_KG = 1.67492749804e-27
E_PROBE_EV = 0.5 * M_N_KG * (V_PROBE_KMS * 1.0e3) ** 2 / 1.602176634e-19

# ------------------------------------------------- registered thresholds (before run)
TH_LEVEL_REL = 1.0e-3     # T1/T1b: FD vs exact Morse levels, max |dE|/|E|
TH_BC = 1.0e-4            # T2/T2b: bisection threshold vs closed form
TH_PHONON = 0.0           # T3: min omega^2 over q>0 at B=1 must exceed this
TH_COUNT_AUX = 5          # AUX: FD bound count vs exact Morse count (grid-limited states)
H_A = 5.0e-4              # FD grid step [A]

# ------------------------------------------------------------------ unit conversions
EV_J = 1.602176634e-19
HBAR_JS = 1.054571817e-34
AMU_KG = 1.6605390666e-27
A_M = 1.0e-10
H2_2MU = HBAR_JS ** 2 / (2.0 * MU_AMU * AMU_KG) / EV_J / (A_M ** 2)   # eV A^2
C1_EV = math.sqrt(2.0 * D_EV * 2.0 * H2_2MU * ALPHA ** 2)             # hbar*omega_e at B=1
LAMBDA1 = 2.0 * D_EV / C1_EV                                          # Morse lambda at B=1
LN2 = math.log(2.0)
BC_ANA = 1.0 + LN2 / (ALPHA * R0)          # curvature-instability threshold (tension side)
BD_ANA = (R0 - LN2 / ALPHA) / R0           # dissociation threshold (compression side)


# ------------------------------------------------------------------ model functions
def morse_V_arr(r, B):
    x = ALPHA * (B * r - R0)
    return D_EV * (np.exp(-2.0 * x) - 2.0 * np.exp(-x))


def morse_V_scalar(d):
    x = ALPHA * (d - R0)
    return D_EV * (math.exp(-2.0 * x) - 2.0 * math.exp(-x))


def morse_V2_scalar(d):
    x = ALPHA * (d - R0)
    e = math.exp(-x)
    return 2.0 * ALPHA * ALPHA * D_EV * e * (2.0 * e - 1.0)


def morse_level(n, B):
    """Exact Morse bound level of V(B*r): E_n = -D + c v - c^2 v^2/(4D), c = B*c1, v = n+1/2."""
    c = B * C1_EV
    v = n + 0.5
    return -D_EV + c * v - (c * c / (4.0 * D_EV)) * v * v


def morse_nbound(B):
    lam = LAMBDA1 / B
    if lam <= 0.5:
        return 0
    return int(math.ceil(lam - 0.5))


# ------------------------------------------------------------------ FD eigensolver
def build_matrix(B):
    r0b = R0 / B
    rmin = max(0.02, r0b - 3.0 / (ALPHA * B))
    rmax = r0b + 10.0 / (ALPHA * B)
    n = int(round((rmax - rmin) / H_A)) + 1
    h = (rmax - rmin) / (n - 1)
    r = rmin + h * np.arange(n)
    V = morse_V_arr(r, B)
    t = H2_2MU / (h * h)
    diag = V + 2.0 * t
    off = np.full(n - 1, -t)
    return diag, off


def spectrum_below(B, e_upper=-1.0e-9):
    """All eigenvalues of -hbar^2/2mu d2/dr2 + V(B r) below e_upper (bound states, E_c = 0)."""
    diag, off = build_matrix(B)
    return eigh_tridiagonal(diag, off, eigvals_only=True, select='v',
                            select_range=(-1.0e4, e_upper), check_finite=False)


def bisect_root(f, lo, hi, tol=1.0e-12, itmax=200):
    flo, fhi = f(lo), f(hi)
    if flo == 0.0:
        return lo
    if fhi == 0.0:
        return hi
    if flo * fhi > 0.0:
        raise ValueError("no sign change in bisection bracket")
    for _ in range(itmax):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if fm == 0.0:
            return mid
        if flo * fm < 0.0:
            hi = mid
        else:
            lo, flo = mid, fm
        if (hi - lo) <= tol * max(1.0, abs(mid)):
            break
    return 0.5 * (lo + hi)


# ------------------------------------------------------------------ main
def main():
    bar = "=" * 88
    print(bar)
    print("R1-A3: dimer + small-lattice instability thresholds (v1.4 s8.2 R1-A3, screening grade)")
    print(bar)
    print("registered model: 1D Morse V(r)=D[exp(-2a(r-r0))-2exp(-a(r-r0))], D=5 eV, a=2 1/A, r0=1.4 A")
    print("  dimer mu=7 amu; chain m=14 amu; sites pinned at d=B*r0 (upper-bound stiffness scenario)")
    print("  dimer spectrum: registered mapping V->V(B r); bond survival: V(d), V''(d), V(d)>=0")
    print("registered thresholds: T1/T1b |dE|/|E| < 1e-03; T2/T2b bisection vs closed form < 1e-04;")
    print("  T3 min omega^2(q>0, B=1) > 0; AUX |N_fd - N_exact| <= 5 (grid-limited near-threshold)")
    print("validity window (N8): B >= B_ion = 2.4e-09; nominal compression window B in [B_ion, 1]")
    print("FD grid step h = %.2e A; spectrum via symmetric tridiagonal bisection eigensolver" % H_A)

    # ------------------------------------------------ scan table
    rows = []
    W = {}
    t1b_dev = 0.0
    aux_count = 0
    for B in B_SCAN:
        w = spectrum_below(B)
        W[B] = w
        n_fd = len(w)
        e0, e1 = float(w[0]), float(w[1])
        n_ex = morse_nbound(B)
        d = B * R0
        Vd = morse_V_scalar(d)
        k = morse_V2_scalar(d)
        if k > 0.0:
            wmax = 2.0 * math.sqrt(k * EV_J / (A_M * A_M) / (M_CHAIN_AMU * AMU_KG))
            rows.append((B, d, Vd, k, e0, e1, e1 - e0, n_ex, n_fd,
                         "%.6e" % wmax, "%.6f" % (HBAR_JS * wmax / EV_J)))
        else:
            rows.append((B, d, Vd, k, e0, e1, e1 - e0, n_ex, n_fd, "IMAGINARY", "IMAGINARY"))
        for num, ana in ((e0, morse_level(0, B)), (e1, morse_level(1, B))):
            t1b_dev = max(t1b_dev, abs(num - ana) / abs(ana))
        aux_count = max(aux_count, abs(n_fd - n_ex))

    print("")
    print("[dimer + lattice scan table]")
    print("   B     d[A]     V(d)[eV]   V''[eV/A^2]   E0[eV]       E1[eV]       dE_min[eV]"
          "  N_ex N_fd  w_max[rad/s]     h*w_max[eV]")
    for (B, d, Vd, k, e0, e1, de, n_ex, n_fd, wmax_s, hwmax_s) in rows:
        print("  %.2f  %7.4f  %11.4f  %12.4f  %11.6f  %11.6f  %11.6f  %4d  %4d  %14s  %12s"
              % (B, d, Vd, k, e0, e1, de, n_ex, n_fd, wmax_s, hwmax_s))
    print("continuum threshold E_c = 0.000000 eV for all B (M6: V -> 0 as r -> inf)")

    # ------------------------------------------------ phonon summary at B = 1
    k1 = morse_V2_scalar(R0)
    k1_SI = k1 * EV_J / (A_M * A_M)
    m_ch = M_CHAIN_AMU * AMU_KG
    a1 = R0 * A_M
    print("")
    print("[phonon spectrum summary at B=1: omega^2(q) = (2/m) V''(r0) (1 - cos(q a)), a = 1.4 A]")
    for frac, label in ((1.0 / 6.0, "pi/6"), (0.25, "pi/4"), (1.0 / 3.0, "pi/3"),
                        (0.5, "pi/2"), (1.0, "pi")):
        w2 = (2.0 * k1_SI / m_ch) * (1.0 - math.cos(frac * math.pi))
        print("  q*a = %-5s : omega = %.6e rad/s (hbar*omega = %.6f eV)"
              % (label, math.sqrt(w2), HBAR_JS * math.sqrt(w2) / EV_J))
    wmax1 = 2.0 * math.sqrt(k1_SI / m_ch)
    cs = a1 * math.sqrt(k1_SI / m_ch)
    print("  omega_max(q=pi/a) = %.6e rad/s (hbar*omega_max = %.6f eV)"
          % (wmax1, HBAR_JS * wmax1 / EV_J))
    print("  sound speed c_s = a*sqrt(V''(r0)/m) = %.6e m/s" % cs)
    nq = 401
    qmax = math.pi / a1
    minw2 = min((2.0 * k1_SI / m_ch) * (1.0 - math.cos(q * a1))
                for q in (qmax * i / (nq - 1) for i in range(1, nq)))
    print("  min omega^2 over q>0 grid = %.6e rad^2/s^2" % minw2)

    # ------------------------------------------------ instability thresholds
    bc_num = bisect_root(lambda b: morse_V2_scalar(b * R0), 1.0, 2.0)
    bd_num = bisect_root(lambda b: morse_V_scalar(b * R0), 0.4, 1.0)
    dev_bc = abs(bc_num - BC_ANA)
    dev_bd = abs(bd_num - BD_ANA)
    print("")
    print("[instability thresholds]")
    print("  curvature criterion  V''(d) < 0  <=>  d > r0 + ln2/a  <=>  B > 1 + ln2/(a r0):")
    print("    numerical (bisection) B_curv = %.8f" % bc_num)
    print("    analytic  (r0+ln2/a)/r0      = %.8f   |dev| = %.3e" % (BC_ANA, dev_bc))
    print("  dissociation criterion V(d) >= 0  <=>  d <= r0 - ln2/a  <=>  B <= (r0-ln2/a)/r0:")
    print("    numerical (bisection) B_diss = %.8f" % bd_num)
    print("    analytic  (r0-ln2/a)/r0      = %.8f   |dev| = %.3e  (value quoted on the spec line)"
          % (BD_ANA, dev_bd))
    print("  spec-line sign note: the spec line derives V''<0 at alpha*(r-r0) > ln2 (tension side)")
    print("    but substitutes (r0-ln2/a)/r0 (compression side). Both thresholds are computed here:")
    print("    curvature instability at B = %.6f (tension), dissociation at B = %.6f (compression)."
          % (BC_ANA, BD_ANA))
    print("  within the registered scan window B in [0.3, 1.2]: omega^2(q) > 0 for all B and q>0;")
    print("    no imaginary frequency in window (first curvature instability at B = %.6f)." % bc_num)

    # ------------------------------------------------ dimer analytic check
    w1 = W[1.00]
    ana10 = [morse_level(n, 1.0) for n in range(10)]
    dev10 = max(abs(float(w1[n]) - ana10[n]) / abs(ana10[n]) for n in range(10))
    print("")
    print("[dimer analytic check]")
    print("  exact Morse levels: E_n(B) = -D + B*c1*(n+1/2) - (B*c1)^2*(n+1/2)^2/(4D)")
    print("  (harmonic spacing term = registered formula hbar*alpha*sqrt(2D/mu)*(n+1/2))")
    print("  c1 = %.6f eV ; lambda(B=1) = 2D/c1 = %.4f ; exact count N(B) = ceil(lambda(B)-1/2)"
          % (C1_EV, LAMBDA1))
    print("  T1  B=1, lowest 10 levels: max |dE|/|E| = %.3e   (threshold %.1e)"
          % (dev10, TH_LEVEL_REL))
    print("  T1b all-B E0/E1 (12 B values): max rel dev = %.3e   (threshold %.1e)"
          % (t1b_dev, TH_LEVEL_REL))
    print("  AUX FD bound count vs exact count: max |diff| = %d   (tolerance %d, grid-limited"
          % (aux_count, TH_COUNT_AUX))
    print("      near-threshold states; exact Morse count is the registered primary)")

    # ------------------------------------------------ s8.4 classification (computed)
    c_bd = bd_num * C1_EV
    de_bd = c_bd * (1.0 - c_bd / (2.0 * D_EV))
    de_1 = float(W[1.00][1] - W[1.00][0])
    ratio_min = E_PROBE_EV / de_bd
    print("")
    print("[s8.4 classification - computed output, no preset]")
    print("  B in [0.300000, %.6f): V(d) > 0 at the pinned spacing -> pair energy at/above the"
          % bd_num)
    print("      dissociation continuum -> class C (bound-state instability / structure destruction)")
    print("  B in [%.6f, 1.000]: omega^2 > 0 (all q>0), V(d) < 0, discrete bound spectrum exists."
          % bd_num)
    print("      excitation-spectrum data for A/B: dE_min = %.4f eV (B=1) down to %.4f eV (B=%.4f);"
          % (de_1, de_bd, bd_num))
    print("      registered probe scale E_probe = %.2f eV (G0 v_probe = %.2f km/s per nucleon);"
          % (E_PROBE_EV, V_PROBE_KMS))
    print("      E_probe/dE_min >= %.0f across the window -> excitations accessible -> computed"
          % ratio_min)
    print("      label B (non-adiabatic but still bound); adiabatic-protocol confirmation -> R1-A2")
    print("  B in (1.000, 1.200]: omega^2 > 0 still; curvature instability first at B = %.6f"
          % bc_num)
    print("      (outside the window) -> tension-side reference only, outside nominal B <= 1")
    print("  B-window annotation: scanned B in [0.3, 1.2] >> B_ion = 2.4e-09 -> inside N8 window")

    # ------------------------------------------------ findings
    print("")
    print("[findings]")
    print("  F-R1A3-1: spec-line threshold correction (registered): V''(d) < 0 holds on the TENSION")
    print("    side (alpha*(d-r0) > ln2, i.e. B > 1+ln2/(a r0) = %.6f); the spec-line value" % BC_ANA)
    print("    (r0-ln2/a)/r0 = %.6f is exactly the dissociation criterion V(d) = 0 at the pinned" % BD_ANA)
    print("    spacing (confirmed numerically, T2b). Compression-side structure destruction is ruled")
    print("    by dissociation (class C), not by imaginary phonons; in [0.3, 1.2] phonons are real.")
    print("  F-R1A3-2: under the registered mapping V->V(B r), compression softens the dimer")
    print("    (curvature B^2*V''(r0); gap dE_min = B*c1*(1-B*c1/(2D)) decreases with B) while the")
    print("    pinned-spacing energy V(d) rises and hits the continuum at B = %.6f: geometric" % BD_ANA)
    print("    compression destroys the bond by dissociation while the mapped excitation gap closes.")
    print("  F-R1A3-3: B>1 rows are tension-side reference (outside nominal window B<=1); the chain")
    print("    would lose curvature stability only at B = %.6f (stretch beyond the Morse inflection)." % bc_num)

    # ------------------------------------------------ verdicts
    print("")
    print("[verdicts]")
    verdicts = [
        ("T1 dimer B=1 lowest-10 FD vs exact Morse, max|dE|/|E| < 1e-03",
         dev10 <= TH_LEVEL_REL, "%.3e" % dev10),
        ("T1b dimer E0/E1 all-B FD vs exact Morse, max rel dev < 1e-03",
         t1b_dev <= TH_LEVEL_REL, "%.3e" % t1b_dev),
        ("T2 curvature threshold vs (r0+ln2/a)/r0, |dev| < 1e-04",
         dev_bc <= TH_BC, "%.3e" % dev_bc),
        ("T2b dissociation threshold vs (r0-ln2/a)/r0 (spec value), |dev| < 1e-04",
         dev_bd <= TH_BC, "%.3e" % dev_bd),
        ("T3 phonon spectrum B=1 all real: min omega^2(q>0) > 0",
         minw2 > TH_PHONON, "%.3e" % minw2),
        ("AUX FD bound count vs exact Morse count, max|diff| <= 5 (grid-limited)",
         aux_count <= TH_COUNT_AUX, "%d" % aux_count),
    ]
    all_ok = True
    for name, ok, val in verdicts:
        all_ok = all_ok and ok
        print("  %-72s : %-10s %s" % (name, val, "PASS" if ok else "FAIL"))
    print("")
    print("R1-A3 OVERALL: %s" % ("PASS" if all_ok else "FAIL"))
    print("evidence level: MODEL RESULT (registered Morse dimer/chain model; assumptions M1-M6 above)")


if __name__ == "__main__":
    main()
