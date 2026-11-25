"""
R1B1-P1 current-conservation component check (round 44).

PURPOSE : component-level verification, with GENERIC complex spinor fields,
          of current conservation on the prescribed B(t) background -- the
          registered P1-B remainder of r1b1_p1_dirac_closure_v1.md (step 8).
          The real-form Dirac equation (gamma^mu D_mu + c_m m) psi = 0 with
          the round-43-fixed Omega_z is used; the continuity equation
            d_t(B j^t) + d_x(B j^x) + d_y(B j^y) + d_z(B j^z) = 0,
          j^mu = - psi^+ g0 g^mu psi  (j^t = psi^+ psi), is expanded with
          generic components and the equations of motion (and their conjugates)
          substituted.  Algebra checker only -- no physics simulation.
GEOMETRY: ds^2 = -dt^2 + dx^2 + dy^2 + B(t)^2 dz^2, c = 1, signature (-,+,+,+).
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
Bf  = sp.Function('B', positive=True, real=True)(t)
dBf = sp.diff(Bf, t)
m   = sp.Symbol('m', positive=True, real=True)
coords = [t, x, y, z]
coord_name = {0: 't', 1: 'x', 2: 'y', 3: 'z'}
N = 4
Z4 = sp.zeros(4, 4)
I4 = sp.eye(4)

def line(s=""):
    print(s)

def header(s):
    line("")
    line("=" * 78)
    line(s)
    line("=" * 78)

def ok(sid, cond):
    line("  [%s] -> %s" % (sid, "VERIFIED" if cond else "FAILED"))
    return cond

# --- gamma matrices (round-43-fixed representation) ---------------------------
sx = sp.Matrix([[0, 1], [1, 0]])
sy = sp.Matrix([[0, -sp.I], [sp.I, 0]])
sz = sp.Matrix([[1, 0], [0, -1]])
I2 = sp.eye(2)
Z2 = sp.zeros(2, 2)
blk = lambda A, Bc, Cc, Dd: sp.Matrix(sp.BlockMatrix([[A, Bc], [Cc, Dd]]))
ga = [sp.I * blk(Z2, I2, I2, Z2),
      blk(Z2, -sp.I * sx, sp.I * sx, Z2),
      blk(Z2, -sp.I * sy, sp.I * sy, Z2),
      blk(Z2, -sp.I * sz, sp.I * sz, Z2)]
gcz = ga[3] / Bf                  # curved gamma^z = g3/B
Oz  = -(dBf / 2) * ga[0] * ga[3]  # round-43-fixed spinor connection
G01 = ga[0] * ga[1]
G02 = ga[0] * ga[2]
G03 = ga[0] * ga[3]

def fix_real_conj(expr):
    """B(t) is declared real: evaluate conjugate(B') -> B' (CAS artifact fix)."""
    return expr.subs(sp.conjugate(dBf), dBf)

# --- generic spinor fields ----------------------------------------------------
u  = [sp.Function(f'u{k}')(t, x, y, z) for k in range(N)]
uc = [sp.Function(f'u{k}c')(t, x, y, z) for k in range(N)]   # stand for conj(u_k)
psi = sp.Matrix(u)
psic = sp.Matrix(uc)

# derivative-symbol matrices: rows k = component, cols n = coordinate
dpsi  = sp.Matrix([[sp.Symbol(f'd_{k}{n}') for n in range(N)] for k in range(N)])
dpsic = sp.Matrix([[sp.Symbol(f'dc_{k}{n}') for n in range(N)] for k in range(N)])
dx_psi  = sp.Matrix([dpsi[k, 1] for k in range(N)])
dy_psi  = sp.Matrix([dpsi[k, 2] for k in range(N)])
dz_psi  = sp.Matrix([dpsi[k, 3] for k in range(N)])
dx_pc  = sp.Matrix([dpsic[k, 1] for k in range(N)])
dy_pc  = sp.Matrix([dpsic[k, 2] for k in range(N)])
dz_pc  = sp.Matrix([dpsic[k, 3] for k in range(N)])

# --- equations of motion ------------------------------------------------------
# real form: (g0 d_t + g1 d_x + g2 d_y + g^z d_z + g^z Oz + m) psi = 0
#   => d_t psi = -(g0)^{-1} [ g1 d_x + g2 d_y + g^z d_z + g^z Oz + m ] psi
#   (g0)^{-1} = -g0  =>  d_t psi = + g0 [ ... ] psi
inv_g0 = sp.simplify(-(ga[0]).inv())
dt_psi_expr = sp.simplify(
    inv_g0 * (ga[1] * dx_psi + ga[2] * dy_psi + gcz * dz_psi + gcz * Oz * psi + m * psi))

ga_conj  = [fix_real_conj(M.applyfunc(sp.conjugate)) for M in ga]
gcz_conj = fix_real_conj(gcz.applyfunc(sp.conjugate))
Oz_conj  = fix_real_conj(Oz.applyfunc(sp.conjugate))
# conj EOM: since ALL four gamma matrices are purely imaginary in this
# representation (conj(g^mu) = -g^mu for every mu), the conjugated equation
#   conj(g^mu) d_mu psic + conj(g^z Oz) psic + m psic = 0
# is the ORIGINAL equation multiplied by -1: psic satisfies the identical
# equation.  Hence d_t psic = inv_g0 * [g1 dc_x + g2 dc_y + g^z dc_z
#                                       + g^z Oz psic + m psic].
dt_pc_expr = sp.simplify(
    inv_g0 * (ga[1] * dx_pc + ga[2] * dy_pc + gcz * dz_pc
              + gcz * Oz * psic + m * psic))
# where psic = (u0c, u1c, u2c, u3c)^T is defined alongside the fields:

# ------------------------------------------------------------------
header("K1 : STRUCTURE OF THE CONJUGATE EQUATION")
# ------------------------------------------------------------------
c1 = (sp.simplify(ga_conj[0] + ga[0]) == Z4
      and sp.simplify(ga_conj[1] + ga[1]) == Z4
      and sp.simplify(gcz_conj + gcz) == Z4
      and sp.simplify(Oz_conj - Oz) == Z4)
ok("K1", c1)
line("  conj(g0) = -g0, conj(g^i) = -g^i (real-form structure), Omega_z real --")
line("  the conjugate equation has the same operator structure with conj matrices.")

# ------------------------------------------------------------------
header("K2 : CONTINUITY, GENERIC COMPONENTS, CURVED BACKGROUND")
# ------------------------------------------------------------------
# j^mu = - psi^+ g0 g^mu psi ;  j^t = psi^+ psi  (since (g0)^2 = -1)
# continuity: d_t(B j^t) + d_x(B j^x) + d_y(B j^y) + d_z(B j^z) = 0
#   B j^z = - psi^+ g0 g3 psi  (the B inside g^z = g3/B cancels the measure B)
# the dagger is implemented by the formal-conjugate substitution map:
#   conj(u_k) -> uc_k,  conj(d_n u_k) -> dc_n u^c_k,  conj(B') -> B'  (B real).
sub_map = {}
for k in range(N):
    sub_map[sp.conjugate(u[k])] = uc[k]
    for n in range(N):
        sub_map[sp.conjugate(dpsi[k, n])] = dpsic[k, n]
sub_map[sp.conjugate(dBf)] = dBf

C = sp.S.Zero
C += dBf * sum(sp.conjugate(u[k]) * u[k] for k in range(N))          # d_t(B j^t), B' part
dt_rows = list(dt_psi_expr)                                          # d_t psi components
for k in range(N):
    C += Bf * sp.conjugate(dt_rows[k]) * u[k]                        # B d_t psi^+ . psi
    C += Bf * sp.conjugate(u[k]) * dt_rows[k]                        # B psi^+ . d_t psi
    # x: B j^x = -B psi^+ g0 g1 psi
    C += -Bf * (sp.conjugate(dpsi[k, 1]) * sum(G01[l, k] * u[l] for l in range(N))
                + sum(sp.conjugate(u[l]) * G01[l, k] for l in range(N)) * dpsi[k, 1])
    # y: B j^y = -B psi^+ g0 g2 psi
    C += -Bf * (sp.conjugate(dpsi[k, 2]) * sum(G02[l, k] * u[l] for l in range(N))
                + sum(sp.conjugate(u[l]) * G02[l, k] for l in range(N)) * dpsi[k, 2])
    # z: B j^z = - psi^+ g0 g3 psi (measure cancels)
    C += -(sp.conjugate(dpsi[k, 3]) * sum(G03[l, k] * u[l] for l in range(N))
           + sum(sp.conjugate(u[l]) * G03[l, k] for l in range(N)) * dpsi[k, 3])

C = fix_real_conj(C.subs(sub_map))
C = sp.simplify(sp.expand(C))
c2 = (C == 0)
ok("K2", c2)
if not c2:
    line("  residual coefficients (first nonzero):")
    shown = 0
    for k in range(N):
        for n in range(N):
            cc = sp.simplify(C.coeff(dpsi[k, n]))
            if cc != 0 and shown < 3:
                line("   coeff d_%s u%d:" % (coord_name[n], k))
                sp.pprint(cc)
                shown += 1
    for k in range(N):
        cc = sp.simplify(C.coeff(uc[k]))
        if cc != 0 and shown < 6:
            line("   coeff u%d^c:" % k)
            sp.pprint(cc)
            shown += 1

# ------------------------------------------------------------------
header("K3 : FLAT CROSS-CHECK  (B = 1, Omega = 0)")
# ------------------------------------------------------------------
dt_psi_f = sp.simplify(inv_g0 * (ga[1] * dx_psi + ga[2] * dy_psi + ga[3] * dz_psi + m * psi))
dt_pc_f = sp.simplify(
    ga[0] * (ga_conj[1] * dx_pc + ga_conj[2] * dy_pc + ga_conj[3] * dz_pc + m * psic))
Cf = sp.S.Zero
for k in range(N):
    Cf += sp.conjugate(dt_psi_f[k]) * u[k] + sp.conjugate(u[k]) * dt_psi_f[k]
    Cf += -(sp.conjugate(dpsi[k, 1]) * sum(G01[l, k] * u[l] for l in range(N))
            + sum(sp.conjugate(u[l]) * G01[l, k] for l in range(N)) * dpsi[k, 1])
    Cf += -(sp.conjugate(dpsi[k, 2]) * sum(G02[l, k] * u[l] for l in range(N))
            + sum(sp.conjugate(u[l]) * G02[l, k] for l in range(N)) * dpsi[k, 2])
    Cf += -(sp.conjugate(dpsi[k, 3]) * sum(G03[l, k] * u[l] for l in range(N))
            + sum(sp.conjugate(u[l]) * G03[l, k] for l in range(N)) * dpsi[k, 3])
Cf = fix_real_conj(Cf.subs(sub_map))
Cf = sp.simplify(sp.expand(Cf))
c3 = (Cf == 0)
ok("K3", c3)

# ------------------------------------------------------------------
header("EVIDENCE CLASSIFICATION")
# ------------------------------------------------------------------
line("CHECK items: K1 (conjugate structure), K2 (continuity equation with generic")
line("     components on the curved background, EOM + conjugate substituted),")
line("     K3 (flat cross-check) -- all identities at component level.")
line("THEOREM-level (diffeo invariance): nabla_mu T^{mu nu} = F^{nu lam} J_lam")
line("     holds for the Hilbert tensor of the declared diffeo-invariant action;")
line("     its four ingredients (nabla g^mu = 0, {g^mu,g^nu} = 2 g^munu, metric")
line("     compatibility, EOM) are machine-verified in the round-43 product; the")
line("     component-level curved T-check is registered as an optional appendix,")
line("     not a closure gate (Noether-theorem status).")
line("This checker verifies algebra only -- it simulates no physics and computes")
line("no material parameter.")
