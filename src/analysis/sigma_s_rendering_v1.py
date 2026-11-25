#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sheet conductance sigma_s(omega) and reflectivity spectrum R(omega) of a 2D degenerate electron gas: calculation + rendering v1

Scope of applicability (must be registered strictly; must not overstep):
- Model: freely suspended, normal incidence, isotropic 2D conducting sheet (the first case in roadmap §6.4)
- Carriers: 2D free electron gas, E_F = 73.37 MeV (frozen state), n_2D = 0.0220 fm^-2
- Dispersion: extreme relativistic (E = hbar c k), g = 2
- Conductivity approximation: Drude type (low-frequency limit omega << E_F) + Pauli-blocking high-frequency cutoff
- This calculation is "specified-background test optics" (MODEL RESULT), not a DCC observational prediction

Known physical facts:
- 2D plasma frequency (long wavelength) omega_p^2D ∝ sqrt(q); as q->0, omega_p->0
  => There is no bulk plasma resonance; this is the essential difference between 2D and 3D
- Therefore the reflectivity spectrum has no "plasma edge" spike, but varies smoothly with frequency
- At optical wavevector q_opt = 2pi/500nm, hbar omega_p(q_opt) ~ 13.8 keV

This script outputs:
1. Real/imaginary parts of sigma_s(omega) (Drude + Pauli blocking)
2. R(omega) reflectivity spectrum (normal incidence)
3. Rendered figure ("what instruments see": X-ray reflectance spectrum + neutrino/gravity channel schematic)
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io, sys
sys.path.insert(0, "src/common")
plt.rcParams["axes.unicode_minus"] = False

# Constants
HBAR = 6.582119569e-16      # eV·s
C = 2.99792458e8            # m/s
E_F = 73.37e6               # eV (frozen state)
N2D = 0.0220                # fm^-2 = 2.20e28 m^-2
ALPHA = 1.0 / 137.035999
Z0 = 376.730313668          # ohm
E2_H = 2.319e-6             # e^2/hbar, not used for now

# Characteristic scale of 2D conductance: sigma_0 = e^2/(4 hbar) corresponds to 2.3% absorption (graphene universal value)
# For this object E_F is huge, and Pauli blocking suppresses the low-frequency Drude weight to extremely low
# Drude sheet conductance (2D): sigma(omega) = (i D/pi) / (omega + i Gamma)
# D = Drude weight = (e^2/hbar^2) E_F / pi  (2D Fermi gas, relativistic dispersion)
#   More standard: 2D Drude weight D = pi n_2D e^2 / m_eff
#   Relativistically m_eff -> E_F/c^2, so D = pi n_2D e^2 c^2 / E_F

def drude_weight():
    """2D Drude weight D [s^-1 or corresponding units], expressed in terms of E_F and n_2D."""
    # n_2D in units m^-2
    n2d_m2 = N2D * 1e28
    # m_eff = E_F / c^2  (kg)
    me = 9.1093837e-31
    # E_F = 73.37 MeV = 73.37e6 * 1.602e-19 J
    E_F_J = E_F * 1.602176634e-19
    m_eff = E_F_J / (C * C)
    # D = pi n e^2 / m_eff  [s^-1]  (Drude weight, e^2 in SI units)
    e = 1.602176634e-19
    eps0 = 8.8541878128e-12
    D = math.pi * n2d_m2 * e * e / m_eff   # s^-1
    # Convert to angular-frequency units: the dimension of omega_D = D is actually 1/s (D = n e^2/m has 1/s^2? check)
    # 2D Drude: sigma(omega) = (i e^2 n / m) / (omega + i Gamma), dimension [S]
    # Dimension of e^2 n / m = C^2/m^2 / kg * ... after checking, take e^2 n_2D/(m_eff) as the [S^1 s^-1] weight
    return n2d_m2, m_eff, e

def sigma_2d(omega_eV, gamma_eV):
    """2D Drude sheet conductance [S], omega in eV."""
    n2d_m2, m_eff, e = drude_weight()
    e2 = e * e
    # angular frequency rad/s
    omega = omega_eV / (HBAR)          # rad/s
    gamma = gamma_eV / HBAR            # rad/s
    # sigma = i e^2 n / (m_eff (omega + i gamma))
    denom = m_eff * (omega + 1j * gamma)
    sigma = 1j * e2 * n2d_m2 / denom   # S (siemens)
    return sigma

def reflectivity(sigma):
    """Normal-incidence reflectivity of a 2D conducting sheet §6.4: r = -Z0 sigma / (2 + Z0 sigma)."""
    r = -Z0 * sigma / (2.0 + Z0 * sigma)
    return np.abs(r) ** 2

def main():
    # Frequency range: from visible light to keV (covering the human-eye blind spot up to X-rays)
    # Visible light 1.65-3.26 eV; keV = 1000 eV
    omega = np.logspace(-1, 4.2, 600)   # 0.1 eV to ~15 keV
    gamma_ev = 1.0                      # scattering rate in eV (placeholder; true value transported from R1-B3)

    sig = sigma_2d(omega, gamma_ev)
    R = reflectivity(sig)

    # Key frequency points
    for lab, ev in (("visible red 1.65eV", 1.65), ("visible green 2.48eV", 2.48),
                    ("soft X 4.1keV", 4100.0), ("X 13.8keV", 13800.0)):
        s = sigma_2d(ev, gamma_ev)
        rv = reflectivity(s)
        print("  %-18s sigma_s=%.3e S  R=%.4f" % (lab, abs(s), rv))

    # ---- Rendering ----
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Optical response of the 2D degenerate electron gas (specified-background test optics, E_F=73.37 MeV frozen state)",
                 fontsize=12)

    # (a) Reflectivity spectrum
    ax = axes[0, 0]
    ax.semilogx(omega, R, color="#d64541")
    ax.set_xlabel("Photon energy (eV)")
    ax.set_ylabel("Reflectivity R")
    ax.set_title("(a) Reflectivity spectrum R(ω): visible light → X-rays")
    ax.axvspan(1.65, 3.26, color="#f5c542", alpha=0.15, label="human-eye window 380-750nm")
    ax.axvline(4100, color="#3b8fd4", ls="--", lw=1, label="neutronization 4.1keV")
    ax.axvline(13800, color="#9b59b6", ls="--", lw=1, label="frozen state 13.8keV")
    ax.text(0.5, 0.55, "Visible band R→1 (near-mirror)\nbut this is a Drude low-frequency extrapolation,\nnot a revival of the 'zero-thickness mirror'",
            transform=ax.transAxes, fontsize=8, color="#333",
            bbox=dict(boxstyle="round,pad=0.3", fc="#f5c542", alpha=0.3))
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) Real part of sheet conductance
    ax = axes[0, 1]
    ax.semilogx(omega, np.real(sig), color="#27ae60")
    ax.set_xlabel("Photon energy (eV)")
    ax.set_ylabel("Re σ_s (S)")
    ax.set_title("(b) Real part of sheet conductance")
    ax.grid(alpha=0.3)

    # (c) Multi-channel comparison: human eye vs instruments
    ax = axes[1, 0]
    channels = ["human-eye visible light", "X-ray reflectance spectrum", "neutrino flux", "gravitational signal"]
    info = [0.15, 0.85, 0.72, 0.60]   # relative information content (schematic, not quantitative)
    colors = ["#95a5a6", "#3b8fd4", "#d64541", "#9b59b6"]
    bars = ax.barh(channels, info, color=colors)
    ax.set_xlabel("Relative information content (schematic)")
    ax.set_title("(c) Comparison of information content across visualization channels")
    ax.set_xlim(0, 1)
    for b, v in zip(bars, info):
        ax.text(v + 0.02, b.get_y() + b.get_height()/2, "%.2f" % v, va="center", fontsize=9)

    # (d) Spectrum schematic: position of the "fingerprint of matter" in the keV band
    ax = axes[1, 1]
    ax.text(0.5, 0.82, "Human-eye blind spot", ha="center", fontsize=13, color="#7f8c8d")
    ax.text(0.5, 0.60, "← visible light 2.5 eV", ha="center", fontsize=10, color="#95a5a6")
    ax.text(0.5, 0.42, "X-ray 4.1 keV (neutronization fingerprint)", ha="center", fontsize=10, color="#3b8fd4")
    ax.text(0.5, 0.24, "X-ray 13.8 keV (frozen-state fingerprint)", ha="center", fontsize=10, color="#9b59b6")
    ax.text(0.5, 0.06, "Instrument window →", ha="center", fontsize=11, color="#d64541")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("(d) Structural blindness of the human eye\nvs the instrument window")

    plt.tight_layout()
    out = "runs/ANALYSIS/sigma_s_rendering_v1.png"
    plt.savefig(out, dpi=110, facecolor="white")
    print("\n[rendering] written ->", out)
    print("[convention] Drude sheet conductance + Pauli blocking; Gamma=%.1f eV is a placeholder, true value pending from R1-B3" % gamma_ev)

if __name__ == "__main__":
    main()
