# -*- coding: utf-8 -*-
"""
R1-A2 moving-wall double benchmark: Pinney equation numerical solution + three registered analytic protocol values (v1.4 §2.7 / §8.2 R1-A2)
=============================================================================

Model (registered assumption checklist, evidence level capped at MODEL RESULT):
  Pinney (Ermakov-Pinney) equation  rho'' + w^2(t) rho = rho^{-3}.
  The Lewis-Riesenfeld invariant exists for arbitrary wall motion, but closed-form analytic excitation numbers hold only for three registered protocols
  (v1.4 §2.7 table): (i) free expansion a(t) ∝ t; (ii) sudden jump; (iii) periodic wall.
  Unregistered protocols must not be called "analytic validation" — this module performs the double benchmark only for the three protocols above.

Protocol (i) free expansion (c=1, a=t): the mode equation u'' + [k/a(t)^2] u = 0 is an Euler equation,
     with exact solution u = sqrt(t) t^{±i sigma}, sigma = sqrt(k^2 - 1/4) (k > 1/2 guarantees oscillation).
     Analytic excitation number N_k = 1/(e^{2 pi sigma} - 1).
     Normalization registration (task-spec note on "normalization and phase matching"): the initial mode is taken as the Fuchsian half-monodromy
     (half-monodromy continuation across t=0, equivalent to Euclidean connection) vacuum
         u_in(t) = sqrt(t) [ e^{+pi sigma/2} t^{-i sigma} + e^{-pi sigma/2} t^{+i sigma} ]
                   / sqrt(4 sigma sinh(pi sigma)),
     whose Bogoliubov coefficients in the power-law basis (alpha, beta) = e^{±pi sigma/2}/sqrt(2 sinh(pi sigma))
     satisfy |alpha|^2 - |beta|^2 = 1 and |beta|^2 = N_k exactly.
     Comparison diagnostic (printed, not counted in the verdict): if instead one uses instantaneous Minkowski vacuum normalization at time t0
     (u = 1/sqrt(2k), u' = -ik u), then beta^2 = [(k - sigma)^2 + 1/4]/(4 k sigma)
     — a power-law tail rather than exponential suppression, inconsistent with the thermal formula; this is the normalization sensitivity flagged in the spec note.
     Numerics: RK45 integration [t0=1, t_end=100], with the final state decomposed via Wronskian onto the power-law basis f_± = sqrt(t) t^{∓i sigma}
     /sqrt(2 sigma) (W(f_+, f_-) = -i, f_- is the positive-frequency branch) to extract beta^2.

Protocol (ii) sudden: a jumps instantly from a1=1 to a2=2; parameterized by the 1D infinite square-well ground state
     w_i = pi/a1 = pi, w_f = pi/a2 = pi/2; analytic beta^2 = (w_f - w_i)^2/(4 w_i w_f) = 1/8.
     Numerics: two-segment static integration (mode function and its derivative continuous across the jump), reusing the same benchmark as module 1 test T4.

Protocol (iii) periodic wall: w(t) = w0 (1 + eps cos(Omega t)), main resonance band center Omega = 2 w0.
     Perturbative analytic Floquet growth rate ln|u|/t = eps w0 / 2 (at the main resonance band center).
     Numerics: long-time integration (eps = 0.05, w0 = 1, T = 400), with a linear fit of
     ln|u| vs t over the final segment [300, 400]; relative deviation < 10%.

Pinney equation deliverables:
  - Closed-form Pinney solution for the Euler case w(t) = k^2/t^2: rho = sqrt(2)|u_in|
    (Ermakov theorem: when W(u_in*, u_in) = -i, rho = sqrt(2)|u| satisfies Pinney exactly,
     rho^2 = t [cosh(pi sigma) + cos(2 sigma ln t)]/(2 sigma sinh(pi sigma))).
    The numerical Pinney solution is compared with it; maximum relative deviation < 1e-3 (numerical check of the Wronskian theorem relation
    rho = sqrt(2)|u|).
  - Lewis invariant I = (1/2)[ |u/rho|^2 + |rho u' - u rho'|^2 ] = 1/2,
    used as an anchor for numerical correctness (tolerance 1e-6), checked in both the Euler case and the constant-w case.
  - The Wronskian W(u1, u2) = 1 of the fundamental real solution pair is conserved (tolerance 1e-6);
    Euler pair: u1 = sqrt(t) cos(sigma ln t)/sqrt(sigma), u2 = sqrt(t) sin(sigma ln t)/sqrt(sigma).
  - Constant-w anchor (spec-registered initial data): w0 = 1.3, rho(0) = 1/sqrt(w0), rho'(0) = 0
    gives the exact solution rho = 1/sqrt(w0) (constant), which the numerics preserve.

Zero file I/O: all results printed to stdout (pure ASCII; Chinese only in comments).
Run: cd D:/Docs/DCC && python -I src/r1_bounded/pinney_double.py > runs/R1A/r1a2_pinney_results.txt
"""
import sys

sys.stdout.reconfigure(encoding="utf-8")

import math

import numpy as np
from scipy.integrate import solve_ivp

# --------------------------------------------------------------------------
# Registered parameters (registered before run)
# --------------------------------------------------------------------------
RTOL = 1e-10                    # solver settings registered in the spec
ATOL = 1e-12
METHOD = "RK45"

# Protocol (i) free expansion
K_LIST = (0.6, 1.0, 1.5, 2.5)
T0_I = 1.0
TEND_I = 100.0

# Protocol (ii) sudden
A1 = 1.0
A2 = 2.0
T_JMP = 1.0
T_END_II = 2.0

# Protocol (iii) periodic wall
W0_III = 1.0
EPS_III = 0.05
T_III = 400.0
FIT_LO = 300.0
FIT_N = 1001

# Pinney Euler case
K_PIN = 1.0
T0_PIN = 1.0
TEND_PIN = 10.0
N_SAMPLE = 181

# Constant-w anchor
W_CONST = 1.3
TEND_CONST = 10.0

# --------------------------------------------------------------------------
# Registered thresholds (registered before run)
# --------------------------------------------------------------------------
TH_PROTO_I = 1e-3               # Protocol (i): max_k |beta^2_num - N_k|
TH_PROTO_II = 1e-3              # Protocol (ii): |beta^2_num - 1/8|
TH_PROTO_III = 0.10             # Protocol (iii): |rate - eps w0/2| / (eps w0/2)
TH_PINNEY = 1e-3                # Maximum relative deviation of Pinney numerics vs closed form (Euler case)
TH_LEWIS = 1e-6                 # Lewis invariant |I - 1/2|
TH_WPAIR = 1e-6                 # Fundamental solution pair |W - 1|

# --------------------------------------------------------------------------
# Exact structure of the Euler equation (protocol (i))
# --------------------------------------------------------------------------
def sigma_of(k):
    return math.sqrt(k * k - 0.25)


def power_branches(t, sig):
    """Exact positive/negative-frequency power-law branches f_∓ = sqrt(t) t^{∓ i sigma}/sqrt(2 sigma) and their derivatives."""
    s = math.sqrt(t)
    th = sig * math.log(t)
    c, sn = math.cos(th), math.sin(th)
    nrm = math.sqrt(2.0 * sig)
    fm = s * (c - 1j * sn) / nrm
    fp = s * (c + 1j * sn) / nrm
    fm_d = fm * (1.0 / (2.0 * t) - 1j * sig / t)
    fp_d = fp * (1.0 / (2.0 * t) + 1j * sig / t)
    return fm, fm_d, fp, fp_d


def u_in_exact(t, sig):
    """Fuchsian half-monodromy vacuum mode (closed form) and its derivative.

    u_in = sqrt(t) [ e^{+pi sigma/2} t^{-i sigma} + e^{-pi sigma/2} t^{+i sigma} ]
           / sqrt(4 sigma sinh(pi sigma)).
    """
    cn = 1.0 / math.sqrt(4.0 * sig * math.sinh(math.pi * sig))
    ap = cn * math.exp(0.5 * math.pi * sig)
    bm = cn * math.exp(-0.5 * math.pi * sig)
    th = sig * math.log(t)
    ep = ap * complex(math.cos(th), -math.sin(th))   # ap * t^{-i sigma}
    em = bm * complex(math.cos(th), math.sin(th))    # bm * t^{+i sigma}
    s = math.sqrt(t)
    u = s * (ep + em)
    ud = (ep * (1.0 - 2j * sig) + em * (1.0 + 2j * sig)) / (2.0 * s)
    return u, ud


def rho_of_u(t, sig):
    """Closed-form Pinney solution rho = sqrt(2)|u_in| and rho' (Ermakov theorem)."""
    u, ud = u_in_exact(t, sig)
    rho = math.sqrt(2.0) * abs(u)
    drho = math.sqrt(2.0) * (ud * np.conj(u)).real / abs(u)
    return rho, drho


def bogoliubov_pl(u, ud, t, sig):
    """Wronskian decomposition onto the power-law basis {f_-, f_+}, returning (beta^2, |alpha|^2 - |beta|^2).

    w(x, y) = x y' - x' y (bilinear, conserved along solutions); alpha = w(u, f_+)/i,
    beta = -w(u, f_-)/i; f_± are unit-KG-normalized (W(f_±*, f_±) = -i).
    """
    fm, fmd, fp, fpd = power_branches(t, sig)
    alpha = (u * fpd - ud * fp) / 1j
    beta = -(u * fmd - ud * fm) / 1j
    return abs(beta) ** 2, abs(alpha) ** 2 - abs(beta) ** 2


def u1_u2_exact(t, sig):
    """Fundamental real solution pair normalized to W = 1: u1 = sqrt(t) cos(sig ln t)/sqrt(sig),
    u2 = sqrt(t) sin(sig ln t)/sqrt(sig)."""
    s = math.sqrt(t)
    th = sig * math.log(t)
    c, sn = math.cos(th), math.sin(th)
    r = 1.0 / math.sqrt(sig)
    u1 = s * c * r
    u2 = s * sn * r
    u1d = (c / (2.0 * s) - sig * sn / s) * r
    u2d = (sn / (2.0 * s) + sig * c / s) * r
    return u1, u1d, u2, u2d

# --------------------------------------------------------------------------
# Protocol (i): free expansion a(t) ∝ t
# --------------------------------------------------------------------------
def proto1():
    rows = []
    for k in K_LIST:
        sig = sigma_of(k)
        nk = 1.0 / math.expm1(2.0 * math.pi * sig)
        u0, ud0 = u_in_exact(T0_I, sig)
        sol = solve_ivp(lambda t, y, k=k: [y[1], -(k * k / (t * t)) * y[0]],
                        (T0_I, TEND_I), [u0, ud0],
                        rtol=RTOL, atol=ATOL, method=METHOD)
        if not sol.success:
            raise RuntimeError("proto1 integration failed: " + str(sol.message))
        u, ud = complex(sol.y[0][-1]), complex(sol.y[1][-1])
        b2, kg = bogoliubov_pl(u, ud, TEND_I, sig)
        # Comparison diagnostic: instantaneous Minkowski vacuum initial data (different normalization -> power-law tail)
        um0 = 1.0 / math.sqrt(2.0 * k)
        umd0 = -1j * k * um0
        solm = solve_ivp(lambda t, y, k=k: [y[1], -(k * k / (t * t)) * y[0]],
                         (T0_I, TEND_I), [um0, umd0],
                         rtol=RTOL, atol=ATOL, method=METHOD)
        b2m, kgm = bogoliubov_pl(complex(solm.y[0][-1]), complex(solm.y[1][-1]),
                                 TEND_I, sig)
        b2m_cf = ((k - sig) ** 2 + 0.25) / (4.0 * k * sig)
        rows.append((k, sig, nk, b2, abs(b2 - nk), kg - 1.0, b2m, b2m_cf, kgm - 1.0))
    return rows

# --------------------------------------------------------------------------
# Protocol (ii): sudden (a1=1 -> a2=2, 1D box ground state)
# --------------------------------------------------------------------------
def proto2():
    w_i = math.pi / A1
    w_f = math.pi / A2
    u0 = 1.0 / math.sqrt(2.0 * w_i)
    ud0 = -1j * w_i / math.sqrt(2.0 * w_i)
    s1 = solve_ivp(lambda t, y: [y[1], -(w_i * w_i) * y[0]], (0.0, T_JMP),
                   [u0, ud0], rtol=RTOL, atol=ATOL, method=METHOD)
    s2 = solve_ivp(lambda t, y: [y[1], -(w_f * w_f) * y[0]], (T_JMP, T_END_II),
                   [s1.y[0][-1], s1.y[1][-1]], rtol=RTOL, atol=ATOL, method=METHOD)
    u, ud = complex(s2.y[0][-1]), complex(s2.y[1][-1])
    b2 = 0.5 * w_f * abs(u) ** 2 + abs(ud) ** 2 / (2.0 * w_f) - 0.5
    ana = (w_f - w_i) ** 2 / (4.0 * w_i * w_f)
    return w_i, w_f, b2, ana, abs(b2 - ana)

# --------------------------------------------------------------------------
# Protocol (iii): periodic-wall parametric resonance (Omega = 2 w0, main resonance band center)
# --------------------------------------------------------------------------
def proto3():
    w0, eps = W0_III, EPS_III
    om2 = lambda t: (w0 * (1.0 + eps * math.cos(2.0 * w0 * t))) ** 2
    u0 = 1.0 / math.sqrt(2.0 * w0)
    ud0 = -1j * w0 * u0
    te = np.linspace(FIT_LO, T_III, FIT_N)
    sol = solve_ivp(lambda t, y: [y[1], -om2(t) * y[0]], (0.0, T_III), [u0, ud0],
                    t_eval=te, rtol=RTOL, atol=ATOL, method=METHOD)
    if not sol.success:
        raise RuntimeError("proto3 integration failed: " + str(sol.message))
    lnu = np.log(np.abs(sol.y[0] + 1j * sol.y[1]))
    rate_amp = float(np.polyfit(te, lnu, 1)[0])    # ln|u|/t: Floquet amplitude growth rate
    rate_sq = 2.0 * rate_amp                        # ln|u|^2/t (printed for comparison)
    ana = eps * w0 / 2.0
    rel = abs(rate_amp - ana) / ana
    return rate_amp, rate_sq, ana, rel

# --------------------------------------------------------------------------
# Pinney Euler case: 10-dimensional coupled system (mode u_in, fundamental pair u1/u2, Pinney rho)
# --------------------------------------------------------------------------
def pinney_euler():
    k = K_PIN
    sig = sigma_of(k)
    t0, t1 = T0_PIN, TEND_PIN
    om2 = lambda t: (k * k / (t * t))
    u0, ud0 = u_in_exact(t0, sig)
    u1_0, v1_0, u2_0, v2_0 = u1_u2_exact(t0, sig)
    r0, dr0 = rho_of_u(t0, sig)

    def rhs(t, y):
        o2 = om2(t)
        u_re, u_im, v_re, v_im, u1, v1, u2, v2, rho, vrho = y
        return [v_re, v_im,
                -o2 * u_re, -o2 * u_im,
                v1, -o2 * u1,
                v2, -o2 * u2,
                vrho, rho ** -3 - o2 * rho]

    y0 = [u0.real, u0.imag, ud0.real, ud0.imag,
          u1_0, v1_0, u2_0, v2_0, r0, dr0]
    te = np.linspace(t0, t1, N_SAMPLE)
    sol = solve_ivp(rhs, (t0, t1), y0, t_eval=te, rtol=RTOL, atol=ATOL,
                    method=METHOD)
    if not sol.success:
        raise RuntimeError("pinney_euler integration failed: " + str(sol.message))
    Y = sol.y
    dev_rho = 0.0
    dev_I = 0.0
    dev_W = 0.0
    for i in range(Y.shape[1]):
        t = te[i]
        u_re, u_im, v_re, v_im, u1, v1, u2, v2, rho, vrho = Y[:, i]
        u = u_re + 1j * u_im
        ud = v_re + 1j * v_im
        rc, _ = rho_of_u(t, sig)
        dev_rho = max(dev_rho, abs(rho - rc) / rc)
        inv = 0.5 * (abs(u) ** 2 / rho ** 2
                     + abs(rho * ud - u * vrho) ** 2)
        dev_I = max(dev_I, abs(inv - 0.5))
        wr = u1 * v2 - v1 * u2
        dev_W = max(dev_W, abs(wr - 1.0))
    return dev_rho, dev_I, dev_W, sig, r0

# --------------------------------------------------------------------------
# Constant-w anchor (spec-registered initial data rho(0)=1/sqrt(w0), rho'(0)=0)
# --------------------------------------------------------------------------
def pinney_const():
    w = W_CONST
    t1 = TEND_CONST
    u0 = 1.0 / math.sqrt(2.0 * w)
    ud0 = -1j * w * u0
    y0 = [u0.real, u0.imag, ud0.real, ud0.imag,
          1.0, 0.0,          # u1 = cos(w t)
          0.0, 1.0,          # u2 = sin(w t)/w
          1.0 / math.sqrt(w), 0.0]

    def rhs(t, y):
        u_re, u_im, v_re, v_im, u1, v1, u2, v2, rho, vrho = y
        o2 = w * w
        return [v_re, v_im,
                -o2 * u_re, -o2 * u_im,
                v1, -o2 * u1,
                v2, -o2 * u2,
                vrho, rho ** -3 - o2 * rho]

    te = np.linspace(0.0, t1, N_SAMPLE)
    sol = solve_ivp(rhs, (0.0, t1), y0, t_eval=te, rtol=RTOL, atol=ATOL,
                    method=METHOD)
    if not sol.success:
        raise RuntimeError("pinney_const integration failed: " + str(sol.message))
    Y = sol.y
    dev_rho = 0.0
    dev_I = 0.0
    dev_W = 0.0
    for i in range(Y.shape[1]):
        t = te[i]
        u_re, u_im, v_re, v_im, u1, v1, u2, v2, rho, vrho = Y[:, i]
        u = u_re + 1j * u_im
        ud = v_re + 1j * v_im
        dev_rho = max(dev_rho, abs(rho - 1.0 / math.sqrt(w)) / (1.0 / math.sqrt(w)))
        inv = 0.5 * (abs(u) ** 2 / rho ** 2 + abs(rho * ud - u * vrho) ** 2)
        dev_I = max(dev_I, abs(inv - 0.5))
        dev_W = max(dev_W, abs(u1 * v2 - v1 * u2 - 1.0))
    return dev_rho, dev_I, dev_W

# --------------------------------------------------------------------------
# Main flow
# --------------------------------------------------------------------------
def main():
    bar = "=" * 74
    print(bar)
    print("R1-A2 moving-wall double benchmark: Pinney numerical + registered analytic protocols")
    print("spec: roadmap v1.4 sec 2.7 / sec 8.2 row R1-A2")
    print(bar)
    print("[parameters] (registered before run)")
    print("  Pinney equation        : rho'' + w^2(t) rho = rho^{-3}")
    print("  protocol (i)           : a(t) = t (c=1), u'' + (k/t)^2 u = 0 (Euler)")
    print("                           exact branches sqrt(t) t^{+-i sigma}, sigma=sqrt(k^2-1/4)")
    print("                           analytic N_k = 1/(e^{2 pi sigma} - 1)")
    print("                           k list: %s ; t0=%.1f, t_end=%.1f"
          % (K_LIST, T0_I, TEND_I))
    print("  protocol (ii)          : sudden a1=%.1f -> a2=%.1f, w_i=pi/a1, w_f=pi/a2" % (A1, A2))
    print("  protocol (iii)         : w(t)=w0(1+eps cos(Omega t)), Omega=2 w0 (band center)")
    print("                           w0=%.2f, eps=%.2f, T=%.0f, fit window [%.0f,%.0f]"
          % (W0_III, EPS_III, T_III, FIT_LO, T_III))
    print("  Pinney Euler case      : w(t)=k^2/t^2 with k=%.1f, t in [%.1f,%.1f]"
          % (K_PIN, T0_PIN, TEND_PIN))
    print("  constant-w anchor      : w0=%.2f, rho(0)=1/sqrt(w0), rho'(0)=0, T=%.0f"
          % (W_CONST, TEND_CONST))
    print("  solver                 : scipy solve_ivp, method=%s, rtol=%.1e, atol=%.1e"
          % (METHOD, RTOL, ATOL))
    print("[thresholds] (registered before run)")
    print("  protocol (i)  max_k |beta^2_num - N_k|        < %.1e" % TH_PROTO_I)
    print("  protocol (ii) |beta^2_num - (w_f-w_i)^2/4w_iw_f| < %.1e" % TH_PROTO_II)
    print("  protocol (iii) |rate - eps*w0/2| / (eps*w0/2) < %.2f" % TH_PROTO_III)
    print("  Pinney Euler  max rel dev vs closed form      < %.1e" % TH_PINNEY)
    print("  Lewis invariant max |I - 1/2|                 < %.1e" % TH_LEWIS)
    print("  Wronskian pair  max |W - 1|                   < %.1e" % TH_WPAIR)
    print()

    # ---- Protocol (i) ----
    rows1 = proto1()
    print("[protocol (i)] free expansion a(t) = t (registered protocol, v1.4 sec 2.7)")
    print("  initial mode: Fuchsian half-monodromy vacuum u_in (registered normalization)")
    print("  u_in = sqrt(t)[e^{+pi s/2} t^{-i s} + e^{-pi s/2} t^{+i s}]/sqrt(4 s sinh(pi s))")
    print("  extraction: Wronskian decomposition onto exact branches f_+- at t_end")
    print("  %-6s %-8s %-13s %-13s %-11s %-10s" % ("k", "sigma", "N_k analytic", "beta^2 num", "|dev|", "KG-1"))
    worst1 = 0.0
    for (k, sig, nk, b2, dv, kgd, b2m, b2mcf, kgmd) in rows1:
        worst1 = max(worst1, dv)
        print("  %-6.2f %-8.4f %-13.6e %-13.6e %-11.3e %-10.2e"
              % (k, sig, nk, b2, dv, kgd))
    ok1 = worst1 < TH_PROTO_I
    print("  max_k |beta^2_num - N_k| = %.3e  <  %.1e" % (worst1, TH_PROTO_I))
    print("  diagnostic (not a verdict): instantaneous-Minkowski-vacuum normalization")
    print("  %-6s %-14s %-14s %-11s" % ("k", "beta^2_MW num", "beta^2_MW closed", "|diff|"))
    for (k, sig, nk, b2, dv, kgd, b2m, b2mcf, kgmd) in rows1:
        print("  %-6.2f %-14.8f %-14.8f %-11.3e" % (k, b2m, b2mcf, abs(b2m - b2mcf)))
    print("  -> MW normalization gives power-law tail [(k-sigma)^2+1/4]/(4 k sigma),")
    print("     NOT the registered thermal N_k: this is the normalization/phase-matching")
    print("     subtlety flagged in the task spec; the Fuchsian vacuum is the registered one.")
    print("  protocol (i) verdict: %s" % ("PASS" if ok1 else "FAIL"))
    print()

    # ---- Protocol (ii) ----
    w_i, w_f, b2_2, ana2, dev2 = proto2()
    print("[protocol (ii)] sudden jump a1=%.1f -> a2=%.1f (1D box ground state)"
          % (A1, A2))
    print("  w_i = pi/a1 = %.6f ; w_f = pi/a2 = %.6f" % (w_i, w_f))
    print("  analytic beta^2 = (w_f-w_i)^2/(4 w_i w_f) = %.8f" % ana2)
    print("  numeric  beta^2 (two-segment integration) = %.8f" % b2_2)
    print("  |numeric - analytic| = %.3e  <  %.1e" % (dev2, TH_PROTO_II))
    ok2 = dev2 < TH_PROTO_II
    print("  protocol (ii) verdict: %s" % ("PASS" if ok2 else "FAIL"))
    print("  (same benchmark as module R1-A1 test T4: sudden-limit cross-check)")
    print()

    # ---- Protocol (iii) ----
    rate_a, rate_sq, ana3, rel3 = proto3()
    print("[protocol (iii)] periodic wall, main parametric resonance band center")
    print("  w(t) = %.2f (1 + %.2f cos(2*%.2f t)) ; long integration T = %.0f"
          % (W0_III, EPS_III, W0_III, T_III))
    print("  fitted Floquet rate ln|u|/t      = %.6f" % rate_a)
    print("  perturbative analytic eps*w0/2   = %.6f" % ana3)
    print("  (cross-check ln|u|^2/t = %.6f)" % rate_sq)
    print("  relative deviation = %.3e  <  %.2f" % (rel3, TH_PROTO_III))
    ok3 = rel3 < TH_PROTO_III
    print("  protocol (iii) verdict: %s" % ("PASS" if ok3 else "FAIL"))
    print()

    # ---- Pinney Euler case ----
    dev_r, dev_I_e, dev_W_e, sig_e, r0_e = pinney_euler()
    print("[Pinney] Euler case w(t) = k^2/t^2 (k = %.1f, sigma = %.6f)" % (K_PIN, sig_e))
    print("  closed form rho = sqrt(2)|u_in| = sqrt(t [cosh(pi s)+cos(2 s ln t)]/(2 s sinh(pi s)))")
    print("  initial rho(t0) = %.6f (order 1/sqrt(w0) with w0 = k = %.1f)" % (r0_e, K_PIN))
    print("  max_t |rho_num - rho_closed|/rho_closed = %.3e  <  %.1e"
          % (dev_r, TH_PINNEY))
    print("  Lewis invariant I = (1/2)[|u/rho|^2 + |rho u' - u rho'|^2], anchor I = 1/2:")
    print("  max_t |I - 1/2| (Euler case)            = %.3e  <  %.1e"
          % (dev_I_e, TH_LEWIS))
    print("  Wronskian pair W(u1,u2), anchor W = 1:")
    print("  max_t |W - 1| (Euler case)              = %.3e  <  %.1e"
          % (dev_W_e, TH_WPAIR))
    ok4 = dev_r < TH_PINNEY
    ok5a = dev_I_e < TH_LEWIS
    ok6a = dev_W_e < TH_WPAIR
    print()

    # ---- Constant-w anchor ----
    dev_rc, dev_I_c, dev_W_c = pinney_const()
    print("[Pinney] constant-w anchor: w0 = %.2f, rho(0)=1/sqrt(w0), rho'(0)=0" % W_CONST)
    print("  exact solution rho = 1/sqrt(w0) = %.6f (constant)" % (1.0 / math.sqrt(W_CONST)))
    print("  max_t |rho_num - 1/sqrt(w0)|/(1/sqrt(w0)) = %.3e" % dev_rc)
    print("  max_t |I - 1/2| (constant case)           = %.3e" % dev_I_c)
    print("  max_t |W - 1| (constant case)             = %.3e" % dev_W_c)
    ok5b = dev_I_c < TH_LEWIS
    ok6b = dev_W_c < TH_WPAIR
    print()

    # ---- verdicts ----
    ok5 = ok5a and ok5b
    ok6 = ok6a and ok6b
    print("[verdicts]")
    print("  V1 protocol (i) free expansion  max|beta^2_num - N_k| = %.3e : %s"
          % (worst1, "PASS" if ok1 else "FAIL"))
    print("  V2 protocol (ii) sudden         |beta^2_num - 1/8|    = %.3e : %s"
          % (dev2, "PASS" if ok2 else "FAIL"))
    print("  V3 protocol (iii) periodic wall rel dev vs eps*w0/2   = %.3e : %s"
          % (rel3, "PASS" if ok3 else "FAIL"))
    print("  V4 Pinney Euler vs closed form  max rel dev           = %.3e : %s"
          % (dev_r, "PASS" if ok4 else "FAIL"))
    print("  V5 Lewis invariant I=1/2        max |I-1/2| both cases= %.3e : %s"
          % (max(dev_I_e, dev_I_c), "PASS" if ok5 else "FAIL"))
    print("  V6 Wronskian pair W=1           max |W-1| both cases  = %.3e : %s"
          % (max(dev_W_e, dev_W_c), "PASS" if ok6 else "FAIL"))
    allok = ok1 and ok2 and ok3 and ok4 and ok5 and ok6
    print("R1-A2 OVERALL: %s" % ("PASS" if allok else "FAIL"))
    print("evidence level: MODEL RESULT (Pinney numerical solution + registered")
    print("                analytic protocols i/ii/iii per v1.4 sec 2.7; unregistered")
    print("                wall motions are not claimed as analytic validation)")


if __name__ == "__main__":
    main()
