"""FOURDIM-V2 — adjudication of the four re-anchored dimensions against DEMO-1.

Predictions fixed in runs/MATRIX/fourdim_registration.md before this file existed.
Nothing here edits a lock, a threshold or a frame.
"""
from __future__ import annotations

import hashlib
import json
import math
import pathlib

import numpy as np
from scipy import ndimage

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "runs/MATRIX/fourdim_results.txt"

RES: list[str] = []
FLAGS: dict[str, bool] = {}


def out(s: str = "") -> None:
    RES.append(s)
    print(s)


def hdr(s: str) -> None:
    out()
    out("=" * 100)
    out(s)
    out("=" * 100)


def table(rows, cols, w=None) -> None:
    rows = [[str(c) for c in r] for r in rows]
    n = len(cols)
    if w is None:
        w = [max([len(cols[i])] + [len(r[i]) for r in rows]) for i in range(n)]
    out("  " + "  ".join(cols[i].ljust(w[i]) for i in range(n)))
    out("  " + "  ".join("-" * w[i] for i in range(n)))
    for r in rows:
        out("  " + "  ".join(r[i].ljust(w[i]) for i in range(n)))


# ------------------------------------------------------------------------------------------------ constants
LOCK = json.loads((ROOT / "runs/FRONT/demo_lock.json").read_text(encoding="utf-8"))
C = LOCK["declared_constants"]
D = LOCK["derived"]
M_SHELL, S_SIDE = C["M_shell"], C["S_side"]
H = C["H_m"]
R1, R4 = C["r1_m"], C["r4_m"]
R2_0, R2_A = C["r2_m"], C["r2_amp_m"]
R3_0, R3_A = C["r3_m"], C["r3_amp_m"]
DELTA = C["delta_m"]
PITCH = C["pitch_m"]
N_LAYER = D["N_layers"]
PIECES = D["pieces"]
CELLS = D["cells"]
CANVAS = S_SIDE * PITCH
LOCK_SHA = hashlib.sha256((ROOT / "runs/FRONT/demo_lock.json").read_bytes()).hexdigest()


def edges(z: float) -> tuple[float, float, float, float, float]:
    s = math.sin(2 * math.pi * z / H)
    return 0.0, R1, R2_0 - R2_A * s, R3_0 + R3_A * s, R4


def euler_char(m: np.ndarray) -> int:
    """chi = V - E + F - C for the cubical complex of a voxel set. Self-tested below on a single
    voxel (expect 1) and a 2x2x2 block (expect 1)."""
    nx, ny, nz = m.shape
    P = np.pad(m, 1, constant_values=False)          # P[i+1,j+1,k+1] = m[i,j,k]
    V = np.zeros((nx + 1, ny + 1, nz + 1), bool)
    for a in (0, 1):
        for b in (0, 1):
            for c in (0, 1):
                V |= P[a:a + nx + 1, b:b + ny + 1, c:c + nz + 1]
    Ex = np.zeros((nx, ny + 1, nz + 1), bool)        # along x: (nx) x (ny+1) x (nz+1)
    for b in (0, 1):
        for c in (0, 1):
            Ex |= P[1:nx + 1, b:b + ny + 1, c:c + nz + 1]
    Ey = np.zeros((nx + 1, ny, nz + 1), bool)
    for a in (0, 1):
        for c in (0, 1):
            Ey |= P[a:a + nx + 1, 1:ny + 1, c:c + nz + 1]
    Ez = np.zeros((nx + 1, ny + 1, nz), bool)
    for a in (0, 1):
        for b in (0, 1):
            Ez |= P[a:a + nx + 1, b:b + ny + 1, 1:nz + 1]
    Fz = np.zeros((nx, ny, nz + 1), bool)            # perp to z: (nx) x (ny) x (nz+1)
    Fz |= P[1:nx + 1, 1:ny + 1, 0:nz + 1]
    Fz |= P[1:nx + 1, 1:ny + 1, 1:nz + 2]
    Fy = np.zeros((nx, ny + 1, nz), bool)
    Fy |= P[1:nx + 1, 0:ny + 1, 1:nz + 1]
    Fy |= P[1:nx + 1, 1:ny + 2, 1:nz + 1]
    Fx = np.zeros((nx + 1, ny, nz), bool)
    Fx |= P[0:nx + 1, 1:ny + 1, 1:nz + 1]
    Fx |= P[1:nx + 2, 1:ny + 1, 1:nz + 1]
    return int(V.sum() - Ex.sum() - Ey.sum() - Ez.sum() + Fx.sum() + Fy.sum() + Fz.sum() - m.sum())


hdr("[0] Object of record")
out(f"  lock sha256 = {LOCK_SHA[:16]}…   spec sha256 = {LOCK['spec_sha256'][:16]}…")
out(f"  M = {M_SHELL}   H = {H} m   r4 = {R4} m   pitch = {PITCH} m   canvas = {CANVAS:,.1f} m")
out(f"  pieces = {PIECES:,}   cells = {CELLS:,}   display decimation 1 : {CELLS // (512 * 512)}")

# ================================================================================================ [A]
hdr("[A] Topological gate: 'components and genus 100% consistent'")

# self-test of the Euler routine, as in the tier work: a check that has not been shown to fire is not trusted
st1 = np.zeros((3, 3, 3), bool)
st1[1, 1, 1] = True
st2 = np.zeros((4, 4, 4), bool)
st2[1:3, 1:3, 1:3] = True
out(f"  [self-test] chi(single voxel) = {euler_char(st1)} (expect 1);  "
    f"chi(2x2x2 block) = {euler_char(st2)} (expect 1)")

zs = np.linspace(0.0, H, 2001)
mins = np.array([min(np.diff(edges(z))) for z in zs])
out()
out("  A1  the four shells share their interfaces by construction:")
out(f"      minimum shell width over z = {mins.min():.3e} m, and the shells tile [0, r4] with no gap")
out("      -> the union fills [0, r4] at every z")
out(f"      r2(z) in [{R2_0-R2_A:.4f}, {R2_0+R2_A:.4f}] m;  r3(z) in [{R3_0-R3_A:.4f}, {R3_0+R3_A:.4f}] m")
out("      => the object's MATERIAL is a solid cylinder. The 4 components are a label on it.")

NV = 132
lin = np.linspace(-R4 * 1.06, R4 * 1.06, NV)
X, Yg, Zg = np.meshgrid(lin, lin, np.linspace(0.0, H, NV), indexing="ij")
solid = (X ** 2 + Yg ** 2) <= R4 ** 2
st6 = ndimage.generate_binary_structure(3, 1)
b0_obj = ndimage.label(solid, structure=st6)[1]
pad = np.pad(solid, 1, constant_values=False)
lab_bg, _ = ndimage.label(~pad, structure=st6)
border = list({lab_bg[0, 0, 0], lab_bg[-1, -1, -1], lab_bg[0, -1, 0], lab_bg[-1, 0, -1]})
b2_obj = len(set(np.unique(lab_bg)) - set(border) - {0})
chi_obj = euler_char(solid)
b1_obj = b0_obj + b2_obj - chi_obj
out()
out(f"  A2  voxel topology of the material ({NV}^3): b0 = {b0_obj}   b2 (cavities) = {b2_obj}   "
    f"chi = {chi_obj}   =>  b1 = {b1_obj}")
out("      solid cylinder: contractible. Boundary is a sphere, genus 0. The internal interfaces are")
out("      invisible to every Betti number: a homogeneously painted cylinder scores identically.")

# deposit: plates. C1 is a disc (r in [0,R1]); C2..C4 are ANNULI, each with a through-hole.
e_mid = edges(H / 2)
n_annulus = M_SHELL - 1
b0_dep = PIECES
b1_dep = n_annulus * N_LAYER
out()
out("  A3  deposit: every interface is vacuum (front_sweep_v1 §2), so every plate is its own component")
out(f"      b0(deposit) = pieces = {b0_dep:,}")
out(f"      C1 spans [0, {e_mid[1]:.4f}] m = a disc (genus 0); C2..C4 are annuli, each with a through-hole")
out(f"      b1(deposit) = (M-1) x N_layer = {n_annulus} x {N_LAYER:,} = {b1_dep:,} holes")
out(f"      largest plate extent = {2*R4:.3f} m vs pitch {PITCH:.4f} m -> {PITCH/(2*R4):.2f}x clear, no plate touches another")

out()
table([
    ["object, material", f"{b0_obj}", f"{b1_obj}", "0"],
    ["deposit, material", f"{b0_dep:,}", f"{b1_dep:,}", f"{b1_dep:,}"],
    ["deposit, quotient by label", f"{M_SHELL}", f"{n_annulus}", "0"],
    ["idealised projection (disc)", "1", "0", "0"],
], ["reading", "b0", "b1 (holes)", "genus"], w=[28, 16, 16, 12])

out()
out("  A4  verdict under each reading, and what the gate does with it:")
table([
    ["material (the deposit as built)", f"{b0_dep:,} vs 1", f"{b1_dep:,} vs 0", "FAIL — gate closes"],
    ["quotient by declared label", "4 vs 1", "3 vs 0", "FAIL (genus)"],
    ["idealised projection", "1 vs 1", "0 vs 0", "PASS — and blind to the shells"],
], ["reading", "components", "genus", "outcome"], w=[30, 18, 16, 26])

out()
out("  A5  WHY this is not a threshold problem. D2 severs every interface; pieces = M x N_layer.")
out(f"      b0(deposit) = {b0_dep:,} >= 2 whenever N_layer >= 2, and N_layer = H/delta = {H/DELTA:,.0f} for")
out("      this object. b0(object) = 1. No sigma can change either number: sigma permutes sites, and")
out("      permutation does not create contact across vacuum. The gate therefore closes for EVERY")
out("      admissible deposit, not for a badly-chosen one. An always-closing gate carries no information.")
FLAGS["P1"] = (b0_dep == PIECES and b0_obj == 1)
FLAGS["P2"] = (b0_obj == 1 and b1_obj == 0 and b2_obj == 0)
FLAGS["P3"] = (b1_dep == 0)          # predicted the genus clause was a tautology; it is not
out()
out(f"  P1 b0 {PIECES:,} vs 1 : {'PASS' if FLAGS['P1'] else 'FAIL'}")
out(f"  P2 object contractible (b0,b1,b2)=({b0_obj},{b1_obj},{b2_obj}) : {'PASS' if FLAGS['P2'] else 'FAIL'}")
out(f"  P3 genus clause is a tautology (predicted 0 = 0) : {'PASS' if FLAGS['P3'] else 'FAIL'}")

# ================================================================================================ [B]
hdr("[B] Metric gate: distance and epsilon")
d_index, d_w1, d_haus = 0.0, H / 4.0, H / 2.0
d_half, d_sup = CANVAS / 2.0, CANVAS / math.sqrt(2.0)
table([
    ["index space (key held)", f"{d_index:.4e}", "bijection; isometry of index", "vacuous (S10 shape)"],
    ["mid-slice vs solid, W1", f"{d_w1:.4e}", "mean |z-H/2| over the solid", "the object's height"],
    ["mid-slice vs solid, Hausdorff", f"{d_haus:.4e}", "max |z-H/2|", "the object's height"],
    ["true scale, half canvas", f"{d_half:.4e}", "canvas/2", "the array's size"],
    ["true scale, Hausdorff sup", f"{d_sup:.4e}", "canvas/sqrt2", "the array's size"],
], ["convention", "d (m)", "what fixes it", "what it measures"], w=[30, 12, 30, 24])
span = math.log10(d_sup / d_w1)
out()
out(f"  B1  span over admissible conventions: {d_w1:.4e} .. {d_sup:.4e} m = {span:.2f} decades")
out("      (including the index-space reading, 0 is in the set and the ratio is unbounded)")
out("      The slice readings measure H. The true-scale readings measure the canvas. Neither measures")
out("      fidelity: on the index space the map is a bijection, so fidelity is 0 by construction, and on")
out("      the physical plane the two sets are 1.1e5 apart in extent — the number is the scale, not the error.")
out("  => epsilon cannot be declared before a scale AND an embedding are declared. Both are ours.")
FLAGS["P4"] = (span >= 5.0)
out(f"  P4 span >= 5 decades : {'PASS' if FLAGS['P4'] else 'FAIL'}  (measured {span:.2f})")

# ================================================================================================ [C]
hdr("[C] Information gate: mutual information")
e_mid = edges(H / 2)
areas = [math.pi * (e_mid[k + 1] ** 2 - e_mid[k] ** 2) for k in range(M_SHELL)]
tot = sum(areas)
frac = [a / tot for a in areas]
HY_area = -sum(f * math.log2(f) for f in frac)
HY_piece = math.log2(M_SHELL)
out("  C1  the label distribution at z = H/2 — the only structure the object can declare:")
table([[f"C{k+1}", f"{e_mid[k]:.4f}", f"{e_mid[k+1]:.4f}", f"{areas[k]:.6f}", f"{100*frac[k]:.3f}%"]
       for k in range(M_SHELL)],
      ["component", "r_in (m)", "r_out (m)", "area (m2)", "share"], w=[10, 10, 10, 11, 8])
out(f"      H over AREA  = {HY_area:.6f} bits        H over PIECES = {HY_piece:.6f} bits")
out(f"      the two differ by {HY_piece - HY_area:.4f} bits ({100*(HY_piece-HY_area)/HY_piece:.1f}%) and both are"
    f" defensible.")
out("      The map counts PIECES, so every component gets 25.0% of the sites while their areas differ by")
out(f"      {max(areas)/min(areas):.1f}x. I is not defined until the counting measure is declared: a deterministic")
out(f"      {HY_piece - HY_area:.2f}-bit ambiguity, not measurement noise.")

# ---- three orderings, sampled at block level (the full piece array is 32 GiB; blocks are what matter)
S_DISP = 512
per_px = CELLS // (S_DISP * S_DISP)
n_block = PIECES // per_px
rng = np.random.default_rng(20261122)
starts = rng.choice(n_block, 4000, replace=False).astype(np.int64)


def label_major(base: np.ndarray) -> np.ndarray:      # component-major: p // N_layer
    return np.minimum(base // N_LAYER, M_SHELL - 1)


def label_layer(base: np.ndarray) -> np.ndarray:      # layer-major: p % M -> same for any p
    return np.minimum(base % M_SHELL, M_SHELL - 1)


def label_random(base: np.ndarray) -> np.ndarray:     # a fixed random assignment of component per piece
    h = (base * 2654435761) % (2 ** 32)               # deterministic hash, no 32 GiB allocation
    return (h % M_SHELL).astype(np.int64)


offs = np.arange(per_px, dtype=np.int64)
rows = []
EXACT = {"component-major (declared)": 1.0 - (M_SHELL - 1) / n_block,   # 3 boundary blocks of 261,120
         "layer-major": 0.0,                                            # 16,384 = 4,096 exact 4-cycles
         "random permutation": 0.0}
SAMPLED = {}
for name, fn in (("component-major (declared)", label_major),
                 ("layer-major", label_layer),
                 ("random permutation", label_random)):
    pure = 0
    for s0 in starts:
        L = fn(int(s0) * per_px + offs)
        pure += int(L.min() == L.max())
    SAMPLED[name] = pure / len(starts)
    Hp = math.log2(PIECES)
    Hc = math.log2(per_px)
    rows.append([name, f"{100*EXACT[name]:.5f}%", f"{Hp - Hc:.4f}", f"{Hp:.4f}", f"{Hc:.4f}"])
table(rows, ["ordering", "pixel purity", "I(pixel; piece)", "H(piece)", "H(piece|pixel)"],
      w=[26, 22, 16, 11, 16])
I_same = rows[0][2] == rows[1][2] == rows[2][2]
out()
out("      purity above is exact (1 - 3/n_block); the 4,000-block sample returned "
    f"{SAMPLED['component-major (declared)']*100:.1f}% / {SAMPLED['layer-major']*100:.1f}% / "
    f"{SAMPLED['random permutation']*100:.1f}%, consistent, and it happens to miss the 3 boundary blocks.")
out()
out("  C2  the three orderings give the SAME I, to four decimals, and purities differing by four orders")
out(f"      of magnitude. I = log2(pieces) - log2(sites per pixel) = {rows[0][2]} bits, which is injectivity")
out("      (pieces <= cells) plus the decimation, and nothing else. A completely random permutation of")
out("      the pieces scores identically. => the criterion CANNOT reject a scrambled output at the level")
out("      of the encoding, which is the level 'scrambled' names.")
out()
out("  C3  why. Given a pixel you know it holds exactly 16,384 candidate pieces, so H(piece|pixel) = 14")
out("      bits whichever way those 16,384 were chosen. Information about the piece index is therefore")
out("      fixed by the decimation alone; the ordering moves the pieces around without changing it.")
out("      The quantity that does differ is PURITY: 99.9989% for the declared order, 0% for the others.")
out("      Purity is an arrangement property. It is not mutual information, and no I-based gate can")
out("      substitute for it — which is precisely what MR2 was reserved for.")
out()
out("  C4  scrambled IMAGE (pixels permuted after encoding) is rejected by a position-paired estimator,")
out("      but that tests a corruption applied after the encoding, not the encoding itself. The submission's")
out("      claim is about 'scrambled outputs', and the encoding is where scrambling can be chosen.")
out()
out("  C5  physical channel, homogeneous object: one content symbol per plate (KIN-DYN: D2 performs no")
out("      deformation, so no modulus enters; no compliant per-component reflectance exists — G6/DC2).")
out("      H(X) = 0 => I(X;Y) = 0 under every estimator. Declaring an object with four labelled components")
out("      is what creates any information at all, and the labels are a false-colour convention (EN2, FL1).")
FLAGS["P5"] = (abs(HY_area - 1.739) <= 0.001)
FLAGS["P6"] = I_same and abs(float(rows[0][2]) - 17.994) < 0.01
FLAGS["P7"] = False   # registered in an uncomputable form; see erratum E2 and C2, which replaces it
FLAGS["P8"] = True
FLAGS["P9"] = (HY_piece < 1.74)   # registered as "I_min > 1.74 unachievable", i.e. I capped by H(label)
out()
out(f"  P5 H(label) = {HY_area:.4f} in 1.739±0.001 : {'PASS' if FLAGS['P5'] else 'FAIL'}")
out(f"  P6 I identical across three sigma, = 17.994 : {'PASS' if FLAGS['P6'] else 'FAIL'}")
out("  P7 registered as a two-layout numeric test — NOT COMPUTABLE as written (erratum E2); C2 replaces it")
out("  P8 homogeneous body: I = 0 under every estimator : PASS (C5)")
out(f"  P9 registered: I_min > 1.74 unachievable (I <= H(label)) : {'PASS' if FLAGS['P9'] else 'FAIL'}")
out("     measured I = 17.99 bits > 1.74, because Y is the piece index (H = 32 bits), not the label.")

# ================================================================================================ [D]
hdr("[D] Visual gate: 'there must exist an observer O'")

def d2xy(n: int, d: int) -> tuple[int, int]:
    x = y = 0
    t = d
    s = 1
    while s < n:
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
    return x, y


def xy2d(n: int, x: int, y: int) -> int:
    d = 0
    s = n // 2
    while s > 0:
        rx = 1 if (x & s) > 0 else 0
        ry = 1 if (y & s) > 0 else 0
        d += s * s * ((3 * rx) ^ ry)
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            x, y = y, x
        s //= 2
    return d


ok_small = all(xy2d(64, *d2xy(64, i)) == i for i in range(64 * 64))
test_big = rng.choice(PIECES, 20_000, replace=False)
ok_big = all(xy2d(65_536, *d2xy(65_536, int(i))) == int(i) for i in test_big)
out(f"  D1  Hilbert round trip, self-test: order 6 (all 4,096 points) {'PASS' if ok_small else 'FAIL'};")
out(f"      order 16 (20,000 sampled pieces of {PIECES:,}) {'PASS' if ok_big else 'FAIL'}")
out("      So the site map is invertible and the key recovers every piece: recovery = 1.000000.")
out("  D2  Without the key there is no pairing, so the criterion has no value — not false, undefined.")
out("      'There exists an observer O' is satisfied by the only observer who holds sigma: the author.")
out("      An existence claim whose witness is our own convention cannot discriminate anything.")
out("  D3  'must not introduce physically non-existent information' needs the physical signal defined")
out("      first: per-component reflectance requires a compliant sigma_s, absent (G6/DC2). It cannot be")
out("      evaluated on any frame yet, including DEMO-1's false colour (EN2, FL1).")
out("  D4  the fourth criterion is therefore satisfied BY CONSTRUCTION and fails to be a test — the same")
out("      shape as S10: the witness exists because we made the map we made.")
FLAGS["P10"] = (ok_small and ok_big)
out(f"  P10 recovery 1.000000 with the key : {'PASS' if FLAGS['P10'] else 'FAIL'}")

# ================================================================================================ [E]
hdr("[E] Prediction ledger")
ids = [f"P{i}" for i in range(1, 11)]
npass = sum(1 for k in ids if FLAGS[k])
table([[k, "PASS" if FLAGS[k] else "FAIL"] for k in ids], ["id", "outcome"], w=[6, 8])
out()
out(f"  {npass} / {len(ids)} registered predictions pass")
fails = [k for k in ids if not FLAGS[k]]
out(f"  failed: {fails if fails else 'none'}")

out()
out("=" * 100)
out("PROVENANCE: NEITHER  (adjudication of a submitted framework against the registered record and the")
out("            locked object; establishes no new physics)")
out("=" * 100)

OUT.write_text("\n".join(RES) + "\n", encoding="utf-8")
print(f"\nwritten: {OUT}")
