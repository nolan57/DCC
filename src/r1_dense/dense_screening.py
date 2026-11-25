# -*- coding: utf-8 -*-
"""
R1-B2/B3/B4 screening module (v1.4 roadmap s8.3 rows R1-B2, R1-B3, R1-B4;
Sprint-1 screening grade). Evidence level capped at MODEL RESULT.

Registered inputs (transcribed from runs/G0/g0_prime_results.json pathA block; the file is
NOT read - zero file I/O constraint; values rounded per the task-line registered constants):
  Gamma_i = 0.179, Gamma_e = 7.14e-3, U_i = 4.14 MeV, a_i = 8.69 fm, Z = 5, m_i = 10 amu,
  tau_T = 0.146, L_z = 1 fm, t_expand = 4.7 ns, v_probe = 42.47 km/s, mu_e(frozen) = 23.20 MeV.
Carrier data transcribed from the completed R1-B1 module (beta_equilibrium.py output):
  X_p(G0 density, beta equilibrium) ~ 1e-5 (scan cross-ref 2.9e-7 at 0.0251 fm^-3),
  mu_e(beta equilibrium, G0 density) = 1.29 MeV.

Registered screening model:
  B2: crystallization thresholds Gamma_c(3D OCP) = 175, Gamma_c(2D triangular) = 130;
      zero-temperature tunnelling penetrability P = exp(-2 pi eta),
      eta = Z^2 e^2/(4 pi eps0 hbar) * sqrt(mu / (2 E_cm)), E_cm = hbar omega_i / 2,
      omega_i = sqrt(Z^2 e^2 / (4 pi eps0 m_i a_i^3)) (registered formula), mu = m_i / 2;
      attempt frequency omega_i/(2 pi); reaction timescale compared to t_expand = 4.7 ns.
  B3: thick-limit diffusion timescale t_diff = 3 tau L / c; thin-limit free streaming
      t_esc = L / c; branch criterion tau >= 1 -> thick, tau < 1 -> thin (registered).
  B4: longitudinal box gap DeltaE_z = pi^2 hbar^2 / (2 m L_z^2) at L_z = 1 fm (registered
      non-relativistic form); effective-2D criterion E_probe << DeltaE_z, operationalized
      as E_probe <= DeltaE_z / 10 (registered margin factor).

Zero file I/O (sandbox hook constraint): results printed to stdout, ASCII only.
Run:  cd D:/Docs/DCC && python -I src/r1_dense/dense_screening.py > runs/R1B/r1b234_screening_results.txt
"""
import math
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------- registered G0 pathA inputs
GAMMA_I = 0.179            # ion coupling (G0 pathA, rounded)
GAMMA_E = 7.14e-3          # electron coupling (G0 pathA, rounded)
U_I_REG_MEV = 4.14         # ion Coulomb energy (G0 pathA)
A_I_FM = 8.69              # ion Wigner-Seitz radius [fm]
Z_ION = 5
M_I_AMU = 10.0
TAU_T = 0.146              # Thomson optical depth (free-electron reference value)
LZ_FM = 1.0                # dense-layer thickness convention (v1.4 s3.4)
T_EXPAND_S = 4.7e-9        # expansion timescale of the 1 m body
V_PROBE_KMS = 42.47
MU_E_FROZEN_MEV = 23.20    # frozen-compression electron chemical potential (removed sector)
MU_E_BETAEQ_MEV = 1.29     # beta-equilibrium mu_e at G0 density (R1-B1)
X_P_REG = 1.0e-5           # beta-equilibrium proton fraction at G0 density (R1-B1)
X_P_SCAN = 2.9e-7          # R1-B1 scan cross-ref at 0.0251 fm^-3
SIGMA_KGM2 = 70.0          # areal mass (G0)
B_ION = 2.4e-9             # N8 window edge; R1-B domain is B < B_ion

# ---------------------------------------------------------------- registered thresholds
GAMMA_C_3D = 175.0         # 3D OCP crystallization coupling (registered)
GAMMA_C_2D = 130.0         # 2D triangular Wigner crystallization coupling (registered)
TAU_THICK = 1.0            # optical-depth branch criterion
EFF2D_MARGIN = 10.0        # "<<" operationalized: E_probe <= DeltaE_z / 10
TH_REL = 1.0e-6            # T1/T2/T4 regression tolerance
TH_CONS = 1.0e-2           # C1/C2 registered-input consistency tolerance
TH_AUX = 1.0e-4            # AUX eta cross-path tolerance

# ---------------------------------------------------------------- constants (SI, G0 set)
HBAR = 1.054571817e-34
C_M_S = 299792458.0
E_C = 1.602176634e-19
EPS0 = 8.8541878128e-12
AMU = 1.6605390666e-27
MEV_J = 1.602176634e-13
M_E = 9.1093837015e-31
M_N = 1.67492749804e-27
M_P = 1.67262192369e-27
E2_4PEPS0 = E_C ** 2 / (4.0 * math.pi * EPS0)          # J m
# natural-unit set (registered independently, for cross-path regressions)
HBARC = 197.3269804        # MeV fm
E2_MEVFM = 1.439964548     # MeV fm
M_N_MEV = 939.56542052
M_P_MEV = 938.27208816
M_E_MEV = 0.51099895069
AMU_MEV = 931.49410242


def t_diff_thick(tau, L):
    """Optically thick limit: diffusion timescale 3 tau L / c."""
    return 3.0 * tau * L / C_M_S


def t_diff_indep(tau, L):
    """Independent path: t = L^2/D with D = c l / 3 and l = L / tau."""
    l_mfp = L / tau
    D_coef = C_M_S * l_mfp / 3.0
    return L * L / D_coef


def t_esc(L):
    """Optically thin limit: free streaming at c."""
    return L / C_M_S


def dez_si(m_kg):
    """Longitudinal box gap, SI numeric path: pi^2 hbar^2 / (2 m L^2) -> MeV."""
    L_m = LZ_FM * 1.0e-15
    return math.pi ** 2 * HBAR ** 2 / (2.0 * m_kg * L_m ** 2) / MEV_J


def dez_nat(m_mev):
    """Longitudinal box gap, natural-unit analytic path: (pi hbar c)^2 / (2 m c^2 L^2)."""
    return (math.pi * HBARC) ** 2 / (2.0 * m_mev * LZ_FM ** 2)


def dez_rel(m_mev):
    """Relativistic exact infinite-well ground state: sqrt((pi hbar c/L)^2 + (m c^2)^2) - m c^2."""
    pz = math.pi * HBARC / LZ_FM
    return math.sqrt(pz * pz + m_mev * m_mev) - m_mev


def verdict_line(name, ok, val):
    print("  %-72s : %-10s %s" % (name, val, "PASS" if ok else "FAIL"))


def main():
    bar = "=" * 88
    print(bar)
    print("R1-B2/B3/B4 screening module (v1.4 s8.3, Sprint-1 screening grade)")
    print(bar)
    print("registered inputs (transcribed from G0 pathA + R1-B1 outputs; files NOT read - zero I/O):")
    print("  Gamma_i = 0.179, Gamma_e = 7.14e-03, U_i = 4.14 MeV, a_i = 8.69 fm, Z = 5, m_i = 10 amu")
    print("  tau_T = 0.146, L_z = 1 fm, t_expand = 4.7 ns, v_probe = 42.47 km/s, mu_e(frozen) = 23.20 MeV")
    print("  carriers (R1-B1): X_p ~ 1e-05 (scan 2.9e-07), mu_e(beta-eq) = 1.29 MeV, electrons removed (N7)")
    print("registered thresholds: Gamma_c(3D OCP) = 175, Gamma_c(2D) = 130; branch tau >= 1 -> thick;")
    print("  T1/T2/T4 rel dev < 1e-06; C1/C2 consistency < 1e-02; AUX < 1e-04; eff-2D margin factor 10")

    # ================================================================ R1-B2
    a_i_m = A_I_FM * 1.0e-15
    m_i_kg = M_I_AMU * AMU
    k_sp = Z_ION ** 2 * E2_4PEPS0 / a_i_m ** 3            # spring constant [kg/s^2]
    omega_i = math.sqrt(k_sp / m_i_kg)                     # registered formula
    hw_i_MeV_SI = HBAR * omega_i / MEV_J
    E_cm_MeV_SI = 0.5 * hw_i_MeV_SI
    # natural-unit cross path (T4)
    k_nat = Z_ION ** 2 * E2_MEVFM / A_I_FM ** 3            # MeV/fm^2
    m_i_nat = M_I_AMU * AMU_MEV                            # MeV
    hw_i_MeV_nat = math.sqrt(k_nat * HBARC ** 2 / m_i_nat)
    E_cm_MeV_nat = 0.5 * hw_i_MeV_nat
    t4_dev = abs(E_cm_MeV_SI - E_cm_MeV_nat) / E_cm_MeV_nat
    mu_kg = 0.5 * m_i_kg
    E_cm_J = E_cm_MeV_SI * MEV_J
    eta = (Z_ION ** 2 * E2_4PEPS0 / HBAR) * math.sqrt(mu_kg / (2.0 * E_cm_J))
    P_tun = math.exp(-2.0 * math.pi * eta)
    nu_try = omega_i / (2.0 * math.pi)
    rate = P_tun * nu_try
    t_react = 1.0 / rate
    ratio_t = t_react / T_EXPAND_S
    U_i_comp = Z_ION ** 2 * E2_4PEPS0 / a_i_m / MEV_J
    gamma_comp = U_i_comp / MU_E_FROZEN_MEV
    c1_ok = abs(U_i_comp - U_I_REG_MEV) / U_I_REG_MEV <= TH_CONS
    c2_ok = abs(gamma_comp - GAMMA_I) / GAMMA_I <= TH_CONS
    # eta cross path (AUX)
    mu_nat = 0.5 * M_I_AMU * AMU_MEV
    beta_nat = math.sqrt(2.0 * E_cm_MeV_nat / mu_nat)
    eta_nat = Z_ION ** 2 * (E2_MEVFM / HBARC) / beta_nat
    aux_dev = abs(eta - eta_nat) / eta

    print("")
    print("[R1-B2 phase screening]")
    print("  Gamma_i = 0.179 < Gamma_c(2D) = 130 < Gamma_c(3D) = 175 -> weakly coupled ion LIQUID")
    print("    under both the 2D and the 3D crystallization thresholds (phase boundaries registered)")
    print("  Gamma_e = 7.14e-03 -> electron sector weakly coupled (degenerate background, registered)")
    print("  determination: no Wigner crystal forms; the pycnonuclear (crystal-lattice zero-point)")
    print("    channel is CLOSED at this Gamma (no lattice to localize ions)")
    print("  input consistency: U_i computed = %.6f MeV vs registered 4.14 (dev %.2e);" % (U_i_comp, abs(U_i_comp - U_I_REG_MEV) / U_I_REG_MEV))
    print("    Gamma_i = U_i/mu_e recomputed = %.6f vs registered 0.179 (dev %.2e)" % (gamma_comp, abs(gamma_comp - GAMMA_I) / GAMMA_I))
    print("")
    print("[R1-B2 zero-temperature tunnelling estimate (registered formulas)]")
    print("  omega_i = sqrt(Z^2 e^2/(4 pi eps0 m_i a_i^3)) = %.6e rad/s" % omega_i)
    print("  hbar*omega_i = %.6f MeV ; E_cm = hbar*omega_i/2 = %.6f MeV" % (hw_i_MeV_SI, E_cm_MeV_SI))
    print("    (zero-point scale is %.1f%% of the ion Coulomb scale U_i = 4.14 MeV)" % (100.0 * E_cm_MeV_SI / U_I_REG_MEV))
    print("  mu = m_i/2 = 5 amu ; v = sqrt(2 E_cm/mu) = %.6e m/s (beta = %.6f)" % (math.sqrt(2.0 * E_cm_J / mu_kg), math.sqrt(2.0 * E_cm_J / mu_kg) / C_M_S))
    print("  eta = (Z^2 e^2/(4 pi eps0 hbar)) sqrt(mu/(2 E_cm)) = %.6f" % eta)
    print("  P = exp(-2 pi eta) = %.6e" % P_tun)
    print("  attempt frequency omega_i/(2 pi) = %.6e 1/s" % nu_try)
    print("  rate = P * attempt = %.6e 1/s ; t_react = 1/rate = %.6e s" % (rate, t_react))
    print("  t_react / t_expand(4.7 ns) = %.3e" % ratio_t)
    if ratio_t > 1.0:
        print("  verdict: reaction timescale >> expansion timescale -> fusion channel CLOSED on the")
    else:
        print("  verdict: reaction timescale <= expansion timescale -> fusion channel NOT suppressed")
    print("    expansion timescale at the registered E_cm (screening level: E_cm = zero-point proxy;")
    print("    Gamow-peak / tail-integrated pycnonuclear rates deferred to the full R1-B2 module)")

    # ================================================================ R1-B3
    t1_dev = 0.0
    for L in (1.0e-15, 1.0):
        a1v = t_diff_thick(TAU_T, L)
        a2v = t_diff_indep(TAU_T, L)
        t1_dev = max(t1_dev, abs(a1v - a2v) / a2v)
    branch_thin = "thin" if TAU_T < TAU_THICK else "thick"
    branch_syn = "thick" if 150.0 >= TAU_THICK else "thin"
    branch_ok = (branch_thin == "thin") and (branch_syn == "thick")
    t_esc_1m = t_esc(1.0)
    t_esc_fm = t_esc(1.0e-15)
    print("")
    print("[R1-B3 entropy-ledger screening]")
    print("  tau_T = 0.146 < 1 -> optically THIN: photon/neutrino free streaming, not diffusion")
    print("  thick-limit branch (validation only, two length tiers): t_diff = 3 tau L / c")
    print("    L = 1 fm : t_diff = %.6e s (indep path dev %.2e)" % (t_diff_thick(TAU_T, 1.0e-15), abs(t_diff_thick(TAU_T, 1.0e-15) - t_diff_indep(TAU_T, 1.0e-15)) / t_diff_indep(TAU_T, 1.0e-15)))
    print("    L = 1 m  : t_diff = %.6e s (indep path dev %.2e)" % (t_diff_thick(TAU_T, 1.0), abs(t_diff_thick(TAU_T, 1.0) - t_diff_indep(TAU_T, 1.0)) / t_diff_indep(TAU_T, 1.0)))
    print("  thin branch (actual physics): t_esc = L / c")
    print("    L = 1 fm : t_esc = %.6e s ; L = 1 m : t_esc = %.6e s" % (t_esc_fm, t_esc_1m))
    print("  branch logic: tau_T = 0.146 -> '%s' branch selected; synthetic tau = 150 -> '%s' branch"
          % (branch_thin, branch_syn))
    print("  t_esc(1 m) / t_expand(4.7 ns) = %.4f" % (t_esc_1m / T_EXPAND_S))
    print("  conclusion: the entropy-drain channel (photon + neutrino free streaming) is NOT the")
    print("    bottleneck: t_esc(1 m) = 3.34 ns < t_expand = 4.7 ns (screening-level MODEL RESULT;")
    print("    transport details - opacity evolution, neutrino diffusion - deferred to full R1-B3)")

    # ================================================================ R1-B4
    species = (("n", M_N, M_N_MEV), ("p", M_P, M_P_MEV), ("e", M_E, M_E_MEV))
    t2_dev = 0.0
    dez = {}
    for name, m_si, m_nat in species:
        v_si = dez_si(m_si)
        v_nat = dez_nat(m_nat)
        dez[name] = (v_si, v_nat)
        t2_dev = max(t2_dev, abs(v_si - v_nat) / v_nat)
    E_probe_MeV = 0.5 * M_N * (V_PROBE_KMS * 1.0e3) ** 2 / MEV_J
    E2D_max = dez["n"][0] / EFF2D_MARGIN
    n2D_n_fm2 = (SIGMA_KGM2 / M_N) * 1.0e-30   # m^-2 -> fm^-2 (1 m^2 = 1e30 fm^2)
    kF2 = math.sqrt(2.0 * math.pi * n2D_n_fm2)
    EF_n_2D = (HBARC * kF2) ** 2 / (2.0 * M_N_MEV)
    print("")
    print("[R1-B4 low-energy spectrum + carrier check]")
    print("  DeltaE_z = pi^2 hbar^2 / (2 m L_z^2), L_z = 1 fm (registered NR box form):")
    for name, _, _ in species:
        v_si, v_nat = dez[name]
        print("    %s : SI numeric %.6e MeV | natural-unit %.6e MeV (rel dev %.2e)" % (name, v_si, v_nat, abs(v_si - v_nat) / v_nat))
    print("    e value = %.3e MeV = %.1f GeV" % (dez["e"][0], dez["e"][0] / 1000.0))
    print("  T2 spec-line correction (registered finding): the task-line quotes 'electron gap")
    print("    ~376 MeV' and 'nucleon gap ~0.2 MeV' are 1e3 unit slips against the registered")
    print("    formula at L_z = 1 fm; corrected values: nucleon %.1f MeV, electron %.2e MeV." % (dez["n"][0], dez["e"][0]))
    print("    Direction of all conclusions unchanged.")
    print("  carriers (N7 + R1-B1): electrons removed (mu_e = 23.2 MeV above all capture thresholds;")
    print("    X_p ~ 1e-05, scan 2.9e-07) -> low-dimensional carriers = n/p (heavy fermions)")
    print("  DeltaE_z(nucleon) = %.1f MeV >> T = 0 -> longitudinal ground band occupied" % dez["n"][0])
    print("    (DeltaE_z(n)/m_n c^2 = %.3f, see relativistic caveat below)" % (dez["n"][0] / M_N_MEV))
    print("  effective-2D domain (registered): E_probe <= DeltaE_z(n)/10 = %.2f MeV" % E2D_max)
    print("    data: E_probe(G0 v_probe) = %.3e MeV (ratio %.2e); E_F,n(strictly 2D, Sigma = 70 kg/m^2)" % (E_probe_MeV, E_probe_MeV / dez["n"][0]))
    print("    = %.2f MeV; mu_e(beta-eq, R1-B1) = %.2f MeV -> all registered low-E scales << %.2f MeV" % (EF_n_2D, MU_E_BETAEQ_MEV, E2D_max))
    print("    -> 'effective 2D' criterion holds across the registered low-energy domain")
    print("  electron gap %.2e MeV: electrons are removed anyway (N7) -> excluded from the" % dez["e"][0])
    print("    low-energy theory regardless of the gap size")
    print("  relativistic caveat (registered): DeltaE_z(n)/m_n c^2 = %.3f -> NR box formula borderline;"
          % (dez["n"][0] / M_N_MEV))
    for name, _, m_nat in species:
        print("    exact relativistic ground state %s : %.1f MeV" % (name, dez_rel(m_nat)))
    print("    (NR form kept as the registered T2 estimator; full treatment -> complete R1-B4 + R3)")

    # ================================================================ s8.4 classification
    print("")
    print("[s8.4 classification - computed screening determinations; B-window: B < B_ion = 2.4e-09")
    print("  (dense layer, R1-B valid domain); no sector triggers label D (all registered models")
    print("  inside their declared validity domains)")
    print("  R1-B2 ion phase: Gamma_i = 0.179 in the liquid region (both thresholds)")
    print("    -> label C for any 'Wigner crystal survives/forms' claim (crystalline order fails to")
    print("    form); computed phase = weakly coupled ion liquid (screening grade)")
    print("  R1-B2 fusion channel: t_react/t_expand = %.2e >> 1 -> channel CLOSED on the expansion" % ratio_t)
    print("    timescale (negative channel result: no restructuring via ion fusion at registered E_cm)")
    print("  R1-B3 entropy drain: t_esc(1 m) = 3.34 ns < t_expand = 4.7 ns, tau_T < 1 free streaming")
    print("    -> label A for the entropy-drain channel (functional, not the bottleneck) at screening")
    print("    grade")
    print("  R1-B4 effective-2D: carriers n/p; DeltaE_z(n) = %.1f MeV >> E_F,n(2D) = %.2f MeV, T = 0" % (dez["n"][0], EF_n_2D))
    print("    -> label A for the low-energy carrier sector within E <= %.2f MeV (longitudinal ground" % E2D_max)
    print("    band occupied); full spectrum and R3 consistency deferred to complete R1-B4")

    # ================================================================ findings
    print("")
    print("[findings]")
    print("  F-R1B2-1: at Gamma_i = 0.179 the ion subsystem sits 3 orders below both crystallization")
    print("    thresholds: liquid, no Wigner order, crystal zero-point (pycnonuclear) channel closed.")
    print("  F-R1B2-2: zero-T tunnelling at E_cm = hbar*omega_i/2 = %.4f MeV (%.1f%% of U_i):"
          % (E_cm_MeV_SI, 100.0 * E_cm_MeV_SI / U_I_REG_MEV))
    print("    eta = %.2f, P = %.2e, t_react = %.2e s = %.1e yr >> 4.7 ns -> fusion cannot restructure"
          % (eta, P_tun, t_react, t_react / 3.156e7))
    print("    the dense layer within the expansion window (screening estimate; tail rates -> full B2).")
    print("  F-R1B3-1: tau_T = 0.146 < 1: the registered Thomson depth is optically thin, so the")
    print("    thick-limit formula t_diff = 3 tau L/c does not describe the layer; it is printed only")
    print("    to validate the thick branch. Actual escape is free streaming, t_esc = L/c < t_expand.")
    print("  F-R1B4-1: spec-line unit slips corrected against the registered formula: DeltaE_z(n) =")
    print("    %.1f MeV (not 0.2 MeV), DeltaE_z(e) = %.2e MeV = 376 GeV (not 376 MeV); the" % (dez["n"][0], dez["e"][0]))
    print("    registered conclusions (ground-band occupation, electrons excluded) are unchanged.")
    print("  F-R1B4-2: the NR box gap for the nucleon is borderline relativistic (ratio 0.218); the")
    print("    exact relativistic ground state is 186.1 MeV (n) / 186.3 MeV (p) - both still >> every")
    print("    registered low-energy scale, so the effective-2D conclusion is robust.")

    # ================================================================ verdicts
    print("")
    print("[verdicts]")
    all_ok = True
    vs = [
        ("T1 thick-limit diffusion formula regression + branch logic (dev < 1e-06)",
         t1_dev <= TH_REL and branch_ok, "%.3e" % t1_dev),
        ("T2 DeltaE_z SI-numeric vs natural-unit analytic, 3 species (max dev < 1e-06)",
         t2_dev <= TH_REL, "%.3e" % t2_dev),
        ("T3 Gamma boolean: Gamma_i = 0.179 < 130 (2D crystal threshold) and < 175 (3D)",
         GAMMA_I < GAMMA_C_2D and GAMMA_I < GAMMA_C_3D, "0.179 < 130 < 175"),
        ("T4 zero-point energy E_cm: SI vs natural-unit path (dev < 1e-06)",
         t4_dev <= TH_REL, "%.3e" % t4_dev),
        ("C1 U_i computed vs registered 4.14 MeV (dev < 1e-02)",
         c1_ok, "%.3e" % (abs(U_i_comp - U_I_REG_MEV) / U_I_REG_MEV)),
        ("C2 Gamma_i = U_i/mu_e recomputed vs registered 0.179 (dev < 1e-02)",
         c2_ok, "%.3e" % (abs(gamma_comp - GAMMA_I) / GAMMA_I)),
        ("AUX eta cross-path SI vs natural (dev < 1e-04)",
         aux_dev <= TH_AUX, "%.3e" % aux_dev),
    ]
    for name, ok, val in vs:
        all_ok = all_ok and ok
        verdict_line(name, ok, val)
    print("")
    print("R1-B2/B3/B4 screening OVERALL: %s" % ("PASS" if all_ok else "FAIL"))
    print("evidence level: MODEL RESULT (screening grade; all inputs and thresholds registered above)")


if __name__ == "__main__":
    main()
