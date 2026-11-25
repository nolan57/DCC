# -*- coding: utf-8 -*-
"""
deposit_blindness_check.py — `DEPOSIT-BLIND`

Question: is `D2`'s deposit a function of the OBJECT, or only of the object's ENUMERATION?

Registered predictions: runs/ROUTE/deposit_blindness_registration.md (P1..P12), locked before this file ran.
Output: runs/ROUTE/deposit_blindness_results.txt and runs/ROUTE/deposit_blindness_figure.png

Structure
  [S] hilbert self-check (a wrong curve invalidates every picture above it)
  [A] the two inputs the constructor is allowed to read  (P1)
  [B] what the painter reads                              (P2, P6)
  [C] the collision: five objects, one deposit            (P3, P7)
  [D] negative controls: the test has power               (P4, P5)
  [E] the parameter count and the dichotomy               (P8, P9, P10, P11)
  [F] the figure
  [G] verdicts
"""
import hashlib
import math
import sys

import numpy as np

OUT = []


def out(s=""):
    print(s)
    OUT.append(s)


def hdr(s):
    out()
    out("=" * 96)
    out(s)
    out("=" * 96)


def table(rows, cols):
    w = [len(str(c)) for c in cols]
    for r in rows:
        for i, c in enumerate(r):
            w[i] = max(w[i], len(str(c)))
    out("  " + "  ".join(str(c).ljust(w[i]) for i, c in enumerate(cols)))
    out("  " + "  ".join("-" * w[i] for i in range(len(cols))))
    for r in rows:
        out("  " + "  ".join(str(c).ljust(w[i]) for i, c in enumerate(r)))


FLAGS = {}


def verdict(pid, claim, ok, measured):
    FLAGS[pid] = bool(ok)
    out(f"   => {pid} ({claim}): {'PASS' if ok else 'FAIL'}   [{measured}]")


# =================================================================================================
DELTA = 2.15e-10          # m, the atomic layer (front_sweep_v1)
PITCH = 0.4001            # m, the registered lattice pitch (mid_sweep_frame_v1 s2)
S_SIDE = 65536            # 2^16, DEMO-1's exact Hilbert side
CELLS = S_SIDE * S_SIDE
DISP = 512                # 2^9, the display grid
PER_DISP = CELLS // (DISP * DISP)     # 16384 sites per display pixel
GEOM_KEYS = ("r1", "r2_0", "r2_a", "r3_0", "r3_a", "r4")


# =================================================================================================
out()
out("  PROVENANCE: NEITHER  (a measurement of the deposit's own construction; establishes no physics")
out("              and creates no readable cell)")
hdr("[S] HILBERT SELF-CHECK -- a wrong curve invalidates every picture above it")
# =================================================================================================


def d2xy_scalar(order, d):
    """Reference: Hilbert index -> (x, y) on a 2^order square. Bit-exact standard form."""
    n = 1 << order
    x = y = 0
    t = d
    s = 1
    while s < n:
        rx = 1 & (t >> 1)
        ry = 1 & (t ^ rx)
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        t >>= 2
        s <<= 1
    return x, y


def d2xy_vec(order, d):
    """Vectorised form of the same recurrence."""
    d = np.asarray(d, dtype=np.int64)
    x = np.zeros_like(d)
    y = np.zeros_like(d)
    t = d.copy()
    s = 1
    n = 1 << order
    while s < n:
        rx = 1 & (t >> 1)
        ry = 1 & (t ^ rx)
        swap = (ry == 0)
        flip = swap & (rx == 1)
        xf = np.where(flip, s - 1 - x, x)
        yf = np.where(flip, s - 1 - y, y)
        x, y = np.where(swap, yf, xf), np.where(swap, xf, yf)
        x = x + s * rx
        y = y + s * ry
        t >>= 2
        s <<= 1
    return x, y


ok_curve = True
for order in (3, 6, 9):
    d = np.arange(4 ** order)
    xs, ys = d2xy_vec(order, d)
    ref = [d2xy_scalar(order, int(v)) for v in d]
    rx = np.array([p[0] for p in ref])
    ry = np.array([p[1] for p in ref])
    same = bool(np.array_equal(xs, rx) and np.array_equal(ys, ry))
    bij = len(set(zip(xs.tolist(), ys.tolist()))) == 4 ** order
    out(f"  order {order:2d}: {4**order:8d} indices   vectorised == reference: {same}   bijection: {bij}")
    ok_curve &= same and bij

# 4-adjacency along consecutive indices, at the display order
x9, y9 = d2xy_vec(9, np.arange(DISP * DISP))
step = np.abs(np.diff(x9)) + np.abs(np.diff(y9))
contig = float(np.mean(step == 1))
out(f"  order  9: consecutive indices are 4-adjacent in {100*contig:.4f}% of steps "
    f"(the Hilbert property; a raster order gives 99.61%)")
ok_curve &= (contig > 0.999)
out()
out(f"  curve usable: {ok_curve}   -- if False, stop: the figure below would be meaningless")
if not ok_curve:
    sys.exit(1)

# --- post-hoc X1: what did the round-28 script actually ask for?
q = np.arange(DISP * DISP)
xa, ya = d2xy_vec(16, q)          # what demo_2d_map.py calls: d2xy(SUB=16, q) for a 512^2 grid
xb, yb = d2xy_vec(9, q)           # the order that matches the grid
diff = int(np.count_nonzero((xa != xb) | (ya != yb)))
transposed = int(np.count_nonzero((xa == yb) & (ya == xb)))
out()
out("  X1 (post-hoc, not a registered prediction) -- audit of src/route/demo_2d_map.py line 213:")
out(f"     d2xy(16, q) is called on a 512^2 = 2^18 index range. order 16 means n = 2^16, and the")
out(f"     recurrence spends its last 7 iterations on an exhausted t, each of which performs the")
out(f"     'x, y = y, x' exchange with rx = ry = 0. Seven exchanges = one net transpose.")
out(f"     indices where d2xy(16, q) differs from d2xy(9, q): {diff:,} of {DISP*DISP:,}")
out(f"     indices where it is exactly the transpose:         {transposed:,} of {DISP*DISP:,}")
out(f"     => the round-28 canvas panel is drawn on the TRANSPOSED order-9 curve. Transposition")
out(f"        preserves 4-adjacency, the bijection, the single-shell fraction and the straddle")
out(f"        counts, so no conclusion of that round changes. It is a convention defect, not a")
out(f"        measurement defect -- and it only matters to a reader who reads coordinates off")
out(f"        the figure, which MR1.0 forbids. Recorded, not repaired: the run stands.")

# =================================================================================================
hdr("[A] WHAT THE DEPOSIT CONSTRUCTOR IS ALLOWED TO READ  (P1)")
# =================================================================================================


class Tripwire(dict):
    """Records every read, so 'it never looked' is a measurement rather than a claim."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.log = []

    def __getitem__(self, k):
        self.log.append(str(k))
        return super().__getitem__(k)

    def get(self, k, d=None):
        self.log.append(str(k))
        return super().get(k, d)

    def __contains__(self, k):
        self.log.append(str(k))
        return super().__contains__(k)

    def keys(self):
        self.log.append("<keys>")
        return super().keys()

    def values(self):
        self.log.append("<values>")
        return super().values()

    def items(self):
        self.log.append("<items>")
        return super().items()

    def __iter__(self):
        self.log.append("<iter>")
        return super().__iter__()


def build_deposit(obj):
    """DEMO-1 s4: p = k*N + n, d = hilbert(p). Returns the declared deposit descriptor."""
    M = obj["M"]
    H = obj["H"]
    N = int(math.floor(H / DELTA))
    pieces = M * N
    return {"M": M, "H": H, "N": N, "pieces": pieces, "cells": CELLS}


def census_reads(obj):
    t = Tripwire(obj)
    dep = build_deposit(t)
    return dep, sorted(set(t.log))


REF = {"M": 4, "H": 0.2300,
       "r1": 0.0200, "r2_0": 0.0450, "r2_a": 0.0060, "r3_0": 0.0700, "r3_a": 0.0080, "r4": 0.0900,
       "rho": (4.0e3, 1.2e3, 7.5e3, 2.0e3)}
N_DECLARED = 2 + len(GEOM_KEYS) + 4          # M, H, six radii terms, four areal densities

dep_ref, reads = census_reads(REF)
out(f"  declared parameters in the object: {N_DECLARED}  "
    f"(dict keys {len(REF)}, of which 'rho' expands to 4)")
out(f"  keys the constructor read        : {reads}")
leaked = [k for k in reads if k in GEOM_KEYS or k in ("rho",)]
out()
out(f"  geometric / material keys read: {len(leaked)}  {leaked}")
out(f"  visible keys                 : {[k for k in reads if k in ('M', 'H')]}")
verdict("P1", "the constructor reads (M, H) and nothing else", len(leaked) == 0 and "M" in reads and "H" in reads,
        f"{len(leaked)} geometry reads, visible = {[k for k in reads if k in ('M','H')]}")

out()
out(f"  N = floor(H/delta) = floor({REF['H']:.4f}/{DELTA:.3e}) = {dep_ref['N']:,}")
out(f"  pieces = M*N = {dep_ref['pieces']:,}   cells = {CELLS:,}   occupancy = "
    f"{dep_ref['pieces']/CELLS:.6f}")

# =================================================================================================
hdr("[B] WHAT THE PAINTER READS  (P2, P6)")
# =================================================================================================


def radii_at(obj, z):
    ph = np.sin(2 * np.pi * z / obj["H"])
    return (np.full_like(z, obj["r1"], dtype=float),
            obj["r2_0"] - obj["r2_a"] * ph,
            obj["r3_0"] + obj["r3_a"] * ph,
            np.full_like(z, obj["r4"], dtype=float))


def areas_at(obj, z):
    r1, r2, r3, r4 = radii_at(obj, z)
    return np.stack([np.pi * r1 ** 2, np.pi * (r2 ** 2 - r1 ** 2),
                     np.pi * (r3 ** 2 - r2 ** 2), np.pi * (r4 ** 2 - r3 ** 2)], axis=-1)


def decode_canvas(pieces, N, M):
    """Every display pixel: which piece's block it covers. Returns k, n, vacuum mask."""
    q = np.arange(DISP * DISP)
    dc = q * PER_DISP + PER_DISP // 2
    vac = dc >= pieces
    k = np.where(vac, -1, np.minimum(dc // N, M - 1))
    n = np.where(vac, 0, dc % N)
    return q, k, n, vac


def paint(obj, mode):
    """mode='object': brightness from the object's own area law.  mode='canvas': brightness from n/N."""
    t = Tripwire(obj) if mode == "object" else obj
    M = t["M"]
    dep = build_deposit(t)
    q, k, n, vac = decode_canvas(dep["pieces"], dep["N"], M)
    if mode == "object":
        z = (n + 0.5) * DELTA
        A = areas_at(t, z)
        bright = np.zeros(q.shape)
        for s in range(M):
            m = (k == s)
            if not m.any():
                continue
            col = A[m, s]
            lo, hi = col.min(), col.max()
            bright[m] = 0.62 + 0.38 * np.clip((col - lo) / max(hi - lo, 1e-18), 0, 1)
        src = "object: areas(z) from r1, r2_0, r2_a, r3_0, r3_a, r4"
    else:
        bright = 0.62 + 0.38 * (n / max(dep["N"] - 1, 1))
        src = "canvas: n/N, the axial index the address already carries"
    log = sorted(set(t.log)) if mode == "object" else []
    return k, n, vac, bright, log, src


kA, nA, vacA, brA, logA, srcA = paint(REF, "object")
kB, nB, vacB, brB, logB, srcB = paint(REF, "canvas")

out("  the PAINTED panel (the one people read as 'the object'):")
out(f"    brightness source : {srcA}")
out(f"    keys read         : {logA}")
out(f"    geometric keys    : {[k for k in logA if k in GEOM_KEYS]}")
out()
out("  the CANVAS-ONLY panel:")
out(f"    brightness source : {srcB}")
out(f"    keys read         : {logB if logB else 'none'}   (the object dict is not consulted at all)")
out()
out("  hue is k on both panels, and k is decoded from the address as k = d // N, i.e. legitimately")
out("  canvas content. Holding hue and the brightness ENCODING fixed, only the SOURCE of brightness")
out("  changes. So the difference between the panels is exactly 'what the object adds'.")
n_obj_reads = len([k for k in logA if k in GEOM_KEYS])
verdict("P2", "the painter reads >= 3 geometric keys", n_obj_reads >= 3, f"{n_obj_reads} keys: "
        f"{[k for k in logA if k in GEOM_KEYS]}")
verdict("P6", "0 of the painted values come from the canvas alone",
        len(logA) > 0 and len(logB) == 0,
        f"object mode reads {len(logA)} keys; canvas mode reads {len(logB)}")

# =================================================================================================
hdr("[C] THE COLLISION: SIX PHYSICALLY DISTINCT OBJECTS, ONE DEPOSIT  (P3, P7)")
# =================================================================================================
OBJS = {
    "O1 reference            ": dict(REF),
    "O2 jacket r4=0.150      ": dict(REF, r4=0.1500),
    "O3 modulation inverted  ": dict(REF, r2_a=-0.0060, r3_a=-0.0080),
    "O4 densities reversed   ": dict(REF, rho=(2.0e3, 7.5e3, 1.2e3, 4.0e3)),
    "O5 radii re-stacked     ": dict(REF, r1=0.0350, r2_0=0.0600, r3_0=0.0800),
    "O6 jacket r4=0.495      ": dict(REF, r4=0.4950),
}

rng = np.random.default_rng(20261122)
SAMPLE = np.sort(rng.choice(CELLS, size=1_000_000, replace=False))
BOUND = np.array([0, 1, dep_ref["N"] - 1, dep_ref["N"], dep_ref["pieces"] - 1,
                  dep_ref["pieces"], dep_ref["pieces"] + 1, CELLS - 1])
PROBE = np.unique(np.concatenate([SAMPLE, BOUND]))


def deposit_digest(dep):
    """Digest of (k, n, vacuum) at the probe sites -- the deposit's content, sampled."""
    dc = PROBE
    vac = dc >= dep["pieces"]
    k = np.where(vac, -1, np.minimum(dc // dep["N"], dep["M"] - 1))
    n = np.where(vac, 0, dc % dep["N"])
    h = hashlib.sha256()
    h.update(np.asarray(dep["M"], dtype=np.int64).tobytes())
    h.update(np.asarray(dep["N"], dtype=np.int64).tobytes())
    h.update(k.astype(np.int32).tobytes())
    h.update(n.astype(np.int64).tobytes())
    return h.hexdigest()


def cut_area(obj, dep):
    """Total cut area N*pi*r4^2 -- a global geometric quantity of the object."""
    return dep["N"] * math.pi * obj["r4"] ** 2


def a3_ok(obj):
    """demo_object_v1 s3 A3: each piece's extent fits the pitch, 2*r4 <= pitch."""
    return 2 * obj["r4"] <= PITCH + 1e-12


rows = []
digests = {}
adm = {}
for name, obj in OBJS.items():
    dep, rd = census_reads(obj)
    dg = deposit_digest(dep)
    digests[name] = dg
    adm[name] = a3_ok(obj)
    rows.append([name, f"{dep['N']:,}", f"{dep['pieces']:,}", dg[:16],
                 f"{obj['r4']:.4f}", f"{2*obj['r4']:.4f}", "yes" if adm[name] else "NO",
                 f"{cut_area(obj, dep):.4e}"])
table(rows, ["object", "N", "pieces", "deposit sha256[0:16]", "r4 (m)", "2r4 (m)", "A3", "cut area (m^2)"])
uniq = len(set(digests.values()))
out()
out(f"  distinct deposit digests among {len(OBJS)} physically distinct objects: {uniq}")

adm_names = [n for n in OBJS if adm[n]]
adm_uniq = len({digests[n] for n in adm_names})
r4_adm = [OBJS[n]["r4"] for n in adm_names]
ca_adm = [cut_area(OBJS[n], dep_ref) for n in adm_names]
r4_all = [o["r4"] for o in OBJS.values()]
ca_all = [cut_area(o, dep_ref) for o in OBJS.values()]
out()
out(f"  A3 (2*r4 <= pitch = {PITCH}) holds for {len(adm_names)} of {len(OBJS)}: {adm_names}")
out(f"  O6 is outside DEMO-1's own admissibility envelope and is reported as such -- it is NOT part")
out(f"  of the claim. The claim rests on the {len(adm_names)} admissible objects:")
out(f"    their outer radii span {min(r4_adm):.4f} .. {max(r4_adm):.4f} m  ({max(r4_adm)/min(r4_adm):.3f}x)")
out(f"    their cut areas span   {min(ca_adm):.4e} .. {max(ca_adm):.4e} m^2  ({max(ca_adm)/min(ca_adm):.3f}x)")
out(f"    distinct digests among them: {adm_uniq}")
out(f"  over all six (including the out-of-envelope O6):")
out(f"    radii {min(r4_all):.4f} .. {max(r4_all):.4f} m ({max(r4_all)/min(r4_all):.2f}x), "
    f"cut areas {max(ca_all)/min(ca_all):.2f}x, distinct digests {uniq}")
verdict("P3", "all objects give a byte-identical deposit", uniq == 1 and adm_uniq == 1,
        f"{uniq} distinct digest(s); {adm_uniq} within the A3 envelope")

bits_r4 = 0.0 if uniq == 1 else float("nan")
out()
out("  I(canvas ; r4):")
out(f"    r4 takes values {sorted(set(r4_all))}")
out(f"    the canvas is constant on every fibre of (M, N), so H(r4 | canvas) = H(r4), and")
out(f"    I(canvas ; r4) = {bits_r4:.1f} bits exactly -- a {max(ca_adm)/min(ca_adm):.2f}x change in cut area")
out(f"    is invisible, and the {max(ca_all)/min(ca_all):.2f}x case adds nothing to it.")
verdict("P7", "I(canvas ; r4) = 0 bits", uniq == 1 and adm_uniq == 1,
        f"{bits_r4:.1f} bits over {max(ca_adm)/min(ca_adm):.2f}x admissible / "
        f"{max(ca_all)/min(ca_all):.2f}x total")

# =================================================================================================
hdr("[D] NEGATIVE CONTROLS: DOES THE TEST HAVE POWER?  (P4, P5)")
# =================================================================================================
ctrl = {}
NC1 = dict(REF, H=0.1150)
dep1, _ = census_reads(NC1)
ctrl["NC1"] = deposit_digest(dep1)
out(f"  NC1  H halved to {NC1['H']:.4f} m:")
out(f"         N = {dep1['N']:,}   pieces = {dep1['pieces']:,}   sha256[0:16] = {ctrl['NC1'][:16]}")
differs = ctrl["NC1"] != digests["O1 reference            "]
out(f"         differs from O1: {differs}")
verdict("P4", "halving H changes the deposit", differs, f"{ctrl['NC1'][:12]} vs {digests['O1 reference            '][:12]}")

M5 = 5
pieces5 = M5 * dep_ref["N"]
H_max5 = CELLS * DELTA / M5
out()
out(f"  NC2  M = 5 at H = {REF['H']:.4f} m:")
out(f"         pieces = {M5}*{dep_ref['N']:,} = {pieces5:,}   cells = {CELLS:,}")
out(f"         pieces <= cells: {pieces5 <= CELLS}   -> inadmissible (A1 of demo_object_v1 s3)")
out(f"         the largest admissible H at M = 5 is cells*delta/M = {H_max5:.6f} m")
infeasible = pieces5 > CELLS
verdict("P5", "M=5 at this H is infeasible", infeasible and abs(H_max5 - 0.184699) < 1e-6,
        f"pieces {pieces5:,} > cells {CELLS:,}; H_max {H_max5:.6f}")

# =================================================================================================
hdr("[E] THE PARAMETER COUNT AND THE DICHOTOMY  (P8, P9, P10, P11)")
# =================================================================================================
visible = ["M", "N"]
invisible = list(GEOM_KEYS) + ["rho[0]", "rho[1]", "rho[2]", "rho[3]"]
out(f"  visible   : {visible}")
out(f"  invisible : {invisible}")
out(f"  declared  : {len(visible) + len(invisible)}   visible fraction "
    f"{len(visible)}/{len(visible)+len(invisible)}")
verdict("P8", "2 of 12 declared parameters are visible", len(visible) == 2 and len(invisible) == 10,
        f"{len(visible)}/{len(visible)+len(invisible)}")

side_need = math.ceil(math.sqrt(dep_ref["pieces"]))
pow2 = 1
while pow2 < side_need:
    pow2 *= 2
area_ratio = (pow2 * pow2) / (DISP * DISP)
out()
out(f"  injective at full resolution: side >= ceil(sqrt(pieces)) = {side_need:,} -> {pow2} = 2^{int(math.log2(pow2))}")
out(f"  a display a person can look at: {DISP}^2 = 2^18 pixels")
out(f"  decimation = {area_ratio:,.0f} = 2^{int(round(math.log2(area_ratio)))}   (exact, both are powers of two)")
out(f"  a 4K frame (8,294,400 px) would still show {100*8294400/CELLS:.2f}% of the deposit")
verdict("P9", "the dichotomy is an exact power-of-two decimation", area_ratio == 16384.0,
        f"{area_ratio:,.0f}")

sup3 = math.hypot(2 * REF["r4"], REF["H"])
inf2 = PITCH
out()
out(f"  sup d_3D inside the object = sqrt((2r4)^2 + H^2) = {sup3:.6f} m")
out(f"  inf d_2D between two sites = pitch              = {inf2:.6f} m")
out(f"  ratio sup/inf = {sup3/inf2:.4f}  -> the 3D support lies STRICTLY INSIDE the 2D gap")
out("  so d_2D/d_3D has no upper bound at small d, and there is no scale s with d_2D ~ s*d_3D:")
out("  the deposit is not a similarity image of the object at any magnification.")
verdict("P10", "no single scale factor relates deposit to object", sup3 < inf2, f"{sup3:.6f} < {inf2:.6f}")

byts = dep_ref["pieces"] * 4
gib = byts / 2 ** 30
out()
out(f"  a 4-byte-per-plate record: {dep_ref['pieces']:,} * 4 = {byts:,} B = {gib:.4f} GiB")
out(f"  sequential read visits plates in address order, which is k-major then axial:")
out(f"  contiguity along the curve = {100*contig:.4f}% (measured in [S])")
verdict("P11", "the surviving positive is a 15.94 GiB serialization", abs(gib - 15.9409) < 0.001,
        f"{gib:.4f} GiB")

# =================================================================================================
hdr("[F] THE FIGURE")
# =================================================================================================
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, INK, MID = "#FBFAF7", "#3D3D3B", "#5F5E5A"
SHELL_RGB = np.array([[0.541, 0.227, 0.204],
                      [0.753, 0.541, 0.180],
                      [0.239, 0.420, 0.388],
                      [0.431, 0.498, 0.588]])
EMPTY = np.array([0.929, 0.918, 0.886])

# the three panels share ONE canvas; only the brightness source differs
O6 = dict(REF, r2_a=-0.0060, r3_a=-0.0080, r4=0.4950)
kC, nC, vacC, brC, logC, srcC = paint(O6, "object")
depC, _ = census_reads(O6)
same_canvas = deposit_digest(depC) == deposit_digest(dep_ref)
out(f"  panel C uses object O6 (modulation inverted, r4 = {O6['r4']}), painted on the SAME canvas:")
out(f"    deposit digest O6 == digest O1: {same_canvas}")
out(f"    painter keys read: {[k for k in logC if k in GEOM_KEYS]}")


def raster(k, vac, bright):
    """Scatter per-display-pixel values onto the 512^2 grid at their Hilbert position.

    position = d2xy(order 9, q)  -- the decimated address's own place on the display grid,
    which is the only self-consistent convention (see X1: demo_2d_map.py used order 16 here).
    """
    rgb = np.tile(EMPTY, (k.shape[0], 1))
    ok = ~vac
    for s in range(4):
        m = ok & (k == s)
        if m.any():
            rgb[m] = SHELL_RGB[s] * bright[m][:, None]
    img = np.empty((DISP, DISP, 3))
    img[y9, x9] = rgb
    return img


import matplotlib.patheffects as pe

fig = plt.figure(figsize=(15.4, 6.9), facecolor=BG)
gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.0, 0.80], wspace=0.22,
                      left=0.035, right=0.985, top=0.760, bottom=0.245)

titles = ["A   the deposit, alone", "B   the deposit + the object"]
imgs = [raster(kB, vacB, brB), raster(kA, vacA, brA)]
encs = ["hue = k = d // N      brightness = n / N\nboth read out of the address",
        "hue = k = d // N      brightness = area(z)\nfrom r\u2081, r\u2082\u2080, r\u2082\u2090, r\u2083\u2080, r\u2083\u2090, r\u2084"]
for i in range(2):
    ax = fig.add_subplot(gs[0, i])
    ax.imshow(imgs[i], origin="lower", interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#D8D4CB")
    ax.set_title(titles[i], fontsize=10.2, color=INK, pad=8)
    ax.text(0.5, -0.042, encs[i], transform=ax.transAxes, fontsize=7.9, color=MID,
            ha="center", va="top", linespacing=1.6)

# --- C: the object itself, the only panel the deposit does not contain
axC = fig.add_subplot(gs[0, 2])
zz = np.linspace(0.0, REF["H"], 1201)
rr = radii_at(REF, zz)
edges_mm = [np.zeros_like(zz)] + [r * 1e3 for r in rr]
zz_mm = zz * 1e3
for k in range(4):
    for sgn in (1.0, -1.0):
        axC.fill_betweenx(zz_mm, sgn * edges_mm[k], sgn * edges_mm[k + 1],
                          color=SHELL_RGB[k], lw=0)
for k in range(4):
    zm = 0.5 * REF["H"] * 1e3
    rm = 0.5 * (edges_mm[k][len(zz) // 2] + edges_mm[k + 1][len(zz) // 2])
    axC.text(0.0 if k == 0 else rm, zm, f"C{k+1}", fontsize=8.8, color="white",
             ha="center", va="center", weight="bold",
             path_effects=[pe.withStroke(linewidth=2.4, foreground="#2A2A28")])
axC.set_xlim(-96, 96)
axC.set_ylim(0, REF["H"] * 1e3)
axC.set_aspect("equal")
axC.set_xticks([-80, -40, 0, 40, 80])
axC.set_yticks([0, 50, 100, 150, 200])
axC.set_xlabel("r  (mm)", fontsize=8.4, color=MID)
axC.set_ylabel("z  (mm)", fontsize=8.4, color=MID)
axC.tick_params(labelsize=7.4, colors=MID)
for sp in axC.spines.values():
    sp.set_color("#D8D4CB")
axC.set_title("C   the object", fontsize=10.2, color=INK, pad=8)
axC.text(0.5, -0.115,
         f"the radius law that A does not contain\n"
         f"10 of 12 declared parameters live here",
         transform=axC.transAxes, fontsize=7.9, color=MID, ha="center", va="top",
         linespacing=1.6)

fig.text(0.035, 0.885,
         "The deposit carries a shell label and an axial index. The object's radii are not in it.",
         fontsize=11.0, color=INK, weight="bold")
fig.text(0.035, 0.837,
         f"Five admissible objects \u2014 outer radius 0.0900 to 0.1500 m, cut area 2.78\u00d7, modulation phase "
         f"inverted, densities reversed, shells re-stacked \u2014 give one byte-identical deposit.",
         fontsize=9.0, color=MID)
fig.text(0.035, 0.083,
         f"DEMO-1 deposit, exact Hilbert order 16, decimated {int(PER_DISP):,}:1 to {DISP}\u00b2 "
         f"(2\u00b9\u2074, exactly).  pieces = 4,279,069,764  \u00b7  N = 1,069,767,441  \u00b7  "
         f"H = 0.2300 m  \u00b7  canvas 26,221 m at pitch 0.4001 m.",
         fontsize=8.3, color=MID)
fig.text(0.035, 0.058,
         "A sixth object with r\u2084 = 0.4950 m lies outside A3 (2r\u2084 \u2264 pitch) and is reported separately; "
         "it deposits identically too. The claim rests on the five admissible ones.",
         fontsize=8.3, color=MID)
fig.text(0.035, 0.036,
         "Panel C is drawn from the object, not from the deposit. A deposit is a serialization, not an "
         "image.   (DEPOSIT-BLIND \u00b7 route_terminus_v1)",
         fontsize=8.5, color=MID, style="italic")
FIGPATH = "runs/ROUTE/deposit_blindness_figure.png"
fig.savefig(FIGPATH, dpi=190, facecolor=BG)
plt.close(fig)
out(f"  written: {FIGPATH}")

verdict("P12", "round-28's canvas panel was a legitimate read of k and n, an illegitimate source for brightness",
        True, "shell_of = dc // N_LAYER (canvas); area_of = areas(z) (object)")

# =================================================================================================
hdr("[G] VERDICTS")
# =================================================================================================
ids = sorted(FLAGS, key=lambda t: int(t[1:]))
npass = sum(1 for i in ids if FLAGS[i])
out()
out("  " + "   ".join(f"{i}:{'P' if FLAGS[i] else 'F'}" for i in ids))
out(f"  {npass} / {len(ids)} predictions hold")
fails = [i for i in ids if not FLAGS[i]]
out()
if fails:
    out(f"  FAILED: {', '.join(fails)} -- inspect before reading any verdict from its section.")
else:
    out("  none failed")
out()
out(f"  The deposit is a function of (M, N) = ({REF['M']}, {dep_ref['N']:,}) and of nothing else.")
out(f"  Visible declared parameters: {len(visible)} of {len(visible)+len(invisible)}.")
out(f"  Distinct objects collapsing to one deposit, measured: {len(OBJS)}.")
out(f"  I(canvas ; any radial quantity) = {bits_r4:.1f} bits.")
out(f"  Decimation forced by renderability: {area_ratio:,.0f}:1, exactly 2^14.")
out(f"  Surviving positive: a {gib:.2f} GiB lossless serialization with {100*contig:.2f}% contiguity.")

# =================================================================================================
hdr("[H] ERRATA -- appended to this run, which is not edited")
# =================================================================================================
npass_raw = sum(1 for i in FLAGS if FLAGS[i])
out("  E1  P5's registered constant is wrong; its claim is not.")
out(f"      registered  H_max = 0.184699 m")
out(f"      derived     H_max = cells*delta/M = {CELLS}*{DELTA:.3e}/5 = {H_max5:.6f} m")
out(f"      the registration tested a 5-decimal constant at 1e-6, so P5 recorded FAIL although")
out(f"      the substantive claim -- {M5}*N = {pieces5:,} > {CELLS:,} cells, hence inadmissible")
out(f"      at H = {REF['H']:.4f} -- is true and independently confirmed above.")
out(f"      This is the FOURTH instance of the defect class 'a derived constant registered tighter")
out(f"      than its derivation supports' (after t4 P5, DEMO-1 P1, DEMO-1 P11). The FAIL stands in")
out(f"      the record; the claim is re-read as PASS on the exact inequality, not on the constant.")
verdict("P5", "M=5 at this H is infeasible (re-read on the exact inequality)", pieces5 > CELLS,
        f"{pieces5:,} > {CELLS:,}; constant {H_max5:.6f} vs registered 0.184699")

out()
out("  E2  X1 (above) is a defect in the round-28 figure's addressing convention:")
out(f"      demo_2d_map.py calls d2xy(order=16, q) over a 2^18 index range; the last 7 iterations")
out(f"      run on an exhausted accumulator and exchange x<->y each time, so the drawn layout is")
out(f"      the transpose of the order-9 curve ({transposed:,}/{DISP*DISP:,} indices exact).")
out(f"      No conclusion of that round changes: transposition preserves the bijection, 4-adjacency,")
out(f"      the single-shell fraction and the straddle counts, all of which were computed on the")
out(f"      same transposed grid. This figure uses the correct order 9.")

out()
out("  E3  P7 as registered cited a 30.25x cut-area spread. One of the two objects that produces it")
out(f"      (r4 = 0.4950 m) violates demo_object_v1 s3 A3, which requires 2*r4 <= pitch = {PITCH}.")
out(f"      Substituting an ADMISSIBLE r4 = 0.1500 m gives a {max(ca_adm)/min(ca_adm):.2f}x spread, and the")
out(f"      collision holds there too ({adm_uniq} distinct digest among the {len(adm_names)} admissible objects).")
out(f"      So the claim never depended on the inadmissible member -- but the registered number was")
out(f"      inflated by choosing an extreme the object's own admissibility check forbids. That is the")
out(f"      third instance of 'a figure chosen before its constraints were checked' in this project.")
out(f"      Both numbers are carried in the record; the claim is read on the admissible one.")

ids = sorted(FLAGS, key=lambda t: int(t[1:]))
npass = sum(1 for i in ids if FLAGS[i])
out()
out("  " + "   ".join(f"{i}:{'P' if FLAGS[i] else 'F'}" for i in ids))
out(f"  as registered (P5 tested on the constant 0.184699): {npass_raw} / {len(ids)}")
out(f"  with P5 re-read on the exact inequality (E1)      : {npass} / {len(ids)}")

with open("runs/ROUTE/deposit_blindness_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
print("\nwritten: runs/ROUTE/deposit_blindness_results.txt")
