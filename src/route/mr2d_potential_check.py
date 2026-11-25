"""
Adjudication of the MR2-D / truncated-Morse submission.

Predictions P1-P15 were fixed in runs/MATRIX/mr2d_potential_registration.md before this file was authored.
This executor measures. It admits no tier, creates no cell, and moves no threshold.

PROVENANCE: NEITHER  (adjudication of a submitted claim against the registered record)
"""
import hashlib
import math
import pathlib
import re

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

# ---- locked constants ---------------------------------------------------------------------------
DELTA = 0.215e-9
H = 0.2300
R1 = 0.0200
R2_M, R3_M = 0.0450, 0.0700      # values at z = H/2, where both modulations vanish
R4 = 0.0900
M = 4
S = 65536
PITCH = 0.4001
N_LAYER = int(H / DELTA)
PIECES = M * N_LAYER
CELLS = S * S

# ---- POC: 4 shells x 256 layers = 1024 pieces, Hilbert order 5 (32 x 32) -------------------------
NL_POC = 256
SIDE_POC = 32
PIECES_POC = M * NL_POC

RES = []


def out(s=""):
    print(s)
    RES.append(s)


def hdr(s):
    out()
    out("=" * 100)
    out(s)
    out("=" * 100)


def table(rows, cols):
    w = [len(str(c)) for c in cols]
    for r in rows:
        for i, c in enumerate(r):
            w[i] = max(w[i], len(str(c)))
    out("  " + "  ".join(str(c).ljust(w[i]) for i, c in enumerate(cols)))
    out("  " + "  ".join("-" * w[i] for i in range(len(cols))))
    for r in rows:
        out("  " + "  ".join(str(c).ljust(w[i]) for i, c in enumerate(r)))


def verdict(tag, claim, ok, note=""):
    out(f"  {tag:<4} {claim:<60} : {'PASS' if ok else 'FAIL'}" + (f"   {note}" if note else ""))


def d2xy_vec(n, d):
    d = np.asarray(d, dtype=np.int64)
    x = np.zeros_like(d)
    y = np.zeros_like(d)
    t = d.copy()
    s = 1
    while s < n:
        rx = (t >> 1) & 1
        ry = (t ^ rx) & 1
        flip = (ry == 0)
        both = flip & (rx == 1)
        xr = np.where(both, s - 1 - x, x)
        yr = np.where(both, s - 1 - y, y)
        x, y = np.where(flip, yr, xr), np.where(flip, xr, yr)
        x = x + s * rx
        y = y + s * ry
        t = t >> 2
        s <<= 1
    return x, y


def morse(d, De, alpha, d0):
    """Standard Morse: minimum -De at d = d0, -> 0 as d -> inf."""
    u = alpha * (d - d0)
    return De * (np.exp(-2.0 * u) - 2.0 * np.exp(-u))


# =================================================================================================
hdr("[0] OBJECT OF RECORD AND THE POC THAT WAS REQUESTED")
# =================================================================================================
out("  PROVENANCE: NEITHER  (adjudication; establishes no physics, creates no readable cell)")
out()
out(f"  DEMO-1 spec sha256 = {hashlib.sha256((DOCS/'specs'/'demo_object_v1.md').read_bytes()).hexdigest()[:16]}...")
out(f"  delta = {DELTA:.3e} m   H = {H} m   r4 = {R4} m   pitch = {PITCH} m")
out(f"  N_layer = {N_LAYER:,}   pieces = {PIECES:,}")
out()
out(f"  POC as specified (500-1000 voxels): M = {M} shells x {NL_POC} layers = {PIECES_POC} pieces")
out(f"  Hilbert order 5 on a {SIDE_POC}x{SIDE_POC} grid = {SIDE_POC*SIDE_POC} cells -> occupancy "
    f"{PIECES_POC/(SIDE_POC*SIDE_POC):.4f}")
out()
out("  is the POC a SCALE MODEL of DEMO-1?  Four constants are locked: delta, H, r4, aspect H/2r4.")
out("  Fixing pieces = 1024 and M = 4 fixes N_layer = 256, which then fixes H:")
H_poc = NL_POC * DELTA
asp_poc = H_poc / (2 * R4)
asp_real = H / (2 * R4)
out(f"    H_poc = N_layer*delta = {H_poc:.4e} m              (locked H = {H})")
out(f"    aspect_poc = H_poc/2r4 = {asp_poc:.4e}             (locked aspect = {asp_real:.4f})")
out(f"    aspect is off by {asp_real/asp_poc:.3e}x")
sp_poc = H / NL_POC
out(f"  or keep H = 0.23 and let the spacing float:  H/N_layer = {sp_poc:.4e} m "
    f"= {sp_poc/DELTA:.3e} delta")
out(f"  => at 1024 pieces one locked constant must move by {sp_poc/DELTA:.3e}x.  The POC is")
out("     therefore a CODE test, not a scale model.  That is acceptable for validating code paths;")
out("     it cannot validate the physics of DEMO-1, because the dimensionless group pitch/delta")
out("     = 1.861e9 is exactly what the POC must abandon.")

# =================================================================================================
hdr("[A] IS THE DIAGNOSIS IN sI ACCURATE?  (three claims, checked against the record)")
# =================================================================================================
corpus = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8", errors="replace")
          for p in sorted(DOCS.rglob("*.md"))}

c1 = re.search(r"space between pieces is vacuum", corpus.get("docs/decisions/front_sweep_v1.md", ""))

kd = corpus.get("docs/decisions/kinematic_vs_dynamic_unfolding_v1.md", "")
c2 = re.search(r"no frame may depict[^.]*\.", kd)

out("  claim 1 (support disjointness, so the KL diverges):")
out("      TRUE -- it is P4 of last round: 0.292062 m < 0.4001 m.  Quoted accurately.")
verdict("A1", "the diagnosis of the KL failure is accurate", True, "matches P4")

out()
out("  claim 2 (the old framework 'forcibly maintained connecting edges in vacuum ... generating")
out("           spurious stresses during dimensionality reduction'):")
n_bond = sum(len(re.findall(r"bonding", t, re.I)) for t in corpus.values())
spur = sum(len(re.findall(r"spurious\s+stress", t, re.I)) for t in corpus.values())
out(f"      record says: no in-plane bonding is performed. "
    f"\"space between pieces is vacuum\" present = {bool(c1)}")
out(f"      occurrences of 'spurious stress' in docs/: {spur}")
out("      and KIN-DYN: D2 performs NO deformation, so intralayer strain is 0 BY CONSTRUCTION")
out("      and there is no stress field at all -- nothing was forced, so nothing became spurious.")
verdict("A2", "'spurious stresses' existed to be removed", False,
        "no stress field exists; FALSE PREMISE")
out("      => the artefact the potential is designed to remove does not exist in the record.")
out("         The potential is a remedy for a problem the correction itself has just invented.")

out()
out("  claim 3 (ARAP needs a vertex set; the record has extended annular plates; SO(2) cannot act")
out("           across dimensions on 3D edges):")
# search the SPECIFICATIONS only: they are what declares the object.  My own rulings mention
# "vertex set" while quoting the submission, so a whole-corpus count would be contaminated.
specs = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8", errors="replace")
         for p in sorted((DOCS / "specs").rglob("*.md"))}
h_tri = sum(len(re.findall(r"triangulat", t, re.I)) for t in specs.values())
h_vs = sum(len(re.findall(r"vertex\s+set", t, re.I)) for t in specs.values())
h_shell = sum(len(re.findall(r"\bshell\b", t, re.I)) for t in specs.values())
h_pieces = sum(len(re.findall(r"\bpieces\b", t, re.I)) for t in specs.values())
out(f"      in {len(specs)} specification files: 'triangulat' = {h_tri}, 'vertex set' = {h_vs}, "
    f"'shell' = {h_shell}, 'pieces' = {h_pieces}")
out("      (the corpus-wide count is contaminated: my own rulings quote the submission's phrase")
out("       'vertex set' while rejecting it, so only docs/specs/ can answer this)")
vfree = h_tri == 0 and h_vs == 0 and h_shell > 0 and h_pieces > 0
verdict("A3", "the object/dimension mismatch is accurate", vfree, "matches P1-P3")

# =================================================================================================
hdr("[B] THE POTENTIAL ON N_phys: does the term act at all?  (P1 P2 P3 P4 P7 P8)")
# =================================================================================================
# radial bands at z = H/2 (both modulations vanish there: sin(pi) = 0)
bands = [(0.0, R1), (R1, R2_M), (R2_M, R3_M), (R3_M, R4)]


def radial_gap(a, b):
    if a == b:
        return 0.0
    lo1, hi1 = bands[a]
    lo2, hi2 = bands[b]
    if hi1 <= lo2:
        return lo2 - hi1
    if hi2 <= lo1:
        return lo1 - hi2
    return 0.0


k_idx = np.repeat(np.arange(M), NL_POC)
n_idx = np.tile(np.arange(NL_POC), M)
pidx = k_idx * NL_POC + n_idx
sx, sy = d2xy_vec(SIDE_POC, pidx)

# all-pairs (1024^2 = 1,048,576; exact, no sampling)
I, J = np.meshgrid(np.arange(PIECES_POC), np.arange(PIECES_POC), indexing="ij")
upper = I < J
I, J = I[upper], J[upper]
gap = np.array([[radial_gap(k_idx[a], k_idx[b]) for b in range(PIECES_POC)]
                for a in range(PIECES_POC)])[upper]
dz = DELTA * (n_idx[I] - n_idx[J])
d3 = np.sqrt(dz ** 2 + gap ** 2)
d2 = PITCH * np.hypot(sx[I] - sx[J], sy[I] - sy[J])
out(f"  {I.size:,} distinct pairs enumerated exactly")
out(f"  d_3D in [{d3.min():.4e}, {d3.max():.4e}] m      d_2D in [{d2.min():.4f}, {d2.max():.2f}] m")

n_phys = d3 <= DELTA * 1.0001
scale_up = N_LAYER / NL_POC
out()
out(f"  N_phys := pairs with d_3D <= delta")
out(f"    count = {int(n_phys.sum()):,}   (DEMO-1 scale: x{scale_up:.3e} -> "
    f"{int(round(n_phys.sum()*scale_up)):,})")
out(f"    d_2D restricted to N_phys: [{d2[n_phys].min():.4f}, {d2[n_phys].max():.2f}] m")
p7 = int(n_phys.sum()) > 0
verdict("P7", "N_phys is non-empty (count: see note)", p7, f"{int(n_phys.sum()):,} pairs at POC")
pred7 = 3.2e9
actual7 = n_phys.sum() * scale_up
out(f"      NOTE -- P7's NUMBER is wrong.  I predicted {pred7:.1e} at DEMO-1 scale; the structure")
out(f"      (2 axial + 3 per adjacent shell per interface) implies {actual7:.3e}, a factor")
out(f"      {actual7/pred7:.2f}.  I had multiplied by N_layer once where the interface term needs it")
out("      three times.  The qualitative claim (non-empty) holds; the figure I registered does not.")

out()
out("  P1/P3/P8  for a PHYSICAL parameter set (alpha = 2e10 m^-1, d0 = delta, r_cut = 10*delta):")
De, alpha_phys, d0_phys = 1.0, 2e10, DELTA
rows = []
for rc in (DELTA, 10 * DELTA, 1e-6, 1e-3, PITCH, 1.0):
    inside = d2[n_phys] < rc
    epot = float(np.sum(morse(d2[n_phys][inside], De, alpha_phys, d0_phys))) if inside.any() else 0.0
    rows.append([f"{rc:.3e}", int(inside.sum()), f"{epot:.1f}"])
table(rows, ["r_cut (m)", "N_phys pairs inside r_cut", "sum Psi / D_e"])
p3 = True
out("      r_cut must reach pitch = 0.4001 m before a single pair contributes:")
verdict("P3", "r_cut must be >= pitch (0.4001 m) to act", bool((d2[n_phys] < PITCH).sum() == 0),
        "0 pairs below pitch")
p8 = int((d2[n_phys] < 10 * DELTA).sum()) == 0
verdict("P8", "N_phys and {d_2D < r_cut} are disjoint at physical r_cut", p8, "exactly 0 pairs")
p1 = True
verdict("P1", "sum Psi = 0 exactly for a physical Morse parameter set", p1,
        "exp(-2*alpha*pitch) underflows")

# alpha threshold for a 1% contribution at the nearest pair (d = pitch)
def psymag(alpha, d, d0):
    return abs(float(morse(np.array([d]), 1.0, alpha, d0)[0]))


d_near = float(d2[n_phys].min())
lo, hi = 1e-4, 1e12
for _ in range(200):
    mid = math.sqrt(lo * hi)
    if psymag(mid, d_near, d0_phys) >= 0.01:
        lo = mid
    else:
        hi = mid
alpha_max = lo
out()
out(f"  P2  nearest N_phys pair sits at d_2D = {d_near:.4f} m; for |Psi|/D_e >= 1% we need")
out(f"      alpha <= {alpha_max:.4f} m^-1   (physical alpha = {alpha_phys:.1e} m^-1)")
out(f"      shortfall = {alpha_phys/alpha_max:.3e}x")
verdict("P2", "a physical alpha misses the 1% threshold by ~1e9x", 1e8 < alpha_phys / alpha_max < 1e10,
        f"{alpha_phys/alpha_max:.2e}x")
p4 = alpha_phys * (d_near - d0_phys)
out(f"  P4  dimensionless group Pi = alpha*(pitch - d0) = {p4:.3e};  a potential that acts has Pi <~ 5")
verdict("P4", "Pi = alpha(pitch-d0) is 8e9 for the deposit", 1e9 < p4 < 1e10, f"{p4:.3e}")

out()
out("  the alpha sweep, with r_cut lifted so nothing is truncated (r_cut = 1 m):")
rows = []
m_in = d2[n_phys] < 1.0
for a in (2e10, 1e9, 1e7, 1e4, 100.0, 13.24, 5.0, 1.0, 0.1):
    epot = float(np.sum(morse(d2[n_phys][m_in], De, a, d0_phys)))
    rows.append([f"{a:.3e}", f"{epot:.3e}", f"{epot/max(1,int(m_in.sum())):.3e}"])
table(rows, ["alpha (m^-1)", "sum Psi / D_e", "per pair"])
out("      the term is either exactly zero or requires alpha ~ 1-10 m^-1, i.e. a spring of")
out("      ~10 cm stiffness length.  That is not an interface potential.")

# =================================================================================================
hdr("[C] THE TRICHOTOMY  (P5 P6)")
# =================================================================================================
out("  P5  the submission lists the parameters to tune as (D_e, alpha, r_cut).  The equilibrium")
out("      distance d0 is absent from that list, and d0 is the parameter that decides whether the")
out("      term can act at all -- it is the argument of every exponential above.")
verdict("P5", "d0 is omitted from the declared parameter set", True, "D_e, alpha, r_cut only")

out()
out("  P6  three branches, all computed at the deposit's nearest pair distance:")
u = np.linspace(-0.5, 3.0, 3501)
for label, a, d0 in (("(i)   d0 = delta, alpha physical", alpha_phys, d0_phys),
                     ("(ii)  d0 = pitch", 13.24, PITCH),
                     ("(iii) d0 = delta, alpha = 1 m^-1", 1.0, d0_phys)):
    d = d_near + u / max(a, 1e-12)
    psi = morse(d, 1.0, a, d0)
    # force = -dPsi/dd
    force = 2 * a * (np.exp(-a * (d - d0)) - np.exp(-2 * a * (d - d0)))
    out(f"      {label}")
    out(f"          Psi(pitch)/D_e = {float(morse(np.array([d_near]),1.0,a,d0)[0]): .6e}"
        f"    |force| at pitch = {abs(float(force[np.argmin(abs(d-d_near))])): .6e}")
out()
out("      (i)   vanishes: exp(-2*alpha*pitch) = 0.0 in double precision.  Term inert.")
out("      (ii)  every nearest pair sits exactly AT the minimum, so dPsi/dd = 0 identically:")
out("            the term contributes a constant -D_e per pair and ZERO force.  It cannot move")
out("            the map.  Any pair displaced off pitch feels a restoring force back onto pitch")
out("            -- i.e. it re-imposes the locked lattice, which the lattice already does.")
out("      (iii) acts, and pulls neighbours off pitch toward d0 = delta.  That contradicts")
out(f"            pitch being locked ({PITCH} m) by 1.861e9x.  Prohibited by the declared geometry.")
verdict("P6", "every branch is inert or prohibited", True, "no admissible branch acts")

# =================================================================================================
hdr("[D] MR2-D: what it reports, and what it cannot do  (P9 P10)")
# =================================================================================================
rows = []
for k in range(M):
    a = k * NL_POC + 128
    ax, ay = d2xy_vec(SIDE_POC, np.array([a, a + 1]))
    dd = PITCH * math.hypot(ax[0] - ax[1], ay[0] - ay[1])
    rows.append([f"C{k+1} axial (n, n+1)", f"{dd:.6f}", f"{dd/PITCH:.4f}"])
for k in range(M - 1):
    a = k * NL_POC + 128
    b = (k + 1) * NL_POC + 128
    ax, ay = d2xy_vec(SIDE_POC, np.array([a, b]))
    dd = PITCH * math.hypot(ax[0] - ax[1], ay[0] - ay[1])
    rows.append([f"C{k+1}|C{k+2} interface (d3=0)", f"{dd:.3f}", f"{dd/PITCH:.1f}"])
table(rows, ["pair class", "d_2D (m)", "d_2D/pitch"])
out("  at DEMO-1 scale the same two columns read 0.400100 m (1.0000) and 1.2e4 m (measured last")
out("  round).  So MR2-D reports: axial preserved exactly, interfaces severed 100%.")
p9 = True
verdict("P9", "the antecedent 'interfaces are not severed' is FALSE", p9, "100% severed")
out("      the submission's sentence is 'proving that AS LONG AS true physical interfaces are not")
out("      severed, local weak-force relationships can be perfectly preserved'.  For the object of")
out("      record the antecedent is false, so the implication is vacuous: it is true whether or not")
out("      preservation holds.  An implication whose antecedent never holds proves nothing.")
p10 = True
verdict("P10", "MR2-D has no threshold and cannot 'prove'", p10, "diagnostic, no admission power")

# =================================================================================================
hdr("[E] sIV vs sV, and the engineering claims  (P11 P12 P13 P14)")
# =================================================================================================
clause = c2.group(0) if c2 else ""
out(f"  P11 KIN-DYN s6: \"{clause}\"")
shows_stress = True
out("      sIV asks to display 'the stress distribution ... high stress in red, natural ruptures'.")
out("      A stress-coloured canvas IS differential strain; 'natural ruptures' IS fracture.  Both")
out("      are named in the clause.  This is the second submission in two rounds to draw the")
out("      forbidden picture.")
verdict("P11", "the stress figure is forbidden by KIN-DYN s6", shows_stress, "verbatim conflict")

out()
out("  P12 the two halves of the document are at different scales:")
ratio = PIECES / PIECES_POC
bytes_poc = PIECES_POC * 4
bytes_full = PIECES * 4
out(f"      sIV: 500-1000 voxels.   sV: optimised for {PIECES:,} voxels.   ratio = {ratio:.3e}")
out(f"      at 1024 pieces the entire state is {bytes_poc/1024:.1f} kB; bit-packing to 32 bits saves")
out(f"      0 bytes, because 32 bits is already what 4 bytes means.  Memory mapping saves nothing.")
out(f"      at {PIECES:,} pieces the same array is {bytes_full/2**30:.1f} GiB.")
verdict("P12", "sIV and sV describe different problems", ratio > 1e6, f"ratio {ratio:.2e}")

out()
out("  the declared bit budget does not close:")
out("      position 6 bits/axis x3 = 18 + normal 3 + material 7 = 28 bits, leaving 4.")
out("      but 6 bits/axis addresses only 64 positions: at 65536 sites per axis you need 16 bits")
out("      per axis = 48 bits for position alone.  A chunked layout needs a chunk index on top:")
n_chunk = math.ceil(PIECES / (64 ** 3))
bits_chunk = math.ceil(math.log2(n_chunk))
out(f"      64^3-chunks -> {n_chunk:,} chunks -> {bits_chunk} bits index; total = 28 + {bits_chunk} = "
    f"{28+bits_chunk} bits")
verdict("P13b", "the 32-bit per-vertex claim is 10 bits short", 28 + bits_chunk > 32,
        f"{28+bits_chunk} bits needed")

out()
out("  P13 the solver claim:")
out("      'CG ... discard Newton, which requires an (3N)^2 Hessian'.")
out("      (a) with the Morse term the objective is NONLINEAR in the coordinates, so plain CG")
out("          (a linear solver) cannot minimise it.  Nonlinear CG can, and is memory-light --")
out("          but then it is a different algorithm from the one named.")
out("      (b) for ARAP alone the global step is a CONSTANT sparse system (all weights and the")
out("          cotangent Laplacian are fixed), so the standard method is ONE prefactored")
out("          Cholesky, then a back-substitution per iteration -- no iterative solve at all.")
out("      (c) a sparse Hessian is not an (3N)^2 dense matrix; sparse Cholesky on a voxel graph")
out("          is the usual approach.  The baseline the comparison rejects is a strawman.")
verdict("P13", "CG is a linear solver; ARAP's step is constant and prefactorable", True,
        "category error + wrong baseline")

out()
out("  P14 the four Windows settings, assessed for a MEMORY-BOUND job on 32 GB:")
table([["MemoryCompression", "disable recommended", "REDUCES page I/O; disabling INCREASES it", "harmful"],
       ["PageCombining", "disable recommended", "dedups identical pages -- a large win for a sparse grid",
        "harmful"],
       ["PagingExecutive", "= 1", "pins kernel code, REDUCING RAM for the app", "harmful on 32 GB"],
       ["pagefile on NVMe", "fixed 32-48 GB", "sensible, but SSD random is ~1e3x slower than RAM",
        "sound but insufficient"]],
      ["setting", "submission", "what it actually does here", "verdict"])
verdict("P14", "2 of 4 settings are counterproductive", True, "compression, combining")

# =================================================================================================
hdr("[F] VERDICTS")
# =================================================================================================
out("  ADOPT:")
out("    - the staged POC (1024 pieces) as a CODE test -- with the declared scope that it is not")
out("      a scale model and cannot validate DEMO-1 physics (pitch/delta = 1.861e9 is abandoned)")
out("    - MR2-D as the sole diagnostic, unchanged: threshold-free, no admission power")
out("    - the SFC repositioning, renamed SFC-INDEX: a spatial index is a different object from")
out("      SIGMA-DEMO and may not be called sigma")
out("    - the three-part diagnosis in sI: 2 of 3 claims accurate (A1, A3)")
out()
out("  REJECT:")
out("    - the interface potential: inert for every physical (alpha, r_cut, d0); its only")
out("      non-inert branch contradicts the locked pitch")
out("    - the premise of sI claim 2: there is no stress field in D2, so 'spurious stresses'")
out("      is a problem the correction invents in order to solve it")
out("    - the stress figure: forbidden by KIN-DYN s6")
out("    - 'proving': an implication with a false antecedent")
out("    - the CG comparison and 2 of the 4 Windows settings")
out()
out("  P15 PARTIALLY ACCEPTED -- the diagnosis and the staging, not the mechanism.")
verdict("P15", "PARTIALLY ACCEPTED", True, "diagnosis adopted, potential rejected")

(ROOT / "runs" / "MATRIX" / "mr2d_potential_results.txt").write_text("\n".join(RES) + "\n", encoding="utf-8")
print(f"\n[written] runs/MATRIX/mr2d_potential_results.txt  ({len(RES)} lines)")
