#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DCC P2 — T_munu symbol generation (1+1 planar symmetry, N=1)
Machine-generate srepr expressions for T_00/T_01/T_11/T_22/T_33 from the stress-energy tensor
definition of the unified action (in terms of the field symbols A,B,C,phi,P,Q,E,f), for the solver
to lambdify. Exactly consistent with the matter terms in DCC_sympy_derivation.py.py (V and Z use the
P1a frozen form). Output: <<<EQS-JSON>>> block on stdout.
"""
import sympy as sp
import json as _json

t, x = sp.symbols('t x', real=True)
A = sp.Function('A')(t, x); B = sp.Function('B')(t, x); C = sp.Function('C')(t, x)
phi = sp.Function('phi')(t, x)
P = sp.Function('P')(t, x)      # phi_dot
Q = sp.Function('Q')(t, x)      # phi_x
E = sp.Function('E')(t, x)
f = sp.Function('f')(t, x)
lam, v, eps, alpha = sp.symbols('lam v eps alpha', positive=True)

gm = {(0,0):-sp.Integer(1),(1,1):A**2,(2,2):B**2,(3,3):C**2}
gmi = {(0,0):-sp.Integer(1),(1,1):1/A**2,(2,2):1/B**2,(3,3):1/C**2}
Vexp = (lam/4*(phi**2 - v**2)**2 + eps*(phi + v)/(2*v) + eps**2/(16*lam*v**4))
Zexp = sp.exp(alpha*phi/v)

dphi = [P, Q, sp.Integer(0), sp.Integer(0)]
dphi2 = sum(gmi[(m,m)]*dphi[m]**2 for m in range(4))
F2 = 2*(gmi[(0,0)]*gmi[(2,2)]*E**2 + gmi[(1,1)]*gmi[(2,2)]*f**2)
Fc = {(0,2):E, (2,0):-E, (1,2):f, (2,1):-f}

def Ttot(m, n):
    gab = gm.get((m,m),0) if m == n else 0
    Tphi = dphi[m]*dphi[n] - sp.Rational(1,2)*gab*dphi2 - gab*Vexp
    contr = sum(Fc.get((m,c),0)*Fc.get((n,c),0)*gmi[(c,c)] for c in range(4))
    TF = Zexp*(contr - sp.Rational(1,4)*gab*F2)
    return sp.expand(Tphi + TF)

out = {}
for (m, n) in [(0,0), (0,1), (1,1), (2,2), (3,3)]:
    out['T%d%d' % (m,n)] = sp.srepr(Ttot(m, n))
# Maxwell divergence-form coefficient (E-1, N=1): d/dt(Pt*E) - d/dx(Px*f) = 0
out['Pt'] = sp.srepr(Zexp*A*C/B)
out['Px'] = sp.srepr(Zexp*C/(A*B))
# Orthonormal-frame pressure auxiliary quantities (p_i = T_ii / a_i^2; the solver performs the division)
print('<<<EQS-JSON-BEGIN>>>')
print(_json.dumps(out, ensure_ascii=False))
print('<<<EQS-JSON-END>>>')
