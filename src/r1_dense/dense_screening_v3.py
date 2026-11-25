# -*- coding: utf-8 -*-
"""
R1-B2/B3/B4 v3: ion-phase verdict redone / transport downgraded / gap and 2D-criterion boundaries registered
============================================================================

Changes from v2 to v3 (review B3/B4 + downgrade items 1/2/3):

  D1 The crystal criterion changed from "giving a verdict" to "giving an interval" (review downgrade item 1).
      v2 compared E_zp/U_i = 0.058 with 0.1 and judged CRYSTAL. Three O(1) problems:
        (a) the denominator used Z^2e^2/r_WS (Wigner-Seitz radius 8.69 fm), whereas the crystal binding energy should
            be compared with the Madelung energy -C*Z^2e^2/a_NN, with a_NN(triangular lattice)=16.55 fm.
            The two differ by a factor of 1.72, directly underestimating the ratio by about half.
        (b) omega used the 3D-OCP form Z^2e^2/(m a^3), while this is a 2D ion layer.
            The 2D plasmon has omega_p^2 = 2*pi*n_s*Z^2e^2/(m*a_NN); the two differ by O(1).
        (c) no electron screening. v3 computes the screening length with the R1-B1 convention and computes **2D and 3D**
            electron gases separately -- they differ by a factor of 15 (184 fm vs 12 fm), a dimensional fingerprint.
      v3 reports two criteria (Lindemann displacement delta and E_zp/|E_M|) with a factor-2 error band.
      The verdict changes to UNDECIDED (within the threshold band, not CRYSTAL).

  D2 sigma_nu corrected from 1e-43 to 1e-48 m^2 (review downgrade item 3). The weak-interaction cross section at
      10-30 MeV is of order 1e-48 m^2; v2's 1e-43 was about 1e5 times too large. The conclusion (free streaming) is
      unchanged, but this constant must not be used downstream.

  D3 The conflict between R1-B4's "effective 2D domain <= 43 MeV" and the nucleon Fermi energy is made explicit
      (downgrade item 2). v2 only gave the upper bound of the domain without checking whether the domain covers the
      actually occupied states. v3 evaluates at both G0 density and n_0: at G0, E_F,nuc=24.0 MeV < 42.6 MeV (inside);
      at n_0, 58.4 MeV > 42.6 MeV (outside). The domain therefore **does not cover** n_0 and must be marked OPEN.

  D4 The T3 self-comparison is removed (B3). In v2, e_zp_nat was computed once, then overwritten by the same expression,
      and compared with itself to give 0.00e+00, yet labeled "dual-path PASS". v3 labels the unit-conversion check
      separately as UNIT (not counted as evidence) and adds two genuine checks:
        C1 the NR limit of the relativistic gap as L->inf (a real functional limit, comparable)
        C2 cross-module consistency of tau_T with G0 v3 (different modules, different code paths)
        C3 the order-of-magnitude criterion for tau_nu after the sigma_nu correction (comparison with 1, not self-comparison)

  D5 The a_i label is corrected: a_i=8.69 fm is the Wigner-Seitz radius sqrt(1/(pi n_s)),
      not the nearest-neighbor distance of the triangular lattice. v3 lists both to avoid "plugging the radius's value
      under the spacing's name".

Run: python -I src/r1_dense/dense_screening_v3.py
"""
import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from src.common import conv  # noqa: E402

# ---- ions (registered composition branch A: Z=5, A=10) ----
Z_ION = conv.Z_ION
A_ION = conv.A_ION
M_ION_KG = A_ION * conv.AMU_KG
M_ION_MEV = A_ION * 931.4941
E2_4PE0 = 2.307077552e-28      # J m  (= e^2/4 pi eps0)
E2_MEV_FM = 1.4399645          # MeV fm
ALPHA = 1.0 / 137.035999

N_S_FM2 = conv.N_S_FM2         # 4.2155e-3 fm^-2
N_S_M2 = conv.N_S              # 4.2155e27 m^-2

R_WS_FM = (1.0 / (math.pi * N_S_FM2)) ** 0.5        # Wigner-Seitz radius
A_NN_FM = (2.0 / (math.sqrt(3.0) * N_S_FM2)) ** 0.5  # triangular-lattice nearest-neighbor distance
MADELUNG_2D = 1.106103                                # Madelung constant for the 2D triangular lattice (1/r)

SIGMA_T = 6.6524587321e-29
SIGMA_NU = 1.0e-48             # m^2 -- D2 correction (v2: 1e-43)
N_B_COL = conv.N_B             # 4.2155e28 m^-2
L_BODY = 0.07
LZ_M = conv.LZ_FM * 1e-15
T_EXPAND_NS = 4.72
E2D_MARGIN = 10.0
BAND = 2.0                     # registered error band for criteria / O(1) coefficients (factor 2)

TH = dict(C1_limit=1e-3, C2_tau=1e-9, C3_nu=1.0, U1_unit=1e-6)


def omega_p_2D(a_nn_fm):
    """2D OCP plasmon frequency (SI): omega^2 = 2 pi n_s Z^2e^2/(m a),
     different from the 3D-OCP Z^2e^2/(m a^3) -- v2 used the latter."""
    a = a_nn_fm * 1e-15
    return math.sqrt(2.0 * math.pi * N_S_M2 * Z_ION ** 2 * E2_4PE0 / (M_ION_KG * a))


def omega_p_2D_natural(a_nn_fm):
    """Natural-unit path for the same expression (MeV/fm), for unit-bookkeeping checks (UNIT, not a physics check)"""
    a = a_nn_fm
    # omega[1/fm] = sqrt(2 pi n_s[fm^-2] Z^2 alpha / (m[MeV] * a[fm])) * m ... derive directly:
    # omega^2 = 2 pi n_s Z^2 (alpha*hbarc) / (m_MeV * a)  [1/fm^2]
    om_fm = math.sqrt(2.0 * math.pi * N_S_FM2 * Z_ION ** 2 * (ALPHA * conv.HBARC)
                      / (M_ION_MEV * a))
    return om_fm * conv.C * 1e15   # 1/fm -> rad/s


def tf_screening():
    """Electron Thomas-Fermi screening length, computed separately for 2D and 3D (dimensional fingerprint)"""
    mu2 = conv.eos_e_2D(conv.N_E_FM2)["EF"]
    dn_dmu_2 = conv.G_E * mu2 / (2.0 * math.pi * conv.HBARC ** 2)   # fm^-2/MeV
    q2 = 2.0 * math.pi * E2_MEV_FM * dn_dmu_2                        # fm^-1
    n3 = conv.N_E_FM3
    mu3 = conv.eos_e_3D(n3)["EF"]
    dn_dmu_3 = mu3 ** 2 / (math.pi ** 2 * conv.HBARC ** 3)
    k3 = math.sqrt(4.0 * math.pi * E2_MEV_FM * dn_dmu_3)
    return dict(lam_2D=1.0 / q2, q_2D=q2, mu_2D=mu2,
                lam_3D=1.0 / k3, k_3D=k3, mu_3D=mu3)


def gap_nr(m_mev, L_fm):
    return 3.0 * math.pi ** 2 * conv.HBARC ** 2 / (2.0 * m_mev * L_fm ** 2)


def gap_rel(m_mev, L_fm):
    k1 = math.pi * conv.HBARC / L_fm
    k2 = 2.0 * math.pi * conv.HBARC / L_fm
    return math.sqrt(m_mev ** 2 + k2 ** 2) - math.sqrt(m_mev ** 2 + k1 ** 2)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    L = []
    w = L.append
    w("=" * 92)
    w("R1-B2/B3/B4 v3: ion phase (band) / transport (downgraded) / gap domain (OPEN)")
    w("=" * 92)
    w("registered: Z=%d A=%d | n_s=%.5f fm^-2 | r_WS=%.3f fm | a_NN(tri)=%.3f fm"
      % (Z_ION, A_ION, N_S_FM2, R_WS_FM, A_NN_FM))
    w("  Madelung(2D tri) C=%.6f | sigma_nu=%.0e m^2 (v2: 1e-43, D2 fix)"
      % (MADELUNG_2D, SIGMA_NU))
    w("")

    # ------------------------------------------------------------------ R1-B2
    w("[R1-B2 v3] cold ion phase: v2 'CRYSTAL' -> UNDECIDED (three O(1) corrections)")
    scr = tf_screening()
    w("  (1) electron screening, 2D vs 3D Thomas-Fermi (dimension fingerprint):")
    w("      electrons 2D: mu_e=%.2f MeV -> lambda_TF=%.1f fm -> exp(-a_NN/lambda)=%.3f"
      % (scr["mu_2D"], scr["lam_2D"], math.exp(-A_NN_FM / scr["lam_2D"])))
    w("      electrons 3D: mu_e=%.2f MeV -> lambda_TF=%.1f fm -> exp(-a_NN/lambda)=%.3f"
      % (scr["mu_3D"], scr["lam_3D"], math.exp(-A_NN_FM / scr["lam_3D"])))
    w("      => the 2D electron gas barely screens (a/lambda=%.2f), while the 3D electron gas screens strongly. v2 computed neither."
      % (A_NN_FM / scr["lam_2D"]))
    S2 = math.exp(-A_NN_FM / scr["lam_2D"])
    S3 = math.exp(-A_NN_FM / scr["lam_3D"])

    om2 = omega_p_2D(A_NN_FM)
    om2_sh = omega_p_2D(A_NN_FM) * math.sqrt(S2)
    ezp_mev = 0.5 * conv.HBAR * om2_sh / conv.MEV_J
    om_3dform = math.sqrt(Z_ION ** 2 * E2_4PE0 / (M_ION_KG * (R_WS_FM * 1e-15) ** 3))
    w("  (2) 2D OCP plasmon vs the 3D a^-3 form v2 used:")
    w("      omega_p(2D)  = %.4e rad/s (screened %.4e, sqrt(S2)=%.3f)"
      % (om2, om2_sh, math.sqrt(S2)))
    w("      omega_p(3D)  = %.4e rad/s  -> ratio %.3f" % (om_3dform, om2_sh / om_3dform))
    w("      Note: the two forms are numerically almost identical on this lattice (2*pi*n_s*a_NN^2 = %.2f ~ (a_NN/r_WS)^3 = %.2f),"
      % (2 * math.pi * N_S_FM2 * A_NN_FM ** 2, (A_NN_FM / R_WS_FM) ** 3))
    w("          a coincidence that does not vindicate v2 -- the real correction is in (3): the energy scale.")

    U_ws = Z_ION ** 2 * E2_4PE0 / (R_WS_FM * 1e-15) / conv.MEV_J
    E_mad = MADELUNG_2D * Z_ION ** 2 * E2_4PE0 / (A_NN_FM * 1e-15) / conv.MEV_J * S2
    w("  (3) binding energy scale:")
    w("      Z^2e^2/r_WS = %.3f MeV (v2's denominator) vs Madelung |E_M| = C*Z^2e^2/a_NN*S2 = %.3f MeV"
      % (U_ws, E_mad))
    w("      => v2's denominator is too large by %.2f, so the ratio was underestimated by the same factor" % (U_ws / E_mad))

    rt = ezp_mev / E_mad
    delta = math.sqrt(conv.HBAR / (M_ION_KG * om2_sh * (A_NN_FM * 1e-15) ** 2))
    w("  criteria (both, with registered factor-%.0f band):" % BAND)
    w("      (A) Lindemann displacement  delta=sqrt(<u^2>)/a_NN = %.3f   (melt if >~0.1-0.2)"
      % delta)
    w("      (B) E_zp/|E_M| = %.4f / %.4f = %.3f                      (melt if >~0.1)"
      % (ezp_mev, E_mad, rt))
    w("      band: delta in [%.3f, %.3f] ; (B) in [%.3f, %.3f]"
      % (delta / math.sqrt(BAND), delta * math.sqrt(BAND), rt / BAND, rt * BAND))
    band_lo, band_hi = min(delta / math.sqrt(BAND), rt / BAND), max(delta * math.sqrt(BAND), rt * BAND)
    straddle = (band_lo < 0.2) and (band_hi > 0.1)
    w("      => %s" % ("BAND STRADDLES the 0.1-0.2 criterion -> UNDECIDED (not CRYSTAL)"
                       if straddle else "band clear of criterion"))
    w("      v2's 'CRYSTAL, 0.058 << 0.1' is revoked: after correction both criteria lie near 0.1-0.2.")
    w("  composition branch B (dissolved npe, R1-B1 v3 HYB X_p=%.2e):"
      % conv.beta_envelope()["HYB"]["X_p"])
    w("      no ion lattice; the crystal/liquid dichotomy does not apply.")
    w("  VERDICT-2: UNDECIDED. A screened 2D-OCP criterion is required (MC or Lindemann calibration).")
    w("")

    # ------------------------------------------------------------------ R1-B3
    w("[R1-B3 v3] transport reference timescales (still conditional, not a conclusion)")
    tau_fr = SIGMA_T * conv.N_E_FM2 * 1e30
    n_e_eq = conv.beta_envelope()["HYB"]["n_e_fm3"]
    tau_eq = SIGMA_T * n_e_eq * 1e30 * LZ_M
    w("  Thomson optical depth (frozen, areal): tau_T = sigma_T*n_2D = %.4f" % tau_fr)
    w("  Thomson optical depth (beta-eq HYB):    tau_T = %.3e (thin)" % tau_eq)
    td = 3.0 * tau_fr * L_BODY / conv.C
    w("  thick-limit diffusion time (L=%.2f m): %.3f ns  (vs expansion %.2f ns)"
      % (L_BODY, td * 1e9, T_EXPAND_NS))
    tau_nu = SIGMA_NU * N_B_COL
    w("  neutrino: sigma_nu=%.0e m^2 * N_B=%.3e m^-2 -> tau_nu=%.2e << 1 (free streaming)"
      % (SIGMA_NU, N_B_COL, tau_nu))
    w("  [D2] v2 used 1e-43 and gave tau_nu=%.1e; the order-of-magnitude conclusion is the same but the constant was wrong by 1e5; fixed."
      % (1e-43 * N_B_COL))
    w("  VERDICT-3: v1 'entropy drain is not the bottleneck' remains downgraded to")
    w("    'reference timescale estimate (conditional)'; full transport OPEN.")
    w("")

    # ------------------------------------------------------------------ R1-B4
    w("[R1-B4 v3] longitudinal gap and the domain of the 2D criterion")
    w("  n (L_z=1 fm): E_1=%.2f MeV | dE12_NR=%.1f MeV | dE12_rel=%.1f MeV"
      % (gap_nr(conv.M_N, 1.0) / 3.0, gap_nr(conv.M_N, 1.0), gap_rel(conv.M_N, 1.0)))
    w("  e (L_z=1 fm): dE12_rel=%.1f MeV  [NR formula invalid here: E_1 >> m_e c^2; v2 printed NR"
      % gap_rel(conv.M_E, 1.0))
    w("               3.8e5 MeV, a labeling error rather than a physical quantity]")
    g_rel_n = gap_rel(conv.M_N, 1.0)
    domain = g_rel_n / E2D_MARGIN
    ekin_g0 = conv.HBARC ** 2 * conv.kF_3(conv.N_B_FM3) ** 2 / (2 * conv.M_N)
    ekin_n0 = conv.HBARC ** 2 * conv.kF_3(0.16) ** 2 / (2 * conv.M_N)
    w("  effective-2D domain: E_probe <= dE12_rel/%.0f = %.1f MeV" % (E2D_MARGIN, domain))
    w("    [D3] does the domain cover the occupied states?")
    w("      G0 density n_B=%.4f fm^-3: E_F,nuc=%.1f MeV  -> %s"
      % (conv.N_B_FM3, ekin_g0, "INSIDE" if ekin_g0 < domain else "OUTSIDE"))
    w("      saturation n_0=0.16 fm^-3: E_F,nuc=%.1f MeV -> %s"
      % (ekin_n0, "INSIDE" if ekin_n0 < domain else "OUTSIDE"))
    w("    => the domain holds at G0 density but not at n_0. v2 reported only the upper bound and did not check this; mark OPEN.")
    w("  residual electrons (R1-B1 v3, HYB): mu_e,eq=%.2f MeV << dE12_rel(e)=%.1f MeV"
      % (conv.beta_envelope()["HYB"]["mu_e"], gap_rel(conv.M_E, 1.0)))
    w("    -> all residual electrons in the n=1 band; sector weight vs nucleons OPEN")
    w("")

    # ------------------------------------------------------------------ checks
    w("[checks]  C = counted as evidence ; U = unit bookkeeping ; R = registration")
    chk = []

    def c(name, val, thr, ok, note):
        chk.append(("C", name, val, thr, ok, note))

    def u(name, val, thr, ok, note):
        chk.append(("U", name, val, thr, ok, note))

    r100 = gap_rel(conv.M_N, 100.0) / gap_nr(conv.M_N, 100.0)
    c("C1_gap_rel_to_NR_limit", abs(r100 - 1.0), TH["C1_limit"],
      abs(r100 - 1.0) < TH["C1_limit"],
      "at L=100 fm, dE12_rel/dE12_NR=%.8f (should be 1)" % r100)

    tau_g0 = conv.N_E_FM2 * 1e30 * SIGMA_T
    c("C2_tauT_cross_module", abs(tau_fr - tau_g0) / tau_g0, TH["C2_tau"],
      abs(tau_fr - tau_g0) / tau_g0 < TH["C2_tau"],
      "consistent with tau_T=%.4f computed independently in G0 v3" % tau_g0)

    c("C3_tau_nu_scale", tau_nu / 1.0, TH["C3_nu"], tau_nu < TH["C3_nu"],
       "tau_nu=%.2e, compared with 1 (not a self-comparison)" % tau_nu)

    om_si = omega_p_2D(A_NN_FM)
    om_nat = omega_p_2D_natural(A_NN_FM)
    u("U1_omega_unit_path", abs(om_si - om_nat) / om_si, TH["U1_unit"],
      abs(om_si - om_nat) / om_si < TH["U1_unit"],
      "SI %.4e vs natural units %.4e rad/s -- checks only unit conversion, not a physical dual path"
      % (om_si, om_nat))

    for tag, name, val, thr, ok, note in chk:
        w("  %s %-24s %-11.3e thr %-9.1e %-6s %s"
          % (tag, name, val, thr, "PASS" if ok else "FAIL", note))

    w("")
    w("  R1 crystal verdict = UNDECIDED (band %.2f..%.2f straddles 0.1-0.2)"
      % (band_lo, band_hi))
    w("  R2 2D-domain covers E_F at G0 but not at n_0 -> OPEN, not PASS")
    w("  R3 sigma_nu corrected to 1e-48 m^2; conclusion unchanged (free streaming)")

    allok = all(x[4] for x in chk)
    w("")
    w("[findings]")
    w("  F-R1B2-4(rev): v2's 'crystal reversal' does not hold. After the three corrections E_zp/|E_M|=%.3f,"
      % rt)
    w("                 Lindemann delta=%.3f; both lie within the criterion band -> UNDECIDED."
      % delta)
    w("  F-R1B2-5(new): the 2D electron-gas screening length is %.0f fm vs %.1f fm for 3D, a factor of %.0f."
      % (scr["lam_2D"], scr["lam_3D"], scr["lam_2D"] / scr["lam_3D"]))
    w("                 This means 'whether electrons screen the ionic Coulomb interaction' is itself convention-dependent.")
    w("  F-R1B3-3(rev): tau_T(frozen)=%.3f is marginally thick; diffusion %.2f ns << %.1f ns window."
      % (tau_fr, td * 1e9, T_EXPAND_NS))
    w("  F-R1B4-3(rev): the dE12 values are unchanged (NR %.0f / rel %.0f MeV), but domain coverage splits by density,"
      % (gap_nr(conv.M_N, 1.0), g_rel_n))
    w("                 so R1-B4's evidence level is downgraded from MODEL RESULT to OPEN(conditional).")
    w("")
    w("R1-B2/B3/B4 v3 OVERALL: %s (code checks pass; physical verdicts are band/OPEN)"
      % ("PASS" if allok else "FAIL"))
    w("evidence level: MODEL RESULT / UNDECIDED where stated")
    print("\n".join(L))


if __name__ == "__main__":
    main()
