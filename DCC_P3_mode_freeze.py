#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DCC P3 — Numerical demonstration of mode freezing and gap opening as C→0
=================================================

Background: P2 homogeneous magnetically driven contracting solution (specified contracting background;
D3 not achieved, see P2 report v2 §10). We adopt a power-law contracting ansatz C(t) = C0*(t/t0)^beta
(beta<0, representing the contracting segment extrapolated from the magnetic attractor; of the homogeneous
Kasner extrapolation type C∝t^{-1/3}, taking beta=-1/2 as representative of magnetic contraction scaling),
with A and B following the magnetic-attractor scaling A∝B∝t^{1/2} (transverse expansion, remaining finite).

Three-dimensional massless scalar mode chi_pz (KK decomposition chi = Σ chi_pz(t,x,y) e^{i p_z z}):
    χ''_pz + (H_A+H_B+H_C) χ'_pz + [p_z^2/C^2 + k_perp^2/A^2] χ_pz = 0
(directly from □χ=0 in the (A,B,C) metric; in the limit C→0 the effective mass of p_z≠0 modes,
   m_eff=|p_z|/C, diverges — mode freezing and the dimension-limited energy gap.)

Outputs:
    DCC_P3_mode_freeze_results.txt
    DCC_P3_mode_freeze.png
      - time series of m_eff(t)=|p_z|/C (gap opening)
      - 2D-observed energy fraction E_pz/E_tot of each p_z mode (energy of high-p_z modes decays → degrees of freedom excluded)
      - adiabatic parameter |m_dot_eff|/m_eff^2 criterion (condition for freezing to occur)

Run: python DCC_P3_mode_freeze.py
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Specified contracting background (phenomenological scaling ansatz; not an implemented D3 solution — constrained by P2 report §10)
# ----------------------------------------------------------------------
T0 = 1.0
BETA_C = -0.5     # C contraction exponent (representative value of magnetic contraction scaling)
BETA_AB = 0.5     # transverse expansion exponent (magnetic attractor: A,B ∝ t^{1/2})
C0 = 1.0
AB0 = 1.0
T_END = 30.0

def Hs(t):
    """H_A=H_B=H, H_C and the scale factors (analytic form of the power-law ansatz)."""
    s = t / T0
    H_AB = BETA_AB / t
    H_C = BETA_C / t
    A = AB0 * s ** BETA_AB
    C = C0 * s ** BETA_C
    return H_AB, H_C, A, C

def mode_rhs(t, y, pz, kperp):
    H_AB, H_C, A, C = Hs(t)
    chi, dchi = y
    S = 2 * H_AB + H_C
    omega2 = pz ** 2 / C ** 2 + kperp ** 2 / A ** 2
    return [dchi, -S * dchi - omega2 * chi]

def main():
    lines = []
    def w(s=''):
        print(s)
        lines.append(s)

    w('=' * 82)
    w('DCC P3 — mode freezing and gap opening as C→0 (specified contracting background, phenomenological scaling ansatz)')
    w('=' * 82)
    w('Background: C=C0*(t/T0)^%.1f, A=B=AB0*(t/T0)^%.1f, t∈[%.0f, %.0f]' % (
        BETA_C, BETA_AB, T0, T_END))
    w("Mode equation: chi'' + (2H_AB+H_C)chi' + [p_z^2/C^2 + k_perp^2/A^2]chi = 0")
    w('Constraint note: the contracting background is a phenomenological scaling extrapolated from the magnetic'
      ' attractor, not an implemented D3 solution (P2 report §10)')
    w('')

    t_eval = np.linspace(T0, T_END, 1200)
    kperp = 0.0   # take the transverse ground state (k_⊥=0) to isolate the p_z effect
    pz_list = [0.0, 0.5, 1.0, 2.0, 4.0]
    H_AB, H_C, A_arr, C_arr = Hs(t_eval)
    m_eff = np.abs(pz_list)[:, None] / C_arr[None, :]

    # Energy fraction of each mode (2D observer: E_pz = 0.5*C*|χ'|^2 + 0.5*(p_z^2/C)*|χ|^2 per comoving volume)
    E_rows = []
    chi_end = []
    for pz in pz_list:
        v0 = 0.1 if pz == 0 else 0.0   # give the p_z=0 massless mode an initial velocity to avoid a 0/0 energy ratio
        y0 = [1.0 / np.sqrt(C_arr[0]), v0]   # initial normalization to the 2D inner product (√C factor)
        sol = solve_ivp(mode_rhs, (T0, T_END), y0, t_eval=t_eval,
                        args=(pz, kperp), method='RK45', rtol=1e-10, atol=1e-12)
        chi = sol.y[0]; dchi = sol.y[1]
        E_kin = 0.5 * C_arr * dchi ** 2
        E_pot = 0.5 * (pz ** 2 / C_arr) * chi ** 2
        E_tot = E_kin + E_pot
        E_rows.append((pz, E_tot))
        chi_end.append((pz, float(np.max(np.abs(chi) * np.sqrt(C_arr)))))
        w('p_z=%.1f: E_tot(final)/E_tot(initial)=%.3e   max|χ√C|=%.3e' % (
            pz, E_tot[-1] / E_tot[0], np.max(np.abs(chi) * np.sqrt(C_arr))))

    # Adiabatic parameter
    w('')
    w('Adiabatic parameter |m_dot_eff|/m_eff^2 = (|β_C|/t)/(p_z^2/C^2)*C*... = |β_C|*C/(|p_z|*t):')
    for i, pz in enumerate(pz_list):
        if pz == 0:
            w('  p_z=0: massless mode (m_eff≡0), does not freeze — degree of freedom retained by the low-dimensional'
              ' effective theory')
            continue
        adiab = np.abs(BETA_C) * C_arr / (pz * t_eval)
        w('  p_z=%.1f: max |m_dot|/m^2 = %.3e (<1 means adiabatic freezing; >1 at early t gives particle production)' % (
            pz, float(np.max(adiab))))

    w('')
    w('Degrees-of-freedom counting conclusion:')
    w('  3D massless scalar → 2D effective theory retains the single p_z=0 massless mode;')
    w('  the p_z≠0 tower acquires a gap Δm(t)=|p_z|/C(t) (diverging as C→0) → dimension-limited gap;')
    w('  Same for the electromagnetic field: the p_z=0 modes of A_x,A_y remain the 2D photon; the p_z=0 mode of A_z')
    w('  becomes a 2D scalar (dimensional conversion of the third photon polarization); the p_z≠0 modes decouple with')
    w('  diverging Proca-type mass |p_z|/C.')

    # Figure
    fig, axes = plt.subplots(1, 3, figsize=(16, 4.5))
    for i, pz in enumerate(pz_list):
        axes[0].loglog(t_eval, m_eff[i], label='p_z=%.1f' % pz)
    axes[0].set_xlabel('t'); axes[0].set_ylabel(r'$m_{\rm eff}=|p_z|/C$')
    axes[0].set_title('gap opening'); axes[0].legend(); axes[0].grid(alpha=0.3)
    for (pz, E) in E_rows:
        axes[1].loglog(t_eval, E / E[0], label='p_z=%.1f' % pz)
    axes[1].set_xlabel('t'); axes[1].set_ylabel(r'$E_{p_z}/E_{p_z}(0)$')
    axes[1].set_title('mode energy (2D observer)')
    axes[1].legend(); axes[1].grid(alpha=0.3)
    for i, pz in enumerate(pz_list):
        if pz > 0:
            adiab = np.abs(BETA_C) * C_arr / (pz * t_eval)
            axes[2].loglog(t_eval, adiab, label='p_z=%.1f' % pz)
    axes[2].axhline(1.0, color='k', ls='--', lw=0.8)
    axes[2].set_xlabel('t'); axes[2].set_ylabel(r'$|\dot m|/m^2$')
    axes[2].set_title('adiabatic parameter'); axes[2].legend(); axes[2].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig('DCC_P3_mode_freeze.png', dpi=140)
    plt.close(fig)

    with open('DCC_P3_mode_freeze_results.txt', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    w('')
    w('Written: DCC_P3_mode_freeze_results.txt / DCC_P3_mode_freeze.png')


if __name__ == '__main__':
    main()
