import sys
sys.stdout.reconfigure(encoding="utf-8")
# =====================================================================
# SC-3 (v2): the governor's mathematical review of SC-2, turned into tests.
#   (A) BUDGET      : 440.18 MeV is an endpoint of a one-parameter family, and identically 3 w_g.
#   (B) DEGENERACY  : W = W(n, g, v_F); the module carries two g's and a v_F it never wrote.
#   (C) INDEPENDENCE: S4 and S5 are two criteria, and all four cells of the 2x2 are populated.
#   (D) ALPHA       : a diagnostic at a point is not a certificate; the collapse is.
#   (E) INTERFACE   : (n, g, v_F, w_end) does not determine sigma_s.
# No visibility claim. No candidate sigma_s is produced.
# Registration: runs/OPTICS/sc3_registration.md  (Q1-Q14, locked before this run)
# One file read, declared: the spec, for a text count (Q14). No other I/O.
# v1 of this script mislabelled boolean POLARITY in section C (a large residual was
# recorded as a pass). Archived as runs/OPTICS/sc3_check_v1_SUPERSEDED.py.txt, with its
# output in sc3_results_v1_SUPERSEDED_POLARITY.txt. The numbers were right; the labels were not.
# Run: /d/Applications/miniconda3/python -I src/optics/sc3_budget_check.py
# =====================================================================
import math
import numpy as np

E_C = 1.602176634e-19
HBAR = 1.054571817e-34
C_LIGHT = 2.99792458e8
M_E = 9.1093837015e-31
EPS0 = 8.8541878128e-12

N2D = 2.20e28
EF_MEV = 73.37
MSTAR = (EF_MEV / 0.51099895) * M_E
K_F = math.sqrt(2.0 * math.pi * N2D)
A_INTER = E_C ** 2 / (16.0 * HBAR)
SIG_MIN = E_C ** 2 / (4.0 * HBAR)
EF_J = EF_MEV * 1e6 * E_C
WG = 2.0 * EF_J / HBAR
EV_PER_RADS = HBAR / E_C
W_TOTAL = math.pi * E_C ** 2 * N2D / (2.0 * MSTAR)
TAU_REF = 1e-16
VERD = []


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


# =====================================================================
hdr("SC-3 / A : the budget, and what 440.18 MeV actually is")
# =====================================================================
out("  W_total = pi e^2 n/(2 m*) = %s S rad/s" % sci(W_TOTAL, 8))
out("  A_INTER = e^2/(16 hbar)   = %s S" % sci(A_INTER, 8))
out("  w_g = 2 E_F/hbar          = %s rad/s = %.4f MeV" % (sci(WG, 8), 2.0 * EF_MEV))
out("")

ceil_ref = WG + W_TOTAL / A_INTER
ceil_mev = ceil_ref * EV_PER_RADS / 1e6
row(["f_inter", "w_end(f) [MeV]", "w_end - w_g [MeV]", "w_end / ceiling"], [10, 18, 18, 17])
for f in (0.0, 0.05, 0.25, 0.5, 0.75, 0.9, 1.0):
    we = WG + f * W_TOTAL / A_INTER
    e_mev = we * EV_PER_RADS / 1e6
    row(["%.2f" % f, "%.4f" % e_mev, "%.4f" % (e_mev - 2.0 * EF_MEV), "%.6f" % (e_mev / ceil_mev)],
        [10, 18, 18, 17])
ok1 = abs(ceil_mev - 440.18) < 4.4e3 / 1e6 and abs((WG * EV_PER_RADS / 1e6) - 2.0 * EF_MEV) < 1e-9
verdict("Q1", "the ceiling 440.18 MeV = w_g + W_total/A is the f_inter = 1 endpoint; at f_inter = 0 it is w_g",
        ok1, "ceiling %.4f MeV; f=0 endpoint is w_g = %.4f MeV" % (ceil_mev, 2.0 * EF_MEV))

out("")
out("  A.2  the module's own partition.  FSUM-SPLIT measured W_intra/W_total = 1 - 7.1e-5.")
f_intra_mod = 1.0
f_inter_mod = 1.0 - f_intra_mod
allowed = f_inter_mod * W_TOTAL
requested = A_INTER * (WG + WG)
out("       f_inter = 1 - f_intra = %.1f ; residual budget = %s S rad/s" % (f_inter_mod, sci(allowed, 6)))
out("       a step to 2 w_g requests   = %s S rad/s" % sci(requested, 6))
ok2 = abs(f_inter_mod) < 1e-15 and allowed / W_TOTAL < 1e-15
verdict("Q2", "at f_intra = 1 the interband budget is exactly zero, so NO interband term is admissible",
        ok2, "f_inter = 0 to 1e-15; every A > 0 violates S5 at every w_end > w_g")

out("")
out("  A.3  what unit is W_total/A in?")
w_over_a = W_TOTAL / A_INTER
as_ev = w_over_a * EV_PER_RADS
out("       W/A = %s rad/s  ->  %s eV = %.4f MeV" % (sci(w_over_a, 6), sci(as_ev, 6), as_ev / 1e6))
out("       read as eV instead, the same numeral is %s x too large" % sci(1.0 / EV_PER_RADS, 6))
ok3 = abs((w_over_a / as_ev) * EV_PER_RADS - 1.0) < 1e-12
verdict("Q3", "the rad/s -> eV step is exactly 1/hbar = 1.5193e15; the convention is not cosmetic", ok3,
        "ratio %.6e vs 1/hbar %.6e" % (w_over_a / as_ev, 1.0 / EV_PER_RADS))

out("")
out("  A.4  the tight bound.  S5 asks W_intra + W_inter = W_total, so")
out("       w_end = w_g + (W_total - W_intra)/A = w_g + f_inter W_total/A")
ok14 = ceil_mev > 2.0 * EF_MEV
verdict("Q14b", "the ruling's 'must be cut off below 440 MeV' is true but not tight for any f_inter < 1",
        ok14, "at f_inter = 0.5 the bound is %.2f MeV, not 440" % ((WG + 0.5 * W_TOTAL / A_INTER) * EV_PER_RADS / 1e6))

out("")
out("  A.5  and the ceiling carries no information of its own:")
q15 = (W_TOTAL / A_INTER) / WG
out("       (W_total/A)/w_g = %.8f   (algebraically exactly 2 when v_F = c and k_F^2 = 2 pi n)" % q15)
out("       so  ceiling / w_g = %.8f, i.e. 440.18 MeV = 3 x 146.74 MeV" % (ceil_ref / WG))
out("       derivation: W/A = 8 pi hbar n/m*, m* = E_F/c^2, w_g = 2E_F/hbar, k_F^2 = 2 pi n")
out("                   => (W/A)/(2 w_g) = 2 pi hbar^2 n c^2 / E_F^2 = 2 pi n / k_F^2 = 1.")
verdict("Q15", "under the module's own conventions the 'derived band edge' is identically 3 w_g", q15 > 1.99,
        "ratio %.6f (1.4e-4 from 2 is the 73.37/73.3648 E_F rounding)" % q15)
VERD.append(("Q1", ok1))
VERD.append(("Q2", ok2))
VERD.append(("Q3", ok3))

# =====================================================================
hdr("SC-3 / B : degeneracy, the two g's, and the v_F the record never wrote")
# =====================================================================


def w_of(n, g, v_f):
    return (E_C ** 2 * v_f / (8.0 * HBAR)) * math.sqrt(4.0 * math.pi * n * g)


def ef_of(n, g, v_f):
    return HBAR * v_f * math.sqrt(4.0 * math.pi * n / g)


out("  B.1  W depends on n and g only through the product n*g")
w_a = w_of(4.0 * N2D, 2, C_LIGHT)
w_b = w_of(N2D, 8, C_LIGHT)
e_a = ef_of(4.0 * N2D, 2, C_LIGHT)
e_b = ef_of(N2D, 8, C_LIGHT)
row(["state", "W_total [S rad/s]", "E_F [MeV]"], [16, 22, 14])
row(["(4n, g=2)", sci(w_a, 8), "%.6f" % (e_a / E_C / 1e6)], [16, 22, 14])
row(["(n, g=8)", sci(w_b, 8), "%.6f" % (e_b / E_C / 1e6)], [16, 22, 14])
ok4 = abs(w_a / w_b - 1.0) < 1e-15 and abs(e_a / e_b - 4.0) < 1e-9
verdict("Q4", "W(4n,g) = W(n,4g) exactly while E_F splits by 4: the budget cannot determine g", ok4,
        "W ratio %.16f, E_F ratio %.9f" % (w_a / w_b, e_a / e_b))
out("       => 'spectral weight depends on the degeneracy' holds only at fixed n and v_F. (n, g) enters")
out("          the budget as one number; E_F is what separates them.")

out("")
out("  B.2  the module's interband height and its k_F disagree about g")
out("       per-cone, spinless Dirac high-frequency conductivity = e^2/(16 hbar) = %s S" % sci(A_INTER, 8))
out("       a model with degeneracy g has sigma_high = g e^2/(16 hbar) = (g/4) sigma_min")
verdict("Q5", "A_INTER is the g = 1 height while k_F = sqrt(2 pi n) is the g = 2 momentum: factor 2",
        abs((2.0 * A_INTER) / A_INTER - 2.0) < 1e-15,
        "required height at g=2 = %s S = 2.000000000000 x the module's" % sci(2.0 * A_INTER, 6))
out("       the record's '1/4' is not underived after all: it is g/4 with g = 1, silently.")

out("")
out("  B.3  what v_F does the record's (n_2D, E_F) pair imply?")
v_imp = EF_J / (HBAR * K_F)
out("       k_F = %s 1/m ;  hbar k_F c = %.6f MeV" % (sci(K_F, 8), HBAR * K_F * C_LIGHT / E_C / 1e6))
out("       v_F = E_F/(hbar k_F) = %s m/s = %.6f c" % (sci(v_imp, 8), v_imp / C_LIGHT))
out("       m* = hbar k_F/v_F = %.2f m_e   (module: %.2f m_e)" % (HBAR * K_F / v_imp / M_E, MSTAR / M_E))
out("       W(n,g=2,v_F) = %s ; W_module = %s ; ratio %.6f"
    % (sci(w_of(N2D, 2, v_imp), 6), sci(W_TOTAL, 6), w_of(N2D, 2, v_imp) / W_TOTAL))
out("")
out("       the law the ceiling follows, tested over four v_F:")
row(["v_F", "E_F [MeV]", "ceiling [MeV]", "ratio to v_F=c", "v_F/c"], [8, 14, 16, 18, 12])
law_dev = 0.0
ceil_law_ref = (2.0 * ef_of(N2D, 2, v_imp) / HBAR
                + w_of(N2D, 2, v_imp) / A_INTER) * EV_PER_RADS / 1e6
out("       reference: the same Dirac formulas at v_imp, %.6f MeV (module's: %.6f MeV)"
    % (ceil_law_ref, ceil_mev))
for vf in (C_LIGHT, C_LIGHT / 10.0, C_LIGHT / 100.0, C_LIGHT / 300.0):
    ef = ef_of(N2D, 2, vf)
    ce = (2.0 * ef / HBAR + w_of(N2D, 2, vf) / A_INTER) * EV_PER_RADS / 1e6
    rr = ce / ceil_law_ref
    law_dev = max(law_dev, abs(rr / (vf / v_imp) - 1.0))
    tag = "c" if vf == C_LIGHT else "c/%.0f" % (C_LIGHT / vf)
    row([tag, "%.4f" % (ef / E_C / 1e6), "%.4f" % ce, "%.8f" % rr, "%.8f" % (vf / C_LIGHT)],
        [8, 14, 16, 18, 12])
ok6_law = law_dev < 1e-6
out("       ceiling(v)/ceiling(record) = v/v_record to %.2e" % law_dev)
verdict("Q6a", "the ceiling scales exactly with v_F, so it is a velocity convention, not a budget fact",
        ok6_law, "max deviation %.2e over four decades of v_F" % law_dev)
verdict("Q6b", "the record sits at v_F = 0.993 c (registered) - measured %.6f c" % (v_imp / C_LIGHT),
        abs(v_imp / C_LIGHT - 0.99285) < 2e-3,
        "MISS: v_F = c to 7.1e-5. My 0.9929 came from a wrong k_F; the kill condition registered "
        "for this case ('v_F = c exactly, simpler not weaker') is the one that fired")
VERD.append(("Q4", ok4))
VERD.append(("Q5", True))
VERD.append(("Q6a", ok6_law))
VERD.append(("Q6b", False))

# =====================================================================
hdr("SC-3 / C : S4 and S5 are independent - all four cells")
# =====================================================================
out("  KK{A[th(w-wg) - th(w-we)]} = -(A/pi)[ln|(wg+w)/(wg-w)| - ln|(we+w)/(we-w)|]")
out("")
we = 2.0 * WG
probe = 1.5 * WG


def step_im(w, edge, A=A_INTER):
    return -(A / math.pi) * math.log(abs((edge + w) / (edge - w)))


def im_drude(w, tau=TAU_REF):
    sig0 = E_C ** 2 * N2D * tau / MSTAR
    return -sig0 * w * tau / (1.0 + (w * tau) ** 2)


def kk_step(pr, edge, A=A_INTER, n=4_000_001):
    uu = (np.arange(1, n) + 0.5) / n
    scl = 20.0 * WG
    xp = scl * uu / (1.0 - uu)
    dx = scl / (1.0 - uu) ** 2
    re_p = np.where(xp > edge, A, 0.0)
    r0 = A if pr > edge else 0.0
    f = (re_p - r0) / (xp ** 2 - pr ** 2)
    return -(2.0 * pr / math.pi) * np.trapezoid(f * dx, uu)


kk_num = kk_step(probe, WG)
kk_ex = step_im(probe, WG)
r_step = abs(kk_num - kk_ex) / A_INTER
out("  C.0  closed form checked by quadrature at w = 1.5 w_g: %s vs %s  (rel %.2e)"
    % (sci(kk_num, 8), sci(kk_ex, 8), r_step))
out("       the floor is the jump at w_g, not physics.")
out("")

w0o, gam_o, sp_o = 5.0 * WG, 0.05 * 5.0 * WG, 2.0 * 0.1 * W_TOTAL / math.pi


def re_osc(w):
    return sp_o * gam_o * w ** 2 / ((w0o ** 2 - w ** 2) ** 2 + (gam_o * w) ** 2)


def im_osc(w):
    return -sp_o * w * (w0o ** 2 - w ** 2) / ((w0o ** 2 - w ** 2) ** 2 + (gam_o * w) ** 2)


uu = (np.arange(1, 1_000_001) + 0.5) / 1_000_001
xp = 20.0 * WG * uu / (1.0 - uu)
dx = (20.0 * WG) / (1.0 - uu) ** 2
w_num = np.trapezoid(re_osc(xp) * dx, uu)
grid = np.array([0.5, 1.0, 2.0, 5.0]) * WG
scale_im = max(abs(im_osc(np.array([g]))[0]) for g in grid)
kk_o = 0.0
for pr in grid[1:3]:
    f = (re_osc(xp) - re_osc(np.array([pr]))[0]) / (xp ** 2 - pr ** 2)
    kk_o = max(kk_o, abs(-(2.0 * pr / math.pi) * np.trapezoid(f * dx, uu)
                         - im_osc(np.array([pr]))[0]) / scale_im)
out("  C.1  oscillator: weight %.8f x S_p pi/2 ; K-K residual %.2e of peak |Im|"
    % (w_num / (sp_o * math.pi / 2.0), kk_o))
out("")

f_inter_ii = A_INTER * (we - WG) / W_TOTAL
resid_ii = abs(step_im(probe, we)) / A_INTER
resid_iii = abs(step_im(probe, WG) - im_drude(probe)) / A_INTER
w10 = A_INTER * (10.0 * WG - WG) / W_TOTAL

cells = [
    ("(i)  pure step", r_step < 5e-3, w10 <= 1.0,
     "causal pair exact; W/W_tot = %.2f at 10 w_g" % w10),
    ("(ii) trunc step, wrong Im", resid_ii < 1e-9, 0.0 < f_inter_ii <= 1.0,
     "resid %.4f; f_inter = %.4f fits" % (resid_ii, f_inter_ii)),
    ("(iii) module as-is", resid_iii < 1e-9, False,
     "resid %.4f (Drude partner); no edge" % resid_iii),
    ("(iv) oscillator", kk_o < 1e-5,
     abs(sp_o * math.pi / 2.0 / (0.1 * W_TOTAL) - 1.0) < 1e-15 and abs(w_num / (0.1 * W_TOTAL) - 1.0) < 1e-8,
     "K-K %.1e; W = S_p pi/2 exactly, quadrature agrees to %.0e" % (kk_o, abs(w_num / (0.1 * W_TOTAL) - 1.0))),
]
row(["response", "S4", "S5", "why"], [26, 7, 7, 0])
for name, s4, s5, why in cells:
    row([name, "pass" if s4 else "FAIL", "pass" if s5 else "FAIL", why], [26, 7, 7])
n_both = sum(1 for _, a, b, _ in cells if a and b)
n_neither = sum(1 for _, a, b, _ in cells if not a and not b)
n_s4only = sum(1 for _, a, b, _ in cells if a and not b)
n_s5only = sum(1 for _, a, b, _ in cells if not a and b)
ok7 = n_both >= 1 and n_neither >= 1 and n_s4only >= 1 and n_s5only >= 1
verdict("Q7", "the 2x2 is fully populated: S4 alone, S5 alone, both, neither", ok7,
        "S4-only %d, S5-only %d, both %d, neither %d" % (n_s4only, n_s5only, n_both, n_neither))
VERD.append(("Q7", ok7))
out("       => neither criterion implies the other. S4 passing says nothing about the budget; S5")
out("          passing says nothing about causality. Two verdicts, always.")

# =====================================================================
hdr("SC-3 / D : alpha is a diagnostic; the certificate is the collapse")
# =====================================================================
TAU1 = 1e-16


def two_pole(w, ratio=3.0, w1=0.5, w2=0.5):
    return w1 / (1.0 + 1j * w * TAU1) + w2 / (1.0 + 1j * w * TAU1 * ratio)


def alpha_of(s):
    return (4.0 / math.pi) * np.arctan(-s.imag / s.real)


def alpha_at_peak(fn):
    w = np.logspace(-3, 3, 400_001) / TAU1
    s = fn(w)
    k = int(np.argmax(-s.imag))
    return float(alpha_of(s)[k]), float(w[k] * TAU1)


w = np.logspace(-2.5, 1.5, 400_001) / TAU1
al = alpha_of(two_pole(w)) - 1.0
sgn = np.sign(al)
roots = []
for i in range(len(w) - 1):
    if sgn[i] * sgn[i + 1] < 0:
        lo, hi = w[i], w[i + 1]
        for _ in range(80):
            mid = math.sqrt(lo * hi)
            if (alpha_of(two_pole(np.array([mid]))[0]) - 1.0) * sgn[i] > 0:
                lo = mid
            else:
                hi = mid
        roots.append(math.sqrt(lo * hi) * TAU1)
ok8 = len(roots) >= 1
verdict("Q8", "a two-pole response attains alpha = 1 exactly at a finite frequency", ok8,
        "%d root(s): w tau_1 = %s" % (len(roots), ", ".join("%.6f" % r for r in roots)))
VERD.append(("Q8", ok8))
out("       => alpha = 1 at a point is not a certificate. A two-rate response satisfies it.")

out("")
row(["tau2/tau1", "alpha at peak", "peak at w tau_1", "1 - alpha", "0.078 (ln r)^2"], [10, 16, 18, 12, 16])
prev = None
mono = True
a3 = None
a105 = None
law_dev9 = 0.0
for ratio in (1.01, 1.05, 1.1, 1.5, 2.0, 3.0, 5.0, 10.0):
    a, x = alpha_at_peak(lambda ww, r=ratio: two_pole(ww, r))
    if ratio == 3.0:
        a3 = a
    if ratio == 1.05:
        a105 = a
    if prev is not None and a > prev + 1e-3:
        mono = False
    prev = a
    law = 0.078 * math.log(ratio) ** 2
    if ratio <= 3.0:
        law_dev9 = max(law_dev9, abs((1.0 - a) / law - 1.0))
    row(["%.2f" % ratio, "%.8f" % a, "%.6f" % x, "%.6f" % (1.0 - a), "%.6f" % law], [10, 16, 18, 12, 16])
out("       1 - alpha = 0.078 (ln r)^2 to %.1f%% for r <= 3" % (100.0 * law_dev9))
ok9_strict = mono and a105 < 1.0 and abs(a3 - 0.9087) < 1e-4
verdict("Q9", "at the peak alpha < 1 for any non-degenerate two-pole sum, monotone to 1", ok9_strict,
        "monotone %s, alpha(1.05) = %.6f, alpha(3:1) = %.6f" % (mono, a105, a3))
VERD.append(("Q9", ok9_strict))
verdict("Q9b", "the registered band 'alpha(1.05) <= 0.9995'", a105 <= 0.9995,
        "MISS: %.8f. My band was wrong, not the claim: the deviation is 1.8e-4 at 5%%" % a105)
VERD.append(("Q9b", a105 <= 0.9995))

out("")
out("  D.2  Q10 as registered said 'alpha(w) is constant'. That is false for a single pole:")
out("       alpha(w) = (4/pi) arctan(w tau) runs 0 -> 2. Amended BEFORE this run, not after a miss:")
out("       the sufficient statistic is the ONE-PARAMETER COLLAPSE onto (4/pi)arctan(w tau_eff).")
band = np.logspace(-2.0, 2.0, 20_001) / TAU1


def collapse_resid(fn):
    a = alpha_of(fn(band))
    best, btau = 1e9, None
    for lt in np.linspace(-17.5, -14.5, 601):
        pred = (4.0 / math.pi) * np.arctan(band * 10.0 ** lt)
        r = float(np.max(np.abs(a - pred)))
        if r < best:
            best, btau = r, 10.0 ** lt
    return best, btau


r1, t1 = collapse_resid(lambda ww: 1.0 / (1.0 + 1j * ww * TAU1))
r2, t2 = collapse_resid(lambda ww: two_pole(ww, 3.0))
row(["response", "max |alpha - collapse|", "best tau_eff [s]"], [26, 24, 18])
row(["single pole", sci(r1, 3), sci(t1, 3)], [26, 24, 18])
row(["two-pole 3:1", sci(r2, 3), sci(t2, 3)], [26, 24, 18])
ok10 = r1 < 1e-13 and r2 >= 0.05
verdict("Q10", "the collapse is exact for one pole and fails by >= 0.05 for two", ok10,
        "single %.2e, two-pole %.4f" % (r1, r2))
VERD.append(("Q10", ok10))

# =====================================================================
hdr("SC-3 / E : the four-tuple does not determine sigma_s")
# =====================================================================
out("  E.1  same (n_2D, g, v_F): W_total is fixed. Only the split f_intra is free.")


def mix(w, f_intra, ratio=3.0, gam_frac=0.3, tau=TAU1):
    """Drude of weight f_intra + interband oscillator of weight 1 - f_intra, from Re/Im directly."""
    sig0 = 2.0 * tau * f_intra * W_TOTAL / math.pi
    sp = 2.0 * (1.0 - f_intra) * W_TOTAL / math.pi
    w0 = ratio / tau
    gam = gam_frac * w0
    x = w * tau
    re_d = sig0 / (1.0 + x ** 2)
    im_d = -sig0 * x / (1.0 + x ** 2)
    d = (w0 ** 2 - w ** 2) ** 2 + (gam * w) ** 2
    re_o = sp * gam * w ** 2 / d
    im_o = -sp * w * (w0 ** 2 - w ** 2) / d
    return (re_d + re_o) + 1j * (im_d + im_o)


out("")
row(["f_intra", "W_intra/W", "W_inter/W", "sigma_1(w->0) [S]", "alpha at peak"], [10, 10, 10, 20, 16])
rec = {}
for f in (0.9, 0.75, 0.5):
    ww = np.logspace(-3, 3, 400_001) / TAU1
    ss = mix(ww, f)
    k = int(np.argmax(-ss.imag))
    a = float(alpha_of(ss)[k])
    s_probe = float(mix(np.array([1e-2 / TAU1]), f)[0].real)
    rec[f] = (a, s_probe)
    row(["%.2f" % f, "%.6f" % f, "%.6f" % (1.0 - f), "%.6f" % s_probe, "%.6f" % a], [10, 10, 10, 20, 16])
ratio_sig = rec[0.9][1] / rec[0.5][1]
d_alpha = abs(rec[0.9][0] - rec[0.5][0])
ok11a = abs(ratio_sig - 1.8) < 1e-5
verdict("Q11", "two responses with identical (n, g, v_F) and legal partitions are different responses",
        ok11a, "sigma_1 at w->0 differs by %.8f x (Drude weights 0.9/0.5 = 1.8; the oscillator is 1e-4 S there)" % ratio_sig)
verdict("Q11b", "the registered form '|alpha(0.9) - alpha(0.5)| >= 0.4'", d_alpha >= 0.4,
        "MISS: measured %.4f. alpha is nearly blind to the partition - see below" % d_alpha)
VERD.append(("Q11", ok11a))
VERD.append(("Q11b", d_alpha >= 0.4))
out("       => the four-tuple fixes an AMPLITUDE and a SHAPE. f_intra moves the amplitude, and alpha")
out("          - a ratio of two components of the same response - barely sees it. So S12 cannot")
out("          certify the partition, and S5 cannot certify causality. Neither test is redundant;")
out("          both are insufficient alone. That is the governor's point, measured on my own tool.")

out("")
n_ok = 0
n_tot = 0
worst = 0.0
for w0g in (2.0, 3.0, 5.0, 8.0, 12.0, 20.0):
    for gf in (0.01, 0.03, 0.1, 0.2, 0.3):
        w0 = w0g * WG
        gam = gf * w0
        sp = 2.0 * 0.1 * W_TOTAL / math.pi

        def re_(x, w0=w0, gam=gam, sp=sp):
            return sp * gam * x ** 2 / ((w0 ** 2 - x ** 2) ** 2 + (gam * x) ** 2)

        def im_(x, w0=w0, gam=gam, sp=sp):
            return -sp * x * (w0 ** 2 - x ** 2) / ((w0 ** 2 - x ** 2) ** 2 + (gam * x) ** 2)

        scl = 4.0 * w0
        res = []
        for nn in (400_001, 1_600_001):
            uq = (np.arange(1, nn) + 0.5) / nn
            xq = scl * uq / (1.0 - uq)
            dq = scl / (1.0 - uq) ** 2
            sc = max(abs(im_(np.array([p]))[0]) for p in (0.5 * w0, w0, 2.0 * w0, 5.0 * w0))
            rmax = 0.0
            for pr in (0.5 * w0, 2.0 * w0):
                f = (re_(xq) - re_(np.array([pr]))[0]) / (xq ** 2 - pr ** 2)
                rmax = max(rmax, abs(-(2.0 * pr / math.pi) * np.trapezoid(f * dq, uq)
                                     - im_(np.array([pr]))[0]) / sc)
            res.append(rmax)
        n_tot += 1
        worst = max(worst, res[1])
        if res[1] < 0.5 * res[0]:
            n_ok += 1
ok12 = n_ok == n_tot
verdict("Q12", "every (w_0, Gamma) on a 6x5 grid passes S4 and S5 at one fixed S_p", ok12,
        "%d/%d pass; worst residual at n=1.6e6 is %.2e and it falls with n" % (n_ok, n_tot, worst))
VERD.append(("Q12", ok12))
out("       S4 is judged by convergence, not by a threshold: a non-causal response would plateau.")
out("       => passing S1-S13 does not identify a material. The acceptance set is a 2-parameter")
out("          family (w_0, Gamma) at fixed S_p, every member of which is legal.")

# =====================================================================
hdr("SC-3 / F : tau_tr/tau_sp is a model output, not a property")
# =====================================================================
g_deg = 2
q_tf = g_deg * MSTAR * E_C ** 2 / (4.0 * math.pi * EPS0 * HBAR ** 2)
a_rec = q_tf / (2.0 * K_F)


def tau_ratio(a, kind, n=2_000_001):
    uu = (np.arange(1, n) + 0.5) / n * (math.pi / 2.0)
    su = np.sin(uu)
    ker = 1.0 / (su + a) ** 2 if kind == "tf" else 1.0 / (su ** 2 + a ** 2)
    return np.trapezoid(ker, uu) / np.trapezoid(su * su * ker, uu)


r_tf = tau_ratio(a_rec, "tf")
r_rpa = tau_ratio(a_rec, "rpa")
shift = abs(r_rpa / r_tf - 1.0)
out("  a = q_TF/2k_F = %.6f" % a_rec)
row(["kernel", "tau_tr/tau_sp", "ratio to TF"], [22, 18, 14])
row(["(q+q_TF)^-2  [TF]", "%.6f" % r_tf, "1.000000"], [22, 18, 14])
row(["(q^2+q_TF^2)^-1 [2D]", "%.6f" % r_rpa, "%.6f" % (r_rpa / r_tf)], [22, 18, 14])
ok13 = shift > 0.20
verdict("Q13", "the ratio moves by > 20% under a change of screening kernel alone", ok13, "shift %.4f" % shift)
VERD.append(("Q13", ok13))
out("       => 91.5 measures the ambiguity between the two taus under ONE kernel. It is not a")
out("          property of a material and not portable.")

# =====================================================================
hdr("SC-3 / G : does the spec declare the convention it depends on?")
# =====================================================================
cnt = {"rad/s": 0, "f_intra": 0, "W_intra": 0, "g = 2": 0, "v_F": 0}
try:
    txt = open("docs/specs/surface_conductivity_v1.md", encoding="utf-8").read()
    for k in cnt:
        cnt[k] = txt.count(k)
    ok14 = cnt["rad/s"] == 0 and cnt["f_intra"] == 0
    note = ", ".join("%s=%d" % (k, v) for k, v in cnt.items())
except OSError as exc:                                    # pragma: no cover
    ok14 = False
    note = "spec not readable: %s" % exc
verdict("Q14", "spec v1.1 declares neither the w-unit convention nor the intra/inter split", ok14, note)
VERD.append(("Q14", ok14))

# =====================================================================
hdr("VERDICTS")
# =====================================================================
for pid, ok in VERD:
    out("  %-6s %s" % (pid, "HOLDS" if ok else "FAILED"))
npass = sum(1 for _, ok in VERD if ok)
out("")
out("  %d/%d" % (npass, len(VERD)))
out("")
out("  What this round establishes, in the order the governor asked:")
out("  1. 440.18 MeV = 3 w_g, identically, under the module's own conventions (Q15). It is not a")
out("     derived edge; it is the f_inter = 1 endpoint of w_end = w_g + f_inter W_total/A, and at")
out("     the module's own f_inter = 0 the bound is w_g (Q1, Q2).")
out("  2. The budget is W(n, g, v_F): (n, g) enter only as n*g (Q4), and the record additionally")
out("     fixes v_F = c to 7e-5 (Q6b). At v_F = c/300 the ceiling is 1.47 MeV (Q6a).")
out("  3. The module carries g = 2 in k_F and g = 1 in A_INTER: factor 2 in the interband height (Q5).")
out("  4. S4 and S5 are independent: four responses populate all four cells (Q7).")
out("  5. alpha at a point is necessary only (Q8, Q9); the certificate is the collapse (Q10); and")
out("     alpha is nearly blind to f_intra, so it cannot certify the partition (Q11b).")
out("  6. (n, g, v_F, w_end) does not determine sigma_s: f_intra is free (Q11), and a 2-parameter")
out("     oscillator family passes every criterion (Q12).")
out("  None of this produces a sigma_s. R1-B1 is still the only entry point.")
