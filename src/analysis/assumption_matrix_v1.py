# -*- coding: utf-8 -*-
"""Three-assumption combination matrix v1: 8 combinations x visual effects (2026-11-21)

Write the three assumptions as three booleans, exhaust all 2^3=8 combinations, and
give, row by row: state of matter / energy ledger / what the eye sees / duration /
verdict.

  E = effective 2D reduction holds (z-direction energy gap > occupation scale and
      probe energy)
  S = smooth 2D reduction holds (quasi-static, reversible, with a before/after order)
  W = weak-interaction preservation holds (no neutronization)

The three are not independent knobs. What this module demonstrates is their
**dependency structure**:

  E is the only energy source: only E requires L_z~1 fm, and only that thickness
    gives nuclear density and MeV-scale degeneracy pressure at Sigma=70 kg/m^2.
    Without E the total energy drops from 41.2 Mt to 0.
  S and W are both downstream of E: without E, mu_e drops to ~4 eV (the 7 cm case),
    so there is no degeneracy pressure to explode (nothing for S to do) and no
    neutronization to occur (nothing for W to do).

Boundaries (already checked):
  E definition boundary    L_z < 8.45 fm     (E_sub = E_F)
  E registration boundary  L_z < 1.99 fm     (K1 threshold ratio>=4.25, stricter for engineering)
  W validity boundary      L_z < 2.32 nm     (mu_e = 1.293 MeV, 3D convention)
  => W's domain strictly contains E's domain.

Labels: geometry/thresholds CHECK; fireball quantities and energy partition ESTIMATE;
dependency structure ARGUMENT.
"""
import math
import sys

sys.path.insert(0, "src/common")
import conv

SIGMA = conv.M_KG / conv.A_PERP
MT = 4.184e15
E_DEG = 1.7245e17                  # J/m^2  (degeneracy areal energy when E holds)
P_2D = 8.62e16                     # N/m
E_KIN_111 = 0.5 * conv.M_KG * (2.0 * P_2D / SIGMA)      # 20.6 Mt
E_NU = 0.56 * E_DEG
P_EQ_LO, P_EQ_HI = 1.84e16, 6.48e16                     # pressure envelope after neutronization

N_E = conv.N_E_FM2
L_E_DEF = math.pi / math.sqrt(2.0 * math.pi * N_E)
L_W = 3 * math.pi ** 2 * N_E / ((1.293 / conv.HBARC) ** 3)
L_7CM = 7.0e-2 / 1e-15

OUT = []


def w(s=""):
    OUT.append(s)


def mu_e_3d(L_fm):
    return conv.HBARC * (3 * math.pi ** 2 * (N_E / L_fm)) ** (1.0 / 3.0)


def ke_from_P(P):
    v = math.sqrt(2.0 * P / SIGMA)
    return 0.5 * conv.M_KG * v ** 2, v


def row(combo, state, energy, visible, dur, verdict):
    w("| %s | %s | %s | %s | %s | %s |" % (combo, state, energy, visible, dur, verdict))


def main():
    w("=" * 78)
    w("Three-assumption combination matrix v1")
    w("=" * 78)
    w("E definition boundary L_z < %.2f fm | W validity boundary L_z < %.2e fm (= %.2f nm)"
      % (L_E_DEF, L_W, L_W * 1e-6))
    w("Sigma=%.0f kg/m^2, E_deg=%.3e J/m^2=%.1f Mt" % (SIGMA, E_DEG, E_DEG / MT))
    w("")

    # ---- numerical ledger
    w("[Numerical ledger]")
    w("  101: KE=%.3e J = %.1f Mt ; radiation=%.1f Mt ; total %.1f Mt"
      % (E_KIN_111, E_KIN_111 / MT, (E_DEG - E_KIN_111) / MT, E_DEG / MT))
    w("  110: nu=%.3e J = %.1f Mt (invisible)" % (E_NU, E_NU / MT))
    k_lo, v_lo = ke_from_P(P_EQ_LO)
    k_hi, v_hi = ke_from_P(P_EQ_HI)
    w("  100: after neutronization P in [%.2e, %.2e] N/m -> KE in [%.1f, %.1f] Mt, v in [%.3f, %.3f]c"
      % (P_EQ_LO, P_EQ_HI, k_lo / MT, k_hi / MT, v_lo / conv.C, v_hi / conv.C))
    w("  0xx: 7 cm, n_e=%.2e fm^-3, mu_e=%.2e MeV -> no degeneracy pressure, no neutronization"
      % (N_E / L_7CM, mu_e_3d(L_7CM)))
    w("")

    # ---- main table
    w("| E/S/W combination | state of matter | energy ledger | what the eye sees | duration | verdict |")
    w("|---|---|---|---|---|---|")
    row("✓✓✓", "1 fm, 0.30ρ_nuc, E_F=73.4 MeV",
        "41.2 Mt all locked inside",
        "mirror (two states ΔR=0.001), no self-emission",
        "3–5 ns",
        "**empty**")
    row("✓✓✗", "after neutronization Y_p=0.005, E_F=21.5 MeV",
        "23.1 Mt → ν (invisible); 18.1 Mt still locked inside",
        "mirror, no self-emission; ν burst needs a 10 kt-class detector",
        "3 ns",
        "**empty** + neutrino burst")
    row("✓✗✓", "1 fm disintegration → thermalization in a meter-scale gas column",
        "20.6 Mt kinetic → fireball; 20.6 Mt γ",
        "**41 Mt fireball, 99× solar surface**",
        "**1–10 s colored**",
        "**fireball (most spectacular)**")
    row("✓✗✗", "ν burst first (3 ns), then disintegration",
        "23.1 Mt → ν; KE 4.4–15.5 Mt",
        "weaker fireball (2–5 times dimmer)",
        "~1–10 s",
        "weak fireball + ν burst")
    row("✗✓✓", "7 cm, 1000 kg/m³, atoms intact",
        "no extra energy (not compressed)",
        "passively reflects 35% of sunlight (same as a white wall)",
        "infinite",
        "static sheet (clear, not spectacular)")
    row("✗✓✗", "same as above (W has no target: μ_e=4 eV)",
        "same as above", "same as above", "infinite", "≡ ✗✓✓")
    row("✗✗✓", "same as above (S has no target: no degeneracy pressure)",
        "same as above", "same as above", "infinite", "≡ ✗✓✓")
    row("✗✗✗", "same as above (all three fail)",
        "same as above", "same as above", "infinite", "≡ ✗✓✓")
    w("")

    # ---- dependency structure
    w("=" * 78)
    w("[Dependency structure] 8 combinations -> 5 distinct outcomes")
    w("=" * 78)
    w("  {111}            empty (mirror, 3 ns)")
    w("  {110}            empty + neutrino burst")
    w("  {101}            41 Mt fireball  <- the only spectacular one")
    w("  {100}            weak fireball + neutrino burst")
    w("  {011,010,001,000} same outcome: 7 cm static sheet")
    w("")
    w("  Reason: E is the only energy source. ¬E => μ_e drops from 73.4 MeV to 4.2e-3 MeV,")
    w("  degeneracy pressure disappears (nothing for S to do), and the neutronization threshold is no longer crossed (nothing for W to do).")
    w("  So the last three combinations share the same physical state; they are not four things but one.")
    w("")
    w("[Inverse relation] Visual effect vs number of assumptions holding")
    w("  3 hold -> empty")
    w("  2 hold -> empty (110) or fireball (101)")
    w("  1 holds -> static sheet")
    w("  0 hold -> static sheet")
    w("  => visual intensity has no monotonic relation to the 'number of assumptions holding'; it depends only on 'whether S is abandoned and E is kept'.")
    w("")
    w("[Only simultaneous condition] To see anything, all of the following must hold at once:")
    w("  (a) MeV-scale energy available for release -> requires E to hold")
    w("  (b) release is allowed -> requires ¬S")
    w("  (c) energy is not carried away by nu -> requires W to hold")
    w("  => 101 is the only solution. E supplies energy, ¬S supplies visibility, W keeps 44% from going to waste.")

    txt = "\n".join(OUT)
    import io
    io.open("runs/ANALYSIS/assumption_matrix_v1.txt", "w", encoding="utf-8").write(txt + "\n")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print(txt)


if __name__ == "__main__":
    main()
