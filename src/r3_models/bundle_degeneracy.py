import sys
sys.stdout.reconfigure(encoding="utf-8")
# =====================================================================
# R3-2: bundle data, degeneracy set of h(x,y), and periodized overlap.
# Spec: DCC roadmap v1.4, sections 5.1(c)(d), 5.2, 5.3, 8.10.
#   Part 1: degeneracy criterion 5.1(c):
#     sphere h = 2*sqrt(R^2-r^2) on the base disc D^2: h -> 0 on the
#       boundary circle {r=R} -> degenerate (interior fibers = intervals,
#       boundary fibers = points).
#     cylinder h = L_z const on D^2 -> non-degenerate trivial bundle.
#     Numeric output: location and measure of the degeneracy set {r=R}:
#       1D measure 2*pi*R on the base boundary circle; zero 2D measure in
#       D^2; the fiber topology jump happens on it. Sublevel areas of
#       {h < eps} restricted to the base disc D^2.
#   Part 2: periodization z ~ z + L_z (5.1(d), NOT preset as bonding or not):
#     two symmetric attractive delta wells on a ring (surface-atom model),
#     momentum-space diagonalization (plane waves N=41):
#       E_even / E_odd = lowest parity-even / parity-odd eigenstates
#         (parity w.r.t. reflection about z = L/2; classification checked
#          by [H,P] = 0),
#       DeltaE = E_even - E_odd,
#       S_ov = |<psi_A|psi_B>| (two isolated-well ground states, numerical
#         integral of the converged ring ground states, np.trapezoid).
#     scan (L, L_z): L/L_z in {0.9, 0.5, 0.1} x L_z in {1 nm, 10 nm}.
#     Supplementary converged solver: the same Hamiltonian is rank-2
#       (diag(T) - alpha*(u u^dagger + w w^dagger)), so the negative-energy
#       (bound) even/odd roots follow from two scalar quantization equations
#       alpha*(S + P) = 1 and alpha*(S - P) = 1 with
#       S = sum_n 1/(T_n+|E|), P = sum_n cos(2 pi n L/L_z)/(T_n+|E|),
#       solved at N_SUM = 2e5 plane waves (basis-truncation-free evidence).
#     Logged relation: |DeltaE| vs tunneling factor exp(-kappa*arc_min)
#       (kappa = sqrt(2 m |E_bind_single|)/hbar scale). NO directional
#       bonding conclusion is issued (5.1(d) / 8.10).
# Zero-file-I/O: results printed to stdout, ASCII only.
# Run: cd D:/Docs/DCC && python -I src/r3_models/bundle_degeneracy.py > runs/R3/r32_bundle_results.txt
# =====================================================================
import math
import numpy as np

# ---------------- physical constants ----------------
HBAR = 1.054571817e-34
C_LIGHT = 2.99792458e8
M_E = 9.1093837015e-31
EV = 1.602176634e-19

# ---------------- logged constants / thresholds (before run) ----------------
DIM = 1                            # ring coordinate dimension (explicit parameter)
R_SPHERE = 1.0                     # sphere radius for the 5.1(c) numeric demo [m]
H_CYL = 1.0                        # cylinder height h = L_z for the demo [m]
N_GRID_DEGEN = 4000                # grid for sublevel-area counting (logged)
EPS_LIST = (0.3, 0.2, 0.1)         # sublevel thresholds h < eps
TOL_SUBLEVEL = 0.10                # |A_num/A_ana - 1| for the sphere demo
N_PW = 41                          # plane-wave basis size (odd; logged per task)
KAPPA_TARGET = 5.0e9               # 1/m ; isolated-well decay scale (logged)
LZ_SCAN = (1.0e-9, 1.0e-8)         # ring circumferences for the scan [m]
FL_SCAN = (0.9, 0.5, 0.1)          # L / L_z values for the scan
N_SUM_CONV = 200000                # plane-wave cutoff of the converged secular solver
LZ_T1 = 2.0e-9                     # T1 ring size (kappa0*L_z = 10 -> free-space ok)
TOL_T1_SINGLE = 1e-3               # single-delta numeric vs -m g^2/(2 hbar^2), relative
LZ_T2_GRID = (2.0e-9, 2.5e-9, 3.0e-9, 3.5e-9, 4.0e-9)   # T2 fit rings, L = L_z/2
TOL_T2_DECAY = 0.30                # |lambda_fit - 1/kappa0| / (1/kappa0)
TOL_SYM = 1e-12                    # DeltaE(L=0.9Lz) vs DeltaE(L=0.1Lz) symmetry check
TOL_COMM = 1e-10                   # max |H P - P H| / energy scale (parity operator check)
G = HBAR**2 * KAPPA_TARGET / M_E   # delta-well strength; E_bind = -m g^2/(2 hbar^2)
E_BIND = M_E * G * G / (2.0 * HBAR**2)     # free-space single-well binding energy [J]
KAPPA0 = math.sqrt(2.0 * M_E * E_BIND) / HBAR   # = KAPPA_TARGET exactly (logged identity)


def sec(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def sci(x, d=6):
    return "%.*e" % (d, x)


# =====================================================================
sec("PART 1:  DEGENERACY SET OF h(x,y)  (v1.4 5.1(c) / 8.10)")
print("Criterion: pi is a locally trivial interval-bundle on Omega = {h>0}; on the set")
print("{h -> 0} the fiber topology jumps (interval -> point) and the bundle degenerates.")
print("")
print("JUDGMENT TABLE")
print("%-12s %-24s %-26s %-24s %-14s" % ("object", "h(x,y)", "degeneracy set", "degeneracy set measure", "verdict"))
print("%-12s %-24s %-26s %-24s %-14s"
      % ("sphere", "2*sqrt(R^2-r^2)", "{r=R} (boundary circle)", "1D: 2*pi*R = %.4f m" % (2 * math.pi * R_SPHERE), "DEGENERATE"))
print("%-12s %-24s %-26s %-24s %-14s"
      % ("sphere", "", "in base D^2: zero 2D measure;", "fiber: interval -> point jump", ""))
print("%-12s %-24s %-26s %-24s %-14s"
      % ("cylinder", "L_z = const on D^2", "empty in Omega", "none", "NON-DEGENERATE"))
print("%-12s %-24s %-26s %-24s %-14s"
      % ("cylinder", "", "(sidewall jump outside base)", "trivial bundle, fiber = I", ""))
print("")
print("Numeric sublevel check: area of {h < eps} INSIDE the base disc D^2 (sphere) vs cylinder.")
print("sphere: within D^2, {h<eps} <=> r > sqrt(R^2-eps^2/4) -> area = pi*eps^2/4 -> 0 quadratically.")
grid = np.linspace(-1.05 * R_SPHERE, 1.05 * R_SPHERE, N_GRID_DEGEN, dtype=np.float64)
X, Y = np.meshgrid(grid, grid)
rr2 = (X * X + Y * Y)
in_disk = rr2 < R_SPHERE**2
h_sph = 2.0 * np.sqrt(np.maximum(R_SPHERE**2 - rr2, 0.0))
print("%-8s %-20s %-20s %-10s" % ("eps", "A_sphere numeric", "A_sphere = pi*eps^2/4", "rel dev"))
sub_ok = True
prev = None
for eps in EPS_LIST:
    sel = (h_sph < eps) & in_disk
    a_num = float(np.mean(sel)) * (2.0 * 1.05 * R_SPHERE) ** 2
    a_ana = math.pi * eps * eps / 4.0
    dev = abs(a_num / a_ana - 1.0)
    ok = dev < TOL_SUBLEVEL
    sub_ok = sub_ok and ok and (prev is None or a_num < prev)
    prev = a_num
    print("%-8.2f %-20s %-20s %-10.3e %s" % (eps, sci(a_num), sci(a_ana), dev, "OK" if ok else "FAIL"))
h_cyl = np.full_like(h_sph, H_CYL)
print("cylinder: count{h<eps} in D^2 = %d, %d, %d for eps = 0.3, 0.2, 0.1 -> identically empty (h = L_z > eps)."
      % (int(np.sum((h_cyl < 0.3) & in_disk)), int(np.sum((h_cyl < 0.2) & in_disk)), int(np.sum((h_cyl < 0.1) & in_disk))))
print("Degeneracy-set measure (sphere): the set {r=R} itself carries 1D measure 2*pi*R =")
print("%.6f m on the base boundary circle, zero 2D measure inside D^2; the fiber topology" % (2 * math.pi * R_SPHERE))
print("jump is located exactly on it (v1.4 5.1(c): R3-2 must report location and measure).")
print("")
print("Bundle data (8.10 deliverable, equation level):")
print("  E = {(x,y,z): |z| <= h(x,y)/2};  B_2 = Omega = {h>0} (subset of the disc D^2);")
print("  fiber: open interval (-h/2, h/2) interior, point on the degeneracy set (sphere);")
print("         constant I (cylinder, trivial bundle).")
print("  transition functions: Omega is a single chart -> identity transition only.")
print("  Chern class: not applicable (fiber is an interval/point, not a principal S^1 bundle);")
print("  for a Model-C S^1 fibration over B_2, c_1 = 0 only for the trivial product (logged;")
print("  global claims require the five items of 5.2 first).")
print("  Consequence for 'no tearing': the v1.1 argument chain fails on the degeneracy set;")
print("  for the cylinder (non-degenerate) it is mathematically valid but does not imply")
print("  chemical-bond continuity (5.1(e)).")

# =====================================================================
sec("PART 2:  PERIODIZED z ~ z + L_z :  S_ov AND DeltaE  (v1.4 5.1(d) / 8.10)")
print("Model: electron on a ring of circumference L_z; two attractive delta wells of")
print("strength -g at z=0 and z=L (arc lengths: L = body-core side, L_z-L = vacuum-gap side).")
print("g = hbar^2*kappa/m with kappa = %.3e 1/m (logged); E_bind(single, free) = -m g^2/(2 hbar^2) = %s eV."
      % (KAPPA0, sci(E_BIND / EV)))
print("kappa identity: sqrt(2 m |E_bind|)/hbar = %.6e 1/m (= logged kappa; 'sqrt(2 m |V0|)/hbar' scale)." % KAPPA0)
print("Momentum-space diagonalization, plane waves n = -%d..%d (N = %d):"
      % (N_PW // 2, N_PW // 2, N_PW))
print("  H_mn = T_n delta_mn - (g/L_z) [1 + exp(i 2 pi (n-m) L / L_z)],  T_n = hbar^2 (2 pi n / L_z)^2 / (2 m).")
print("Parity classification via reflection about z = L/2 (z -> L-z):")
print("  (P psi)(z) = psi(L-z)  ->  P_mn = exp(-i 2 pi m L/L_z) delta_n,-m ; P = P^dagger, P^2 = I.")
print("  E_even = lowest eigenvalue with parity +1 ; E_odd = lowest with parity -1.")
print("  DeltaE = E_even - E_odd.  Bound status: E < 0 means below the ring continuum threshold.")
print("  S_ov = |<psi_A|psi_B>|: overlap of the two ISOLATED-well ground states (numerical")
print("  integral of the converged ring ground states A*cosh(kappa(L_z/2-d(z,well))).")
print("Bonding criterion logged as a QUANTITATIVE relation only: |DeltaE| vs exp(-kappa*arc);")
print("NO directional bonding conclusion is issued (v1.4 5.1(d), 8.10).")


def build_ham(L_z, L, g, N_PW):
    n = np.arange(-(N_PW // 2), N_PW // 2 + 1)
    T = (HBAR * 2.0 * np.pi * n / L_z) ** 2 / (2.0 * M_E)
    dm = n[:, None] - n[None, :]
    # wells at z=0 and z=+L:  V_mn = -alpha [1 + exp(i 2 pi (n-m) L / L_z)]
    V = -(g / L_z) * (1.0 + np.exp(-1j * 2.0 * np.pi * dm * L / L_z))
    return np.diag(T) + V, n


def parity_matrix(n, L, L_z):
    K = len(n)
    P = np.zeros((K, K), dtype=complex)
    for a, na in enumerate(n):
        b = int(np.argmin(np.abs(n - (-na))))
        P[a, b] = np.exp(-1j * 2.0 * np.pi * na * L / L_z)
    return P


def two_delta_split(L_z, L, g, N_PW):
    """N=41 plane-wave eigh; returns (E_even, E_odd, comm_norm, w0, w1)."""
    H, n = build_ham(L_z, L, g, N_PW)
    P = parity_matrix(n, L, L_z)
    comm = float(np.max(np.abs(H @ P - P @ H)))
    w, v = np.linalg.eigh(H)
    par = np.real(np.einsum("ij,jk,ki->i", v.conj().T, P, v))
    ev = min(w[i] for i in range(len(w)) if par[i] > 0.9)
    od = min(w[i] for i in range(len(w)) if par[i] < -0.9)
    return ev, od, comm, w[0], w[1]


def kappa_s_ring(L_z, kappa0):
    """single-delta ring ground-state decay constant: kappa*tanh(kappa*L_z/2)=kappa0.

    Bracket: for kappa <= kappa0 the LHS <= kappa <= kappa0 (f <= 0), and the
    LHS is strictly increasing, so a unique root exists in (0.5*kappa0, 50*kappa0).
    """
    lo, hi = 0.5 * kappa0, 50.0 * kappa0
    f = lambda k: k * math.tanh(k * L_z / 2.0) - kappa0
    flo = f(lo)
    for _ in range(200):
        m = 0.5 * (lo + hi)
        fm = f(m)
        if flo * fm <= 0.0:
            hi = m
        else:
            lo = m
            flo = fm
    ks = 0.5 * (lo + hi)
    x = ks * L_z / 2.0
    y = kappa0 * L_z / 2.0
    r = min(max(y / x, -1.0 + 1e-16), 1.0 - 1e-16)   # guard fp round-off at the fixed point
    resid = abs(x - math.atanh(r))         # inverted-form identity check (math.atanh)
    return ks, resid


def psi_ring(L_z, ks, z, well_pos):
    """single-delta ring ground state A*cosh(kappa*(L_z/2 - d(z, well))), normalized."""
    zm = np.mod(z - well_pos, L_z)
    d0 = np.minimum(zm, L_z - zm)
    arg = ks * (L_z / 2.0 - d0)
    norm = L_z / 2.0 + math.sinh(min(ks * L_z, 700.0)) / (2.0 * ks)
    return np.cosh(np.minimum(arg, 700.0)) / math.sqrt(norm)


def single_delta_quant(L_z, g, N_SUM):
    """converged momentum-space quantization for ONE delta well: 1 = (g/L_z) sum 1/(T_n+|E|)."""
    n = np.arange(N_SUM + 1)
    T = (HBAR * (2.0 * np.pi * n / L_z)) ** 2 / (2.0 * M_E)
    E0 = HBAR**2 * (M_E * g / HBAR**2) ** 2 / (2.0 * M_E)

    def f(x):
        s = 1.0 / x + 2.0 * np.sum(1.0 / (T[1:] + x))
        return (g / L_z) * s - 1.0

    lo, hi = 1e-3 * E0, 100.0 * E0
    flo = f(lo)
    for _ in range(300):
        m = 0.5 * (lo + hi)
        fm = f(m)
        if flo * fm <= 0.0:
            hi = m
        else:
            lo = m
            flo = fm
    return -0.5 * (lo + hi)


def two_delta_converged(L_z, L, g, N_SUM):
    """Converged negative-energy even/odd roots of the SAME two-delta ring Hamiltonian.

    H = diag(T) - alpha*(u u^dag + w w^dag), u_n = 1, w_n = exp(i 2 pi n L/L_z),
    alpha = g/L_z. Bound roots (E = -x, x > 0) follow from the rank-2 secular
    equations  alpha*(S + P) = 1  (even, b ~ (1,1))  and  alpha*(S - P) = 1
    (odd, b ~ (1,-1)), with
       S(x) = sum_n 1/(T_n + x),   P(x) = sum_n cos(2 pi n L/L_z)/(T_n + x).
    Both sums are positive, decreasing in x; the n=0 term 2/x (even) or 0 (odd)
    fixes the small-x behaviour. Returns (E_even or None, E_odd or None).
    """
    n = np.arange(N_SUM + 1)
    T = (HBAR * (2.0 * np.pi * n / L_z)) ** 2 / (2.0 * M_E)
    alpha = g / L_z
    T1 = T[1:]
    cosn = np.cos(2.0 * np.pi * n[1:] * L / L_z)

    def sp(x):
        inv = 1.0 / (T1 + x)
        S = 1.0 / x + 2.0 * np.sum(inv)
        P = 1.0 / x + 2.0 * np.sum(cosn * inv)
        return S, P

    def root(f):
        lo, hi = 1e-6 * E0g, 1e4 * E0g
        flo = f(lo)
        # f is strictly decreasing in x: flo < 0 means f < 0 everywhere on the
        # bracket -> no negative-energy root of this parity (state above the
        # ring continuum threshold). flo > 0 is the normal case (root exists).
        if flo < 0.0:
            return None
        if f(hi) > 0.0:
            return None
        for _ in range(200):
            m = 0.5 * (lo + hi)
            fm = f(m)
            if flo * fm <= 0.0:
                hi = m
            else:
                lo = m
                flo = fm
        return 0.5 * (lo + hi)

    E0g = HBAR**2 * KAPPA0**2 / (2.0 * M_E)

    def fe(x):
        S, P = sp(x)
        return alpha * (S + P) - 1.0        # even branch

    def fo(x):
        S, P = sp(x)
        return alpha * (S - P) - 1.0        # odd branch

    xp = root(fe)
    xm = root(fo)
    ev = -xp if xp is not None else None
    od = -xm if xm is not None else None
    return ev, od


# ---- T1: single delta well, free-space analytic vs converged numeric ----
sec("TEST T1:  SINGLE DELTA WELL  E = -m g^2 / (2 hbar^2)")
E_free = -E_BIND
ks1, resid1 = kappa_s_ring(LZ_T1, KAPPA0)
E_ring_ana = -HBAR**2 * ks1**2 / (2.0 * M_E)
E_num = single_delta_quant(LZ_T1, G, N_SUM_CONV)
rel1 = abs(E_num - E_free) / abs(E_free)
n1 = np.arange(-(N_PW // 2), N_PW // 2 + 1)
T1d = (HBAR * 2.0 * np.pi * n1 / LZ_T1) ** 2 / (2.0 * M_E)
H1s = np.diag(T1d) - (G / LZ_T1) * np.ones((len(n1), len(n1)))   # SINGLE delta well
E_pw41 = float(np.linalg.eigvalsh(H1s)[0])
print("setup: ring L_z = %.1f nm (kappa0*L_z = %.1f), kappa0 = %.3e 1/m" % (LZ_T1 * 1e9, KAPPA0 * LZ_T1, KAPPA0))
print("analytic free space   E = -m g^2/(2 hbar^2)      = %s eV" % sci(E_free / EV))
print("analytic ring         kappa*tanh(kappa L_z/2)=kappa0 -> E = %s eV (tanh saturation shift %.2e rel)"
      % (sci(E_ring_ana / EV), abs(E_ring_ana - E_free) / abs(E_free)))
print("   inverted-form check: |x - atanh(y/x)| = %.2e (math.atanh; x=kappa L_z/2, y=kappa0 L_z/2)" % resid1)
print("numeric (converged momentum sum, N_SUM = %d): E = %s eV" % (N_SUM_CONV, sci(E_num / EV)))
print("   sum-truncation error estimate: 2*kappa0*L_z/(pi^2*N_SUM) ~ %.2e rel" % (2 * KAPPA0 * LZ_T1 / (math.pi**2 * N_SUM_CONV)))
print("reference N=%d plane-wave matrix eigenvalue: E = %s eV (N=41 truncation gives a variational"
      % (N_PW, sci(E_pw41 / EV)))
print("   upper bound, i.e. a less-bound state; convergence columns below quantify this)")
print("[T1] |E_num - E_free|/|E_free| = %.3e   threshold %.1e -> %s"
      % (rel1, TOL_T1_SINGLE, "PASS" if rel1 < TOL_T1_SINGLE else "FAIL"))
t1_pass = rel1 < TOL_T1_SINGLE

# ---- scan (L, L_z) ----
sec("SCAN (L, L_z):  DeltaE AND S_ov  (no bonding-direction claim)")
print("DeltaE(N=41): registered basis per task. DeltaE_conv: converged secular solver")
print("(same Hamiltonian, N_SUM = %d plane waves, negative-energy roots; 'none' = no bound" % N_SUM_CONV)
print("state of that parity, i.e. the lowest state of that parity lies in the continuum).")
print("")
print("%-6s %-8s %-9s %-10s %-14s %-14s %-14s %-12s" %
      ("L/L_z", "L_z", "min-arc", "kappa*arc", "DeltaE(N41) eV", "E_even eV", "E_odd eV", "S_ov"))
scan_rows = []
for L_z in LZ_SCAN:
    ks, _ = kappa_s_ring(L_z, KAPPA0)
    for fl in FL_SCAN:
        L = fl * L_z
        ev, od, comm, w0, w1 = two_delta_split(L_z, L, G, N_PW)
        dE = ev - od
        ev_c, od_c = two_delta_converged(L_z, L, G, N_SUM_CONV)
        z = np.linspace(0.0, L_z, 200001)
        pA = psi_ring(L_z, ks, z, 0.0)
        pB = psi_ring(L_z, ks, z, L)
        S_num = float(np.trapezoid(pA * pB, z))
        Hs, ns = build_ham(L_z, 0.0, G, N_PW)
        _, vs = np.linalg.eigh(Hs)
        c = vs[:, 0]
        S_pw = abs(np.sum(np.abs(c) ** 2 * np.exp(-1j * 2.0 * np.pi * ns * L / L_z)))
        arc_min = min(L, L_z - L)
        exmin = math.exp(-KAPPA0 * arc_min)
        ratio = abs(dE / EV) / exmin
        scan_rows.append((fl, L_z, dE, ev, od, S_num, S_pw, arc_min, exmin, ratio, comm,
                          ev_c, od_c))
        print("%-6.1f %-8.1f %-9.2f %-10.3f %-14s %-14s %-14s %-12s"
              % (fl, L_z * 1e9, arc_min * 1e9, KAPPA0 * arc_min, sci(dE / EV, 6),
                 sci(ev / EV, 6), sci(od / EV, 6), sci(S_num, 6)))
print("")
print("converged negative-energy roots (secular solver) and parity-commutation check:")
e_scale = max((HBAR * 2.0 * np.pi * (N_PW // 2) / Lz) ** 2 / (2.0 * M_E) for Lz in LZ_SCAN)
print("max |H P - P H| = %.3e J ; /energy scale %.3e -> ratio %.2e (threshold %.1e) %s"
      % (max(r[10] for r in scan_rows), e_scale, max(r[10] for r in scan_rows) / e_scale,
         TOL_COMM, "OK" if max(r[10] for r in scan_rows) / e_scale < TOL_COMM else "FAIL"))
comm_ok = max(r[10] for r in scan_rows) / e_scale < TOL_COMM
print("%-6s %-8s %-16s %-16s %-14s" % ("L/L_z", "L_z[nm]", "E_even_conv [eV]", "E_odd_conv [eV]", "bound?"))
for r in scan_rows:
    ev_c, od_c = r[11], r[12]
    def fmtE(x):
        return "none" if x is None else sci(x / EV, 6)
    status = []
    status.append("even:" + ("bound" if ev_c is not None else "unbound"))
    status.append("odd:" + ("bound" if od_c is not None else "unbound"))
    print("%-6.1f %-8.1f %-16s %-16s %-14s" % (r[0], r[1] * 1e9, fmtE(ev_c), fmtE(od_c), ",".join(status)))
print("")
print("S_ov cross-check: Parseval momentum sum of the N=%d truncated isolated ground state vs" % N_PW)
print("the converged integral (difference = N=41 basis truncation): max abs diff = %.3e"
      % max(abs(r[5] - r[6]) for r in scan_rows))
print("internal symmetry check (ring arc relabeling): DeltaE(0.9 L_z) vs DeltaE(0.1 L_z):")
sym_dev = 0.0
for L_z in LZ_SCAN:
    d90 = [r[2] for r in scan_rows if r[1] == L_z and r[0] == 0.9][0]
    d10 = [r[2] for r in scan_rows if r[1] == L_z and r[0] == 0.1][0]
    dev = abs(d90 - d10) / max(abs(d90), 1e-300)
    sym_dev = max(sym_dev, dev)
    print("   L_z = %.1f nm: DeltaE(0.9) = %s eV, DeltaE(0.1) = %s eV, rel dev = %.2e"
          % (L_z * 1e9, sci(d90 / EV), sci(d10 / EV), dev))
sym_ok = sym_dev < TOL_SYM
print("   threshold %.1e -> %s" % (TOL_SYM, "OK" if sym_ok else "FAIL"))
print("")
print("per-point tunneling factors (dimensionless) and the logged quantitative relation:")
print("%-6s %-8s %-14s %-14s %-16s %-14s" %
      ("L/L_z", "L_z[nm]", "exp(-k*arc)", "exp(-k*L)", "exp(-k*(L_z-L))", "|DE(N41)|/exp"))
for r in scan_rows:
    L = r[0] * r[1]
    print("%-6.1f %-8.1f %-14s %-14s %-16s %-14s" %
          (r[0], r[1] * 1e9, sci(r[8], 6), sci(math.exp(-KAPPA0 * L), 6),
           sci(math.exp(-KAPPA0 * (r[1] - L)), 6), sci(r[9], 6)))
print("")
print("DeltaE basis convergence at N = %d / 81 / 161 plane waves (DeltaE in eV):" % N_PW)
for L_z in LZ_SCAN:
    for fl in FL_SCAN:
        L = fl * L_z
        e41 = [r[2] for r in scan_rows if r[1] == L_z and r[0] == fl][0]
        e81 = two_delta_split(L_z, L, G, 81)[:2]
        e161 = two_delta_split(L_z, L, G, 161)[:2]
        print("   L/L_z %.1f, L_z %.1f nm: %s / %s / %s"
              % (fl, L_z * 1e9, sci(e41 / EV), sci((e81[0] - e81[1]) / EV), sci((e161[0] - e161[1]) / EV)))
print("")
print("LOGGED RELATION (quantitative only): |DeltaE| tracks the tunneling factor")
print("exp(-kappa*arc_min) with kappa = sqrt(2 m |E_bind,single|)/hbar; pointwise ratios")
print("are printed above. Whether any point constitutes 'bonding' is a statement about")
print("the spectrum of the specified Hamiltonian only; per 5.1(d)/8.10 it is NOT inferred")
print("from topology, and no directional conclusion is issued here. For L/L_z = 0.9 vs 0.1")
print("the arc multiset is the same -> identical spectra (symmetry check above).")

# ---- T2: large-separation exponential decay fit (converged solver) ----
sec("TEST T2:  LARGE-SEPARATION LIMIT  DeltaE -> 0 (EXPONENTIAL FIT)")
print("wells at 0 and L_z/2 (equal arcs); DeltaE from the CONVERGED secular solver")
print("(the N=41 splitting falls below the finite-basis noise floor at kappa*arc >~ 8;")
print("both values are printed for comparison).")
gaps, dEs = [], []
print("%-10s %-10s %-12s %-16s %-16s" % ("L_z [nm]", "gap [nm]", "kappa*gap", "|DE| conv [eV]", "DE(N41) [eV]"))
for L_z in LZ_T2_GRID:
    L = 0.5 * L_z
    ev, od, _, _, _ = two_delta_split(L_z, L, G, N_PW)
    ev_c, od_c = two_delta_converged(L_z, L, G, N_SUM_CONV)
    dE_c = ev_c - od_c
    gaps.append(0.5 * L_z)
    dEs.append(abs(dE_c))
    print("%-10.1f %-10.2f %-12.3f %-16s %-16s" % (L_z * 1e9, 0.5 * L_z * 1e9, KAPPA0 * 0.5 * L_z,
                                                   sci(abs(dE_c) / EV), sci((ev - od) / EV)))
mono = all(dEs[i] > dEs[i + 1] for i in range(len(dEs) - 1))
slope, inter = np.polyfit(np.array(gaps), np.log(np.array(dEs)), 1)
lam_fit = -1.0 / slope
lam_ref = 1.0 / KAPPA0
pred = slope * np.array(gaps) + inter
ss_res = float(np.sum((np.log(np.array(dEs)) - pred) ** 2))
ss_tot = float(np.sum((np.log(np.array(dEs)) - np.mean(np.log(np.array(dEs)))) ** 2))
r2 = 1.0 - ss_res / ss_tot
dev_t2 = abs(lam_fit - lam_ref) / lam_ref
print("fit ln|DeltaE| = a + b*gap:  b = %.6e 1/m  -> decay length lambda = 1/|b| = %.4f nm"
      % (slope, lam_fit * 1e9))
print("reference 1/kappa0 = %.4f nm ; relative dev = %.3e ; fit R^2 = %.8f ; monotone decay: %s"
      % (lam_ref * 1e9, dev_t2, r2, mono))
t2_pass = (dev_t2 < TOL_T2_DECAY) and mono
print("[T2] threshold |lambda-1/kappa|/kappa < %.2f AND monotone decay -> %s"
      % (TOL_T2_DECAY, "PASS" if t2_pass else "FAIL"))

# =====================================================================
sec("VERDICTS")
print("T1  single delta well, numeric vs -m g^2/(2 hbar^2) (rel, tol %.1e): %s (%.3e)"
      % (TOL_T1_SINGLE, "PASS" if t1_pass else "FAIL", rel1))
print("T2  double-well large-separation exponential decay, converged solver (tol %.2f + monotone): %s (lambda = %.4f nm vs 1/kappa = %.4f nm)"
      % (TOL_T2_DECAY, "PASS" if t2_pass else "FAIL", lam_fit * 1e9, lam_ref * 1e9))
print("C1  sphere sublevel areas {h<eps} ~ pi*eps^2/4 inside D^2, monotone (tol %.2f): %s"
      % (TOL_SUBLEVEL, "PASS" if sub_ok else "FAIL"))
print("C2  ring arc-relabeling symmetry DeltaE(0.9L_z)=DeltaE(0.1L_z) (tol %.1e): %s (%.2e)"
      % (TOL_SYM, "PASS" if sym_ok else "FAIL", sym_dev))
print("C3  parity operator check [H,P]=0 (rel, tol %.1e): %s"
      % (TOL_COMM, "PASS" if comm_ok else "FAIL"))
overall = "PASS" if (t1_pass and t2_pass and sub_ok and sym_ok and comm_ok) else "FAIL"
print("OVERALL: %s" % overall)
print("EVIDENCE LEVEL: MODEL RESULT (v1.4 8.10 mapping layer; designated background;")
print("no visibility claim; no 'unique self-consistent form' claim; no bonding-direction claim).")
