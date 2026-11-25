# -*- coding: utf-8 -*-
"""DCC global convention registration module (conv v1, 2026-11-21, review-fix driven)

Single source of truth (B5 fix): the physical constants, column/bulk density
conversions, dimension assignments and beta-equilibrium solutions of all modules
are imported from this module. Do not duplicate constants inside individual
modules -- during v2, G0 and R1-B1 each kept their own copy, causing a factor-of-10
discrepancy in the n_e handoff (F-G0-9) that nobody noticed.

Dimension assignment (human-readable version in docs/conventions/dimensional_conventions_v1.md)
--------------------------------------------------------------------------
Electrons: D=2 (single subband). The reason is computable, not conventional: for
  a slab thickness L_z=1 fm the transverse subband spacing is
  E_sub = hbar*c*pi/L_z = 619.9 MeV, while E_F = 73.37 MeV, so only the n=1
  subband is occupied and the electrons obey the 2D dispersion n_2D = g k_F^2/(4 pi).
Nucleons: D=3 by default (HYB / ALL3D), D=2 as a parallel branch (ALL2D). The 3D
  assignment relies on the premise that "nucleons are in a nuclear bound state or
  a dynamical layer, rather than a hard-wall single-particle state"; it is in
  tension with the 204 MeV subband spacing of R1-B4, so ALL2D must be registered
  as a parallel branch rather than deleted.

Three conventions (MODES) and defaults
--------------------------------------
  ALL3D : electrons 3D + nucleons 3D   (historical v2 convention, kept for comparison)
  HYB   : electrons 2D + nucleons 3D   (default; electron dimensionality argued from
          E_sub, nucleons use the 3D EOS)
  ALL2D : electrons 2D + nucleons 2D   (fully quantized limit)

Any downstream quantity depending on X_p / mu_e / n_e / P(Sigma) must report the
MODES envelope, not a single-point value from one convention (B2 fix).

Units: energy MeV, length fm, density fm^-2 (areal) or fm^-3 (bulk); pressure
conversions are explicit.
"""
import math

# ---------------------------------------------------------------- registered constants
HBARC = 197.3269804          # MeV fm
HBAR = 1.054571817e-34       # J s
C = 2.99792458e8             # m/s
MEV_J = 1.602176634e-13      # J / MeV
AMU_KG = 1.6605390666e-27
M_N = 939.565                # MeV
M_P = 938.272
M_E = 0.511

# G0 registered inputs (sole source; must match configs/g0_prime*.json)
M_KG = 70.0
A_PERP = 1.0
M_BAR_AMU = 10.0
ZA = 0.522                   # electrons per baryon (Z/A)
Z_ION = 5
A_ION = 10.0
G_E = 2
LZ_FM = 1.0                  # areal-to-bulk density conversion convention (also the physical thickness)

# ------------------------------------------------------- column density and areal/bulk density
N_S = M_KG / (M_BAR_AMU * AMU_KG * A_PERP)      # m^-2   nuclear column density
N_B = M_KG / (AMU_KG * A_PERP)                  # m^-2   baryon column density
N_S_FM2 = N_S / 1e30
N_B_FM2 = N_B / 1e30
N_E_FM2 = ZA * N_B_FM2                          # fm^-2  electron areal density (main convention)
N_E_FM3 = N_E_FM2 / LZ_FM                       # fm^-3  equivalent bulk density
N_B_FM3 = N_B_FM2 / LZ_FM
N_NUC_FM3 = N_S_FM2 / LZ_FM
Z_EFF = ZA * M_BAR_AMU                          # electrons per nucleus = 5.22

# L_z = 1 fm makes the numerical values of fm^-2 and fm^-3 identical (0.0220);
# this is exactly the breeding ground for the factor-of-10 error in v2, where Z_eff
# (5.22 per nucleus) was multiplied by the baryon density (0.0422).
E_SUBBAND = math.pi * HBARC / LZ_FM             # 619.9 MeV transverse subband spacing

D_E = 2                     # electron dimensionality (single subband, see module header)
MODES = ("ALL3D", "HYB", "ALL2D")
DEFAULT_MODE = "HYB"

# ------------------------------------------------------------- unit conversions
J_PER_MEV_FM2 = MEV_J * 1e30        # J/m^2 per MeV/fm^2
J_PER_MEV_FM3 = MEV_J * 1e45        # J/m^3 per MeV/fm^3


def P_areal_to_Nm(P_mev_fm2):
    """Areal pressure MeV/fm^2 -> N/m"""
    return P_mev_fm2 * J_PER_MEV_FM2


def P_vol_to_Nm(P_mev_fm3, lz_fm=LZ_FM):
    """Bulk pressure MeV/fm^3 -> equivalent areal pressure N/m (times layer thickness)"""
    return P_mev_fm3 * J_PER_MEV_FM3 * (lz_fm * 1e-15)


# ----------------------------------------------------------------- Fermi wave vector
def kF_2(n2, g=G_E):
    """D=2: n = g k^2/(4 pi)"""
    return math.sqrt(4.0 * math.pi * n2 / g)


def kF_3(n3, g=G_E):
    """D=3: n = g k^3/(6 pi^2)  =>  (6 pi^2 n/g)^(1/3); for g=2, (3 pi^2 n)^(1/3)"""
    return (6.0 * math.pi ** 2 * n3 / g) ** (1.0 / 3.0)


# ------------------------------------------------------------- electron equation of state
def eos_e_2D(n2, g=G_E):
    """2D ultrarelativistic electron gas: u=(2/3) n E_F, P=u/2 (E_F=hbar c k_F)"""
    kF = kF_2(n2, g)
    EF = HBARC * kF
    u = (2.0 / 3.0) * n2 * EF          # MeV/fm^2
    return dict(kF=kF, EF=EF, u=u, P=u / 2.0, D=2)


def eos_e_3D(n3, g=G_E):
    """3D relativistic exact (Chandrasekhar integral); the UR limit automatically gives P/u=1/3"""
    p = HBARC * kF_3(n3, g)
    E = math.sqrt(p * p + M_E * M_E)
    lg = math.log((p + E) / M_E)
    hc3 = HBARC ** 3
    f = g / 2.0
    u = f * (p * (2 * p * p + M_E ** 2) * E - M_E ** 4 * lg) / (8 * math.pi ** 2 * hc3)
    P = f * (p * (2 * p * p - 3 * M_E ** 2) * E + 3 * M_E ** 4 * lg) / (24 * math.pi ** 2 * hc3)
    return dict(kF=p / HBARC, EF=E, u=u, P=P, D=3)


# ------------------------------------------------------------- nucleon equation of state
def eos_n_2D(n2, m, g=G_E):
    """2D nonrelativistic: u_kin=(1/2) n E_F, P=(2/D) u_kin = u_kin"""
    EF = HBARC ** 2 * kF_2(n2, g) ** 2 / (2.0 * m)
    u_kin = 0.5 * n2 * EF
    return dict(EF=EF, u_kin=u_kin, P=u_kin, u=n2 * m + u_kin, D=2)


def eos_n_3D(n3, m, g=G_E):
    """3D nonrelativistic: u_kin=(3/5) n E_F, P=(2/3) u_kin"""
    EF = HBARC ** 2 * kF_3(n3, g) ** 2 / (2.0 * m)
    u_kin = 0.6 * n3 * EF
    return dict(EF=EF, u_kin=u_kin, P=(2.0 / 3.0) * u_kin, u=n3 * m + u_kin, D=3)


# ------------------------------------------------------- beta equilibrium (three conventions)
def beta_eq(NB_areal, mode=DEFAULT_MODE, g=G_E):
    """Given baryon column density NB[fm^-2], solve for X_p; return all downstream quantities.

    Charge neutrality is treated consistently with dimensionality: D=3 uses the bulk
    density N/L_z, D=2 uses the areal density N.
    Beta equilibrium: mu_n = mu_p + mu_e.
    """
    if mode not in MODES:
        raise ValueError("mode must be one of %s" % (MODES,))
    dnuc = 2 if mode == "ALL2D" else 3
    de = 3 if mode == "ALL3D" else 2

    def state(X):
        Np = max(X * NB_areal, 1e-300)
        Nn = max((1.0 - X) * NB_areal, 1e-300)
        if dnuc == 3:
            sn = eos_n_3D(Nn / LZ_FM, M_N, g)
            sp = eos_n_3D(Np / LZ_FM, M_P, g)
            Pn, Pp = sn["P"] * LZ_FM, sp["P"] * LZ_FM      # MeV/fm^2
        else:
            sn = eos_n_2D(Nn, M_N, g)
            sp = eos_n_2D(Np, M_P, g)
            Pn, Pp = sn["P"], sp["P"]
        mun, mup = M_N + sn["EF"], M_P + sp["EF"]
        if de == 3:
            se = eos_e_3D(Np / LZ_FM, g)
            Pe, mue = se["P"] * LZ_FM, se["EF"]
        else:
            se = eos_e_2D(Np, g)
            Pe, mue = se["P"], se["EF"]
        return mun, mup, mue, Pn, Pp, Pe

    def f(X):
        mn_, mp_, me_, _, _, _ = state(X)
        return mn_ - mp_ - me_

    lo, hi = 1e-14, 1.0 - 1e-14
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        raise RuntimeError("no bracket: f(lo)=%.3e f(hi)=%.3e" % (flo, fhi))
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    X = 0.5 * (lo + hi)
    mun, mup, mue, Pn, Pp, Pe = state(X)
    n_e_areal = X * NB_areal
    P_tot = Pn + Pp + Pe
    return dict(mode=mode, X_p=X, X_n=1.0 - X, mu_n=mun, mu_p=mup, mu_e=mue,
                n_e_areal=n_e_areal, n_e_fm3=n_e_areal / LZ_FM,
                reduction=N_E_FM2 / n_e_areal,
                P_nuc_areal=Pn + Pp, P_e_areal=Pe, P_tot_areal=P_tot,
                P_nuc_Nm=P_areal_to_Nm(Pn + Pp), P_e_Nm=P_areal_to_Nm(Pe),
                P_tot_Nm=P_areal_to_Nm(P_tot), beta_res=f(X),
                D_nuc=dnuc, D_e=de)


def beta_envelope(nB_fm3=None, modes=MODES):
    """Beta-equilibrium envelope for the three dimensional conventions at the same bulk density"""
    nB = N_B_FM3 if nB_fm3 is None else nB_fm3
    NB = nB * LZ_FM
    return {m: beta_eq(NB, m) for m in modes}


def envelope_spread(env, key):
    vals = [env[m][key] for m in env]
    return min(vals), max(vals)


# --------------------------------------------------------- frozen state (G0 baseline)
def frozen_state():
    """G0 frozen state: electron gas at areal density N_E_FM2 (2D main convention + 3D comparison)"""
    e2 = eos_e_2D(N_E_FM2, G_E)
    e3 = eos_e_3D(N_E_FM3, G_E)
    return dict(n_areal=N_E_FM2, n_fm3=N_E_FM3,
                EF_2D=e2["EF"], EF_3D=e3["EF"],
                u_2D_Jm2=e2["u"] * J_PER_MEV_FM2,
                P_2D_Nm=P_areal_to_Nm(e2["P"]),
                P_3D_Nm=P_vol_to_Nm(e3["P"]),
                ratio_EF=e3["EF"] / e2["EF"])


# ------------------------------------------------- three-route consistency audit of handoff quantities
def handoff_routes():
    """Put the four algorithms for n_e side by side, one of which is the v2 erroneous
    formula (regression guard).

    r1 = ZA * n_B[fm^-3]                  (electrons per baryon × baryon bulk density)
    r2 = n_2D[fm^-2] / L_z                (definition of the main convention)
    r3 = Z_eff * n_nuc[fm^-3]             (electrons per nucleus × nuclear bulk density)
    r4 = Z_eff * n_B[fm^-3]               (what v2 actually wrote -- wrong by 10x)
    """
    r1 = ZA * N_B_FM3
    r2 = N_E_FM2 / LZ_FM
    r3 = Z_EFF * N_NUC_FM3
    r4 = Z_EFF * N_B_FM3
    return dict(r1=r1, r2=r2, r3=r3, r4_v2_wrong=r4,
                dev12=abs(r1 - r2) / r1, dev13=abs(r1 - r3) / r1,
                dev14=abs(r4 - r1) / r1)


if __name__ == "__main__":
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    fs = frozen_state()
    hr = handoff_routes()
    print("conv v1 self-report")
    print("  N_s=%.6e m^-2  N_B=%.6e m^-2" % (N_S, N_B))
    print("  n_2D=%.6e fm^-2  n_B=%.6e fm^-3  n_e=%.6e fm^-3" % (N_E_FM2, N_B_FM3, N_E_FM3))
    print("  Z_eff=ZA*m_bar=%.4f  E_sub=%.1f MeV  E_F(2D)=%.2f MeV  E_F(3D)=%.2f MeV"
          % (Z_EFF, E_SUBBAND, fs["EF_2D"], fs["EF_3D"]))
    print("  handoff r1=%.6e r2=%.6e r3=%.6e" % (hr["r1"], hr["r2"], hr["r3"]))
    print("  r4(v2 wrong)=%.6e : ratio r4/r1 = %.6f (must be m_bar=%.0f), reldev = %.3f (=m_bar-1)"
          % (hr["r4_v2_wrong"], hr["r4_v2_wrong"] / hr["r1"], M_BAR_AMU, hr["dev14"]))
    env = beta_envelope()
    for m in MODES:
        r = env[m]
        print("  %-6s D_e=%d D_nuc=%d  X_p=%.4e  mu_e=%.2f  n_e=%.4e  reduction=%.1f  P_tot=%.3e N/m"
              % (m, r["D_e"], r["D_nuc"], r["X_p"], r["mu_e"], r["n_e_fm3"],
                 r["reduction"], r["P_tot_Nm"]))
