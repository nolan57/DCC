#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analytical expression for the sheet conductivity σ_s(ω) of a 2D degenerate electron gas -- complete instrument visualization v2

Corrects the ill-conditioned v2 numerical Lindhard calculation (q_opt/kF ~ 3e-8 leading to 0/0).
Instead use the analytical sheet conductivity in the 2D optical limit (q→0) plus a
high-frequency Pauli-blocking cutoff.

Conventions (strictly registered; specified-background test optics / MODEL RESULT):
- 2D free electron gas, g=2, ultrarelativistic dispersion E = ħc k
- optical limit q→0 (normal incidence), finite ω
- low frequency (ω << E_F): Drude limit σ(ω) = i n e²/(m_eff ω), m_eff = E_F/c²
- high frequency (ω ~ E_F): Pauli blocking; the real part of the conductivity falls
  with the interband-transition weight
- this result is not a DCC observational prediction

Analytical 2D conductivity (relativistic, T=0, q→0):
  the real part of the low-frequency limit σ(ω→0) is set by the scattering rate Γ;
  the imaginary part ∝ 1/ω (Drude weight D)
  D = π n_2D e² c² / E_F  (relativistic m_eff = E_F/c²)

Here we implement a self-consistent, dimensionally correct 2D σ_s(ω):
  σ(ω) = i D/(ω + iΓ) × F(ω/E_F)     [Drude + Pauli-blocking cutoff]
  F(x) = Pauli-blocking factor: x<<1 -> F→1; x>1 -> F→ (interband-transition weight, decreasing)
  simply take the smooth cutoff F(x) = 1/sqrt(1 + (x/x_c)²), with x_c ~ 1
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, "src/common")

plt.rcParams["axes.unicode_minus"] = False

# Constants
HBAR_EVS = 6.582119569e-16   # eV·s
C = 2.99792458e8
MEV = 1.602176634e-13        # J
E2 = 2.3070776e-28           # e² [J·m]
Z0 = 376.730313668
E_CHARGE = 1.602176634e-19

def drude_weight_si(n2d_m2, EF_MeV):
    """Drude weight D [s^-1] (2D, relativistic m_eff=E_F/c²).
    D = π n_2D e² / m_eff = π n_2D e² c² / E_F
    """
    EF_J = EF_MeV * MEV
    m_eff = EF_J / (C*C)
    D = math.pi * n2d_m2 * E_CHARGE**2 / m_eff   # s^-1
    return D, m_eff

def sigma_s(omega_eV, EF_MeV, n2d_m2, gamma_eV):
    """2D sheet conductivity [S], Drude + Pauli-blocking cutoff.
    σ(ω) = i D/(ω+iΓ) × F(ω/E_F)
    """
    D, m_eff = drude_weight_si(n2d_m2, EF_MeV)
    omega = omega_eV / HBAR_EVS          # rad/s
    gamma = gamma_eV / HBAR_EVS          # rad/s
    # Drude part (dimension [S]): σ = i e² n /(m_eff (ω+iΓ))
    sig = 1j * E_CHARGE**2 * n2d_m2 / (m_eff * (omega + 1j*gamma))
    # Pauli-blocking cutoff F(x), x = ħω/E_F
    x = omega_eV / (EF_MeV*1e6)          # dimensionless
    xc = 1.0
    F = 1.0 / math.sqrt(1.0 + (x/xc)**2)
    return sig * F

def reflectivity(sigma):
    r = -Z0*sigma/(2.0 + Z0*sigma)
    return np.abs(r)**2

def main():
    n2d_m2 = 0.0220e28   # frozen-state areal density (fm^-2 -> m^-2)
    gamma_eV = 1.0

    states = [
        ("frozen state Z/A=0.522", 73.37, 0.0220e28),
        ("neutronized state HYB", 21.54, 0.00190e28),  # electron areal density after neutronization (bulk density × Lz)
    ]
    omega = np.logspace(-1, 4.5, 300)

    print("="*70)
    print("2D degenerate electron gas sheet conductivity σ_s(ω): frozen state vs neutronized state (analytical Drude + Pauli blocking)")
    print("="*70)

    results = {}
    for name, ef, n2d in states:
        kF = ef/197.3269804
        print("\n[%s] E_F=%.2f MeV, n_2D=%.4e m^-2, k_F=%.4f fm^-1" % (name, ef, n2d, kF))
        sigs = np.array([sigma_s(w, ef, n2d, gamma_eV) for w in omega])
        Rs = np.array([reflectivity(s) for s in sigs])
        results[name] = (Rs, sigs)
        for lab, ev in (("visible 2.48eV",2.48),("X 4.1keV",4100.0),("X 13.8keV",13800.0)):
            s = sigma_s(ev, ef, n2d, gamma_eV)
            print("    %-14s |σ|=%.4e S  R=%.4f" % (lab, abs(s), reflectivity(s)))

    # ================= rendering =================
    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(3, 3, height_ratios=[1.1, 1.0, 1.0])
    c_f, c_n = "#d64541", "#3b8fd4"

    ax1 = fig.add_subplot(gs[0, :2])
    for name, ef, n2d in states:
        Rs, _ = results[name]
        ax1.semilogx(omega, Rs, lw=2, color=c_f if "frozen" in name else c_n, label=name)
    ax1.axvspan(1.65, 3.26, color="#f5c542", alpha=0.12, label="human-eye window")
    ax1.axvline(4100, color="#7f8c8d", ls=":", lw=1)
    ax1.axvline(13800, color="#7f8c8d", ls=":", lw=1)
    ax1.text(3.2, 0.5, "human eye: near mirror\n(least information)", fontsize=9, color="#7f8c8d")
    ax1.text(5000, 0.4, "keV transmission window:\ncomposition fingerprint legible", fontsize=9, color="#d64541")
    ax1.set_xlabel("photon energy (eV)"); ax1.set_ylabel("reflectivity R")
    ax1.set_title("(a) Reflectivity spectrum: frozen (red) vs neutronized (blue)")
    ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

    ax2 = fig.add_subplot(gs[0, 2])
    for name, ef, n2d in states:
        _, sigs = results[name]
        ax2.semilogx(omega, np.real(sigs), lw=1.5, color=c_f if "frozen" in name else c_n, label=name)
    ax2.set_xlabel("photon energy (eV)"); ax2.set_ylabel("Re σ_s (S)")
    ax2.set_title("(b) Real part of sheet conductivity"); ax2.legend(fontsize=7); ax2.grid(alpha=0.3)

    ax3 = fig.add_subplot(gs[1, :2])
    Rf = results[states[0][0]][0]; Rn = results[states[1][0]][0]
    diff = np.abs(Rf - Rn)
    ax3.semilogx(omega, diff, color="#9b59b6", lw=2)
    ax3.axvspan(1.65, 3.26, color="#f5c542", alpha=0.12)
    ax3.set_xlabel("photon energy (eV)"); ax3.set_ylabel("|ΔR|")
    ax3.set_title("(c) Reflectivity difference between the two states: largest discrimination in the keV range")
    ax3.grid(alpha=0.3)
    imax = omega[np.argmax(diff)]
    ax3.axvline(imax, color="#d64541", ls="--", lw=1)
    ax3.text(imax*1.5, max(diff)*0.7, "discrimination peak\n%.2f keV" % (imax/1000), fontsize=9, color="#d64541")

    ax4 = fig.add_subplot(gs[1, 2])
    ax4.text(0.5, 0.92, "Instrument visualization overview", ha="center", fontsize=12, weight="bold", color="#2c3e50")
    ax4.text(0.5, 0.76, "X-ray reflectivity spectrum", ha="center", fontsize=10, color="#3b8fd4")
    ax4.text(0.5, 0.63, "composition fingerprint from the keV transmission window", ha="center", fontsize=8, color="#555")
    ax4.text(0.5, 0.48, "neutrino flux", ha="center", fontsize=10, color="#d64541")
    ax4.text(0.5, 0.35, "direct evidence of neutronization", ha="center", fontsize=8, color="#555")
    ax4.text(0.5, 0.20, "gravitational signal", ha="center", fontsize=10, color="#9b59b6")
    ax4.text(0.5, 0.07, "3.8e18 J/m² stress-energy", ha="center", fontsize=8, color="#555")
    ax4.set_xlim(0,1); ax4.set_ylim(0,1); ax4.axis("off")

    ax5 = fig.add_subplot(gs[2, :])
    ax5.semilogx(omega, Rf, color=c_f, lw=2, label="frozen state R(ω)")
    ax5.semilogx(omega, Rn, color=c_n, lw=2, label="neutronized state R(ω)")
    ax5.fill_between(omega, Rf, Rn, color="#f5c542", alpha=0.3, label="region where the two states are distinguishable")
    ax5.axvspan(1.65, 3.26, color="#95a5a6", alpha=0.08)
    ax5.text(2.0, 0.05, "human-eye blind spot (only a mirror is visible)", fontsize=9, color="#7f8c8d")
    ax5.set_xlabel("photon energy (eV)"); ax5.set_ylabel("reflectivity")
    ax5.set_title("(e) Spectral fingerprint: the two states separate in the keV range")
    ax5.legend(fontsize=8, loc="center right"); ax5.grid(alpha=0.3)

    fig.suptitle("Complete instrument visualization of a 2D degenerate electron gas (analytical Drude + Pauli blocking, specified-background test optics)", fontsize=13)
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    out = "runs/ANALYSIS/instrument_visualization_v2.png"
    plt.savefig(out, dpi=115, facecolor="white")
    print("\n[rendered] ->", out)

if __name__ == "__main__":
    main()
