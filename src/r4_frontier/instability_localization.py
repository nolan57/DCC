# -*- coding: utf-8 -*-
"""
R4 instability localization -- is the grid-scale mode BULK or EDGE?
=====================================================================
Registration (thresholds fixed before the run):
    runs/R4/r4_instability_localization_registration.md

Question: the 2+1 ADM free evolution is unstable at the grid scale. Is that mode
  (A) BULK  -- weak hyperbolicity => BSSN/Z4c is genuinely required, or
  (B) EDGE  -- produced by the RHO_IN excise surface / frozen Dirichlet edge => a BC bug?

The production operator is imported, never re-implemented: geometry (Christoffel, Ricci,
D_iD_j alpha, D^2 phi), parity fill and boundary treatment all come from
axisym_2p1_evolution. This module only adds (i) a state-vector wrapper, (ii) a finite-difference
Jacobian of the semi-discrete operator, and (iii) the geometry-dependence scan.

Order of execution matters: C3 validates the Jacobian assembly FIRST; if C3 fails, the
spectra (C2/C4/C5) are void and are not interpreted.

Disclosure: C2/C4/C5 build the Jacobian of the UNDISSIPATED operator (KO_EPS = 0), because an
eigen-analysis of a dissipation operator answers a different question. C1 uses the production
value (KO_EPS = 0.2). The module global is restored after use.
"""
import os
import sys
import math

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import axisym_2p1_evolution as ax

FIELDS = tuple(ax.FIELDS)
NF = len(FIELDS)
RHO_IN = ax.RHO_IN
R_DOM = 24.0
KO_PROD = ax.KO_EPS

# ---------------------------------------------------------------- registered thresholds
TH_C3 = 1.0e-6          # Jacobian vs directional derivative
TH_C1_BULK = 1.5        # all growth factors within 1.5x  => BULK
TH_C1_EDGE = 2.0        # a config differs by >2x        => EDGE
TH_EDGE_MASS = 0.50     # >=50% of eigenvector mass in first/last 8%  => edge-localized
TH_CHECKER = 0.50       # checkerboard index > 0.5                     => grid-scale
TH_C4 = (0.3, 3.0)      # |Re lam / measured rate| window
TH_C5 = 0.01            # FD-step independence of the leading eigenvalue
TH_SCALE = 1.5          # Re lam ~ 1/h tolerance


# ---------------------------------------------------------------- state-vector wrapper
def state_vec(st, g):
    return np.concatenate([np.asarray(st[k][g.sl, g.sl], dtype=float).ravel() for k in FIELDS])


def vec_state(x, g, base):
    st = {k: base[k].copy() for k in FIELDS}
    n = g.N * g.N
    for i, k in enumerate(FIELDS):
        st[k][g.sl, g.sl] = x[i * n:(i + 1) * n].reshape(g.N, g.N)
    return st


def rhs_vec(x, g, bc):
    """Semi-discrete operator F(x) = rhs(symmetrise(x)) restricted to the interior block."""
    st = vec_state(x, g, bc)
    ax.symmetrise(st, g, bc)
    out, _ = ax.rhs(st, g)
    return np.concatenate([np.asarray(out[k][g.sl, g.sl], dtype=float).ravel() for k in FIELDS])


def jacobian(x0, g, bc, eps=1e-6, label=""):
    n = x0.size
    J = np.empty((n, n))
    for j in range(n):
        xp = x0.copy()
        xp[j] += eps
        xm = x0.copy()
        xm[j] -= eps
        J[:, j] = (rhs_vec(xp, g, bc) - rhs_vec(xm, g, bc)) / (2.0 * eps)
    print("    assembled %s: n = %d (%.1f MB)" % (label or "J", n, J.nbytes / 1e6))
    return J


def flat_setup(N, Rdom, rho_in, verbose=True):
    """Flat space, production initial normalisation, frozen-background Dirichlet edge."""
    g = ax.Grid(N, Rdom, rho_in)
    st0 = ax.flat_state(g, ax.homod.V_VAC)
    ax.symmetrise(st0, g)
    bc = {k: v.copy() for k, v in st0.items()}
    return g, st0, bc


# ---------------------------------------------------------------- C3: Jacobian anchor
def c3(x0, g, bc, J, rng):
    print("[C3] Jacobian correctness anchor: J.d vs central finite-difference directional derivative")
    d = rng.standard_normal(x0.size)
    d /= np.linalg.norm(d)
    jd = J @ d
    best = (np.inf, None)
    for eps in (1e-5, 1e-6, 1e-7):
        fd = (rhs_vec(x0 + eps * d, g, bc) - rhs_vec(x0 - eps * d, g, bc)) / (2.0 * eps)
        rel = float(np.linalg.norm(fd - jd) / max(np.linalg.norm(fd), 1e-300))
        print("    eps=%.0e   rel = %.3e" % (eps, rel))
        if rel < best[0]:
            best = (rel, eps)
    ok = best[0] < TH_C3
    print("    best rel = %.3e at eps=%.0e  (threshold %.1e) : %s"
          % (best[0], best[1], TH_C3, "PASS" if ok else "FAIL"))
    if not ok:
        print("    !! C3 FAILED -- the spectrum below is VOID and is not interpreted.")
    return ok


# ---------------------------------------------------------------- C1: geometry dependence
def ham_profile(st, g, rho_in, Rdom):
    _, info = ax.rhs(st, g)
    H = np.abs(info["Ham"])[g.sl, g.sl]
    rs = g.rho[g.sl]
    span = rs[-1] - rs[0] + g.h
    inner = rs < rs[0] + 0.15 * span
    outer = rs > rs[-1] - 0.15 * span
    tot = max(H.sum(), 1e-300)
    return H[inner, :].sum() / tot, H[outer, :].sum() / tot, float(H.max())


def c1():
    print("[C1] geometry dependence: flat space, h = 0.4 fixed, THREE geometries")
    print("     if the mode is BULK the three growth factors agree; if EDGE they track the edge")
    configs = [
        ("baseline  rho_in=4, R=24", 50, 24.0, 4.0),
        ("inner cut rho_in=8, R=24", 40, 24.0, 8.0),
        ("outer     rho_in=4, R=36", 80, 36.0, 4.0),
    ]
    rows = []
    for nm, N, Rdom, rin in configs:
        g, st0, bc = flat_setup(N, Rdom, rin)
        ax.KO_EPS = KO_PROD
        d0 = ax.diagnostics(st0, g)
        st = {k: v.copy() for k, v in st0.items()}
        try:
            st, hist, dt, ns = ax.run(g, st, 2.0)
            h1 = hist[-1][1]["ham"]
            growth = h1 / max(d0["ham"], 1e-300)
            fi, fo, hm = ham_profile(st, g, rin, Rdom)
            rows.append((nm, N, g.h, dt, d0["ham"], h1, growth, fi, fo, True))
            print("  %-26s N=%3d h=%.3f dt=%.3f steps=%2d  Ham(0)=%.3e  Ham(2)=%.3e  growth=%7.2f"
                  % (nm, N, g.h, dt, ns, d0["ham"], h1, growth))
            print("      |Ham| mass: inner 15%% = %.2f   outer 15%% = %.2f   max|Ham| = %.3e"
                  % (fi, fo, hm))
        except Exception as exc:
            rows.append((nm, N, g.h, 0.0, d0["ham"], float("nan"), float("nan"), 0.0, 0.0, False))
            print("  %-26s N=%3d  FAILED with %s (logged, not deleted)" % (nm, N, type(exc).__name__))
    ax.KO_EPS = KO_PROD
    good = [r for r in rows if r[9] and np.isfinite(r[6])]
    verdict = "INCONCLUSIVE"
    if len(good) == len(rows):
        base = good[0][6]
        ratios = [r[6] / base for r in good]
        print("    growth ratios relative to baseline: " + ", ".join("%.2f" % x for x in ratios))
        inner_ch = max(good[1][6] / base, base / good[1][6])
        outer_ch = max(good[2][6] / base, base / good[2][6])
        if inner_ch > TH_C1_EDGE:
            verdict = "INNER-EDGE"
        elif outer_ch > TH_C1_EDGE:
            verdict = "OUTER-EDGE"
        elif all(max(x, 1.0 / x) < TH_C1_BULK for x in ratios):
            verdict = "BULK"
        else:
            verdict = "MIXED/UNCLASSIFIED"
        print("    inner-cut change factor %.2f (edge threshold %.1f) ; outer-domain %.2f"
              % (inner_ch, TH_C1_EDGE, outer_ch))
    print("    C1 verdict: %s" % verdict)
    return verdict, rows


# ---------------------------------------------------------------- C2: spectrum
def spectrum(J, k=8):
    n = J.shape[0]
    if n <= 3200:
        w, V = np.linalg.eig(J)
        return w, V, "dense-eig"
    from scipy.sparse.linalg import eigs, LinearOperator
    op = LinearOperator((n, n), matvec=lambda v: J @ v, dtype=float)
    try:
        w, V = eigs(op, k=k, which="LR")
        return w, V, "arpack-LR(k=%d)" % k
    except Exception as exc:
        print("    arpack failed (%s); falling back to dense eig" % type(exc).__name__)
        w, V = np.linalg.eig(J)
        return w, V, "dense-eig(fallback)"


def analyze_vec(v, g):
    a = np.abs(v)
    n = g.N * g.N
    mass = np.array([a[i * n:(i + 1) * n].sum() for i in range(NF)])
    mass = mass / max(mass.sum(), 1e-300)
    V2 = a.reshape(NF, g.N, g.N).sum(axis=0)
    rs = g.rho[g.sl]
    span = rs[-1] - rs[0] + g.h
    inner = rs < rs[0] + 0.08 * span
    outer = rs > rs[-1] - 0.08 * span
    tot = max(V2.sum(), 1e-300)
    sign = (-1.0) ** (np.arange(g.N)[:, None] + np.arange(g.N)[None, :])
    checker = abs(float((sign * V2).sum())) / tot
    return mass, V2[inner, :].sum() / tot, V2[outer, :].sum() / tot, checker


def c2(res=(16, 20)):
    print("[C2] eigen-analysis of the undissipated semi-discrete operator (KO_EPS = 0)")
    out = []
    for N in res:
        g, st0, bc = flat_setup(N, R_DOM, RHO_IN)
        x0 = state_vec(st0, g)
        print("  N=%d  h=%.4f  n_dof=%d" % (N, g.h, x0.size))
        J = jacobian(x0, g, bc, 1e-6, label="J(N=%d)" % N)
        w, V, meth = spectrum(J)
        order = np.argsort(-w.real)
        wl = w[order[0]]
        vl = V[:, order[0]]
        mass, fi, fo, chk = analyze_vec(vl, g)
        print("    method %s ; leading Re lambda = %+.5f  Im = %+.5f" % (meth, wl.real, wl.imag))
        print("    top-5 Re lambda: " + ", ".join("%+.4f" % w[order[i]].real for i in range(min(5, len(order)))))
        print("    eigenvector field mass: " + "  ".join("%s=%.2f" % (FIELDS[i], mass[i])
                                                         for i in np.argsort(-mass)[:5]))
        print("    |v| mass: inner 8%% = %.2f  outer 8%% = %.2f  checkerboard index = %.2f"
              % (fi, fo, chk))
        out.append(dict(N=N, h=g.h, re=float(wl.real), im=float(wl.imag), mass=mass,
                        inner=fi, outer=fo, checker=chk, meth=meth, J=J, g=g, bc=bc, x0=x0))
    return out


def c5(rec):
    print("[C5] FD-step independence of the leading eigenvalue (eps = 1e-6 vs 1e-7)")
    J2 = jacobian(rec["x0"], rec["g"], rec["bc"], 1e-7, label="J(eps=1e-7)")
    w2, _, _ = spectrum(J2)
    re2 = float(np.max(w2.real))
    rel = abs(re2 - rec["re"]) / max(abs(rec["re"]), 1e-300)
    ok = rel < TH_C5
    print("    N=%d  Re lam(1e-6) = %+.5f   Re lam(1e-7) = %+.5f   rel diff = %.2e  (threshold %.0e): %s"
          % (rec["N"], rec["re"], re2, rel, TH_C5, "PASS" if ok else "FAIL"))
    return ok


# ---------------------------------------------------------------- C4: consistency
def c4(rec):
    N, g2 = rec["N"], rec["g"]
    print("[C4] consistency: Re lambda_max vs the growth rate measured by time integration")
    print("    same grid N=%d, KO_EPS=0, cfl=0.1 (tighter than production so that the RK4" % N)
    print("    stability limit cannot be mistaken for the physical growth)")
    ax.KO_EPS = 0.0
    g, st0, bc = flat_setup(N, R_DOM, RHO_IN)
    d0 = ax.diagnostics(st0, g)
    st = {k: v.copy() for k, v in st0.items()}
    try:
        st, hist, dt, ns = ax.run(g, st, 2.0, cfl=0.1)
        rate = math.log(hist[-1][1]["ham"] / max(d0["ham"], 1e-300)) / 2.0
        print("    Ham(0)=%.3e  Ham(2)=%.3e  dt=%.3f steps=%d  measured rate=%.4f"
              % (d0["ham"], hist[-1][1]["ham"], dt, ns, rate))
        ratio = rec["re"] / rate if abs(rate) > 1e-12 else float("inf")
        ok = (TH_C4[0] <= ratio <= TH_C4[1])
        print("    Re lam / rate = %.2f   (window %s) : %s"
              % (ratio, TH_C4, "PASS" if ok else "FAIL"))
        return ok, rate, ratio
    except Exception as exc:
        print("    FAILED with %s (logged, not deleted)" % type(exc).__name__)
        return False, float("nan"), float("nan")
    finally:
        ax.KO_EPS = KO_PROD


# ---------------------------------------------------------------- driver
def main():
    print("=" * 90)
    print("R4 instability localization: is the grid-scale mode BULK or EDGE?")
    print("registration: runs/R4/r4_instability_localization_registration.md")
    print("=" * 90)
    print("[parameters]")
    print("  production operator imported from axisym_2p1_evolution (no geometry re-implemented)")
    print("  RHO_IN=%.1f  R_DOM=%.1f  KO_PROD=%.1f  CFL=%.2f  WEIGHT=%.3f  field count=%d"
          % (RHO_IN, R_DOM, KO_PROD, ax.CFL, ax.WEIGHT, NF))
    print("  registered thresholds: C3 %.0e ; C1 bulk %.1f / edge %.1f ; edge-mass %.2f ;"
          % (TH_C3, TH_C1_BULK, TH_C1_EDGE, TH_EDGE_MASS))
    print("                         checker %.2f ; C4 %s ; C5 %.0e"
          % (TH_CHECKER, TH_C4, TH_C5))
    print()

    rng = np.random.default_rng(20261122)

    # ---- C3 first: a wrong Jacobian voids everything downstream
    g, st0, bc = flat_setup(12, R_DOM, RHO_IN)      # small grid only for the anchor
    x0 = state_vec(st0, g)
    Js = jacobian(x0, g, bc, 1e-6, label="J(N=12, anchor)")
    ok3 = c3(x0, g, bc, Js, rng)
    print()

    verdict, rows = c1()
    print()

    recs = c2()
    print()

    c5_ok = c5(recs[0])
    print()

    c4_ok, rate, ratio = c4(recs[1])
    print()

    # scaling check Re lam ~ 1/h
    print("[C2-scaling] grid-scale modes should have Re lam ~ 1/h")
    r = recs[0]
    for other in recs[1:]:
        pred = r["h"] / other["h"]
        obs = other["re"] / max(r["re"], 1e-300)
        print("    N=%d vs %d: h ratio %.3f (predicted Re-lam ratio if ~1/h) vs observed %.3f"
              % (r["N"], other["N"], pred, obs))
    print()

    print("[verdicts]")
    print("  C3 Jacobian anchor        : %s%s" % ("PASS" if ok3 else "FAIL",
                                                 "" if ok3 else "  <-- downstream spectra VOID"))
    print("  C1 geometry dependence    : %s" % verdict)
    print("  C5 FD-step independence   : %s" % ("PASS" if c5_ok else "FAIL"))
    print("  C4 spectrum-vs-evolution  : %s" % ("PASS" if c4_ok else "FAIL"))
    lead = recs[0]
    if not ok3:
        concl = "VOID -- C3 failed, no statement about the mode is licensed"
    elif verdict == "BULK":
        concl = "BULK mode: the instability is not produced by an edge; BSSN/Z4c is the registered route"
    elif verdict in ("INNER-EDGE", "OUTER-EDGE"):
        concl = ("%s mode: the instability tracks a boundary. The F.7.2-3 sentence "
                 "'the cure is a strongly hyperbolic formulation, not parameter tuning' is "
                 "OVERTURNED for this mode and must be amended" % verdict)
    else:
        concl = "UNCLASSIFIED -- C1 did not separate the branches; no amendment licensed"
    print()
    print("[conclusion] " + concl)
    print("  leading eigenvalue (N=%d): Re = %+.5f, Im = %+.5f; checkerboard %.2f; inner mass %.2f"
          % (lead["N"], lead["re"], lead["im"], lead["checker"], lead["inner"]))
    print("  REMINDER: locating the mode is not curing it. B1/B3/B4/B6 remain FAIL, and any fix")
    print("  requires a full re-run of the B-block before a stability claim is licensed.")
    print("  no physical-scale statement: kappa = 1 code units (roadmap 8.12 prohibition).")


if __name__ == "__main__":
    main()
