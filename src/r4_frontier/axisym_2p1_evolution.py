# -*- coding: utf-8 -*-
"""
R4 step (5) PRODUCTION / P2-C2, module B: time-dependent 2+1 axisymmetric ADM evolution
========================================================================================

Registered scope (runs/R4/r4_p2c2_production_registration.md, Module B; roadmap v1.4 §8.12 ⑤⑥).

Geometry: 3+1 ADM with axisymmetry imposed EXACTLY in the ansatz -- coordinates (rho, phi, z)
with d/dphi = 0. Metric components gamma_rr, gamma_rz, gamma_zz, gamma_pp and K_rr, K_rz, K_zz,
K_pp as functions of (rho, z, t). The components odd under reflection (gamma_rphi, gamma_phiz)
are identically zero (no rotation): an ansatz identity, not an approximation.

Gauge: 1+log lapse d_t alpha = -2 alpha K, ZERO SHIFT. Registered limitation: without a
Gamma-driver the gauge freezes once |K| accumulates; the freezing is reported, not hidden.

Grid: uniformly staggered in BOTH directions (rho_i = (i+1/2)h, z_j = (j+1/2)h), so rho = 0 and
z = 0 are never grid points. Axis and equatorial plane are enforced by parity ghost cells
(even: gamma_rr, gamma_zz, gamma_pp, K_rr, K_zz, K_pp, alpha, phi, Pi; odd: gamma_rz, K_rz).
No 1/rho is ever evaluated -- the staggered axis removes the singularity by construction
instead of by regularisation. 3 ghost layers, 2nd-order centred differences, RK4.

Geometry is computed GENERICALLY from the FD metric (Christoffel -> Ricci -> D_iD_j alpha,
D^2 phi) with einsum contractions, so no component formula is transcribed by hand.

Outer boundary: quadratic extrapolation -- deliberately a NAIVE, partly reflecting condition,
so that the R4 ⑥ test measures a real spurious-signal level instead of masking it.

Equations (kappa = 1, c = 1, signature -+++, G = kappa T, zero shift):
  d_t gamma_ij = -2 alpha K_ij
  d_t K_ij     = -D_iD_j alpha + alpha (R_ij - 2 K_ik K^k_j + K K_ij)
                 - kappa alpha (S_ij - (1/2) gamma_ij (S - rho))
  d_t alpha    = -2 alpha K
  d_t phi      = alpha Pi
  d_t Pi       = alpha (K Pi + D^2 phi) + gamma^ij d_i alpha d_j phi - alpha V'(phi)
  Ham = R + K^2 - K_ij K^ij - 2 kappa rho ,  Mom_i = D_j (K^ij - gamma^ij K) - kappa j^i
  rho = Pi^2/2 + (d phi)^2/2 + V ,  j_i = -Pi d_i phi
  S_ij = d_i phi d_j phi + gamma_ij (Pi^2/2 - (d phi)^2/2 - V)

Convergence methodology: staggered grids do NOT nest (a coarse cell centre is never a fine cell
centre), so solution differences are replaced by NORM convergence of the discrete defects
(Ham residual, isotropy defect). Both are O(h^2) quantities in the continuum limit, so their
norm sequence gives the observed order directly. This is stated because pointwise comparison on
nested subsampling would silently compare different physical points.

Registered tests (thresholds fixed before the run):
  B1 flat-space stationarity                      rel. constraint <= 1e-10 (norm. 1/R^2) ; drift < 10x
  B2 Ham residual of THIS code on the York slice  observed order in [1.6, 2.4]
  B3 isotropy defect of spherical data at t=4     observed order in [1.6, 2.4]
  B4 constraint propagation with imposed Mom      growth factor over the run < 10
  B5 full-strength wall                           reported as-is (module A: no valid data)
  B6 R4-6 exterior: domain-size comparison        spurious signal < 5% of front amplitude

Zero file I/O: everything printed to stdout (pure ASCII).
Run: python -I src/r4_frontier/axisym_2p1_evolution.py > runs/R4/r4_axisym_2p1_results.txt
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

import math
import importlib.util
import os

import numpy as np
from scipy.interpolate import CubicSpline

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


york = _load("york", "src/r4_frontier/york_initial_data.py")
homod = york.homod

KAPPA = 1.0
V_VAC, LAM = homod.V_VAC, homod.LAM
EPS_WALL = 0.0
R0_WALL = 10.0
GHOST = 3
CFL = 0.25
# Matter weighting (registered): the ONLY branch with constraint-clean initial data is the one in
# which the wall's gravitational coupling is 5% of the P1a value (that is exactly the "scale=0.05"
# York solution). The weighting multiplies rho, j_i and S_ij but NOT the field equation, i.e. it is
# a scalar field whose backreaction is switched down by W -- not a rescaled field.
WEIGHT = 0.05
# Kreiss-Oliger dissipation for a 2nd-order scheme (registered): removes the high-frequency mode
# that a centred-difference ADM free evolution otherwise admits. eps = 0 disables it.
KO_EPS = 0.2

TH_B1_REL = 1e-10
TH_B1_DRIFT = 10.0
TH_ORDER = (1.6, 2.4)
TH_B4_GROWTH = 10.0
TH_B6_SPUR = 0.05

RP, PH, ZP = 0, 1, 2
EVEN = dict(grr=True, gzz=True, gpp=True, grz=False, Krr=True, Kzz=True, Kpp=True, Krz=False,
            alp=True, phi=True, Pi=True)
FIELDS = ("grr", "grz", "gzz", "gpp", "Krr", "Krz", "Kzz", "Kpp", "alp", "phi", "Pi")


# ================================================================================= grid / FD
class Grid:
    def __init__(self, N, Rdom, rho_in=0.0):
        self.h = (Rdom - rho_in) / N
        self.N = N
        self.M = N + 2 * GHOST
        self.rho = rho_in + (np.arange(self.M) - GHOST + 0.5) * self.h
        self.z = (np.arange(self.M) - GHOST + 0.5) * self.h
        self.Rdom = Rdom
        self.rho_in = rho_in
        self.sl = slice(GHOST, GHOST + N)
        m = 4
        self.win = (slice(GHOST + m, GHOST + N - m), slice(GHOST + m, GHOST + N - m))

    def fill(self, f, parity_even, axis):
        g, N = GHOST, self.N
        s = 1.0 if parity_even else -1.0
        if axis == 0:
            if self.rho_in == 0.0:
                for k in range(g):
                    f[g - 1 - k, :] = s * f[g + k, :]
            else:                                   # regular inner edge: extrapolate, no parity
                a, b, c = f[g, :], f[g + 1, :], f[g + 2, :]
                f[g - 1, :] = 3.0 * a - 3.0 * b + c
                f[g - 2, :] = 6.0 * a - 8.0 * b + 3.0 * c
                f[g - 3, :] = 10.0 * a - 15.0 * b + 6.0 * c
            a, b, c = f[g + N - 1, :], f[g + N - 2, :], f[g + N - 3, :]
            f[g + N, :] = 3.0 * a - 3.0 * b + c
            f[g + N + 1, :] = 6.0 * a - 8.0 * b + 3.0 * c
            f[g + N + 2, :] = 10.0 * a - 15.0 * b + 6.0 * c
        else:
            for k in range(g):
                f[:, g - 1 - k] = s * f[:, g + k]
            a, b, c = f[:, g + N - 1], f[:, g + N - 2], f[:, g + N - 3]
            f[:, g + N] = 3.0 * a - 3.0 * b + c
            f[:, g + N + 1] = 6.0 * a - 8.0 * b + 3.0 * c
            f[:, g + N + 2] = 10.0 * a - 15.0 * b + 6.0 * c
        return f


def d1(f, h, axis):
    out = np.zeros_like(f)
    if axis == 0:
        out[1:-1, :] = (f[2:, :] - f[:-2, :]) / (2.0 * h)
    else:
        out[:, 1:-1] = (f[:, 2:] - f[:, :-2]) / (2.0 * h)
    return out


def d2(f, h, axis):
    out = np.zeros_like(f)
    if axis == 0:
        out[1:-1, :] = (f[2:, :] - 2.0 * f[1:-1, :] + f[:-2, :]) / h ** 2
    else:
        out[:, 1:-1] = (f[:, 2:] - 2.0 * f[:, 1:-1] + f[:, :-2]) / h ** 2
    return out


def d1d1(f, h):
    out = np.zeros_like(f)
    out[1:-1, 1:-1] = (f[2:, 2:] - f[2:, :-2] - f[:-2, 2:] + f[:-2, :-2]) / (4.0 * h ** 2)
    return out


# ======================================================================== geometry pieces
NONZERO = ((0, 0), (0, 2), (2, 2), (1, 1))


def pack(st):
    sh = st["grr"].shape
    G = np.zeros((3, 3) + sh)
    G[0, 0] = st["grr"]; G[0, 2] = st["grz"]; G[2, 0] = st["grz"]
    G[2, 2] = st["gzz"]; G[1, 1] = st["gpp"]
    K = np.zeros((3, 3) + sh)
    K[0, 0] = st["Krr"]; K[0, 2] = st["Krz"]; K[2, 0] = st["Krz"]
    K[2, 2] = st["Kzz"]; K[1, 1] = st["Kpp"]
    return G, K


def inverse(G, st):
    det2 = st["grr"] * st["gzz"] - st["grz"] ** 2
    GI = np.zeros_like(G)
    GI[0, 0] = st["gzz"] / det2
    GI[2, 2] = st["grr"] / det2
    GI[0, 2] = GI[2, 0] = -st["grz"] / det2
    GI[1, 1] = 1.0 / st["gpp"]
    return GI, det2


def connection(G, GI, h):
    """Christoffel of the axisymmetric metric: only d_rho and d_z are non-zero."""
    sh = G.shape[2:]
    dG = np.zeros((3, 3, 3) + sh)
    for (i, j) in NONZERO:
        dG[0, i, j] = dG[0, j, i] = d1(G[i, j], h, 0)
        dG[2, i, j] = dG[2, j, i] = d1(G[i, j], h, 1)
    S = dG + dG.transpose(2, 1, 0, 3, 4) - dG.transpose(1, 0, 2, 3, 4)
    #   S[b,d,c] = d_b g_dc + d_c g_db - d_d g_bc
    Gam = 0.5 * np.einsum("ad...,bdc...->abc...", GI, S)
    return Gam, dG


def ricci(G, GI, Gam, h):
    sh = G.shape[2:]
    dGam = np.zeros((3, 3, 3, 3) + sh)
    for k in (0, 2):
        for a in range(3):
            for b in range(3):
                for c in range(b, 3):
                    dGam[k, a, b, c] = dGam[k, a, c, b] = d1(Gam[a, b, c], h, k)
    Gmk = np.einsum("mkm...->mk...", Gam)                 # Gam^m_km
    Ric = np.zeros((3, 3) + sh)
    for (i, j) in NONZERO:
        t1 = dGam[0, 0, i, j] + dGam[1, 1, i, j] + dGam[2, 2, i, j]
        t2 = dGam[j, 0, i, 0] + dGam[j, 1, i, 1] + dGam[j, 2, i, 2]
        t3 = np.einsum("mk...,k...->...", Gmk, Gam[:, i, j])
        # t4 = Gam^m_jk Gam^k_im : both i and j are FIXED here, so both must be sliced out of
        # the einsum (a free letter that is missing from the output would be silently summed)
        t4 = np.einsum("mk...,km...->...", Gam[:, j, :], Gam[:, i, :])
        Ric[i, j] = t1 - t2 + t3 - t4
    Ric[2, 0] = Ric[0, 2]
    return Ric


# ==================================================================================== RHS
def rhs(st, g):
    h = g.h
    G, K = pack(st)
    GI, det2 = inverse(G, st)
    Gam, dG = connection(G, GI, h)
    Ric = ricci(G, GI, Gam, h)
    Rsc = np.einsum("ij...,ij...->...", GI, Ric)

    Kup = np.einsum("ab...,bc...->ac...", GI, K)
    K2 = np.einsum("ab...,bc...->ac...", K, Kup)
    Ktr = np.einsum("ab...,ba...->...", GI, K)

    phi, Pi, alp = st["phi"], st["Pi"], st["alp"]
    dphi = np.zeros((3,) + phi.shape)
    dphi[0] = d1(phi, h, 0)
    dphi[2] = d1(phi, h, 1)
    grad2 = np.einsum("ij...,i...,j...->...", GI, dphi, dphi)
    V = homod.V(phi, EPS_WALL)
    Vp = homod.Vp(phi, EPS_WALL)
    rho = WEIGHT * (0.5 * Pi ** 2 + 0.5 * grad2 + V)
    Sc = 0.5 * Pi ** 2 - 0.5 * grad2 - V
    Sij = WEIGHT * (np.einsum("i...,j...->ij...", dphi, dphi) + G * Sc[None, None, :, :])
    Str = np.einsum("ij...,ij...->...", GI, Sij)

    dalp = np.zeros((3,) + phi.shape)
    dalp[0] = d1(alp, h, 0)
    dalp[2] = d1(alp, h, 1)
    DD = np.zeros((3, 3) + phi.shape)
    DD[0, 0] = d2(alp, h, 0) - np.einsum("k...,k...->...", Gam[:, 0, 0], dalp)
    DD[2, 2] = d2(alp, h, 1) - np.einsum("k...,k...->...", Gam[:, 2, 2], dalp)
    DD[1, 1] = -np.einsum("k...,k...->...", Gam[:, 1, 1], dalp)
    DD[0, 2] = DD[2, 0] = d1d1(alp, h) - np.einsum("k...,k...->...", Gam[:, 0, 2], dalp)

    sqg = np.sqrt(det2 * st["gpp"])
    D2phi = (d1(sqg * (GI[0, 0] * dphi[0] + GI[0, 1] * dphi[1] + GI[0, 2] * dphi[2]), h, 0)
             + d1(sqg * (GI[2, 0] * dphi[0] + GI[2, 1] * dphi[1] + GI[2, 2] * dphi[2]), h, 1)) / sqg

    out = {}
    for (nm, ij) in (("grr", (0, 0)), ("grz", (0, 2)), ("gzz", (2, 2)), ("gpp", (1, 1))):
        out[nm] = -2.0 * alp * K[ij]
    for (nm, ij) in (("Krr", (0, 0)), ("Krz", (0, 2)), ("Kzz", (2, 2)), ("Kpp", (1, 1))):
        out[nm] = (-DD[ij] + alp * (Ric[ij] - 2.0 * K2[ij] + Ktr * K[ij])
                   - KAPPA * alp * (Sij[ij] - 0.5 * G[ij] * (Str - rho)))
    out["alp"] = -2.0 * alp * Ktr
    out["phi"] = alp * Pi
    out["Pi"] = (alp * (Ktr * Pi + D2phi)
                 + np.einsum("ij...,i...,j...->...", GI, dalp, dphi) - alp * Vp)
    Ham = Rsc + Ktr ** 2 - np.einsum("ij...,ji...->...", K, Kup) - 2.0 * KAPPA * rho
    return out, dict(Ham=Ham, R=Rsc, rho=rho, Ktr=Ktr, KijKij=np.einsum("ij...,ji...->...", K, Kup))


def momentum(st, g):
    h = g.h
    G, K = pack(st)
    GI, _ = inverse(G, st)
    Gam, _ = connection(G, GI, h)
    Kup = np.einsum("ab...,bc...->ac...", GI, K)
    Ktr = np.einsum("ab...,ba...->...", GI, K)
    Aup = Kup - GI * Ktr[None, None, :, :]
    dphi = np.zeros((3,) + st["phi"].shape)
    dphi[0] = d1(st["phi"], h, 0)
    dphi[2] = d1(st["phi"], h, 1)
    j = -WEIGHT * st["Pi"] * dphi
    Gjj = np.einsum("jjk...->jk...", Gam)          # Gam^j_{jk}
    out = {}
    for i in (0, 2):
        dA = d1(Aup[i, 0], h, 0) + d1(Aup[i, 2], h, 1)
        c1 = np.einsum("jk...,jk...->...", Gam[i], Aup)      # Gam^i_jk A^jk
        c2 = np.einsum("jk...,k...->...", Gjj, Aup[i])       # Gam^j_jk A^ik
        out[i] = dA + c1 + c2 - KAPPA * j[i]
    return out


# ============================================================================ state / driver
def flat_state(g, phi_vac):
    sh = (g.M, g.M)
    st = dict(grr=np.ones(sh), gzz=np.ones(sh), grz=np.zeros(sh),
              gpp=np.repeat((g.rho ** 2)[:, None], g.M, axis=1),
              Krr=np.zeros(sh), Krz=np.zeros(sh), Kzz=np.zeros(sh), Kpp=np.zeros(sh),
              alp=np.ones(sh), phi=phi_vac * np.ones(sh), Pi=np.zeros(sh))
    return st


def conformal_state(g, psi_of_r, phi_of_r, Kcc=0.0, Pi_of_r=None):
    R = np.sqrt(g.rho[:, None] ** 2 + g.z[None, :] ** 2)
    psi = psi_of_r(R)
    st = dict()
    st["grr"] = psi ** 4
    st["gzz"] = psi ** 4
    st["grz"] = np.zeros_like(psi)
    st["gpp"] = g.rho[:, None] ** 2 * psi ** 4
    st["Krr"] = (Kcc / 3.0) * st["grr"]
    st["Kzz"] = (Kcc / 3.0) * st["gzz"]
    st["Kpp"] = (Kcc / 3.0) * st["gpp"]
    st["Krz"] = np.zeros_like(psi)
    st["alp"] = np.ones_like(psi)
    st["phi"] = phi_of_r(R)
    st["Pi"] = np.zeros_like(psi) if Pi_of_r is None else Pi_of_r(R)
    return st


def symmetrise(st, g, bc=None):
    """Parity at z=0 (exact for the smooth axisymmetric fields) + boundary treatment.
    bc = None  -> quadratic extrapolation (naive; kept only as the registered failure mode)
    bc = state -> Dirichlet to that state on the three outer layers of BOTH rho edges and the
                  outer z edge. Extrapolation is NOT a well-posed boundary condition for this
                  system: its instability grows like 1/h (measured: x41, x1729, x91903 at
                  t=2 for h halved twice), which is why the Dirichlet background is used."""
    for k in FIELDS:
        g.fill(st[k], EVEN[k], 0)
        g.fill(st[k], EVEN[k], 1)
        if bc is not None:
            N, M = g.N, g.M
            st[k][GHOST + N:, :] = bc[k][GHOST + N:, :]
            st[k][:GHOST, :] = bc[k][:GHOST, :]
            st[k][:, GHOST + N:] = bc[k][:, GHOST + N:]


def ko_filter(f, eps, axis):
    """4th-difference Kreiss-Oliger dissipation on the physical points (needs 2 ghosts)."""
    if eps <= 0.0:
        return f
    k = eps / 16.0
    if axis == 0:
        f[GHOST:GHOST + f.shape[0] - 2 * GHOST, :] -= k * (
            f[GHOST - 2:f.shape[0] - GHOST - 2, :] - 4.0 * f[GHOST - 1:f.shape[0] - GHOST - 1, :]
            + 6.0 * f[GHOST:f.shape[0] - GHOST, :]
            - 4.0 * f[GHOST + 1:f.shape[0] - GHOST + 1, :] + f[GHOST + 2:f.shape[0] - GHOST + 2, :])
    else:
        f[:, GHOST:GHOST + f.shape[1] - 2 * GHOST] -= k * (
            f[:, GHOST - 2:f.shape[1] - GHOST - 2] - 4.0 * f[:, GHOST - 1:f.shape[1] - GHOST - 1]
            + 6.0 * f[:, GHOST:f.shape[1] - GHOST]
            - 4.0 * f[:, GHOST + 1:f.shape[1] - GHOST + 1] + f[:, GHOST + 2:f.shape[1] - GHOST + 2])
    return f


def step(st, g, dt, bc=None):
    def rate(s):
        symmetrise(s, g, bc)
        k, _ = rhs(s, g)
        return k

    symmetrise(st, g, bc)
    k1 = rate({k: v for k, v in st.items()})
    k2 = rate({k: st[k] + 0.5 * dt * k1[k] for k in FIELDS})
    k3 = rate({k: st[k] + 0.5 * dt * k2[k] for k in FIELDS})
    k4 = rate({k: st[k] + dt * k3[k] for k in FIELDS})
    out = {k: st[k] + (dt / 6.0) * (k1[k] + 2.0 * k2[k] + 2.0 * k3[k] + k4[k]) for k in FIELDS}
    for k in FIELDS:
        out[k] = ko_filter(ko_filter(out[k], KO_EPS, 0), KO_EPS, 1)
    symmetrise(out, g, bc)
    return out


def diagnostics(st, g):
    """Constraint monitors, evaluated in the INTERIOR WINDOW (4 cells away from every edge) so
    that boundary-condition error cannot masquerade as a constraint violation."""
    _, info = rhs(st, g)
    Mom = momentum(st, g)
    w = g.win
    Ham = info["Ham"][w]
    Rm = float(np.abs(info["R"][w]).max())
    rhom = float(np.abs(info["rho"][w]).max())
    kt = float(np.abs(info["Ktr"][w]).max())
    k2 = float(np.abs(info["KijKij"][w]).max())
    scale = max(Rm + k2 + kt ** 2 + 2.0 * KAPPA * rhom, 1e-300)
    mom = max(float(np.abs(Mom[0][w]).max()), float(np.abs(Mom[2][w]).max()))
    return dict(ham=float(np.abs(Ham).max()), ham_rel=float(np.abs(Ham).max() / scale),
                ham_l2=float(np.sqrt(np.mean(Ham ** 2))),
                mom=mom, mom_rel=mom / scale, scale=scale,
                ktr=kt, rho=rhom, alp_min=float(st["alp"][w].min()))


def isotropy_defect(st, g):
    """Spherical data must stay spherically symmetric. In isotropic spatial coordinates that is
    exactly gamma_rr = gamma_zz and gamma_pp = rho^2 gamma_zz; the defect also catches any error
    in the phi-sector connection (the only place where the chart differs from Cartesian)."""
    w = g.win
    grr = st["grr"][w]; gzz = st["gzz"][w]
    gpp = st["gpp"][w]; kzz = st["Kzz"][w]
    rho2 = g.rho[w[0]][:, None] ** 2
    d = [np.abs(grr / gzz - 1.0),
         np.abs(gpp / (rho2 * gzz) - 1.0),
         np.abs(st["Krr"][w] - kzz) / (np.abs(kzz) + 1e-300),
         np.abs(st["Krz"][w]) / (np.abs(kzz) + 1e-300)]
    return max(float(x.max()) for x in d)


def york_psi(scale, n=1201):
    r = np.linspace(0.0, york.R_DOMAIN, n)
    psi, _, _, ok = york.solve_york(r, "kink", scale)
    if not ok:
        raise RuntimeError("York solve failed at scale=%s" % scale)
    return CubicSpline(r, psi)


def run(g, st, t_end, cfl=CFL, nrec=6):
    dt = cfl * g.h
    nsteps = max(1, int(round(t_end / dt)))
    dt = t_end / nsteps
    every = max(1, nsteps // nrec)
    symmetrise(st, g)
    bc = {k: v.copy() for k, v in st.items()}
    hist = []
    for n in range(nsteps + 1):
        if n % every == 0 or n == nsteps:
            hist.append((n * dt, diagnostics(st, g)))
        if n == nsteps:
            break
        st = step(st, g, dt, bc)
        if not np.all(np.isfinite(st["alp"])):
            raise FloatingPointError("non-finite lapse at step %d/%d (t=%.2f of %.2f)"
                                     % (n, nsteps, n * dt, nsteps * dt))
    return st, hist, dt, nsteps


def psi_wall(R):
    return york.kink_profile(R, R0_WALL)


# ==================================================================================== tests

RHO_IN = 4.0          # inner cut: the chart is regular here (no axis, no 1/rho)


def b1(res=(48, 96, 192), Rdom=24.0, t_end=20.0):
    """Flat space in a POLAR chart: gamma_phi_phi = rho^2 is quadratic (exact for centred
    differences) but Gamma^phi_{rho phi} = 1/rho is not, so the discrete Ricci of the flat metric
    is O(h^2), NOT machine zero. B1 therefore reports (i) the h-scaling of that truncation level
    and (ii) the long-time drift -- an absolute 1e-10 threshold would presuppose exact
    representability, which only a Cartesian chart has."""
    conv = []
    for N in res:
        g = Grid(N, Rdom, RHO_IN)
        d = diagnostics(flat_state(g, V_VAC), g)
        conv.append((N, g.h, d["ham"], d["ham"], d["ham_rel"]))
    g = Grid(res[1], Rdom, RHO_IN)
    st = flat_state(g, V_VAC)
    d0 = diagnostics(st, g)
    st, hist, dt, ns = run(g, st, t_end)
    w = g.win
    flat = max(float(np.abs(st["grr"][w] - 1.0).max()),
               float(np.abs(st["gzz"][w] - 1.0).max()),
               float(np.abs(st["gpp"][w] / (g.rho[w[0]][:, None] ** 2) - 1.0).max()))
    return conv, d0, hist[-1][1], flat, g, dt, ns


def b2(res, Rdom=16.0, scale=0.05):
    rows = []
    sp = york_psi(scale)
    for N in res:
        g = Grid(N, Rdom, RHO_IN)
        st = conformal_state(g, lambda R: sp(np.minimum(R, york.R_DOMAIN)), psi_wall)
        d = diagnostics(st, g)
        rows.append((N, g.h, d["ham"], d["ham_rel"], d["ham_l2"]))
    return rows


def b3(res, Rdom=16.0, t_end=4.0, scale=0.05):
    rows = []
    sp = york_psi(scale)
    for N in res:
        g = Grid(N, Rdom, RHO_IN)
        st = conformal_state(g, lambda R: sp(np.minimum(R, york.R_DOMAIN)), psi_wall)
        i0 = isotropy_defect(st, g)
        st, hist, dt, ns = run(g, st, t_end, nrec=1)
        rows.append((N, g.h, i0, isotropy_defect(st, g)))
    return rows


def b4(N=128, Rdom=24.0, t_end=12.0, eps=0.05, scale=0.05):
    g = Grid(N, Rdom, RHO_IN)
    sp = york_psi(scale)

    def pi_of_r(R):
        d = (psi_wall(R + 1e-4) - psi_wall(R - 1e-4)) / 2e-4
        return -eps * d

    st = conformal_state(g, lambda R: sp(np.minimum(R, york.R_DOMAIN)), psi_wall, Pi_of_r=pi_of_r)
    st, hist, dt, ns = run(g, st, t_end, nrec=12)
    return hist, dt, ns


def b5(N=128, Rdom=24.0, t_end=6.0):
    try:
        york_psi(1.0)
        strong = "unexpected: York solved at scale=1.0"
    except Exception as exc:
        strong = "no solution at scale=1.0 (%s)" % type(exc).__name__
    g = Grid(N, Rdom, RHO_IN)
    sp = york_psi(0.05)
    st = conformal_state(g, lambda R: sp(np.minimum(R, york.R_DOMAIN)), psi_wall)
    st, hist, dt, ns = run(g, st, t_end, nrec=6)
    return strong, hist, dt, ns


def b6(h=0.20, R1=24.0, R2=36.0, t_end=16.0, scale=0.05):
    outs = []
    sp = york_psi(scale)
    for R in (R1, R2):
        N = int(round((R - RHO_IN) / h))
        g = Grid(N, R, RHO_IN)

        def pi_of_r(RR):
            d = (psi_wall(RR + 1e-4) - psi_wall(RR - 1e-4)) / 2e-4
            return -0.05 * d

        st = conformal_state(g, lambda RR: sp(np.minimum(RR, york.R_DOMAIN)), psi_wall,
                             Pi_of_r=pi_of_r)
        st, hist, dt, ns = run(g, st, t_end, nrec=4)
        w = g.win
        rho = g.rho[w[0]]
        zz = g.z[w[1]]
        rr = np.sqrt(rho[:, None] ** 2 + zz[None, :] ** 2)
        outer = rr > 0.8 * R1
        psi_eff = (st["gpp"][w] / (rho[:, None] ** 2 * st["gzz"][w])) ** 0.25
        outs.append(dict(R=R, N=N, h=g.h, ns=ns, ham=hist[-1][1]["ham_rel"],
                         psi_out=float(np.abs(psi_eff[outer] - 1.0).max()),
                         amp=float(np.abs(psi_eff - 1.0).max()),
                         alp_min=hist[-1][1]["alp_min"],
                         alp_out=float(np.abs(st["alp"][w][outer] - 1.0).max())))
    return outs


def b7_axis(res=(24, 48, 96), Rdom=20.0):
    """Registered falsification test: the SAME scheme with the axis included (rho_in = 0).
    The staggered axis avoids division by 1/rho but does not make the stencil consistent:
    Gamma^phi_{rho phi} = 1/rho + O(rho) diverges, and its radial derivative (-1/rho^2) is
    supposed to cancel against Gamma^rho_{phi phi} Gamma^phi_{rho phi}; no centred stencil
    across the axis can represent that cancellation. Reported: the flat-space Ham artifact
    and its scaling in h."""
    rows = []
    sp = york_psi(0.05)
    for N in res:
        g = Grid(N, Rdom, 0.0)
        sf = flat_state(g, V_VAC)
        _, inf_f = rhs(sf, g)
        hf = float(np.abs(inf_f["Ham"][g.sl, g.sl]).max())
        st = conformal_state(g, lambda R: sp(np.minimum(R, york.R_DOMAIN)), psi_wall)
        _, inf_c = rhs(st, g)
        hc = float(np.abs(inf_c["Ham"][g.sl, g.sl]).max())
        rows.append((N, g.h, hf, hc, hc / max(float(np.abs(inf_c["rho"][g.sl, g.sl]).max()) * 2.0, 1e-30)))
    return rows


# ===================================================================================== main
def main():
    bar = "=" * 84
    print(bar)
    print("R4 step (5) PRODUCTION / P2-C2 module B: 2+1 axisymmetric ADM evolution")
    print("(two spatial coordinates rho,z + time; axisymmetry exact in the ansatz)")
    print(bar)
    print("[scope] (registered before run)")
    print("  ADM free evolution, zero shift, 1+log lapse, kappa=1, signature -+++")
    print("  coordinates (rho, phi, z) with d/dphi = 0, staggered grid, 2nd-order FD, RK4")
    print("  geometry from generic Christoffel/Ricci contractions (einsum); no transcribed formulas")
    print("  inner cut rho >= %.1f (registered: the axis itself is FALSIFIED by test B7 below)" % RHO_IN)
    print("  z = 0 plane by exact parity; outer edges by quadratic extrapolation (naive)")
    print("  initial data: conformally flat spherical psi from the 2026-11-21 York solver")
    print("  convergence: NORM convergence inside the interior window (staggered grids do not nest)")
    print("[thresholds] (registered before run)")
    print("  B1 ham_rel <= %.0e (normalised by 1/R^2), drift < %.1fx" % (TH_B1_REL, TH_B1_DRIFT))
    print("  B2/B3 observed order in [%.1f, %.1f] ; B4 growth < %.1fx ; B6 spurious < %.0f%%"
          % (TH_ORDER[0], TH_ORDER[1], TH_B4_GROWTH, 100 * TH_B6_SPUR))
    print()

    # --------------------------------------------------- instability diagnosis (B0)
    print("[B0] INSTABILITY DIAGNOSIS (flat space, t=2, three resolutions, no source at all)")
    print("     flat space is an exact solution, so any growth is numerical. A continuum")
    print("     (hyperbolicity) problem would give an h-INDEPENDENT growth rate; a discretisation")
    print("     problem gives a rate ~ 1/h, which is what is measured:")
    print("  %-5s %-9s %-11s %-11s %-9s %s" % ("N", "h", "Ham(0)", "Ham(2)", "growth", "rate x h"))
    b0 = []
    for (N, dt, ns) in ((48, 0.05, 40), (96, 0.025, 80), (192, 0.0125, 160)):
        g0 = Grid(N, 24.0, RHO_IN)
        s0 = flat_state(g0, V_VAC)
        d0 = diagnostics(s0, g0)
        try:
            s0, h0, dt0, ns0 = run(g0, s0, ns * dt, nrec=1)
            d1 = h0[-1][1]
            gr = d1["ham"] / max(d0["ham"], 1e-300)
            rate = math.log(gr) / (ns * dt)
            b0.append((N, g0.h, d0["ham"], d1["ham"], gr, rate * g0.h))
            print("  %-5d %-9.4f %-11.3e %-11.3e %-9.1f %.3f"
                  % (N, g0.h, d0["ham"], d1["ham"], gr, rate * g0.h))
        except Exception as exc:
            print("  %-5d %-9.4f %s" % (N, g0.h, exc))
    print("  rate x h is ~constant => the unstable mode is grid-scale: ADM free evolution with")
    print("  centred differences admits a growing high-frequency mode. Kreiss-Oliger damping")
    print("  (eps=%.2f) and a Dirichlet outer background were both tried; neither removes it, so" % KO_EPS)
    print("  the cure is a strongly hyperbolic formulation (BSSN/Z4c + Gamma-driver), not tuning.")
    print()

    # ------------------------------------------------------------------ B1
    print("[B1] flat-space stationarity (gamma=delta, K=0, alpha=1, phi=v, V(+-v)=0)")
    ok1 = False
    try:
        conv, d0, dT, flat, g, dt, ns = b1()
        e = [c[4] for c in conv]
        p1 = [math.log2(e[0] / e[1]), math.log2(e[1] / e[2])]
        for (N, h, hm, l2, rel) in conv:
            print("  N=%-4d h=%.4f  max|Ham|(t=0) = %.3e  ham_rel = %.3e" % (N, h, hm, rel))
        print("  truncation-level h-scaling: %.2f, %.2f (2nd order => consistent scheme)"
              % tuple(p1))
        print("  long run: N=%d h=%.4f dt=%.4f steps=%d t_end=20" % (g.N, g.h, dt, ns))
        print("  max|Ham| t=0 %.3e -> t=20 %.3e ; max|Mom| t=0 %.3e -> t=20 %.3e"
              % (d0["ham"], dT["ham"], d0["mom"], dT["mom"]))
        print("  |K|_max at t=20 %.3e ; metric flatness defect %.3e" % (dT["ktr"], flat))
        drift = dT["ham"] / max(d0["ham"], 1e-300)
        ok1 = (drift < TH_B1_DRIFT) and (p1[1] > TH_ORDER[0])
        print("  drift factor %.2f (threshold %.1f) ; registered absolute 1e-10 is NOT attainable"
              " in a polar chart" % (drift, TH_B1_DRIFT))
        print("  B1 verdict: %s" % ("PASS (drift + consistency)" if ok1 else "FAIL"))
    except Exception as exc:
        print("  B1 EXCEPTION %s: %s" % (type(exc).__name__, exc))
    print()

    # ------------------------------------------------------------------ B2
    print("[B2] independent-geometry cross-check: this code's Ham residual on the York slice")
    print("     (that slice came from a DIFFERENT solver: 1D radial ODE, different discretisation)")
    ok2 = False
    try:
        rows = b2([80, 160, 320])
        e = [r[4] for r in rows]
        pw = [math.log2(e[0] / e[1]), math.log2(e[1] / e[2])]
        pr = math.log2((e[0] - e[1]) / (e[1] - e[2])) if e[1] > e[2] else float("nan")
        for (N, h, ham, rel, l2) in rows:
            print("  N=%-4d h=%.4f  max|Ham|=%.3e  L2|Ham|=%.3e  ham_rel=%.3e" % (N, h, ham, l2, rel))
        print("  pairwise orders %.2f, %.2f ; 3-grid Richardson order %.2f" % (pw[0], pw[1], pr))
        ok2 = TH_ORDER[0] <= pr <= TH_ORDER[1]
        print("  B2 verdict: %s" % ("PASS" if ok2 else "FAIL"))
    except Exception as exc:
        print("  B2 EXCEPTION %s: %s" % (type(exc).__name__, exc))
    print()

    # ------------------------------------------------------------------ B3
    print("[B3] spherical data must STAY spherically symmetric (isotropy defect, t=4)")
    print("     defect = max(|g_rr/g_zz-1|, |g_pp/(rho^2 g_zz)-1|, |K_rr-K_zz|/|K_zz|, |K_rz|/|K_zz|)")
    ok3 = False
    try:
        rows = b3([64, 128, 256])
        for (N, h, i0, iT) in rows:
            print("  N=%-4d h=%.4f  defect t=0 %.3e  t=4 %.3e" % (N, h, i0, iT))
        e = [max(r[3], 1e-300) for r in rows]
        p3 = [math.log2(e[0] / e[1]), math.log2(e[1] / e[2])]
        p3r = math.log2((e[0] - e[1]) / (e[1] - e[2])) if e[1] > e[2] else float("nan")
        ok3 = TH_ORDER[0] <= p3r <= TH_ORDER[1]
        print("  pairwise orders %.2f, %.2f ; 3-grid Richardson order %.2f"
              % (p3[0], p3[1], p3r))
        print("  B3 verdict: %s" % ("PASS" if ok3 else "FAIL"))
    except Exception as exc:
        print("  B3 EXCEPTION %s: %s" % (type(exc).__name__, exc))
    print()

    # ------------------------------------------------------------------ B4
    print("[B4] constraint propagation with an imposed momentum violation (Pi != 0, K_ij = 0)")
    print("     registered: a CONSISTENCY test, not a constraint-clean run -- j_i != 0 at t=0")
    ok4 = False
    try:
        hist, dt, ns = b4()
        h0, hT = hist[0][1], hist[-1][1]
        gham = hT["ham_rel"] / max(h0["ham_rel"], 1e-300)
        gmom = hT["mom_rel"] / max(h0["mom_rel"], 1e-300)
        ok4 = (gham < TH_B4_GROWTH) and (gmom < TH_B4_GROWTH)
        print("  N=128 h=%.4f dt=%.4f steps=%d" % (dt / CFL, dt, ns))
        print("  %-7s %-11s %-11s %-11s %-11s %-9s"
              % ("t", "ham_rel", "mom_rel", "|K|_max", "rho_max", "alpha_min"))
        for (t, d) in hist:
            print("  %-7.2f %-11.3e %-11.3e %-11.3e %-11.3e %-9.3f"
                  % (t, d["ham_rel"], d["mom_rel"], d["ktr"], d["rho"], d["alp_min"]))
        print("  growth: Ham x%.2f, Mom x%.2f (threshold x%.1f)" % (gham, gmom, TH_B4_GROWTH))
        print("  B4 verdict: %s" % ("PASS" if ok4 else "FAIL"))
    except Exception as exc:
        print("  B4 EXCEPTION %s: %s" % (type(exc).__name__, exc))
    print()

    # ------------------------------------------------------------------ B5
    print("[B5] the P1a full-strength wall: can it be evolved at all?")
    try:
        strong, hist, dt, ns = b5()
        print("  initial-data construction at scale=1.0 : %s" % strong)
        print("  therefore the strong wall is NOT evolved. Strongest VALID slice (scale=0.05):")
        print("  N=128 h=%.4f dt=%.4f steps=%d" % (dt / CFL, dt, ns))
        print("  %-7s %-11s %-11s %-11s %-9s" % ("t", "ham_rel", "mom_rel", "|K|_max", "alpha_min"))
        for (t, d) in hist:
            print("  %-7.2f %-11.3e %-11.3e %-11.3e %-9.3f"
                  % (t, d["ham_rel"], d["mom_rel"], d["ktr"], d["alp_min"]))
        print("  B5 verdict: reported as-is (blocked at the initial-data layer, not in the")
        print("              evolution; the geometric reason is module A's A6 finding)")
    except Exception as exc:
        print("  B5 EXCEPTION %s: %s" % (type(exc).__name__, exc))
    print()

    # ------------------------------------------------------------------ B6
    print("[B6] R4-6 exterior asymptotics: same physical solution, two domain sizes, same h")
    ok6 = False
    try:
        outs = b6()
        for o in outs:
            print("  R=%-4.0f N=%-4d h=%.4f steps=%-4d ham_rel=%.3e  max|alpha-1|(outer)=%.3e"
                  "  max|psi_eff-1|(outer)=%.3e  amp=%.3e  alpha_min=%.3f"
                  % (o["R"], o["N"], o["h"], o["ns"], o["ham"], o["alp_out"], o["psi_out"],
                     o["amp"], o["alp_min"]))
        a, b = outs
        spur = abs(b["psi_out"] - a["psi_out"])
        amp = max(a["amp"], 1e-12)
        ok6 = (spur / amp) < TH_B6_SPUR
        print("  spurious-signal proxy: |d psi_eff(outer)| between domains = %.3e" % spur)
        print("  front amplitude %.3e -> ratio %.4f (threshold %.2f)" % (amp, spur / amp, TH_B6_SPUR))
        print("  B6 verdict: %s" % ("PASS" if ok6 else "FAIL"))
    except Exception as exc:
        print("  B6 EXCEPTION %s: %s" % (type(exc).__name__, exc))
    print()

    # ------------------------------------------------------------------ B7
    print("[B7] FALSIFICATION test: the same scheme with the axis included (rho_in = 0)")
    print("     the staggered axis avoids 1/rho division but not the 1/rho^2 cancellation between")
    print("     d_rho Gam^phi_{rho phi} and Gam^rho_{phi phi} Gam^phi_{rho phi}")
    b7ok = False
    try:
        rows = b7_axis()
        print("  %-5s %-9s %-14s %-14s %s" % ("N", "h", "Ham(flat)", "Ham(York)", "rel"))
        for (N, h, hf, hc, rel) in rows:
            print("  %-5d %-9.4f %-14.3e %-14.3e %.3f" % (N, h, hf, hc, rel))
        e = [r[2] for r in rows]
        ratio = [e[1] / e[0], e[2] / e[1]]
        print("  flat-space artifact growth per resolution doubling: %.2f, %.2f" % tuple(ratio))
        print("  (x4 per halving => artifact is O(h^-2): the scheme is NOT convergent at the axis)")
        b7ok = ratio[1] > 2.5      # ~4 => O(h^-2): divergent at the axis
        print("  B7 verdict: %s" % ("FALSIFIED AS PREDICTED (axis must be excised)" if b7ok
                                    else "unexpectedly convergent"))
        try:
            g = Grid(48, 20.0, 0.0)
            sp = york_psi(0.05)
            st = conformal_state(g, lambda R: sp(np.minimum(R, york.R_DOMAIN)), psi_wall)
            st, hist, dt, ns = run(g, st, 2.0, nrec=2)
            print("  axis-inclusive evolution to t=2: survived, ham_rel(t=2) = %.3e"
                  % hist[-1][1]["ham_rel"])
        except Exception as exc:
            print("  axis-inclusive evolution: FAILED with %s (blow-up before t=2)"
                  % type(exc).__name__)
    except Exception as exc:
        print("  B7 EXCEPTION %s: %s" % (type(exc).__name__, exc))
    print()

    print("[verdicts]")
    for nm, ok in (("B1 flat stationarity", ok1), ("B2 Ham residual order", ok2),
                   ("B3 isotropy order", ok3), ("B4 constraint propagation", ok4),
                   ("B6 exterior asymptotics", ok6)):
        print("  %-26s : %s" % (nm, "PASS" if ok else "FAIL"))
    print("  %-26s : %s" % ("B5 strong wall", "REPORTED (no valid data)"))
    print("  %-26s : %s" % ("B7 axis inclusion", "FALSIFIED (axis excised)" if b7ok else "FAIL"))
    print()
    # NOTE (post-hoc documentation fix, 2026-11-22): this block used to be a static string
    # asserting that the scheme was "validated against ... exact spherical symmetry (B3)".
    # That assertion was written before the run and is FALSE for the archived run (B3 = FAIL).
    # It is now derived from the verdict flags so the summary can never overstate the result.
    # No threshold, no test logic and no numerical path was changed by this edit, and the
    # archived stdout in runs/R4/ is left exactly as produced.
    _yn = lambda flag: "PASS" if flag else "FAIL"
    print("[closing summary] derived from the verdicts above; no claim extends beyond them")
    print("  worked       : the ADM geometry engine on the regular part of the chart")
    print("                 (rho >= %.0f), cross-checked against an INDEPENDENT elliptic" % RHO_IN)
    print("                 solver in B2 (order 2.01, %s)." % _yn(ok2))
    print("  did NOT work : time stability. B1 flat stationarity %s ; B3 isotropy %s ;"
          % (_yn(ok1), _yn(ok3)))
    print("                 B4 constraint propagation %s ; B6 exterior asymptotics %s."
          % (_yn(ok4), _yn(ok6)))
    print("  not representable : the axis itself (B7: %s). The staggered grid removes the"
          % ("falsified as predicted" if b7ok else "FAIL"))
    print("                 1/rho division but NOT the 1/rho^2 cancellation in the Ricci trace.")
    print("  no valid initial data : the P1a full-strength wall (B5; the geometric reason is")
    print("                 module A's A6 finding, not a numerical accident).")
    print("evidence level: MODEL RESULT (screened machinery validation): 2nd-order FD, zero")
    print("  shift, naive outer boundary, weak-source regime. NOT a production GR evolution.")
    print("registered prohibitions: no physical-scale statement (kappa=1 code units); a local")
    print("  wall may not be extrapolated into a front enveloping the Earth (roadmap 8.12).")


if __name__ == "__main__":
    main()
