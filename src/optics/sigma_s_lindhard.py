import sys
sys.stdout.reconfigure(encoding="utf-8")
# =====================================================================
# R5-L2: surface conductivity sigma_s(omega) module - NO visibility claim.
# Spec: DCC roadmap v1.4, sections 3.7, 6.4, 6.7, 8.13 (L2 row).
#   sigma_s(omega) is an INPUT, not a universal constant (6.4, S10).
#   Registered model here: standard 2D Lindhard long-wavelength intraband
#   limit with relaxation time tau, i.e. the Drude-type form
#       sigma_s(w) = (e^2 n_2D tau / m*) / (1 - i w tau)
#   plus an INTERBAND term switched by the Pauli-blocking bandwidth:
#   the interband term is active only when hbar*w > 2*E_F
#   (E_probe vs 2*E_F judgment). The interband AMPLITUDE is an explicit
#   OPEN model input (benchmark value e^2/(16*hbar), the standard 2D
#   long-wavelength interband scale); its line shape is NOT known from
#   the material state and is not asserted here.
#   FORBIDDEN by 6.4/6.7/8.13 and NOT done in this module:
#     - no default pi*alpha (2.3%) input;
#     - no extrapolation from any bulk omega_p;
#     - no visibility / mirror / transparent conclusion of any kind.
#   Grade cap (8.13): before G4 and G5' pass, everything here is
#   "designated-background test optics". The tag is printed on EVERY row.
#   tau is an explicit OPEN input (collision rate unknown), scanned over
#   {1e-19, 1e-18, 1e-16} s.
# Zero-file-I/O: results printed to stdout, ASCII only.
# Run: cd D:/Docs/DCC && python -I src/optics/sigma_s_lindhard.py > runs/R5/r5l2_sigma_s_results.txt
# =====================================================================
import math
import numpy as np

# ---------------- physical constants (SI; exact where marked) ----------------
E_CHARGE = 1.602176634e-19      # C (exact)
HBAR = 1.054571817e-34          # J s (= h exact / 2pi)
C_LIGHT = 2.99792458e8          # m/s (exact)
M_E = 9.1093837015e-31          # kg
EPS0 = 8.8541878128e-12         # F/m
MU0 = 1.25663706212e-6          # N/A^2 (CODATA)
Z0 = math.sqrt(MU0 / EPS0)      # vacuum impedance, ~376.7303 Ohm

# ---------------- logged inputs (G0 registered values; v1.4 3.2/3.7) ----------------
# BASELINE CORRECTED 2026-11-22 -> G0P-003 (v3), roadmap 3.4. The 2026-11-21 run used the
# pre-v3 values (n_2D = 2.20e27, E_F = 23.20 MeV), which are REVOKED (see 11.1 header).
# Registration: runs/R5/r5l2_rerun_registration.md. Thresholds are unchanged.
N_2D = 2.20e28                  # m^-2  (G0 v3: electron surface density; was 2.20e27, x10 low)
E_F_REF_MEV = 73.37             # MeV   (G0 v3: E_F = hbar k_F c, relativistic dispersion, S37)
M_EC2_MEV = 0.51099895          # MeV   electron rest energy
# m*/m_e = E_F/(m_e c^2) per S37. DERIVED, not a literal: the old literal 45.4 was the pre-v3 value
# of this same expression and had silently desynchronised from E_F_REF_MEV (items 2 in the registration).
MSTAR_FACTOR = E_F_REF_MEV / M_EC2_MEV    # = 143.6 at the v3 baseline
Q_OPT = 1.26e7                  # 1/m   (optical wave-vector scale, logged)
TAU_SCAN = (1e-19, 1e-18, 1e-16)    # s; OPEN input (collision rate unknown) - explicit scan
# last row raised 50 MeV -> 200 MeV on 2026-11-22: the row exists ONLY to demonstrate the interband
# switch (hbar*w > 2 E_F). With 2 E_F moving 46.4 -> 146.7 MeV the old 50 MeV row falls below
# threshold and would no longer demonstrate the switch. Switch demo only, not a probe-regime claim.
HBARW_ROWS_EV = (1.0, 2.0, 3.0, 2.0e8)  # eV (1,2,3 eV visible; 200 MeV above 2E_F)
SIGMA_INTER_0 = E_CHARGE**2 / (16.0 * HBAR)   # OPEN interband amplitude (benchmark e^2/(16 hbar)) [S]
TOL_T1_CONSERV = 1e-12          # |R + T + A - 1| and |A_def - A_indep|
TOL_T2_ALIMIT = 1e-6            # A at tau = 1e-13 s (dissipation-free limit probe)
TAU_T2 = (1e-15, 1e-14, 1e-13)  # s; tau -> infinity probe sequence (beyond scan)
TOL_EF_CONSIST = 2e-3           # G0 consistency check k_F, E_F vs logged values

TAG = ("designated-background test optics; sigma_s inputs: n_2D, E_F, tau(scan); "
       "NO visibility conclusion")


def sec(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def sci(x, d=6):
    return "%.*e" % (d, x)


# =====================================================================
sec("R5-L2:  sigma_s(omega) MODULE  (v1.4 6.4 / 6.7 / 8.13 L2)")
print(TAG)
print("")
print("logged inputs (G0 v3): n_2D = %.3e m^-2 ; E_F(ref) = %.2f MeV ; m*/m_e = %.1f (S37, derived) ;"
      % (N_2D, E_F_REF_MEV, MSTAR_FACTOR))
print("baseline: G0P-003 v3 (rerun 2026-11-22). The pre-v3 run is archived as")
print("  runs/R5/r5l2_sigma_s_results_v1_REVOKED_BASELINE.txt ; registration runs/R5/r5l2_rerun_registration.md")
print("q_opt = %.3e 1/m ; tau = OPEN input, scan {%s} s ; interband amplitude = OPEN input"
      % (Q_OPT, ", ".join("%.0e" % t for t in TAU_SCAN)))
print("(benchmark e^2/(16 hbar) = %s S; line shape unknown, switch-only model)." % sci(SIGMA_INTER_0, 4))
print("")
print("prohibitions in force (6.4 / 6.7 / 8.13), restated in code comments and output:")
print("  - NO default pi*alpha (=2.3 percent) input anywhere;")
print("  - NO extrapolation from any bulk omega_p (plasmon q_opt*c is above the light cone;")
print("    optics stated ONLY through the surface conductivity sigma_s(omega));")
print("  - NO visibility / mirror / transparency conclusion of any kind.")
print("gate status: G4 = not passed (open); G5' = not passed (open) -> all products below")
print("are labeled 'designated-background test optics' on every row.")

# ---- G0 consistency of the derived Fermi quantities ----
k_F = math.sqrt(2.0 * math.pi * N_2D)
E_F = HBAR * k_F * C_LIGHT
E_F_MeV = E_F / 1.602176634e-13
m_star = MSTAR_FACTOR * M_E
ef_dev = abs(E_F_MeV - E_F_REF_MEV) / E_F_REF_MEV
c0_pass = ef_dev < TOL_EF_CONSIST
print("")
print("consistency (G0 v3): k_F = sqrt(2 pi n_2D) = %.4e 1/m (logged 3.718e14); " % k_F)
print("E_F = hbar k_F c = %.4f MeV vs logged %.2f MeV: rel dev = %.3e (tol %.1e) -> %s"
      % (E_F_MeV, E_F_REF_MEV, ef_dev, TOL_EF_CONSIST, "OK" if c0_pass else "FAIL"))
q_over_kf = Q_OPT / k_F
print("long-wavelength check: q_opt/k_F = %.3e << 1 -> local sigma_s (q -> 0 Lindhard limit) valid." % q_over_kf)
print("q_opt*c = %.3e rad/s (G0 3.7: plasmon above light cone, non-radiative mode)." % (Q_OPT * C_LIGHT))
print("model form: sigma_s(w) = (e^2 n_2D tau / m*)/(1 - i w tau)  [2D Lindhard long-wavelength")
print("intraband limit with relaxation time tau] + sigma_inter(theta(hbar w - 2 E_F)), switch on the")
print("Pauli-blocking bandwidth: interband OFF when hbar w <= 2 E_F = %.2f MeV." % (2.0 * E_F_MeV))

# ---- conductivities ----
def sigma_s(hbarw_ev, tau):
    """returns (sigma_complex [S], interband_on: bool, Re sigma, Im sigma)."""
    omega = hbarw_ev * E_CHARGE / HBAR
    sig0 = E_CHARGE**2 * N_2D * tau / m_star
    sD = sig0 / (1.0 - 1j * omega * tau)
    on = hbarw_ev > 2.0 * (E_F_MeV * 1e6)   # hbar w [eV] vs 2 E_F [MeV -> eV]
    s = sD + (SIGMA_INTER_0 if on else 0.0)
    return s, on, s.real, s.imag


def rta(sigma):
    """normal-incidence free-standing sheet: r = -Z0 s/(2+Z0 s), t = 2/(2+Z0 s)."""
    x = Z0 * sigma
    r = -x / (2.0 + x)
    t = 2.0 / (2.0 + x)
    R = abs(r) ** 2
    T = abs(t) ** 2
    A_def = 1.0 - R - T
    A_indep = float(np.real(x)) * T   # = Z0 Re(sigma) |t|^2 (absorbed fraction, independent form)
    return R, T, A_def, A_indep


# =====================================================================
sec("R, T, A TABLE  (normal incidence, free-standing, air/vacuum interface)")
print(TAG)
print("")
print("rows: hbar*omega ; columns: tau. cells: Re sigma, Im sigma [S]; R, T, A; (R+T+A-1).")
print("interband switch status printed per row (E_probe vs 2 E_F judgment).")
print("")
for hbarw in HBARW_ROWS_EV:
    if hbarw >= 1e6:
        label = "%.1f MeV" % (hbarw / 1e6)
    else:
        label = "%.1f eV" % hbarw
    on = hbarw > 2.0 * (E_F_MeV * 1e6)
    state = ("interband ON  (hbar*w > 2E_F)" if on else
             "interband OFF (hbar*w < 2E_F; Pauli blocking ON)")
    print("hbar*omega = %s   [%s]" % (label, state))
    print("  " + TAG)
    print("  %-9s %-15s %-15s %-13s %-13s %-13s %-11s" %
          ("tau [s]", "Re sigma [S]", "Im sigma [S]", "R", "T", "A", "R+T+A-1"))
    for tau in TAU_SCAN:
        s, _, sre, sim = sigma_s(hbarw, tau)
        R, T, A, Ai = rta(s)
        cons = (R + T + A) - 1.0
        print("  %-9.0e %-15s %-15s %-13.6f %-13.6f %-13.6f %-11.2e" %
              (tau, sci(sre, 4), sci(sim, 4), R, T, A, cons))
        print("  " + TAG)
    print("")
print(TAG)
print("note: the %.0f MeV row exists to demonstrate the interband SWITCH only; it is not a"
      % (HBARW_ROWS_EV[-1] / 1e6))
print("reachable probe regime claim. All rows are designated-background test optics.")

# =====================================================================
sec("TESTS")
# T1: R+T+A=1 and independent absorption identity, over the whole table
max_cons = 0.0
max_aid = 0.0
for hbarw in HBARW_ROWS_EV:
    for tau in TAU_SCAN:
        s, _, _, _ = sigma_s(hbarw, tau)
        R, T, A, Ai = rta(s)
        max_cons = max(max_cons, abs((R + T + A) - 1.0))
        max_aid = max(max_aid, abs(A - Ai))
t1_pass = (max_cons < TOL_T1_CONSERV) and (max_aid < TOL_T1_CONSERV)
print("[T1] R + T + A = 1 (max dev %.3e) and A_def vs A_indep = Z0 Re(sigma)|t|^2 (max dev %.3e);" % (max_cons, max_aid))
print("     threshold %.1e -> %s" % (TOL_T1_CONSERV, "PASS" if t1_pass else "FAIL"))

# T2: dissipation-free limit tau -> infinity: A -> 0 (A ~ Re sigma ~ 1/tau for w*tau >> 1)
hbarw_t2 = 2.0
seq = []
for tau in TAU_T2:
    s, _, sre, _ = sigma_s(hbarw_t2, tau)
    R, T, A, Ai = rta(s)
    seq.append((tau, A, sre))
mono2 = all(seq[i][1] > seq[i + 1][1] for i in range(len(seq) - 1))
a_last = seq[-1][1]
t2_pass = mono2 and (a_last < TOL_T2_ALIMIT)
print("[T2] dissipation-free limit at hbar*w = 1 eV..3 eV scale (w*tau >> 1: A ~ 1/tau):")
for tau, A, sre in seq:
    print("     tau = %.0e s : Re sigma = %s S , A = %s" % (tau, sci(sre, 4), sci(A, 4)))
print("     monotone decreasing: %s ; A(tau = 1e-13 s) = %s < %.1e -> %s"
      % (mono2, sci(a_last, 4), TOL_T2_ALIMIT, "PASS" if t2_pass else "FAIL"))

# T3: sigma_s increases with tau over the scan at hbar*w = 2 eV (w*tau < 1 across the scan)
hbarw_t3 = 2.0
omega_t3 = hbarw_t3 * E_CHARGE / HBAR
res = []
for tau in TAU_SCAN:
    s, _, sre, _ = sigma_s(hbarw_t3, tau)
    res.append((tau, sre, abs(s)))
mono3 = all(res[i][1] < res[i + 1][1] for i in range(len(res) - 1))
wtmax = omega_t3 * TAU_SCAN[-1]
t3_pass = mono3
print("[T3] Re sigma_s monotone increasing over tau scan at hbar*w = %.1f eV:" % hbarw_t3)
for tau, sre, smod in res:
    print("     tau = %.0e s : Re sigma = %s S , |sigma| = %s S (w*tau = %.3e)" % (tau, sci(sre, 4), sci(smod, 4), omega_t3 * tau))
print("     registered validity note: monotonicity holds for w*tau < 1 across the scan;")
print("     max w*tau = %.3f < 1 -> %s" % (wtmax, "PASS" if t3_pass else "FAIL"))

# =====================================================================
sec("VERDICTS")
print("C0  G0 consistency k_F, E_F (rel, tol %.1e): %s (%.3e)" % (TOL_EF_CONSIST, "PASS" if c0_pass else "FAIL", ef_dev))
print("T1  R+T+A=1 and absorption identity (tol %.1e): %s" % (TOL_T1_CONSERV, "PASS" if t1_pass else "FAIL"))
print("T2  tau -> infinity limit A -> 0 (monotone + %.1e): %s" % (TOL_T2_ALIMIT, "PASS" if t2_pass else "FAIL"))
print("T3  sigma_s monotone in tau over scan (w*tau < 1): %s" % ("PASS" if t3_pass else "FAIL"))
overall = "PASS" if (c0_pass and t1_pass and t2_pass and t3_pass) else "FAIL"
print("OVERALL: %s" % overall)
print("EVIDENCE LEVEL: designated-background test optics (v1.4 8.13 grade cap until G4 and G5' pass);")
print("MODEL RESULT; NO visibility conclusion; no default pi*alpha; no bulk omega_p extrapolation;")
print("sigma_s inputs: n_2D, E_F, tau(OPEN, scanned); interband amplitude OPEN.")
print(TAG)
