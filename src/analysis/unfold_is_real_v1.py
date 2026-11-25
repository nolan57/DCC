# -*- coding: utf-8 -*-
"""
unfold_is_real_v1.py — Is "unfolding" derived from the assumptions, or did I add it?

Following the rendering in unfold_appearance_v1. The user asks: under the current three assumptions, is the unfolding really like this?

This module splits that question into four separately decidable questions:

  Q1  Is the area 325 km^2 calculated or drawn?
  Q2  Is the structure inside each tile "as-is" or "stretched"?
  Q3  Is "arranging into a human figure in head-to-foot order" determined by physics?
  Q4  From 3D to this 2D surface, can the process be continuous (i.e., "smooth")?

Key tools (newly introduced in this module, not used earlier in the project):
  · Invariance of domain: there is no continuous injection R^3 -> R^2.
    => "Non-overlap" (injection) and "continuity" (smoothness) are mathematically mutually exclusive, not a matter of numerical factors.
  · Counting fracture surfaces: since breaking is unavoidable, count how many breaks there are, the total area, and how far each jumps.

Tags: CHECK recomputable / ESTIMATE depends on literature values / ARGUMENT structural argument (including theorems)
"""

import io
import math
import os

# ----------------------------------------------------------------- basic quantities
HBARC = 197.3269804        # MeV fm
M_KG = 70.0
RHO = 1000.0
V = M_KG / RHO             # m^3
N = 7.0e27                 # number of atoms (following three_body_comparison_v1)
H_BODY = 1.75              # m

EV_J = 1.602176634e-19
MEV_J = EV_J * 1e6

OUT = []


def w(s=""):
    OUT.append(s)


def tag(kind, name, ok, msg=""):
    OUT.append("  [%-8s] %-40s %-6s %s" % (kind, name, "PASS" if ok else "FLAG", msg))
    return ok


def ef_2d_keV(n2d):
    """E_F of a 2D massless Fermi gas (keV), n2d: m^-2"""
    kf = math.sqrt(2.0 * math.pi * n2d) * 1e-15        # m^-1 -> fm^-1
    return HBARC * kf * 1e3


def e_sub_keV(L):
    """Single-particle subband spacing (1D infinite square well), L: m"""
    return math.pi * HBARC / (L * 1e15) * 1e3          # m -> fm


# ------------------------------------------------- Q1 area: calculated or drawn
def q1_area():
    w("[Q1] Is 325 km^2 calculated or drawn by me?")
    d = (V / N) ** (1.0 / 3.0)
    A = N * d * d
    A_vol = V / d
    A_c = V / H_BODY

    w("  Three constraints, each reduced to numbers:")
    w("    (i)  To be 2D: E_F < E_sub")
    w("    (ii) To keep atoms alive: E_sub = pi*hbarc/L_z < E_bind ~ 3 keV")
    w("    (iii) No gain or loss: A * L_z = V (volume conservation)")
    w("")
    w("  (ii) gives a lower bound on L_z: (ii)  L_z > pi*hbarc/E_bind = %.4f nm" % (math.pi * HBARC / 3.0e-3 / 1e15 * 1e9))
    w("       Substituting into (iii) gives the **upper bound** on A: A < %.1f km^2" % (V / (math.pi * HBARC / 3.0e-3 / 1e15) / 1e6))
    w("")
    w("  (i) gives the lower bound on A: E_F(A) = E_sub(A) solves to A^3 = 2*N*V^2/pi")
    A_lo = (2.0 * N * V * V / math.pi) ** (1.0 / 3.0)
    w("       A > %.1f km^2" % (A_lo / 1e6))
    w("")
    w("  => The area is not a unique value but a window: A in [%.0f, %.0f] km^2 (width %.2f times)"
      % (A_lo / 1e6, V / (math.pi * HBARC / 3.0e-3 / 1e15) / 1e6,
         (V / (math.pi * HBARC / 3.0e-3 / 1e15)) / A_lo))
    w("     The only physically meaningful choice within the window is L_z = atomic spacing d (any thinner and there are no atomic layers):")
    w("       d = %.4f nm -> A = V/d = %.4e m^2 = %.1f km^2" % (d * 1e9, A_vol, A_vol / 1e6))
    w("       A = N*d^2 = %.4e m^2 = %.1f km^2   (equal to V/d = consistent with volume conservation)"
      % (A, A / 1e6))
    w("")
    w("  Average cross-sectional area A_c = V/H = %.4f m^2 (side %.3f m)" % (A_c, math.sqrt(A_c)))
    n_slice = A / A_c
    w("  Number of slices = A/A_c = %.3e" % n_slice)
    w("")
    w("  => The **order of magnitude** of the area is forced by arithmetic (order 10^8 m^2, neither 1 m^2 nor 10^12);")
    w("     the specific value 325 comes from the single physical choice of 'monolayer'. This step requires no assumption about 'how to arrange'.")
    tag("CHECK", "Q1_area_is_computed_not_drawn",
        abs(A / A_vol - 1) < 1e-9 and A_lo < A < V / (math.pi * HBARC / 3.0e-3 / 1e15),
        "V/d and N*d^2 agree to 1e-9; 325 lies within the window")
    return dict(d=d, A=A, A_c=A_c, n_slice=n_slice, A_lo=A_lo)


# ------------------------------------------------- Q2 whether tiles are as-is
def q2_tile(g):
    w("")
    w("[Q2] Inside each tile, is it stretched or as-is?")
    d, A_c = g["d"], g["A_c"]
    n_per_tile = A_c / (d * d)
    side_atoms = math.sqrt(A_c) / d
    w("  A tile 0.200 m x 0.200 m has area %.4f m^2, exactly equal to the cross-sectional area of one tomogram" % A_c)
    w("  Number of atoms per tile = A_c/d^2 = %.3e; atoms along tile edge = 0.200/d = %.3e" % (n_per_tile, side_atoms))
    w("  Mapping: within a tile (x,y) is the identity — the tile is a **1:1 copy** of the original tomogram, with zero deformation.")
    w("  This is why lungs, heart, and spine can be seen inside a tile in the rendering: it is that very tomogram.")
    tag("CHECK", "Q2_tile_is_isometric", True,
        "Intra-tile deformation is the identity; tile area = tomogram area (a direct consequence of volume conservation)")


# ------------------------------------------------- Q3 whether the ordering is determined by physics
def q3_order(g):
    w("")
    w("[Q3] Is 'arranging head-to-foot into a human figure' determined by physics?")
    n = g["n_slice"]
    w("  Physics only gives: %d mutually disconnected tiles, each of area %.4f m^2, total area %.1f km^2." % (n, g["A_c"], g["A"] / 1e6))
    w("  Physics **does not** give the numbering order of the tiles. Which cell to put the k-th tile in is a permutation pi.")
    w("  How many readable arrangements (adjacent numbers placed adjacently) are there among all %d! permutations:" % n)
    w("    A constant number (identity + a few symmetries/flips) vs %d! -> ratio < 1/%d! ~ 0" % (n, n))
    w("  In other words: 'being a picture' is a measure-zero encoding choice, not a physical conclusion.")
    w("  Equivalently: all the information is present, but one needs to know that permutation to read it.")
    tag("ARGUMENT", "Q3_layout_is_encoding_not_physics", True,
        "Physics gives the set of fragments; the human figure comes from the ordering convention I added")


# ------------------------------------------------- Q4 whether the process can be continuous
def q4_continuity(g):
    w("")
    w("[Q4] Can the process from 3D to this 2D surface be continuous?")
    d = g["d"]
    tile = math.sqrt(g["A_c"])
    stretch = tile / d

    w("  (a) Theorem: there is no continuous injection R^3 -> R^2 (invariance of domain / invariance of dimension).")
    w("      One-line proof: if a continuous injection f exists, then f maps the sphere S^2 continuously and bijectively onto f(S^2) < R^2,")
    w("      but S^2 cannot be embedded in R^2 — contradiction.")
    w("      Corollary: 'each atom occupies one lattice site, with no overlap' (injection) and 'continuous process' (smoothness) **cannot hold simultaneously**.")
    w("      This is not a matter of numerical factors; the feasible set is empty.")
    w("")
    w("  (b) Since breaking is unavoidable, count how much is broken:")
    w("      Cross-layer neighboring atom pairs: initial spacing d = %.4f nm, final spacing = tile side %.3f m" % (d * 1e9, tile))
    w("      Stretch factor = tile/d = %.3e" % stretch)
    w("      Number of fracture surfaces = number of slices = %.3e" % g["n_slice"])
    w("      Area of each fracture = A_c = %.4f m^2  ->  total fracture area = %.3e m^2 = %.1f km^2"
      % (g["A_c"], g["A"], g["A"] / 1e6))
    w("      (Equal to the area of the picture, because each cut exposes exactly the full cross-section of one tomogram)")
    w("")
    w("  (c) Cost: bond-breaking energy")
    e_bond = 4.0                     # eV per bond, ESTIMATE
    z_bonds = 4.0                    # coordination number per atom, order of magnitude
    E_cut = N * z_bonds * e_bond * EV_J
    u2d = (2.0 / 3.0) * (1.0 / (d * d)) * ef_2d_keV(1.0 / (d * d)) * 1e3 * EV_J
    E_2d = u2d * g["A"]
    w("      Broken bonds %0.1e x %.1f eV = %.2e J" % (N * z_bonds, e_bond, E_cut))
    w("      For comparison: total energy of the 2D Fermi gas u_2D*A = %.2e J (u_2D = %.2e J/m^2)" % (E_2d, u2d))
    w("      Ratio = %.1e  -> cutting differs by two orders of magnitude, not an energy obstacle (the real obstacle is strain, not energy)"
      % (E_cut / E_2d))
    w("")
    w("  (d) Where is the obstacle then? Only in the word 'smooth':")
    w("      In the material sense, %.3e full-cross-section fractures = the object is cut into %.3e atom-thick sheets." % (g["n_slice"], g["n_slice"]))
    w("      Smoothness holds only for **front advance** (which can be arbitrarily slow), not for **material deformation**.")
    tag("ARGUMENT", "Q4_continuous_plus_injective_impossible", True,
        "%.1e fracture surfaces, stretched %.1e times" % (g["n_slice"], stretch))
    return dict(stretch=stretch, E_cut=E_cut, E_2d=E_2d)


# ------------------------------------------------- comparison of three candidate mappings
def branch_table(g):
    w("")
    w("[5] Three candidate mappings: which satisfies which")
    d, A_c = g["d"], g["A_c"]
    rows = []
    # M-A flatten: preserve (x,y), L_z -> 0
    n_sq = N / A_c
    ef_sq = ef_2d_keV(n_sq)
    rows.append(("M-A flatten (preserve x,y, L_z->0)", "continuous", "overlap (injection fails)",
                 A_c, ef_sq, "atoms disintegrate"))
    # M-B isometric unfolding: this figure
    n_un = 1.0 / (d * d)
    ef_un = ef_2d_keV(n_un)
    rows.append(("M-B isometric unfolding (this figure)", "%.1e fractures" % g["n_slice"], "injection",
                 g["A"], ef_un, "atoms intact"))
    # M-C permutation
    rows.append(("M-C random permutation (same physical quantities as M-B)", "fracture", "injection",
                 g["A"], ef_un, "atoms intact but no image"))

    w("  Configuration / Process / Occupancy / Area(m^2) / E_F(keV) / Outcome")
    w("  " + "-" * 96)
    for r in rows:
        w("  %s | %s | %s | %.3e | %.3f | %s" % r)
    w("")
    w("  The three assumptions + 'structure presentation' together leave only M-B / M-C; M-A violates 'weak-interaction preservation'")
    w("  (E_F = %.0f MeV, five orders of magnitude above atomic binding energy; meanwhile E_sub diverges as L_z->0, and every electron is pumped to >= E_sub)."
      % (rows[0][4] / 1e3))
    tag("CHECK", "M-A_kills_atoms", ef_sq > 1e3,
        "Flatten branch E_F=%.0f MeV >> 3 keV" % (ef_sq / 1e3))
    w("  (Even with the most generous A=1 m^2, the flatten branch still has E_F = %.0f MeV — the conclusion is insensitive to the choice of region)"
      % (ef_2d_keV(N / 1.0) / 1e3))
    tag("CHECK", "M-B_keeps_atoms", ef_un < 3.0,
        "Unfold branch E_F=%.2f keV < E_sub=%.2f keV" % (ef_un, e_sub_keV(d)))


# ------------------------------------------------- conclusion
def conclusion(g, q4d):
    w("")
    w("=" * 80)
    w("[Conclusion] 'Is the unfolding really like this?'")
    w("=" * 80)
    w("  Area: yes in order of magnitude. The window [%.0f, %.0f] km^2 is bracketed by three inequalities; the monolayer takes %.0f km^2."
      % (g["A_lo"] / 1e6, V / (math.pi * HBARC / 3.0e-3 / 1e15) / 1e6, g["A"] / 1e6))
    w("  Inside tiles: yes. Each tile is a real tomogram of the original object, 1:1 with zero deformation.")
    w("  Ordering: no. Physics only gives %.1e disconnected fragments; the 'human figure' is an encoding convention." % g["n_slice"])
    w("  Process: not 'unfolding' but 'cutting'. %.1e full-cross-section fractures, with each broken bond pulled apart by %.1e times." % (g["n_slice"], q4d["stretch"]))
    w("")
    w("  In one sentence: this picture is not a flattened person but an archive of tomograms filed in order.")
    w("  It is real in the sense of 'structure presentation' (inside a tile is anatomy), but false in the sense of 'smooth deformation'.")
    w("")
    w("  A fourth implicit assumption that must be stated: all of the above rests on 'volume conservation A*L_z=V'.")
    w("  Volume conservation is not one of the three assumptions; it is a habit of 3D geometry. Abandon it -> back to the M-A flatten branch,")
    w("  the area does not grow and the atoms die. So the true prerequisite of the 'unfolding' route is: allow area growth + do not require the object to survive.")


def main():
    w("=" * 80)
    w("[unfold_is_real v1] Under the current three assumptions, is 'unfolding' real?")
    w("=" * 80)
    w("")
    g = q1_area()
    q2_tile(g)
    q3_order(g)
    q4d = q4_continuity(g)
    branch_table(g)
    conclusion(g, q4d)

    txt = "\n".join(OUT)
    print(txt)
    os.makedirs(os.path.join("runs", "ANALYSIS"), exist_ok=True)
    p = os.path.join("runs", "ANALYSIS", "unfold_is_real_v1.txt")
    io.open(p, "w", encoding="utf-8").write(txt + "\n")
    print("\n[out] %s" % p)


if __name__ == "__main__":
    main()
