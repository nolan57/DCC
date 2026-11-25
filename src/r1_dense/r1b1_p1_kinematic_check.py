"""
R1B1-P1 kinematic closure checks (round 42).

PURPOSE : symbolic (CAS) verification of the hand derivations collected in
          runs/R1B/r1b1_p1_closure_review_v1.md.  Algebra checker ONLY:
          selects no numerical method, simulates no physics, produces no
          material parameter (r1b1_p1_registration.md, round-42 amendment).
GEOMETRY: ds^2 = -dt^2 + dx^2 + dy^2 + B(t)^2 dz^2,  c = 1 in this check
          (dimensional restoration is mechanical), signature (-,+,+,+),
          coordinates (t,x,y,z), B(t) > 0 prescribed.
EM CONVENTION (fixed once, used everywhere):
          F_{0i} = E_i,  F_{ij} = -eps_{ijk} B_k,  eps_{xyz} = +1.
          At B = 1 this reproduces canonical flat Maxwell exactly (checked).
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
Bf  = sp.Function('B', positive=True)(t)
dB  = sp.diff(Bf, t)
coords = [t, x, y, z]

g   = sp.diag(-1, 1, 1, Bf**2)
gv  = g.inv()
N   = 4

def line(s=""):
    print(s)

def header(s):
    line("")
    line("=" * 78)
    line(s)
    line("=" * 78)

# ------------------------------------------------------------------
header("R1 : CHRISTOFFEL SYMBOLS OF THE B(t) BACKGROUND")
# ------------------------------------------------------------------
Gam = {}
for lam in range(N):
    for mu in range(N):
        for nu in range(mu, N):
            e = sp.simplify(sp.Rational(1, 2) * sum(
                gv[lam, s] * (sp.diff(g[s, nu], coords[mu])
                              + sp.diff(g[s, mu], coords[nu])
                              - sp.diff(g[mu, nu], coords[s]))
                for s in range(N)))
            if e != 0:
                Gam[(lam, mu, nu)] = e
                if nu != mu:
                    Gam[(lam, nu, mu)] = e

names = {0: 't', 1: 'x', 2: 'y', 3: 'z'}
line("non-zero Christoffel symbols (indices in t,x,y,z order):")
for k in sorted(Gam):
    line("  Gamma^%s_{%s%s} = %s" % (names[k[0]], names[k[1]], names[k[2]], Gam[k]))

g_tzz = Gam.get((0, 3, 3))
g_ztz = Gam.get((3, 0, 3))
ok1 = sp.simplify(g_tzz - Bf * dB) == 0 and sp.simplify(g_ztz - dB / Bf) == 0
line("  [R1] only two independent symbols, Gamma^t_zz = B*B', Gamma^z_tz = B'/B"
     "   -> %s" % ("VERIFIED" if ok1 else "FAILED"))

def G(lam, mu, nu):
    return Gam.get((lam, mu, nu), sp.S.Zero)

# ------------------------------------------------------------------
header("R2 : ANISOTROPIC FLUID CONSERVATION  (comoving, diagonal T)")
# ------------------------------------------------------------------
rho, px, py, pz = (sp.Function(f, real=True)(t) for f in ('rho', 'px', 'py', 'pz'))
drho = sp.diff(rho, t)
# comoving u=(1,0,0,0); unit z-vector w=(0,0,0,1/B)  =>  T^{zz} = p_z / B^2
T = sp.diag(rho, px, py, pz / Bf**2)

divT = []
for nu in range(N):
    e = sp.S.Zero
    for mu in range(N):
        e += sp.diff(T[mu, nu], coords[mu])
        for k in range(N):
            e += G(mu, mu, k) * T[k, nu]
            e += G(nu, mu, k) * T[mu, k]
    divT.append(sp.simplify(e))

line("nabla_mu T^{mu t} (homogeneous, no lateral fluxes) =")
line("   " + str(divT[0]))
expected_t = drho + (dB / Bf) * (rho + pz)
ok2 = sp.simplify(divT[0] - expected_t) == 0
line("  [R2a] divT^t = d rho/dt + (B'/B)(rho + p_z)   -> %s"
     % ("VERIFIED" if ok2 else "FAILED"))
ok2b = all(sp.simplify(divT[nu]) == 0 for nu in (1, 2, 3))
line("  [R2b] divT^x = divT^y = divT^z = 0 (homogeneous, diagonal T)  -> %s"
     % ("VERIFIED" if ok2b else "FAILED"))
line("  NOTE: only p_z enters the t-equation -- the x,y stresses do not couple")
line("        to the background (their scale factors are static).")

# ------------------------------------------------------------------
header("R3 : THE BACKGROUND WORK TERM  (governor check-item IV.1)")
# ------------------------------------------------------------------
# E(t) = integral sqrt(h) rho d^3x  =  B(t) rho  per unit comoving lateral area.
E = Bf * rho
dE = sp.diff(E, t)
# local conservation (homogeneous): d rho/dt = -(B'/B)(rho + p_z)
dE_int = sp.simplify(dB * rho + Bf * (-(dB / Bf) * (rho + pz)))
ok3 = sp.simplify(dE_int + dB * pz) == 0
line("  local law  : d rho/dt = -(B'/B)(rho + p_z)")
line("  integrated : dE/dt = d/dt[B rho] = -B' * p_z   per unit lateral area")
line("             = -(B'/B) * integral sqrt(h) T^zz d^3x   (z-piston work)")
line("  [R3] the background works on matter through the z-stress ONLY;"
     "     in-plane stresses do no work   -> %s" % ("VERIFIED" if ok3 else "FAILED"))
line("  coordinate-split form (the governor's S^nu_background), nu = t:")
line("     d_mu T^{mu t} = F^{t lam} J_lam  -  (B'/B)(rho + p_z)")
line("  i.e. S^t_bg = -(B'/B)(rho + p_z) -- DERIVED from the connection and the")
line("  measure, never assumed zero.  The local covariant form carries no S term:")
line("  nabla_mu T^{mu nu} = F^{nu lam} J_lam exactly; the two forms must not be mixed.")
line("  checks: B'=0  ->  dE/dt = 0 (static anisotropy conserves energy);")
line("          B=1  ->  flat conservation recovered.")
ok3b = sp.simplify(divT[0].subs(dB, 0) - drho) == 0
line("  [R3b] B'=0 : divT^t = d rho/dt (no exchange)   -> %s"
     % ("VERIFIED" if ok3b else "FAILED"))

# ------------------------------------------------------------------
header("R4 : MAXWELL ON THE B(t) BACKGROUND  (source-free, inhomogeneous pair)")
# ------------------------------------------------------------------
Ex, Ey, Ez = (sp.Function('E_' + f, real=True)(t, x, y, z) for f in ('x', 'y', 'z'))
Bx, By, Bz = (sp.Function('B_' + f, real=True)(t, x, y, z) for f in ('x', 'y', 'z'))
F = sp.zeros(N, N)
F[0, 1] = Ex; F[0, 2] = Ey; F[0, 3] = Ez
F[1, 2] = -Bz; F[1, 3] = By; F[2, 3] = -Bx
for mu in range(N):
    for nu in range(mu):
        F[mu, nu] = -F[nu, mu]
Fup = sp.simplify(gv * F * gv)

Gmax = []
for nu in range(N):
    e = sp.S.Zero
    for mu in range(N):
        e += sp.diff(Bf * Fup[mu, nu], coords[mu])
    Gmax.append(sp.simplify(e / Bf))

line("generic-B components (printed for the record):")
for nu in range(N):
    line("  G^%s = %s" % (names[nu], Gmax[nu]))
line("  NOTE: the homogeneous pair dF = 0 is metric-independent: div B = 0 and")
line("        dB/dt + curl E = 0 hold identically on any background.")

canon = [
    sp.diff(Ex, x) + sp.diff(Ey, y) + sp.diff(Ez, z),
    -sp.diff(Ex, t) + sp.diff(Bz, y) - sp.diff(By, z),
    -sp.diff(Ey, t) + sp.diff(Bx, z) - sp.diff(Bz, x),
    -sp.diff(Ez, t) + sp.diff(By, x) - sp.diff(Bx, y),
]
ok4 = True
for nu in range(N):
    flat = Gmax[nu].subs(sp.Derivative(Bf, t), 0).subs(Bf, 1)
    ok4 = ok4 and sp.simplify(flat - canon[nu]) == 0
line("  [R4] B = 1 recovers canonical flat Maxwell, all four components  -> %s"
     % ("VERIFIED" if ok4 else "FAILED"))
line("  structural reading: E_z flux is weighted by 1/B (z-dilution); the")
line("  z-derivatives of transverse fields carry 1/B; the transverse sector is")
line("  untouched by B(t).")

# ------------------------------------------------------------------
header("R5 : SCALAR PROBE -- HOW EVERY FIELD FEELS THE BACKGROUND")
# ------------------------------------------------------------------
phi = sp.Function('phi', real=True)(t, x, y, z)
dphi = [sp.diff(phi, c) for c in coords]
box = sp.S.Zero
for mu in range(N):
    inner = sum(gv[mu, nu] * dphi[nu] for nu in range(N))
    box += sp.diff(Bf * inner, coords[mu])
box = sp.simplify(box / Bf)
line("Box_B phi = " + str(box))
box_flat = box.subs(sp.Derivative(Bf, t), 0).subs(Bf, 1)
canon_box = (-sp.diff(phi, t, 2) + sp.diff(phi, x, 2)
             + sp.diff(phi, y, 2) + sp.diff(phi, z, 2))
ok5 = sp.simplify(box_flat - canon_box) == 0
line("  [R5] B = 1 recovers the flat d'Alembertian   -> %s"
     % ("VERIFIED" if ok5 else "FAILED"))
line("  structural reading: every field equation acquires (i) 1/B^2 weights on")
line("  z-kinetics (the spec 3.2 E_z estimate is the adiabatic floor of this)")
line("  and (ii) a (B'/B) friction term -- B' drives transitions between z-modes.")
line("  The Dirac analogue (spin connection, B'-coupling in the z sector) is a")
line("  remaining P1-B derivation deliverable with declared conventions.")

# ------------------------------------------------------------------
header("R6 : CHARGE CONSERVATION FORM ON THE BACKGROUND (Ward-side statement)")
# ------------------------------------------------------------------
Jt, Jx, Jy, Jz = (sp.Function('J' + f, real=True)(t, x, y, z) for f in ('t', 'x', 'y', 'z'))
J = [Jt, Jx, Jy, Jz]
geom_div = sum(sp.diff(Bf * J[mu], coords[mu]) for mu in range(N)) / Bf
cov_div = sum(sp.diff(J[mu], coords[mu]) for mu in range(N)) \
    + sum(G(mu, mu, k) * J[k] for mu in range(N) for k in range(N))
ok6 = sp.simplify(geom_div - cov_div) == 0
line("  (1/sqrt(-g)) d_mu (sqrt(-g) J^mu) == nabla_mu J^mu   -> %s"
     % ("VERIFIED" if ok6 else "FAILED"))
line("  internal U(1) charges (electric charge, baryon number) are conserved on")
line("  the background exactly as in flat space: B(t) does not couple to phases.")

# ------------------------------------------------------------------
header("EVIDENCE CLASSIFICATION")
# ------------------------------------------------------------------
line("CHECK items (independent symbolic identities, usable as correctness")
line("     evidence): R1, R2a, R2b, R3, R3b, R4, R5, R6  ->  8/8 VERIFIED"
     if ok1 and ok2 and ok2b and ok3 and ok3b and ok4 and ok5 and ok6
     else "     -> SOME CHECKS FAILED (see above)")
line("IDENT items (definitional, not evidence): the EM convention F_0i = E_i,")
line("     F_ij = -eps_ijk B_k; the c = 1 working convention (restoration mechanical).")
line("This checker simulates no physics: it verifies algebra only.")
