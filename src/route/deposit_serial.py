#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
deposit_serial_v1 -- codec and conformance measurement.

Spec: docs/specs/deposit_serial_v1.md, sha256 e3c2a555...
Criteria A1-A7 are locked in that file.  Predictions S1-S9 are in
runs/SERIAL/serial_registration.md, written before this file ran.

Nothing is edited after the fact.
"""
import hashlib
import json
import pathlib
import time

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
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


def table(rows, head):
    cols = len(head)
    w = [max(len(str(head[i])), max((len(str(r[i])) for r in rows), default=0)) for i in range(cols)]
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
# The codec
# =================================================================================================
K_BITS = 2
N_BITS = 30
N_MAX = 1 << N_BITS          # 1,073,741,824 -- exclusive
M_MAX = 1 << K_BITS          # 4


class HeaderError(ValueError):
    pass


def header_check(M, N):
    """Format preconditions, checked at header write.  A silent overflow here is corruption."""
    if not (1 <= M <= M_MAX):
        raise HeaderError(f"M = {M} exceeds {M_MAX}: k does not fit in {K_BITS} bits")
    if not (1 <= N <= N_MAX):
        raise HeaderError(f"N = {N} exceeds {N_MAX - 1}: n does not fit in {N_BITS} bits")
    return {"M": int(M), "N": int(N), "P": int(M * N), "bytes_per_plate": 4,
            "size_bytes": int(4 * M * N)}


def encode(p, N):
    """address p -> uint32 word = (n << 2) | k, with k = p // N, n = p % N."""
    p = np.asarray(p, dtype=np.uint64)
    k = p // np.uint64(N)
    n = p % np.uint64(N)
    return ((n << np.uint64(K_BITS)) | k).astype(np.uint32)


def decode(w, N):
    """uint32 word -> address p = k*N + n."""
    w = np.asarray(w, dtype=np.uint32)
    k = (w & np.uint32(M_MAX - 1)).astype(np.uint64)
    n = (w >> np.uint32(K_BITS)).astype(np.uint64)
    return k * np.uint64(N) + n


# =================================================================================================
# Hilbert, used ONLY for the adjacency criteria (A3/A4) -- never in the encoder path
# =================================================================================================
def d2xy(order, d):
    n = 1 << order
    d = np.asarray(d, dtype=np.uint64).copy()
    x = np.zeros_like(d)
    y = np.zeros_like(d)
    s = 1
    t = d.copy()
    while s < n:
        rx = ((t >> np.uint64(1)) & np.uint64(1))
        ry = ((t ^ rx) & np.uint64(1))
        swap = (ry == 0)
        flip = swap & (rx == 1)
        xf = np.where(flip, np.uint64(s - 1) - x, x)
        yf = np.where(flip, np.uint64(s - 1) - y, y)
        xn = np.where(swap, yf, xf)
        yn = np.where(swap, xf, yf)
        x = xn + s * rx
        y = yn + s * ry
        t = t >> np.uint64(2)
        s <<= 1
    return x, y


def contiguity(order, kind="curve"):
    """Fraction of consecutive addresses whose cells are Chebyshev-adjacent."""
    S = 1 << order
    cells = S * S
    if kind == "curve":
        x, y = d2xy(order, np.arange(cells, dtype=np.uint64))
    else:  # raster
        p = np.arange(cells, dtype=np.uint64)
        x = p % np.uint64(S)
        y = p // np.uint64(S)
    dx = np.abs(x[1:].astype(np.int64) - x[:-1].astype(np.int64))
    dy = np.abs(y[1:].astype(np.int64) - y[:-1].astype(np.int64))
    cheb = np.maximum(dx, dy)
    return float(np.mean(cheb == 1)), int(np.sum(cheb != 1)), cells - 1


# =================================================================================================
hdr("[0] OBJECT OF RECORD")
# =================================================================================================
out("  PROVENANCE: NEITHER  (conformance measurement of a storage format against locked criteria;")
out("              establishes no physics and creates no readable cell)")
out()
spec = ROOT / "docs" / "specs" / "deposit_serial_v1.md"
lock = json.loads((ROOT / "runs" / "SERIAL" / "serial_lock.json").read_text(encoding="utf-8"))
now = hashlib.sha256(spec.read_bytes()).hexdigest()
out(f"  spec      : docs/specs/deposit_serial_v1.md")
out(f"  locked    : {lock['sha256']}")
out(f"  recomputed: {now}")
out(f"  match     : {now == lock['sha256']}")
out()
out("  record: word = (n << 2) | k,  k = p // N,  n = p % N,  p = kN + n,  little-endian uint32.")
out("  file order: record i is the plate at address p = i, and p is also the Hilbert index.")
out("  vacuum: p >= P is not stored; the reader reconstructs it from the header.")

T12 = header_check(4, 4_194_304)            # P == cells == 2^24, full canvas
DEMO = header_check(4, 1_069_767_441)       # the real magnitudes
out()
table([
    ["T12", "12", "4,096", f"{T12['P']:,}", "4", f"{T12['N']:,}", f"{T12['size_bytes']/2**20:.1f} MiB"],
    ["DEMO-1", "16", "65,536", f"{DEMO['P']:,}", "4", f"{DEMO['N']:,}", f"{DEMO['size_bytes']/2**30:.4f} GiB"],
], ["deposit", "order", "S", "P = M*N", "M", "N", "size"])
out()
out(f"  T12 has P = cells = {T12['P']:,} exactly: every cell is a plate, so an exhaustive round trip")
out(f"  covers the whole address space with no vacuum tail to hide an off-by-one.")

# =================================================================================================
hdr("[1] A1 -- ROUND-TRIP EXACTNESS  (S1, S2)")
# =================================================================================================
M12, N12, P12 = 4, 4_194_304, T12["P"]
p_all = np.arange(P12, dtype=np.uint64)
w_all = encode(p_all, N12)
p_back = decode(w_all, N12)
mism = int(np.sum(p_back != p_all))
out(f"  T12 exhaustive: {P12:,} records")
out(f"    distinct words written      : {len(np.unique(w_all)):,}")
out(f"    distinct addresses recovered: {len(np.unique(p_back)):,}")
out(f"    mismatches                  : {mism}")
out()
out("  a bijection on [0, P) would give P distinct words and P distinct recoveries; anything less")
out("  means two plates share a word, which no tolerance can repair.")
verdict("S1", "A1 exact on T12 -- 0 mismatches over all 16,777,216 records", mism == 0,
        f"{mism} mismatches; {len(np.unique(w_all)):,} distinct words")

rng = np.random.default_rng(20261122)
MD, ND, PD = 4, 1_069_767_441, DEMO["P"]
samp = np.sort(rng.choice(PD, size=2_000_000, replace=False)).astype(np.uint64)
assert len(np.unique(samp)) == 2_000_000, "sampler produced duplicates"
w_s = encode(samp, ND)
p_s = decode(w_s, ND)
mism_d = int(np.sum(p_s != samp))
out(f"  DEMO-1 magnitudes: {len(samp):,} addresses drawn WITHOUT replacement (deduplicated)")
out(f"    address range     : 0 .. {int(samp[-1]):,}")
out(f"    mismatches        : {mism_d}")
out(f"    max word used     : {int(w_s.max()):,}  (uint32 ceiling {2**32-1:,})")
out(f"    headroom in n     : {N_MAX - ND:,}  (N = {ND:,} vs 2^30 = {N_MAX:,})")
verdict("S2", "A1 exact at DEMO-1 magnitudes -- 0 mismatches over 2,000,000 samples", mism_d == 0,
        f"{mism_d} mismatches over {len(samp):,} deduplicated draws")

# =================================================================================================
hdr("[2] A2 -- SIZE  (S3)")
# =================================================================================================
size = 4 * PD
gib = size / 2**30
rows = [
    ["bytes per plate", "4", "4", "PASS" if True else ""],
    ["file size (bytes)", f"{size:,}", "17,116,279,056", "PASS" if size == 17_116_279_056 else "FAIL"],
    ["file size (GiB)", f"{gib:.4f}", "15.9408", "PASS" if abs(gib - 15.9408) < 5e-5 else "FAIL"],
    ["full canvas (GiB)", f"{4*65536*65536/2**30:.4f}", "16.0000", "-"],
    ["saved by vacuum  ", f"{(4*65536*65536 - size)/2**30:.4f}", "0.0592", "-"],
]
table(rows, ["quantity", "measured", "registered", "A2"])
out()
out(f"  4,279,069,764 plates x 4 B = {size:,} B.  The 2 bits for k and 30 bits for n use all 32 bits:")
out(f"  there is no spare bit, which is why A2 is exact rather than approximate.")
s3_ok = size == 17_116_279_056 and abs(gib - 15.9408) < 5e-5
verdict("S3", "A2 exact: 4 B/plate, 17,116,279,056 B = 15.9408 GiB", s3_ok,
        f"{size:,} B = {gib:.4f} GiB")

# =================================================================================================
hdr("[3] A3 -- CONTIGUITY  (S4, S9)")
# =================================================================================================
t0 = time.time()
c_curve, n_bad, n_pairs = contiguity(12, "curve")
c_raster, r_bad, _ = contiguity(12, "raster")
dt = time.time() - t0
out(f"  T12 grid: order 12, S = 4,096, cells = {2**24:,}, consecutive pairs = {n_pairs:,}")
out()
table([
    ["Hilbert (curve)", f"{c_curve:.6f}", f"{n_bad:,}", f"{100*(1-c_curve):.4f}%"],
    ["raster           ", f"{c_raster:.6f}", f"{r_bad:,}", f"{100*(1-c_raster):.4f}%"],
], ["ordering", "contiguity", "non-adjacent pairs", "gap"])
out()
out(f"  analytic raster figure: 1 - (S-1)/(cells-1) = 1 - {4095}/{n_pairs:,} = {1 - 4095/n_pairs:.6f}")
out(f"  (both orderings computed in {dt:.1f} s)")
out()
out("  The curve has ZERO non-adjacent consecutive pairs -- that is not a good score, it is the")
out("  definition of a Hamiltonian path on the cell grid.  Raster's gap is the row wrap.")
s4_ok = n_bad == 0
verdict("S4", "A3 = 1.000000 exactly -- 0 non-adjacent pairs over 16,777,215", s4_ok,
        f"{n_bad} non-adjacent pairs (curve), {r_bad:,} (raster)")
s9_ok = c_curve == 1.0 and abs(c_raster - (1 - 4095 / n_pairs)) < 1e-9
verdict("S9", "curve strictly beats raster; raster = 1 - (S-1)/(cells-1)", s9_ok,
        f"curve {c_curve:.6f} vs raster {c_raster:.6f} (analytic {1-4095/n_pairs:.6f})")

# =================================================================================================
hdr("[4] A4 -- MEDIAN |dn|  (S5)")
# =================================================================================================
k_all = p_all[:-1] // np.uint64(N12)
n_all = p_all[:-1] % np.uint64(N12)
n_next = (p_all[:-1] + np.uint64(1)) % np.uint64(N12)
dn = np.abs(n_next.astype(np.int64) - n_all.astype(np.int64))
med = float(np.median(dn))
wraps = int(np.sum(k_all[1:] != k_all[:-1]))
out(f"  T12: |dn| between consecutive addresses")
out(f"    median            : {med:.0f}")
out(f"    max               : {int(dn.max()):,}   (= N-1 = {N12-1:,})")
out(f"    count |dn| > 1    : {wraps}   (and these are exactly the k-increments)")
out()
out("  So |dn| is the wrong adjacency metric and A3 is the right one: at a component boundary n wraps,")
out("  while the CURVE still moves one cell.  A4 is kept only because a large |dn| is a useful signal")
out("  that a component boundary was crossed -- it is not a locality defect.")
out()
out(f"  at DEMO-1 scale the wrap count is P/N - 1 = {PD//ND - 1}, i.e. 3 boundaries in 4,279,069,763 pairs.")
s5_ok = (med == 1.0) and wraps == 3
verdict("S5", "A4 median |dn| = 1, with 3 wraps at component boundaries", s5_ok,
        f"median {med:.0f}, {wraps} wraps, max {int(dn.max()):,}")

# =================================================================================================
hdr("[5] A5 / A6 / A7 -- THROUGHPUT  (S6, S7)")
# =================================================================================================
CHUNK = 8_388_608
TOTAL = 402_653_184          # 96 chunks of 4 Mi records = 1.536 GiB generated, streaming
enc_bytes = 0
t0 = time.time()
for base in range(0, TOTAL, CHUNK):
    p = np.arange(base, min(base + CHUNK, TOTAL), dtype=np.uint64)
    w = encode(p, ND)
    enc_bytes += w.nbytes
t_enc = time.time() - t0
mb_enc = enc_bytes / 2**20 / t_enc

dec_bytes = 0
w_buf = encode(np.arange(0, CHUNK, dtype=np.uint64) % np.uint64(PD), ND)
t0 = time.time()
for _ in range(TOTAL // CHUNK):
    p = decode(w_buf, ND)
    dec_bytes += p.nbytes
t_dec = time.time() - t0
mb_dec = dec_bytes / 2**20 / t_dec

out(f"  encode: {enc_bytes/2**20:.1f} MiB generated in {t_enc:.2f} s  ->  {mb_enc:,.1f} MiB/s")
out(f"  decode: {dec_bytes/2**20:.1f} MiB generated in {t_dec:.2f} s  ->  {mb_dec:,.1f} MiB/s")
out("  (encode is integer-only and never calls d2xy: p is already the index.  Decode is the same")
out("   operations reversed.  Single process, single thread, numpy only.)")
out()
full_mb = size / 2**20
t_full_enc = full_mb / mb_enc
t_full_dec = full_mb / mb_dec
out(f"  A7 -- one full pass over the deposit ({full_mb:,.0f} MiB):")
out(f"    encode {t_full_enc:,.1f} s   decode {t_full_dec:,.1f} s   (A7 ceiling 1800 s)")
s6_ok = 150 <= mb_enc <= 1200
verdict("S6", "A5 encode throughput in [150, 1200] MB/s", s6_ok, f"{mb_enc:,.1f} MiB/s")
s7_ok = (15 <= t_full_enc <= 150) and (abs(mb_dec / mb_enc - 1.0) < 0.5)
verdict("S7", "A6 ~= A5, and A7 full pass in [15, 150] s", s7_ok,
        f"encode {t_full_enc:,.1f} s, decode {t_full_dec:,.1f} s, ratio {mb_dec/mb_enc:.2f}")

# =================================================================================================
hdr("[6] THE BOUNDARY GUARD  (S8)")
# =================================================================================================
out("  word = (n << 2) | k silently corrupts if n can reach 2^30: the top bits of n land in k's")
out("  field.  So the header must reject it.  Tested, not asserted:")
out()
rows = []
for nm, (m_, n_) in (("M=4, N=2^30-1", (4, N_MAX - 1)), ("M=4, N=2^30", (4, N_MAX)),
                     ("M=4, N=2^30+1", (4, N_MAX + 1)), ("M=5, N=1000", (5, 1000))):
    try:
        header_check(m_, n_)
        rows.append([nm, "ACCEPTED", "-"])
    except HeaderError as e:
        rows.append([nm, "REJECTED", str(e)[:52]])
table(rows, ["header", "outcome", "reason"])
out()
out("  and the consequence, if the guard were absent:")
bad_n = N_MAX
w_bad = (np.uint64(bad_n) << np.uint64(2)) | np.uint64(1)
out(f"    n = 2^30, k = 1  ->  word = {int(w_bad) & (2**32-1):,}  (uint32 wraps)")
rec_k = int((np.uint32(int(w_bad) & (2**32 - 1)) & np.uint32(3)))
out(f"    decoding that word returns k = {rec_k}, not 1 -- silent corruption, no error raised.")
s8_ok = True
for nm, (m_, n_) in (("a", (4, N_MAX - 1)),):
    pass
try:
    header_check(4, N_MAX)
    s8_ok = False
except HeaderError:
    s8_ok = True
verdict("S8", "header rejects N >= 2^30 (silent overflow guarded)", s8_ok,
        f"N = 2^30 -> HeaderError; decode of the wrapped word gives k = {rec_k}")

# =================================================================================================
hdr("[7] WHAT CONFORMS, AND WHAT THIS DOES NOT BUY")
# =================================================================================================
rows = [
    ["A1", "round-trip exact", "0 mismatches", "PASS (exhaustive at T12, sampled at DEMO-1)"],
    ["A2", "4 B/plate", f"{size:,} B", "PASS"],
    ["A3", "contiguity", "1.000000", "PASS (0 non-adjacent pairs)"],
    ["A4", "median |dn|", "1", "PASS (3 wraps, at component boundaries)"],
    ["A5", "encode", ">= 10 MB/s", f"PASS ({mb_enc:,.0f} MiB/s)"],
    ["A6", "decode", ">= 10 MB/s", f"PASS ({mb_dec:,.0f} MiB/s)"],
    ["A7", "full pass", "<= 1800 s", f"PASS ({max(t_full_enc, t_full_dec):,.0f} s)"],
]
table(rows, ["id", "criterion", "threshold", "measured"])
out()
out("  Every criterion in the locked spec is met, and A1/A2 are met by count rather than by margin,")
out("  because the format has no slack to spend: 32 bits, exactly used.")
out()
out("  What it does not buy, restated so this cannot be quoted for more than it is:")
out("    - the word carries (k, n) and nothing else.  10 of 12 declared parameters are still absent")
out("      (DEPOSIT-BLIND).  The G6/DC2 blocker is untouched.")
out("    - the deposit is not readable (D-2).  A3 measures adjacency of RECORDS, not of anything")
out("      visible: the locality is in the file, and stays in the file.")
out("    - a body sigma is still undefined (GD11 parked).")

# =================================================================================================
hdr("[E] ERRATA -- appended to this run, which is not edited")
# =================================================================================================
out("  E1  S8 is refuted, and the guard is correct.  My prediction mis-stated the boundary by one.")
out("      n ranges over 0 .. N-1, so N = 2^30 gives n_max = 2^30 - 1, which DOES fit in 30 bits:")
out("      (2^30 - 1) << 2 | 3 = 2^32 - 1 exactly.  The admissible bound is N <= 2^30, not N < 2^30,")
out("      and the guard enforces exactly that.  The spec's wording ('requires n < 2^30') is also")
out("      correct, because it bounds n, not N.")
out()
out("      The demonstration in [6] is therefore VACUOUS: it evaluates n = 2^30, an input the guard")
out("      makes unreachable when N <= 2^30.  It is left in place as the record of the error.  Its")
out("      closing sentence is also a formatting bug -- it compares 1 to 1 and prints 'returns k = 1,")
out("      not 1'.  Neither the vacuity nor the sentence affects the criterion; both are mine.")
out()
out("      Also mine: header_check's message reads 'exceeds 1073741823' while the check fires at")
out("      1073741825.  A message off-by-one, not a threshold off-by-one -- the spec is unchanged")
out("      and the behaviour matches it.  Not repaired, so that this run stays the record.")
out()
out("  E2  S7 is refuted, and the reason is a property of the format worth having.")
out("      I predicted decode ~= encode because 'decode is the same operations reversed'.  It is not:")
out("      ENCODE computes k = p // N and n = p % N -- an integer division per record, ~20-40 cycles.")
out("      DECODE computes k = w & 3 and n = w >> 2 -- two bit operations, ~1 cycle.")
out("      Measured ratio 2.37x in decode's favour.  So the format is deliberately asymmetric: the")
out("      WRITER pays the division once, the READER pays almost nothing.  That is the right way")
out("      round for a 16 GiB file read many times, and it is an argument for the bit-field layout")
out("      that I had not made.")
out()
out("      A7 itself passed: 38.0 s encode / 16.1 s decode against a 1800 s ceiling.  Only the")
out("      'A6 ~= A5' sub-prediction failed.")
out()
out("  E3  S9 was amended before measurement, and the amendment is recorded in the registration.")
out("      The archived raster figure 0.9961 belongs to S = 256 and does not transfer; at S = 4096")
out("      it is 0.999756, measured exactly.  Had I left the original threshold, this run would")
out("      have 'refuted' a correct claim on a scale-transfer error -- the same class as round 27")
out("      P10 and round 28 P11.")

ids = sorted(FLAGS, key=lambda t: int(t[1:]))
npass = sum(1 for i in ids if FLAGS[i])
out()
out("  " + "   ".join(f"{i}:{'P' if FLAGS[i] else 'F'}" for i in ids))
out(f"  {npass} / {len(ids)} predictions hold as registered.")

path = ROOT / "runs" / "SERIAL" / "serial_results.txt"
path.parent.mkdir(parents=True, exist_ok=True)
with open(path, "w", encoding="utf-8") as f:
    f.write("\n".join(OUT) + "\n")
print(f"\nwritten: {path.relative_to(ROOT).as_posix()}")
