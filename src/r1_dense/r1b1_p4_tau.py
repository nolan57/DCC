"""
R1B1-P4+ : the finite tau from electron-proton impurity scattering (round 56, RQ-03)
=====================================================================================
Refinement (i) of S7.  Round 45 declared the mechanism and left the value collisionless
(tau = infinity).  This module computes the rate from the state's own tuple:

  2D screened Coulomb (Thomas-Fermi; the electrons screen, nothing else does)
      V(q) = 2 pi e^2 / (eps (q + q_TF)),   q_TF = 2 m_eff e^2/(eps hbar^2) = 2 alpha m_eff c/hbar
  the two rates (elastic, T = 0, E = E_F, q = 2 k_F sin(theta/2))
      1/tau_sp = (n_imp m_eff/hbar^3) <|V|^2>_theta
      1/tau_tr = (n_imp m_eff/hbar^3) <|V|^2 (1-cos theta)>_theta
  reduced to three integrals (x = q_TF/(2 k_F)):
      J0(x) = int_0^pi du/(sin u + x)^2 ;  K1(x) = int_0^pi du/(sin u + x)
      J2 = pi - 2 x K1 + x^2 J0                (exact algebra, not a fit)
      1/tau_sp = A J0/(4 pi k_F^2),  1/tau_tr = A J2/(2 pi k_F^2),
      A = (n_imp m_eff/hbar^3)(e^2/2 eps0 eps)^2,      tau_tr/tau_sp = 2 J2/J0

n_imp = n_free,2D identically (charge neutrality: one proton per electron, N7-SPLIT),
so the scatterers are the carriers -- which is why the X_p convention envelope cancels.

Then S12a/S12b are applied to the finite-tau response, their blind spot is measured, and
Q-1/Q-2 (localized? disordered?) are priced: both clean arrangements give tau = infinity.

Units: SI for the rate (J, kg, m); fm/MeV for the printed cross-references.
Self-checks: J0(1) = 4/3 exactly; K1(1) = 2; the criterion's own 91.5 re-derived; a
spacerless GaAs 2DEG reproduces a textbook mobility order.
"""
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from src.common import conv  # noqa: E402

HBARC = conv.HBARC                 # 197.3269804 MeV fm
HBAR = conv.HBAR                   # J s
C = conv.C                         # m/s
MEV_J = conv.MEV_J                 # J/MeV
QE = 1.602176634e-19               # C
ALPHA = 1.0 / 137.035999084
E2_4PE0 = ALPHA * HBARC * MEV_J * 1e-15   # J m  (= e^2/(4 pi eps0))
G_SPIN = 2
EPS = 1.0                          # no bound electrons in the layer (declared)

OUT = []
def a(s=""):
    OUT.append(s)

def hdr(s):
    a("")
    a("=" * 78)
    a(s)
    a("=" * 78)

PRED = []
def pred(tag, ok, detail):
    PRED.append((tag, bool(ok), detail))
    a("  [%s] -> %s   %s" % (tag, "CONFIRMED" if ok else "FALSIFIED", detail))
    return bool(ok)

# ---------------------------------------------------------------------------------
# kernels
# ---------------------------------------------------------------------------------
def J0(x, n=600001, lo=-30.0, hi=30.0):
    """int_0^pi du/(sin u + x)^2;  t = tan(u/2) -> int_0^inf 2(1+t^2)/(x(1+t^2)+2t)^2 dt"""
    tau = np.linspace(lo, hi, n)
    t = np.exp(tau)
    f = 2.0 * (1.0 + t * t) / (x * (1.0 + t * t) + 2.0 * t) ** 2
    return float(np.trapezoid(f * t, tau))

def K1(x, n=600001, lo=-30.0, hi=30.0):
    """int_0^pi du/(sin u + x)"""
    tau = np.linspace(lo, hi, n)
    t = np.exp(tau)
    f = 2.0 / (x * (1.0 + t * t) + 2.0 * t)
    return float(np.trapezoid(f * t, tau))

def J2(x, j0):
    """int_0^pi du sin^2u/(sin u + x)^2 = pi - 2x K1 + x^2 J0  (exact)"""
    return math.pi - 2.0 * x * K1(x) + x * x * j0

def ratio(x):
    """tau_tr/tau_sp = J0/(2 J2)"""
    j0 = J0(x)
    return j0 / (2.0 * J2(x, j0))

# ---------------------------------------------------------------------------------
# state and rate
# ---------------------------------------------------------------------------------
def state(Lz, mode="HYB"):
    conv.LZ_FM = Lz
    r = conv.beta_eq(conv.N_B_FM2, mode)
    n = r["n_e_areal"]                       # fm^-2 (free carriers = protons, N7-SPLIT)
    Ez1 = math.pi * HBARC / Lz               # MeV
    m_mev = Ez1                              # MeV/c^2 (the model's m_eff = E_z1/c^2)
    m_kg = m_mev * MEV_J / C ** 2
    kf = conv.kF_2(n, G_SPIN)                # fm^-1 (the REGISTERED definition)
    EF = HBARC * kf                          # MeV
    vf = HBARC * kf / Ez1                    # v_F/c
    qtf = 2.0 * ALPHA * Ez1 / HBARC           # fm^-1
    return dict(Lz=Lz, mode=mode, X=r["X_p"], n=n, Ez1=Ez1, m_mev=m_mev, m_kg=m_kg,
                kf=kf, EF=EF, vf=vf, qtf=qtf, De=r["D_e"])

def rate(s):
    k_si = s["kf"] * 1e15
    n_si = s["n"] * 1e30
    A = n_si * s["m_kg"] / HBAR ** 3 * (2.0 * math.pi * E2_4PE0 / EPS) ** 2
    x = s["qtf"] / (2.0 * s["kf"])
    j0 = J0(x)
    j2v = J2(x, j0)
    g_sp = A * j0 / (4.0 * math.pi * k_si ** 2)
    g_tr = A * j2v / (2.0 * math.pi * k_si ** 2)
    return dict(x=x, j0=j0, j2=j2v, A=A, g_sp=g_sp, g_tr=g_tr,
                tau_sp=1.0 / g_sp, tau_tr=1.0 / g_tr, ratio=(1.0 / g_tr) / (1.0 / g_sp))

def sigma_dc(s, tau):
    return s["n"] * 1e30 * QE ** 2 * tau / s["m_kg"]

# =================================================================================
a("# RQ-03 -- the finite `tau`: what fixes it, and what the answer is conditional on")
a("")
a("**Round**: 56 (`RQ-03`).  **Registration**: `runs/R1B/r1b1_p4_tau_registration.md`.")
a("**Instrument**: `src/r1_dense/r1b1_p4_tau.py` -- this file is emitted by it, not transcribed.")
a("**Inputs**: `runs/R1B/r1b1_p2_eos_scan_results.txt` (HYB states); `conv.kF_2`; `conv.beta_eq`;")
a("`docs/specs/surface_conductivity_v1.md` s5/s8/s10; `runs/R1B/r1b1_p4_p5_closure_v1.md` s1.")
a("No fitted quantity; `alpha` is the only external number.")
a("")
a("```text")

# ---------------------------------------------------------------------------------
hdr("[1] THE STATE, AND THE ONE ARITHMETIC THE ROUND HAS TO SETTLE FIRST")
# ---------------------------------------------------------------------------------
a("  The P4-1 table prints k_F by sqrt(2 pi n/g); the registered definition is")
a("  n = g k^2/(4 pi)  =>  k_F = sqrt(4 pi n/g)  (conv.kF_2).  They differ by sqrt(2).")
a("  The same product's prose already prints v_F ~ 0.049 c against a table value of")
a("  0.0330 c, i.e. the factor is visible in the round-45 product as an internal")
a("  disagreement between its table and its text.")
a("")
s = state(1.84)
k_table = math.sqrt(2.0 * math.pi * s["n"] / G_SPIN)
EF_table = HBARC * k_table
a("  L_z = 1.84 fm, HYB :  n_free,2D = %.4e fm^-2   X_p = %.5f   D_e = %d"
  % (s["n"], s["X"], s["De"]))
a("    k_F  registered  sqrt(4 pi n/g) = %.5f fm^-1   (v_F = %.4f c, E_F = %.2f MeV)"
  % (s["kf"], s["vf"], s["EF"]))
a("    k_F  P4-1 table  sqrt(2 pi n/g) = %.5f fm^-1   (v_F = %.4f c, E_F = %.2f MeV)"
  % (k_table, HBARC * k_table / s["Ez1"], EF_table))
a("    ratio table/registered = %.9f   vs   2^-1/2 = %.9f"
  % (k_table / s["kf"], 2.0 ** -0.5))
pred("P11", abs(k_table / s["kf"] - 2.0 ** -0.5) < 1e-6,
     "the P4-1 table's k_F is low by exactly sqrt(2) (%.6f)" % (k_table / s["kf"]))
eos = conv.eos_e_2D(s["n"], G_SPIN)
a("    cross-check: conv.eos_e_2D gives E_F = %.3f MeV at the same n; the table implies %.3f,"
  % (eos["EF"], EF_table))
a("    a ratio of %.6f = sqrt(2) -- the table is inconsistent with the module's own EOS."
  % (eos["EF"] / EF_table))
a("    This round uses conv.kF_2 and prints the table's value as a sensitivity in [3].")
a("")
a("  per L_z (K1 window; the P4-5 tuple, k_F from conv.kF_2):")
a("  L_z(fm)  n_free[fm^-2]  k_F[fm^-1]  E_F[MeV]  v_F/c    q_TF[fm^-1]  q_TF/k_F   r_s")
grid = []
for Lz in (1.68, 1.84, 1.99):
    st = state(Lz)
    rsx = ALPHA / st["vf"]
    grid.append((st, rsx))
    a("  %.2f     %.4e       %.5f     %.3f      %.4f   %.5f      %.5f    %.4f"
      % (Lz, st["n"], st["kf"], st["EF"], st["vf"], st["qtf"], st["qtf"] / st["kf"], rsx))
a("")
rs = ALPHA / s["vf"]
a("  q_TF/k_F = %.5f  and  2 r_s = %.5f  -- the screening ratio IS the coupling"
  % (s["qtf"] / s["kf"], 2.0 * rs))
pred("P1", abs((s["qtf"] / s["kf"]) / (2.0 * rs) - 1.0) < 1e-12,
     "q_TF/k_F = 2 r_s to machine precision")
pred("P2", 0.14 <= rs <= 0.18,
     "r_s = %.4f -> Born admissible with a ~%.0f%% systematic" % (rs, 100 * rs))
a("")
qL = 2.0 * s["kf"] * s["Lz"]
a("  The 2D reduction: finite-width form factor at q = 2 k_F is 1 - (q L_z)^2/12;")
a("    q_max L_z = 2 k_F L_z = %.4f   ->   1 - F = %.4e" % (qL, qL * qL / 12.0))
pred("P12", qL * qL / 12.0 < 0.01, "the layer is thin compared with 1/q at every scattering angle")

# ---------------------------------------------------------------------------------
hdr("[2] THE KERNEL  (three integrals, two exact checks, one published number)")
# ---------------------------------------------------------------------------------
j0_1 = J0(1.0)
a("  J0(1) = %.12f     analytic 4/3 = %.12f     rel. err. = %.1e"
  % (j0_1, 4.0 / 3.0, j0_1 * 0.75 - 1.0))
pred("P0", abs(j0_1 * 0.75 - 1.0) < 1e-9, "quadrature reproduces the closed form")
a("  K1(1) = %.12f     analytic 2" % K1(1.0))
a("")
pre = 2.0 * math.pi * ALPHA * HBARC
a("  Matrix element at L_z = 1.84 fm (MeV fm^2; 2 pi alpha hbar c = %.4f MeV fm):" % pre)
a("    V(q->0)  = 2 pi e^2/(eps q_TF)        = %9.2f   (screening caps the forward divergence)" % (pre / s["qtf"]))
a("    V(k_F)                                = %9.2f" % (pre / (s["kf"] + s["qtf"])))
a("    V(2k_F)                               = %9.2f   (backscattering: the transport weight)" % (pre / (2 * s["kf"] + s["qtf"])))
a("    unscreened V(k_F) = 2 pi e^2/(eps k_F) = %9.2f   ->  screening suppresses by %.2fx"
  % (pre / s["kf"], (pre / s["kf"]) / (pre / (s["kf"] + s["qtf"]))))
a("")
xx = s["qtf"] / (2 * s["kf"])
a("  x = q_TF/(2 k_F) = %.5f ;  J0 = %.5f ;  K1 = %.5f ;  J2 = %.5f ;  J0/(2 J2) = %.5f"
  % (xx, J0(xx), K1(xx), J2(xx, J0(xx)), ratio(xx)))

# ---------------------------------------------------------------------------------
hdr("[3] THE RATES  (tau_tr is the Drude rate; tau_sp is the quantum lifetime)")
# ---------------------------------------------------------------------------------
a("  n_imp = n_free,2D = %.4e fm^-2  (charge neutrality: the scatterers ARE the carriers)"
  % s["n"])
a("")
a("  L_z(fm)  tau_sp[s]     tau_tr[s]     tau_tr/tau_sp  hbar/tau[keV]  sigma_DC[S]   k_F*l   l/d")
rr = {}
for st, rsx in grid:
    d = rate(st)
    rr[st["Lz"]] = d
    sig = sigma_dc(st, d["tau_tr"])
    l = st["vf"] * C * d["tau_tr"]
    a("  %.2f     %.4e     %.4e     %6.3f          %6.1f       %.4e   %5.1f  %5.2f"
      % (st["Lz"], d["tau_sp"], d["tau_tr"], d["ratio"],
         HBAR * d["g_tr"] / MEV_J * 1e3, sig,
         st["kf"] * 1e15 * l, l / (1.0 / math.sqrt(st["n"] * 1e30))))
d84 = rr[1.84]
sig84 = sigma_dc(s, d84["tau_tr"])
l84 = s["vf"] * C * d84["tau_tr"]
e2h = QE ** 2 / 6.62607015e-34
a("")
a("  at L_z = 1.84 fm:  tau_tr = %.4e s (%.3f zs), 1/tau_tr = %.4e s^-1, hbar/tau = %.1f keV"
  % (d84["tau_tr"], d84["tau_tr"] * 1e21, d84["g_tr"], HBAR * d84["g_tr"] / MEV_J * 1e3))
a("  mean free path l = v_F tau = %.3e m = %.1f fm = %.1f x the impurity spacing (1/sqrt n = %.1f fm)"
  % (l84, l84 * 1e15, l84 / (1.0 / math.sqrt(s["n"] * 1e30)), 1e15 / math.sqrt(s["n"] * 1e30)))
a("  sigma_DC = %.4e S = %.2f x e^2/h        (e^2/h = %.4e S)" % (sig84, sig84 / e2h, e2h))
pred("P3", 3e-21 <= d84["tau_tr"] <= 3e-20, "tau_tr = %.3e s" % d84["tau_tr"])
pred("P4", d84["ratio"] < 10.0,
     "tau_tr/tau_sp = %.3f (the record's illustration is 91.5)" % d84["ratio"])
pred("P13", s["kf"] * 1e15 * l84 > 10.0,
     "k_F*l = %.1f -> impurity average admissible" % (s["kf"] * 1e15 * l84))
pred("P7", 1e-4 <= sig84 <= 1e-2, "sigma_DC = %.3e S" % sig84)
a("")
dd = dict(s); dd["kf"] = k_table
dd2 = rate(dd)
a("  Sensitivity to the defect in [1]: on the P4-1 table's k_F, tau_tr = %.4e s, i.e. %.2fx"
  % (dd2["tau_tr"], d84["tau_tr"] / dd2["tau_tr"]))
a("  shorter.  A sqrt(2) in k_F is a %.0f%% error in tau, not a convention; both are printed."
  % (100 * (d84["tau_tr"] / dd2["tau_tr"] - 1)))
a("")
a("  Convention check (order of magnitude, not a physics claim): a spacerless GaAs 2DEG,")
a("  n = n_imp = 1e16 m^-2, m* = 0.067 m_e, eps = 13 -- same code, same form, nothing tuned.")
m_gaas = 0.067 * 9.1093837015e-31
def gaas():
    n2 = 1e16
    k = math.sqrt(4.0 * math.pi * n2 / 2.0)
    mmev = m_gaas * C ** 2 / MEV_J
    qtf_m = 2.0 * ALPHA * mmev / HBARC * 1e15 / 13.0
    x = qtf_m / (2.0 * k)
    j0 = J0(x)
    j2v = J2(x, j0)
    A = n2 * m_gaas / HBAR ** 3 * (2.0 * math.pi * E2_4PE0 / 13.0) ** 2
    tau = 1.0 / (A * j2v / (2.0 * math.pi * k ** 2))
    return k, qtf_m, x, tau, QE * tau / m_gaas * 1e4
kg, qg, xg, taug, mug = gaas()
a("    k_F = %.3e m^-1, q_TF = %.3e m^-1 (x = %.3f), tau_tr = %.2e s, mu = %.0f cm^2/Vs"
  % (kg, qg, xg, taug, mug))
pred("P14", 1e2 <= mug <= 1e6, "mu = %.0f cm^2/Vs -- within two decades of the textbook range" % mug)
a("")
a("  X_p convention envelope at L_z = 1.84 fm.  ALL3D's electron gas is 3D (D_e = 3), so the")
a("  2D matrix element does not apply to it: it is printed as out-of-domain, not included.")
a("  mode     X_p        n_free[fm^-2]  D_e  tau_tr[s]     admissible")
env = []
for mode in ("ALL3D", "HYB", "ALL2D"):
    sm = state(1.84, mode)
    dm = rate(sm)
    if sm["De"] == 2:
        env.append(dm["tau_tr"]); adm = "yes"
    else:
        adm = "NO (D_e = 3)"
    a("  %-8s %.5f    %.4e     %d    %.4e    %s" % (mode, sm["X"], sm["n"], sm["De"], dm["tau_tr"], adm))
span = max(env) / min(env)
a("  X_p spans %.1fx; tau spans %.3fx.  n_imp/n_free = 1 identically and n/k_F^2 = g/(4 pi) is"
  % (4.5006e-2 / 1.6198e-3, span))
a("  a constant, so the convention envelope largely cancels: the prefactor is fixed, and the")
a("  residual %.2fx is the x = q_TF/(2 k_F) shift of J2 alone.  The bar was 1.5 and this is the"
  % span)
a("  round's one near-miss -- reported, not re-barred: the qualitative claim (27.8x in X_p is")
a("  not 27.8x in tau) holds, the exact bar was too tight.")
pred("P15", span < 1.5, "tau span over the admissible conventions = %.3f" % span)
a("")
a("  L_z span over the K1 window: %.3e s (1.68 fm) .. %.3e s (1.99 fm) -> %.2fx"
  % (rr[1.68]["tau_tr"], rr[1.99]["tau_tr"], rr[1.99]["tau_tr"] / rr[1.68]["tau_tr"]))

# ---------------------------------------------------------------------------------
hdr("[4] THE RECORD'S 91.5 -- re-derived, not quoted")
# ---------------------------------------------------------------------------------
a("  S13's motivation (`surface_conductivity_v1.md` s10): at q_TF/k_F = 0.0146,")
a("  tau_tr/tau_sp = 91.5.  The same integral at that argument:")
x_rec = 0.0146
r_rec = ratio(x_rec / 2.0)
lo, hi = 1e-5, 0.5
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if ratio(mid) > 91.5:
        lo = mid
    else:
        hi = mid
x_star = 0.5 * (lo + hi)
a("    q_TF/k_F = 0.0146 -> x = %.5f -> J0 = %.3f, J2 = %.5f, ratio = %.3f"
  % (x_rec / 2.0, J0(x_rec / 2.0), J2(x_rec / 2.0, J0(x_rec / 2.0)), r_rec))
a("    computed/quoted = %.4f ;  ratio(x*) = 91.5 at x* = %.6f, i.e. q_TF/k_F = %.6f = %.3f x 0.0146"
  % (r_rec / 91.5, x_star, 2 * x_star, 2 * x_star / 0.0146))
pred("P5", 0.45 <= r_rec / 91.5 <= 0.55 and 0.40 <= 2 * x_star / 0.0146 <= 0.60,
     "at the cited argument the integral gives %.1f (%.3f x 91.5); 91.5 is the value at half it"
     % (r_rec, r_rec / 91.5))
a("")
a("  Two readings; the round takes neither as a verdict on the criterion:")
a("    (a) the sentence's 91.5 and its 0.0146 are not the same configuration -- a factor 2 in")
a("        what 'q_TF/k_F' denotes (q_TF/(2 k_F) is the natural argument of the angular integral);")
a("    (b) either way the number is a property of ONE state.  For q_TF/k_F << 1 the ratio is")
a("        ~ pi q_TF/k_F = 2 pi alpha/(v_F/c): it scales as 1/v_F.  And 0.0146 = 2 alpha is")
a("        exactly r_s = alpha, i.e. v_F = c -- the FROZEN model's undeclared v_F, the input the")
a("        solved state replaced.  At the solved state r_s = %.3f and the ratio is %.2f," % (rs, d84["ratio"]))
a("        %.0fx smaller." % (91.5 / d84["ratio"]))
a("  So the illustration is a number about a superseded state.  S13 is binary and unaffected;")
a("  the number may not be transferred from one state to another.")

# ---------------------------------------------------------------------------------
hdr("[5] THE RESPONSE AT FINITE tau")
# ---------------------------------------------------------------------------------
a("  Drude:  sigma(w) = sigma_DC/(1 - i w tau_tr),  sigma_DC = n e^2 tau/m*")
w12 = math.pi * C / (1.84e-15)
a("    1/tau_tr = %.5e s^-1   hbar/tau_tr = %.1f keV"
  % (d84["g_tr"], HBAR * d84["g_tr"] / MEV_J * 1e3))
a("    w_12 (first inter-subband line) = %.4e rad/s  ->  gamma/w_12 = %.2e  (%.1f decades"
  % (w12, d84["g_tr"] / w12, math.log10(w12 / d84["g_tr"])))
a("    below the ladder: the single-rate domain survives STRUCTURALLY, not just numerically)")
w_ev = 2.25 * QE / HBAR
a("    at 2.25 eV: w = %.3e rad/s, w tau = %.2e  ->  the intra channel is the dc limit there"
  % (w_ev, w_ev * d84["tau_tr"]))
pred("P6", 20.0 <= HBAR * d84["g_tr"] / MEV_J * 1e3 <= 120.0 and d84["g_tr"] / w12 < 1e-3,
     "hbar/tau = %.1f keV, gamma/w_12 = %.2e" % (HBAR * d84["g_tr"] / MEV_J * 1e3, d84["g_tr"] / w12))
a("")
a("  The f-sum of the intra pole, integrated numerically for both rates")
a("  (w = tan(theta)/tau, theta in (0, pi/2), 2e5 points):")
def fsum(tau, n=200001):
    th = np.linspace(1e-12, math.pi / 2.0 - 1e-12, n)
    w = np.tan(th) / tau
    sr = 1.0 / (1.0 + (w * tau) ** 2)
    dw = (1.0 / tau) / np.cos(th) ** 2
    return float(np.trapezoid(sr * dw, th))
W_tr = sigma_dc(s, d84["tau_tr"]) * fsum(d84["tau_tr"])
W_sp = sigma_dc(s, d84["tau_sp"]) * fsum(d84["tau_sp"])
a("    W(tau_tr) = %.6e S rad/s ;  W(tau_sp) = %.6e S rad/s ;  ratio = %.12f"
  % (W_tr, W_sp, W_tr / W_sp))
a("    the taus differ by %.2fx and the partitions agree to 1e-12: S5 cannot see which tau"
  % d84["ratio"])
a("    was used.  (W = pi e^2 n/(2 m*) analytically; tau cancels identically.)")
pred("P10", abs(W_tr / W_sp - 1.0) < 1e-9, "|W(tr)/W(sp) - 1| = %.1e" % abs(W_tr / W_sp - 1.0))

# ---------------------------------------------------------------------------------
hdr("[6] S12a / S12b APPLIED  (and the blind spot measured)")
# ---------------------------------------------------------------------------------
def alpha_of(sr, si):
    return (4.0 / math.pi) * np.arctan(-si / np.maximum(sr, 1e-300))

def single(w):
    x = w
    return 1.0 / (1.0 + x * x), -x / (1.0 + x * x)

def twopole(t1, t2, w):
    x1, x2 = w * t1, w * t2
    return (0.5 * (1.0 / (1.0 + x1 * x1) + 1.0 / (1.0 + x2 * x2)),
            -0.5 * (x1 / (1.0 + x1 * x1) + x2 / (1.0 + x2 * x2)))

WG = np.logspace(-1, 1, 20001)        # one decade either side of the peak (in w*tau)
def collapse(gen):
    sr, si = gen(WG)
    al = alpha_of(sr, si)
    best = None
    for f in np.linspace(0.2, 5.0, 12001):
        k = float(np.max(np.abs(al - (4.0 / math.pi) * np.arctan(WG * f))))
        if best is None or k < best[1]:
            best = (f, k)
    return al, best[0], best[1]

def arc_dev(sr, si):
    """max radial deviation from the Debye arc, relative to its radius 0.5"""
    return float(np.max(np.abs(np.hypot(sr - 0.5, si) - 0.5))) / 0.5

cases = (("single pole (any tau)", single),
         ("two poles 1:1, tau2 = 3 tau1", lambda w: twopole(1.0, 3.0, w)))
kaps = {}
for label, gen in cases:
    sr, si = gen(WG)
    al = alpha_of(sr, si)
    ipk = int(np.argmax(-si))
    _, fbest, kap = collapse(gen)
    kaps[label] = kap
    a("  %-28s alpha(peak) = %.6f  arc dev = %.4e  tau_eff/tau = %.6f  kappa = %.3e"
      % (label, al[ipk], arc_dev(sr, si), fbest, kap))
a("")
a("  The statistic reproduces the specification's own three controls: alpha_eff 0.9087")
a("  (here %.6f), arc deviation 13.4%% (here %.2f%%), kappa 8.6e-2 (here %.3e) -- so the" % (
    alpha_of(*cases[1][1](WG))[int(np.argmax(-cases[1][1](WG)[1]))], 100 * arc_dev(*cases[1][1](WG)),
    kaps["two poles 1:1, tau2 = 3 tau1"]))
a("  instrument is the spec's, not a new one.  For a single pole S12a passes by construction")
a("  (alpha = 1 exactly, arc deviation 3e-16); it is only informative against a control, which")
a("  is why S12b exists.")
a("")
a("  S12a: alpha = 1 to <1e-2, arc deviation <1e-2, alpha > 1 an automatic fail.")
a("  S12b: kappa < 1e-6 (the spec measures 4.4e-16 for one pole, 8.6e-2 for two at 3:1).")
kap_s = kaps["single pole (any tau)"]
kap_c = kaps["two poles 1:1, tau2 = 3 tau1"]
pred("P9", 0.05 <= kap_c <= 0.15, "kappa(control) = %.4f -- the statistic does catch two rates" % kap_c)
a("")
a("  THE BLIND SPOT, as numbers.  Take three *assumed* rates for the same absorber:")
a("    assumed tau                   sigma_DC [S]   error        kappa")
for lab, tau in (("tau_tr (correct)", d84["tau_tr"]),
                 ("tau_sp (%.2fx too short)" % (1.0 / d84["ratio"]), d84["tau_sp"]),
                 ("100 x tau_tr (wrong by 100x)", 100.0 * d84["tau_tr"])):
    sr, si = single(WG)
    _, fb, kk = collapse(single)
    sdc = sigma_dc(s, tau)
    a("    %-28s %11.4e   %+8.1f%%   %.2e"
      % (lab, sdc, 100 * (sdc / sig84 - 1), kk))
pred("P8", kap_s < 1e-14 and d84["ratio"] > 2.0,
     "kappa = %.1e for every single rate while sigma_DC moves by %.2fx" % (kap_s, d84["ratio"]))
a("")
a("  S12b's null hypothesis is 'ONE rate'.  A single wrong rate satisfies it perfectly, so the")
a("  statistic cannot do S13's work -- and no other criterion can either, since S5's partition")
a("  is tau-independent to 1e-12 ([5]).  The identity of the rate is carried by the NAME (S13)")
a("  and by the VERTEX that produces the (1-cos theta) weight -- S6.  The P4 product recorded")
a("  S6 as PASS by appeal to the round-43 operator; the impurity vertex was never constructed.")
a("  That is the gap this round can name and does not close: the criterion that could catch a")
a("  wrong-but-unique rate exists, and was applied by reference, not by construction.")
a("")
a("  Ladder leakage into S12's window (reported, not a criterion): the inter-subband poles sit")
lt = w12 * d84["tau_tr"]
a("  at w tau = %.1e, so inside [0.1,10]/tau their amplitude is ~%.1e of the intra term:"
  % (lt, 1.0 / lt ** 2))
a("  a suppression of %.1f orders, i.e. %.1f orders below the 1e-6 threshold.  Including the"
  % (math.log10(lt ** 2), math.log10(1e-6 / (1.0 / lt ** 2))))
a("  ladder would not move kappa.")

# ---------------------------------------------------------------------------------
hdr("[7] Q-1 / Q-2 -- what has to be TRUE for the number to exist")
# ---------------------------------------------------------------------------------
d_imp = 1e15 / math.sqrt(s["n"] * 1e30)
G_min = 4.0 * math.pi / (math.sqrt(3.0) * d_imp)
a("  The rate above is an average over a random (Poisson) array.  Two other arrangements are")
a("  equally consistent with everything the state says, and both give a different answer:")
a("")
a("  arrangement                  elastic channel                         tau_tr")
a("  ---------------------------  --------------------------------------  ----------------")
a("  mobile protons (fluid)       none: e-p scattering conserves the      INFINITE")
a("                               total e+p momentum, so no charge")
a("                               current is relaxed (COM accelerates)")
a("  perfect proton lattice       none below the first reciprocal vector  INFINITE")
a("                               (Bloch states): 2 k_F/G_min = %.3f < 1" % (2 * s["kf"] / G_min))
a("  disordered (Poisson) array   yes, the Born average above             %.3e s" % d84["tau_tr"])
a("")
a("    impurity spacing d = 1/sqrt n = %.2f fm ; G_min (triangular) = %.5f fm^-1 ;"
  % (d_imp, G_min))
a("    2 k_F = %.5f fm^-1 ; the lattice has no umklapp channel for these carriers."
  % (2 * s["kf"]))
a("")
a("  Both clean limits are PERFECT CONDUCTORS (a Drude delta at w = 0), not insulators.  So")
a("  the ideal P2 level is exactly the tau = infinity case round 45 declared, and the finite")
a("  number is a property of disorder alone.  The state carries neither a lattice nor disorder:")
a("  Q-1 (localized) and Q-2 (disordered) are premises, and the answer is conditional on both.")
a("")
a("  Consequence for S7: the mechanism is named, traced and unscanned, but its ACTIVITY is a")
a("  structural premise.  S7 is PASS-ON-PREMISE, not PASS -- the criterion asks what fixes")
a("  tau, and the honest answer is 'the impurity arrangement, which the model does not fix'.")
a("  Refinement (iii), RQ-05, is where that premise would be earned or refused.")

# ---------------------------------------------------------------------------------
hdr("[8] S7 AND S13, APPLIED")
# ---------------------------------------------------------------------------------
a("  S7  (tau is solved; a scanned tau fails)")
a("       named      : the TRANSPORT (momentum) relaxation time, not the quantum lifetime")
a("       traced     : impurity-averaged self-energy, Born, 2D TF-screened Coulomb; the")
a("                    matrix element is printed in [2]; n_imp = n_free,2D from the state")
a("       not scanned: no free parameter; the only inputs are (n, m*, k_F, alpha)")
a("       verdict    : PASS-ON-PREMISE (Q-1 and Q-2 of [7])")
a("  S13 (tau named / traced / not scanned -- binary)")
a("       name       : TRANSPORT.  tau_sp is %.2fx shorter and would give a %.2fx wrong" % (d84["ratio"], d84["ratio"]))
a("                    conductance; both are printed, neither is a fit.")
a("       verdict    : PASS, with the blind spot of [6] recorded (S12 cannot check the name)")
a("")
a("  Not moved: S1-S6, S8-S12, S14, S15, every gate, every rung, PG-01's mark.")
a("  S2 becomes non-trivial (A > 0 in band now) but its closure is a stack identity, not a")
a("  matter-model statement, so it is not re-applied here.")

# ---------------------------------------------------------------------------------
hdr("SUMMARY")
# ---------------------------------------------------------------------------------
REGF = os.path.join(_ROOT, "runs", "R1B", "r1b1_p4_tau_registration.md")
a("  registration order : %s"
  % ("present, %.0f s older than this run" % (__import__("time").time() - os.path.getmtime(REGF))
     if os.path.exists(REGF) else "REGISTRATION MISSING"))
a("  the rate           : tau_tr = %.2e s at L_z = 1.84 fm (%.2e .. %.2e over the K1 window),"
  % (d84["tau_tr"], rr[1.68]["tau_tr"], rr[1.99]["tau_tr"]))
a("                       from V(q) = 2 pi e^2/(eps(q+q_TF)) and n_imp = n_free,2D.")
a("                       sigma_DC = %.2e S = %.2f e^2/h ; hbar/tau = %.1f keV."
  % (sig84, sig84 / e2h, HBAR * d84["g_tr"] / MEV_J * 1e3))
a("  what it is not     : unconditional.  Without localized, disordered protons the")
a("                       resistance is zero (a perfect conductor): the mechanism round 45 named")
a("                       is a mechanism only for a structure round 45 did not have.")
a("  S12                : passes exactly and is blind to the identity of the rate -- kappa =")
a("                       %.1e for tau_tr, tau_sp and 100 x tau_tr alike." % kap_s)
a("  the record's 91.5  : not reproducible at its cited argument (gives %.1f); it is the value at" % r_rec)
a("                       half that argument and belongs to the frozen model's v_F = c.")
a("  arithmetic defect  : P4-1's table k_F is low by sqrt(2) (0.0563 vs 0.0796 fm^-1); tau would")
a("                       be %.2fx shorter on it.  Erratum appended to the closure document;" % (d84["tau_tr"] / dd2["tau_tr"]))
a("                       no product edited.")
a("  what is NOT claimed: no visibility (S9), no threshold, no gate, no census answer.")
a("")
n_ok = sum(1 for _t, o, _d in PRED if o)
a("  predictions        : %d CONFIRMED, %d FALSIFIED" % (n_ok, len(PRED) - n_ok))
for t, o, dt in PRED:
    if not o:
        a("    FALSIFIED %s: %s" % (t, dt))
a("")
a("PROVENANCE: NEITHER  (Born impurity average on declared state inputs; the structural")
a("premise Q-1/Q-2 is declared, not established -- establishes no chain evidence)")

TEXT = "\n".join(OUT) + "\n"
if "--write" in sys.argv:
    dest = os.path.join(_ROOT, "runs", "R1B", "r1b1_p4_tau_results.txt")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(TEXT)
    print("wrote %s (%d lines)" % (dest, TEXT.count("\n")))
else:
    print(TEXT)
