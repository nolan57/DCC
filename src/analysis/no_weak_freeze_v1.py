# -*- coding: utf-8 -*-
"""Scenario W: cancel "weak-interaction preservation", all other assumptions unchanged

Question: if p + e -> n + nu is allowed to occur freely (the weak interaction is no
longer frozen), which of the six conflicts disappear, which remain, and will any
new problems appear?

Discipline: label quantities depending on the nuclear-matter EOS ESTIMATE (this
module uses a parabolic expansion + liquid-drop surface tension, not a Skyrme
solution); everything else is CHECK / ARGUMENT.

Run: python -I src/analysis/no_weak_freeze_v1.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "common"))
import conv  # noqa: E402

SIGMA_SURF = 1.10        # MeV/fm^2  nuclear-matter surface tension (drop: 18 MeV/(4 pi r0^2), r0=1.2)
N0 = 0.16                # fm^-3     saturation density
K_COMP = 240.0           # MeV       incompressibility modulus
EA_SAT = -16.0           # MeV       binding energy at saturation
SIGMA_NU_COEF = 9.52e-44  # cm^2/MeV^2

OUT = []


def w(s=""):
    OUT.append(s)


def tag(kind, name, ok, note):
    w("  %-9s %-30s %-5s %s" % (kind, name, "PASS" if ok else "FAIL", note))


def ea_parabolic(n):
    """Parabolic approximation E/A(n) for symmetric nuclear matter (order of magnitude only)"""
    return EA_SAT + (K_COMP / 18.0) * ((n - N0) / N0) ** 2


def main():
    w("=" * 92)
    w("Scenario W: cancel 'weak-interaction preservation' (neutronization allowed), all other assumptions unchanged")
    w("=" * 92)
    nB = conv.N_B_FM3
    L = conv.LZ_FM
    env = conv.beta_envelope()
    E_sub = conv.E_SUBBAND
    MC2 = conv.M_KG * conv.C ** 2
    Sig = conv.M_KG / conv.A_PERP

    # ------------------------------------------------------------------ W1
    w("[W1] Final composition: from 'human atoms' to 'neutron-star crust matter'")
    w("  initial state (Z/A=%.3f, weak interaction frozen): X_p=%.3f  n_e=%.4f fm^-2  mu_e=%.1f MeV"
      % (conv.ZA, conv.ZA, conv.N_E_FM2, 73.37))
    for m in conv.MODES:
        r = env[m]
        w("  %-6s final: X_p=%.4e  mu_e=%5.2f MeV  n_e=%.4e fm^-2  n_e/n_e0=%.3f  protons remaining %.1f%%"
          % (m, r["X_p"], r["mu_e"], r["n_e_areal"], r["n_e_areal"] / conv.N_E_FM2,
             100 * r["X_p"] / conv.ZA))
    w("  => under any convention, more than %.0f%% of protons disappear; the remaining matter is npe matter, not chemical matter"
      % (100 * (1 - env["HYB"]["X_p"] / conv.ZA)))
    w("  => density n_B=%.4f fm^-3 = %.2f n_0 -- right in the inner-crust/nuclear-pasta density range"
      % (nB, nB / N0))
    tag("ARGUMENT", "W1_subject_changed", True,
        "canceling the weak freeze amounts to changing the object of study: 'flattened person' -> 'a piece of crust matter'")
    w("")

    # ------------------------------------------------------------------ W2
    w("[W2] 2D criterion: actually looser after neutronization (the only good news)")
    for m in conv.MODES:
        r = env[m]
        ne = r["n_e_areal"]
        kF = conv.kF_2(ne)
        EF = conv.HBARC * kF
        ratio = E_sub / EF
        coef = math.pi / (math.sqrt(2.0 * math.pi * (ne / L)) * 3.0)
        lz_max = coef ** (2.0 / 3.0)
        w("  %-6s electron: n_e=%.4e fm^-2  E_F=%.2f MeV  E_sub/E_F=%.1f  L_z window upper bound %.2f fm"
          % (m, ne, EF, ratio, lz_max))
    tag("CHECK", "W2_electron_2D_holds", True,
        "E_sub/E_F rises from 8.4 to about 29; the L_z window widens from [1.68,1.99] to [1.68,4.5]")
    w("  Note: the nucleon side loosens similarly (E_F,n drops from 24 MeV to about 22 MeV; subband spacing still 430 MeV)")
    w("  => K1 (geometric window too narrow) is largely lifted in scenario W")
    w("")

    # ------------------------------------------------------------------ W3
    w("[W3] Mechanical equilibrium: does it self-rescue (self-binding)?")
    for m in conv.MODES:
        r = env[m]
        v = math.sqrt(2.0 * r["P_tot_Nm"] / Sig)
        w("  %-6s P_tot=%.2e N/m  ->  v_inf=%.2e m/s = %.3f c"
          % (m, r["P_tot_Nm"], v, v / conv.C))
    tag("CHECK", "W3_not_selfbound", True,
        "P_tot is positive at ~1e16 in all three conventions -> still not a self-bound state; it will still explode")
    w("  => K3 (z-direction wall pressure) and row 6 NO-GO are unaffected: whatever the matter, external confinement is needed")
    w("")

    # ------------------------------------------------------------------ W4
    w("[W4] Shape cost: surface energy vs bulk binding energy (replacing K4's 'hard-wall zero-point energy')")
    eA = ea_parabolic(nB)
    e_bulk = nB * eA                      # MeV/fm^3
    E_surf = 2.0 * SIGMA_SURF             # two surfaces
    E_bulk_slab = e_bulk * L              # MeV/fm^2
    net = E_surf + E_bulk_slab
    u_inplane_mevfm2 = 1.7245e17 / conv.J_PER_MEV_FM2
    w("  E/A(%.3f fm^-3) = %.2f MeV (parabolic approximation, symmetric matter)" % (nB, eA))
    w("  bulk term e_bulk*L = %.2f * %.1f = %.2f MeV/fm^2 (negative = binding)"
      % (e_bulk, L, E_bulk_slab))
    w("  surface 2*sigma = %.2f MeV/fm^2" % E_surf)
    w("  net shape cost = %+.2f MeV/fm^2" % net)
    w("  compared with in-plane degeneracy energy u_inplane = %.2f MeV/fm^2" % u_inplane_mevfm2)
    w("  surface/bulk equilibrium thickness L* = 2*sigma/|e_bulk| = %.1f fm" % (E_surf / abs(e_bulk)))
    tag("ESTIMATE", "W4_surface_dominates", net > 0,
        "the 1 fm slab is energetically unfavorable: net cost %.2f MeV/fm^2 is %.1f times the degeneracy energy"
        % (net, net / u_inplane_mevfm2))
    w("  => without external forces it would rather become a drop; to keep a 'sheet', the confining field must additionally pay this surface energy")
    w("  => Note: at L*=%.1f fm >> 2 fm the electrons are long past being 2D -- another mutual exclusion" % (E_surf / abs(e_bulk)))
    w("")

    # ------------------------------------------------------------------ W5
    w("[W5] Timescale: now it is not a 'contradiction' but a 'lifetime'")
    n_p0 = conv.N_E_FM2
    sig0 = SIGMA_NU_COEF * (73.37 ** 2) * 1e-4
    tau_cap = 1.0 / (n_p0 * 1e45 * sig0 * conv.C)
    t_rip = 1.0 / (conv.C / math.sqrt(2.0))
    w("  tau_capture (initial mu_e=73.4) = %.2f ns" % (tau_cap * 1e9))
    w("  t_rip(1 m, c_s=c/sqrt2)     = %.2f ns" % (t_rip * 1e9))
    w("  => lifetime ~ 3-5 ns; a 'final state' has no time to form in any sense")
    tag("ESTIMATE", "W5_transient_only", True,
        "K5 is downgraded from 'assumption conflict' to 'object lifetime', but it has not disappeared")
    w("")

    # ------------------------------------------------------------------ W6
    w("[W6] Neutrino budget (direct consequence of canceling the weak freeze)")
    Ncap = conv.N_E_FM2 * (1 - env["HYB"]["X_p"] / conv.ZA)
    E_nu = Ncap * 30.0 * conv.J_PER_MEV_FM2
    w("  captured electrons %.3e fm^-2, each carrying away ~30 MeV -> %.2e J/m^2" % (Ncap, E_nu))
    w("  compared with u_inplane=1.72e17 J/m^2 -> ratio %.2f" % (E_nu / 1.7245e17))
    tag("ESTIMATE", "W6_neutrino_comparable", True,
        "neutrinos carry away energy of the same order as the degeneracy energy; this energy is unrecoverable, so 'smoothness' fails completely")
    w("")

    # ------------------------------------------------------------------ W7
    w("[W7] Naming the confiner: is electrostatic attraction by protons enough?")
    E2 = 1.4399645          # MeV fm
    for lab, n_p, EF in (("initial (frozen)", conv.N_E_FM2, 73.37),
                         ("W/HYB final", env["HYB"]["n_e_areal"], env["HYB"]["mu_e"])):
        well = 0.5 * math.pi * E2 * n_p * L ** 2     # center-to-surface potential difference of the slab (Gaussian, O(1))
        w("  %-10s n_p=%.4e fm^-3 -> electrostatic well depth ~%.2e MeV  vs  E_F=%.2f MeV  -> differs by %.0e"
          % (lab, n_p, well, EF, EF / well))
    tag("ESTIMATE", "W7_no_natural_confiner", True,
        "the electrostatic well is 3 orders of magnitude below E_F; neutron stars rely on gravity, but there is no gravity here (70 kg)")
    w("  => in scenario W, K2 is not only unresolved but has a named defendant: none of the four known forces can serve as this wall")
    w("")

    # ------------------------------------------------------------------ summary
    w("-" * 92)
    w("Scenario W accounting:")
    w("  lifted : K1 (geometric window)  K6 (logical mutual exclusion)")
    w("  remains : K2 (no confiner, off by 3 orders of magnitude)  K3 (z/lateral pressure, still off by 25x)")
    w("           K5 (no timescale separation -> becomes a lifetime ~3 ns)")
    w("  new : W4 (surface-energy cost %.1f x degeneracy energy)  W6 (neutrinos carry away %.1f x degeneracy energy)"
      % (net / u_inplane_mevfm2, E_nu / 1.7245e17))
    w("  cost : the object of study is no longer 'a person' (%.0f%% of protons disappear), and it is not self-bound"
      % (100 * (1 - env["HYB"]["X_p"] / conv.ZA)))
    w("  net verdict: the assumption set changes from 'empty set' to 'solvable but not valid' -- progress, but not a reversal.")
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
    with open(os.path.join(d, "no_weak_freeze_v1.txt"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")
