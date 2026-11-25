"""Phase 1b: coordinate-independent classification of the f->0 limit surface.

Metric ds^2 = -dt^2 + dx^2 + dy^2 + f(t,x)^2 dz^2, f>0.
Emission rule: build all lines in memory, then write once under --write.
No threshold, no gate mark, no matter-survival claim.
"""
import sys
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
f = sp.Function('f')(t, x)
p = sp.symbols('p', positive=True)
CO = [t, x, y, z]
N = 4


def christoffel(g, gin, co):
    n = len(co)
    return [[[sp.simplify(sum(gin[a, d] * (sp.diff(g[d, b], co[c]) + sp.diff(g[d, c], co[b])
                                          - sp.diff(g[b, c], co[d])) for d in range(n)) / 2)
              for c in range(n)] for b in range(n)] for a in range(n)]


def riemann_down(g, gin, co):
    gam = christoffel(g, gin, co)
    n = len(co)
    up = [[[[None] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    s = sp.diff(gam[a][d][b], co[c]) - sp.diff(gam[a][c][b], co[d])
                    for e in range(n):
                        s += gam[a][c][e] * gam[e][d][b] - gam[a][d][e] * gam[e][c][b]
                    up[a][b][c][d] = sp.expand(s)
    dn = [[[[None] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    dn[a][b][c][d] = sp.expand(sum(g[a, e] * up[e][b][c][d] for e in range(n)))
    return dn


def kretschmann(rdn, gin):
    n = gin.rows
    return sp.simplify(sum(
        rdn[a][b][c][d] * sum(gin[a, e] * gin[b, g] * gin[c, h] * gin[d, k]
                              * rdn[e][g][h][k]
                              for e in range(n) for g in range(n)
                              for h in range(n) for k in range(n))
        for a in range(n) for b in range(n) for c in range(n) for d in range(n)))


def ricci_scalar(rdn, gin):
    # Ricci R_bc = R^a_{bac} = g^(ae) R_{e b a c}. One index MUST be raised;
    # contracting two lower positions (rdn[a][b][a][c]) is not a valid contraction.
    n = gin.rows
    ric = [[sp.expand(sum(gin[a, e] * rdn[e][b][a][c]
                          for a in range(n) for e in range(n)))
            for c in range(n)] for b in range(n)]
    return sp.simplify(sum(gin[i, j] * ric[i][j] for i in range(n) for j in range(n)))


def electric(rdn, v):
    """E_ab = R_{a c b d} v^c v^d (two vectors, not four)."""
    return sp.Matrix(N, N, lambda a, b: sp.simplify(
        sum(rdn[a][c][b][d] * v[c] * v[d] for c in range(N) for d in range(N))))


def contract4(rdn, v):
    """The literal R_abcd u^a u^b u^c u^d requested in the mandate."""
    return sp.simplify(sum(rdn[a][b][c][d] * v[a] * v[b] * v[c] * v[d]
                           for a in range(N) for b in range(N)
                           for c in range(N) for d in range(N)))


def zero(e):
    return sp.simplify(sp.expand(e)) == 0


def main():
    L = []
    A = L.append

    g = sp.diag(-1, 1, 1, f ** 2)
    gin = g.inv()
    rdn = riemann_down(g, gin, CO)
    K = kretschmann(rdn, gin)
    R = ricci_scalar(rdn, gin)

    K_expect = 4 * (sp.diff(f, t, 2) ** 2 + sp.diff(f, x, 2) ** 2
                    - 2 * sp.diff(f, t, x) ** 2) / f ** 2
    R_expect = 2 * (sp.diff(f, t, 2) - sp.diff(f, x, 2)) / f
    ok_sg1 = zero(K - K_expect)
    ok_sg2 = zero(R - R_expect)

    # SG3: the four-identical-vector contraction vanishes identically (antisymmetry).
    u = sp.Matrix(sp.symbols('u0:4', real=True))
    c4 = contract4(rdn, u)
    ok_sg3 = zero(c4)

    # SG4: comoving tidal tensor u = d_t.
    Ecom = electric(rdn, sp.Matrix([1, 0, 0, 0]))
    e_zz = Ecom[3, 3]
    e2 = sp.simplify(sum(gin[a, c] * gin[b, d] * Ecom[a, b] * Ecom[c, d]
                         for a in range(N) for b in range(N)
                         for c in range(N) for d in range(N)))
    ok_sg4 = zero(e_zz + f * sp.diff(f, t, 2)) and zero(e2 - sp.diff(f, t, 2) ** 2 / f ** 2)

    # SG5: boosted and null tidal components. C,S treated as cosh/sinh symbols (C^2-S^2=1).
    C, S = sp.symbols('C S', positive=True)
    uz = sp.Matrix([C, 0, 0, S / f])
    Ez = electric(rdn, uz)
    kn = sp.Matrix([1, 1, 0, 0])          # null in (t,x)
    kz = sp.Matrix([1, 0, 0, 1 / f])      # null in (t,z)
    En = electric(rdn, kn)
    Ekz = electric(rdn, kz)
    ok_sg5 = (zero(Ez[3, 3] + C ** 2 * f * sp.diff(f, t, 2))
              and zero(Ez[1, 1] + S ** 2 * sp.diff(f, x, 2) / f)
              and zero(En[1, 1])
              and zero(Ekz[1, 1] + sp.diff(f, x, 2) / f))

    # SG6: Kasner control f=t. Flat; g_zz=t^2 -> 0 at t=0.
    gk = sp.diag(-1, 1, 1, t ** 2)
    rdn_k = riemann_down(gk, gk.inv(), CO)
    K_k = kretschmann(rdn_k, gk.inv())
    R_k = ricci_scalar(rdn_k, gk.inv())
    Ek = electric(rdn_k, sp.Matrix([1, 0, 0, 0]))
    tidal_k_flat = all(zero(Ek[i, j]) for i in range(N) for j in range(N))
    ok_sg6 = zero(K_k) and zero(R_k) and tidal_k_flat

    # SG7: power law f=t^p -> K = 4 p^2 (p-1)^2 t^-4.
    fp = t ** p
    K_fp = 4 * sp.diff(fp, t, 2) ** 2 / fp ** 2
    K_fp_expect = 4 * p ** 2 * (p - 1) ** 2 * t ** (-4)
    ok_sg7 = (zero(K_fp - K_fp_expect)
              and zero(K_fp.subs(p, 1))
              and zero(K_fp.subs(p, 2) - 16 * t ** (-4)))

    # ---- output ----
    A("=" * 78)
    A("PHASE 1b — COORDINATE-INDEPENDENT CLASSIFICATION OF THE f -> 0 LIMIT SURFACE")
    A("=" * 78)
    A("  metric: ds^2 = -dt^2 + dx^2 + dy^2 + f(t,x)^2 dz^2  (c=1, f>0)")
    A("  scope: initial simplified f(t,x) model; z-domain NOT assigned; geometry only")
    A("  PROVENANCE: NEITHER (coordinate-invariant analysis; adjudicates no gate)")
    A("")
    A("[thresholds] (registered before run)")
    A("  SG1-SG7: exact simplify == 0 ; SG3 is an IDENT (not evidence) ; SG8 classifier")
    A("  SG9 procedural. Three classifier slots only: SINGULARITY / HORIZON / UNDETERMINED")
    A("")
    A("-" * 78)
    A("[invariants]")
    A("  Kretschmann K              = %s" % K)
    A("  Ricci scalar R             = %s" % R)
    A("  g_zz                       = f^2  (-> 0 iff f -> 0)")
    A("")
    A("[tidal tensor E_ab = R_{a c b d} u^c u^d]")
    A("  literal R_abcd u^a u^b u^c u^d = %s   <- IDENTICALLY ZERO for any metric (antisymmetry)" % c4)
    A("  comoving u=d_t : E_zz      = %s" % e_zz)
    A("  comoving E_ab E^ab         = %s" % e2)
    A("  z-boost  E_zz              = -cosh^2(eta) * f * f_tt")
    A("  z-boost  E_xx              = -sinh^2(eta) * f_xx / f")
    A("  null(t,z) E_xx             = %s" % Ekz[1, 1])
    A("  null(t,z) E_zz             = %s" % Ekz[3, 3])
    A("  null(t,x) E_xx             = %s" % En[1, 1])
    A("")
    A("[controls]")
    A("  Kasner f=t   : K = %s , R = %s , all E_ab = %s , g_zz = t^2 -> 0 at t=0"
      % (K_k, R_k, '0' if tidal_k_flat else 'NONZERO'))
    A("  power f=t^p  : K = %s" % K_fp_expect)
    A("    p=1 -> K = %s (flat; coordinate degeneration only)" % K_fp.subs(p, 1))
    A("    p=2 -> K = %s (curvature blow-up)" % K_fp.subs(p, 2))
    A("")
    A("[CHECK / IDENT / NEGCTRL]")
    A("  CHECK  SG1  Kretschmann identity                %s" % ("PASS" if ok_sg1 else "FAIL"))
    A("  CHECK  SG2  Ricci scalar identity               %s" % ("PASS" if ok_sg2 else "FAIL"))
    A("  IDENT  SG3  four-u contraction vanishes         %s (not evidence: antisymmetry)"
      % ("PASS" if ok_sg3 else "FAIL"))
    A("  CHECK  SG4  comoving tidal E_zz, E_ab E^ab      %s" % ("PASS" if ok_sg4 else "FAIL"))
    A("  CHECK  SG5  boosted / null tidal components     %s" % ("PASS" if ok_sg5 else "FAIL"))
    A("  NEGCTRL SG6  Kasner flat while g_zz->0           %s" % ("PASS" if ok_sg6 else "FAIL"))
    A("  NEGCTRL SG7  power-law K and p=1,p=2 endpoints   %s" % ("PASS" if ok_sg7 else "FAIL"))
    A("")

    checks = [ok_sg1, ok_sg2, ok_sg4, ok_sg5, ok_sg6, ok_sg7]
    overall = all(checks) and ok_sg3

    A("[three-way classification — reported, not applied to any gate]")
    A("  slot 1 CURVATURE-SINGULARITY : K ~ 4 f_tt^2 / f^2 diverges when f->0 with f_tt != 0;")
    A("         generic f=t^p (p != 0,1) gives K ~ t^-4 -> infinity. Coordinate-independent.")
    A("  slot 2 HORIZON/EXTENDABLE   : Kasner f=t has K=R=E=0 while g_zz=t^2->0; no curvature")
    A("         singularity at the limit surface. Extension across t=0 is possible in the flat")
    A("         continuation; a z-directed geodesic reaches it at finite affine parameter.")
    A("  slot 3 UNDETERMINED          : applies when the z-domain topology and the t<0 continuation")
    A("         are not declared. THIS REVIEW LEAVES BOTH UNDECLARED, so for the actual project")
    A("         metric the classification is CONDITIONAL, not an unconditional 'extendable'.")
    A("")
    A("[consequence — triggered by the result, not applied by this instrument]")
    A("  - The premise 'L_z=0 is a geometric singularity' (effective_2d_definition_v1.md §5 reason 2)")
    A("    is NOT true for every geometry: the flat Kasner slice is a counterexample at the level")
    A("    of curvature invariants. It remains true for the generic contracting family with f_tt!=0.")
    A("  - G0' row 1's 'no reverse-on stated (geometric, convention-independent)' is therefore")
    A("    qualified for the flat-slice sector only; this result TRIGGERS that clause but does not")
    A("    move the gate, the terminal class, RL pricing, or any threshold.")
    A("  - No matter-survival, physical-attainability or visibility conclusion follows.")
    A("")
    A("[verdicts]")
    A("  CHECK %d/%d - IDENT %d/%d (not evidence) - NEGCTRL %d/%d"
      % (sum(checks), len(checks), 1 if ok_sg3 else 0, 1,
         sum([ok_sg6, ok_sg7]), 2))
    A("  SG8 classifier: three slots above; project metric -> CONDITIONAL (slot 2 for f=t flat slice,")
    A("                  slot 1 for generic f_tt!=0, slot 3 until domain/continuation declared)")
    A("  SG9 procedural: no gate/terminal/threshold/queue/RQ state written")
    A("  OVERALL: %s" % ("PASS" if overall else "FAIL"))
    A("  evidence level: COORDINATE-INVARIANT GEOMETRY / NOT GATE EVIDENCE")
    A("  PROVENANCE: NEITHER")
    A("")
    A("Content generated by AI")

    text = "\n".join(L) + "\n"
    if "--write" in sys.argv:
        path = "runs/P1/phase1b_singularity_results.txt"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("written:", path)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
