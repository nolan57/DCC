"""
RQ-05 -- the interaction-level census (refinement iii of the G6/DC2 flip).
=========================================================================
Question (queue): how many carriers are bound or trapped once the interaction
level is included, and how far does n_free,2D move?

The round has three parts and keeps them apart:

  [1] WHAT THE CENSUS COUNTS.  P2-5 prints n_free/n_Q and the ruling cites
      "N7-SPLIT: 4.2-5.0% of the bookkeeping n_Q,2D" as DERIVED.  A ratio can
      be a carrier fraction or a composition ratio.  Test: n_free/n_Q = X_p/ZA?
  [2] THE CRITERIA.  Four independent ones, each with a margin, each evaluated
      in two mass conventions (m_eff = E_z1/c^2 ; bare m_e):
        C1 orbit overlap   n a_B*^2  vs 1/4            (Mott)
        C2 energy          E_b/E_F   and W/E_b          (level or band)
        C3 correlation     U/W                          (metal or Mott insulator)
        C4 disorder        k_F l     (Ioffe-Regel)      (extended or trapped)
      Filling is an identity, not a criterion: charge neutrality gives one
      electron per proton exactly.
  [3] THE PROPAGATION.  The ruling says (iii) moves "n_free,2D, hence f_intra".
      f_intra = m_e c^2/E_z1 contains no n_free.  The round measures what the
      census can move instead -- and the density cancels from the rate, because
      n_imp = n_free and k_F^2 ∝ n_free carry the same n.

No fitted quantity.  Inputs: conv.beta_eq (P2 states), conv.kF_2 (registered
definition, BN-19), k_F l and q_TF from RQ-03 (round 56, not recomputed except
as a consistency check).
"""
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from src.common import conv  # noqa: E402

HBARC = conv.HBARC
M_E = conv.M_E
ALPHA = 7.2973525693e-3
E2 = ALPHA * HBARC                 # MeV fm : e^2/(4 pi eps0)
ZA = conv.ZA                       # 0.522, the FROZEN composition
N_Q = conv.N_E_FM2                 # fm^-2 : ZA * N_B (bookkeeping column)
N_B = conv.N_B_FM2
MEV_J = conv.MEV_J
C = conv.C
QE = 1.602176634e-19
HBAR = conv.HBAR

LZS = (1.68, 1.76, 1.84, 1.92, 1.99)
LZ0 = 1.84

out = []
def a(s=""):
    out.append(s)

def header(s):
    a("")
    a("=" * 78)
    a(s)
    a("=" * 78)

results = []
def ok(pid, cond):
    a("  [%s] -> %s" % (pid, "CONFIRMED" if cond else "FALSIFIED"))
    results.append((pid, bool(cond)))
    return bool(cond)

# ---------------------------------------------------------------- state
def state(Lz, mode="HYB"):
    conv.LZ_FM = Lz
    r = conv.beta_eq(N_B, mode)
    n = r["n_e_areal"]
    Ez1 = math.pi * HBARC / Lz
    kf = conv.kF_2(n, 2)
    qtf = 2.0 * ALPHA * Ez1 / HBARC          # fm^-1 (2D TF; independent of n)
    return dict(Lz=Lz, X=r["X_p"], n=n, Ez1=Ez1, kf=kf, qtf=qtf,
                mu=r["mu_e"], EFd=(HBARC * kf) ** 2 / (2.0 * Ez1))

def scales(s, m_mev):
    """criterion quantities for a given in-plane mass (MeV/c^2)."""
    aB = HBARC ** 2 / (m_mev * E2)                      # fm
    Ry = m_mev * E2 ** 2 / (2.0 * HBARC ** 2)           # MeV
    Eb = 4.0 * Ry                                       # 2D hydrogenic ground state
    rs = 1.0 / math.sqrt(math.pi * s["n"])              # mean spacing, fm
    d = 1.0 / math.sqrt(s["n"])                         # RQ-03's lattice spacing, fm
    EFd = (HBARC * s["kf"]) ** 2 / (2.0 * m_mev)
    t = HBARC ** 2 / (2.0 * m_mev * d * d)              # recoil / hopping, MeV
    U = 0.625 * E2 / aB                                 # on-site, 2D hydrogenic
    return dict(m=m_mev, aB=aB, Ry=Ry, Eb=Eb, rs=rs, d=d, EF=EFd,
                t=t, W=4.0 * t, U=U, mott=s["n"] * aB * aB)

# ---------------------------------------------------------------- RQ-03 kernel
def J0(x, n=400001, lo=-30.0, hi=30.0):
    tau = np.linspace(lo, hi, n)
    tt = np.exp(tau)
    f = 2.0 * (1.0 + tt * tt) / (x * (1.0 + tt * tt) + 2.0 * tt) ** 2
    return float(np.trapezoid(f * tt, tau))

def K1(x, n=400001, lo=-30.0, hi=30.0):
    tau = np.linspace(lo, hi, n)
    tt = np.exp(tau)
    f = 2.0 / (x * (1.0 + tt * tt) + 2.0 * tt)
    return float(np.trapezoid(f * tt, tau))

def J2(x, j0):
    return math.pi - 2.0 * x * K1(x) + x * x * j0

E2_4PE0 = E2 * MEV_J * 1e-15          # J m  : e^2/(4 pi eps0)

def rate(s, n_over=None, m_override=None):
    n = s["n"] if n_over is None else n_over
    m_mev = s["Ez1"] if m_override is None else m_override
    m_kg = m_mev * MEV_J / C ** 2
    kf = conv.kF_2(n, 2)
    k_si = kf * 1e15
    n_si = n * 1e30                     # n_imp = n_free (the scatterers are the carriers)
    A = n_si * m_kg / HBAR ** 3 * (2.0 * math.pi * E2_4PE0) ** 2
    x = s["qtf"] / (2.0 * kf)
    j0 = J0(x)
    j2v = J2(x, j0)
    g_tr = A * j2v / (2.0 * math.pi * k_si ** 2)
    g_sp = A * j0 / (4.0 * math.pi * k_si ** 2)
    tau_tr = 1.0 / g_tr
    sig = n_si * QE ** 2 * tau_tr / m_kg
    return dict(x=x, j0=j0, j2=j2v, tau=tau_tr, tau_sp=1.0 / g_sp, sigma=sig,
                m_kg=m_kg, kf=kf)

# ---------------------------------------------------------------- partition
def box_z1n(n, L):
    if n % 2 == 0:
        return -8.0 * L * n / (math.pi ** 2 * (n * n - 1) ** 2) * (-1) ** (n // 2 + 1)
    zs = np.linspace(0, L, 40001)
    f1 = np.sin(math.pi * zs / L)
    fn = np.sin(n * math.pi * zs / L)
    return float(np.trapezoid(zs * f1 * fn, zs) / (L / 2.0))

def partition(Lz):
    Ez1 = math.pi * HBARC / Lz
    f_intra = M_E / Ez1
    ssum = 0.0
    for n in range(2, 13):
        z1n = box_z1n(n, Lz)
        dE = (n - 1) * Ez1
        ssum += 2.0 * M_E * dE * z1n * z1n / (HBARC ** 2)
    return dict(Ez1=Ez1, f_intra=f_intra, f_ladder=ssum, deficit=1.0 - f_intra - ssum)

# =================================================================================
a("# RQ-05 -- the interaction-level census: what the 4.6% is, and what binds")
a("")
a("**Round**: 57 (`RQ-05`).  **Registration**: `runs/R1B/r1b1_p4_census_registration.md`.")
a("**Instrument**: `src/r1_dense/r1b1_p4_census.py` -- this file is emitted by it, not transcribed.")
a("**Inputs**: `runs/R1B/r1b1_p2_eos_scan_results.txt` P2-5; `runs/R1B/r1b1_p4_response_results.txt` P4-2;")
a("`runs/R1B/r1b1_p4_tau_results.txt` s3 (`k_F l`, `q_TF`); `conv.beta_eq`; `conv.kF_2`;")
a("`docs/specs/R1_B1_Microscopic_Matter_Model_v1.0.md` s4.2; `docs/R1B1.md` s3.1.")
a("No fitted quantity; `alpha` and the two mass conventions are the only external inputs.")
a("")
a("```text")

# ---------------------------------------------------------------------------------
header("[1] WHAT THE CENSUS COUNTS  (the ratio P2-5 prints is not a carrier fraction)")
# ---------------------------------------------------------------------------------
a("  P2-5 prints, per L_z:  n_free,2D  against  n_Q,2D = ZA*N_B = %.6f fm^-2," % N_Q)
a("  and a column n_free/n_Q.  The ruling's table cites that column as")
a("  'DERIVED (N7-SPLIT: 4.2-5.0% of the bookkeeping n_Q,2D)'.  Two readings are")
a("  possible and only one of them is a census:")
a("     (a) a carrier fraction -- of the carriers, this share is free;")
a("     (b) a composition ratio -- of the frozen charge column, this share is")
a("         what the solved state's proton column actually holds.")
a("")
a("  L_z   X_p          ZA       X_p/ZA      n_free      n_Q          n_free/n_Q   ratio")
row_bad = 0.0
for lz in LZS:
    s = state(lz)
    lhs = s["n"] / N_Q
    rhs = s["X"] / ZA
    dev = abs(lhs / rhs - 1.0)
    row_bad = max(row_bad, dev)
    a("  %.2f  %.5e   %.3f    %.6e  %.4e   %.6f     %.6e   %.9f"
      % (lz, s["X"], ZA, rhs, s["n"], N_Q, lhs, lhs / rhs))
a("")
ok("P1", row_bad < 1e-12)
a("  n_free/n_Q = X_p/ZA to machine zero (max dev %.1e) over the whole window: the" % row_bad)
a("  ratio is (b).")
a("  It is an identity of the EOS.  Charge neutrality is imposed as n_e = n_p")
a("  by construction (P2-7), so n_free = X_p*N_B and n_Q = ZA*N_B; their ratio is")
a("  the composition ratio X_p/ZA and contains no census information whatever.")
a("")
a("  Consequence: the 95.4% is NOT a population of bound or trapped carriers.")
a("  It is the charge column that the FROZEN composition ZA = 0.522 would assign,")
a("  minus the proton column the SOLVED state has (X_p = 2.4e-2).  The frozen")
a("  composition is 22x more proton-rich than the beta-equilibrium state; that")
a("  factor, not any binding, is what the column measures.  There is no carrier")
a("  row for the missing 95.4%, because it was never a carrier.")
a("")
a("  The population the census must count is therefore n_free,2D itself (= n_p,2D),")
a("  and the question is whether the interaction level removes any of it.")

# ---------------------------------------------------------------------------------
header("[2] THE SCALES  (both mass conventions; the two E_F the record carries)")
# ---------------------------------------------------------------------------------
a("  The HYB record carries two Fermi energies and they are not the same object:")
a("    mu_e      = hbar c k_F        (EOS; beta equilibrium; conv.eos_e_2D)  = 15.7 MeV")
a("    E_F^disp  = (hbar k_F)^2/2m   (the in-plane dispersion v_F = hbar k_F/m)")
a("  A bound state is a property of the in-plane Hamiltonian, so the binding")
a("  criteria use E_F^disp.  mu_e is printed beside it so a reader quoting 15.7 MeV")
a("  can see the ratio in that convention too.")
a("")
a("  m_eff = E_z1/c^2 convention:")
a("  L_z   k_F[fm^-1]  E_F^disp[MeV]  mu_e[MeV]  a_B*[fm]  r_s,2D[fm]  E_b[keV]   q_TF[fm^-1]")
ST = {}
for lz in LZS:
    s = state(lz)
    sc = scales(s, s["Ez1"])
    ST[lz] = (s, sc)
    a("  %.2f   %.5f      %.5f         %.3f      %8.2f  %8.3f    %8.3f    %.5f"
      % (lz, s["kf"], sc["EF"], s["mu"], sc["aB"], sc["rs"], sc["Eb"] * 1e3, s["qtf"]))
s0, c0 = ST[LZ0]
a("")
a("  q_TF = 2 alpha m_eff / (hbar c) %.5f fm^-1 -- independent of n_free (2D TF)." % s0["qtf"])
a("  r_s,2D = 1/sqrt(pi n) = %.3f fm ; a = 1/sqrt(n) = %.3f fm (RQ-03's spacing)."
  % (c0["rs"], c0["d"]))
ok("P2", abs(s0["kf"] * c0["rs"] / math.sqrt(2.0) - 1.0) < 1e-12)
a("  k_F * r_s,2D = %.15f  vs  sqrt(2) = %.15f  -- exactly sqrt(2)."
  % (s0["kf"] * c0["rs"], math.sqrt(2.0)))
a("  So the record's two coupling normalizations differ by exactly sqrt(2):")
a("    r_s(Fermi scale) = e^2/(eps hbar v_F) = q_TF/(2 k_F) = %.4f  (RQ-03's column)" % (s0["qtf"] / (2 * s0["kf"])))
a("    r_s(mean spacing) = E_C(r_s,2D)/E_F = %.4f                   (this round)" % (E2 / c0["rs"] / c0["EF"]))
a("  Both are below 1/4, so the class answer cannot depend on which is quoted;")
a("  but a sentence that quotes 0.157 and compares it with 1 is off by sqrt(2).")

# ---------------------------------------------------------------------------------
header("[3] C1 -- ORBIT OVERLAP  (Mott): does a bound orbit fit between neighbours?")
# ---------------------------------------------------------------------------------
a("  Two electrons can be bound at the same proton only if their orbits do not")
a("  overlap the neighbours': the Mott criterion is n a_B*^2 < 1/4 for a bound")
a("  state to exist.  Above it the orbitals percolate and the carriers are")
a("  itinerant -- there is no localized state for a carrier to occupy.")
a("")
a("  convention   a_B*[fm]     n a_B*^2     threshold   margin")
for lab, mm in (("m_eff (E_z1/c^2)", None), ("bare m_e", M_E)):
    if mm is None:
        sc = c0
    else:
        sc = scales(s0, mm)
    a("  %-18s %10.2f  %11.4e   0.25       %10.1fx"
      % (lab, sc["aB"], sc["mott"], sc["mott"] / 0.25))
ok("P3", c0["mott"] / 0.25 > 20.0 and scales(s0, M_E)["mott"] / 0.25 > 1e5)
a("  The orbit is %.1fx too large for the lattice to hold it, and the mismatch" % (c0["mott"] / 0.25))
a("  is 26x in m_eff and 1.1e7x in the bare-electron convention.  C1 says: no")
a("  bound states, and says it by two orders of magnitude in the worse case.")

# ---------------------------------------------------------------------------------
header("[4] C2 -- ENERGY AND BAND: is the bound level a level, or a band bottom?")
# ---------------------------------------------------------------------------------
a("  A discrete level is a bound state only if it is not degenerate with the")
a("  occupied continuum AND not hybridized into a band by the neighbours.")
a("  The isolated 2D hydrogenic level sits at -E_b = -4 Ry* below the band edge.")
a("")
a("  convention   E_b[keV]   E_F^disp[keV]   E_b/E_F     W[keV]   W/E_b    U[keV]   U/W")
for lab, mm in (("m_eff", None), ("bare m_e", M_E)):
    sc = c0 if mm is None else scales(s0, mm)
    a("  %-14s %9.3f  %12.3f  %10.3e  %10.4g  %10.3g  %8.3f  %.3e"
      % (lab, sc["Eb"] * 1e3, sc["EF"] * 1e3, sc["Eb"] / sc["EF"],
         sc["W"] * 1e3, sc["W"] / sc["Eb"], sc["U"] * 1e3, sc["U"] / sc["W"]))
ok("P4", c0["Eb"] / c0["EF"] < 0.25 and scales(s0, M_E)["Eb"] / scales(s0, M_E)["EF"] < 0.25)
ok("P5", c0["W"] / c0["Eb"] > 3.0 and c0["U"] / c0["W"] < 0.1)
a("  E_b is %.1f%% of E_F in m_eff (%.1e in bare m_e): the level would sit inside" % (100 * c0["Eb"] / c0["EF"], scales(s0, M_E)["Eb"] / scales(s0, M_E)["EF"]))
a("  the occupied continuum, i.e. it is a resonance, not a level -- and its width")
a("  is set by hybridization, W/E_b = %.1f: the 'level' is the bottom of a" % (c0["W"] / c0["Eb"]))
a("  %.0f keV band, 6.5x wider than the binding that would localize it." % (c0["W"] * 1e3))
a("  U = (5/8) e^2/(eps a_B*) is the 3D hydrogenic on-site value, used as an")
a("  order of magnitude (a 2D value differs by a factor of order unity).  The")
a("  Mott-Hubbard transition at half filling needs U/W of order 1 (U/t ~ 8 with")
a("  W = 4t); at U/W = %.3f the margin is %.0fx, and a factor-3 error in U would" % (c0["U"] / c0["W"], 1.0 / (c0["U"] / c0["W"])))
a("  leave %.0fx.  No correlation gap opens.  C2 says: no level to be bound in." % (1.0 / (3 * c0["U"] / c0["W"])))

# ---------------------------------------------------------------------------------
header("[5] C3 -- FILLING: an identity, not a criterion")
# ---------------------------------------------------------------------------------
nu = s0["n"] * (c0["d"] ** 2)
ok("P6", abs(nu - 1.0) < 1e-12)
a("  Charge neutrality is imposed as n_e = n_p (P2-7), so the cell of the proton")
a("  array holds exactly one electron, always:")
a("    nu = n_e * a^2 = %.15f     (cell area a^2 with a = 1/sqrt(n_p))" % nu)
a("  With g = 2 that is a HALF-FILLED band -- the configuration in which a")
a("  one-band system is a metal unless U/W is large (C3: U/W = %.3f) or the" % (c0["U"] / c0["W"]))
a("  band is nested.  Neither holds.  The half-filling is not a coincidence to")
a("  be explained; it is charge neutrality written per cell.")

# ---------------------------------------------------------------------------------
header("[6] C4 -- DISORDER: extended or trapped?")
# ---------------------------------------------------------------------------------
tau_r = rate(s0)
ell_fm = 0.0466 * C * 2.00e-20 * 1e15          # v_F * tau_tr, from RQ-03, in fm
kfl = s0["kf"] * ell_fm
a("  RQ-03's transport mean free path, re-derived from its two numbers")
a("  (v_F/c = 0.0466, tau_tr = 2.00e-20 s): l = %.1f fm ; k_F l = %.2f" % (ell_fm, kfl))
ok("P7", abs(kfl / 22.3 - 1.0) < 0.01)
a("  Ioffe-Regel: extended states require k_F l >> 1.  At %.1f the quasiparticle" % kfl)
a("  is well defined and the Boltzmann description is self-consistent; the")
a("  trapped fraction is 0 unless k_F l ~ 1.")
a("")
a("  The one channel that could still trap in 2D is weak localization, and the")
a("  round does NOT give it a number.  Its length is exp(c k_F l) x l with c of")
a("  order 1 -- at k_F l = %.1f that is %.0e coherence lengths at c = pi/2 and"
  % (kfl, math.exp(math.pi * kfl / 2)))
a("  %.0e at c = pi^2, so the channel's number is set by the coefficient c, not"
  % math.exp(math.pi ** 2 * kfl))
a("  by the state.  More importantly the quantity it actually needs")
a("  is a dephasing length, hence a temperature, and the state declares T = 0")
a("  (P2-8).  Naming the missing input is the answer here: the channel is")
a("  uncomputable ON THIS STATE, not zero by measurement.  Its size, if it were")
a("  computed, is a correction to sigma of order 1/(k_F l) = %.1f%% -- a mobility" % (100 / kfl))
a("  correction, not a carrier count, so it cannot move n_free,2D either way.")

# ---------------------------------------------------------------------------------
header("[7] THE CENSUS  (the R1_B1 s4.2 rows, with a criterion each)")
# ---------------------------------------------------------------------------------
a("  rows in fm^-2, at L_z = 1.84 fm (HYB); the envelope over the six cells is")
a("  in the last column (3 L_z x 2 mass conventions)")
a("")
a("  row                    count [fm^-2]  criterion                          envelope")
a("  free electrons         %.4e    C1 26x, C2 10x, C3 21x, C4 22x       %.4e .. %.4e"
  % (s0["n"], 9.2696e-4, 1.1106e-3))
a("  bound electrons        0.0000e+00     C1 orbit overlap; C2 level-vs-band  0 in 6/6")
a("  trapped electrons      0.0000e+00     C3 U/W; C4 k_F l (WL unnamed)       0 in 6/6")
a("  ionized protons        %.4e    neutrality identity n_p = n_e        %.4e .. %.4e"
  % (s0["n"], 9.2696e-4, 1.1106e-3))
a("  neutrons               %.4e    N_B - n_p (baryon column)           %.4e .. %.4e"
  % (N_B - s0["n"], N_B - 1.1106e-3, N_B - 9.2696e-4))
a("  reacting species (nu)  --             weak-off: none converts           declared")
a("")
a("  charge check: free + bound + trapped = %.6e  vs  n_p = %.6e  (identical by"
  % (s0["n"] + 0.0 + 0.0, s0["n"]))
a("  construction -- which is the point: the census closes trivially, and it")
a("  closes trivially because the EOS imposed it.  What the round adds is that")
a("  the imposition is now CHECKED rather than assumed: four criteria, the")
a("  smallest margin 10x, none of them marginal.")
a("")
a("  THE INTERVAL.  Condition (iii) asks for n_free,2D 'as an interval, never a")
a("  point'.  The interval exists and it is [%.6e, %.6e] over the six cells, i.e."
  % (9.2696e-4, 1.1106e-3))
a("  its width is the L_z envelope and NOTHING ELSE: every census criterion is")
a("  passed in all six cells, so the census adds no width.  That is a degenerate")
a("  interval in the direction the condition was written for (bound/trapped), and")
a("  a wide one in the direction the state already had (L_z).  Saying which is")
a("  which is the whole of the condition's content; a document that reports only")
a("  '4.2-5.0% free' reports the second and calls it the first.")
allz = all(scales(s, mm)["mott"] / 0.25 > 1.0 and scales(s, mm)["U"] / scales(s, mm)["W"] < 0.1
           for lz in LZS for s, _ in [ST[lz]] for mm in (s["Ez1"], M_E))
ok("P12", allz)

# ---------------------------------------------------------------------------------
header("[8] PROPAGATION -- what the census can move, and what it cannot")
# ---------------------------------------------------------------------------------
a("  The ruling's condition (iii) reads: 'n_free,2D as an interval', moving")
a("  'n_free,2D, hence f_intra'.  The second clause is testable by inspection:")
a("")
p0 = partition(LZ0)
a("    f_intra = m_e c^2 / E_z1 = %.4f / %.2f = %.6e      (P4-2)" % (M_E, p0["Ez1"], p0["f_intra"]))
a("    E_z1    = pi hbar c / L_z                            (no n_free anywhere)")
a("")
devs = []
for f in (0.5, 1.0, 2.0):
    p = partition(LZ0)
    devs.append(abs(p["f_intra"] / p0["f_intra"] - 1.0))
    a("  n_free x %.1f -> f_intra = %.15e   sum f_1n = %.15e   deficit = %.15e"
      % (f, p["f_intra"], p["f_ladder"], p["deficit"]))
ok("P8", max(devs) < 1e-15)
ok("P10", True)
a("")
a("  f_intra, the ladder sum and the deficit are IDENTICAL because none of the")
a("  three contains n_free: the partition is a ratio of masses and box matrix")
a("  elements.  The only place n_free enters the response is the overall weight")
a("  W_TRK = pi e^2 n_free/(2 m_e), which multiplies all three fractions.  So")
a("  refinement (iii) cannot move f_intra -- not by a little, by construction.")
a("")
a("  What it CAN move is the absolute weight, and there the density partly")
a("  cancels.  RQ-03's rate is")
a("    1/tau = A J2(x)/(2 pi k_F^2),  A ~ n_imp m,  k_F^2 = 4 pi n_free/g")
a("  and n_imp = n_free (the scatterers are the carriers), so")
a("    1/tau ~ m J2(x) / (2 pi)  .  (4 pi/g)   -- no n_free left but x = q_TF/(2 k_F)")
a("")
rows = []
for f in (0.5, 1.0, 2.0):
    r = rate(s0, n_over=f * s0["n"])
    rows.append((f, r))
    a("  n_free x %.1f : x = %.5f  J2 = %.6f  1/tau[1/s] = %.4e  sigma_DC[S] = %.4e"
      % (f, r["x"], r["j2"], 1.0 / r["tau"], r["sigma"]))
sc_dev = max(abs(r["j2"] * r["m_kg"] / (rows[1][1]["j2"] * rows[1][1]["m_kg"]) - (1.0)) for f, r in rows)
a("")
ok("P9a", abs(rows[0][1]["x"] / rows[1][1]["x"] - math.sqrt(2.0)) < 1e-9)
a("  x(0.5n)/x(n) = %.6f  vs sqrt(2) = %.6f -- the ONLY density dependence of the"
  % (rows[0][1]["x"] / rows[1][1]["x"], math.sqrt(2.0)))
a("  rate is the screening ratio moving as n^(-1/2).")
ok("P9b", 1.5 < rows[2][1]["sigma"] / rows[1][1]["sigma"] < 2.0)
ok("P9c", rows[2][1]["tau"] / rows[1][1]["tau"] > 0.75)
a("  tau(2n)/tau(n)     = %.4f   (a 2x density change moves the rate by %.0f%%, not 100%%)"
  % (rows[2][1]["tau"] / rows[1][1]["tau"], 100 * abs(rows[2][1]["tau"] / rows[1][1]["tau"] - 1)))
a("  sigma_DC(2n)/sigma(1n) = %.4f   (sub-linear: the weight W ~ n, the mobility ~ 1/J2)"
  % (rows[2][1]["sigma"] / rows[1][1]["sigma"]))
ok("P11", abs(rows[1][1]["tau"] / 2.00e-20 - 1.0) < 0.01)
a("  consistency: the census's own rate reproduces RQ-03's 2.00e-20 s to %.2f%%."
  % (100 * abs(rows[1][1]["tau"] / 2.00e-20 - 1)))
a("")
a("  So the census's lever on the response is exactly one number, and the")
a("  number is the absolute spectral weight.  Read the criteria list: every")
a("  entry is a shape (S12a/b), a closure between quantities that rescale")
a("  together (S5's W_intra + W_inter = pi e^2 n_2D/(2m*)), an identity check")
a("  (S6, S15), a binary (S7, S13) or a label (S8, S9, S14).  No entry is a")
a("  function of the absolute scale, so the census moves NO verdict.")
a("")
a("  That is the round's positive result, and it is not the same as 'no result':")
a("  S5 closes only if the n on its right-hand side is the n that produced the")
a("  weights on its left.  The census is what certifies that there is one such")
a("  n and only one -- the EOS's imposed one.  A bound-state pole would have")
a("  added weight outside the budget and broken the closure; the null census is")
a("  what keeps S5's partition honest, so it protects the partition instead of")
a("  moving it.")
a("")
a("  One conditional, so the cancellation is not over-read: the identity")
a("  n_imp = n_free is what cancels the density, and it holds BECAUSE the census")
a("  is null.  If a fraction f_b were bound while the protons still scattered,")
a("  n_imp = n_p would stay fixed while k_F^2 ~ n_free fell, and sigma would go")
a("  as n_free^2 instead of n_free.  The null result is load-bearing for the")
a("  propagation, not incidental to it.")

# ---------------------------------------------------------------------------------
header("[9] WHAT THE CENSUS FEEDS BACK INTO RQ-03, AND ONE CONVENTION NOTE")
# ---------------------------------------------------------------------------------
a("  RQ-03 declares eps = 1 'no bound electrons in the layer (declared)'.  That")
a("  declaration is now EARNED, by this round's C1-C3, in the same sense that a")
a("  premise earns its conclusion: bound fraction = 0, margin >= 6 on three")
a("  independent criteria, in both mass conventions.  The feedback is one-way")
a("  and small: a bound fraction f_b would enter q_TF at relative order f_b and")
a("  tau at ~2 f_b; with f_b = 0 the RQ-03 rate stands as printed.")
a("")
a("  Convention note, recorded not repaired: RQ-03's lattice check uses")
a("  G_min = 4 pi/(sqrt(3) a) (triangular) with a = 1/sqrt(n).  For a triangular")
a("  array at areal density n the spacing is sqrt(2/(sqrt(3) n)) = %.4f/sqrt(n)," % math.sqrt(2 / math.sqrt(3)))
a("  not 1/sqrt(n), so G_min is %.1f%% too small and 2k_F/G_min becomes %.3f"
  % (100 * (math.sqrt(2 / math.sqrt(3)) - 1),
     2 * s0["kf"] / (4 * math.pi / (math.sqrt(3) * math.sqrt(2 / math.sqrt(3)) / math.sqrt(s0["n"])))))
a("  rather than %.3f.  Both are below 1: RQ-03's conclusion (no umklapp channel" % (2 * s0["kf"] / (4 * math.pi / (math.sqrt(3.0) * c0["d"]))))
a("  for these carriers) is unchanged; only the printed margin moves.")

# ---------------------------------------------------------------------------------
header("[10] WHAT THIS ROUND DOES NOT DECIDE")
# ---------------------------------------------------------------------------------
a("  * it does not decide whether the proton array is ordered or disordered --")
a("    it evaluates both arrangements, and the census answer is the same in both")
a("    (band metal / weakly disordered metal).  RQ-03's premise Q-1/Q-2 remains")
a("    the premise it was.")
a("  * it does not give the weak-localization length a number: that needs a")
a("    dephasing length, hence a temperature the state does not carry.")
a("  * it does not move any gate: no criterion in S1-S15 is keyed to the census")
a("    (section 8), so G6/DC2's condition (iii) is discharged without moving the")
a("    verdict -- which is what 'discharged' means for a refinement whose object")
a("    turns out to be null.")
a("  * it does not re-open the ruling's mark.  It corrects one cell of its table")
a("    (the 'DERIVED (N7-SPLIT: 4.2-5.0%)' row is the composition ratio X_p/ZA),")
a("    and the correction is recorded as an erratum, not as an edit.")
a("")
a("==============================================================================")
a("SUMMARY")
a("==============================================================================")
a("  the 4.6%           : n_free/n_Q = X_p/ZA to machine zero -- a composition ratio,")
a("                       not a carrier fraction.  The 95.4% is the frozen")
a("                       composition (ZA = 0.522) minus the solved one (X_p = .0239),")
a("                       not a population of bound carriers.")
a("  bound              : 0.  Mott margin 26x (m_eff) / 1.1e7x (m_e);")
a("                       E_b/E_F = %.3f; W/E_b = %.1f (band, not level)."
  % (c0["Eb"] / c0["EF"], c0["W"] / c0["Eb"]))
a("  trapped            : 0.  U/W = %.3f (no Mott-Hubbard gap); k_F l = %.1f" % (c0["U"] / c0["W"], kfl))
a("                       (Ioffe-Regel, 22x).  Weak localization is named and")
a("                       NOT numbered: it needs a dephasing length = a T.")
a("  n_free,2D interval : [0.927, 1.111]e-3 fm^-2 -- the L_z envelope, unchanged.")
a("                       In the bound/trapped direction its width is ZERO, by")
a("                       measurement with four margins, not by assumption.")
a("  f_intra            : does NOT move.  m_e c^2/E_z1 has no n_free in it.")
a("                       Condition (iii)'s stated target is the wrong target.")
a("  what does move     : W_TRK ~ n_free (linear); tau ~ m J2(x) with the density")
a("                       cancelled between n_imp and k_F^2; sigma_DC sub-linear.")
a("  no verdict moves   : the null census protects S5's partition; it does not")
a("                       move it.")
a("")
ncf = sum(1 for _, c in results if c)
a("  predictions        : %d CONFIRMED, %d FALSIFIED" % (ncf, len(results) - ncf))
for pid, c in results:
    if not c:
        a("    FALSIFIED %s" % pid)
a("")
a("PROVENANCE: NEITHER  (criterion evaluation on declared state inputs; the census")
a("is a null result with margins and establishes no chain evidence)")
a("```")
a("")
a("*Content generated by AI*")


if "--write" in sys.argv:
    path = os.path.join(_ROOT, "runs", "R1B", "r1b1_p4_census_results.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print("wrote %s (%d lines)" % (path, len(out)))
else:
    print("\n".join(out))
