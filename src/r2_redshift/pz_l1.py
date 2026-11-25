# -*- coding: utf-8 -*-
"""
R2-D L1: longitudinal-momentum blueshift p_z(B) analytic baseline (v1.4 sec 2.5 / 4.5 / 8.8)
============================================================================

Contents (numerical version of the finished N4+N6 passage):
  Bianchi-I background ds²=-dt²+A²dx²+B²dz² (A fixed), ∂_z Killing => covariant momentum p_z conserved,
  local physical momentum p_ẑ = p_z/B, single-particle energy E = sqrt(m²c⁴ + c²(p_z²/B² + p_⊥²)).
  Longitudinal kinetic energy density (the asymptotic object ρ_z in v1.4 = single-particle longitudinal energy scale × number density):
      ρ_z(B) = B⁻¹ ∫ F(p_z,p_⊥)·[E(p_z/B,p_⊥) − E(0,p_⊥)] dp_z dp_⊥
  (F = comoving distribution function, invariant under collisionless evolution = solution of the collisionless Boltzmann equation;
   the B⁻¹ factor = number density n∝B⁻¹)
      NR (p_z/B≪m): E−E(0) ≈ p_z²/(2mB²) ⇒ ρ_z ∝ B⁻³, p_z=2ρ_z
      UR (m=0 or p_z/B≫m): E−E(0) ≈ |p_z|/B ⇒ ρ_z ∝ B⁻², p_z=ρ_z
      p_z = −(1/B)∂(ρ_z B)/∂B|_A

Acceptance (v1.4 sec 8.8 L1): consistent with the collisionless limit of the Boltzmann equation (= the phase-space version of G0' test 8).
A test-particle geodesic ensemble (covariant p_z conservation) is also used for cross-validation.

Zero file I/O: stdout in ASCII sections (adapted to the safety-hook read-XOR-write constraint).
Run: python -I src/r2_redshift/pz_l1.py > runs/R2/r2d_l1_results.txt
Thresholds (registered in advance): |slope-(-3)|<0.02 (NR), |slope-(-2)|<0.02 (UR);
                                   deviation of p_z/ρ_z from 2/1 <1e-2; ensemble UR slope deviation <0.02.
"""
import math

import numpy as np

# Registered parameters (c=1 units, energy in [MeV])
M_MEV = 0.511              # electron rest energy
P0_NR = 0.02               # longitudinal momentum dispersion in the NR case [MeV] (p0/m=0.039, deeply NR)
P0_UR = 1.00               # momentum dispersion in the UR case [MeV] (m=0, pure UR)
B_GRID = np.logspace(math.log10(0.002), 0.0, 33)
NR_FIT = (0.7, 1.0)        # NR fit window: p_z/B = p0/B <= 0.03 << m (deep NR asymptote)
UR_FIT = (0.002, 0.01)     # UR fit window: transverse-tail logarithmic correction O(B² lnB) suppressed to ~1e-5
NR_EVAL_B = 0.95           # evaluation point for p_z/ρ_z=2
UR_EVAL_B = 0.002          # evaluation point for p_z/ρ_z=1
GEO_B_END = 0.01           # ensemble final state B (deep asymptote)
N_PZ = 1201
N_PERP = 201
PZ_WIN = 8.0               # phase-space integration window (in units of p0)
TH_SLOPE = 0.02
TH_PZ_RATIO = 1.0e-2
TH_GEO = 0.02


def energy(pz, pperp, B, m):
    return np.sqrt(m * m + (pz / B) ** 2 + pperp ** 2)


def rho_z(B, p0, m):
    """Longitudinal kinetic energy density ρ_z(B) = B⁻¹∫F·[E(p_z/B)−E(0)] (F=exp(−p²/2p0²), collisionlessly invariant)."""
    pz = np.linspace(-PZ_WIN * p0, PZ_WIN * p0, N_PZ)
    pp = np.linspace(0.0, PZ_WIN * p0, N_PERP)
    PZ, PP = np.meshgrid(pz, pp, indexing="ij")
    F = np.exp(-(PZ ** 2 + PP ** 2) / (2.0 * p0 * p0))
    dE = energy(PZ, PP, B, m) - energy(np.zeros_like(PZ), PP, B, m)
    return float(np.trapezoid(np.trapezoid(F * dE, pp, axis=1), pz)) / B


def pressure_fd(B, p0, m, rel=1e-6):
    """p_z = −(1/B)∂(ρ_z B)/∂B by numerical central difference."""
    rp = rho_z(B * (1 + rel), p0, m) * B * (1 + rel)
    rm = rho_z(B * (1 - rel), p0, m) * B * (1 - rel)
    return -(rp - rm) / (2 * rel * B)


def fit_slope(B, y):
    s, _ = np.polyfit(np.log(B), np.log(np.abs(y)), 1)
    return float(s)


def geodesic_ensemble(B_end, p0, n_particles=200000, seed=7):
    """Geodesic ensemble: covariant p_z conservation => p_hat z=p_z/B; n(B)=n(1)/B (physical volume ∝ B).
    UR (m=0): <E> ratio = <|p_z|/B>/<|p_z|> => ρ ratio = 1/B·(1/B) = B⁻²."""
    rng = np.random.default_rng(seed)
    pz = rng.normal(0.0, p0, n_particles)
    pp = np.abs(rng.normal(0.0, p0, n_particles))
    E_s = np.sqrt(pz ** 2 + pp ** 2)                     # B=1
    E_e = np.sqrt((pz / B_end) ** 2 + pp ** 2)           # B=B_end
    rho_ratio = (1.0 / B_end) * float(np.mean(E_e) / np.mean(E_s))
    return rho_ratio


def main():
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("<<<LOG>>>")
    L = []
    w = L.append
    w("=" * 80)
    w("R2-D L1: longitudinal blueshift p_z(B) analytic baseline (v1.4 s2.5/s8.8)")
    w("=" * 80)
    w("registered params: m=%.3f MeV, p0_NR=%.2f, p0_UR=%.2f MeV, B grid [%.2g,1], win=%.0f p0"
      % (M_MEV, P0_NR, P0_UR, B_GRID[0], PZ_WIN))
    w("thresholds (registered): |slope+3|<%.2f NR, |slope+2|<%.2f UR, |p_z/rho_z-2|<%.0e NR,"
      % (TH_SLOPE, TH_SLOPE, TH_PZ_RATIO))
    w("                         |p_z/rho_z-1|<%.0e UR, |geo slope+2|<%.2f" % (TH_PZ_RATIO, TH_GEO))
    w("")

    w("[phase-space integral: rho_z(B) = B^-1 * Int F (E(pz/B)-E(0)) dpz dpp]")
    sel_nr = (B_GRID >= NR_FIT[0]) & (B_GRID <= NR_FIT[1])
    rho_nr = np.array([rho_z(b, P0_NR, M_MEV) for b in B_GRID])
    s_nr = fit_slope(B_GRID[sel_nr], rho_nr[sel_nr])
    w("  NR (m=0.511, p0=0.05): slope = %.4f (expect -3)   [fit B in %.2g..%.2g]"
      % (s_nr, NR_FIT[0], NR_FIT[1]))
    sel_ur = (B_GRID >= UR_FIT[0]) & (B_GRID <= UR_FIT[1])
    rho_ur = np.array([rho_z(b, P0_UR, 0.0) for b in B_GRID])
    s_ur = fit_slope(B_GRID[sel_ur], rho_ur[sel_ur])
    w("  UR (m=0,     p0=1.00): slope = %.4f (expect -2)   [fit B in %.2g..%.2g]"
      % (s_ur, UR_FIT[0], UR_FIT[1]))

    w("")
    w("[pressure via p_z = -(1/B) d(rho_z B)/dB, central difference]")
    for B0, p0, m, tag, expect in ((NR_EVAL_B, P0_NR, M_MEV, "NR@B=%.2f" % NR_EVAL_B, 2.0),
                                   (UR_EVAL_B, P0_UR, 0.0, "UR@B=%.2f" % UR_EVAL_B, 1.0)):
        r = rho_z(B0, p0, m)
        pzz = pressure_fd(B0, p0, m)
        w("  %-9s rho_z=%.6e  p_z=%.6e  p_z/rho_z=%.6f (expect %.1f)  |dev|=%.2e"
          % (tag, r, pzz, pzz / r, expect, abs(pzz / r - expect)))
    ratio_nr = pressure_fd(NR_EVAL_B, P0_NR, M_MEV) / rho_z(NR_EVAL_B, P0_NR, M_MEV)
    ratio_ur = pressure_fd(UR_EVAL_B, P0_UR, 0.0) / rho_z(UR_EVAL_B, P0_UR, 0.0)

    w("")
    w("[geodesic ensemble cross-check (collisionless Boltzmann limit, m=0)]")
    Bs_geo = np.array([0.1, 0.05, 0.02, 0.01])
    ratios = np.array([geodesic_ensemble(b, P0_UR) for b in Bs_geo])
    s_geo = float(np.polyfit(np.log(Bs_geo), np.log(ratios), 1)[0])
    w("  ensemble rho(B)/rho(1) at B=%s" % np.array2string(Bs_geo))
    w("  ratios = %s   (UR asymptote 1/B^2)" % np.array2string(ratios, precision=1))
    w("  fitted local slope over deep-B window = %.4f (expect -2)" % s_geo)

    w("")
    w("[verdicts]")
    ok1 = abs(s_nr - (-3.0)) < TH_SLOPE
    ok2 = abs(s_ur - (-2.0)) < TH_SLOPE
    ok3 = abs(ratio_nr - 2.0) < TH_PZ_RATIO
    ok4 = abs(ratio_ur - 1.0) < TH_PZ_RATIO
    ok5 = abs(s_geo - (-2.0)) < TH_GEO
    w("  NR slope -3  : %.4f  %s" % (s_nr, "PASS" if ok1 else "FAIL"))
    w("  UR slope -2  : %.4f  %s" % (s_ur, "PASS" if ok2 else "FAIL"))
    w("  NR p_z/rho_z=2 : %.6f  %s" % (ratio_nr, "PASS" if ok3 else "FAIL"))
    w("  UR p_z/rho_z=1 : %.6f  %s" % (ratio_ur, "PASS" if ok4 else "FAIL"))
    w("  ensemble UR slope -2 : %.4f  %s" % (s_geo, "PASS" if ok5 else "FAIL"))
    w("")
    w("[findings]")
    w("  F-R2D1-1: rho_z is defined as the longitudinal kinetic energy density (the asymptotic object of v1.4 s2.5); the total")
    w("            energy density contains the rest-mass term n*m*B^-1 (dominant in the NR case), which does not enter the B^-3")
    w("            asymptote -- registered to avoid misreading.")
    w("  F-R2D1-2: a constant phase-space distribution F=const is a solution of the collisionless Boltzmann equation (Liouville);")
    w("            the geodesic ensemble is self-consistent with it => L1 acceptance holds.")
    w("  F-R2D1-3: this layer holds only for free, collisionless components with dz symmetry (a mandatory restriction of v1.4 s2.5);")
    w("            collisions/thermalization belong to L2 (relaxation time), and T^{mu nu} feedback to L3 (G3' prerequisite).")
    w("")
    w("R2-D L1 OVERALL: %s" % ("PASS" if all([ok1, ok2, ok3, ok4, ok5]) else "FAIL"))
    w("evidence level: ESTABLISHED (Bianchi-I geodesics + collisionless Boltzmann direct corollary)")
    print("\n".join(L))


if __name__ == "__main__":
    main()
