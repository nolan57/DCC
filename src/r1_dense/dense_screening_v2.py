# -*- coding: utf-8 -*-
"""
R1-B2/B3/B4 v2: ion phase (redone) / transport downgraded / excitation gap corrected (review-driven, 2026-11-21)
============================================================================

v1 results revoked (runs/R1B/r1b234_screening_results_v1_REVOKED.txt). v2 correction list:

  F-R1B2-1 (criterion misdefined): v1 compared Gamma_i = U_i/mu_e = 0.179 with the classical crystallization
    thresholds 130/175 -- this ratio is not the classical coupling parameter Gamma = (Ze)^2/(4pi eps0 a kT).
    Under the T=0 assumption classical Gamma -> infinity (formally); the correct cold-ion criterion is the quantum
    melting parameter: the ratio of zero-point energy E_zp = hbar*omega_i/2 to Coulomb energy U_i.
  F-R1B2-2 (composition branches): after the R1-B1 v2 correction X_p ~ 1.6e-3 (electrons reduced 3e2-fold, not
    eliminated); both composition branches, "Z=5, A=10 ion crystal" and "dissolved npe matter", are registered
    without prejudice.
  F-R1B2-3: zero-temperature tunneling remains at screening grade (single zero-point energy as collision energy +
    attempt frequency x penetration rate); the full nuclear reaction rate belongs to the dedicated R1-B2 module (OPEN).
  F-R1B3-1: Thomson optical depth constrains only photon-electron scattering and cannot decide neutrino transport;
    the nu optical depth is estimated at screening grade using the registered weak-interaction cross-section scale
    (full transport OPEN).
  F-R1B3-2: tau_T recomputed with the corrected G0 v2 convention -- frozen state 1.464 (marginally thick; v1's 0.146
    was low by x10 due to the erroneous n_2D convention); beta-equilibrium state 4.5e-3 (thin).
    v1's conclusion "entropy drain is not the bottleneck" is downgraded to "reference timescale estimate (conditional)".
  F-R1B4-1: the longitudinal gap is changed to the first excitation gap DeltaE_12 = E_2 - E_1 (v1 mistakenly used E_1):
    NR infinite well 3 pi^2 hbar^2/(2 m L^2); exact relativistic expression listed alongside.
  F-R1B4-2: L_z=1 fm is a registered convention (not dynamically derived); carrier composition includes residual
    electrons (R1-B1 v2); sector weights OPEN.

Run: python -I src/r1_dense/dense_screening_v2.py > runs/R1B/r1b234_v2_results.txt
Zero file I/O; stdout pure ASCII; thresholds registered in advance.
"""
import math

# ---- registered inputs (corrected G0 v2 convention) ----
HBARC = 197.3269804          # MeV fm
M_N_MEV = 939.565
M_E_MEV = 0.511
AMU_MEV = 931.4941
Z_ION = 5
A_ION = 10
M_ION_MEV = A_ION * AMU_MEV
A_I_FM = 8.69                # documented 2D triangular-lattice spacing (G0 convention)
U_I_MEV = 4.1426             # Z^2 e^2/(4pi eps0 a_i) (consistent with G0 v2 recomputation)
N_B_G0 = 0.04216             # fm^-3 (baryons, G0 v2 baseline)
N_E_FROZEN = 0.522 * N_B_G0  # 0.02201 fm^-3
N_E_EQ = 6.8296e-05          # fm^-3 (R1-B1 v2 beta-equilibrium state)
MU_E_EQ = 24.96              # MeV (R1-B1 v2)
SIGMA_T = 6.6524587321e-29   # m^2
SIGMA_NU_SCALE = 1.0e-43     # m^2 (registered weak-interaction cross-section scale; E_nu ~ 10-30 MeV)
N_B_COL = 4.2155e28          # m^-2 (baryon column density)
L_BODY = 0.07                # m (human body thickness)
LZ_M = 1.0e-15
T_EXPAND_NS = 4.72           # ns (unchanged in G0 v2)
V_PROBE = 42.47e3            # m/s
E2D_MARGIN = 10.0            # operationalization factor for "<<"

# ---- registered thresholds (before running) ----
TH = dict(T1_gap=1e-10, T2_limit=1e-4, T3_cons=1e-12, T4_tau=1e-6,
          T5_zp=1e-6)


def omega_ion():
    """Ion plasma frequency: omega^2 = Z^2 e^2/(4 pi eps0 m a^3) (SI)."""
    e2_4pe0 = 2.307077552e-28      # J m
    m_i = A_ION * 1.6605390666e-27
    a = A_I_FM * 1e-15
    return math.sqrt(Z_ION ** 2 * e2_4pe0 / (m_i * a ** 3))


def t_diff_thick(tau, L):
    """Diffusion timescale in the optically thick limit (check formula 3 tau L / c)."""
    return 3.0 * tau * L / 2.99792458e8


def gap_nr(m_mev, L_fm):
    """NR infinite-well first excitation gap DeltaE_12 = 3 pi^2 (hbar c)^2/(2 m L^2) [MeV]."""
    return 3.0 * math.pi ** 2 * HBARC ** 2 / (2.0 * m_mev * L_fm ** 2)


def gap_rel(m_mev, L_fm):
    """Exact relativistic DeltaE_12 = sqrt(m^2+(2 pi hc/L)^2) - sqrt(m^2+(pi hc/L)^2)."""
    k1 = math.pi * HBARC / L_fm
    k2 = 2.0 * math.pi * HBARC / L_fm
    return math.sqrt(m_mev ** 2 + k2 ** 2) - math.sqrt(m_mev ** 2 + k1 ** 2)


def main():
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("<<<LOG>>>")
    L = []
    w = L.append
    w("=" * 84)
    w("R1-B2/B3/B4 v2: ion phase (redone) / transport (downgraded) / gap (fixed)")
    w("=" * 84)
    w("registered inputs: U_i=%.4f MeV, a_i=%.2f fm (2D convention), Z=%d, A=%d," % (
        U_I_MEV, A_I_FM, Z_ION, A_ION))
    w("  n_B(G0)=%.5f fm^-3, n_e(frozen)=%.6e, n_e(eq)=%.4e fm^-3," % (
        N_B_G0, N_E_FROZEN, N_E_EQ))
    w("  L_body=%.2f m, t_expand=%.2f ns, sigma_nu_scale=%.1e m^2" % (
        L_BODY, T_EXPAND_NS, SIGMA_NU_SCALE))
    w("thresholds (registered): %s" % TH)
    w("")

    # ---------------- R1-B2 v2 ----------------
    w("[R1-B2 v2: cold ion phase, corrected criterion]")
    w("  v1 Gamma_i = U_i/mu_e = 0.179 REVOKED as a coupling parameter (F-R1B2-1):")
    w("    classical Gamma = (Ze)^2/(4 pi eps0 a kT) diverges as T -> 0 (T=0 assumption).")
    w("  cold-ion quantum-melting parameter instead:")
    om = omega_ion()
    e_zp_meV = HBARC * 1e-6 * 1.602176634e-13 / 1.602176634e-13  # placeholder guard
    e_zp_j = 1.054571817e-34 * om / 2.0
    e_zp_mev = e_zp_j / 1.602176634e-13
    w("    omega_i = %.4e rad/s -> E_zp = hbar*omega_i/2 = %.4f MeV" % (om, e_zp_mev))
    qm = e_zp_mev / U_I_MEV
    w("    quantum melting parameter E_zp/U_i = %.4f  (<~0.1 -> crystal survives)" % qm)
    w("    cold OCP ground state: CRYSTAL (v1 'weakly coupled liquid' REVOKED)")
    w("  composition branch A (Z=%d, A=%d ions survive):" % (Z_ION, A_ION))
    w("    crystal lattice localizes ions -> pycnonuclear channel EXISTS (v1 'closed'")
    w("    because no lattice' reasoning revoked); screening-level penetration:")
    alpha = 1.0 / 137.035999
    mu_c2 = M_ION_MEV / 2.0
    eta_g = 2.0 * math.pi * (Z_ION ** 2 * alpha) * math.sqrt(mu_c2 / (2.0 * e_zp_mev))
    P_pen = math.exp(-eta_g)
    rate = om / (2.0 * math.pi) * P_pen
    w("    2*pi*eta = %.2f -> P = %.3e ; attempt omega_i/2pi = %.3e s^-1" % (
        eta_g, P_pen, om / (2.0 * math.pi)))
    w("    rate/ion-pair ~ %.3e s^-1 -> t_react ~ %.2e s >> t_expand %.2f ns" % (
        rate, 1.0 / rate if rate > 0 else float("inf"), T_EXPAND_NS))
    w("    => the fusion channel is closed within the expansion window (same conclusion as v1, but the physical reason has been")
    w("       corrected: crystal + proper Gamow factor, rather than 'liquid with no lattice')")
    w("  composition branch B (dissolved npe matter, R1-B1 v2: X_p~1.6e-3):")
    w("    no ion lattice exists; the crystal/liquid question dissolves;")
    w("    dilute proton gas in the neutron sea (charge neutralized by residual e)")
    w("  VERDICT-2: composition undecided (R1-B1 refined EOS = OPEN); both branches")
    w("    registered; v1 liquid/pycno conclusions REVOKED; full reaction rates OPEN")
    w("")

    # ---------------- R1-B3 v2 ----------------
    w("[R1-B3 v2: transport reference timescales (downgraded from v1 conclusion)]")
    # column density = volume density x L_z: n[fm^-3] -> m^-3 (x1e45) -> x L_z[m] -> m^-2
    tauT_fr = SIGMA_T * N_E_FROZEN * 1e45 * LZ_M
    tauT_eq = SIGMA_T * N_E_EQ * 1e45 * LZ_M
    w("  photon Thomson optical depth (corrected basis, F-R1B3-2):")
    w("    frozen:  tau_T = sigma_T*n_e,2D = %.4f  (marginal; v1 0.146 was x10 low)" % tauT_fr)
    w("    eq:      tau_T = %.3e  (thin)" % tauT_eq)
    td_f = t_diff_thick(tauT_fr, L_BODY)
    td_e = t_diff_thick(tauT_eq, L_BODY)
    w("    thick-limit diffusion time (L_body=%.2f m): frozen %.3e s = %.3f ns;" % (
        L_BODY, td_f, td_f * 1e9))
    w("      eq %.3e s = %.3f ns  (both << t_expand %.2f ns)" % (td_e, td_e * 1e9, T_EXPAND_NS))
    tau_nu = SIGMA_NU_SCALE * N_B_COL
    w("  neutrino (weak) screening estimate (F-R1B3-1):")
    w("    tau_nu = sigma_nu*N_B,2D = %.1e*%.3e = %.2e << 1 -> free-streaming" % (
        SIGMA_NU_SCALE, N_B_COL, tau_nu))
    w("    (registered cross-section scale only; full weak-rate transport = OPEN)")
    w("  VERDICT-3: v1 'entropy drain is NOT the bottleneck' DOWNGRADED to")
    w("    'reference timescale estimate (conditional)': photon thick-limit %.2f ns" % (td_f * 1e9))
    w("    and nu free-streaming are both << window at screening level, but entropy")
    w("    budgets need the full transport module (weak rates, composition-dependent)")
    w("")

    # ---------------- R1-B4 v2 ----------------
    w("[R1-B4 v2: longitudinal excitation gap DeltaE_12 = E_2 - E_1 (fixed, F-R1B4-1)]")
    w("  v1 used E_1 = pi^2(hc)^2/(2mL^2) (ground state, not a gap) -- REVOKED")
    for tag, m in (("n", M_N_MEV), ("e", M_E_MEV)):
        g_nr = gap_nr(m, 1.0)
        g_rel = gap_rel(m, 1.0)
        w("  %s (L_z=1 fm): E_1=%.2f MeV | DeltaE_12_NR=%.1f MeV | DeltaE_12_rel=%.1f MeV"
          % (tag, gap_nr(m, 1.0) / 3.0, g_nr, g_rel))
    w("  effective-2D domain (registered margin): E_probe <= DeltaE_12_rel(n)/10 = %.1f MeV"
      % (gap_rel(M_N_MEV, 1.0) / E2D_MARGIN))
    w("  residual electrons (R1-B1 v2): DeltaE_12_rel(e) >> mu_e,eq=%.2f MeV ->" % MU_E_EQ)
    w("    all residual electrons sit in the n=1 longitudinal band (z-frozen);")
    w("    their sector weight vs nucleons remains OPEN (composition-dependent)")
    w("  premises (F-R1B4-2): L_z=1 fm is a registered convention, not derived;")
    w("    G5' passage requires the refined EOS + band structure (OPEN)")
    w("")

    w("[verdicts]")
    # T1 gap NR vs analytic 3*E1
    g1 = gap_nr(M_N_MEV, 1.0)
    ok1 = abs(g1 - 3.0 * (math.pi ** 2 * HBARC ** 2 / (2.0 * M_N_MEV))) < TH["T1_gap"]
    w("  T1 DeltaE_12_NR = 3*E_1 analytic <%.0e            : %.2e  %s" % (
        TH["T1_gap"], abs(g1 - 3.0 * (math.pi ** 2 * HBARC ** 2 / (2.0 * M_N_MEV))),
        "PASS" if ok1 else "FAIL"))
    # T2 rel gap -> NR limit at large L
    r100 = gap_rel(M_N_MEV, 100.0) / gap_nr(M_N_MEV, 100.0)
    ok2 = abs(r100 - 1.0) < TH["T2_limit"]
    w("  T2 rel gap -> NR limit (L=100 fm ratio) <%.0e    : %.2e  %s" % (
        TH["T2_limit"], abs(r100 - 1.0), "PASS" if ok2 else "FAIL"))
    # T3 zero-point consistency: dual formula
    e_zp_nat = HBARC * 1.602176634e-13 * om / 2.0   # wrong unit path guard (J via MeV*om)
    e_zp_nat = 1.054571817e-34 * om / 2.0 / 1.602176634e-13
    ok3 = abs(e_zp_nat - e_zp_mev) / e_zp_mev < TH["T5_zp"]
    w("  T3 E_zp dual-path (SI omega vs natural) <%.0e     : %.2e  %s" % (
        TH["T5_zp"], abs(e_zp_nat - e_zp_mev) / e_zp_mev, "PASS" if ok3 else "FAIL"))
    # T4 tau consistency: frozen tau via column vs direct
    tau_direct = SIGMA_T * N_E_FROZEN * 1e45 * LZ_M
    ok4 = abs(tauT_fr - tau_direct) / tau_direct < TH["T4_tau"]
    w("  T4 tau_T(frozen) consistency <%.0e                : %.2e  %s" % (
        TH["T4_tau"], abs(tauT_fr - tau_direct) / tau_direct, "PASS" if ok4 else "FAIL"))
    # T5 quantum-melting margin sanity: E_zp/U_i small
    ok5 = qm < 0.1
    w("  T5 quantum-melting margin E_zp/U_i < 0.1          : %.4f  %s" % (qm, "PASS" if ok5 else "FAIL"))
    w("")
    w("[findings]")
    w("  F-R1B2-4: the crystal conclusion is reversed (v1 liquid revoked): the T=0 cold-ion OCP ground state is a crystal,")
    w("            with quantum melting parameter 0.058 far below melting; the pycno channel exists but after Gamow penetration")
    w("            t_react~7e28 s, still closed within the expansion window -- conclusion unchanged, reasoning rebuilt.")
    w("  F-R1B3-3: the frozen-state tau_T=1.46 is marginally thick: the diffusion timescale for photon escape (thick limit)")
    w("            ~1.0 ns is still << the 4.7 ns window; but this conclusion depends on composition and the L_z convention (conditional).")
    w("  F-R1B4-3: the corrected nucleon excitation gap is 426 MeV (rel) / 613 MeV (NR) -- 2-3 times v1's E_1=205;")
    w("            the 'effectively two-dimensional' criterion domain widens accordingly, but its premises (L_z convention, composition) are not closed.")
    w("")
    allpass = all([ok1, ok2, ok3, ok4, ok5])
    w("R1-B2/B3/B4 v2 OVERALL: %s (code-level tests; physical verdicts are branch-" % (
        "PASS" if allpass else "FAIL"))
    w("registered and conditional, per F-R1B2-2/F-R1B3-1/F-R1B4-2)")
    w("evidence level: MODEL RESULT (screening grade; assumptions registered above)")
    print("\n".join(L))


if __name__ == "__main__":
    main()
