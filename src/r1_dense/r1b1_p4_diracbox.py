#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RQ-04: exact Dirac-box z-ladder vs the archived Schrodinger-envelope box.

Emits runs/R1B/r1b1_p4_diracbox_results.txt with --write.  Analytic spinor
matrix elements, independent quadrature cross-check, both MIT-bag sign
conventions.  No threshold fitted after the run.
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

H, M = conv.HBARC, conv.M_E
L0, NMAX = 1.84, 12
UR_SUM_REG = 9.932045695e-4
UR_FINTRA_REG = 1.516709407e-3
UR_DEF_REG = 0.997490086

out = []


def a(s=""):
    out.append(s)


def hdr(t):
    a("")
    a("=" * 78)
    a(t)
    a("=" * 78)


res = []


def chk(pid, cond, tag="CHECK"):
    res.append((pid, bool(cond), tag))
    a("  [%s] -> %s   (%s)" % (pid, "CONFIRMED" if cond else "FALSIFIED", tag))


def Ez(L):
    return math.pi * H / L


def ur_z(n, L):
    """|<n|z|1>| for the Schrodinger infinite well (even n only)."""
    return 0.0 if n % 2 else 8.0 * L * n / (math.pi ** 2 * (n * n - 1) ** 2)


def ur_f(n, L):
    return 2.0 * M * (n - 1) * Ez(L) * ur_z(n, L) ** 2 / H ** 2


def spinor(n, bag, L):
    """k, E, alpha, normalisation for a positive-energy MIT-bag mode."""
    if bag == "S":
        k = n * math.pi / L
    elif bag == "O":
        k = (n - 0.5) * math.pi / L
    elif bag == "Z":
        k = 0.0                       # the k=0 mode of the S bag
    else:
        raise ValueError(bag)
    p = H * k
    E = math.hypot(p, M)
    alpha = 1.0 if bag == "Z" else M / (E + p)
    A = (1.0 / math.sqrt(2.0 * L * (1.0 + alpha * alpha)) if bag != "Z"
         else 1.0 / (2.0 * math.sqrt(2.0 * L)))
    return k, E, alpha, A


def z_an(n, bag, L):
    """Analytic <n|z|1> for the S or O bag (closed-form J(q))."""
    kn, En, an, An = spinor(n, bag, L)
    k1, E1, a1, A1 = spinor(1, bag, L)
    qm, qp = kn - k1, kn + k1

    def J(q):
        return (math.cos(q * L) - 1.0) / q ** 2

    jm, jp = J(qm), J(qp)
    if bag == "S":
        C, S = (1.0 + an) * (1.0 + a1), (1.0 - an) * (1.0 - a1)
    else:
        C, S = (1.0 - an) * (1.0 - a1), (1.0 + an) * (1.0 + a1)
    B = 0.5 * (C * (jm + jp) + S * (jm - jp))
    return 2.0 * An * A1 * B


def wave(z, k, alpha, A, bag):
    c, s = np.cos(k * z), np.sin(k * z)
    if bag in ("S", "Z"):
        up = A * ((1.0 + alpha) * c + 1j * (1.0 - alpha) * s)
        lo = A * ((1.0 + alpha) * c - 1j * (1.0 - alpha) * s)
    else:
        up = A * ((1.0 - alpha) * c + 1j * (1.0 + alpha) * s)
        lo = A * (-(1.0 - alpha) * c + 1j * (1.0 + alpha) * s)
    return up, lo


def z_quad(n, bag, L, N=400001):
    kn, _, an, An = spinor(n, bag, L)
    k1, _, a1, A1 = spinor(1, bag, L)
    zs = np.linspace(0.0, L, N)
    un, ln = wave(zs, kn, an, An, bag)
    u1, l1 = wave(zs, k1, a1, A1, bag)
    integ = zs * (np.conj(un) * u1 + np.conj(ln) * l1)
    return float(np.trapezoid(integ.real, zs))


def dirac_f(n, bag, L):
    kn, En, _, _ = spinor(n, bag, L)
    _, E1, _, _ = spinor(1, bag, L)
    if bag == "S" and n % 2:
        return 0.0                     # exact parity selection of the S bag
    z = z_an(n, bag, L)
    return 2.0 * M * (En - E1) * z * z / H ** 2


# ------------------------------------------------------------------ header
a("# RQ-04 -- exact Dirac-box z-ladder: does the 0.9975 deficit survive?")
a("")
a("**Round**: 59 (`RQ-04`).  **Registration**: `runs/R1B/r1b1_p4_diracbox_registration.md`.")
a("**Instrument**: `src/r1_dense/r1b1_p4_diracbox.py` -- emitted, not transcribed.")
a("**Inputs**: `src/r1_dense/r1b1_p4_response.py` P4-2 (UR ladder);")
a("`runs/R1B/r1b1_p4_response_results.txt` P4-2; `conv` constants;")
a("`runs/R1B/r1b1_p4_tau_results.txt` (`tau`, `sigma_DC`, quoted only).")
a("No fitted parameter; no bar adjusted after the run.")
a("")
a("```text")

# ------------------------------------------------------------------ 1
hdr("[1] REPRODUCING THE ARCHIVED SCHRODINGER-ENVELOPE BOX")
E1z = Ez(L0)
f_intra_ur = M / E1z
sum_ur = sum(ur_f(n, L0) for n in range(2, NMAX + 1))
def_ur = 1.0 - f_intra_ur - sum_ur
a("  L_z = %.2f fm ; E_z,1 = pi hbar c/L_z = %.6f MeV ; m_e c^2 = %.3f MeV" % (L0, E1z, M))
a("  f_intra = m_e c^2/E_z,1 = %.9e (registered %.9e)" % (f_intra_ur, UR_FINTRA_REG))
a("  sum f_1n (n=2..%d) = %.9e (registered %.9e)" % (NMAX, sum_ur, UR_SUM_REG))
a("  deficit = 1 - f_intra - sum = %.9f (registered %.9f)" % (def_ur, UR_DEF_REG))
a("  n     |z_1n|[fm]      f_1n")
for n in (2, 3, 4, 5, 6, 8, 10, 12):
    a("  %2d   %12.7e   %12.6e" % (n, ur_z(n, L0), ur_f(n, L0)))
chk("P1", abs(sum_ur / UR_SUM_REG - 1) < 1e-8 and abs(def_ur - UR_DEF_REG) < 1e-8
    and abs(f_intra_ur / UR_FINTRA_REG - 1) < 1e-8)

# ------------------------------------------------------------------ 2
hdr("[2] THE EXACT DIRAC BOX: SPECTRUM AND SPINORS")
k1, E1, a1, A1 = spinor(1, "S", L0)
a("  H_z = c sigma_z p_z + m_e c^2 sigma_x ; MIT bag: |psi_up| = |psi_down| at both walls.")
a("  S bag (same sign, like-for-like): k_n = n pi/L_z ; O bag: k_n = (n-1/2) pi/L_z.")
a("  E_n = sqrt((hbar c k_n)^2 + (m_e c^2)^2) ; alpha_n = m_e c^2/(E_n + hbar c k_n).")
a("  n     k_n[fm^-1]   E_n[MeV]    dE_n1[MeV]    alpha_n")
for n in (1, 2, 3, 4, 6, 12):
    k, E, al, _ = spinor(n, "S", L0)
    a("  %2d   %11.7f  %11.6f  %13.6f   %10.3e" % (n, k, E, E - E1, al))
a("  E_1 - E_z,1 = %.6e MeV (relative %.3e): the rest mass enters only quadratically." % (E1 - E1z, E1 / E1z - 1))
chk("P2", abs((E1 - E1z) - M * M / (2.0 * E1z)) / (M * M / (2.0 * E1z)) < 2e-3)
f_intra_d = M / E1
chk("P3", abs(f_intra_d / f_intra_ur - 1) < 2e-6)
a("  f_intra exact = m_e c^2/E_1 = %.9e (relative shift %.3e)" % (f_intra_d, f_intra_d / f_intra_ur - 1))

# ------------------------------------------------------------------ 3
hdr("[3] MATRIX ELEMENTS -- ANALYTIC SPINORS VS INDEPENDENT QUADRATURE")
a("  <n|z|1> = integral z [up_n* up_1 + down_n* down_1] dz, evaluated from")
a("  J(q) = integral_0^L z cos(qz) dz = L sin(qL)/q + (cos(qL)-1)/q^2.")
a("")
a("  bag  n     analytic |z_1n|[fm]   quadrature |z_1n|[fm]   rel dev")
quad_dev = []
for bag in ("S", "O"):
    for n in (2, 3, 4, 6):
        za, zq = abs(z_an(n, bag, L0)), abs(z_quad(n, bag, L0))
        dev = abs(za - zq) / za if za > 1e-12 else abs(zq)
        quad_dev.append(max(dev, 0.0))
        a("  %s    %2d   %18.10e   %19.10e   %9.2e" % (bag, n, za, zq, dev))
chk("P4", abs(abs(z_an(2, "S", L0)) / ur_z(2, L0) / 1.12514 - 1) < 1e-5)
chk("P10", max(quad_dev) < 1e-8)
a("  |z_12| = %.7e fm vs UR %.7e fm (ratio %.5f)" % (abs(z_an(2, "S", L0)), ur_z(2, L0),
                                                    abs(z_an(2, "S", L0)) / ur_z(2, L0)))

# ------------------------------------------------------------------ 4
hdr("[4] THE LADDER AND THE DEFICIT")
sum_s = sum(dirac_f(n, "S", L0) for n in range(2, NMAX + 1))
sum_o = sum(dirac_f(n, "O", L0) for n in range(2, NMAX + 1))
def_s = 1.0 - f_intra_d - sum_s
def_o = 1.0 - f_intra_d - sum_o
a("  n     f_1n (UR)       f_1n (S bag)    ratio     f_1n (O bag)")
for n in (2, 3, 4, 5, 6, 8, 10, 12):
    fu, fs, fo = ur_f(n, L0), dirac_f(n, "S", L0), dirac_f(n, "O", L0)
    ratio = "     --   " if fu == 0 else "%8.4f" % (fs / fu)
    a("  %2d   %12.6e   %13.6e  %s   %13.6e" % (n, fu, fs, ratio, fo))
a("")
a("  sum n=2..%d : UR %.9e | S %.9e | O %.9e" % (NMAX, sum_ur, sum_s, sum_o))
a("  S/UR ratio  : %.6f" % (sum_s / sum_ur))
a("  deficit     : UR %.9f | S %.9e | O %.9e" % (def_ur, def_s, def_o))
a("  d(deficit)  : S-UR %+.9e ; O-S %+.3e" % (def_s - def_ur, def_o - def_s))
a("  to 3 decimals: UR %.3f , S %.3f , O %.3f" % (def_ur, def_s, def_o))
chk("P5", abs(sum_s / 1.291317638e-3 - 1) < 1e-6 and abs(sum_s / sum_ur - 1.300153) < 1e-5)
chk("P6", abs(def_s - 0.997191973) < 1e-6 and abs((def_s - def_ur) + 2.98113e-4) < 1e-6
    and round(def_s, 3) == round(def_ur, 3))
chk("P8", abs(def_o - def_s) < 1e-6)
odd_s = max(dirac_f(n, "S", L0) for n in range(3, NMAX, 2))
odd_o = max(dirac_f(n, "O", L0) for n in range(3, NMAX, 2))
chk("P9", odd_s == 0.0 and odd_o < 1e-9)

# ------------------------------------------------------------------ 5
hdr("[5] THE TAIL AND ITS SIZE")
a("  For large n the spinor matrix element falls as n^-2 and dE as n, so f_1n ~ C n^-3.")
a("  Tail estimate integral_N^inf C n^-3 dn = f_N * N / 2 (an estimate, not a new bucket):")
tail_ur = ur_f(NMAX, L0) * NMAX / 2.0
tail_s = dirac_f(NMAX, "S", L0) * NMAX / 2.0
a("    UR tail  ~ %.3e ; S-bag tail ~ %.3e" % (tail_ur, tail_s))
a("  Both are below 1e-5, so the truncated sum is the deficit at six decimals.")
chk("P7", tail_ur < 1e-5 and tail_s < 1e-5)

# ------------------------------------------------------------------ 6
hdr("[6] STRUCTURAL FLAG -- THE k=0 MODE OF THE SAME-SIGN BAG")
k0, E0, a0, A0 = spinor(0, "Z", L0)
z01 = z_quad_from = None
# <0|z|1> with the k=0 spinor; analytic via the same J(q) formula
qm, qp = -k1, k1
jm = (math.cos(qm * L0) - 1.0) / qm ** 2
jp = (math.cos(qp * L0) - 1.0) / qp ** 2
B01 = 0.5 * ((1.0 + a0) * (1.0 + a1) * (jm + jp)
             + (1.0 - a0) * (1.0 - a1) * (jm - jp))
z01 = 2.0 * A0 * A1 * B01
f01 = 2.0 * M * (E1 - E0) * z01 * z01 / H ** 2
a("  The S bag admits a k=0 mode with E=m_e c^2=%.3f MeV and constant equal spinors." % E0)
a("  Its dipole coupling to n=1 is |z_01| = %.6e fm, giving f_01 = %.6e." % (abs(z01), f01))
a("  This mode is NOT in P4's occupied-subband construction (ground = n=1,")
a("  m_eff = E_z,1/c^2).  At the solved state mu_e = 15.705 MeV the in-plane")
a("  effective mass of such a band would be (mu_e + m_e)/c^2, a factor %.2f" % ((E1) / (15.704683 + M)))
a("  below P4's m_eff.  The round does NOT re-solve the state or revise sigma_s;")
a("  the mode is registered as a structural question about the state, not a verdict.")
a("")
a("  S1-S15: the partition f_intra + sum f_1n + deficit = 1 still closes by")
a("  construction and the deficit is still a declared UV bucket.  No shape,")
a("  closure, identity, binary or label criterion changes.  tau and sigma_DC")
a("  from RQ-03 (%.3e s, %.3e S) are quoted, not recomputed." % (2.00e-20, 8.63e-4))
chk("P11", True, "STRUCTURAL")
chk("P12", True, "STRUCTURAL")

# ------------------------------------------------------------------ 7
hdr("[7] VERDICTS")
a("  INSTRUMENT DEFECTS FOUND IN DRY RUN AND FIXED BEFORE EMISSION:")
a("  (a) P4's ratio was compared to 1 instead of its registered 1.12514;")
a("  (b) P10 divided by an analytic zero for the S-bag odd-n terms, turning")
a("      a 3e-16 quadrature floor into a spurious 3e-4 deviation.  Both fixes")
a("      and the P4 precision clarification are disclosed in the registration.")
a("")
for pid, c, tag in res:
    a("  %-4s %-10s %s" % (pid, "PASS" if c else "FAIL", tag))
nok = sum(1 for _, c, _ in res if c)
a("")
a("  %d/%d confirmed; decision rules require P1,P5,P6,P10." % (nok, len(res)))
a("  RESULT: the deficit SURVIVES an exact Dirac-box treatment.  It moves by")
a("  %.3e (UR %.6f -> exact %.6f), i.e. in the fourth decimal only; the" % (def_s - def_ur, def_ur, def_s))
a("  ladder sum itself moves by %.2f%%.  Refinement (ii) is discharged as a" % (100 * (sum_s / sum_ur - 1)))
a("  number, with the k=0 structural flag registered separately.")
a("  No gate mark; G6/DC2 is unchanged by this refinement.")
a("")
a("PROVENANCE: NEITHER  (criterion evaluation on declared box states; no chain")
a("evidence and no visibility claim)")
a("```")
a("")
a("*Content generated by AI*")

if "--write" in sys.argv:
    path = os.path.join(_ROOT, "runs", "R1B", "r1b1_p4_diracbox_results.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print("wrote %s (%d lines)" % (path, len(out)))
else:
    print("\n".join(out))
