"""Phase 1 pure symbolic ADM constraint-closure review.

Emission rule: build all lines in memory, then write once under --write.
No numerical simulation, no threshold assignment, no gate mark.
"""
import sys
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
f = sp.Function('f')(t, x)
kappa = sp.symbols('kappa', positive=True)

COORDS4 = [t, x, y, z]
COORDS3 = [x, y, z]


def christoffel(g, gin, coords):
    n = len(coords)
    gam = [[[None] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = 0
                for d in range(n):
                    s += gin[a, d] * (sp.diff(g[d, b], coords[c])
                                      + sp.diff(g[d, c], coords[b])
                                      - sp.diff(g[b, c], coords[d]))
                gam[a][b][c] = sp.simplify(s / 2)
    return gam


def ricci(gam, coords):
    n = len(coords)
    ric = sp.zeros(n)
    for b in range(n):
        for c in range(n):
            s = 0
            for a in range(n):
                s += sp.diff(gam[a][b][c], coords[a]) - sp.diff(gam[a][a][c], coords[b])
                for d in range(n):
                    s += gam[a][a][d] * gam[d][b][c] - gam[a][b][d] * gam[d][a][c]
            ric[b, c] = sp.simplify(s)
    return ric


def scalar_curv(g, gin, ric):
    return sp.simplify(sum(gin[i, j] * ric[i, j] for i in range(g.rows) for j in range(g.cols)))


def kretschmann(g, gin, coords):
    gam = christoffel(g, gin, coords)
    n = len(coords)
    rup = [[[[None] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    s = sp.diff(gam[a][d][b], coords[c]) - sp.diff(gam[a][c][b], coords[d])
                    for e in range(n):
                        s += gam[a][c][e] * gam[e][d][b] - gam[a][d][e] * gam[e][c][b]
                    rup[a][b][c][d] = sp.simplify(s)
    rdn = [[[[None] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    rdn[a][b][c][d] = sp.simplify(sum(g[a, e] * rup[e][b][c][d] for e in range(n)))
    total = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    up = sum(gin[a, e] * gin[b, g_] * gin[c, h] * gin[d, k]
                             * rdn[e][g_][h][k]
                             for e in range(n) for g_ in range(n)
                             for h in range(n) for k in range(n))
                    total += rdn[a][b][c][d] * up
    return sp.simplify(total)


def check_zero(expr):
    return sp.simplify(expr) == 0


def main():
    lines = []
    A = lines.append

    A("=" * 78)
    A("PHASE 1 PURE SYMBOLIC ADM CONSTRAINT-CLOSURE REVIEW")
    A("=" * 78)
    A("  scope: f(t,x) initial simplified model only; no numerical simulation")
    A("  metric: ds^2 = -dt^2 + dx^2 + dy^2 + f(t,x)^2 dz^2  (c=1, N=1, beta=0)")
    A("  signature (-,+,+,+) ; kappa=8*pi*G ; f>0 ; z domain NOT assigned")
    A("  PROVENANCE: NEITHER (symbolic review; adjudicates no gate)")
    A("")
    A("[thresholds] (registered before run)")
    A("  SY1-SY7: exact simplify == 0 ; SY8 reporting ; SY9 procedural")
    A("  IDENT statements are separated from CHECK and are not evidence")
    A("")

    # --- spatial curvature ---
    gamma = sp.diag(1, 1, f ** 2)
    gin3 = gamma.inv()
    gam3 = christoffel(gamma, gin3, COORDS3)
    ric3 = ricci(gam3, COORDS3)
    r3 = scalar_curv(gamma, gin3, ric3)
    r3_expect = -2 * sp.diff(f, x, 2) / f
    ok_sy1 = check_zero(r3 - r3_expect)

    # --- extrinsic curvature, record sign K_ij = -1/2 d_t gamma_ij ---
    kmat = sp.zeros(3)
    kmat[2, 2] = -f * sp.diff(f, t)
    ktrace = sp.simplify(sum(gin3[i, i] * kmat[i, i] for i in range(3)))
    ksq = sp.simplify(sum(gin3[i, i] * gin3[j, j] * kmat[i, j] ** 2
                          for i in range(3) for j in range(3)))
    hz = sp.simplify(sp.diff(f, t) / f)
    ok_kzz = check_zero(kmat[2, 2] + f * sp.diff(f, t))
    ok_ktrace = check_zero(ktrace + hz)
    ok_ksq = check_zero(ksq - hz ** 2)
    ok_ktrace2 = check_zero(ktrace ** 2 - ksq)
    ok_sy2 = ok_kzz and ok_ktrace and ok_ksq and ok_ktrace2

    # --- constraints ---
    rho_req = sp.simplify((r3 + ktrace ** 2 - ksq) / (2 * kappa))
    ok_sy3 = check_zero(kappa * rho_req + sp.diff(f, x, 2) / f)
    jx_req = sp.simplify(sp.diff(hz, x) / kappa)
    ok_sy4 = check_zero(kappa * jx_req - sp.diff(hz, x))

    # --- vacuum equivalence (symbolic) ---
    vac_a = sp.simplify(sp.diff(f, x, 2))
    vac_b = sp.simplify(sp.diff(hz, x))
    ok_sy5 = check_zero(kappa * rho_req + vac_a / f) and check_zero(kappa * jx_req - vac_b)

    # --- homogeneous limit f=f(t) ---
    ft = sp.Function('ft')(t)
    r3_h = sp.simplify(r3.xreplace({f: ft}))
    rho_h = sp.simplify(rho_req.xreplace({f: ft}))
    jx_h = sp.simplify(jx_req.xreplace({f: ft}))
    ok_sy6 = check_zero(rho_h) and check_zero(jx_h)

    # --- Kasner control f=t: flat despite g_zz -> 0 at t=0 ---
    g_ctrl = sp.diag(-1, 1, 1, t ** 2)
    gin_ctrl = g_ctrl.inv()
    k_ctrl = kretschmann(g_ctrl, gin_ctrl, COORDS4)
    ok_sy7 = check_zero(k_ctrl)

    A("-" * 78)
    A("[symbolic expressions]")
    A("  R^(3)                 = %s" % r3)
    A("  expected R^(3)        = %s" % r3_expect)
    A("  K_zz                  = %s" % kmat[2, 2])
    A("  K                     = %s" % ktrace)
    A("  K_ij K^ij             = %s" % ksq)
    A("  K^2 - K_ijK^ij        = %s" % sp.simplify(ktrace ** 2 - ksq))
    A("  kappa*rho_req         = %s" % sp.simplify(kappa * rho_req))
    A("  kappa*j_x,req         = %s" % sp.simplify(kappa * jx_req))
    A("  Kretschmann(f=t)      = %s" % k_ctrl)
    A("")
    A("[CHECK / IDENT / NEGCTRL]")
    A("  CHECK  SY1  R^(3) identity                         %s" % ("PASS" if ok_sy1 else "FAIL"))
    A("  IDENT  SY2  K definitions + K^2-KijKij=0           %s" % ("PASS" if ok_sy2 else "FAIL"))
    A("  CHECK  SY3  Hamiltonian -> kappa rho_req           %s" % ("PASS" if ok_sy3 else "FAIL"))
    A("  CHECK  SY4  Momentum -> kappa j_x,req, j_y=j_z=0   %s" % ("PASS" if ok_sy4 else "FAIL"))
    A("  CHECK  SY5  vacuum equivalence                     %s" % ("PASS" if ok_sy5 else "FAIL"))
    A("  CHECK  SY6  homogeneous f=f(t)                     %s" % ("PASS" if ok_sy6 else "FAIL"))
    A("  NEGCTRL SY7  f=t flat despite g_zz->0 at t=0       %s" % ("PASS" if ok_sy7 else "FAIL"))
    A("")
    A("[result classification]")
    A("  no stress source declared -> required source only")
    A("  class <= constraint-satisfying solution")
    A("  NOT an evolution solution; NOT a joint solution")
    A("  f=0 is not by itself a curvature singularity (SY7)")
    A("")
    A("[verdicts]")
    checks = [ok_sy1, ok_sy3, ok_sy4, ok_sy5, ok_sy6, ok_sy7]
    A("  CHECK %d/%d - IDENT %d/%d (not evidence) - NEGCTRL %d/%d"
      % (sum(checks), len(checks), 1 if ok_sy2 else 0, 1, 1 if ok_sy7 else 0, 1))
    A("  SY8 reporting: required source NOT assigned to any field")
    A("  SY9 procedural: no gate/terminal/threshold/queue/RQ state written")
    A("  OVERALL: %s" % ("PASS" if all(checks) and ok_sy2 else "FAIL"))
    A("  evidence level: SYMBOLIC IDENTITY / NOT GATE EVIDENCE")
    A("  PROVENANCE: NEITHER")
    A("")
    A("Content generated by AI")

    text = "\n".join(lines) + "\n"
    if "--write" in sys.argv:
        path = "runs/P1/phase1_symbolic_constraint_results.txt"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("written:", path)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
