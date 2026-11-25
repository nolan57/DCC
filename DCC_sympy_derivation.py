import sympy as sp
t,x=sp.symbols('t x',real=True)
N=sp.Function('N')(t,x);A=sp.Function('A')(t,x);B=sp.Function('B')(t,x);C=sp.Function('C')(t,x)
phi=sp.Function('phi')(t,x);Ay=sp.Function('Ay')(t,x)
gm={(0,0):-N**2,(1,1):A**2,(2,2):B**2,(3,3):C**2}
gmi={(0,0):-1/N**2,(1,1):1/A**2,(2,2):1/B**2,(3,3):1/C**2}
def gdn(c,i):
    return sp.Integer(0) if i in (2,3) else sp.diff(c,t if i==0 else x)
# v1.2 correction (originally summing over k with g^{kk}): the sum over k for Γ^l_mn in a diagonal metric
# The weight is g^{lk} (zero when l≠k), so only the k=l term survives. The old form mixed in k≠l terms with weight g^{kk}
# (e.g., Γ^0_22 picked up -B B_x/A²), distorting the printed G_munu.
# Note: E-1..E-8, Box phi, and T_munu recorded in the v1.1 document do not go through Christoffels and are unaffected.
Ch={(l,m,n):sp.simplify(gmi[(l,l)]*(gdn(gm.get((n,l),0),m)+gdn(gm.get((m,l),0),n)-gdn(gm.get((m,n),0),l))/2) for l in range(4) for m in range(4) for n in range(4)}
Ric={}
for m in range(4):
    for n in range(4):
        s=0
        for l in range(4):
            dl=(sp.diff(Ch[l,m,n],t) if l==0 else sp.diff(Ch[l,m,n],x)) if l<2 else 0
            dn=(sp.diff(Ch[l,m,l],t) if n==0 else sp.diff(Ch[l,m,l],x)) if n<2 else 0
            s+=dl-dn
            for sig in range(4):s+=Ch[l,m,n]*Ch[sig,l,sig]-Ch[sig,m,l]*Ch[l,n,sig]
        Ric[m,n]=sp.simplify(s)
R=sp.simplify(sum(gmi[(k,k)]*Ric[k,k] for k in range(4)))
def Gmn(m,n):
    gmm=gm.get((m,m),0) if m==n else 0
    return sp.simplify(Ric[m,n]-sp.Rational(1,2)*gmm*R)
print('sqrt(-g) =',sp.simplify(sp.sqrt(-gm[(0,0)]*gm[(1,1)]*gm[(2,2)]*gm[(3,3)])))
for (a,b) in [(0,0),(1,1),(2,2),(3,3),(0,1)]:
    print('G_%d%d ='%(a,b),sp.simplify(Gmn(a,b)))
# Maxwell
E=sp.diff(Ay,t);f=sp.diff(Ay,x)
Fty=gmi[(0,0)]*gmi[(2,2)]*E;Fxy=gmi[(1,1)]*gmi[(2,2)]*f
F2=sp.simplify(2*(Fty*E+Fxy*f));print('F^2 =',F2)
Z=sp.Function('Z')(phi)
Fc={(0,2):E,(2,0):-E,(1,2):f,(2,1):-f}
def Fc_m(m,n):return Fc.get((m,n),0)
def Fus(m,a):return sum(Fc_m(m,b)*gmi[(b,b)] for b in range(4))
print('--- Maxwell T_{mu nu} ---')
for (a,b) in [(0,0),(1,1),(2,2),(3,3),(0,1)]:
    contr=sum(Fc_m(a,c)*Fus(b,c) for c in range(4));gmm=gm.get((a,a),0) if a==b else 0
    print('T_%d%d ='%(a,b),sp.simplify(Z*(contr-sp.Rational(1,4)*gmm*F2)))
# orthonormal pure-magnetic pressures (E=0)
print('--- orthonormal pressures, pure magnetic (E=0) ---')
def T(m,n):
    contr=sum(Fc_m(m,c)*Fus(n,c) for c in range(4));gmm=gm.get((m,m),0) if m==n else 0
    return Z*(contr-sp.Rational(1,4)*gmm*F2)
scale={0:N**2,1:A**2,2:B**2,3:C**2}
for i in range(4):
    print('p_hat[%d] ='%i, sp.simplify((T(i,i)/scale[i]).subs(E,0)))
# Box phi (N kept)
def Boxphi():
    sg=N*A*B*C;res=0
    for mu in [0,1]:res+=sp.diff(sg*gmi[(mu,mu)]*sp.diff(phi,[t,x][mu]),[t,x][mu])
    return sp.simplify(res/sg)
print('Box phi =',Boxphi())
print('Box phi: coef phi_t =',sp.simplify(sp.diff(Boxphi(),sp.diff(phi,t))))
print('Box phi: coef phi_x =',sp.simplify(sp.diff(Boxphi(),sp.diff(phi,x))))

# --- v1.1 addendum: Maxwell divergence and scalar T ---
print('--- Maxwell divergence (A_mu=(0,0,Ay,0)) ---')
Fup = {(m,n): gmi[(m,m)]*gmi[(n,n)]*Fc_m(m,n) for m in range(4) for n in range(4)}
sg = N*A*B*C
coord = {0:t, 1:x, 2:0, 3:0}
for nu in range(4):
    e = 0
    for mu in range(4):
        if coord[mu] == 0:
            continue
        e += sp.diff(sg*Z*Fup[(mu,nu)], coord[mu])
    print('div_%s ='%['t','x','y','z'][nu], sp.simplify(e/sg))
print('sqrtg*Z*F^{ty} =', sp.simplify(sg*Z*Fup[(0,2)]))
print('sqrtg*Z*F^{xy} =', sp.simplify(sg*Z*Fup[(1,2)]))

print('--- scalar T_{mu nu} ---')
dphi = [sp.diff(phi,t), sp.diff(phi,x), sp.Integer(0), sp.Integer(0)]
dphi2 = sum(gmi[(m,m)]*dphi[m]**2 for m in range(4))
V = sp.Function('V')(phi)
for (a,b) in [(0,0),(1,1),(2,2),(3,3),(0,1)]:
    gab = gm.get((a,a),0) if a == b else 0
    Tab = dphi[a]*dphi[b] - sp.Rational(1,2)*gab*dphi2 - gab*V
    print('Tphi_%d%d ='%(a,b), sp.simplify(Tab))

# ======================================================================
# P2 addendum (v1.2): 1+1 plane-symmetric synchronous ADM system, N=1
# Machine-generated: constraints (Hamiltonian/Momentum), the 3x3 linear system for dH evolution,
# scalar phiddot, Maxwell Edot, and Kretschmann.
# Automatic checks: the gradient-free limit must reproduce the homogeneous Bianchi I equations and the homogeneous Kretschmann formula.
# Output: the <<<EQS-JSON>>> block (srepr text) at the end of stdout, captured by redirecting the run command,
#       parsed and loaded by the solver; manual transcription is forbidden.
# ======================================================================
import time as _time
import json as _json
_t0 = _time.time()
print('='*70)
print('P2 addendum: 1+1 plane-symmetric N=1 ADM system')

lam_s, v_s, eps_s, al_s, kap_s = sp.symbols('lam v eps alpha kappa', positive=True)
HAf = sp.Function('HA')(t,x); HBf = sp.Function('HB')(t,x); HCf = sp.Function('HC')(t,x)
dHA = sp.Function('dHA')(t,x); dHB = sp.Function('dHB')(t,x); dHC = sp.Function('dHC')(t,x)
Ef = sp.Function('E')(t,x); ff = sp.Function('f')(t,x)
Pf = sp.Function('P')(t,x)      # phi_dot
Qf = sp.Function('Q')(t,x)      # phi_x
Qx = sp.Function('Qx')(t,x)     # phi_xx
Pddot = sp.Function('Pddot')(t,x)  # phi_ddot
Ax_s = sp.Symbol('Ax'); Axx_s = sp.Symbol('Axx')
Bx_s = sp.Symbol('Bx'); Bxx_s = sp.Symbol('Bxx')
Cx_s = sp.Symbol('Cx'); Cxx_s = sp.Symbol('Cxx')
HAx = sp.Symbol('HAx'); HBx = sp.Symbol('HBx'); HCx = sp.Symbol('HCx')

gm1 = {(0,0):-sp.Integer(1),(1,1):A**2,(2,2):B**2,(3,3):C**2}
gmi1 = {(0,0):-sp.Integer(1),(1,1):1/A**2,(2,2):1/B**2,(3,3):1/C**2}

def gdn1(c,i):
    return sp.diff(c, t if i==0 else x) if i in (0,1) else sp.Integer(0)

Ch1 = {(l,m,n): sp.simplify(gmi1[(l,l)]*(gdn1(gm1.get((n,l),0),m)
        + gdn1(gm1.get((m,l),0),n) - gdn1(gm1.get((m,n),0),l))/2)
        for l in range(4) for m in range(4) for n in range(4)}
Ric1 = {}
for m in range(4):
    for n in range(4):
        s = 0
        for l in range(4):
            dl = sp.diff(Ch1[l,m,n], t) if l==0 else (sp.diff(Ch1[l,m,n], x) if l==1 else 0)
            dn = sp.diff(Ch1[l,m,l], t) if n==0 else (sp.diff(Ch1[l,m,l], x) if n==1 else 0)
            s += dl - dn
            for sg_ in range(4):
                s += Ch1[l,m,n]*Ch1[sg_,l,sg_] - Ch1[sg_,m,l]*Ch1[l,n,sg_]
        Ric1[m,n] = s
R1 = sum(gmi1[(k,k)]*Ric1[k,k] for k in range(4))
def G1(m,n):
    gmm = gm1.get((m,m),0) if m==n else 0
    return sp.expand(Ric1[m,n] - sp.Rational(1,2)*gmm*R1)
print('Christoffel and Ricci done at %.1fs' % (_time.time()-_t0))

# Matter: explicit V and Z (P1a frozen form, with concrete derivative expressions)
Vexp = (lam_s/4*(phi**2 - v_s**2)**2 + eps_s*(phi + v_s)/(2*v_s)
        + eps_s**2/(16*lam_s*v_s**4))
Zexp = sp.exp(al_s*phi/v_s)
Vp_exp = sp.diff(Vexp, phi)
Zp_exp = sp.diff(Zexp, phi)
E_raw = sp.diff(Ay, t); f_raw = sp.diff(Ay, x)
F2_1 = sp.expand(2*(gmi1[(0,0)]*gmi1[(2,2)]*E_raw**2 + gmi1[(1,1)]*gmi1[(2,2)]*f_raw**2))
Fc1 = {(0,2):E_raw,(2,0):-E_raw,(1,2):f_raw,(2,1):-f_raw}
def Fus1(m,a_): return sum(Fc1.get((m,b),0)*gmi1[(b,b)] for b in range(4))
dphi1 = [sp.diff(phi,t), sp.diff(phi,x), sp.Integer(0), sp.Integer(0)]
dphi2_1 = sum(gmi1[(m,m)]*dphi1[m]**2 for m in range(4))
def Tot_raw(m,n):
    gab = gm1.get((m,m),0) if m==n else 0
    Tphi = dphi1[m]*dphi1[n] - sp.Rational(1,2)*gab*dphi2_1 - gab*Vexp
    contr = sum(Fc1.get((m,c),0)*Fus1(n,c) for c in range(4))
    TF = Zexp*(contr - sp.Rational(1,4)*gab*F2_1)
    return sp.expand(Tphi + TF)

subs_list = [
    # Mixed derivatives must be substituted before pure time derivatives; otherwise subs triggers
    # "substitute, then differentiate" inside Derivative, leaving uncaught Derivative(H*, x) terms.
    (sp.Derivative(A, t, x), Ax_s*HAf + A*HAx),
    (sp.Derivative(A, x, t), Ax_s*HAf + A*HAx),
    (sp.Derivative(B, t, x), Bx_s*HBf + B*HBx),
    (sp.Derivative(B, x, t), Bx_s*HBf + B*HBx),
    (sp.Derivative(C, t, x), Cx_s*HCf + C*HCx),
    (sp.Derivative(C, x, t), Cx_s*HCf + C*HCx),
    (sp.Derivative(A,(t,2)), A*(dHA + HAf**2)), (sp.Derivative(A,t), A*HAf),
    (sp.Derivative(B,(t,2)), B*(dHB + HBf**2)), (sp.Derivative(B,t), B*HBf),
    (sp.Derivative(C,(t,2)), C*(dHC + HCf**2)), (sp.Derivative(C,t), C*HCf),
    (sp.Derivative(Ay,t), Ef), (sp.Derivative(Ay,x), ff),
    (sp.Derivative(phi,(t,2)), Pddot), (sp.Derivative(phi,t), Pf),
    (sp.Derivative(phi,(x,2)), Qx), (sp.Derivative(phi,x), Qf),
    (sp.Derivative(A,(x,2)), Axx_s), (sp.Derivative(A,x), Ax_s),
    (sp.Derivative(B,(x,2)), Bxx_s), (sp.Derivative(B,x), Bx_s),
    (sp.Derivative(C,(x,2)), Cxx_s), (sp.Derivative(C,x), Cx_s),
]
def subs1(e):
    e = e.doit()
    for a_, b_ in subs_list:
        e = e.subs(a_, b_)
    e = e.subs(sp.Derivative(HAf,x), HAx).subs(sp.Derivative(HBf,x), HBx)
    e = e.subs(sp.Derivative(HCf,x), HCx)
    return sp.expand(e)
print('substitution map done at %.1fs' % (_time.time()-_t0))

Ham_raw = subs1(G1(0,0) - kap_s*Tot_raw(0,0))
Mom_raw = subs1(G1(0,1) - kap_s*Tot_raw(0,1))
assert not Ham_raw.has(dHA, dHB, dHC), 'Hamiltonian constraint must not contain dH'
print('Hamiltonian constraint G_00 - kappa T_00 = 0:')
print(sp.simplify(Ham_raw))
print('Momentum constraint G_01 - kappa T_01 = 0:')
print(sp.simplify(Mom_raw))

Eqs = [subs1(G1(i,i) - kap_s*Tot_raw(i,i)) for i in (1,2,3)]
M_mat = sp.Matrix(3,3, lambda j,k: sp.simplify(Eqs[j].coeff([dHA,dHB,dHC][k])))
b_vec = sp.Matrix([sp.simplify(Eqs[j].subs({dHA:0,dHB:0,dHC:0})) for j in range(3)])
for j in range(3):
    chk = sp.simplify(Eqs[j] - (M_mat[j,0]*dHA + M_mat[j,1]*dHB + M_mat[j,2]*dHC) - b_vec[j])
    assert chk == 0, 'evolution equation %d not linear in dH' % j
detM = sp.simplify(M_mat.det())
sp.pprint(M_mat)
sp.pprint(b_vec)
print('det(M) =', detM)
assert detM != 0, 'dH linear system singular'
# Eqs = M*dH + b = 0  =>  dH = -M^{-1} b. Store -b as the right-hand side; the solver calls solve(M, b) directly.
dH_sol = M_mat.LUsolve(-b_vec)
print('dH solution (dH = -M^-1 b) obtained at %.1fs' % (_time.time()-_t0))

flat = {Ax_s:0, Axx_s:0, Bx_s:0, Bxx_s:0, Cx_s:0, Cxx_s:0,
        HAx:0, HBx:0, HCx:0, Qf:0, Qx:0}
def flatsubs(e):
    e = e.subs(flat)
    e = e.subs({sp.Derivative(Ay,t):Ef, sp.Derivative(Ay,x):ff,
                sp.Derivative(phi,t):Pf, sp.Derivative(phi,x):Qf,
                sp.Derivative(phi,(x,2)):Qx})
    return sp.simplify(e)
dHA_flat = flatsubs(dH_sol[0])
dHC_flat = flatsubs(dH_sol[2])
px_c = flatsubs(Tot_raw(1,1)/A**2)
py_c = flatsubs(Tot_raw(2,2)/B**2)
pz_c = flatsubs(Tot_raw(3,3)/C**2)
dHA_ref = (-HAf**2 - sp.Rational(1,2)*HAf*(HBf+HCf) + sp.Rational(1,2)*HBf*HCf
           - kap_s/2*(py_c + pz_c - px_c))
dHC_ref = (-HCf**2 - sp.Rational(1,2)*HCf*(HAf+HBf) + sp.Rational(1,2)*HAf*HBf
           - kap_s/2*(px_c + py_c - pz_c))
chk1 = sp.simplify(dHA_flat.subs({Ef:0, ff:0, Pf:0, Qf:0})
                   - dHA_ref.subs({Ef:0, ff:0, Pf:0, Qf:0}))
chk2 = sp.simplify(dHC_flat.subs({Ef:0, ff:0, Pf:0, Qf:0})
                   - dHC_ref.subs({Ef:0, ff:0, Pf:0, Qf:0}))
print('homogeneous-limit check dHA:', chk1, 'dHC:', chk2)
assert chk1 == 0 and chk2 == 0, 'gradient-free limit does not match Bianchi I'

sg1 = A*B*C
Box1 = sum(sp.diff(sg1*gmi1[(mu,mu)]*sp.diff(phi, [t,x][mu]), [t,x][mu]) for mu in (0,1))/sg1
scal_eq = sp.expand((Box1 - Vp_exp - Zp_exp/(2*B**2)*(f_raw**2/A**2 - E_raw**2)).doit())
for a_, b_ in subs_list:
    scal_eq = scal_eq.subs(a_, b_)
scal_eq = sp.expand(scal_eq)
assert scal_eq.coeff(Pddot) == -1, 'scalar equation structure unexpected'
# scal_eq = -Pddot + REST = 0  =>  Pddot = REST = scal_eq + Pddot
phiddot_expr = sp.expand(scal_eq + Pddot)
# Check: the homogeneous (gradient-free) limit must reproduce the homogeneous scalar equation
# phiddot = -(HA+HB+HC)*P - V' - (alpha/v)*rho_B,  rho_B = Z*f^2/(2 A^2 B^2)
phidot_flat = sp.simplify(flatsubs(phiddot_expr).subs({Ef: 0}))
phidot_ref = (-(HAf+HBf+HCf)*Pf - Vp_exp
              - (al_s/v_s)*Zexp*ff**2/(2*A**2*B**2))
chkS = sp.simplify(phidot_flat - phidot_ref)
print('homogeneous-limit check phiddot:', chkS)
assert chkS == 0, 'scalar homogeneous limit mismatch'

Pt_c = Zexp*A*C/B
Px_c = Zexp*C/(A*B)
Pt_t = sp.expand(sp.diff(Pt_c, t).doit())
for a_, b_ in subs_list:
    Pt_t = Pt_t.subs(a_, b_)
Pt_t = sp.expand(Pt_t)
dE_expr = sp.expand((sp.Derivative(Px_c*ff, x) - Ef*Pt_t)/Pt_c)
print('Maxwell Pt_t/Pt =', sp.simplify(Pt_t/Pt_c))

def Riem_u(a_, b_, c_, d_):
    """R^a_{bcd} (first index raised), after first-order variable substitution."""
    e = sp.Integer(0)
    if c_ in (0, 1):
        e += sp.diff(Ch1[a_,b_,d_], t if c_==0 else x)
    if d_ in (0, 1):
        e -= sp.diff(Ch1[a_,b_,c_], t if d_==0 else x)
    for f_ in range(4):
        e += Ch1[a_,c_,f_]*Ch1[f_,b_,d_] - Ch1[a_,d_,f_]*Ch1[f_,b_,c_]
    return subs1(e)

# Independent fully lowered components: R_{0x0x}, R_{0y0y}, R_{0z0z}, R_{xyxy}, R_{xzxz}, R_{yzyz}
R01 = gm1[(0,0)]*Riem_u(0,1,0,1)
R02 = gm1[(0,0)]*Riem_u(0,2,0,2)
R03 = gm1[(0,0)]*Riem_u(0,3,0,3)
R12 = gm1[(1,1)]*Riem_u(1,2,1,2)
R13 = gm1[(1,1)]*Riem_u(1,3,1,3)
R23 = gm1[(2,2)]*Riem_u(2,3,2,3)
z1 = sp.simplify(gm1[(0,0)]*Riem_u(0,2,0,3))
z2 = sp.simplify(gm1[(1,1)]*Riem_u(1,2,1,3))
z3 = sp.simplify(gm1[(1,1)]*Riem_u(1,2,2,3))
z4 = sp.simplify(gm1[(0,0)]*Riem_u(0,1,0,2))
print('vanishing checks (must be 0):', z1, z2, z3, z4)
assert z1==0 and z2==0 and z3==0 and z4==0, 'unexpected off-diagonal Riemann'
# K = sum R_abcd R^abcd = 4 * sum_comp R_c^2 * (g^aa g^bb g^cc g^dd) (diagonal metric)
Kexpr = 4*(R01**2*gmi1[(0,0)]**2*gmi1[(1,1)]**2
           + R02**2*gmi1[(0,0)]**2*gmi1[(2,2)]**2
           + R03**2*gmi1[(0,0)]**2*gmi1[(3,3)]**2
           + R12**2*gmi1[(1,1)]**2*gmi1[(2,2)]**2
           + R13**2*gmi1[(1,1)]**2*gmi1[(3,3)]**2
           + R23**2*gmi1[(2,2)]**2*gmi1[(3,3)]**2)
R01_f = sp.simplify(flatsubs(R01))
print('R_0101 flat limit =', R01_f)
K_flat = sp.simplify(flatsubs(Kexpr))
K_ref = 4*((dHA+HAf**2)**2 + (dHB+HBf**2)**2 + (dHC+HCf**2)**2)
K_ref += 4*(HAf**2*HBf**2 + HAf**2*HCf**2 + HBf**2*HCf**2)
chkK = sp.simplify(K_flat.subs({dHA:0,dHB:0,dHC:0}) - K_ref.subs({dHA:0,dHB:0,dHC:0}))
print('Kretschmann flat-limit check:', chkK)
assert chkK == 0, 'Kretschmann flat limit mismatch'
print('Kretschmann derived at %.1fs' % (_time.time()-_t0))

_srepr = {
    'Ham': sp.srepr(sp.simplify(Ham_raw)),
    'Mom': sp.srepr(sp.simplify(Mom_raw)),
    'M': [[sp.srepr(M_mat[i,j]) for j in range(3)] for i in range(3)],
    'b': [sp.srepr(b_vec[i]) for i in range(3)],
    'dH': [sp.srepr(dH_sol[i]) for i in range(3)],
    'phiddot': sp.srepr(phiddot_expr),
    'Pt_t_over_Pt': sp.srepr(sp.simplify(Pt_t/Pt_c)),
    'Kretschmann': sp.srepr(sp.simplify(Kexpr)),
}
print('<<<EQS-JSON-BEGIN>>>')
print(_json.dumps(_srepr, ensure_ascii=False))
print('<<<EQS-JSON-END>>>')
print('addendum finished at %.1fs' % (_time.time()-_t0))
