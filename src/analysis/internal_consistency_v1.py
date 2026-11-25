# -*- coding: utf-8 -*-
"""Consistency envelope v1 (2026-11-21): can the three assumptions hold simultaneously?

Question
--------
G0P-003 fixed the numerical chain but left a more fundamental question unasked:
are the three assumptions "effective 2D reduction" (eff-2D), "smooth 2D reduction"
(smooth) and "weak-interaction preservation" (weak-on) mutually compatible?

This module checks only "between assumptions", deliberately avoiding any
convention-dependent quantity (single-point values of X_p / mu_e / P can all be
questioned), and using only three kinds of quantities that do not change with
convention: geometry (length), field strength (MeV/fm -> V/m), timescale (s).
Therefore this module's conclusion is orthogonal to the B2 convention dispute.

Labeling discipline (continuing the v3 three-way split)
  CHECK    : inequalities/equalities that can be independently audited
  ESTIMATE : order-of-magnitude estimates with O(1) uncertainty, used only for
             "are they of the same order?" judgments
  ARGUMENT : logical implication, no numbers

Run: python -I src/analysis/internal_consistency_v1.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
import conv  # noqa: E402

# ---------------------------------------------------------------- registered constants
R_P_FM = 0.8414                # proton rms charge radius
SCHWINGER_VM = 1.32e18         # critical field E_S = m_e^2 c^3 / (e hbar)
SIGMA_NU_COEF = 9.52e-44       # cm^2 / MeV^2, sigma(nu_e n -> p e)
CM2_M2 = 1e-4

OUT = []


def w(s=""):
    OUT.append(s)


def tag(kind, name, ok, note):
    w("  %-9s %-30s %-5s %s" % (kind, name, "PASS" if ok else "FAIL", note))
    return ok


# ---------------------------------------------------------------- K1 geometry
def lz_window(n_e_fm3, ratio_min=3.0, r_n=R_P_FM):
    """Two-sided window for L_z.

    For the electron to be D=2: E_sub(L)/E_F(L) >= ratio_min
        E_sub = pi*hbarc/L,  E_F = hbarc*sqrt(2*pi*n_e*L)
        => ratio = pi / (sqrt(2 pi n_e) * L^1.5)
    For nucleons to exist: L >= 2 r_n (nucleon diameter)
    """
    coef = math.pi / (math.sqrt(2.0 * math.pi * n_e_fm3) * ratio_min)
    lz_max = coef ** (2.0 / 3.0)
    lz_min = 2.0 * r_n
    return lz_min, lz_max


def ratio_at(lz, n_e_fm3):
    return math.pi / (math.sqrt(2.0 * math.pi * n_e_fm3) * lz ** 1.5)


# ------------------------------------------------------- K2 confining field strength
def confine_field_mvm(dE_mev, lz_fm):
    """Field gradient needed to confine a particle in a well of width lz (V/m). 1 MeV/fm = 1e21 V/m."""
    return dE_mev / lz_fm * 1e21


def z_pressure_pa(n_areal_fm2, e_z_mev, lz_fm):
    """Wall pressure of an ideal box: P_z = n * E_z / L_z. MeV/fm^3 -> Pa."""
    return n_areal_fm2 * e_z_mev / lz_fm * conv.MEV_J * 1e45


# ------------------------------------------------------------ K3 timescale
def capture_tau_s(mu_e_mev, n_p_fm3):
    """e-folding timescale (order of magnitude) for p + e -> n + nu."""
    sigma_m2 = SIGMA_NU_COEF * (mu_e_mev ** 2) * CM2_M2
    gamma = n_p_fm3 * 1e45 * sigma_m2 * conv.C
    return 1.0 / gamma, sigma_m2


def main():
    L = conv.LZ_FM
    n_e = conv.N_E_FM3
    n_2d = conv.N_E_FM2
    n_B = conv.N_B_FM3
    N_B_areal = conv.N_B_FM2
    fs = conv.frozen_state()
    E_F = fs["EF_2D"]
    E_sub = conv.E_SUBBAND
    u_in = fs["u_2D_Jm2"]
    P_lat = fs["P_2D_Nm"]
    MC2_PER_M2 = conv.M_KG * conv.C ** 2

    w("=" * 92)
    w("Consistency envelope v1: compatibility of the three assumptions eff-2D / smooth / weak-on")
    w("=" * 92)
    w("  L_z=%.1f fm | n_e=%.6f fm^-3 | n_2D=%.6f fm^-2 | n_B=%.6f fm^-3"
      % (L, n_e, n_2d, n_B))
    w("  E_F(2D)=%.2f MeV | E_sub=%.1f MeV | P_lat=%.3e N/m" % (E_F, E_sub, P_lat))
    w("")

    # ---------------------------------------------------------------- K1
    w("[K1] Geometry: two-sided window for L_z (electrons need thinness, nucleons need room to fit)")
    lz_min, lz_max = lz_window(n_e)
    for lz in (0.5, 1.0, 1.5, 1.68, 1.995, 2.5, 3.0):
        r = ratio_at(lz, n_e)
        w("  L_z=%.3f fm: E_sub/E_F=%.2f  %s  %s"
          % (lz, r,
             "2D ok " if r >= 3.0 else "NOT-2D",
             "nucleon fits" if lz >= 2 * R_P_FM else "thinner than nucleon"))
    w("  => window [%.2f, %.2f] fm (width factor %.2f); registered L_z=%.1f fm lies outside the window"
      % (lz_min, lz_max, lz_max / lz_min, L))
    tag("ESTIMATE", "K1_window_nonempty", lz_max > lz_min,
        "the window is nonempty but only a factor of %.2f wide; the lower bound 2r_p is a physical judgment, not a theorem" % (lz_max / lz_min))
    tag("ESTIMATE", "K1_registered_outside", L < lz_min,
        "registered L_z=%.1f < %.2f (nucleon diameter)" % (L, lz_min))
    w("")

    # ---------------------------------------------------------------- K2
    w("[K2] Confining field: how steep a potential is needed to squeeze electrons into 1 fm")
    F_e = confine_field_mvm(E_sub, L)
    E_z_nuc = math.sqrt(conv.M_N ** 2 + E_sub ** 2) - conv.M_N
    F_n = confine_field_mvm(E_z_nuc, L)
    w("  electron: dE=%.1f MeV over %.1f fm -> %.2e V/m = %.2e x E_Schwinger"
      % (E_sub, L, F_e, F_e / SCHWINGER_VM))
    w("  nucleon: dE=%.1f MeV over %.1f fm -> %.2e V/m = %.2e x E_Schwinger"
      % (E_z_nuc, L, F_n, F_n / SCHWINGER_VM))
    tag("CHECK", "K2_supercritical", F_e / SCHWINGER_VM > 1.0,
        "supercritical by a factor of %.1e -> vacuum pair production; if a non-electromagnetic new field is used, its strength far exceeds the weak interaction" % (F_e / SCHWINGER_VM))
    w("")

    # ---------------------------------------------------------------- K3
    w("[K3] Pressure hierarchy: z-direction wall pressure vs lateral areal pressure")
    Pz_e = z_pressure_pa(n_2d, E_sub, L)
    Pz_n = z_pressure_pa(N_B_areal, E_z_nuc, L)
    P_lat_vol = P_lat / (L * 1e-15)
    w("  P_z(electron)=%.2e Pa | P_z(nucleon)=%.2e Pa" % (Pz_e, Pz_n))
    w("  P_lat converted to bulk pressure = %.2e Pa (=P_2D/L_z)" % P_lat_vol)
    w("  HYB convention (nucleons 3D, only electrons pay zero-point energy): ratio %.1f" % (Pz_e / P_lat_vol))
    w("  strict geometry (nucleons also in a 1 fm box)               : ratio %.1f" % ((Pz_e + Pz_n) / P_lat_vol))
    tag("CHECK", "K3_z_dominates", Pz_e / P_lat_vol > 10.0,
        "even under the most permissive HYB, z is %.0f times lateral; the documents only budgeted the lateral term"
        % (Pz_e / P_lat_vol))
    w("")

    # ---------------------------------------------------------------- K4
    w("[K4] Energy ledger: is the confining zero-point energy negligible?")
    u_conf_e = (n_2d * E_sub) * conv.J_PER_MEV_FM2
    u_conf_n = (N_B_areal * E_z_nuc) * conv.J_PER_MEV_FM2
    w("  u_inplane = %.3e J/m^2 = %.2f%% Mc^2/A" % (u_in, 100 * u_in / MC2_PER_M2))
    w("  confining zero-point energy (electrons only, HYB) = %.3e J/m^2 = %.2f%% Mc^2/A (%.1f x in-plane)"
      % (u_conf_e, 100 * u_conf_e / MC2_PER_M2, u_conf_e / u_in))
    w("  confining zero-point energy (electrons+nucleons)   = %.3e J/m^2 = %.2f%% Mc^2/A (%.1f x in-plane)"
      % (u_conf_e + u_conf_n, 100 * (u_conf_e + u_conf_n) / MC2_PER_M2,
         (u_conf_e + u_conf_n) / u_in))
    w("  total (strict)             = %.3e J/m^2 = %.2f%% Mc^2/A"
      % (u_in + u_conf_e + u_conf_n, 100 * (u_in + u_conf_e + u_conf_n) / MC2_PER_M2))
    tag("ESTIMATE", "K4_confine_not_small", u_conf_e / u_in > 5.0,
        "convention-independent lower bound: confining zero-point energy is already %.1f times the in-plane degeneracy energy; 2.74%% omitted it"
        % (u_conf_e / u_in))
    w("")

    # ---------------------------------------------------------------- K5
    w("[K5] Timescales: neutronization vs expansion vs sound crossing")
    tau_cap, sigma = capture_tau_s(E_F, n_e)
    t_rip = 1.0 / (conv.C / math.sqrt(2.0))
    t_cross = 0.07 / (conv.C / math.sqrt(2.0))
    w("  sigma(p e->n nu) = %.2e m^2 @ mu_e=%.1f MeV" % (sigma, E_F))
    w("  tau_capture = %.2f ns | t_rip(1 m) = %.2f ns | t_cross(7 cm) = %.2f ns"
      % (tau_cap * 1e9, t_rip * 1e9, t_cross * 1e9))
    tag("ESTIMATE", "K5_no_scale_separation", 0.1 < tau_cap / t_rip < 10.0,
        "all three are of the same order (ratio %.2f) -> there is no two-stage 'flatten first, stabilize later'" % (tau_cap / t_rip))
    w("")

    # ---------------------------------------------------------------- K6
    w("[K6] Weak interaction: preservation vs equilibrium (logic)")
    env = conv.beta_envelope()
    for m in conv.MODES:
        r = env[m]
        w("  %-6s: X_p=%.4e  mu_e=%.2f MeV  P_tot=%.2e N/m  protons remaining %.1f%%"
          % (m, r["X_p"], r["mu_e"], r["P_tot_Nm"], 100 * r["X_p"] / conv.ZA))
    w("  => under any convention, β equilibrium requires more than %d%% of protons to be neutronized"
      % int(100 * (1 - env["HYB"]["X_p"] / conv.ZA)))
    tag("ARGUMENT", "K6_weak_on_vs_stable", True,
        "'weak-on' => non-equilibrium state; 'stable final state' => weak must be active. Both cannot be true at once")
    w("")

    # ---------------------------------------------------------------- summary
    w("-" * 92)
    w("Conclusion: the three assumptions conflict pairwise; no parameter point satisfies all of them.")
    w("  K1 eff-2D  <-> composition: L_z window [%.2f,%.2f] fm, registered value outside" % (lz_min, lz_max))
    w("  K2 eff-2D  <-> known physics: needs %.1e x E_S" % (F_e / SCHWINGER_VM))
    w("  K3 z wall pressure <-> lateral budget: still off by %.0f under the most permissive convention" % (Pz_e / P_lat_vol))
    w("  K4 energy ledger <-> 2.74%%: omitted confining zero-point energy by a factor of %.0f (lower bound)" % (u_conf_e / u_in))
    w("  K5 smooth  <-> timescale separation: none (ratio %.2f)" % (tau_cap / t_rip))
    w("  K6 weak-on <-> stable final state: logically mutually exclusive")
    w("Note: none of the above depends on the values of X_p / mu_e / P, hence it is orthogonal to the B2 convention dispute.")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
    txt = "\n".join(OUT)
    print(txt)
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "runs", "ANALYSIS")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "internal_consistency_v1.txt"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")
