#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DCC P2 — 1+1 Planar-Symmetry ADM Coupled Solver (Bubble Wall + Geometry + Magnetic Flux)
==========================================================

Metric (synchronous gauge N=1, beta=0)
    ds^2 = -dt^2 + A(t,x)^2 dx^2 + B(t,x)^2 dy^2 + C(t,x)^2 dz^2

Evolution variables (13 per grid point)
    lnA, lnB, lnC, HA, HB, HC, a=dx(lnA), b=dx(lnB), c=dx(lnC),
    phi, P=phi_dot, E=F_ty, f=F_xy

Equations (all machine-generated; do not transcribe by hand)
    Geometry/scalar/constraints/Kretschmann from the <<<EQS-JSON>>> block of
    DCC_sympy_derivation.py.py (sympy_stdout.txt);
    T_munu and the Maxwell coefficients from DCC_P2_1p1_Tmn_derivation.py (sympy_T_stdout.txt).
    d(lnA)=HA ... da=dx(HA) ... (kinematics)
    (dHA,dHB,dHC) = M^{-1} b          [G_11,G_22,G_33 = kappa T_11,T_22,T_33]
    dP = phiddot                       [Box phi - V' - Z'/(2B^2)(f^2/A^2-E^2)=0, E-7]
    dE = dx(Px*f)/Pt - E*(Pt_t/Pt)     [E-1 divergence form]
    df = dx(E)                         [Bianchi]
    Constraints (diagnostic): Ham=G_00-kappa*T_00=0, Mom=G_01-kappa*T_01=0

Initial data (both constraints satisfied exactly; implementation of roadmap §6.2-3 "must not be freely specified")
    Flat slice A=B=C=1, a=b=c=0;
    phi = v tanh(a_w x) (static) or the exact boosted kink (u chosen freely); P given by the boost;
    Pure magnetic: E=0, Px*f=Q=const => f = Q/Z(phi) (E-6 static sector);
    Free K data (the only free function): transverse-x isotropic H_A=H_B=:h(x);
    Momentum (j_x known): H_B+H_C =: w(x) = s0 + kappa*∫_0^x j_x dx';
    Hamiltonian (flat slice): h^2+2h*H_C = kappa*rho
      => h = w - sqrt(w^2-kappa*rho),  H_C = sqrt(w^2-kappa*rho)
      (take the smaller root; require w^2>kappa*rho everywhere; s0=m_s0*max(sqrt(kappa rho)))

Numerics
    RK4 + 2nd-order centered differences (same order as P1a, convergence target 2nd order) + zero-gradient boundaries.
    CFL=0.2; optional Kreiss-Oliger dissipation (off by default).

Run: python DCC_P2_wall_1p1.py
Output: DCC_P2_1p1_results.txt / DCC_P2_1p1_profiles.png /
      DCC_P2_1p1_observables.png / DCC_P2_1p1_L2.txt / DCC_P2_1p1_frames.npz
"""
import json
import re
import sys
import numpy as np
import sympy as sp
from sympy.core.function import AppliedUndef
from sympy.parsing.sympy_parser import parse_expr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Loading machine-generated equations (sympy srepr -> lambdify)
# ----------------------------------------------------------------------
_ARG_NAMES = ['A', 'Ax', 'Axx', 'B', 'Bx', 'Bxx', 'C', 'Cx', 'Cxx',
              'HA', 'HB', 'HC', 'HAx', 'HBx', 'HCx',
              'phi', 'P', 'Q', 'Qx', 'E', 'f',
              'dHA', 'dHB', 'dHC', 'lam', 'v', 'eps', 'alpha', 'kappa']
ARG_NAMES = _ARG_NAMES
ARG_SYMS = [sp.Symbol(nm) for nm in ARG_NAMES]
_FIELD_NAMES = {'A', 'B', 'C', 'phi', 'HA', 'HB', 'HC', 'dHA', 'dHB', 'dHC',
                'P', 'Q', 'Qx', 'E', 'f', 'Ay'}


def load_json_block(path):
    with open(path, encoding='utf-8') as fh:
        txt = fh.read()
    m = re.search(r'<<<EQS-JSON-BEGIN>>>\s*\n(.*?)\n?<<<EQS-JSON-END>>>', txt, re.S)
    if not m:
        raise RuntimeError('EQS-JSON block not found in %s' % path)
    return json.loads(m.group(1).strip())


def flatten(e):
    """Replace Function('X')(t,x) (with any t,x symbol variants) by Symbol('X'),
    and unify parameter symbols with assumptions (positive=True, etc.) into plain Symbol."""
    reps = {}
    for fn in e.atoms(AppliedUndef):
        nm = str(fn.func)
        if nm in _FIELD_NAMES:
            reps[fn] = sp.Symbol(nm)
    for s in e.atoms(sp.Symbol):
        if s.name in _ARG_NAMES and s != sp.Symbol(s.name):
            reps[s] = sp.Symbol(s.name)
    return e.xreplace(reps)


def build_func(srepr_str, allow_dH=False):
    e = flatten(parse_expr(srepr_str))
    if not allow_dH:
        for nm in ('dHA', 'dHB', 'dHC'):
            assert not e.has(sp.Symbol(nm)), 'unexpected %s in generated expression' % nm
    used = [s for s in ARG_SYMS if e.has(s)]
    f = sp.lambdify(used, e, 'numpy')
    # Wrapper with a unified signature: take arguments in ARG_NAMES order
    idx = [ARG_NAMES.index(str(s)) for s in used]
    def wrapper(vals):
        return f(*[vals[i] for i in idx])
    return wrapper


class Eqs(object):
    """Load and lambdify all machine-generated expressions."""
    def __init__(self, main_path='sympy_stdout.txt', t_path='sympy_T_stdout.txt'):
        main = load_json_block(main_path)
        tmn = load_json_block(t_path)
        self.M = [[build_func(main['M'][i][j]) for j in range(3)] for i in range(3)]
        self.b = [build_func(main['b'][i]) for i in range(3)]
        self.phiddot = build_func(main['phiddot'])
        self.Ptt = build_func(main['Pt_t_over_Pt'])
        self.Ham = build_func(main['Ham'])
        self.Mom = build_func(main['Mom'])
        self.Kret = build_func(main['Kretschmann'], allow_dH=True)
        self.T = {k: build_func(v) for k, v in tmn.items() if k.startswith('T')}
        self.Pt = build_func(tmn['Pt'])
        self.Px = build_func(tmn['Px'])

    def lin_system(self, vals):
        """Return M and the right-hand side rhs = -b: Eqs = M*dH + b = 0 => dH = M^{-1}*(-b)."""
        Mm = np.empty((3, 3) + vals[0].shape)
        bb = np.empty((3,) + vals[0].shape)
        for i in range(3):
            for j in range(3):
                Mm[i, j] = self.M[i][j](vals)
            bb[i] = -self.b[i](vals)
        return Mm, bb


# ----------------------------------------------------------------------
# Grid and differential operators (2nd-order centered differences, same order as P1a)
# ----------------------------------------------------------------------
def D(f, dx):
    """Periodic centered difference (periodic boundary configuration; eliminates
    constraint-projection incompatibility and boundary instability caused by one-sided boundary differences)."""
    return (np.roll(f, -1) - np.roll(f, 1)) / (2.0 * dx)


IDX = dict(lnA=0, lnB=1, lnC=2, HA=3, HB=4, HC=5,
           a=6, b=7, c=8, phi=9, P=10, E=11, f=12)
NF = 13


def pack(d):
    u = np.empty((NF,) + d['lnA'].shape)
    for k, i in IDX.items():
        u[i] = d[k]
    return u


def unpack(u):
    return {k: u[i] for k, i in IDX.items()}


# ----------------------------------------------------------------------
# Solver
# ----------------------------------------------------------------------
class Sim(object):
    def __init__(self, eqs, L=80.0, N=801, kappa=1.0, lam=1.0, v=1.0,
                 eps=0.0, alpha=0.5, Q=0.1, X0=20.0, m_s0=1.02):
        """Periodic domain [-L/2, L/2) (L is the period length); X0 = half-width of the vacuum slab (double-wall configuration)."""
        self.eqs = eqs
        self.x = np.linspace(-L/2, L/2, N, endpoint=False)
        self.dx = self.x[1] - self.x[0]
        self.kappa, self.lam, self.v = kappa, lam, v
        self.eps, self.alpha, self.Q = eps, alpha, Q
        self.X0, self.m_s0 = X0, m_s0

    def _geom_args(self, u):
        d = unpack(u)
        A = np.exp(d['lnA']); B = np.exp(d['lnB']); C = np.exp(d['lnC'])
        HA, HB, HC = d['HA'], d['HB'], d['HC']
        a, b, c = d['a'], d['b'], d['c']
        phi, P, E, f = d['phi'], d['P'], d['E'], d['f']
        Ax = A * a; Bx = B * b; Cx = C * c
        ax = D(a, self.dx); bx = D(b, self.dx); cx = D(c, self.dx)
        Axx = Ax * a + A * ax
        Bxx = Bx * b + B * bx
        Cxx = Cx * c + C * cx
        Q = D(phi, self.dx); Qx = D(Q, self.dx)
        HAx = D(HA, self.dx); HBx = D(HB, self.dx); HCx = D(HC, self.dx)
        zero = np.zeros_like(A)
        vals = [A, Ax, Axx, B, Bx, Bxx, C, Cx, Cxx, HA, HB, HC,
                HAx, HBx, HCx, phi, P, Q, Qx, E, f, zero, zero, zero,
                self.lam, self.v, self.eps, self.alpha, self.kappa]
        return vals, dict(A=A, B=B, C=C, HA=HA, HB=HB, HC=HC, phi=phi,
                          P=P, Q=Q, E=E, f=f)

    def orthonormal_stress(self, u):
        """Orthonormal-frame rho and p_i (N=1: rho=T_00, p_i=T_ii/a_i^2) from the machine-generated T."""
        vals, _ = self._geom_args(u)
        T00 = self.eqs.T['T00'](vals)
        T11 = self.eqs.T['T11'](vals)
        T22 = self.eqs.T['T22'](vals)
        T33 = self.eqs.T['T33'](vals)
        A = vals[0]; B = vals[3]; C = vals[6]
        rho = T00
        px = T11 / A ** 2
        py = T22 / B ** 2
        pz = T33 / C ** 2
        return rho, px, py, pz

    def kretschmann(self, u, dH):
        vals, _ = self._geom_args(u)
        full = vals + [dH[0], dH[1], dH[2]]
        return self.eqs.Kret(full)

    def rhs(self, u):
        vals, aux = self._geom_args(u)
        Mm, bb = self.eqs.lin_system(vals)
        dH = np.linalg.solve(np.moveaxis(Mm, 2, 0), bb.T[:, :, None])[:, :, 0].T  # (3, N)
        d = np.empty_like(u)
        d[IDX['lnA']], d[IDX['lnB']], d[IDX['lnC']] = aux['HA'], aux['HB'], aux['HC']
        d[IDX['HA']], d[IDX['HB']], d[IDX['HC']] = dH[0], dH[1], dH[2]
        d[IDX['a']], d[IDX['b']], d[IDX['c']] = D(aux['HA'], self.dx), \
            D(aux['HB'], self.dx), D(aux['HC'], self.dx)
        d[IDX['phi']] = aux['P']
        d[IDX['P']] = self.eqs.phiddot(vals)
        Pt = self.eqs.Pt(vals)
        Px = self.eqs.Px(vals)
        d[IDX['E']] = D(Px * aux['f'], self.dx) / Pt - aux['E'] * self.eqs.Ptt(vals)
        d[IDX['f']] = D(aux['E'], self.dx)
        return d

    def constraints(self, u):
        vals, _ = self._geom_args(u)
        return self.eqs.Ham(vals), self.eqs.Mom(vals)

    def initial_data(self, phi_override=None, ansatz='zstatic'):
        """Flat slice + K profile solved exactly from both constraints (symmetric double-wall slab, periodic domain).
        phi_override: uniform phi value (for the homogeneous cross-check).
        ansatz:
          'zstatic': H_A=0 (x static), H_B+H_C=s0 (Mom, j_x=0),
                     Ham: H_B·H_C = κρ → two-root decomposition (s0±Δ)/2, Δ=√(s0²-4κρ).
                     Far field H_C≈0 (nearly static in Z), magnetic tension p_ẑ=-ρ_B rapidly drives H_C<0
                     -- shortest D2 physical window.
          'transverse-iso': H_A=H_B=h, h+H_C=s0 (original scheme; s0 is raised by the wall density,
                     far-field H_C≈s0, D2 crosses zero more slowly)."""
        x, dx, v, lam = self.x, self.dx, self.v, self.lam
        aw = v * np.sqrt(lam / 2.0)
        if phi_override is not None:
            phi = phi_override * np.ones_like(x)
            P = np.zeros_like(x)
        else:
            # Symmetric double-wall slab: the inner region |x|<X0 is true vacuum -v, the outer region is false vacuum +v
            X0 = self.X0
            phi = -v * np.tanh(aw * (x + X0)) * np.tanh(aw * (X0 - x))
            P = np.zeros_like(x)   # Static initial data (expansion driven by eps, momentum neutralized by Z2 symmetry)
        E = np.zeros_like(x)
        # Purely magnetic initial sector: Px*f = Q (E-6); on a flat slice Px=Z => f = Q/Z
        Zv = np.exp(self.alpha * phi / v)
        f = self.Q / Zv
        z = np.zeros_like(x)
        u0 = pack(dict(lnA=z.copy(), lnB=z.copy(), lnC=z.copy(),
                       HA=z.copy(), HB=z.copy(), HC=z.copy(),
                       a=z.copy(), b=z.copy(), c=z.copy(),
                       phi=phi, P=P, E=E, f=f))
        # Matter density and current (flat slice, K=0)
        vals, _ = self._geom_args(u0)
        rho = self.eqs.T['T00'](vals)
        krho = self.kappa * rho
        jx = self.eqs.T['T01'](vals)      # = P*Q + Z*E*f/B^2
        if ansatz == 'zstatic':
            # Mom: H_B + H_C = s0 (j_x=0); Ham: H_B·H_C = κρ (H_A=0)
            s0 = self.m_s0 * 2.0 * np.sqrt(np.max(krho))
            disc = s0 ** 2 - 4.0 * krho
            assert np.min(disc) > 1e-12, \
                'initial-data discriminant failed: %.3e' % np.min(disc)
            sq = np.sqrt(disc)
            HB = 0.5 * (s0 + sq)          # Larger root for y (transverse B stays finite and expands)
            HC = 0.5 * (s0 - sq)          # Smaller root for z (nearly static, contraction driven by tension)
            u0[IDX['HA']] = z.copy()
            u0[IDX['HB']] = HB
            u0[IDX['HC']] = HC
        else:
            # transverse-iso: H_A = H_B = h, h + H_C = s0, h² + 2h·H_C = κρ
            s0 = self.m_s0 * np.sqrt(np.max(krho))
            disc = s0 ** 2 - krho
            assert np.min(disc) > 1e-12, \
                'initial-data discriminant failed: %.3e' % np.min(disc)
            h = s0 - np.sqrt(disc)
            HC = np.sqrt(disc)
            u0[IDX['HA']] = h
            u0[IDX['HB']] = h.copy()
            u0[IDX['HC']] = HC
        Ham, Mom = self.constraints(u0)
        info = dict(rho0=rho, s0=float(s0), jx=jx, ansatz=ansatz,
                    Ham0_max=float(np.max(np.abs(Ham))),
                    Mom0_max=float(np.max(np.abs(Mom))),
                    krho_max=float(np.max(krho)))
        return u0, info

    def _D_matrix(self):
        """Linear-operator matrix for the periodic centered difference (sparse; corner wraparound)."""
        import scipy.sparse as sp_sp
        N = len(self.x)
        dx = self.dx
        rows = np.arange(N)
        cols_up = (rows + 1) % N
        cols_dn = (rows - 1) % N
        Dm = sp_sp.csr_matrix((np.ones(N)/(2*dx), (rows, cols_up)), shape=(N, N))
        Dm = Dm - sp_sp.csr_matrix((np.ones(N)/(2*dx), (rows, cols_dn)), shape=(N, N))
        return Dm

    def project_constraints(self, u, n_iter=3):
        """Consistent projection of both constraints (roadmap §6.1 constraint-preservation scheme; periodic domain).
        Adjust (H_B, H_C) to zero both Ham and Mom simultaneously. Linearization (per point):
          Ham: (HA+HC)*dHB + (HA+HB)*dHC = -Ham
          Mom: -D(dHB) - D(dHC) - b*dHB - c*dHC = -Mom
        (Auxiliary variables b, c are the connection coefficients -- in the machine expressions Bx = B*b.)
        Substituting the Ham relation gives a sparse linear system for w=dHC. On a periodic domain the columns of D sum to zero,
        so the Mom equations have exactly one redundant row whose sum is zero (telescoping); replace it with the gauge row Σw=0,
        and all Mom equations are still satisfied exactly (the redundancy follows from the periodic solvability condition;
        the Z2-symmetric slab gives kappa*Σ(PQ+ZEF/B²)=0)."""
        import scipy.sparse as sp_sp
        from scipy.sparse.linalg import spsolve
        N = len(self.x)
        if not hasattr(self, '_Dmat'):
            self._Dmat = self._D_matrix()
        Dm = self._Dmat
        for _ in range(n_iter):
            Ham, Mom = self.constraints(u)
            HA = u[IDX['HA']]
            HB = u[IDX['HB']]
            HC = u[IDX['HC']]
            a1 = HA + HC          # dHam/dHB
            a2 = HA + HB          # dHam/dHC
            gB = u[IDX['b']].copy()
            gC = u[IDX['c']].copy()
            inv_a1 = 1.0 / a1
            c = 1.0 - a2 * inv_a1
            rhs = -Mom - Dm @ (Ham * inv_a1) - gB * Ham * inv_a1
            Amat = -(Dm @ sp_sp.diags(c)) + sp_sp.diags(gB * a2 * inv_a1 - gC)
            # Gauge fixing: Σw = 0 (removes the constant-vector null space of D; the replaced Mom row
            # is guaranteed by periodic telescoping redundancy)
            Amat = Amat.tolil()
            Amat[0, :] = 1.0
            Amat = Amat.tocsr()
            rhs = rhs.copy()
            rhs[0] = 0.0
            w = spsolve(Amat.tocsr(), rhs)
            dHC = w
            dHB = -Ham * inv_a1 - a2 * inv_a1 * w
            u[IDX['HB']] = HB + dHB
            u[IDX['HC']] = HC + dHC
        Ham, Mom = self.constraints(u)
        return Ham, Mom

    def run(self, u0, T, cfl=0.1, dt=None, rec_every=20, project=False):
        """Evolution. With project=True, enable consistent projection of both constraints (note: under synchronous gauge +
        frozen shift, the large-scale component of the Mom residual cannot be removed by (H_B,H_C) corrections; the projection
        blows up pathologically, so it is off by default -- instead monitor the drift and report drift bounds and convergence)."""
        dt = dt if dt is not None else cfl * self.dx
        nsteps = int(round(T / dt))
        u = u0.copy()
        rec = dict(t=[0.0], u=[u.copy()], Ham=[], Mom=[])
        Ham0, Mom0 = self.constraints(u)
        rec['Ham'].append(Ham0)
        rec['Mom'].append(Mom0)
        maxCH = float(np.max(np.abs(Ham0)))
        maxMom = float(np.max(np.abs(Mom0)))
        for n in range(nsteps):
            k1 = self.rhs(u)
            k2 = self.rhs(u + 0.5*dt*k1)
            k3 = self.rhs(u + 0.5*dt*k2)
            k4 = self.rhs(u + dt*k3)
            u = u + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
            # Periodic domain: no boundary conditions (wraparound handled by the periodic difference operator)
            if project:
                self.project_constraints(u)
            Ham, Mom = self.constraints(u)
            maxCH = max(maxCH, float(np.max(np.abs(Ham))))
            maxMom = max(maxMom, float(np.max(np.abs(Mom))))
            if (n + 1) % rec_every == 0 or n == nsteps - 1:
                rec['t'].append((n + 1) * dt)
                rec['u'].append(u.copy())
                rec['Ham'].append(Ham)
                rec['Mom'].append(Mom)
        rec['t'] = np.array(rec['t'])
        rec['Ham'] = np.array(rec['Ham'])
        rec['Mom'] = np.array(rec['Mom'])
        rec['maxCH'] = maxCH
        rec['maxMom'] = maxMom
        rec['dt'] = dt
        return u, rec


# ----------------------------------------------------------------------
# Main workflow: homogeneous cross-check + bubble-wall cases + convergence
# ----------------------------------------------------------------------
def homogeneous_reference(y0, T, dt, pars):
    """Integrate the same initial data with the frozen homogeneous implementation (DCC_P2_homogeneous.py) as a reference for 1+1."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('homog', 'DCC_P2_homogeneous.py')
    hom = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hom)
    from scipy.integrate import solve_ivp
    f, eps = pars
    sol = solve_ivp(hom.rhs, (0.0, T), y0, args=(f, eps), method='RK45',
                    rtol=1e-11, atol=1e-13, dense_output=True, max_step=dt)
    return sol


def main():
    lines = []

    def w(s=''):
        print(s)
        lines.append(s)

    w('=' * 82)
    w('DCC P2 — 1+1 Planar-Symmetry ADM Coupled Solver (Bubble Wall + Geometry + Magnetic Flux)')
    w('=' * 82)
    eqs = Eqs()
    w('Machine-generated equations loaded: M/b/constraints/phiddot/Maxwell/Kretschmann/T_munu')

    # ------------------------------------------------------------------
    # V0: homogeneous cross-check (uniform phi ≡ -1, all gradients zero; compare with DCC_P2_homogeneous.py)
    # ------------------------------------------------------------------
    w('-' * 82)
    w('[V0] Homogeneous cross-check: 1+1 solver (zero-gradient limit) vs frozen homogeneous ODE implementation')
    simV = Sim(eqs, L=160.0, N=401, eps=0.0, Q=0.1)
    u0V, infoV = simV.initial_data(phi_override=-1.0)
    w('  t=0 constraints: max|Ham|=%.3e  max|Mom|=%.3e' % (infoV['Ham0_max'], infoV['Mom0_max']))
    T_V = 10.0
    uV, recV = simV.run(u0V, T_V, cfl=0.1, rec_every=50)
    w('  1+1:  max|Ham|=%.3e  max|Mom|=%.3e (t<=%.1f)'
      % (recV['maxCH'], recV['maxMom'], T_V))
    # Extract the HC(t) time series at the center point
    ic = len(simV.x) // 2
    hc_1p1 = np.array([fr[IDX['HC'], ic] for fr in recV['u']])
    # Reference: homogeneous ODE with the same initial data (f taken from the 1+1 initial F_xy to ensure identical magnetic energy)
    f_center = float(u0V[IDX['f'], ic])
    y0h = np.array([0.0, 0.0, 0.0,
                    u0V[IDX['HA'], ic], u0V[IDX['HB'], ic], u0V[IDX['HC'], ic],
                    u0V[IDX['phi'], ic], u0V[IDX['P'], ic]])
    solH = homogeneous_reference(y0h, T_V, recV['dt'], (f_center, 0.0))
    hc_ref = solH.sol(recV['t'])[5]
    dev = float(np.max(np.abs(hc_1p1 - hc_ref)))
    scale = float(np.max(np.abs(hc_ref))) + 1e-30
    w('  H_C(t) deviation: max|1+1 - ODE| = %.3e  (relative %.3e)' % (dev, dev / scale))
    V0_pass = dev / scale < 5e-3
    w('  V0 %s (threshold 5e-3 relative deviation; affected by 2nd-order differences and boundaries)'
      % ('PASS' if V0_pass else 'FAIL'))

    # ------------------------------------------------------------------
    # W1/W2/W3: vacuum-slab double walls (periodic domain)
    # ------------------------------------------------------------------
    cases = [
        dict(name='W1-slab-static', eps=0.0, Q=0.1, T=6.0),
        dict(name='W2-slab-expand', eps=0.01, Q=0.1, T=6.0),
        dict(name='W3-slab-nob', eps=0.0, Q=0.0, T=6.0),
    ]
    all_results = {}
    frames_out = {}
    for cs in cases:
        w('-' * 82)
        w('[%s] periodic L=160 N=801 dx=%.3f eps=%.2f Q=%.2f X0=20 T=%.0f'
          % (cs['name'], 160.0 / 801, cs['eps'], cs['Q'], cs['T']))
        sim = Sim(eqs, L=160.0, N=801, eps=cs['eps'], Q=cs['Q'])
        u0, info = sim.initial_data()
        w('  Initial data: s0=%.4f  krho_max=%.4f  Ham0=%.3e  Mom0=%.3e'
          % (info['s0'], info['krho_max'], info['Ham0_max'], info['Mom0_max']))
        u, rec = sim.run(u0, cs['T'], cfl=0.1, rec_every=40)
        w('  Final state: max|Ham|=%.3e  max|Mom|=%.3e  (overall)'
          % (rec['maxCH'], rec['maxMom']))
        # Observable time series (inside the slab at x≈0 (true vacuum) and outside at x≈±60 (false vacuum))
        ic = len(sim.x) // 2
        ivac = int(np.argmin(np.abs(sim.x - 60.0)))  # Outer false-vacuum region
        tarr = rec['t']
        HCc = np.array([fr[IDX['HC'], ic] for fr in rec['u']])
        HAv = np.array([fr[IDX['HA'], ic] for fr in rec['u']])
        HCv = np.array([fr[IDX['HC'], ivac] for fr in rec['u']])
        HAv2 = np.array([fr[IDX['HA'], ivac] for fr in rec['u']])
        CC = np.exp(np.array([fr[IDX['lnC'], ic] for fr in rec['u']]))
        AC = np.exp(np.array([fr[IDX['lnA'], ic] for fr in rec['u']]))
        Cv_ = np.exp(np.array([fr[IDX['lnC'], ivac] for fr in rec['u']]))
        Av_ = np.exp(np.array([fr[IDX['lnA'], ivac] for fr in rec['u']]))
        # L2: Cddot/C = dHC + HC^2 (using the final-frame rhs)
        dHend = sim.rhs(u)[IDX['HC']]
        CddC_end = dHend + u[IDX['HC']] ** 2
        # NEC/WEC (final frame + sampling over all frames)
        nec_min = np.inf
        wec_min = np.inf
        for fr, Ham in zip(rec['u'][::4], rec['Ham'][::4]):
            rho, px, py, pz = sim.orthonormal_stress(fr)
            nec = np.minimum(np.minimum(rho + px, rho + py), rho + pz)
            nec_min = min(nec_min, float(np.min(nec)))
            wec_min = min(wec_min, float(np.min(np.minimum(rho, nec))))
        # Kretschmann at the final frame
        dHf = sim.rhs(u)
        K = sim.kretschmann(u, np.stack([dHf[IDX['HA']], dHf[IDX['HB']],
                                         dHf[IDX['HC']]]))
        w('  Wall center:   H_C(min)=%.4e  H_C(end)=%.4e  C/A(end)=%.4e'
          % (float(np.min(HCc)), HCc[-1], CC[-1] / AC[-1]))
        w('  True-vac region: H_C(min)=%.4e  H_C(end)=%.4e  C/A(end)=%.4e'
          % (float(np.min(HCv)), HCv[-1], Cv_[-1] / Av_[-1]))
        w('  D1 (wall center, any t)=%s  D2 (wall center, any t)=%s  D2 (true-vac region)=%s'
          % (bool(np.any(HCc < HAv)), bool(np.any(HCc < 0)),
             bool(np.any(HCv < 0))))
        w('  L2: Cddot/C(end) wall center=%.3e  true vacuum=%.3e  min=%.3e  max=%.3e'
          % (CddC_end[ic], CddC_end[ivac], float(np.min(CddC_end)),
             float(np.max(CddC_end))))
        w('  K(end): max=%.3e @x=%.1f   NEC_min=%.3e  WEC_min=%.3e'
          % (float(np.max(K)), sim.x[int(np.argmax(K))], nec_min, wec_min))
        all_results[cs['name']] = dict(sim=sim, rec=rec, x=sim.x,
                                       HCc=HCc, HAv=HAv, HCv=HCv, CC=CC, AC=AC)
        frames_out[cs['name']] = dict(t=rec['t'], x=sim.x,
                                      u=np.stack(rec['u'], axis=0),
                                      Ham=rec['Ham'], Mom=rec['Mom'])
        # Save one case's fields for plotting
        if cs['name'] == 'W1-slab-static':
            W1 = dict(sim=sim, rec=rec)

    np.savez_compressed('DCC_P2_1p1_frames.npz', **frames_out)

    # ------------------------------------------------------------------
    # Convergence test (W1, T=20, dx halved)
    # ------------------------------------------------------------------
    w('-' * 82)
    w('[CONV] W1 convergence: dx=0.4/0.2/0.1 (dt=0.2dx), T=20, self-convergence order')
    conv = []
    for N in [401, 801, 1601]:
        simc = Sim(eqs, L=160.0, N=N, eps=0.0, Q=0.1)
        u0c, _ = simc.initial_data()
        uc, recc = simc.run(u0c, 6.0, cfl=0.1, rec_every=1000000)
        conv.append(dict(N=N, dx=simc.dx, u=uc, sim=simc, rec=recc))
        w('  N=%4d dx=%.3f  final-frame |Ham|=%.3e |Mom|=%.3e' % (
            N, simc.dx, np.max(np.abs(recc['Ham'][-1])), np.max(np.abs(recc['Mom'][-1]))))
    # Self-convergence: coarse-minus-fine difference sampled on the fine grid
    def interp_to(y, x_src, x_dst):
        return np.interp(x_dst, x_src, y)
    orders = {}
    for key, idxx in [('lnC', IDX['lnC']), ('phi', IDX['phi']), ('HC', IDX['HC'])]:
        u_c, u_m, u_f = conv[0]['u'], conv[1]['u'], conv[2]['u']
        x_c, x_m, x_f = conv[0]['sim'].x, conv[1]['sim'].x, conv[2]['sim'].x
        cm = u_c[idxx] - interp_to(u_m[idxx], x_m, x_c)
        mf = u_m[idxx] - interp_to(u_f[idxx], x_f, x_m)
        n = min(len(cm), len(mf))
        r = float(np.max(np.abs(cm[:n]))) / (float(np.max(np.abs(mf[:n]))) + 1e-30)
        order = np.log2(r) if r > 0 else float('nan')
        orders[key] = (r, order)
        w('  %s: coarse/fine difference ratio=%.3f  self-convergence order=%.2f' % (key, r, order))

    # ------------------------------------------------------------------
    # Plots
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    ax = axes.ravel()
    simW = W1['sim']
    recW = W1['rec']
    snaps = [0, len(recW['t']) // 3, 2 * len(recW['t']) // 3, len(recW['t']) - 1]
    for k, si in enumerate(snaps[:4]):
        fr = recW['u'][si]
        ax[0].plot(simW.x, np.exp(fr[IDX['lnC']]),
                   label='t=%.1f' % recW['t'][si])
    ax[0].set_title('W1: C(t,x)')
    ax[0].set_xlabel('x'); ax[0].legend(); ax[0].grid(alpha=0.3)
    for k, si in enumerate(snaps[:4]):
        fr = recW['u'][si]
        ax[1].plot(simW.x, np.exp(fr[IDX['lnA']]), label='t=%.1f' % recW['t'][si])
    ax[1].set_title('W1: A(t,x)')
    ax[1].set_xlabel('x'); ax[1].legend(); ax[1].grid(alpha=0.3)
    ax[2].plot(recW['t'], frames_out['W1-slab-static']['Ham'].max(axis=1) if False else
               np.max(np.abs(frames_out['W1-slab-static']['Ham']), axis=1),
               label='Ham')
    ax[2].plot(recW['t'], np.max(np.abs(frames_out['W1-slab-static']['Mom']), axis=1),
               '--', label='Mom')
    ax[2].set_yscale('log'); ax[2].set_title('W1: constraint residuals')
    ax[2].set_xlabel('t'); ax[2].legend(); ax[2].grid(alpha=0.3)
    rW = all_results['W1-slab-static']
    ax[3].plot(rW['rec']['t'], rW['HCc'], label=r'$H_C$ wall center')
    ax[3].plot(rW['rec']['t'], rW['HAv'], '--', label=r'$H_A$ wall center')
    ax[3].plot(rW['rec']['t'], rW['HCv'], ':', label=r'$H_C$ true-vac')
    ax[3].axhline(0, color='k', lw=0.5)
    ax[3].set_title('W1: expansion rates'); ax[3].set_xlabel('t')
    ax[3].legend(); ax[3].grid(alpha=0.3)
    ax[4].plot(rW['rec']['t'], rW['CC'] / rW['AC'], label='C/A wall center')
    ax[4].set_yscale('log'); ax[4].set_title('W1: C/A')
    ax[4].set_xlabel('t'); ax[4].legend(); ax[4].grid(alpha=0.3)
    # The same HC curve is plotted on ax[3]; here plot the moving wall
    rM = all_results['W2-slab-expand']
    ax[5].plot(rM['rec']['t'], rM['HCv'], label=r'$H_C$ true-vac (moving)')
    ax[5].axhline(0, color='k', lw=0.5)
    ax[5].set_title('W2: H_C true-vac region'); ax[5].set_xlabel('t')
    ax[5].legend(); ax[5].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig('DCC_P2_1p1_profiles.png', dpi=140)
    plt.close(fig)

    with open('DCC_P2_1p1_results.txt', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    w('')
    w('Wrote DCC_P2_1p1_results.txt / DCC_P2_1p1_profiles.png / DCC_P2_1p1_frames.npz')


if __name__ == '__main__':
    main()
