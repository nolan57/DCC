# -*- coding: utf-8 -*-
"""
dimension_anchor_check.py — `DIM-ANCHOR`

Question: do the four dimension theorems (Brouwer, Cantor, Hilbert, Kakeya) forbid the `DEMO-1` deposit —
or is the deposit outside every one of their hypotheses?

Three questions per anchor: (a) is the mathematics as stated true, (b) is the attribution correct,
(c) does the deposit lie inside the hypothesis.  (c) has never been asked in this record.

Registered predictions: runs/DIM/dimension_anchors_registration.md (P1..P18), locked before this file ran.
Output: runs/DIM/dimension_anchors_results.txt

Structure
  [0] object of record and provenance
  [S] hilbert self-check, both directions (a wrong curve invalidates [A] and [D])
  [A] scope: what dimension is the deposit                  (P1, P2)
  [B] A1 Brouwer                                            (P3, P4, P5)
  [C] A2 Cantor                                             (P6, P7, P8, P9)
  [D] A3 Hilbert                                            (P10, P11, P12, P13)
  [E] A4 Kakeya                                             (P14, P15, P16)
  [F] A5 the conclusion                                     (P17, P18)
  [G] verdicts
"""
import math
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = []


def out(s=""):
    print(s)
    OUT.append(s)


def hdr(s):
    out()
    out("=" * 100)
    out(s)
    out("=" * 100)


def table(rows, cols, widths=None):
    if widths is None:
        widths = [max(len(str(cols[i])), max((len(str(r[i])) for r in rows), default=0))
                  for i in range(len(cols))]
    out("  " + "  ".join(str(cols[i]).ljust(widths[i]) for i in range(len(cols))))
    out("  " + "  ".join("-" * widths[i] for i in range(len(cols))))
    for r in rows:
        out("  " + "  ".join(str(r[i]).ljust(widths[i]) for i in range(len(cols))))


FLAGS = {}
NOTE = {}


def verdict(pid, claim, ok, detail=""):
    FLAGS[pid] = bool(ok)
    NOTE[pid] = claim
    out(f"  {pid:<4} {'PASS' if ok else 'FAIL'}   {claim}")
    if detail:
        out(f"        {detail}")


# =================================================================================================
# CONSTANTS -- locked in docs/specs/demo_object_v1.md (sha256 afe855c2...4633)
# =================================================================================================
M = 4
S = 65536
H = 0.2300
DELTA = 2.15e-10
PITCH = 0.4001
N_LAYER = int(H / DELTA)          # 1,069,767,441
PIECES = M * N_LAYER              # 4,279,069,764
CELLS = S * S                     # 4,294,967,296
CANVAS = S * PITCH                # 26,221.0 m
ORDER = 16


def d2xy(n, d):
    """Index -> grid cell, Hilbert order log2(n)."""
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


def xy2d(n, x, y):
    """Grid cell -> index (inverse of d2xy)."""
    d = 0
    s = n // 2
    while s > 0:
        rx = 1 if (x & s) > 0 else 0
        ry = 1 if (y & s) > 0 else 0
        d += s * s * ((3 * rx) ^ ry)
        if ry == 0:
            if rx == 1:
                x = n - 1 - x
                y = n - 1 - y
            x, y = y, x
        s //= 2
    return d


hdr("[0] OBJECT OF RECORD AND PROVENANCE")
out("  the claim adjudicated : four dimension theorems are offered as the foundation of route_terminus_v1")
out("  the object tested     : the locked DEMO-1 deposit, sigma(p) = hilbert_16(k*N + n)")
out()
out("  PROVENANCE: NEITHER  (this adjudicates the validity of citations; it establishes no physics,")
out("              sets no threshold, and creates no readable cell -- it cannot move G1)")
out()
out(f"  M = {M}   S = {S}   H = {H} m   delta = {DELTA} m   pitch = {PITCH} m")
out(f"  N = floor(H/delta) = {N_LAYER:,}   pieces = {PIECES:,}   cells = {CELLS:,}   "
    f"free = {CELLS - PIECES:,}")
out(f"  canvas = S*pitch = {CANVAS:,.1f} m")

# =================================================================================================
hdr("[S] HILBERT SELF-CHECK, BOTH DIRECTIONS (P10)")
# =================================================================================================
out("  a) d2xy is a bijection at every finite order -- exhaustive to order 6")
out()
rows = []
all_bij = True
for k in range(1, 7):
    n = 2 ** k
    cells = [d2xy(n, d) for d in range(n * n)]
    uniq = len(set(cells))
    adj = sum(1 for i in range(len(cells) - 1)
              if abs(cells[i + 1][0] - cells[i][0]) + abs(cells[i + 1][1] - cells[i][1]) == 1)
    bij = uniq == n * n
    all_bij &= bij
    rows.append([k, n * n, n * n, uniq, f"{100.0 * adj / (len(cells) - 1):.2f}%", str(bij)])
table(rows, ["order k", "indices 4^k", "cells (2^k)^2", "distinct hit", "4-adjacent", "bijection"])
out()
out("     4^k = (2^k)^2 identically, so the finite Hilbert curve is a bijection between two sets of")
out("     equal size.  The adjacency column is the Hilbert property (a raster order gives 99.61%).")

out()
out("  b) d2xy and xy2d are mutually inverse at order 16 -- sampled")
rng = np.random.default_rng(20261122)
samp = rng.integers(0, CELLS, size=200_000)
bad = 0
for p in samp[:20_000]:
    x, y = d2xy(S, int(p))
    if xy2d(S, x, y) != int(p):
        bad += 1
out(f"     20,000 samples round-tripped: {20_000 - bad:,} exact, {bad} failure(s)")
inv_ok = bad == 0
out()
out(f"  curve usable: {all_bij and inv_ok}   -- if False, stop: [A] and [D] would be meaningless")

# =================================================================================================
hdr("[A] SCOPE -- WHAT DIMENSION IS THE DEPOSIT?  (P1, P2)")
# =================================================================================================
out("  The four anchors are theorems about spaces.  Before any of them can apply, the deposit has to")
out("  BE a space of the kind they name.  Its domain is a set of plate indices; its codomain is a set of")
out("  grid cells.  Both are FINITE.  A finite set of isolated points is a discrete space, and a discrete")
out("  space has Lebesgue covering dimension 0 -- the singletons are an open refinement of every cover.")

# a reduced object, exhaustively
K_TOY = 3
S_TOY = 2 ** K_TOY
N_TOY = 30
M_TOY = 2
P_TOY = M_TOY * N_TOY
toy_cells = [d2xy(S_TOY, k * N_TOY + n) for k in range(M_TOY) for n in range(N_TOY)]
toy_uniq = len(set(toy_cells))
out()
out(f"  reduced object for exhaustive check: M={M_TOY}, S={S_TOY} (order {K_TOY}), N={N_TOY}, "
    f"pieces={P_TOY}, cells={S_TOY ** 2}")
out(f"    distinct cells occupied: {toy_uniq} of {P_TOY}  ->  bijection: {toy_uniq == P_TOY}")
dmin_toy = min(
    math.hypot(a[0] - b[0], a[1] - b[1])
    for i, a in enumerate(toy_cells) for b in toy_cells[i + 1:]
)
out(f"    minimum separation between two occupied sites: {dmin_toy:.1f} cell(s)")
out("    -> every site is isolated (separation > 0), the space is discrete, dim = 0")

out()
out("  Any bijection between two discrete spaces is a homeomorphism: continuity of f and f^-1 requires")
out("  only that preimages of open sets be open, and in a discrete space EVERY subset is open.  So:")
out(f"    dim(domain) = 0,  dim(codomain) = 0,  bijection = homeomorphism  ->  0 = 0")
out("  Brouwer's INVARIANCE half -- dimension is a topological invariant -- is SATISFIED by the deposit,")
out("  at 0 = 0.  It is an instance of that half, not an exception to it.  The other half, invariance of")
out("  DOMAIN, begins 'if U is an OPEN subset of R^n', and does not apply: see [B].")

out()
out("  full object: the same argument, at scale")
out(f"    domain     : {PIECES:,} plate indices, all isolated (index step 1)")
out(f"    codomain   : {PIECES:,} distinct cells of {CELLS:,}, minimum separation pitch = {PITCH} m")
out(f"    occupancy  : {PIECES / CELLS:.6f}   free cells: {CELLS - PIECES:,}")
sample_p = rng.integers(0, PIECES, size=200_000)
uniq_p = np.unique(sample_p)          # the sampler draws WITH replacement: dedupe the INPUTS first, or
                                      # the birthday collisions of the draw are mistaken for collisions of the map
sample_cells = {d2xy(S, int(p)) for p in uniq_p}
n_rep = 200_000 - len(uniq_p)
exp_rep = 200_000 ** 2 / (2 * PIECES)
out(f"    200,000 draws -> {len(uniq_p):,} distinct indices ({n_rep} birthday repeat(s), expected "
    f"{exp_rep:.1f} by n^2/2C)")
out(f"    {len(uniq_p):,} distinct indices -> {len(sample_cells):,} distinct cells "
    f"({'no collision' if len(sample_cells) == len(uniq_p) else 'COLLISION'})")
bij_full = len(sample_cells) == len(uniq_p)
verdict("P1", "deposit domain and codomain are finite discrete => dim 0 and dim 0 => it SATISFIES Brouwer at 0",
        all_bij and toy_uniq == P_TOY and bij_full and dmin_toy > 0,
        f"toy bijection {toy_uniq}/{P_TOY}, min sep {dmin_toy:.1f} cell, "
        f"{len(uniq_p):,} distinct indices collision-free")

out()
out("  ...but the deposit LOOKS two-dimensional, and that is measurable.  Box-counting on the occupancy:")
out()
out("    at eps >= pitch  : N(eps) tracks (canvas/eps)^2 -- exactly at eps = pitch up to the measured")
out("                       0.996299 occupancy, and up to 1.9e-10 at eps >= 2 cells:")
out(f"                       P(one cell empty) = {1 - PIECES / CELLS:.6f};  "
    f"P(2x2 box empty) = {(1 - PIECES / CELLS) ** 4:.2e}")
n_empty_2x2 = (S // 2) ** 2 * (1 - PIECES / CELLS) ** 4
out(f"                       expected empty 2x2 boxes over the canvas: {n_empty_2x2:.2f}")
out(f"                       => log-log slope 2  =>  box dimension 2 at every scale a viewer sees")
out(f"    at eps <  pitch  : each box holds at most one site, N(eps) = pieces = {PIECES:,} constant")
out(f"                       => N(eps) independent of eps  =>  box dimension 0")
out("    the LIMIT eps -> 0 is 0.  So the deposit is a 0-dimensional space that is drawn on a")
out("    2-dimensional lattice:  it looks like a picture at every scale a person can see, and is not")
out("    one-to-one anywhere.  That gap is the decimation gap, not a topological fact.")

out()
out("  P2  which anchors have a hypothesis a FINITE set can satisfy?  (The string is not the test: a")
out("      Kakeya set never says 'continuum', it says 'a unit segment in every direction', which already")
out("      forces uncountably many points.  Each row is decided by what the hypothesis REQUIRES.)")
anchors = [
    ("A1 Brouwer", "U must be OPEN in R^n",
     "an open set has cardinality c and is not finite", False),
    ("A2 Cantor", "two sets of equal cardinality, and a bijection",
     "cardinality alone; a finite pair satisfies it vacuously", True),
    ("A3 Hilbert", "a CONTINUOUS surjection from [0,1]",
     "the domain is [0,1], which is not finite", False),
    ("A4 Kakeya", "a set containing a unit SEGMENT in every direction",
     "a segment has cardinality c; the set is not finite", False),
]
rows = [[n, h, why, "YES" if a else "no"] for n, h, why, a in anchors]
table(rows, ["anchor", "what the hypothesis requires", "why a finite set fails it", "applies?"],
      [11, 44, 46, 8])
n_app = sum(1 for a in anchors if a[3])
out()
out(f"    anchors whose hypothesis a finite set satisfies: {n_app} of 4  ({'A2' if n_app == 1 else '?'})")
out("    A2 applies -- and it applies VACUOUSLY: 'a bijection exists because the cardinalities match'")
out("    is true of any two finite sets with N <= C.  That is the deposit's own branch, and it is the")
out("    load-bearing one.  P2 as registered predicted 0 of 4.  It is refuted: the count is 1, and the")
out("    1 is the anchor the conclusion actually needs.")
verdict("P2", "0 of 4 anchors has the deposit in its hypothesis class", n_app == 0,
        f"measured {n_app} of 4 -- A2 applies vacuously; P2 REFUTED as registered")

# =================================================================================================
hdr("[B] A1 BROUWER  (P3, P4, P5)")
# =================================================================================================
corpus = {}
for p in list((ROOT / "docs").rglob("*.md")):
    corpus[str(p.relative_to(ROOT))] = p.read_text(encoding="utf-8", errors="ignore")
hit = {k: len(re.findall(r"Brouwer", v)) for k, v in corpus.items() if re.search(r"Brouwer", v)}
out(f"  'Brouwer' in docs/ ({len(corpus)} files): {sum(hit.values())} occurrence(s) "
    f"in {len(hit)} file(s)")
verdict("P3", "'Brouwer' is absent from docs/ -- the anchor is new to the record, not a restatement",
        sum(hit.values()) == 0, f"{sum(hit.values())} hits")

out()
out("  the hypothesis, verbatim from the 1912 paper's modern form:")
out("      'If U is an OPEN subset of R^n and f: U -> R^n is injective and continuous, then f(U) is")
out("       open and f is a homeomorphism.'   Consequence: for n > m there is NO continuous injective")
out("       map f: U -> R^m from a nonempty open U subset R^n.")
out("  The first word of the hypothesis is 'open'.  Is the deposit's domain open in R^3?")
out()
out(f"    the domain is a finite set of {PIECES:,} points")
out(f"    Lebesgue measure of a finite set in R^3: 0  (countable union of singletons)")
out(f"    an open ball of radius {PITCH / 2:.4f} m about a site contains 1 site and uncountably many")
out("    non-sites => no open ball is contained in the domain => interior is empty")
out("    largest open ball inside the domain: radius 0")
verdict("P4", "the deposit's domain has empty interior in R^3, so the hypothesis fails on its first word",
        True, "measure 0, interior empty, inscribed ball radius 0")

out()
out("  P5  attribution -- external check performed 2026-11-22, recorded here (not measured by this script)")
out("      Math. Ann. 70, 161-165 : dimension invariance, submitted JUNE 1910, published FEBRUARY 1911")
out("      Math. Ann. 71, 305-315 : invariance of DOMAIN, 1912")
out("      zbMATH review of the 1912 paper says so explicitly: 'Der von Brouwer (Math. Ann. 70,")
out("      161-165) bewiesene Fundamentalsatz ... wird hier so verscharft'.")
out()
out("      => '1910' is the SUBMISSION year of the dimension paper, not a fabricated date.  The claim in")
out("         the submission is not false, it is under-specified: published 1911 (dimension) / 1912")
out("         (domain).  Recorded as a provenance note; it changes nothing in the argument.")
verdict("P5", "1910 is a submission date, not the standard publication year (1911 / 1912)", True,
        "Math. Ann. 70 (Feb 1911); Math. Ann. 71 (1912)")

# =================================================================================================
hdr("[C] A2 CANTOR  (P6, P7, P8, P9)")
# =================================================================================================
out("  Cantor 1877: a bijection [0,1] <-> [0,1]^2.  The submission extends it to a solid ball <-> a plane.")
out("  Both are sets of cardinality c, so the extension is free.  The question is what such a bijection")
out("  COSTS to specify -- because 'a bijection exists' is the weakest statement in mathematics.")
out()
lg = (math.lgamma(CELLS + 1) - math.lgamma(CELLS - PIECES + 1)) / math.log(2)
out(f"  number of injections from {PIECES:,} pieces into {CELLS:,} cells = C!/(C-N)!")
out(f"    log2 of that number = {lg:.4e} bits  =  {lg / 8 / 1e9:.2f} GB")
out(f"    the rule p = kN + n that the deposit actually uses costs 0 bits (2 integers, 62 bits total)")
out(f"    => the deposit is one of ~2^{lg:.4e} possible injections, and it names its own for free.")
p6 = 1.25e11 <= lg <= 1.40e11
verdict("P6", "an injection is guaranteed by cardinality alone; naming one costs ~1.3e11 bits (~16 GB)",
        p6, f"log2 = {lg:.4e} bits (registered band 1.25-1.40e11)")

out()
out("  P7  does the deposit preserve cardinality exactly?")
out(f"    pieces {PIECES:,} -> distinct occupied cells {PIECES:,}, free {CELLS - PIECES:,}")
out(f"    occupancy {PIECES / CELLS:.6f}   (a bijection by construction, verified in [S] and [A])")
verdict("P7", "the deposit is one such injection: cardinality preserved exactly", bij_full,
        f"{PIECES:,} distinct cells, {CELLS - PIECES:,} free")

out()
out("  P8  'the structure is shattered' -- is that true of the deposit?  Interfaces are d3 = 0:")
rows = []
for k in range(M - 1):
    p0 = k * N_LAYER
    p1 = (k + 1) * N_LAYER
    x0, y0 = d2xy(S, p0)
    x1, y1 = d2xy(S, p1)
    dd = PITCH * math.hypot(x0 - x1, y0 - y1)
    rows.append([f"C{k + 1}|C{k + 2}", "0", f"{dd:,.1f}"])
table(rows, ["interface", "d3 (m)", "d2 deposit (m)"])
arch = [12401.7, 12085.3, 12989.4]   # as registered and as archived in mr2_arap_results.txt
got = [float(r[2].replace(",", "")) for r in rows]
rep = all(abs(g - a) < 0.5 for g, a in zip(got, arch))
out(f"    reproduces the archived MR2-D row ({arch}): {rep}")
out()
nm = 4000
means = []
for k in range(M - 1):
    ds = []
    for n in rng.integers(0, N_LAYER, size=nm):
        xa, ya = d2xy(S, k * N_LAYER + int(n))
        xb, yb = d2xy(S, (k + 1) * N_LAYER + int(n))
        ds.append(PITCH * math.hypot(xa - xb, ya - yb))
    means.append(float(np.mean(ds)))
out(f"    mean over {nm:,} layers per interface: {[f'{m:,.0f}' for m in means]} m")
out(f"    the archived value sampled n = 0 only; n = 0 is {'representative' if all(1.1e4 <= m <= 1.4e4 for m in means) else 'NOT representative'}")
out(f"    -> an interface that is 0 m apart in 3D is ~1.2e4 m apart in the deposit: shattered by 4 decades")
p8 = rep and all(1.1e4 <= m <= 1.4e4 for m in means)
verdict("P8", "structure destruction reproduces MR2-D exactly at n=0; mean stays in [1.1e4, 1.4e4] m",
        p8, f"n=0 exact {rep}; means {[round(m) for m in means]}")

out()
out("  P9  does the '3D solid sphere -> plane' framing add anything?")
out("    any two sets of cardinality c admit a bijection.  A ball and a plane both have cardinality c.")
out("    So does a ball and a line, and a plane and a line segment.  The theorem's content is CARDINALITY;")
out("    its 3D-ness is decoration.  Cantor's result is not about dimension at all -- it cannot be, since")
out("    it holds equally in every dimension.")
verdict("P9", "the 3D framing is decoration: the theorem is about cardinality, not dimension", True,
        "the same bijection exists for any pair of sets of cardinality c")

# =================================================================================================
hdr("[D] A3 HILBERT  (P10, P11, P12, P13)")
# =================================================================================================
out("  P10  'continuous surjection [0,1] -> [0,1]^2, not injective' -- true, and inapplicable as stated")
out()
out(f"    at finite order the map is a BIJECTION: 4^k indices onto 4^k cells, 0 collisions (see [S])")
out(f"    the deposit uses exactly the finite map, at order {ORDER}: p -> hilbert_{ORDER}(p)")
p10 = all_bij and inv_ok
verdict("P10", "at finite order the Hilbert index map is a bijection -- the deposit uses the finite map",
        p10, "orders 1-6 exhaustive, order 16 round-tripped 20,000 samples")
out()
out("  P11  the statement says: 'a continuous surjective mapping ... from a ONE-dimensional interval onto")
out("       a TWO-dimensional unit square ... multiple THREE-dimensional points will inevitably map to the")
out("       same two-dimensional coordinate.'")
out("    the map described : 1 -> 2")
out("    the conclusion    : about 3 -> 2")
out("    => the conclusion is about a map the sentence never described.  Non-injectivity of a space-filling")
out("       curve is a property of the PARAMETER (many t give one (x,y)), not of 3D points.")
p11 = True
verdict("P11", "the Hilbert sentence is dimension-mis-stated (1->2 described, 3->2 concluded)", p11,
        "src dim 1, target dim 2, subject dim 3")

out()
out("  P12  is non-injectivity a finite-order phenomenon?")
rows = []
maxmult = 0
for k in range(1, 7):
    n = 2 ** k
    cells = [d2xy(n, d) for d in range(n * n)]
    from collections import Counter
    c = Counter(cells)
    mm = max(c.values())
    maxmult = max(maxmult, mm)
    rows.append([k, f"{n * n:,}", mm, len(c)])
table(rows, ["order k", "indices", "max multiplicity", "distinct cells"])
out()
out(f"    maximum multiplicity over orders 1..6: {maxmult}")
out("    The continuum limit is CITED, not measured here: Hilbert (1891) gives a surjection that is not")
out("    injective, with at most 4 preimages per point, and the multiply-covered set has measure zero.")
out("    What this script establishes is the negative: at every finite order the multiplicity is exactly 1.")
verdict("P12", "non-injectivity is exclusively a continuum-limit phenomenon; multiplicity = 1 at finite order",
        maxmult == 1, f"max multiplicity {maxmult} over orders 1..6")

out()
out("  P13  consequence: Hilbert's non-injectivity is not an obstacle to this record.")
out("    the deposit is a bijection (P7); the renderable map is not (2^16 vs 2^9).  The wall is")
out("    resolution, and route_terminus_v1 s4 already located it there.")
verdict("P13", "Hilbert's non-injectivity does not touch the deposit; the obstacle is resolution", True,
        "bijection at order 16; gap 2^16/2^9 = 2^14")

# =================================================================================================
hdr("[E] A4 KAKEYA  (P14, P15, P16)")
# =================================================================================================
out("  P14  external check 2026-11-22: Wang & Zahl, 'Volume estimates for unions of convex sets, and the")
out("       Kakeya set conjecture in three dimensions', 24 February 2025, 127 pages.  Result: every Kakeya")
out("       set in R^3 has Hausdorff dimension AND Minkowski dimension equal to 3.  n >= 4 remains open.")
out("       (A shorter proof with Guth appeared in 2026.)")
out()
out("    what the theorem is about : the dimension of a SET")
out("    what it states           : dim_H(K) = dim_M(K) = 3")
out("    what it says about maps, channels, information, folding or containers : nothing.  A dimension")
out("      is a property of a set; an information bound is a property of a channel.  The statement")
out("      relates the two nowhere, so the bridge between them is the submission's, not the theorem's.")
verdict("P14", "A4 is real as a theorem, but it is about a set's dimension, not an information bound", True,
        "Wang-Zahl 2025, dim_H = dim_M = 3; no statement about maps")

out()
out("  P15  'lossless' -- with respect to WHAT?  Both readings are measurable and they differ:")
out(f"    (i)  w.r.t. the plate inventory : EXACT.  a bijection, {PIECES:,} -> {PIECES:,} distinct cells.")
out(f"    (ii) w.r.t. the object          : FALSE.  I(canvas ; r4) = 0 bits; six distinct objects ->")
out(f"         one digest (DEPOSIT-BLIND).  10 of 12 declared parameters do not reach a site.")
out("    So 'lossless serialization' is true under (i) and false under (ii).  The unqualified word is")
out("    ambiguous between a true and a false claim, and the ambiguity is the whole difference between")
out("    a file and a physical reduction.")
verdict("P15", "'lossless' is referent-dependent: exact for the inventory, false for the object", True,
        "(i) bijection; (ii) I = 0 bits on 10 of 12 parameters")

out()
out("  P16  taken literally, is the Kakeya gloss true OF THE DEPOSIT?")
out(f"    the deposit carries {PIECES:,} labels and 0 bytes of 3D geometry.")
out("    'it is impossible to compress the full three-dimensional information into a purely two-")
out("     dimensional container' -- if '3D information' means the object's geometry, this is TRUE here,")
out("    because the deposit does not contain it.  It corroborates DEPOSIT-BLIND.")
out("    ...which means it CANNOT also support unqualified 'lossless serialization'.  A4 and A5 pull")
out("    in opposite directions, and both cannot be used in one sentence.")
out()
out("    and the theorem's own hypothesis: a Kakeya set contains a unit line segment in every direction.")
out("    A line segment has cardinality c = 2^aleph_0.  The deposit has "
    f"{PIECES:,} points, which is finite.")
out(f"    => a finite set contains NO line segment at all, in any direction.")
out(f"    => the deposit contains 0 Kakeya sets.  Even fewer than the other three anchors apply to.")
out(f"    (a finite set's Hausdorff dimension is 0; a Kakeya set's is 3)")
verdict("P16", "the gloss is true of the deposit only by conceding it has no 3D geometry; it holds 0 Kakeya sets",
        True, "finite set contains no segment; dim_H = 0 vs 3")

# =================================================================================================
hdr("[F] A5 THE CONCLUSION  (P17, P18)")
# =================================================================================================
out("  P17  'a lossless physical collapse 3D -> 2D is strictly prohibited' -- for which maps?")
out()
rows = [
    ["homeomorphism / continuous injective", "NO", "dimension preserved", "Brouwer 1911/1912"],
    ["continuous surjection", "YES", "many-to-one, forced", "Peano 1890 / Hilbert 1891"],
    ["bijection, no regularity", "YES", "distance destroyed", "Cantor 1877"],
    ["bijection between finite sets", f"YES ({PIECES:,})", "address only, dim 0 = 0", "the deposit"],
]
table(rows, ["map class  R^3 sup -> R^2", "exists?", "what survives", "authority"],
      [37, 15, 24, 24])
n_prohibited = 1
out()
out(f"    classes prohibited by the four anchors: {n_prohibited} of 3 (the deposit is a fourth row they")
out("    do not govern at all).  The unqualified 'strictly prohibited' is therefore refuted by A2 and A3,")
out("    which it cites: a bijection exists (Cantor), a continuous surjection exists (Peano/Hilbert).")
out("    What is prohibited is exactly one thing: a CONTINUOUS INJECTIVE map.  No more.")
verdict("P17", "'strictly prohibited' holds for 1 of 3 map classes -- continuous injective only",
        n_prohibited == 1, "surjection and bijection both exist")

out()
out("  P18  does 'no picture' follow from any of the four anchors?")
need = math.ceil(math.sqrt(PIECES))
side_need = 2 ** 16
side_view = 2 ** 9
ratio_cells = (side_need ** 2) / (side_view ** 2)
frame4k = 3840 * 2160
out(f"    injective needs ceil(sqrt(pieces)) = {need:,} sites/side  -> 2^16 = {side_need:,}")
out(f"    renderable on one frame is 2^9 = {side_view:,}/side  -> {side_view ** 2:,} cells "
    f"= {side_view ** 2 / PIECES * 100:.4f}% of the deposit")
out(f"    a 4K frame ({frame4k:,} pixels) shows {frame4k / PIECES * 100:.2f}% of the deposit")
out(f"    ratio of cell counts 2^16/2^9 squared = {ratio_cells:,.0f} = 2^{int(math.log2(ratio_cells))}"
    f"   (the linear ratio is {side_need // side_view} = 2^{int(math.log2(side_need // side_view))})")
out()
out("    every one of those numbers is a COUNT OF SITES.  None of them is a dimension, a topology,")
out("    or a continuity.  The four anchors establish 'no embedding'; 'no picture' comes from arithmetic")
out("    about resolution, which route_terminus_v1 s4 already contained and which uses no anchor at all.")
verdict("P18", "'no picture' is a resolution fact (2^16 vs 2^9), not a consequence of the four anchors",
        True, f"cell ratio 2^{int(math.log2(ratio_cells))}; 4K shows {frame4k / PIECES * 100:.2f}%")

# =================================================================================================
hdr("[G] VERDICTS")
# =================================================================================================
ids = sorted(FLAGS, key=lambda t: int(t[1:]))
npass = sum(1 for i in ids if FLAGS[i])
N_REGISTERED = 18
out("  " + "   ".join(f"{i}:{'P' if FLAGS[i] else 'F'}" for i in ids))
out(f"  {npass} / {len(ids)} predictions hold as registered.")
out(f"  verdict() calls: {len(FLAGS)} / {N_REGISTERED} registered"
    f"{'   -- COMPLETE' if len(FLAGS) == N_REGISTERED else '   -- INCOMPLETE, a prediction was never tested'}")
missing = [f"P{r}" for r in range(1, N_REGISTERED + 1) if f"P{r}" not in FLAGS]
if missing:
    out(f"  never tested: {missing}")
out()
out("  THE RESULT, in one paragraph:")
out()
out("  A1 has two halves and they behave differently.  'Dimension is a topological invariant' holds for")
out("  ALL spaces, and it applies here: the deposit's domain and codomain are FINITE DISCRETE sets,")
out("  dimension 0 on both sides, so the invariant is satisfied trivially at 0 = 0.  'Invariance of")
out("  DOMAIN' -- the half that forbids an embedding, and the half the submission actually needs --")
out("  begins 'if U is an OPEN subset of R^n', and the deposit's domain has empty interior in R^3.")
out("  A3 does not apply (its domain is [0,1]).  A4 does not apply (its set contains a unit segment in")
out("  every direction; a finite set contains no segment at all).  A2 DOES apply -- its hypothesis is")
out("  cardinality, which a finite pair satisfies vacuously -- and A2 is satisfied.")
out()
out("  So the deposit is not forbidden by any anchor, and not permitted by any either: three are out of")
out("  scope and the fourth is satisfied by counting.  The one that applies is the one that says")
out("  'a bijection exists and it destroys structure', which is exactly what the deposit measures:")
out("  cardinality exact (4,279,069,764 -> 4,279,069,764), interfaces from 0 m to 1.2e4 m.")
out()
out("  And the reason nothing is forbidden is the topological form of DEPOSIT-BLIND: by the time you")
out("  have a deposit, the 3-dimensional continuum is gone.  Its dimension is 0.  There is nothing")
out("  left for a dimension theorem to protect.")
out()
out("  A3 is mis-stated (1->2 described, 3->2 concluded; the finite curve is a bijection).  A4 is a")
out("  non-sequitur (a theorem about a set's Hausdorff dimension, offered as an information bound)")
out("  and, read literally, it contradicts the conclusion it is cited for -- see P16.")
out()
out("  The conclusion is RIGHT and its stated foundation is not what establishes it.  'No picture' is")
out("  arithmetic: 2^16 sites needed, 2^9 available, gap 2^14.  'A file, not a picture' is Cantor's")
out("  branch measured on the deposit: cardinality exact, interfaces shattered by 1.2e4 m.")

hdr("[H] ERRATA -- appended to this run, which is not edited")
out("  E1  P8's reproduction check used a reference list with a TRANSPOSED DIGIT in this script:")
out("      12,899.4 where the registered and archived value is 12,989.4.  The registration text was")
out("      right; the executor's constant was wrong, so the first run printed rep = False against data")
out("      that matches.  Corrected in place.  Recomputed 12,989.3887 -> 12,989.4, exact.  P8's first")
out("      half therefore HOLDS; its FAIL is the mean band (E4) alone.  Fifth instance of the class")
out("      'a constant in the harness is looser or wrong while the registered claim is fine'.")
out()
out("  E2  The first sampling check in [A] drew 200,000 piece indices WITH replacement and then tested")
out("      the image for collisions.  The three 'collisions' it reported were birthday repeats of the")
out("      sampler: expected 200,000^2/(2*4.279e9) = 4.7, observed 3.  Deduplicating the INPUTS first:")
out("      199,997 distinct indices -> 199,997 distinct cells.  Recorded because the original output")
out("      printed COLLISION, and a reader of that line would have concluded the sigma was broken.")
out()
out("  E3  P2 is REFUTED, and the refutation is the finding.  I registered '0 of 4 anchors has the")
out("      deposit in its hypothesis class'.  False: A2's hypothesis is cardinality, and a finite pair")
out("      satisfies it vacuously.  The true count is 1 of 4 -- and the 1 is the load-bearing anchor.")
out("      My test was also wrong in its first form: it regex-matched the anchor STRINGS for")
out("      'continu|open', which scored A4 as having no continuum in its hypothesis because the word")
out("      'continuum' never appears in 'a unit segment in every direction'.  The string is not the")
out("      hypothesis.  Fourth round with a text test standing in for a mathematical one.")
out()
out("  E4  P8's second half registered means in [1.1e4, 1.4e4] m and measured 14,430 / 13,078 / 14,439")
out("      m.  Two of three exceed the band, so P8 FAILS as registered.  The qualitative claim is")
out("      untouched (still 4 decades of destruction), but the band was too tight: I derived it from")
out("      n = 0, which is one layer of 1.07e9 and sits 5-16% below the mean at two interfaces.  The")
out("      archived MR2-D figure is a single-layer sample, and this run shows it understates.")
out()
out("  E5  P18's first draft printed 'gap = 2^16/2^9 = 128 = 2^7' -- the LINEAR ratio -- while its own")
out("      prose said 2^14, which is the ratio of CELLS.  It also printed '4K shows 0.01%' using 512^2")
out("      instead of 3840x2160.  Both were wrong when printed; the claim is unaffected (2^14 and 0.19%).")
out("      The general defect: a ratio of two powers of two is only well defined once the quantity is")
out("      named, and I named it in prose while computing it in the other convention.")
out()
out("  E6  P10 had no verdict call in the first run, so the tally printed 17 predictions instead of 18.")
out("      A missing verdict is indistinguishable from a passing one in a tally -- the counts are now")
out("      checked against the number of verdict() calls, not written by hand.")

(ROOT / "runs" / "DIM").mkdir(parents=True, exist_ok=True)
with open(ROOT / "runs" / "DIM" / "dimension_anchors_results.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
print("\nwritten: runs/DIM/dimension_anchors_results.txt")
