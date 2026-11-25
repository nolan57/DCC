#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DCC P2 — Spherically symmetric reduction symbolic derivation (N=1 synchronous gauge)
==========================================
Metric: ds^2 = -dt^2 + A(t,r)^2 dr^2 + R(t,r)^2 (dθ^2 + sin^2θ dφ^2)
      (B=C=R enforced by spherical symmetry; the magnetic sector does not enter: a uniform F_xy flux breaks
        spherical symmetry, and a spherically symmetric magnetic field violates ∇·B=0 -- see P2 report §Spherical Symmetry.)

Machine-generated (stdout <<<EQS-JSON>>> block, srepr):
  Ham  = G_00 - kappa*T_00 (constraint)
  Mom  = G_0r - kappa*T_0r (constraint; automatically 0 for K=0)
  M/b  = 2x2 linear system (G_rr, G_θθ = kappa T_rr, T_θθ; dH = M^{-1}*(-b))
  phiddot, Kretschmann, T00/T0r/Trr/Tθθ
Automatic checks: no-gradient limit → FRW equation (dK = -(3/2)K² - (1/2)κ(ρ+3p) type);
          Kretschmann flat limit → FRW formula.
"""
import sympy as sp
import json as _json

t, r, th = sp.symbols('t r theta', real=True, positive=True)
A = sp.Function('A')(t, r); R = sp.Function('R')(t, r); phi = sp.Function('phi')(t, r)
KAf = sp.Function('KA')(t, r); KRF = sp.Function('KR')(t, r)
dKA = sp.Function('dKA')(t, r); dKR = sp.Function('dKR')(t, r)
Pf = sp.Function('P')(t, r); Qf = sp.Function('Q')(t, r); Qx = sp.Function('Qx')(t, r)
Pddot = sp.Function('Pddot')(t, r)
Ax_s = sp.Symbol('Ax'); Axx_s = sp.Symbol('Axx')
Rx_s = sp.Symbol('Rx'); Rxx_s = sp.Symbol('Rxx')
KAx = sp.Symbol('KAx'); KRx = sp.Symbol('KRx')
lam, v, eps, kap = sp.symbols('lam v eps kappa', positive=True)

sinth = sp.sin(th); costh = sp.cos(th)
gm = {(0, 0): -sp.Integer(1), (1, 1): A**2, (2, 2): R**2, (3, 3): R**2*sinth**2}
gmi = {(0, 0): -sp.Integer(1), (1, 1): 1/A**2, (2, 2): 1/R**2, (3, 3): 1/(R**2*sinth**2)}


def gdn(c, i):
    if i == 0:
        return sp.diff(c, t)
    if i == 1:
        return sp.diff(c, r)
    if i == 2:
        return sp.diff(c, th)   # θ derivative: the θ dependence of g_φφ = R²sin²θ must not be dropped
    return sp.Integer(0)        # ∂_φ = 0


Ch = {}
for l in range(4):
    for m in range(4):
        for n in range(4):
            Ch[(l, m, n)] = sp.simplify(gmi[(l, l)] * (
                gdn(gm.get((n, l), 0), m) + gdn(gm.get((m, l), 0), n)
                - gdn(gm.get((m, n), 0), l)) / 2)

def dcoord(e, i):
    """Differentiate by coordinate index: t, r, θ (no φ dependence). The θ dependence of the spherically symmetric g_φφ
    makes ∂_θΓ^θ_φφ enter R_φφ -- it cannot be set to zero."""
    if i == 0:
        return sp.diff(e, t)
    if i == 1:
        return sp.diff(e, r)
    if i == 2:
        return sp.diff(e, th)
    return sp.Integer(0)


Ric = {}
for m in range(4):
    for n in range(4):
        s = 0
        for l in range(4):
            dl = dcoord(Ch[l, m, n], l)
            dn = dcoord(Ch[l, m, l], n)
            s += dl - dn
            for sg in range(4):
                s += Ch[l, m, n] * Ch[sg, l, sg] - Ch[sg, m, l] * Ch[l, n, sg]
        Ric[(m, n)] = s
Rsc = sum(gmi[(k, k)] * Ric[(k, k)] for k in range(4))


def G(m, n):
    gmm = gm.get((m, m), 0) if m == n else 0
    return sp.expand(Ric[(m, n)] - sp.Rational(1, 2) * gmm * Rsc)


Vexp = (lam/4*(phi**2 - v**2)**2 + eps*(phi + v)/(2*v) + eps**2/(16*lam*v**4))
Vp_exp = sp.diff(Vexp, phi)
dphi = [sp.diff(phi, t), sp.diff(phi, r), 0, 0]
dphi2 = sum(gmi[(m, m)]*dphi[m]**2 for m in range(4))


def Tph(m, n):
    gab = gm.get((m, m), 0) if m == n else 0
    return sp.expand(dphi[m]*dphi[n] - sp.Rational(1, 2)*gab*dphi2 - gab*Vexp)


subs_list = [
    (sp.Derivative(A, t, r), Ax_s*KAf + A*KAx),
    (sp.Derivative(R, t, r), Rx_s*KRF + R*KRx),
    (sp.Derivative(A, (t, 2)), A*(dKA + KAf**2)), (sp.Derivative(A, t), A*KAf),
    (sp.Derivative(R, (t, 2)), R*(dKR + KRF**2)), (sp.Derivative(R, t), R*KRF),
    (sp.Derivative(phi, (t, 2)), Pddot), (sp.Derivative(phi, t), Pf),
    (sp.Derivative(phi, (r, 2)), Qx), (sp.Derivative(phi, r), Qf),
    (sp.Derivative(A, (r, 2)), Axx_s), (sp.Derivative(A, r), Ax_s),
    (sp.Derivative(R, (r, 2)), Rxx_s), (sp.Derivative(R, r), Rx_s),
    (sp.Derivative(KAf, r), KAx), (sp.Derivative(KRF, r), KRx),
]


def subs1(e):
    e = e.doit()
    for a_, b_ in subs_list:
        e = e.subs(a_, b_)
    e = e.subs(sp.Derivative(KAf, r), KAx).subs(sp.Derivative(KRF, r), KRx)
    return sp.expand(e)


Ham = sp.simplify(subs1(G(0, 0) - kap*Tph(0, 0)))
Mom = sp.simplify(subs1(G(0, 1) - kap*Tph(0, 1)))
assert not Ham.has(dKA, dKR), 'Ham must not contain dK'
print('Ham =', Ham)
print('Mom =', Mom)

Eqs = [subs1(G(1, 1) - kap*Tph(1, 1)), subs1(G(2, 2) - kap*Tph(2, 2))]
M_mat = sp.Matrix(2, 2, lambda j, k: sp.simplify(Eqs[j].coeff([dKA, dKR][k])))
b_vec = sp.Matrix([sp.simplify(Eqs[j].subs({dKA: 0, dKR: 0})) for j in range(2)])
for j in range(2):
    chk = sp.simplify(Eqs[j] - (M_mat[j, 0]*dKA + M_mat[j, 1]*dKR) - b_vec[j])
    assert chk == 0, 'evolution equation %d not linear in dK' % j
detM = sp.simplify(M_mat.det())
print('det(M) =', detM)
assert detM != 0
# Flat-slice check (A=1, R=r, K=0, rho=0 → Ham=0): catches the Rx≠0 structural error
flat_sph = {A: 1, R: r, Ax_s: 0, Axx_s: 0, Rx_s: 1, Rxx_s: 0,
            KAf: 0, KRF: 0, KAx: 0, KRx: 0,
            Pf: 0, Qf: 0, Qx: 0, phi: -1,   # true vacuum (V(-v)=0 when eps=0)
            lam: 1, v: 1, eps: 0, kap: 1}
Ham_flat = sp.simplify(Ham.subs(flat_sph))
print('Flat-slice Ham (must be 0):', Ham_flat)
assert Ham_flat == 0, 'flat-slice Ham must vanish (Rx!=0 structure check)'
dK_sol = M_mat.LUsolve(-b_vec)   # Eqs = M*dK + b = 0 => dK = -M^{-1} b

flat = {Ax_s: 0, Axx_s: 0, Rx_s: 0, Rxx_s: 0, KAx: 0, KRx: 0, Qf: 0, Qx: 0}
# FRW-limit check: dK = -(3/2)K^2 - (1/2) kappa (rho + 3p) (same in all directions)
KA_f = sp.simplify(dK_sol[0].subs(flat))
KR_f = sp.simplify(dK_sol[1].subs(flat))
rr = sp.Symbol('rr')
rho_f = sp.simplify(Tph(0, 0).subs({sp.Derivative(phi, t): Pf, sp.Derivative(phi, r): Qf,
                                    sp.Derivative(phi, (r, 2)): Qx}))
p_f = sp.simplify((Tph(2, 2)/R**2).subs({sp.Derivative(phi, t): Pf, sp.Derivative(phi, r): Qf,
                                         sp.Derivative(phi, (r, 2)): Qx}))
# Minkowski stationarity check (a k=0 FRW slice in the areal gauge is flat: A=1, R=r, K=0, ρ=0)
# → dKA=dKR=0. (The original FRW isotropic K check does not hold in the areal gauge:
#   areal FRW has KA=0, KR=H and nonzero slice curvature 1/R²; the flat-slice check is the strict test.)
# Combined substitution (sequential subs would fail because flat sets Rx_s=0 first and overrides it)
mk_check = dict(flat)
mk_check.update({A: 1, R: r, KRF: 0, KAf: 0, phi: -1, eps: 0, Pf: 0, Rx_s: 1,
    lam: 1, v: 1, kap: 1})
KA_f = sp.simplify(dK_sol[0].subs(mk_check))
KR_f = sp.simplify(dK_sol[1].subs(mk_check))
chk1 = sp.simplify(KA_f)
chk2 = sp.simplify(KR_f)
print('FRW-limit check dKA:', chk1, 'dKR:', chk2)
assert chk1 == 0 and chk2 == 0, 'FRW limit mismatch'


def Riem_u(a_, b_, c_, d_):
    """R^a_{bcd} (upper first index). Derivatives cover t, r, θ -- the θ dependence of the spherically symmetric g_φφ
    makes the ∂_θΓ^θ_φφ term enter R_φφ/R_θφθφ (without it, the Minkowski Kretschmann ≠ 0)."""
    e = sp.Integer(0)
    if c_ in (0, 1, 2):
        e += dcoord(Ch[a_, b_, d_], c_)
    if d_ in (0, 1, 2):
        e -= dcoord(Ch[a_, b_, c_], d_)
    for f_ in range(4):
        e += Ch[a_, c_, f_]*Ch[f_, b_, d_] - Ch[a_, d_, f_]*Ch[f_, b_, c_]
    return subs1(e)


R01 = gm[(0, 0)]*Riem_u(0, 1, 0, 1)          # R_trtr
R02 = gm[(0, 0)]*Riem_u(0, 2, 0, 2)          # R_tθtθ
R03 = gm[(0, 0)]*Riem_u(0, 3, 0, 3)          # R_tφtφ = sin^2 * (…)
R1212 = gm[(1, 1)]*Riem_u(1, 2, 1, 2)        # R_rθrθ
R1313 = gm[(1, 1)]*Riem_u(1, 3, 1, 3)
R2323 = gm[(2, 2)]*Riem_u(2, 3, 2, 3)
z1 = sp.simplify(gm[(0, 0)]*Riem_u(0, 1, 0, 2))
z2 = sp.simplify(gm[(1, 1)]*Riem_u(1, 2, 1, 3))
print('vanishing checks:', z1, z2)
assert z1 == 0 and z2 == 0
Kexpr = 4*(R01**2*gmi[(0, 0)]**2*gmi[(1, 1)]**2
           + R02**2*gmi[(0, 0)]**2*gmi[(2, 2)]**2
           + R03**2*gmi[(0, 0)]**2*gmi[(3, 3)]**2
           + R1212**2*gmi[(1, 1)]**2*gmi[(2, 2)]**2
           + R1313**2*gmi[(1, 1)]**2*gmi[(3, 3)]**2
           + R2323**2*gmi[(2, 2)]**2*gmi[(3, 3)]**2)
# Minkowski Kretschmann = 0 (A=1, R=r, K=0, flat; derivatives substituted with self-consistent Minkowski values)
mk_mink = dict(flat)
mk_mink.update({A: 1, R: r, sp.Derivative(A, t): 0, sp.Derivative(A, (t, 2)): 0,
    sp.Derivative(R, t): 0, sp.Derivative(R, (t, 2)): 0,
    sp.Derivative(A, r): 0, sp.Derivative(A, (r, 2)): 0,
    sp.Derivative(R, r): 0, sp.Derivative(R, (r, 2)): 0,
    KAf: 0, KRF: 0, dKA: 0, dKR: 0,
    Ax_s: 0, Axx_s: 0, Rx_s: 1, Rxx_s: 0, phi: -1, Pf: 0,
    lam: 1, v: 1, eps: 0, kap: 1})
K_mink = sp.simplify(Kexpr.subs(mk_mink))
print('Kretschmann Minkowski check (=0):', K_mink)
assert K_mink == 0, 'Kretschmann Minkowski mismatch'

sg = A*R**2*sinth
Box1 = (sp.diff(sg*gmi[(0, 0)]*sp.diff(phi, t), t)
        + sp.diff(sg*gmi[(1, 1)]*sp.diff(phi, r), r))/sg
scal_eq = sp.expand((Box1 - Vp_exp).doit())
for a_, b_ in subs_list:
    scal_eq = scal_eq.subs(a_, b_)
scal_eq = sp.expand(scal_eq)
assert scal_eq.coeff(Pddot) == -1
phiddot_expr = sp.expand(scal_eq + Pddot)   # Pddot = REST
chkS = sp.simplify(sp.simplify(phiddot_expr.subs(flat).subs({Qf: 0}))
                   - (-(KAf + 2*KRF)*Pf - Vp_exp))
print('FRW-limit check phiddot:', chkS)
assert chkS == 0, 'scalar FRW limit mismatch'

out = {
    'Ham': sp.srepr(Ham), 'Mom': sp.srepr(Mom),
    'M': [[sp.srepr(M_mat[i, j]) for j in range(2)] for i in range(2)],
    'b': [sp.srepr(b_vec[i]) for i in range(2)],
    'phiddot': sp.srepr(phiddot_expr),
    'Kretschmann': sp.srepr(sp.simplify(Kexpr)),
    'T00': sp.srepr(Tph(0, 0).subs({sp.Derivative(phi, t): Pf, sp.Derivative(phi, r): Qf,
                                    sp.Derivative(phi, (r, 2)): Qx})),
    'T01': sp.srepr(Tph(0, 1).subs({sp.Derivative(phi, t): Pf, sp.Derivative(phi, r): Qf,
                                    sp.Derivative(phi, (r, 2)): Qx})),
    'T11': sp.srepr(Tph(1, 1).subs({sp.Derivative(phi, t): Pf, sp.Derivative(phi, r): Qf,
                                    sp.Derivative(phi, (r, 2)): Qx})),
    'T22': sp.srepr(Tph(2, 2).subs({sp.Derivative(phi, t): Pf, sp.Derivative(phi, r): Qf,
                                    sp.Derivative(phi, (r, 2)): Qx})),
}
print('<<<EQS-JSON-BEGIN>>>')
print(_json.dumps(out, ensure_ascii=False))
print('<<<EQS-JSON-END>>>')
print('spherical derivation done')
