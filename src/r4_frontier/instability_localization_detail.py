# -*- coding: utf-8 -*-
"""
R4 instability localization, stage 2 -- C6 (mode structure / constraint content) and
C7 (seeded amplification, the unconfounded version of C1).
=========================================================================================
Registration: runs/R4/r4_instability_localization_registration.md, section "Addendum"
(the C6/C7 criteria were written BEFORE this script was run; see disclosure A1/A2/A3).

Why this stage exists: the stage-1 metrics were defective.
  A1 the 2D checkerboard index cancels for one-directional alternation -> cannot certify "smooth".
  A2 C1's growth ratio divides by an initial truncation level that depends on the geometry
     -> the INNER-EDGE verdict was not licensed.
  A3 C4's factor-5 mismatch may mean the leading mode is a constraint-neutral GAUGE mode,
     which must be measured, not assumed.

Output: runs/R4/r4_instability_localization_stage2_results.txt
"""
import os
import sys
import math

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import axisym_2p1_evolution as ax
import instability_localization as s1

FIELDS = tuple(ax.FIELDS)
NF = len(FIELDS)
RHO_IN = ax.RHO_IN
R_DOM = 24.0
KO_PROD = ax.KO_EPS

# registered thresholds (addendum)
TH_GRIDSCALE = 0.50     # either-direction alternation
TH_EDGE_MASS = 0.50     # within 10% of an edge
TH_NEUTRAL = 0.01       # Ham content below 1% of the top-8 max
TH_C7_EDGE = 2.0        # amplification ratio => EDGE
TH_C7_BULK = 1.5        # all within 1.5x  => BULK


# ---------------------------------------------------------------- constraint content via FD
def constraint_content(v, x0, g, bc, eps=1e-6):
    """||Ham[v]|| / ||v|| and max-momentum content, linearised about the flat state."""
    n = g.N * g.N
    vv = np.asarray(v, dtype=float).reshape(NF, n)
    nv = math.sqrt(float((vv ** 2).sum())) or 1e-300

    res = []
    for sgn in (+1.0, -1.0):
        st = s1.vec_state(x0 + sgn * eps * v, g, bc)
        ax.symmetrise(st, g, bc)
        _, info = ax.rhs(st, g)
        mom = ax.momentum(st, g)
        ham = np.asarray(info["Ham"])[g.sl, g.sl].ravel()
        m0 = np.asarray(mom[0])[g.sl, g.sl].ravel()
        m2 = np.asarray(mom[2])[g.sl, g.sl].ravel()
        res.append((ham, m0, m2))
    ham_d = (res[0][0] - res[1][0]) / (2 * eps)
    m0_d = (res[0][1] - res[1][1]) / (2 * eps)
    m2_d = (res[0][2] - res[1][2]) / (2 * eps)
    ham_n = math.sqrt(float((ham_d ** 2).sum())) / nv
    mom_n = max(math.sqrt(float((m0_d ** 2).sum())), math.sqrt(float((m2_d ** 2).sum()))) / nv
    return ham_n, mom_n


def mode_structure(v, g):
    a = np.abs(np.asarray(v, dtype=float))
    n = g.N * g.N
    V2 = a.reshape(NF, g.N, g.N).sum(axis=0)
    tot = max(float(V2.sum()), 1e-300)
    m_rho = V2.sum(axis=1)
    m_z = V2.sum(axis=0)
    ir = np.arange(g.N)
    alt_rho = abs(float((((-1.0) ** ir) * m_rho).sum())) / max(float(m_rho.sum()), 1e-300)
    alt_z = abs(float((((-1.0) ** ir) * m_z).sum())) / max(float(m_z.sum()), 1e-300)
    rs = g.rho[g.sl]
    span = rs[-1] - rs[0] + g.h
    inner = rs < rs[0] + 0.10 * span
    outer = rs > rs[-1] - 0.10 * span
    edge_in = float(V2[inner, :].sum()) / tot
    edge_out = float(V2[outer, :].sum()) / tot
    peak = float(np.argmax(m_rho) + 0.5) / g.N
    mass = np.array([a[i * n:(i + 1) * n].sum() for i in range(NF)])
    mass = mass / max(float(mass.sum()), 1e-300)
    return dict(alt_rho=alt_rho, alt_z=alt_z, edge_in=edge_in, edge_out=edge_out,
                peak=peak, mass=mass)


def c6(res=(16, 20), ntop=8):
    print("[C6] mode structure + constraint content of the top-%d eigenmodes" % ntop)
    print("     criteria: grid-scale iff max(alt_rho,alt_z) > %.2f ; edge iff >=%.0f%% within 10%%"
          % (TH_GRIDSCALE, 100 * TH_EDGE_MASS))
    print("               constraint-neutral iff Ham content < %.0f%% of the top-%d max"
          % (100 * TH_NEUTRAL, ntop))
    out = []
    for N in res:
        g, st0, bc = s1.flat_setup(N, R_DOM, RHO_IN)
        x0 = s1.state_vec(st0, g)
        print("  --- N=%d  h=%.4f  n_dof=%d" % (N, g.h, x0.size))
        J = s1.jacobian(x0, g, bc, 1e-6, label="J(N=%d)" % N)
        w, V, meth = s1.spectrum(J, k=ntop)
        order = np.argsort(-w.real)[:ntop]
        rows = []
        for idx in order:
            v = np.real(V[:, idx])
            ms = mode_structure(v, g)
            ham_n, mom_n = constraint_content(v, x0, g, bc)
            rows.append(dict(re=float(w[idx].real), im=float(w[idx].imag), ham=ham_n,
                             mom=mom_n, **ms))
        ham_max = max(r["ham"] for r in rows) or 1e-300
        print("    %-3s %-9s %-8s %-8s %-8s %-8s %-8s %-9s %s"
              % ("#", "Re lam", "alt_rho", "alt_z", "edge_in", "edge_out", "peak", "Ham/|v|", "dominant"))
        for i, r in enumerate(rows):
            dom = FIELDS[int(np.argmax(r["mass"]))]
            print("    %-3d %+9.5f %8.3f %8.3f %8.2f %8.2f %8.3f %9.2e %s%s"
                  % (i, r["re"], r["alt_rho"], r["alt_z"], r["edge_in"], r["edge_out"],
                     r["peak"], r["ham"], dom,
                     "   <- CONSTRAINT-NEUTRAL" if r["ham"] < TH_NEUTRAL * ham_max else ""))
        carry = [r for r in rows if r["ham"] >= TH_NEUTRAL * ham_max]
        lead = rows[0]
        lc = max(carry, key=lambda r: r["re"]) if carry else None
        gridscale = max(lead["alt_rho"], lead["alt_z"]) > TH_GRIDSCALE
        edge = max(lead["edge_in"], lead["edge_out"]) >= TH_EDGE_MASS
        print("    leading mode: %s ; %s ; %s"
              % ("GRID-SCALE (max alt %.2f)" % max(lead["alt_rho"], lead["alt_z"])
                 if gridscale else "NOT grid-scale by either-direction metric (max alt %.2f)"
                 % max(lead["alt_rho"], lead["alt_z"]),
                 "EDGE-LOCALIZED" if edge else "delocalized (edge mass %.2f)" % max(lead["edge_in"], lead["edge_out"]),
                 "CONSTRAINT-NEUTRAL" if lead["ham"] < TH_NEUTRAL * ham_max else "constraint-carrying"))
        if lc:
            print("    largest CONSTRAINED mode: Re lam = %+.5f  (Ham/|v| = %.2e, dominant %s, alt max %.2f)"
                  % (lc["re"], lc["ham"], FIELDS[int(np.argmax(lc["mass"]))],
                     max(lc["alt_rho"], lc["alt_z"])))
        else:
            print("    no constraint-carrying mode among the top-%d" % ntop)
        out.append(dict(N=N, h=g.h, meth=meth, rows=rows, lead=lead, carry=lc))
    return out


# ---------------------------------------------------------------- C7: seeded amplification
SEED_COEF = dict(grr=1.0, grz=0.5, gzz=1.0, gpp=1.0, Krr=0.5, Krz=0.5, Kzz=0.5, Kpp=0.5,
                 alp=1.0, phi=0.5, Pi=0.5)


def seeded_state(g, st_ref):
    """Identical analytic perturbation in EVERY geometry: a Gaussian at (rho=12, z=0)."""
    R2 = (g.rho[:, None] - 12.0) ** 2 + g.z[None, :] ** 2
    shape = np.exp(-R2 / (2.0 * 2.0 ** 2))
    st = {k: v.copy() for k, v in st_ref.items()}
    for k in FIELDS:
        st[k] = st[k] + 1.0e-4 * SEED_COEF[k] * shape
    return st


def evolve_to(g, st0, bc, times, cfl=0.25):
    """Fixed external bc for both the seeded and the unseeded run -> delta has zero ghosts."""
    dt = cfl * g.h
    nst = max(1, int(round(max(times) / dt)))
    dt = max(times) / nst
    st = {k: v.copy() for k, v in st0.items()}
    ax.symmetrise(st, g, bc)
    snaps = {}
    t = 0.0
    k = 0
    order = sorted(times)
    for n in range(nst + 1):
        if k < len(order) and t >= order[k] - 1e-12:
            snaps[order[k]] = {kk: vv.copy() for kk, vv in st.items()}
            k += 1
        if n == nst:
            break
        st = ax.step(st, g, dt, bc)
        t += dt
    return snaps


def delta_norm(a, b, g):
    return math.sqrt(sum(float(((a[k][g.sl, g.sl] - b[k][g.sl, g.sl]) ** 2).sum()) for k in FIELDS))


def c7(times=(2.0, 4.0)):
    print("[C7] seeded amplification: the SAME analytic seed in every geometry, differenced")
    print("     against an unseeded control on the same grid (removes the truncation-amplitude")
    print("     confound A2). registered criterion is evaluated at t=%.0f ; t=%.0f is supplementary."
          % (times[0], times[1]))
    configs = [
        ("baseline  rho_in=4, R=24", 50, 24.0, 4.0),
        ("inner cut rho_in=8, R=24", 40, 24.0, 8.0),
        ("outer     rho_in=4, R=36", 80, 36.0, 4.0),
    ]
    ax.KO_EPS = KO_PROD
    amps = {}
    for nm, N, Rdom, rin in configs:
        g, st0, bc = s1.flat_setup(N, Rdom, rin)
        base = evolve_to(g, st0, bc, times)
        pert = evolve_to(g, seeded_state(g, st0), bc, times)
        d0 = None
        line = []
        for t in times:
            dn = delta_norm(pert[t], base[t], g)
            if d0 is None:
                d0n = delta_norm(seeded_state(g, st0), st0, g)
            line.append((t, dn, dn / max(d0n, 1e-300)))
        amps[nm] = dict(t=[x[0] for x in line], amp=[x[2] for x in line], N=N, h=g.h)
        print("  %-26s N=%3d h=%.2f  " % (nm, N, g.h)
              + "  ".join("A(t=%.0f)=%6.3f" % (x[0], x[2]) for x in line))
    ax.KO_EPS = KO_PROD
    names = [c[0] for c in configs]
    a = [amps[n]["amp"] for n in names]
    verdict = "INCONCLUSIVE"
    i = times.index(times[0])
    base = a[0][i]
    inner_ch = max(a[1][i] / base, base / max(a[1][i], 1e-300))
    outer_ch = max(a[2][i] / base, base / max(a[2][i], 1e-300))
    all_within = all(max(x[i] / base, base / max(x[i], 1e-300)) < TH_C7_BULK for x in a)
    if inner_ch > TH_C7_EDGE:
        verdict = "INNER-EDGE"
    elif outer_ch > TH_C7_EDGE:
        verdict = "OUTER-EDGE"
    elif all_within:
        verdict = "BULK"
    else:
        verdict = "MIXED/UNCLASSIFIED"
    print("    amplification ratios at t=%.0f: %s" % (times[0], ", ".join("%.3f" % (x[i] / base) for x in a)))
    print("    inner-cut change %.2f ; outer-domain change %.2f (edge threshold %.1f) -> %s"
          % (inner_ch, outer_ch, TH_C7_EDGE, verdict))
    print("    C7 verdict: %s" % verdict)
    return verdict, amps


def main():
    print("=" * 100)
    print("R4 instability localization, STAGE 2 -- C6 mode structure / constraint content, C7 seeded amplification")
    print("registration + addendum: runs/R4/r4_instability_localization_registration.md")
    print("stage-1 output: runs/R4/r4_instability_localization_results.txt")
    print("=" * 100)
    print("[parameters]")
    print("  operator imported from axisym_2p1_evolution ; RHO_IN=%.1f R_DOM=%.1f KO_PROD=%.1f"
          % (RHO_IN, R_DOM, KO_PROD))
    print("  thresholds: grid-scale alt > %.2f ; edge mass >= %.2f ; neutral < %.0f%% ; C7 edge %.1f bulk %.1f"
          % (TH_GRIDSCALE, TH_EDGE_MASS, 100 * TH_NEUTRAL, TH_C7_EDGE, TH_C7_BULK))
    print()

    recs = c6()
    print()
    v7, amps = c7()
    print()

    print("[verdicts stage 2]")
    for r in recs:
        lead = r["lead"]
        print("  N=%d leading mode: Re %+.5f ; alt_rho %.2f alt_z %.2f ; edge_in %.2f edge_out %.2f ; Ham %.2e ; dominant %s"
              % (r["N"], lead["re"], lead["alt_rho"], lead["alt_z"], lead["edge_in"],
                 lead["edge_out"], lead["ham"], FIELDS[int(np.argmax(lead["mass"]))]))
        if r["carry"]:
            print("         largest constrained mode: Re %+.5f (Ham %.2e, dominant %s)"
                  % (r["carry"]["re"], r["carry"]["ham"], FIELDS[int(np.argmax(r["carry"]["mass"]))]))
    print("  C7 geometry dependence: %s" % v7)
    print()
    print("[reading]")
    print("  If the leading mode is constraint-neutral, stage-1 C4's failure is EXPLAINED and")
    print("  not a contradiction: ||Ham|| grows at the rate of the largest CONSTRAINED mode,")
    print("  not of the largest mode overall. The consistency test must use the former.")
    print("  C7 is the unconfounded geometry test: if it says BULK, then the stage-1 INNER-EDGE")
    print("  verdict is retracted as an artefact of A2, and the boundary is exonerated.")
    print("  No verdict on B1/B3/B4/B6 changes here, and no physical-scale statement is made.")


if __name__ == "__main__":
    main()
