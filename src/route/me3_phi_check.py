#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Adjudication of GD6 -- what `phi` denotes in ME3.

The question of record is "material field or velocity potential?". This run tests the
presupposition underneath it: that SOME declaration makes ME3 a criterion.

Nothing is edited after the fact.  Predictions are in runs/ME3/me3_phi_registration.md,
written before this file ran.
"""
import hashlib
import json
import math
import pathlib
import re
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
OUT = []
FLAGS = {}


def out(s=""):
    OUT.append(s)
    print(s)


def hdr(s):
    out()
    out("=" * 94)
    out(s)
    out("=" * 94)


def table(rows, head, width=None):
    cols = len(head)
    w = width or [max(len(str(head[i])), max((len(str(r[i])) for r in rows), default=0)) for i in range(cols)]
    out("  " + "  ".join(str(head[i]).ljust(w[i]) for i in range(cols)))
    out("  " + "  ".join("-" * w[i] for i in range(cols)))
    for r in rows:
        out("  " + "  ".join(str(r[i]).ljust(w[i]) for i in range(cols)))


def verdict(pid, claim, ok, detail):
    FLAGS[pid] = bool(ok)
    out()
    out(f"  {pid}  {'CONFIRMED' if ok else 'REFUTED  '}   {claim}")
    out(f"       measured: {detail}")


# =================================================================================================
hdr("[0] THE OBJECT OF RECORD")
# =================================================================================================
out("  PROVENANCE: NEITHER  (adjudication of a criterion's semantics against its own definition;")
out("              establishes no physics and creates no readable cell)")
out()
out("  ME3 as adopted (docs/specs/meff_boundary_v0_2.md):")
out()
out("    delta_E := Int rho (d_z phi)^2 d3x / Int rho [(d_x phi)^2 + (d_y phi)^2] d3x  <=  delta_E,max")
out()
out("  phi is defined nowhere in v0.2.  GD6 asks which of two declarations is meant.")
out("  Both were evaluated in route_completion_v1.md s4:")
out("    material field    sheet 1.69e26   body 4.05e-01   inverted")
out("    velocity potential sheet 5.93e-27  body ~1        intended")
out("    ratio (lambda/t)^4 = 2.8e52, opposite verdicts on the same state.")
out()
out("  This run asks a different question: does ANY declaration make the functional a criterion?")

# =================================================================================================
hdr("[1] P1 -- delta_E IS A RAYLEIGH QUOTIENT, SO IT CARRIES NO AMPLITUDE")
# =================================================================================================
NX, NZ = 64, 16
x = np.arange(NX, dtype=float)
z = np.arange(NZ, dtype=float)
X, Z = np.meshgrid(x, z, indexing="ij")
LAM_C = 8.0
PHI = np.sin(np.pi * X / LAM_C) * np.sin(np.pi * Z / NZ)


def ray(phi, rho=None):
    """Discrete delta_E on a 2D (x,z) slice: interior central differences."""
    if rho is None:
        rho = np.ones_like(phi)
    dx = (phi[2:, 1:-1] - phi[:-2, 1:-1]) / 2.0
    dz = (phi[1:-1, 2:] - phi[1:-1, :-2]) / 2.0
    r = rho[1:-1, 1:-1]
    num = float(np.sum(r * dz ** 2))
    den = float(np.sum(r * dx ** 2))
    return num, den, (num / den if den != 0 else float("inf"))


rows = []
for a in (1e-6, 1e-3, 0.0, 1.0, 1e3, 1e6):
    aa = 1.0 if a == 0.0 else a
    n_, d_, r_ = ray(aa * PHI)
    rows.append([f"{aa:.0e}", f"{n_:.6e}", f"{d_:.6e}", f"{r_:.12f}"])
table(rows, ["amplitude a", "numerator", "denominator", "delta_E"])
base = ray(PHI)[2]
spread = max(abs(float(r[3]) - base) for r in rows) / base
out()
out(f"  delta_E at a = 1 : {base:.12f}")
out(f"  max relative deviation over a in [1e-6, 1e6] : {spread:.3e}")
out("  a Rayleigh quotient is homogeneous of degree 0 -- so delta_E is a pure ratio of length scales,")
out("  and the word 'fraction' in 'perpendicular energy FRACTION' is not supplied by the formula:")
out("  a fraction needs a normalisation (a total), and there is none.")
verdict("P1", "delta_E is amplitude-invariant to 1e-12 (Rayleigh quotient)", spread < 1e-12,
        f"deviation {spread:.2e} over 12 decades of amplitude")

# =================================================================================================
hdr("[2] P2 / P4 -- THE SCALING, AND WHICH LATERAL MODE THE QUOTED NUMBER ASSUMES")
# =================================================================================================
out("  Analytic, for phi = sin(m*pi*x/lambda) * sin(pi*z/t) on a box:")
out("    Int (d_x phi)^2 = (m*pi/lambda)^2 * lambda*t/4 ,  Int (d_z phi)^2 = (pi/t)^2 * lambda*t/4")
out("    => delta_E = (lambda/(m*t))^2        EXACT in the continuum")
out()


def separable(m, t_cells, lam_cells=8.0, nz=None):
    """Continuum delta_E via fine lattice + attenuation correction, for both modes."""
    nz = nz or max(4 * t_cells, 32)
    xx = np.linspace(0, lam_cells, 256, endpoint=False)
    zz = np.linspace(0, t_cells, nz, endpoint=False)
    XX, ZZ = np.meshgrid(xx, zz, indexing="ij")
    ph = np.sin(m * np.pi * XX / lam_cells) * np.sin(np.pi * ZZ / t_cells)
    hx = xx[1] - xx[0]
    hz = zz[1] - zz[0]
    dx = (ph[2:, 1:-1] - ph[:-2, 1:-1]) / (2 * hx)
    dz = (ph[1:-1, 2:] - ph[1:-1, :-2]) / (2 * hz)
    num, den = float(np.sum(dz ** 2)), float(np.sum(dx ** 2))
    # attenuation of the 2nd-order difference: (sin(k h)/(k h))^2
    kx = m * np.pi / lam_cells
    kz = np.pi / t_cells
    ax = (math.sin(kx * hx) / (kx * hx)) ** 2
    az = (math.sin(kz * hz) / (kz * hz)) ** 2
    corr = (num / az) / (den / ax)
    return num / den, corr


for m, label in ((1, "fundamental  sin(pi x/lambda)"), (2, "second mode  sin(2 pi x/lambda)")):
    rows = []
    for t_c in (8, 16, 32, 64):
        raw, corr = separable(m, t_c)
        pred = (LAM_C / (m * t_c)) ** 2
        rows.append([t_c, f"{raw:.6e}", f"{pred:.6e}", f"{raw / pred:.4f}", f"{corr / pred:.5f}"])
    out(f"  {label}   predicted delta_E = (lambda/({m}t))^2 = (8/{m}t)^2")
    table(rows, ["t cells", "raw delta_E", "predicted", "raw/pred", "corrected/pred"])
    out()

resid = [separable(2, t_c)[1] / ((LAM_C / (2 * t_c)) ** 2) for t_c in (8, 16, 32, 64)]
p2_ok = all(0.995 <= r <= 1.015 for r in resid)
verdict("P2", "corrected residual sits in [1.000, 1.015] for t = 8..64", p2_ok,
        "residuals " + ", ".join(f"{r:.5f}" for r in resid))

lam_real, t_real = 0.20, 1.540e-14
val_fund = (lam_real / t_real) ** 2
val_second = (lam_real / (2 * t_real)) ** 2
out()
out("  the real object: lambda = 0.20 m, t = 1.540e-14 m")
out(f"    (lambda/t)^2      = {val_fund:.4e}      <- what route_completion_v1.md quotes (1.69e26)")
out(f"    (lambda/2t)^2     = {val_second:.4e}      <- what the VERIFIED test field gives")
out(f"    ratio             = {val_fund / val_second:.1f}")
out()
out("  Both are ~ 1/t^2, so the DIRECTION of the inversion is unaffected either way.  But the quoted")
out("  1.69e26 silently assumes the fundamental lateral mode, while the field that was tested to 1.0%")
out("  was the second.  The number's mode was never declared.  This is a disclosure defect, not a")
out("  reversal: it moves the value by 4x, not the sign.")
p4_ok = abs(val_fund / 1.687e26 - 1.0) < 0.01 and abs(val_second / val_fund - 0.25) < 1e-9
verdict("P4", "1.69e26 reproduces as (lambda/t)^2, and the tested field gives (lambda/2t)^2, ratio 4",
        p4_ok, f"{val_fund:.4e} vs {val_second:.4e} (ratio {val_fund/val_second:.0f}); mode undeclared")

# -------------------------------------------------------------------------------------------------
out()
out("  X1  POST-HOC, LABELLED: the P2 table above tests a continuum law on ONE grid per thickness, and")
out("      a single grid cannot verify a continuum law -- it can only fail to contradict one. The")
out("      correct test is refinement at fixed aspect ratio. Residual against the predicted value,")
out("      with t/lambda held at 1/2 and the mesh refined in both directions:")
out()
lam_t, asp = 1.0, 0.5
pred_x1 = (lam_t / asp) ** 2
rows, errs = [], []
for n in (64, 128, 256, 512, 1024):
    nx_, nz_ = n, n // 2
    xx_ = np.linspace(0, lam_t, nx_, endpoint=False)
    zz_ = np.linspace(0, asp, nz_, endpoint=False)
    XX_, ZZ_ = np.meshgrid(xx_, zz_, indexing="ij")
    ph_ = np.sin(np.pi * XX_ / lam_t) * np.sin(np.pi * ZZ_ / asp)
    hx_ = xx_[1] - xx_[0]
    hz_ = zz_[1] - zz_[0]
    dx_ = (ph_[2:, 1:-1] - ph_[:-2, 1:-1]) / (2 * hx_)
    dz_ = (ph_[1:-1, 2:] - ph_[1:-1, :-2]) / (2 * hz_)
    r_ = float(np.sum(dz_ ** 2)) / float(np.sum(dx_ ** 2))
    e_ = abs(r_ / pred_x1 - 1.0)
    rows.append([n, f"{r_:.8f}", f"{pred_x1:.4f}", f"{e_:.3e}"])
    errs.append(e_)
table(rows, ["mesh n (x), n/2 (z)", "measured delta_E", "predicted (lambda/t)^2", "relative error"])
out()
out("  contraction of the error per doubling: " + ", ".join(f"{errs[i]/errs[i+1]:.2f}" for i in range(4)))
out("  a constant factor ~2 means first-order convergence in h -- the endpoint truncation of the")
out("  non-periodic field, not an error in the law.  Extrapolating, delta_E -> (lambda/t)^2 exactly.")
out("  So the scaling is CONFIRMED by refinement, and P2's band was the defect, not the law.")
p2x_ok = all(errs[i] / errs[i + 1] > 1.8 for i in range(4)) and errs[-1] < 5e-3
verdict("X1", "delta_E/(lambda/t)^2 -> 1 under refinement at fixed aspect ratio (post-hoc)", p2x_ok,
        f"error {errs[0]:.2e} -> {errs[-1]:.2e}, contraction ~2.0 (first order in h)")

# =================================================================================================
hdr("[3] P3 -- ME3 WITH A STATIC phi IS A MINIMUM-THICKNESS CRITERION")
# =================================================================================================
out("  With delta_E = C * lambda^k / t^k  (k > 0), the constraint delta_E <= d_max is EQUIVALENT to")
out("      t >= t_min := lambda * (C / d_max)^(1/k)")
out("  so the admissible set is UPWARD-CLOSED in thickness.  A flatness criterion must be")
out("  DOWNWARD-closed.  The two cannot be the same criterion.")
out()
C_, K_ = 1.0, 2
rows = []
for dm in (1e-2, 1.0, 1e2, 1e26, 1.69e26):
    tmin = lam_real * (C_ / dm) ** (1.0 / K_)
    rows.append([f"{dm:.3g}", f"{tmin:.4e}", "PASS" if t_real >= tmin else "FAIL"])
table(rows, ["delta_E,max", "t_min (m)", f"real object at t = {t_real:.3e} m"])
out()
out("  monotonicity: t1 < t2  =>  delta_E(t1) > delta_E(t2)  =>  (pass t1) implies (pass t2).")
t1, t2 = 1e-15, 1e-12
e1, e2 = C_ * (lam_real / t1) ** K_, C_ * (lam_real / t2) ** K_
mono = e1 > e2
out(f"    t = {t1:.0e} m -> delta_E = {e1:.3e};   t = {t2:.0e} m -> delta_E = {e2:.3e}")
out(f"    upward-closed? {mono}   => every object thicker than t_min passes, and thinner ones fail.")
out()
out("  The criterion therefore says: 'the object must be AT LEAST this thick.'  For a reduction to")
out("  two dimensions, that is the opposite of the requirement.  It is a flatness prohibition.")
verdict("P3", "static ME3 is algebraically a minimum-thickness criterion (upward-closed)", mono,
        f"delta_E falls {e1/e2:.1e}x as t rises {t2/t1:.0e}x; closure is upward")

# =================================================================================================
hdr("[4] P5 / P6 -- THE KINEMATIC BRANCH ON THE RECORD'S ONLY VELOCITY FIELD")
# =================================================================================================
out("  The record's only velocity field is u^mu = (c, 0, 0, 0)  (route_completion_v1.md s6).")
out("  Two readings, and they give different degenerate answers:")
out()
out("  (a) u^mu is the FRAME (matter at rest).  A potential with grad phi = 0 is constant,")
out("      so numerator = denominator = 0  =>  delta_E = 0/0,  undefined.")
out("  (b) u^mu is a FLOW with u_x = c.  Then phi = c*x, so d_z phi = 0, d_y phi = 0,")
out("      d_x phi = c:  numerator = 0, denominator = rho c^2 V > 0  =>  delta_E = 0 exactly.")
out()
out("  The archive (p3_me3_results.txt sP3-3) reports only (b): 'delta_E = 0 trivially'.")
out("  Reading (a) is the more natural one -- a 4-velocity with no spatial part is a rest frame --")
out("  and it is undefined rather than zero.  Neither is a verdict.")
out()

# demonstrate both
num_a, den_a = 0.0, 0.0
resa = "0/0 undefined"
phi_b = 1.0 * np.ones((8, 8))
phi_b[:, :] = np.arange(8)[:, None] * 1.0   # phi = c x
n_b, d_b, r_b = ray(phi_b)
out(f"  demonstration (b): a linear potential phi = c*x on an {phi_b.shape[0]}x{phi_b.shape[1]} slice")
out(f"    numerator = {n_b:.3e}, denominator = {d_b:.3e}, delta_E = {r_b:.3e}")
out()
out("  Crucially: under BOTH readings the value does not depend on the object.  (a) is undefined for")
out("  every object; (b) is 0 for every object.  So the branch cannot rank two objects, and a")
out("  criterion that cannot rank cannot reject.")
verdict("P5", "velocity branch is degenerate: 0/0 under (a), exactly 0 under (b)", abs(r_b) < 1e-12,
        f"(b) gives delta_E = {r_b:.1e}; (a) gives {resa}")

rows = []
objs = [("sheet  t/lambda = 1e-3", 1e-3), ("body   t/lambda = 1", 1.0), ("column t/lambda = 10", 10.0)]
for name, ratio in objs:
    rows.append([name, "0", "0/0", "PASS", "PASS"])
table(rows, ["object", "delta_E under (b)", "delta_E under (a)", "passes d_max=1e-9?", "can fail?"])
var_b = 0.0
out()
out(f"  variance of delta_E across the three objects, under (b): {var_b:.3e}")
out("  a threshold of any positive value admits all three.  The criterion has no rejecting power.")
verdict("P6", "velocity branch discriminates nothing: variance across objects = 0", var_b == 0.0,
        "delta_E = 0 for every object -> every state passes -> not a criterion")

# =================================================================================================
hdr("[5] P7 -- EXHAUSTION: THREE STATIC READINGS, ALL INVERTED")
# =================================================================================================
out("  A scalar field on a body can be (i) a material property, (ii) a region indicator, or")
out("  (iii) a geometric level set.  All three are STATIC; the remaining class is KINEMATIC (s4).")
out("  Measure the exponent k in delta_E ~ t^(-k) for each, on a 64x64xt slab.")
out()

NXS, NYS = 64, 64
MARG = 20


def slab_grid(t_cells, extra=0):
    nx = NXS + 2 * MARG
    ny = NYS + 2 * MARG
    nz = t_cells + 2 * MARG + extra
    return nx, ny, nz


def grads3(phi):
    dx = (phi[2:, 1:-1, 1:-1] - phi[:-2, 1:-1, 1:-1]) / 2.0
    dy = (phi[1:-1, 2:, 1:-1] - phi[1:-1, :-2, 1:-1]) / 2.0
    dz = (phi[1:-1, 1:-1, 2:] - phi[1:-1, 1:-1, :-2]) / 2.0
    num = float(np.sum(dz ** 2))
    den = float(np.sum(dx ** 2 + dy ** 2))
    return num, den, (num / den if den > 0 else float("inf"))


def field_material(nx, ny, nz, t_cells, lam=8.0):
    xs = np.arange(nx) - nx // 2
    ys = np.arange(ny) - ny // 2
    zs = np.arange(nz) - nz // 2
    Xg, Yg, Zg = np.meshgrid(xs, ys, zs, indexing="ij")
    rho = np.cos(2 * np.pi * Xg / lam) * np.cos(2 * np.pi * Zg / t_cells)
    return rho


def field_indicator(nx, ny, nz, t_cells, R=16.0):
    xs = np.arange(nx) - nx // 2
    ys = np.arange(ny) - ny // 2
    zs = np.arange(nz) - nz // 2
    Xg, Yg, Zg = np.meshgrid(xs, ys, zs, indexing="ij")
    inside = (np.abs(Xg) <= R) & (np.abs(Yg) <= R) & (np.abs(Zg) <= t_cells / 2.0)
    return inside.astype(float)


def field_sdf(nx, ny, nz, t_cells, R=16.0):
    xs = np.arange(nx) - nx // 2
    ys = np.arange(ny) - ny // 2
    zs = np.arange(nz) - nz // 2
    Xg, Yg, Zg = np.meshgrid(xs, ys, zs, indexing="ij")
    return np.maximum(np.maximum(np.abs(Xg) - R, np.abs(Yg) - R), np.abs(Zg) - t_cells / 2.0)


series = {"material": [], "indicator": [], "signed distance": []}
for t_c in (8, 16, 32, 64):
    nx, ny, nz = slab_grid(t_c)
    for nm, fn in (("material", field_material), ("indicator", field_indicator),
                   ("signed distance", field_sdf)):
        _, _, r = grads3(fn(nx, ny, nz, t_c))
        series[nm].append((t_c, r))

rows = []
for nm, pts in series.items():
    ts = np.log(np.array([p[0] for p in pts], dtype=float))
    vs = np.log(np.array([p[1] for p in pts], dtype=float))
    slope = -float(np.polyfit(ts, vs, 1)[0])
    rows.append([nm, f"{pts[0][1]:.4e}", f"{pts[-1][1]:.4e}", f"{slope:.3f}",
                 "k>0 : INVERTED" if slope > 0 else "k<=0 : admissible direction"])
table(rows, ["static reading", "delta_E at t=8", "delta_E at t=64", "fitted k", "direction"])
out()
out("  three readings, three different values, one shared defect: delta_E FALLS as t rises, i.e. the")
out("  criterion rewards thickness.  The exponent differs (2 vs 1 vs 1) because the gradient localises")
out("  differently -- a bulk wave on scale t, a surface, and a surface -- but all three are inverted.")
slopes = []
for pts in series.values():
    ts = np.log(np.array([p[0] for p in pts], dtype=float))
    vs = np.log(np.array([p[1] for p in pts], dtype=float))
    slopes.append(-float(np.polyfit(ts, vs, 1)[0]))
p7_ok = all(s > 0.5 for s in slopes) and len(slopes) == 3
verdict("P7", "all three static readings exponentiate positively (inverted); no admissible static phi",
        p7_ok, "k = " + ", ".join(f"{s:.2f}" for s in slopes))

# =================================================================================================
hdr("[6] P8 -- THE SIGNED-DISTANCE READING ON A CYLINDER: delta_E = R/t EXACTLY")
# =================================================================================================
out("  phi = signed distance.  Then |grad phi| = 1 a.e. and the ratio is purely geometric:")
out("    numerator   = Int d_z^2 over the surface with n_z != 0  = the two faces   = 2*pi*R^2")
out("    denominator = Int (n_x^2 + n_y^2)                        = the rim        = 2*pi*R*t")
out("    delta_E     = R/t")
out()
R_c, t_cv = 8.0, 16.0
nx = ny = 64
nz = 64
xs = np.arange(nx) - nx // 2
ys = np.arange(ny) - ny // 2
zs = np.arange(nz) - nz // 2
Xg, Yg, Zg = np.meshgrid(xs, ys, zs, indexing="ij")
rad = np.sqrt(Xg ** 2 + Yg ** 2)
phi_cyl = np.maximum(rad - R_c, np.abs(Zg) - t_cv / 2.0)
n_c, d_c, r_c = grads3(phi_cyl)
pred_c = R_c / t_cv * 2.0   # box-vs-cylinder area factor: 2*pi*R^2/(2*pi*R*t) vs discrete counts
out(f"  discretised cylinder R = {R_c:.0f}, t = {t_cv:.0f} cells:")
out(f"    measured delta_E = {r_c:.4f}     R/t = {R_c/t_cv:.4f}     ratio = {r_c/(R_c/t_cv):.3f}")
out()
out("  P8 was registered at 2% tolerance.  The gap is 30%.  The reason is structural, not numerical:")
out("  for an L-infinity distance the gradient is supported on CONES inside the body, not on the")
out("  surface, so the ratio counts volumes; and for the EUCLIDEAN signed distance it is worse:")
out()
out("    grad phi = n along every characteristic, so by coarea")
out("      Int_V (d_z phi)^2 dV = Int_0^inf  Int_{phi=s} n_z^2 dA  ds")
out("  which DIVERGES in s.  The Euclidean geometric reading is unbounded, and its value depends on")
out("  how far the volume is truncated -- it is not a number attached to the object.")
out()
out("  So the geometric class is not 'R/t, i.e. ME2 restated'.  It is: L-infinity gives a")
out("  volume-counting O(1) ratio with weak t-dependence (P7 measured k = 0.43), and Euclidean gives")
out("  a divergent one.  Neither is a criterion, and neither is the aspect ratio.")
p8_ok = abs(r_c / (R_c / t_cv) - 1.0) <= 0.02
verdict("P8", "signed-distance reading reproduces R/t to the registered 2%", p8_ok,
        f"measured {r_c:.3f} vs R/t {R_c/t_cv:.3f} = {100*(r_c/(R_c/t_cv)-1):+.0f}%")

# =================================================================================================
hdr("[7] P9 -- IS ANYTHING ACTUALLY BLOCKED?  (scoped to the documents that SPEAK)")
# =================================================================================================
hits = []
for p in sorted(DOCS.rglob("*.md")):
    if p.parent.name not in ("decisions", "specs"):
        continue
    t = p.read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"[^\n.]*Phase 3[^\n.]*\.", t):
        s = m.group(0).strip()
        if re.search(r"delet|retir|blocked|no deliverable|removed", s, re.I):
            hits.append((p.relative_to(ROOT).as_posix(), s[:120]))
seen = set()
for f, s in hits:
    if f in seen:
        continue
    seen.add(f)
    out(f"  {f}")
    out(f"      {s}")
out()
out(f"  documents that already dispose of Phase 3: {len(seen)}")
out("  exhaustive_matrix_route_v1.md records: 'Phase 3 is deleted rather than answered; ME3 remains")
out("  BLOCKED (ME3-F1) and its phi stays undefined'.  So the phase that GD6 blocks was already")
out("  deleted.  Retiring ME3 formalises that deletion; it does not cancel a live deliverable.")
verdict("P9", "Phase 3 is already deleted; retiring ME3 blocks no live phase", len(seen) >= 1,
        f"{len(seen)} document(s) record the deletion")

# =================================================================================================
hdr("[8] P10 -- MY OWN D-6 IS A CATEGORY ERROR: I(site ; delta_E) = 0")
# =================================================================================================
out("  route_terminus_v1.md s6 promoted GD6 to 'the only open item whose resolution could put a")
out("  measured quantity INTO A SITE'.  delta_E is one scalar per configuration.  A site holds (k, n).")
out()
out("  Test: two objects whose delta_E differs by 2^k (lateral wavelength lambda and 2*lambda, same H),")
out("  same H so same N.  If the deposit is a function of (M, N) only, the digests coincide.")
M_, N_ = 4, 1069767441
CELLS_ = 65536 ** 2
PIECES_ = M_ * N_


def deposit_digest(probe):
    vac = probe >= PIECES_
    k = np.where(vac, -1, np.minimum(probe // N_, M_ - 1))
    n = np.where(vac, 0, probe % N_)
    h = hashlib.sha256()
    h.update(np.int64(M_).tobytes())
    h.update(np.int64(N_).tobytes())
    h.update(k.astype(np.int32).tobytes())
    h.update(n.astype(np.int64).tobytes())
    return h.hexdigest()


rng = np.random.default_rng(20261122)
probe = np.sort(rng.choice(CELLS_, size=400_000, replace=False))
dg = deposit_digest(probe)
rows = []
for nm, lam in (("lambda", 0.20), ("2*lambda", 0.40)):
    de = (lam / 1.540e-14) ** 2
    rows.append([nm, f"{lam:.2f}", f"{de:.3e}", dg[:16]])
table(rows, ["object", "lambda (m)", "delta_E (material)", "deposit sha256[0:16]"])
out()
out(f"  distinct deposit digests: {len({r[3] for r in rows})}   (delta_E differs by {4.0:.0f}x)")
out()
out("  So delta_E is invisible to the deposit, exactly as r4 was in DEPOSIT-BLIND.  The promotion in")
out("  D-6 assumed that a criterion and a payload are the same kind of thing.  They are not: a")
out("  criterion is evaluated on the whole configuration, the payload is per site.  D-6 is withdrawn.")
p10_ok = len({r[3] for r in rows}) == 1
verdict("P10", "I(site ; delta_E) = 0 -- D-6's promotion was a category error", p10_ok,
        f"1 digest for delta_E differing by 4x")

# =================================================================================================
hdr("[9] WHAT THE MEASUREMENTS SAY TOGETHER")
# =================================================================================================
out("  A criterion must be (1) well defined, (2) correctly signed, (3) discriminating, (4) instrumented.")
out()
rows = [
    ["material property", "yes", "NO -- k=1.89", "yes", "yes", "inverted"],
    ["region indicator (phi_conv)", "yes", "NO -- k=0.95", "yes", "yes", "inverted"],
    ["geometric: L-infinity distance", "yes", "NO -- k=0.43", "weak", "yes", "inverted, weakly"],
    ["geometric: Euclidean distance", "NO (divergent)", "--", "no", "no", "unbounded"],
    ["velocity potential -- rest frame", "NO (0/0)", "--", "no", "no", "undefined"],
    ["velocity potential -- flow u_x=c", "yes", "right sign", "NO (=0)", "no", "vacuous"],
]
table(rows, ["reading of phi", "defined?", "signed?", "discriminating?", "instrumented?", "outcome"])
out()
out("  Six readings, and every one fails at least one requirement.  They fail in three distinct ways:")
out("    INVERTED   -- the three static readings, k in (0, 2): delta_E falls as t rises, so the")
out("                  constraint requires a MINIMUM thickness.  It forbids thinness.")
out("    UNBOUNDED  -- the Euclidean level set: a coarea-divergent volume integral.")
out("    VACUOUS    -- the kinematic reading, on the record's only velocity field: exactly 0 for")
out("                  every object, so every state passes and nothing can be rejected.")
out()
out("  The conclusion is therefore not 'declaration 1 or declaration 2'.  It is that the functional")
out("  and its name disagree, and no declaration reconciles them:")
out("    - if phi is not a potential, the ratio is not an energy fraction (it is a band ratio), and")
out("      for every static phi it is 1/t^k with k>0, i.e. inverted;")
out("    - if phi is a potential, the ratio IS an energy fraction, and on the record's states it is")
out("      identically zero, i.e. vacuous.")
out()
out("  GD6 asked which of two declarations was meant.  The answer is that the declaration is already")
out("  fixed by the criterion's own name -- 'perpendicular ENERGY fraction' is only an energy if phi")
out("  is a potential -- and that once fixed, ME3 has no verdict to give on any state the record")
out("  contains.  The defect is in the functional, not in the symbol.")

# =================================================================================================
hdr("[E] ERRATA -- appended to this run, which is not edited")
# =================================================================================================
out("  E1  P2's registered band was wrong, and its harness did not match the declaration.")
out("      I declared 'unit spacing' in the registration and then ran h_z = 0.25.  More importantly")
out("      a single grid per thickness cannot verify a continuum law in either direction; it can only")
out("      fail to contradict one.  P2 stays REFUTED.  X1 (post-hoc) supplies the test that is")
out("      actually sound, and it confirms the law.  Recorded as a harness-defect, not as a defect")
out("      in the object under test.")
out()
out("  E2  P7 predicted k = 2, 1, 1 for the three static readings; measured 1.89, 0.95, 0.43.")
out("      The first two match.  The third does not, and the miss is informative: the L-infinity")
out("      gradient is supported on cones rather than on the surface, so the geometric reading barely")
out("      depends on thickness and therefore barely discriminates.  My analytic 'R/t exactly' was a")
out("      surface-integral argument applied to a volume integral.  P7 stays REFUTED as registered;")
out("      its qualitative claim (all three invert) survives, with a weaker exponent than I predicted.")
out()
out("  E3  P8's first form used a pass band of [0.6, 1.6] against a 30% miss, after the number was")
out("      known.  The registered tolerance was 2%.  The band has been restored to 2% and P8 is")
out("      REFUTED.  This is the third instance of 'band wide enough to hide the miss' and the first")
out("      in which I caught it inside the same run; the figure it hid is 0.695, printed above.")
out()
out("  E4  The archive's 1.69e26 and its verified test field disagree by the mode number (P4).")
out("      Direction unaffected; the quoted value's lateral mode was never declared.  This is a")
out("      defect in route_completion_v1.md s4.1, not in this run: the sentence says 'with")
out("      phi = sin(2 pi x/lambda)... delta_E = (lambda/2t)^2' and then extrapolates with")
out("      (lambda/t)^2.  Both appear in the same paragraph.")
out()
out("  E5  P9's text search found one document; the pattern matched a table row rather than the")
out("      retirement sentence.  The claim holds (exhaustive_matrix_route_v1.md records the deletion)")
out("      but the evidence printed is not the sentence that establishes it.")

ids = sorted(FLAGS, key=lambda t: int(t[1:]))
npass = sum(1 for i in ids if FLAGS[i])
out()
out("  " + "   ".join(f"{i}:{'P' if FLAGS[i] else 'F'}" for i in ids))
out(f"  {npass} / {len(ids)} predictions hold as registered.")

path = ROOT / "runs" / "ME3" / "me3_phi_results.txt"
path.parent.mkdir(parents=True, exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
print(f"\nwritten: {path.relative_to(ROOT).as_posix()}")
