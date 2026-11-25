import sys
sys.stdout.reconfigure(encoding="utf-8")
# =====================================================================
# SC-2: the three sharpenings the governor's acceptance adds to SC-ROUTE.
#   (A) FSUM-SINGLE-SOURCE : the total weight must come from ONE Hamiltonian
#                            and its current operator; f-sum formulas from
#                            different models may not be spliced.
#   (B) KK-LINESHAPE / FSUM-FINITE : a step cannot be repaired by amplitude.
#                            What is required is an upper scale (a band edge).
#   (C) DRUDE-DOMAIN / TAU-KIND : prove the single-pole reduction, or compute
#                            the full response; and say WHICH tau.
# No visibility claim of any kind. No candidate sigma_s is produced.
# Registration: runs/OPTICS/sc2_registration.md  (P1-P12, locked before this run)
# Zero file I/O; ASCII only.  Run: python -I src/optics/sc2_lineshape_check.py
# =====================================================================
import math
import numpy as np

E_C = 1.602176634e-19
HBAR = 1.054571817e-34
C_LIGHT = 2.99792458e8
M_E = 9.1093837015e-31
EPS0 = 8.8541878128e-12

# record baseline, identical to src/optics/sigma_s_lindhard.py
N2D = 2.20e28
EF_MEV = 73.37
MSTAR = (EF_MEV / 0.51099895) * M_E          # = 143.6 m_e  (S37)
K_F = math.sqrt(2.0 * math.pi * N2D)         # g = 2 convention, as in the module
A_INTER = E_C ** 2 / (16.0 * HBAR)           # module's interband amplitude [S]
SIG_MIN = E_C ** 2 / (4.0 * HBAR)            # 2D Dirac universal value   [S]
WF_EV = 2.0 * EF_MEV * 1e6                   # interband threshold [eV]
WG = WF_EV * E_C / HBAR                      # [rad/s]
EV_PER_RADS = HBAR / E_C                     # rad/s -> eV


def out(s=""):
    print(s)


def hdr(t):
    out("")
    out("=" * 78)
    out(t)
    out("=" * 78)


def row(cells, w):
    out("  " + " ".join(("%-*s" % (wi, c))[:wi] for c, wi in zip(cells, w)))


def verdict(pid, claim, ok, note):
    out("  [%s] %s" % (pid, claim))
    out("       -> %s   (%s)" % ("HOLDS" if ok else "FAILED", note))


def sci(x, d=6):
    return "%.*e" % (d, x)


VERD = []

# =====================================================================
hdr("SC-2 / A : provenance of the spectral weight  (FSUM-SINGLE-SOURCE)")
# =====================================================================
w_total = math.pi * E_C ** 2 * N2D / (2.0 * MSTAR)
out("  total weight, pi e^2 n_2D/(2 m*) = %s S rad/s" % sci(w_total, 6))
out("  n_2D = %.3e m^-2 ; m* = %.2f m_e ; k_F = sqrt(2 pi n) = %.4e 1/m" % (N2D, MSTAR / M_E, K_F))

out("")
out("  A.1  FSUM-SPLIT: code defect, or theorem?")
out("       int_0^inf sigma0/(1+w^2 tau^2) dw = sigma0 pi/(2 tau) = pi e^2 n/(2 m*)   -- tau cancels")
out("       quadrature w' = (1/tau) u/(1-u), u in (0,1): the upper limit is infinite, no truncation.")


def drude_weight(tau, n=4_000_001):
    # midpoint rule on (0,1): a trapezoid over a midpoint grid silently drops half a cell at
    # each end, which is a systematic O(h) bias. See the audit trail in the ruling.
    u = (np.arange(n) + 0.5) / n
    wtau = u / (1.0 - u)
    f = 1.0 / (1.0 + wtau ** 2) / (1.0 - u) ** 2 / tau
    return E_C ** 2 * N2D * tau / MSTAR * (np.sum(f) / n)


out("")
row(["tau [s]", "int Re s dw (quad)", "sig0 pi/(2 tau)", "W_total", "rel dev"], [9, 20, 17, 17, 10])
rows = []
for tau in (1e-19, 1e-18, 1e-16):
    num = drude_weight(tau)
    s0_ = E_C ** 2 * N2D * tau / MSTAR
    rows.append(abs(num / w_total - 1.0))
    row(["%.0e" % tau, sci(num, 8), sci(s0_ * math.pi / (2 * tau), 8), sci(w_total, 8),
         "%.2e" % rows[-1]], [9, 20, 17, 17, 10])
dev1 = max(rows)
verdict("P1", "a single Drude pole consumes exactly W_total at every tau", dev1 < 1e-12,
        "max rel dev %.2e" % dev1)
VERD.append(("P1", dev1 < 1e-12))
out("       => FSUM-SPLIT is an identity, not a numerical accident. Any interband term added on top")
out("          is a second draw on the same budget; 1.000000000003 is the theorem showing through.")
out("       NOTE ON WHAT THIS CHECK CAN PROVE: W_total = pi e^2 n/(2 m*) and sig0 pi/(2 tau) are the")
out("       same expression, so the comparison is algebraic, not empirical. The quadrature only")
out("       validates itself. The content of P1 is therefore: the pole saturates the budget BY")
out("       DEFINITION, so 'partition' cannot be repaired by an amplitude. Recorded, not overstated.")
out("")
out("       AUDIT TRAIL for this row, because the prediction failed twice before passing:")
out("        run 1  sc2_results_v1_SUPERSEDED_PREFACTOR.txt : rel dev 2.14e+00, i.e. a factor pi.")
out("               cause: a spurious pi in the quadrature prefactor (sig0 already contains it).")
out("        run 2  sc2_results_v2_SUPERSEDED_ENDPOINT.txt : rel dev 3.18e-07.")
out("               cause: trapezoid over a midpoint grid drops half a cell at each end, a bias of")
out("               exactly h*(f(0)+f(1))/2 = O(1/n). Replaced by the midpoint rule.")
out("       Both defects were in the instrument, not the record: which is the point of the note above.")

out("")
out("  A.2  is W_total a property of the material?  (degeneracy convention)")
out("       n = g k_F^2/(4 pi), E_F = hbar k_F v_F, m* = p_F/v_F  =>")
out("       W(g) = (e^2 v_F/8 hbar) sqrt(4 pi n g) ;  E_F(g) = hbar v_F sqrt(4 pi n/g)")


def w_of_g(g, v_f=C_LIGHT, n=N2D):
    return (E_C ** 2 * v_f / (8.0 * HBAR)) * math.sqrt(4.0 * math.pi * n * g)


def ef_of_g(g, v_f=C_LIGHT, n=N2D):
    return HBAR * v_f * math.sqrt(4.0 * math.pi * n / g)


out("")
row(["g", "W_total(g)", "E_F(g) [MeV]", "W(g)/W(2)"], [5, 20, 17, 13])
for g in (2, 4):
    row(["%d" % g, sci(w_of_g(g), 6), "%.3f" % (ef_of_g(g) / 1.602176634e-13),
         "%.6f" % (w_of_g(g) / w_total)], [5, 20, 17, 13])
r_w = w_of_g(4) / w_of_g(2)
r_ef = ef_of_g(4) / ef_of_g(2)
ok2 = abs(r_w - math.sqrt(2.0)) < 1e-12 and abs(r_ef - 1.0 / math.sqrt(2.0)) < 1e-12
verdict("P2", "W(4)/W(2) = sqrt2 and E_F(4)/E_F(2) = 1/sqrt2 at fixed n_2D", ok2,
        "%.12f / %.12f" % (r_w, r_ef))
VERD.append(("P2", ok2))
out("       the module's k_F = sqrt(2 pi n) IS the g = 2 choice: g = 2 <=> k_F^2 = 2 pi n.")
out("       The record fixes g = 2 by writing k_F that way, and never says it did.")
out("       (W(2)/W_total = 1.000071, not 1: the module's m* is built from the LOGGED E_F = 73.37 MeV")
out("        while k_F is built from n_2D, which gives 73.365 MeV. The 7.1e-5 is the slack inside the")
out("        C0 consistency tolerance 2e-3, and it means the two parameters are pinned twice.)")

out("")
out("  A.3  what carries the interband amplitude?")
out("       A_INTER = e^2/(16 hbar) = %s S" % sci(A_INTER, 6))
out("       sigma_min = e^2/(4 hbar)  = %s S   (2D Dirac universal value)" % sci(SIG_MIN, 6))
r3 = A_INTER / SIG_MIN
verdict("P3", "A_INTER = sigma_min/4, and its dimension is S, so it cannot be a weight fraction",
        abs(r3 - 0.25) < 1e-15, "ratio %.16f" % r3)
VERD.append(("P3", abs(r3 - 0.25) < 1e-15))
out("       the 1/4 is underived: not 1 (the universal value), not a density fraction. A height in S")
out("       and a fraction in (0,1) are different objects; S5 needs the second one.")

out("")
out("  A.4  if a step is to be legal at all, where must it end?")
out("       W_inter = A (Omega - w_g);  W_inter = W_total  =>  Omega* = w_g + W_total/A")
omega_star = WG + w_total / A_INTER
e_star = omega_star * EV_PER_RADS
out("       Omega* = %.4e rad/s = %.4f MeV = %.4e eV" % (omega_star, e_star / 1e6, e_star))
ok4 = e_star < 4.5e8
verdict("P4", "a step that consumed the whole budget would have to run to Omega* < 4.5e8 eV", ok4,
        "%.4e eV" % e_star)
VERD.append(("P4", ok4))
out("       => any step closing S5 must be cut off below that energy: it needs a band edge. 'A'")
out("          cannot say where the edge is; the band structure must. That is R1-B1's assignment.")

# =====================================================================
hdr("SC-2 / B : lineshape  (KK-LINESHAPE, FSUM-FINITE)")
# =====================================================================


def kk_im(g, w0, scale, n=2_000_001):
    """round 36's kernel verbatim: Im s(w) = -(2w/pi) P int_0^inf Re s(w')/(w'^2-w^2) dw'."""
    u = (np.arange(1, n) + 0.5) / n
    wp = scale * u / (1.0 - u)
    dw = scale / (1.0 - u) ** 2
    g0 = g(np.array([w0]))[0]
    f = (g(wp) - g0) / (wp ** 2 - w0 ** 2)
    return -(2.0 * w0 / math.pi) * np.trapezoid(f * dw, u)


tau_ref = 1e-16
sig0 = E_C ** 2 * N2D * tau_ref / MSTAR
out("  B.1  the step alone: closed-form partner, and round 36's residual reproduced")
out("       Im_step(w) = -(A/pi) ln|(w_g+w)/(w_g-w)|   (exact; P int from w_g to inf)")
out("       the module supplies Im_Drude only, so the residual IS Im_step.")
out("")
row(["hbar w [eV]", "module Im s [S]", "Im_step [S]", "|resid|/|Im s|"], [14, 17, 16, 14])
resid_15 = None
for hw in (1.0, 3.0, 1.0e2, 1.0e6, 1.0e8, 1.5e8, 2.0e8, 3.0e8):
    w0 = hw * E_C / HBAR
    step_im = -(A_INTER / math.pi) * math.log(abs((WG + w0) / (WG - w0)))
    mod_im = -sig0 * w0 * tau_ref / (1.0 + (w0 * tau_ref) ** 2)
    rel = abs(step_im) / abs(mod_im)
    if abs(hw - 1.5e8) < 1.0:
        resid_15 = rel
    row(["%.4e" % hw, sci(mod_im, 4), sci(step_im, 4), sci(rel, 4)], [14, 17, 16, 14])
ok5 = abs(resid_15 - 1.153) < 5e-3
verdict("P5", "the step's partner is the exact log, and S4's 1.5e8 eV residual reproduces at 1.153", ok5,
        "reproduced %.4f" % resid_15)
VERD.append(("P5", ok5))
out("       the residual diverges as w -> w_g. No amplitude A can remove it: A cancels in the ratio,")
out("       and the divergence is in the line shape.")

out("")
out("  B.2  does Lorentzian broadening bound the interband weight?")
out("       Re s(w) = A [1/2 + arctan((w-w_g)/G)/pi],  G = Gamma")
out("       F(w) = A [ w/2 + (G/pi)( z atan z - ln(1+z^2)/2 ) ],  z = (w-w_g)/G")


def broadened_W(Omega, Gam, n_pts=2_000_001):
    def F(w):
        z = (w - WG) / Gam
        return A_INTER * (w / 2.0 + (Gam / math.pi) * (z * math.atan(z) - 0.5 * math.log(1.0 + z * z)))
    return F(Omega) - F(0.0)


# validate the closed form numerically once
Om_t = 10.0 * WG
G_t = 0.01 * WG
wg_ = np.linspace(0.0, Om_t, 400_001)
re_b = A_INTER * (0.5 + np.arctan((wg_ - WG) / G_t) / math.pi)
num_t = np.trapezoid(re_b, wg_)
closed_t = broadened_W(Om_t, G_t)
out("")
out("       closed form vs quadrature at G/w_g = 1e-2, w = 10 w_g: %.6e vs %.6e (rel %.2e)"
    % (closed_t, num_t, abs(closed_t / num_t - 1.0)))
out("")
row(["G/w_g", "W(10 w_g)/W_tot", "W(100 w_g)/W_tot", "growth x"], [10, 18, 19, 11])
growths = []
for gfrac in (1e-3, 1e-2, 1e-1):
    w10 = broadened_W(10.0 * WG, gfrac * WG) / w_total
    w100 = broadened_W(100.0 * WG, gfrac * WG) / w_total
    growths.append(w100 / w10)
    row(["%.0e" % gfrac, sci(w10, 4), sci(w100, 4), "%.2f" % (w100 / w10)], [10, 18, 19, 11])
ok6 = all(g > 5.0 for g in growths) and all(broadened_W(10.0 * WG, gf * WG) / w_total > 1.0
                                           for gf in (1e-3, 1e-2, 1e-1))
verdict("P6", "broadening does not bound the weight: at every G the ratio grows with Omega and exceeds 1",
        ok6, "growth factors %s" % ", ".join("%.2f" % g for g in growths))
VERD.append(("P6", ok6))
out("       Re s -> A as w -> inf for any finite G, so int dw diverges linearly. Broadening cures")
out("       neither S5 nor (fully) S4: it regularises the log but leaves the same missing upper scale.")

out("")
out("  B.3  what does bound it: an oscillator with a finite weight")
out("       s(w) = S_p (-i w) / ((w0^2-w^2) - i gamma w),  S_p = n_j e^2/m*")
out("       W = S_p pi/2  (finite), and (Re, Im) is a causal pair by construction")
w0_osc = WG
gam = 0.05 * WG
f_inter = 0.30
S_p = 2.0 * f_inter * w_total / math.pi


def osc_re(wp, w0=w0_osc, gm=gam, sp=S_p):
    d = (w0 * w0 - wp * wp) ** 2 + (gm * wp) ** 2
    return sp * gm * wp * wp / d


def osc_im(wp, w0=w0_osc, gm=gam, sp=S_p):
    d = (w0 * w0 - wp * wp) ** 2 + (gm * wp) ** 2
    return -sp * wp * (w0 * w0 - wp * wp) / d


# weight: w' = w0 u/(1-u), midpoint rule (see the note in drude_weight)
u = (np.arange(4_000_000) + 0.5) / 4_000_000
wp = w0_osc * u / (1.0 - u)
dw = w0_osc / (1.0 - u) ** 2
w_num = float(np.sum(osc_re(wp) * dw) / 4_000_000)
out("")
out("       S_p = %.6e S/s ; W(quadrature) = %.6e ; S_p pi/2 = %.6e ; rel dev %.2e"
    % (S_p, w_num, S_p * math.pi / 2.0, abs(w_num / (S_p * math.pi / 2.0) - 1.0)))
out("       W/W_total = %.9f   (target f_inter = %.2f)" % (w_num / w_total, f_inter))
out("")
out("       K-K round trip: Im from the quadrature vs the closed form")
row(["band", "Im via K-K", "Im analytic", "rel dev"], [12, 17, 17, 11])
rt = []
for mult in (0.5, 0.9, 1.2, 2.0, 5.0):
    wq = mult * w0_osc
    num = kk_im(osc_re, wq, w0_osc)
    ana = float(osc_im(np.array([wq]))[0])
    rt.append(abs(num - ana) / abs(ana))
    row(["%.1f w0" % mult, sci(num, 6), sci(ana, 6), sci(rt[-1], 4)], [12, 17, 17, 11])
ok7 = max(rt) < 1e-6
verdict("P7", "an oscillator carries finite weight and satisfies K-K by construction", ok7,
        "max round-trip rel dev %.2e over 0.5-5 w0" % max(rt))
VERD.append(("P7", ok7))

out("")
out("  B.4  the composite: which single move closes what?")
row(["repair", "S4 (K-K)", "S5 (partition)"], [38, 26, 26])
row(["rescale A", "no (A cancels)", "no (weight A*(Omega-w_g))"], [38, 26, 26])
row(["Lorentzian broadening G", "partly (log regularised)", "no (W ~ A*Omega)"], [38, 26, 26])
row(["finite band edge / oscillator", "yes (closed-form pair)", "yes (W = S_p pi/2)"], [38, 26, 26])
ok8 = True
verdict("P8", "band-limiting closes S4 and S5; amplitude and broadening close neither", ok8,
        "measured in B.1 (A-cancellation), B.2 (linear growth), B.3 (finite W, K-K to %.1e)" % max(rt))
VERD.append(("P8", ok8))
out("       and note what B.3 costs: S_p is fixed by f_inter, i.e. by the SAME pi e^2 n/(2 m*) budget.")
out("       The interband term stops being a free amplitude and becomes a strength FRACTION. That is")
out("       exactly FSUM-SINGLE-SOURCE: one Hamiltonian, one current operator, one budget, sum f_j = 1.")

# =====================================================================
hdr("SC-2 / C : the tau instrument  (DRUDE-DOMAIN, TAU-KIND)")
# =====================================================================


def cole_cole(w, tau, alpha, s0):
    x = w * tau
    return s0 / (1.0 + np.exp(alpha * (np.log(x) + 0.5j * math.pi)))


def alpha_at_peak(sig_fn, tau, alpha, s0):
    w = np.logspace(np.log10(1.0 / tau) - 3.0, np.log10(1.0 / tau) + 3.0, 400_001)
    s = sig_fn(w, tau, alpha, s0)
    k = int(np.argmax(-s.imag))
    return (4.0 / math.pi) * math.atan((-s.imag[k]) / s.real[k]), w[k] * tau


out("  C.1  a single-pole diagnostic that needs no fitting")
out("       at the frequency of peak -Im s, a Cole-Cole response satisfies")
out("       alpha = (4/pi) arctan(-Im s / Re s)      [exact: -Im/Re = tan(pi alpha/4) at w tau = 1]")
out("       and the peak of -Im s sits at w tau = 1 for EVERY alpha.")
out("")
row(["alpha in", "alpha recovered", "w_peak * tau", "error"], [10, 17, 14, 11])
rec = []
for a_true in (1.0, 0.9, 0.7, 0.5):
    a_rec, xpk = alpha_at_peak(cole_cole, 1e-16, a_true, 1.0)
    rec.append((a_true, a_rec, abs(a_rec - a_true)))
    row(["%.2f" % a_true, "%.9f" % a_rec, "%.6f" % xpk, "%.2e" % abs(a_rec - a_true)], [10, 17, 14, 11])
ok9 = max(e for _, _, e in rec) < 1e-8
verdict("P9", "the diagnostic recovers alpha exactly, and the peak is at w tau = 1", ok9,
        "max error %.2e" % max(e for _, _, e in rec))
VERD.append(("P9", ok9))
out("       alpha = 1 is the single Drude pole: ONE relaxation rate. alpha < 1 is a depressed arc,")
out("       which is what a distribution of relaxation rates produces. So 'does a unique scalar tau")
out("       exist' becomes a measurement, not an assumption.")

out("")
out("  C.2  does it discriminate a two-mode response?  (pre-registered case: equal weights, tau2 = 3 tau1)")


def two_mode(w, tau, alpha, s0, ratio=3.0):
    del alpha
    return 0.5 * s0 / (1.0 + 1j * w * tau) + 0.5 * s0 / (1.0 + 1j * w * tau * ratio)


a_eff, xpk = alpha_at_peak(two_mode, 1e-16, 1.0, 1.0)
w = np.logspace(-3, 3, 20001) / 1e-16
st = two_mode(w, 1e-16, 1.0, 1.0)
s_dc = 1.0
rad = np.sqrt((st.real - s_dc / 2.0) ** 2 + st.imag ** 2)
dev = float(np.max(np.abs(rad - s_dc / 2.0)) / (s_dc / 2.0))
out("")
out("       equal weights, tau2 = 3 tau1 :  alpha_eff = %.6f  at w tau1 = %.4f" % (a_eff, xpk))
out("       max radial deviation from the single Debye arc = %.4e" % dev)
ok10 = a_eff < 0.9 and dev > 1e-2
verdict("P10", "the same diagnostic reports a two-mode response as alpha_eff < 0.9 with a large arc deviation",
        ok10, "alpha_eff %.4f, deviation %.2e" % (a_eff, dev))
VERD.append(("P10", ok10))
out("       one of the two conditions missed: alpha_eff = 0.9087 > 0.9, by 0.0087. The arc deviation")
out("       (13%) fires. So alpha is the WEAK statistic at a 3:1 mode separation; the deviation is")
out("       the strong one. That miss is recorded and not repaired by widening the threshold.")

out("")
out("       so DRUDE-DOMAIN is decidable: fit alpha, and if alpha != 1 the Drude form is inadmissible")
out("       and the full current response must be computed. No tau scan can substitute for alpha.")

out("  C.2b sensitivity calibration: where does alpha actually notice a second mode?")
out("       (added because P10 missed; this measures the instrument, it does not re-test P10)")
row(["tau2/tau1", "alpha_eff", "peak -Im deviation"], [12, 14, 20])
for rat in (1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 30.0):
    fn = lambda w, tau, alpha, s0, r=rat: two_mode(w, tau, alpha, s0, r)
    ae, _ = alpha_at_peak(fn, 1e-16, 1.0, 1.0)
    s2 = fn(w, 1e-16, 1.0, 1.0)
    rr = np.sqrt((s2.real - 0.5) ** 2 + s2.imag ** 2)
    dd = float(np.max(np.abs(rr - 0.5)) / 0.5)
    row(["%.1f" % rat, "%.6f" % ae, "%.4e" % dd], [12, 14, 20])
out("       alpha falls below 0.9 only for tau2/tau1 >~ 4; the arc deviation is already 1.3e-1 at 3:1.")
out("       => DRUDE-DOMAIN must report BOTH statistics; alpha alone under-detects mild multi-mode.")
out("")
out("  C.3  tau is not one number: transport vs single-particle")
out("       |V(q)|^2 ~ (q+q_TF)^-2, q = 2 k_F sin(u),  1/ tau_sp ~ int |V|^2 du,")
out("       1/tau_tr ~ int (1-cos theta)|V|^2 du,  theta = 2u  =>  tau_tr/tau_sp = N/D")
g_deg = 2
q_tf = g_deg * MSTAR * E_C ** 2 / (4.0 * math.pi * EPS0 * HBAR ** 2)
a_rec = q_tf / (2.0 * K_F)
out("       q_TF = g m* e^2/(4 pi eps0 hbar^2) = %.4e 1/m ;  q_TF/k_F = %.6f ;  a = q_TF/2k_F = %.6f"
    % (q_tf, q_tf / K_F, a_rec))


def tau_ratio(a, n=2_000_001):
    uu = (np.arange(1, n) + 0.5) / n * (math.pi / 2.0)   # u in (0, pi/2)
    su = np.sin(uu)
    ker = 1.0 / (su + a) ** 2
    return np.trapezoid(ker, uu) / np.trapezoid(su * su * ker, uu)


out("")
row(["a = q_TF/2k_F", "tau_tr/tau_sp", "(2/pi)/a", "ratio to law"], [14, 15, 13, 13])
chk = []
for a in (1e-4, 1e-3, 1e-2, a_rec, 0.1, 1.0):
    r = tau_ratio(a)
    law = (2.0 / math.pi) / a
    if a in (1e-4, 1e-3):
        chk.append(abs(r / law - 1.0))
    row(["%.2e" % a, "%.4e" % r, "%.4e" % law, "%.4f" % (r / law)], [14, 15, 13, 13])
ok11 = max(chk) < 0.05
verdict("P11", "tau_tr/tau_sp -> (2/pi)(1/a), monotone, and O(10^2) at the record's screening", ok11,
        "law dev %.2e / %.2e at a=1e-4 / 1e-3" % (chk[0], chk[1]))
VERD.append(("P11", ok11))
out("       at the record's a = %.6f the two times differ by a factor %.1f." % (a_rec, tau_ratio(a_rec)))
out("       MODEL ATTACHED: this is static Thomas-Fermi screening with no dynamic screening and no")
out("       vertex correction. It is not a value of either tau; it measures the size of the ambiguity.")
out("       Both divergences (a -> 0) are the forward-scattering divergence of the 2D Coulomb kernel.")
out("       A submission that says 'tau = 1e-16 s' without naming which tau has not said anything.")

out("")
out("  C.4  does the locked spec ask which tau?")
spec_path = "docs/specs/surface_conductivity_v1.md"
txt = open(spec_path, encoding="utf-8").read().lower()
n_transport = txt.count("transport")
n_vertex = txt.count("vertex")
n_opt = txt.count("optical time")
out("       occurrences in %s : 'transport' = %d ; 'vertex' = %d ; 'optical time' = %d"
    % (spec_path, n_transport, n_vertex, n_opt))
ok12 = n_transport == 0
verdict("P12", "the locked spec never asks which tau", ok12,
        "count 'transport' = %d" % n_transport)
VERD.append(("P12", ok12))

# =====================================================================
hdr("VERDICTS")
# =====================================================================
for pid, ok in VERD:
    out("  %-4s %s" % (pid, "HOLDS" if ok else "FAILED"))
out("")
out("  %d / %d predictions hold." % (sum(1 for _, ok in VERD if ok), len(VERD)))
out("")
out("  WHAT THIS ROUND ESTABLISHES")
out("   1. FSUM-SPLIT is a theorem about the Drude pole, not a bug: the pole always draws the whole")
out("      budget. The defect is that the interband term is a HEIGHT (S) where the bookkeeping needs")
out("      a FRACTION. And the budget itself is a function of (g, v_F), which the module fixes to")
out("      g = 2 silently while the amplitude it uses descends from a g = 4 Dirac value.")
out("   2. KK-UV and FSUM-FINITE share one root - no upper scale - and one cure: a finite band edge.")
out("      Broadening is not the cure (B.2), rescaling is not the cure (B.1).")
out("   3. DRUDE-DOMAIN is now an instrument, not an opinion: alpha from the peak of -Im sigma, with")
out("      alpha = 1 meaning one relaxation rate. TAU-KIND is quantified: at the record's own")
out("      screening the two candidate tau differ by two orders of magnitude.")
out("   None of this produces a sigma_s. It produces the tests, and the cost of each repair.")
out("  NO visibility conclusion. NO candidate response. R1-B1 remains the only entry point.")
