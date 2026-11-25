#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Persistent visualization / instrument visualization boundary analysis v1

Question: if "persistent visualization" or "instrument visualization" is required, (1) how do the boundaries change, (2) what would the visualization roughly look like?

Conventions: use the constants from conv.py; all downstream quantities use the three-convention envelope. All optical conclusions are labeled "specified-background test optics" and are not stated at the level of physical predictions (required by roadmap §6.4/6.7).

Only numerical analysis is output; no rendering.
"""
import math, sys, io

sys.path.insert(0, "src/common")
import conv  # noqa

HBAR = 6.582119569e-16   # eV s
C = 2.99792458e8
MEV = 1.602176634e-13    # J
E_SCHW = 1.32            # MeV/fm
Z0 = 376.730313668       # ohm
E2_4HBAR = 2.302e-5      # alpha / (4*eps0...) constant not used after simplification

# ---------------------------------------------------------------- basic quantities
n2D = conv.N_E_FM2          # fm^-2
Lz = 1.0                    # fm
E_F = 73.37                 # MeV
E_sub = conv.E_SUBBAND      # 619.9 MeV
u_in = 1.7245e17            # J/m^2 (G0 v3)
P_lat = 8.623e16            # N/m
MC2_m2 = 70.0 * 9.0e16      # J/m^2
tau_rip = 4.72e-9           # s

W = io.StringIO()
def w(*a): print(*a, file=W)

w("=" * 80)
w("Persistent/instrument visualization boundary analysis v1")
w("=" * 80)
w("  L_z=%.1f fm | n_2D=%.4f fm^-2 | E_F=%.2f MeV | E_sub=%.1f MeV" % (Lz, n2D, E_F, E_sub))
w("")

# ================================================================ P1 persistence definition
w("[P1] Energy cost of persistence (sustained on demand vs one-time generation)")
w("  One-time generation energy u_in = %.3e J/m^2 = %.2f%% Mc^2/A" % (u_in, 100*u_in/MC2_m2))
w("  Confinement zero-point energy (electrons + nucleons) = 3.44e18 J/m^2 = 54.7%% Mc^2/A (K4, route M)")
w("  => First cost of 'persistence': turning the total energy of the transient state (including confinement zero-point energy) from 'paid once' into 'held continuously'")
w("  Strictly speaking, if the state does not dissipate, no supplementary power is needed; but any real confinement field has leakage/tunneling/radiative losses,")
w("  so the substantive requirement for persistence is: the confinement field maintains the potential shape over the lifetime, and loss channels are continuously compensated.")
w("  This is an engineering constraint rather than a new physical quantity: the boundary is upgraded from R1 (instantaneous field) to R1' (sustained field + loss compensation)")
w("")

# ================================================================ P2 timescales
w("[P2] Persistence requirements vs natural timescales")
w("  Natural timescales: neutronization tau_cap=%.2f ns | tearing t_rip=%.2f ns | sound crossing 0.33 ns" % (2.96, 4.72))
w("  'Persistent' must far exceed all three, so persistence = simultaneously switch off the weak interaction (or accept neutronization) + sustained confinement + sustained energy supply")
w("  => Persistence is not 'extending the lifetime' but 'turning a transient into a steady state'; K5 changes from a conflict to an engineering constraint")
w("")

# ================================================================ P3 instrument window (beyond the human eye)
w("[P3] Instrument visualization: translating 'invisible to the human eye' into 'detectable frequency bands'")
w("  Human eye: 380-750 nm = 1.65-3.26 eV")
w("  2D plasmon (optical wavevector) hbar*w_p(q_opt) = 13.8 keV -> in the X-ray/deep-UV band, a blind spot of the human eye")
w("  After neutronization hbar*w_p(q_opt) = 4.1 keV -> still X-ray")
w("  Conclusion: the characteristic optical response of this object lies in the keV band, to which the human eye is structurally blind; but X-ray/extreme-UV instruments are exactly in the window")
w("")

# wavelengths corresponding to the X-ray energy band
for E_keV, lab in ((13.8, "frozen state"), (4.1, "neutronized state")):
    lam_nm = 1239.8 / (E_keV * 1e3)   # nm
    w("  %-6s hbar*w=%.1f keV -> lambda=%.3f nm (X/soft-X band)" % (lab, E_keV, lam_nm))

w("")
w("  Four channels detectable by instruments (independent of the human eye):")
w("  (a) Reflectance spectrum R(lambda): plasmon edge in the keV band")
w("  (b) Neutrino flux (W6: 9.7e16 J/m^2, 0.56 x u_in) — neutrino detector")
w("  (c) Thermal emission spectrum (if T is known) — but adiabatic => cold => weak thermal signal")
w("  (d) Gravitational signal (stress-energy of 3.8e18 J/m^2) — gravitational wave/equivalence principle detection")
w("")

# ================================================================ P4 optical orders of magnitude (sheet-conductance framework)
w("[P4] Optical orders of magnitude in the sheet-conductance framework (specified-background test optics, not a prediction)")
w("  For an ultrathin film, R/T/A are determined by sigma_s(omega); sigma_s is given by the finite-density polarization tensor")
w("  Reference order of magnitude: graphene sigma=e^2/4hbar -> Z0*sigma = pi*alpha = 2.3%%")
w("  For this object E_F=73 MeV, sigma_s is unrelated to graphene (§6.4 forbids assuming 2.3% by default)")
w("  The only robust conclusion: both R and T can be O(1), and have plasmon structure vs omega in the keV band")
w("  => Whether the visible band is 'nearly transparent or highly reflective' cannot be determined a priori; must wait for the sigma_s calculation")
w("")

# ================================================================ P5 boundary comparison: persistent vs one-time
w("[P5] Boundary comparison: one-time vs persistent")
w("  One-time (previous round): R1 field >=6e23 V/m, lifetime 3-5 ns, imageable window < light-crossing timescale")
w("  Persistent: R1' field + sustained energy source, lifetime >> t_rip, must simultaneously suppress the weak interaction (or accept steady-state neutronization)")
w("           New R5: stable energy supply (power >= zero-point energy/lifetime), R6: sustained maintainability of weak suppression")
w("  Number of knobs: 4 -> 6 (added: energy supply, persistence of weak suppression)")
w("")

# ================================================================ P6 visualization effect (human eye vs instruments)
w("[P6] Visualization effect (under the persistent boundary)")
w("  Human eye (if visible light is still used):")
w("    - Zero-thickness mirror is void (physically unreachable); the real object is an ultrathin film with extremely small but nonzero L_z")
w("    - If R~1: mirror (reflects the environment, no intrinsic color); if T~1: nearly invisible; both are forbidden as a priori assertions")
w("    - The only a priori statement: no diffuse-reflection texture (the surface has no atomic-scale roughness structure), no chemical color")
w("  Instruments (X-ray/neutrino/gravity):")
w("    - X-ray reflectance spectrum: plasmon edge in the keV band, a 'fingerprint of matter'")
w("    - Neutrino flux: 0.56 x degeneracy energy, direct evidence of the neutronization process")
w("    - Gravity: stress-energy of 3.8e18 J/m^2, detectable at the equivalence-principle scale")
w("  => 'Human-eye visualization' has almost only two degenerate limits (mirror/transparent); 'instrument visualization' is the information-rich window")
w("")

# ================================================================ Summary
w("=" * 80)
w("Summary")
w("=" * 80)
w("1. Persistence turns one-time energy into sustained power, increasing the boundary knobs from 4 to 6 (+energy supply, +persistence of weak suppression)")
w("2. Persistence does not change K6 (weak preservation vs stability are mutually exclusive); it only requires weak suppression to be sustained as well")
w("3. The human-eye window is structurally blind: the characteristic response is in the keV band, so the eye can only see the two degenerate limits of mirror/transparent")
w("4. The instrument window is the information-rich one: three independent channels — X-ray reflectance spectrum, neutrino flux, gravitational signal")
w("5. All optical conclusions remain subject to §6.7: labeled 'specified-background test optics', with a priori mirror/transparent assertions forbidden")
w("")

open("runs/ANALYSIS/persistent_visualization_v1.txt", "w", encoding="utf-8").write(W.getvalue())
print(W.getvalue())
