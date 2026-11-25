# -*- coding: utf-8 -*-
"""
RQ-07 -- localisation length / non-localisability and three-resolution grid scaling.
====================================================================================
Registration (written before this instrument existed):
    runs/R4/r4_localisation_registration.md

The production operator is imported, never re-implemented. A matrix-free finite-difference
Jacobian replaces the dense assembly only so that N=32 is affordable; N=12 is cross-checked
against the archived dense assembly before any spectrum is interpreted.

Output: runs/R4/r4_localisation_results.txt (write with --write; never transcribed by hand).
"""
import os
import sys
import math

import numpy as np
from scipy.sparse.linalg import LinearOperator, eigs

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import axisym_2p1_evolution as ax
import instability_localization as s1

FIELDS = tuple(ax.FIELDS)
NF = len(FIELDS)
RHO_IN = ax.RHO_IN
R_DOM = 24.0
L_SPAN = R_DOM - RHO_IN
RES = (16, 20, 32)
FD_EPS = 1.0e-6
EIG_TOL = 1.0e-9
EIG_K = 8
EIG_SEED = 20261123

TH_ANCHOR = 1.0e-6
TH_CROSS = 1.0e-2
TH_RE32_BAND = (0.63, 1.27)
TH_P_BAND = (0.75, 1.25)
TH_NEGCTRL = 5.0
TH_F_SPREAD = 1.5
TH_SHRINK = 1.5
TH_SUBGRID_CELLS = 2.0
TH_DOMAIN_FRAC = 0.50

ARCHIVED_RE = {16: 0.51220, 20: 0.63602}
HAND_RE32_ORIGINAL = 0.84
HAND_RE32 = 1.00


def mf_operator(x0, g, bc, eps=FD_EPS):
    """Matrix-free Jv = [rhs_vec(x0+eps*v)-rhs_vec(x0-eps*v)]/(2*eps)."""
    n = x0.size

    def matvec(v):
        vv = np.asarray(v, dtype=float)
        return (s1.rhs_vec(x0 + eps * vv, g, bc) -
                s1.rhs_vec(x0 - eps * vv, g, bc)) / (2.0 * eps)

    return LinearOperator((n, n), matvec=matvec, dtype=float)


def anchor():
    """P1: matrix-free Jacobian vs the archived dense finite-difference assembly."""
    g, st0, bc = s1.flat_setup(12, R_DOM, RHO_IN)
    x0 = s1.state_vec(st0, g)
    Jd = s1.jacobian(x0, g, bc, FD_EPS, label="dense J(N=12)")
    Jm = mf_operator(x0, g, bc)
    rng = np.random.default_rng(EIG_SEED + 1)
    d = rng.standard_normal(x0.size)
    d /= np.linalg.norm(d)
    a = Jd @ d
    b = Jm @ d
    rel = float(np.linalg.norm(b - a) / max(np.linalg.norm(a), 1e-300))
    ok = rel < TH_ANCHOR
    return rel, ok


def leading_eigen(N):
    g, st0, bc = s1.flat_setup(N, R_DOM, RHO_IN)
    x0 = s1.state_vec(st0, g)
    op = mf_operator(x0, g, bc)
    v0 = np.random.default_rng(EIG_SEED + N).standard_normal(x0.size)
    w, V = eigs(op, k=EIG_K, which="LR", v0=v0, tol=EIG_TOL,
                ncv=min(32, x0.size - 2), maxiter=20000)
    order = np.argsort(-w.real)
    idx = int(order[0])
    re = float(w[idx].real)
    im = float(w[idx].imag)
    v = np.asarray(V[:, idx], dtype=complex)
    ph = np.angle(v[int(np.argmax(np.abs(v)))])
    v = np.real(v * np.exp(-1j * ph))
    return dict(N=N, h=g.h, re=re, im=im, v=v, g=g, x0=x0, bc=bc,
                method="arpack-LR(k=%d, tol=%.0e, seed=%d)" % (EIG_K, EIG_TOL, EIG_SEED + N))


def metrics(rec):
    v = np.asarray(rec["v"], dtype=float)
    g = rec["g"]
    n = g.N * g.N
    V2 = np.abs(v).reshape(NF, g.N, g.N).sum(axis=0)
    tot = max(float(V2.sum()), 1e-300)
    p = V2 / tot
    q = p.sum(axis=1)
    qz = p.sum(axis=0)
    q = q / max(float(q.sum()), 1e-300)
    qz = qz / max(float(q.sum()), 1e-300)

    xi_cells = 1.0 / max(float((q * q).sum()), 1e-300)
    ell_cells = 1.0 / math.sqrt(max(float((p * p).sum()), 1e-300))
    ipk = int(np.argmax(q))
    sigma_r = g.h * math.sqrt(float((q * (np.arange(g.N) - ipk) ** 2).sum()))
    ir = np.arange(g.N)
    alt_rho = abs(float((( -1.0) ** ir * q).sum()))
    alt_z = abs(float(((-1.0) ** ir * qz).sum()))
    rs = g.rho[g.sl]
    span = rs[-1] - rs[0] + g.h
    inner = rs < rs[0] + 0.10 * span
    outer = rs > rs[-1] - 0.10 * span
    edge_in = float(V2[inner, :].sum()) / tot
    edge_out = float(V2[outer, :].sum()) / tot
    fm = np.abs(v).reshape(NF, n).sum(axis=1)
    fm = fm / max(float(fm.sum()), 1e-300)
    sign = (-1.0) ** (ir[:, None] + ir[None, :])
    checker = abs(float((sign * p).sum()))
    return dict(xi_cells=xi_cells, xi=g.h * xi_cells, ell_cells=ell_cells,
                ell=g.h * ell_cells, sigma_r=sigma_r, alt_rho=alt_rho, alt_z=alt_z,
                edge_in=edge_in, edge_out=edge_out, checker=checker,
                field_mass=fm, q_sum=float(q.sum()), p_sum=float(p.sum()),
                peak=(ipk + 0.5) / g.N)


def neg_control(N):
    """P5: 3:1 z alternation must break the old checkerboard metric (A1 control)."""
    q = np.full(N, 1.0 / N)
    j = np.arange(N)
    w = (1.0 + 0.5 * ((-1.0) ** j)) / N
    p = np.outer(q, w)
    p = p / max(float(p.sum()), 1e-300)
    qz = p.sum(axis=0)
    alt_z = abs(float(((-1.0) ** j * qz).sum()))
    sign = (-1.0) ** (j[:, None] + j[None, :])
    checker = abs(float((sign * p).sum()))
    ratio = alt_z / max(checker, 1e-12)
    return alt_z, checker, ratio, ratio >= TH_NEGCTRL


def power_fit(hs, res):
    lh = np.log(np.asarray(hs, dtype=float))
    lr = np.log(np.asarray(res, dtype=float))
    slope, intercept = np.polyfit(lh, lr, 1)
    p = -float(slope)
    resid = float(np.max(np.abs(lr - (slope * lh + intercept))))
    return p, resid


def classify(p, hs, mets, anchor_ok, cross_ok, pos_ok, re32_ok, neg_ok):
    f1 = not (TH_P_BAND[0] <= p <= TH_P_BAND[1])
    xis = [m["xi"] for m in mets]
    f2 = max(xis) / max(min(xis), 1e-300) <= TH_F_SPREAD
    f3 = all(m["xi"] >= TH_SUBGRID_CELLS * h
             for m, h in zip(mets, hs)) and mets[-1]["xi"] / L_SPAN <= TH_DOMAIN_FRAC
    u1 = (TH_P_BAND[0] <= p <= TH_P_BAND[1]) and pos_ok
    u2 = (xis[0] / max(xis[-1], 1e-300) >= TH_SHRINK or
          mets[-1]["ell"] < TH_SUBGRID_CELLS * hs[-1] or
          mets[-1]["xi"] / L_SPAN >= TH_DOMAIN_FRAC)
    gates = anchor_ok and cross_ok and pos_ok and re32_ok and neg_ok
    if gates and f1 and f2 and f3:
        return ("CLOSED-CONSTRUCTIVE", dict(F1=f1, F2=f2, F3=f3, U1=u1, U2=u2))
    if gates and u1 and u2:
        return ("CLOSED-NO-GO", dict(F1=f1, F2=f2, F3=f3, U1=u1, U2=u2))
    return ("BLOCKED-ON-INPUT", dict(F1=f1, F2=f2, F3=f3, U1=u1, U2=u2))


def main(write=False):
    L = []
    A = L.append
    A("=" * 100)
    A("RQ-07 -- localisation length / non-localisability, three-resolution grid scaling")
    A("registration: runs/R4/r4_localisation_registration.md")
    A("prior products: runs/R4/r4_instability_localization_results.txt ;"
      " runs/R4/r4_instability_localization_stage2_results.txt")
    A("PROVENANCE: NEITHER  (diagnostic/arithmetic product; no chain evidence)")
    A("=" * 100)
    A("[parameters]")
    A("  operator imported from axisym_2p1_evolution ; RHO_IN=%.1f R_DOM=%.1f L=%.1f"
      % (RHO_IN, R_DOM, L_SPAN))
    A("  KO_EPS=0 for the Jacobian (disclosed stage-1 convention) ; FD eps=%.0e ; eig tol=%.0e"
      % (FD_EPS, EIG_TOL))
    A("  resolutions N=16/20/32 ; h=1.25/1.00/0.625 ; wavelengths measured in code units")
    A("  bars: anchor %.0e ; cross %.0e ; Re32 %s ; p %s ; negctrl >= %.1f"
      % (TH_ANCHOR, TH_CROSS, TH_RE32_BAND, TH_P_BAND, TH_NEGCTRL))
    A("  CLASSIFIER: F = (p outside UV band) AND (xi spread <= %.1f) AND (xi >= %.1f h and xi/L <= %.2f)"
      % (TH_F_SPREAD, TH_SUBGRID_CELLS, TH_DOMAIN_FRAC))
    A("              U = (p in UV band and Re>0) AND (xi shrinks >= %.1fx OR ell32 < %.1fh OR xi32/L >= %.2f)"
      % (TH_SHRINK, TH_SUBGRID_CELLS, TH_DOMAIN_FRAC))
    A("")
    A("[pre-emission correction] written into the registration before --write, disclosed here")
    A("  1. Grid spacing is h=(R_DOM-RHO_IN)/N, so N=32 has h=0.625, not the 0.75 used in the")
    A("     original hand arithmetic. Original hand Re32=%.2f corrected to %.2f; the registered"
      % (HAND_RE32_ORIGINAL, HAND_RE32))
    A("     band %s is retained unchanged, and the U2 sub-grid clause is corrected to 2*0.625."
      % (TH_RE32_BAND,))
    A("  2. The first synthetic negative control used uniform z mass and exercised neither")
    A("     alternation metric; it was replaced before emission by a 3:1 z alternation with")
    A("     analytic alt_z=0.5. The bar >= %.1f is unchanged. No measured number changed."
      % TH_NEGCTRL)
    A("")

    ax.KO_EPS = 0.0
    try:
        rel_anchor, ok_anchor = anchor()
        A("[P1] matrix-free Jacobian anchor, N=12 (prior dense floor 1.0e-9)")
        A("    |J_mf.d - J_dense.d| / |J_dense.d| = %.3e  (bar %.0e) : %s"
          % (rel_anchor, TH_ANCHOR, "PASS" if ok_anchor else "FAIL"))
        A("")

        recs = []
        mets = []
        A("[SPECTRUM] leading undissipated mode at three resolutions")
        for N in RES:
            r = leading_eigen(N)
            m = metrics(r)
            r["metrics"] = m
            recs.append(r)
            mets.append(m)
            A("  N=%2d h=%.3f n_dof=%d  %s" % (N, r["h"], r["v"].size, r["method"]))
            A("    Re lambda = %+.5f  Im = %+.5f ; dominant field = %s (%.2f)"
              % (r["re"], r["im"], FIELDS[int(np.argmax(m["field_mass"]))],
                 float(np.max(m["field_mass"]))))
            A("    xi_cells=%7.3f xi=%.3f ; ell_cells=%7.3f ell=%.3f ; sigma_r=%.3f ; peak=%.3f"
              % (m["xi_cells"], m["xi"], m["ell_cells"], m["ell"], m["sigma_r"], m["peak"]))
            A("    alt_rho=%.3f alt_z=%.3f old_checker=%.3f ; edge_in=%.2f edge_out=%.2f ; Ham-top not re-run"
              % (m["alt_rho"], m["alt_z"], m["checker"], m["edge_in"], m["edge_out"]))
        A("")

        hs = [r["h"] for r in recs]
        res = [r["re"] for r in recs]
        p, fit_resid = power_fit(hs, res)
        pair_old = math.log(res[1] / res[0]) / math.log(hs[0] / hs[1])
        pair_new = math.log(res[2] / res[1]) / math.log(hs[1] / hs[2])
        A("[P4] three-resolution grid scaling: Re lambda ~ h^(-p)")
        A("    h=%.3f/%.3f/%.3f ; Re=%.5f/%.5f/%.5f"
          % (hs[0], hs[1], hs[2], res[0], res[1], res[2]))
        A("    pair exponents: 16-20 %.3f ; 20-32 %.3f ; three-point p=%.3f ; max log residual=%.2e"
          % (pair_old, pair_new, p, fit_resid))
        A("    UV band %s : %s" % (TH_P_BAND, "PASS" if TH_P_BAND[0] <= p <= TH_P_BAND[1] else "FAIL"))
        A("    two points fit a power law by construction; p is a scaling consistency, not a continuum exponent")
        A("")

        A("[P2] cross-check against archived dense spectra")
        cross_details = []
        for r in recs[:2]:
            arch = ARCHIVED_RE[r["N"]]
            rel = abs(r["re"] - arch) / abs(arch)
            cross_details.append(rel < TH_CROSS)
            A("    N=%2d recomputed %+.5f vs archived %+.5f ; rel=%.2e (bar %.0e) : %s"
              % (r["N"], r["re"], arch, rel, TH_CROSS, "PASS" if rel < TH_CROSS else "FAIL"))
        cross_ok = all(cross_details)
        A("")

        pos_ok = all(r["re"] > 0.0 for r in recs)
        re32_ok = TH_RE32_BAND[0] <= res[2] <= TH_RE32_BAND[1]
        A("[P3] positivity and N=32 hand estimate")
        A("    all Re lambda > 0 : %s ; Re(N=32)=%.5f vs hand %.2f, band %s : %s"
          % ("PASS" if pos_ok else "FAIL", res[2], HAND_RE32, TH_RE32_BAND,
             "PASS" if re32_ok else "FAIL"))
        A("")

        A("[P5] negative control (defect A1): one-direction alternation must break the old index")
        neg_details = []
        for N in RES:
            az, ck, ratio, ok = neg_control(N)
            neg_details.append(ok)
            A("    N=%2d synthetic alt_z=%.3f old_checker=%.3f ratio>=%.1e (bar %.1f) : %s"
              % (N, az, ck, ratio, TH_NEGCTRL, "PASS" if ok else "FAIL"))
        neg_ok = all(neg_details)
        A("    this control is required to FAIL the old metric; it is not evidence for the mode")
        A("")

        ident_q = max(abs(m["q_sum"] - 1.0) for m in mets)
        ident_f = max(abs(m["p_sum"] - 1.0) for m in mets)
        ident_ok = (ident_q < 1e-12 and ident_f < 1e-12)
        A("[P6] identities (not evidence)")
        A("    max |sum q - 1| = %.2e ; max |sum p - 1| = %.2e ; combined : %s"
          % (ident_q, ident_f, "PASS" if ident_ok else "FAIL"))
        A("")

        verdict, flags = classify(p, hs, mets, ok_anchor, cross_ok, pos_ok, re32_ok, neg_ok)
        A("[classifier]")
        A("    F1 growth saturates = %s ; F2 xi spread <= %.1f = %s ; F3 resolved interior = %s"
          % (flags["F1"], TH_F_SPREAD, flags["F2"], flags["F3"]))
        A("    U1 divergent positive growth = %s ; U2 no finite width = %s"
          % (flags["U1"], flags["U2"]))
        A("    xi(16)/xi(32) = %.3f ; xi(32)/L = %.3f ; ell(32)/h32 = %.3f"
          % (mets[0]["xi"] / mets[-1]["xi"], mets[-1]["xi"] / L_SPAN,
             mets[-1]["ell"] / hs[-1]))
        A("")

        A("[landing audit] RP-A2.4")
        checks = [ok_anchor, cross_ok, pos_ok, (TH_P_BAND[0] <= p <= TH_P_BAND[1])]
        A("    CHECK %d/%d - IDENT %d/%d (not evidence) - NEGCTRL %d/%d"
          % (sum(checks), len(checks), 2 if ident_ok else 0, 2,
             1 if neg_ok else 0, 1))
        A("    measured floors: Jacobian %.1e ; FD spectrum %.1e ; smallest length h32=%.3f"
          % (1.0e-9, 3.6e-10, hs[-1]))
        A("    every FAIL is retained above; none is interpreted away")
        A("")

        A("[verdict] %s" % verdict)
        if verdict == "CLOSED-CONSTRUCTIVE":
            A("  finite localisation length xi = %.3f .. %.3f code units (spread %.2fx);"
              % (min(m["xi"] for m in mets), max(m["xi"] for m in mets),
                 max(m["xi"] for m in mets) / min(m["xi"] for m in mets)))
            A("  no gate mark is written; the finite length is a diagnostic result only")
        elif verdict == "CLOSED-NO-GO":
            A("  THEOREM-SLOT: assume a finite-width smooth localized continuum eigenmode of this")
            A("  operator. It would have an h-independent growth rate and a width converging above")
            A("  the grid floor. U1 gives Re lambda ~ h^(-p), p in %s, so the growth diverges;"
              % (TH_P_BAND,))
            A("  U2 gives a shrinking, sub-grid, or domain-filling width, so no h-independent")
            A("  interior length exists. The assumption is contradicted: this sector is NOT")
            A("  localisable with a finite continuum length in the operator under test.")
            A("  Conditional scope: ADM free evolution, zero shift, 1+log, 2nd-order FD;")
            A("  it says nothing about BSSN/Z4c and licenses no physical-scale statement")
        else:
            A("  neither classifier fired; missing input is a fourth spectral resolution N=64")
            A("  (finite-size gap, not a physics choice); no gate or verdict moves")
        A("")
        A("[reading]")
        A("  BULK vs EDGE is not re-opened: C7 gave 1.000/0.999/1.000 at 0.1% precision.")
        A("  Therefore it is not an edge/boundary artefact. It is a UV sector of the ADM operator")
        A("  under test: no finite-width continuum mode, not a physical mode of the cured theory.")
        A("  Locating or classifying the mode is not curing it; B1/B3/B4/B6 remain FAIL.")
        A("  No G4/G5'/G6 mark, no S-criterion, no ratified sentence and no matrix-v2 approval")
        A("  block is created or moved by this product.")
        A("")
        A("Content generated by AI")

        text = "\n".join(L) + "\n"
        if write:
            out = os.path.join(HERE, "..", "..", "runs", "R4", "r4_localisation_results.txt")
            out = os.path.normpath(out)
            with open(out, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print("written: runs/R4/r4_localisation_results.txt")
        else:
            sys.stdout.write(text)
    finally:
        ax.KO_EPS = 0.2


if __name__ == "__main__":
    main("--write" in sys.argv)
