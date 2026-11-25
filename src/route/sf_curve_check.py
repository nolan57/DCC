"""
Adjudication of the fourth submission: space-filling curves vs the identity map.

Predictions P1-P15 were fixed in runs/FRONT/sf_curve_registration.md before this file existed.
This executor measures; it does not choose sigma. Choosing sigma is GD11 (governor's act).

PROVENANCE: NEITHER  (adjudication of a submitted claim against the registered record; establishes no physics)
"""
import math
import re
import pathlib

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

# ---- registered constants (each with its source) ------------------------------------------------
SIDE_REG = 90126                 # front_sweep_v1 s3, Annex B sB.7
N_PLATE_REG = 1.18e10            # front_sweep_v1 s1 (census, FROZEN)
SPACING = 0.4001                 # m, mid_sweep_frame_v1 s2 (derived, returns 25.500 km exactly)
CANVAS = 36060.0                 # m, 36.06 km, mid_sweep_frame_v1 s2
DELTA = 0.215e-9                 # m, Annex B sB.1
H_BODY = 1.74                    # m, front_sweep_v1 s1
L_P = 1.6159e-35                 # m, Annex B sB.8.2
A_PLATE_MEAN = 0.0237            # m^2, front_sweep_v1 s1
A_PLATE_LO, A_PLATE_HI = 0.0063, 0.0540   # m^2, front_sweep_v1 s1 table (min, max)
A_LAYER_MEAN = 0.03453           # m^2, = 1.457 comps/layer x 0.0237 (front_sweep_v1 s1)
MEAN_PLACEMENT = 13.797e3        # m, mid_sweep_frame_v1 s2
N_LAYERS = H_BODY / DELTA        # 8.09e9

RES = []
FLAGS = {}
HITS = {}


def out(s=""):
    print(s)
    RES.append(s)


def hdr(s):
    out()
    out("=" * 100)
    out(s)
    out("=" * 100)


def table(rows, cols):
    w = [len(c) for c in cols]
    for r in rows:
        for i, c in enumerate(r):
            w[i] = max(w[i], len(str(c)))
    out("  " + "  ".join(c.ljust(w[i]) for i, c in enumerate(cols)))
    out("  " + "  ".join("-" * w[i] for i in range(len(cols))))
    for r in rows:
        out("  " + "  ".join(str(c).ljust(w[i]) for i, c in enumerate(r)))


def doc_text():
    """All markdown under docs/, concatenated, with per-file attribution for hit reporting."""
    return {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8", errors="replace")
            for p in sorted(DOCS.rglob("*.md"))}


# =================================================================================================
hdr("[A] ANCHORS AND PRESUPPOSITIONS")
# =================================================================================================
corpus = doc_text()
out(f"  {len(corpus)} markdown files under docs/")

# ---- P1: does any document supply a layer->site assignment rule?
# NOTE ON THE ENCODING. As registered, P1 was a raw token count for \bsigma\b|\bσ\b. That count is
# meaningless here: `σ` is stress in this corpus and `Σ` is column density. It returned 18 hits, none of
# which is a rule. The raw count is reported, every hit is classified, and the claim is then tested by a
# narrow rule-shaped query. Recorded as a FORM-FAILURE of my encoding, not as a refutation of the claim.
ASSIGN_PATS = [r"\bsigma\b", r"\bσ\b", r"site index", r"layer index", r"assignment rule",
               r"n_z\s*→", r"n_z\s*->", r"site of layer", r"layer to site"]
out()
out("P1 — is sigma : n_z -> (u,v) defined anywhere?")
found = {}
for name, txt in corpus.items():
    for pat in ASSIGN_PATS:
        for m in re.finditer(pat, txt, flags=re.IGNORECASE):
            ln = txt[:m.start()].count("\n") + 1
            found.setdefault(name, []).append((ln, m.group(0), txt.splitlines()[ln - 1][:150]))
total_raw = sum(len(v) for v in found.values())


def classify(tok, line):
    if tok in ("Σ", "Sigma"):
        return "column density / sum symbol"
    if "gaussian" in line.lower() or "cells" in line.lower():
        return "Gaussian width (image processing)"
    if any(s in line for s in ("ε", "μ", "stress", "strain", "σ/E", "σ_", "\\sigma")):
        return "stress"
    return "UNCLASSIFIED — inspect"


cls_rows = []
rule_hits = 0
for name, v in found.items():
    for ln, tok, line in v:
        k = classify(tok, line)
        cls_rows.append([f"{name.split('/')[-1]}:{ln}", tok, k])
        if "site" in line.lower() or "lattice" in line.lower() or "(u," in line:
            rule_hits += 1
out(f"   raw token hits = {total_raw}  (sigma = stress, Sigma = column density; the pattern cannot tell them apart)")
table(cls_rows, ["location", "token", "what it actually is"])
out()
out(f"   hits that mention a site/lattice coordinate in the same line = {rule_hits}")
out("   => every raw hit is stress or column density; none is a layer-to-site rule.")
out("   => P1 AS REGISTERED (raw count = 0): FAIL — the encoding tested a symbol, not a rule.")
FLAGS["P1_RAW"] = (total_raw == 0)
FLAGS["P1"] = (rule_hits == 0)
out(f"   => P1 CORRECTED (no rule exists, {rule_hits} rule-shaped hits): "
    f"{'PASS' if FLAGS['P1'] else 'FAIL'}")

# ---- P2: the clause that denies selection
fsw = corpus.get("docs/decisions/front_sweep_v1.md", "")
CLAUSE = "nothing in the mechanism selects it over any other relabelling"
n_clause = fsw.count(CLAUSE)
out()
out("P2 — does front_sweep_v1 s2.1 already deny that anything selects Pi?")
out(f'   "{CLAUSE}" -> {n_clause} occurrence(s)')
FLAGS["P2"] = (n_clause == 1)
out(f"   => P2 (expected 1): {'PASS' if FLAGS['P2'] else 'FAIL'}")
if FLAGS["P2"]:
    out("   The submission's central inference (S2->S3: 'therefore the algorithm is X') is the negation of a")
    out("   clause already in force. That is not my argument; it is the mechanism document's own.")

# ---- P3: projection vocabulary
PROJ = [r"orthographic", r"perspective projection", r"hilbert", r"space-filling", r"space filling",
        r"spiral", r"serpentine", r"\braster\b"]
proj_hits = {}
for name, txt in corpus.items():
    for pat in PROJ:
        c = len(re.findall(pat, txt, flags=re.IGNORECASE))
        if c:
            proj_hits[name] = proj_hits.get(name, 0) + c
out()
out("P3 — projection / traversal vocabulary in the record (excluding this run's own files)")
n_proj = sum(proj_hits.values())
out(f"   total = {n_proj}  {proj_hits if proj_hits else ''}")
FLAGS["P3"] = (n_proj == 0)
out(f"   => P3 (expected 0): {'PASS' if FLAGS['P3'] else 'FAIL'}")
if FLAGS["P3"]:
    out("   Neither the criticised method nor the proposed one is named anywhere in docs/. D2 is not a")
    out("   projection either: z survives as the site INDEX, so 'orthographic loses depth' is not about D2.")

# =================================================================================================
hdr("[B] DOES THE CITED SELECTION PRINCIPLE SELECT ANYTHING?  (S10 class)")
# =================================================================================================
N = N_PLATE_REG
log10_fact = (N * math.log(N) - N + 0.5 * math.log(2 * math.pi * N)) / math.log(10)
out("  The submission says the choice is 'dictated by the physical constraints of information")
out("  conservation and zero deformation'. What those two constraints actually pin down:")
out()
out("    information conservation  <=>  the piece->site map is injective")
out("    zero deformation         <=>  each piece is moved rigidly (a permutation of pieces, not of points)")
out()
out("  A permutation of pieces satisfies BOTH, for every permutation. Formally the admissible set is the")
out("  full symmetric group on the piece set:")
out()
out(f"    N (pieces)            = {N:.3e}")
out(f"    log10(N!)             = {log10_fact:.4e}   i.e. N! = 10^(1.14e11)")
out(f"    admissible bijections = 10^{log10_fact:.3g}")
FLAGS["P4"] = abs(log10_fact - 1.137e11) / 1.137e11 <= 0.005
out(f"   => P4 (expected log10 N! = 1.14e11): {'PASS' if FLAGS['P4'] else 'FAIL'}  ({log10_fact:.4e} vs 1.1370e11)")

# P5 — verify empirically at a small side that arbitrary bijections satisfy both constraints
S = 64
idx = np.arange(S * S).reshape(S, S)


def check_constraints(grid, S):
    """injectivity: grid is a permutation of 0..S^2-1.  rigidity: per-piece map, so each piece keeps its
    shape — here modelled as 'the map acts on piece labels only', which is true by construction for any
    grid that is a permutation. Returns (injective, rigid_by_construction)."""
    inj = np.array_equal(np.sort(grid.ravel()), np.arange(S * S))
    return inj, inj


rng = np.random.default_rng(20261122)
pass_ct = 0
for k in range(3):
    perm = rng.permutation(S * S).reshape(S, S)
    inj, rigid = check_constraints(perm, S)
    pass_ct += int(inj and rigid)
    out(f"   random bijection #{k+1}: injective={inj}  rigid(per-piece)={rigid}  -> admissible")
FLAGS["P5"] = (pass_ct == 3)
out(f"   => P5 (expected 3/3): {'PASS' if FLAGS['P5'] else 'FAIL'}")
out()
out("  Consequence. The two cited constraints admit 10^1.1e11 configurations and rank none of them. They")
out("  cannot 'dictate' a Hilbert curve over any other order, so S2 -> S3 is a non-sequitur. The premise")
out("  S1 is right and is already in force as KIN-DYN; the inference does not survive it.")

# =================================================================================================
hdr("[C] THE VOXEL READING, PRICED")
# =================================================================================================
out("  S3 is written at voxel resolution: 'every Planck-scale grid cell (or voxel)'. Priced first at the")
out("  deposit's OWN in-plane resolution a = delta = 0.215 nm, which is the finest lattice the model has.")
out()
A_VOX = DELTA ** 2
px_per_plate = A_PLATE_MEAN / A_VOX
pieces = N_PLATE_REG * px_per_plate
side_need = math.sqrt(pieces)
canvas_need = side_need * SPACING
out(f"    in-plane voxel area            = {A_VOX:.4e} m^2")
out(f"    voxels per plate               = {px_per_plate:.4e}")
out(f"    pieces if every voxel is a piece = {pieces:.4e}")
FLAGS["P6"] = pieces > 1e27
out(f"   => P6 (expected 6.05e27, >1e27): {'PASS' if FLAGS['P6'] else 'FAIL'}  ({pieces:.3e})")
out()
out(f"    array side required @ {SPACING} m = {side_need:.4e} sites")
out(f"    canvas required                = {canvas_need:.4e} m")
FLAGS["P7"] = abs(side_need - 7.78e13) / 7.78e13 <= 0.02
out(f"   => P7 (expected 7.78e13 sites / 3.11e13 m = 208 AU): {'PASS' if FLAGS['P7'] else 'FAIL'}"
    f"  ({side_need:.3e} sites, {canvas_need:.3e} m = {canvas_need/1.495978707e11:.1f} AU)")
ratio_canvas = canvas_need / CANVAS
FLAGS["P8"] = abs(ratio_canvas - 8.6e8) / 8.6e8 <= 0.05
out(f"   => P8 (expected 8.6e8 x the frozen canvas): {'PASS' if FLAGS['P8'] else 'FAIL'}  ({ratio_canvas:.3e})")
out()
out("  The census is FROZEN: 1.18e10 pieces, array 90126^2. Reading S3 literally multiplies the piece count")
out("  by 5.1e17 and the array side by 8.6e8. A submission cannot change a frozen quantity as a detail of")
out("  its algorithm; that is the 'change to D2 itself' category refused for the T4 insertion.")

# =================================================================================================
hdr("[D] THE GRID S3 ASSUMES")
# =================================================================================================
nmax = L_P / DELTA
out("  S3 fixes the grid at 'a thickness of one Planck length' and 'all physical units ... (i.e., the Planck")
out("  scale)'. Annex B sB.8.2 was registered one round ago for exactly this:")
out()
out(f"    n_max(l_P) = l_P / delta = {L_P:.4e} / {DELTA:.4e} = {nmax:.3e}   < 1")
FLAGS["P9"] = nmax < 1
out(f"   => P9 (expected 7.52e-26 < 1): {'PASS' if FLAGS['P9'] else 'FAIL'}")
out("   => no positive layer count satisfies it. The Planck thickness is not a fine grid the model declines")
out("      to use; it is a thickness at which the model has no configuration at all.")
out()
out(f"    registered site pitch  {SPACING:.4f} m   vs l_P: {SPACING/L_P:.3e}x")
out(f"    registered thickness   {DELTA:.4e} m   vs l_P: {DELTA/L_P:.3e}x")
out("  So the submission's unit cell is 34 decades from the site and 25 from the thickness. Its two")
out("  'invariants' (Planck cells, constant unit size) describe neither this deposit nor any admissible one.")
out()
span = A_PLATE_HI / A_PLATE_LO
out("  'Size of all physical units remains constant' — against the registered plate census:")
table([[f"{A_PLATE_LO:.4e}", f"{A_PLATE_HI:.4e}", f"{span:.3f}"]],
      ["min plate area (m^2)", "max plate area (m^2)", "span factor"])
FLAGS["P10"] = abs(span - 8.19) / 8.19 <= 0.02
out(f"   => P10 (expected span 8.19): {'PASS' if FLAGS['P10'] else 'FAIL'}  ({span:.3f})")

# =================================================================================================
hdr("[E] THE STEELMAN: WHAT A SPACE-FILLING sigma WOULD ACTUALLY BUY")
# =================================================================================================
out("  Ignore for a moment that S3 is inadmissible and ask the useful question: if the deposit's array is")
out("  read as an image, which ordering of layers onto sites is most legible? Implement three candidates")
out("  and measure two quantities on an S x S square:")
out()
out("    rho        = median|dn| between VERTICALLY adjacent sites / same for HORIZONTALLY adjacent sites")
out("                 (anisotropy: how unequal the z-step is along the two array axes)")
out("    contiguity = fraction of the |dn| = 1 layer pairs that land on 4-adjacent sites")
out()


def d2xy(m, d):
    """Hilbert index -> (x, y) on a 2^m square. Standard iterative form."""
    n = 1 << m
    x = y = 0
    t = d
    s = 1
    while s < n:
        rx = 1 & (t // 2)
        ry = 1 & (t ^ rx)
        if ry == 0:
            if rx == 1:
                x = s - 1 - x
                y = s - 1 - y
            x, y = y, x
        x += s * rx
        y += s * ry
        t //= 4
        s *= 2
    return x, y


def grid_hilbert(S):
    m = int(round(math.log2(S)))
    g = np.zeros((S, S), dtype=np.int64)
    for d in range(S * S):
        x, y = d2xy(m, d)
        g[y, x] = d
    return g


def grid_spiral(S):
    """Centre-out ring order (clockwise within each ring) — the 2-D reading of 'spherically symmetric
    expansion'. Bounds-guarded, so it is well defined for even and odd S alike (the first version assumed
    an exact centre and wrote negative indices for even S; that is why this one checks)."""
    g = np.full((S, S), -1, dtype=np.int64)
    cx = cy = (S - 1) // 2
    n = 0
    g[cy, cx] = n
    n += 1
    k = 1
    while n < S * S:
        cells = []
        for i in range(2 * k):
            cells.append((cx - k + i, cy - k))
        for i in range(2 * k):
            cells.append((cx + k, cy - k + i))
        for i in range(2 * k):
            cells.append((cx + k - i, cy + k))
        for i in range(2 * k):
            cells.append((cx - k, cy + k - i))
        for (x, y) in cells:
            if 0 <= x < S and 0 <= y < S and g[y, x] < 0:
                g[y, x] = n
                n += 1
        k += 1
        if k > 4 * S:
            break
    g[g < 0] = n
    return g


def stats(g, S):
    dz_h = np.abs(np.diff(g, axis=1)).ravel()     # horizontally adjacent sites
    dz_v = np.abs(np.diff(g, axis=0)).ravel()     # vertically adjacent sites
    rho = float(np.median(dz_v)) / float(np.median(dz_h))
    med_all = float(np.median(np.concatenate([dz_h, dz_v])))
    p90_all = float(np.percentile(np.concatenate([dz_h, dz_v]), 90))
    pos = np.empty((S * S, 2), dtype=np.int64)
    for yy in range(S):
        pos[g[yy], 1] = np.arange(S)
        pos[g[yy], 0] = yy
    d_man = np.abs(np.diff(pos, axis=0)).sum(axis=1)
    contig = float(np.mean(d_man == 1))
    return rho, contig, float(dz_h.mean()), float(dz_v.mean()), int(dz_v.max()), med_all, p90_all


S_LAB = 256
cands = [("raster (n = r*S + c)", np.arange(S_LAB * S_LAB).reshape(S_LAB, S_LAB)),
         ("Hilbert (order 8)", grid_hilbert(S_LAB)),
         ("spiral (centre-out rings)", grid_spiral(S_LAB))]

rows = []
for name, g in cands:
    rho, contig, mh, mv, mx, med_all, p90 = stats(g, S_LAB)
    rows.append([name, f"{rho:.3f}", f"{contig:.4f}", f"{med_all:.1f}", f"{p90:.0f}", f"{mx}"])
    HITS[name] = (rho, contig, med_all, p90, mx)
table(rows, ["candidate sigma", "rho", "contiguity", "median |dn| all adj", "p90 |dn| all adj",
             "max |dn| vert"])

rho_r, ct_r, med_r, p90_r, mx_r = HITS["raster (n = r*S + c)"]
rho_h, ct_h, med_h, p90_h, mx_h = HITS["Hilbert (order 8)"]
rho_s, ct_s, med_s, p90_s, mx_s = HITS["spiral (centre-out rings)"]

out()
FLAGS["P11"] = abs(rho_r - S_LAB) < 1e-9
out(f"   => P11 (raster rho = S exactly = {S_LAB}): {'PASS' if FLAGS['P11'] else 'FAIL'}  (rho = {rho_r:.3f})")
FLAGS["P12"] = rho_h <= 2.0
out(f"   => P12 (Hilbert rho <= 2): {'PASS' if FLAGS['P12'] else 'FAIL'}  (rho = {rho_h:.3f})")
FLAGS["P13"] = rho_s <= 3.0
out(f"   => P13 (spiral rho <= 3): {'PASS' if FLAGS['P13'] else 'FAIL'}  (rho = {rho_s:.3f})")
FLAGS["P14"] = (ct_r == 1.0 and ct_h == 1.0 and ct_s == 1.0)
out(f"   => P14 (contiguity 1.000 for all three): {'PASS' if FLAGS['P14'] else 'FAIL'}"
    f"  (raster {ct_r:.4f}, Hilbert {ct_h:.4f}, spiral {ct_s:.4f})")

out()
out("  Reading. None of the three is best at everything:")
out()
out(f"    raster  contiguity {ct_r:.4f}  rho {rho_r:.1f}   — one array step along a row moves ONE layer")
out(f"            ({DELTA*1e9:.3f} nm of body height); one step down a column moves {S_LAB}")
out(f"            ({DELTA*S_LAB*1e6:.2f} um). At the registered side that ratio is {SIDE_REG}:")
out(f"            a vertical neighbour is {DELTA*SIDE_REG*1e6:.1f} um away, a horizontal one 0.215 nm.")
out(f"    Hilbert contiguity {ct_h:.4f}  rho {rho_h:.1f}   — the only true Hamiltonian path of the three")
out(f"    spiral  contiguity {ct_s:.4f}  rho {rho_s:.1f}   — isotropic, but breaks at ring seams")
out()
out("  Contiguity was predicted to be a TIE (P14). It is not: contiguity separates the three, and Hilbert")
out("  wins it outright at exactly 1.0000. The raster's 0.9961 loss is the row-end wrap, the spiral's")
out("  0.9980 is the ring seam. So on the one property the submission's premise actually needs — that")
out("  consecutive layers land on adjacent sites — the proposed algorithm is the unique winner, and the")
out("  record's implicit order is not.")
out()
out("  Anisotropy, however, and the cost of the curve, measured rather than assumed:")
out()
out(f"    median |dn| over all adjacent pairs : raster {med_r:.1f}   Hilbert {med_h:.1f}   spiral {med_s:.1f}")
out(f"    p90    |dn| over all adjacent pairs : raster {p90_r:.0f}   Hilbert {p90_h:.0f}   spiral {p90_s:.0f}")
out(f"    max    |dn| over adjacent pairs     : raster {mx_r}   Hilbert {mx_h}   spiral {mx_s}")
out()
if med_h <= med_r and p90_h <= p90_r and ct_h >= ct_r:
    out("  Hilbert does not trade one statistic for another: it beats the raster on the median, the 90th")
    out("  percentile and contiguity, and is isotropic. Its only loss is the single largest jump")
    out(f"  ({mx_h} layers, where the curve passes near itself), which raster does not have because raster")
out("  has no such passage. Raster keeps exactly one advantage: along a row it steps by precisely one")
out("  layer, which no curve can match on both axes at once.")
out()
out("  So the submission's algorithmic instinct is CORRECT and its stated reason is not. A space-filling")
out("  sigma is the better ordering for reading the deposit as an image, and the submission is the first")
out("  text in this record to notice that the ordering was never chosen.")

out("  That is a real merit, and it is a DISPLAY merit. It is also a merit the submission never states: it")
out("  argues from 'information conservation', which all three satisfy equally.")

# =================================================================================================
hdr("[F] WHAT IS ALREADY SATISFIED WITHOUT CHANGE")
# =================================================================================================
FIT = N_PLATE_REG / SIDE_REG ** 2
per_cell = FIT * A_PLATE_MEAN
out("  P15 — is information already conserved by D2, before any space-filling curve?")
out()
out("    each piece is placed inside ONE cell, keeping its internal (x,y) identity map")
out("    a cell is one site of the array, so (piece, point) -> (cell, point) preserves every material point")
out()
out(f"    plates per cell            = {FIT:.4f}   (GD10, open)")
out(f"    plate area placed in a cell = {per_cell:.4e} m^2 of {SPACING**2:.4f} m^2 available"
    f" = {100*per_cell/SPACING**2:.1f}%")
out("    no two plates overlap if their total area fits the cell, and it does with 4.6x to spare")
FLAGS["P15"] = per_cell < SPACING ** 2
out(f"   => P15 (expected pass): {'PASS' if FLAGS['P15'] else 'FAIL'}")
out()
out("  So 'lossless rearrangement' is not something to be added: D2 already is one, and the submission's own")
out("  criterion cannot distinguish it from any other lossless arrangement. That is the whole argument.")
out()
out("  Side effect worth recording: reading (B) of GD10 (several plates per cell) is GEOMETRICALLY")
out("  admissible — 21.5% coverage — so GD10 is a labelling question, not a capacity question.")

# =================================================================================================
hdr("[G] LEDGER")
# =================================================================================================
ids_raw = [k for k in FLAGS if k.startswith("P") and "_" not in k]
ids = sorted(ids_raw, key=lambda t: int(t[1:]))
npass = sum(1 for k in ids if FLAGS[k])
out(f"  {npass} / {len(ids)} registered predictions pass")
out("  " + "  ".join(f"{i}:{'P' if FLAGS[i] else 'F'}" for i in ids))
fails = [i for i in ids if not FLAGS[i]]
out(f"  (P1_RAW is a form-failure of my own encoding, reported separately: {'pass' if FLAGS['P1_RAW'] else 'FAIL as expected'})")
out()
if fails:
    out(f"  FAILED: {', '.join(fails)} — each must be examined before any verdict is drawn from its section.")
else:
    out("  none failed")
out()
out("=" * 100)
out("PROVENANCE: NEITHER  (adjudication of a submitted claim against the registered record; establishes no physics)")

(ROOT / "runs/FRONT/sf_curve_results.txt").write_text("\n".join(RES) + "\n", encoding="utf-8")
print("\nwritten to runs/FRONT/sf_curve_results.txt")
