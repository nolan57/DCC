#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DCC P2 — Spherically symmetric (B=C=R) coupled solver: spherical bubble wall + geometry
====================================================

Metric (synchronous gauge N=1)
    ds^2 = -dt^2 + A(t,r)^2 dr^2 + R(t,r)^2 (dθ^2 + sin^2θ dφ^2)

Evolution variables (8 per grid point)
    lnA, lnR, KA=Ȧ/A, KR=Ṙ/R, a=∂r(lnA), q=∂r(lnR), phi, P=φ̇

Equations (machine-generated: <<<EQS-JSON>>> block of DCC_P2_sph_derivation.py)
    d(lnA)=KA, d(lnR)=KR; da=D(KA), dq=D(KR)
    (dKA,dKR) = M^{-1}*(-b)     [G_rr, G_θθ = κ T_rr, T_θθ]
    dP = phiddot                [□φ - V' = 0]
    Constraints (diagnostic): Ham = G_00 - κT_00, Mom = G_0r - κT_0r
    No Maxwell sector: a uniform F_xy flux breaks spherical symmetry and a spherically symmetric
    magnetic field violates ∇·B=0 (P0 conclusion), so this case verifies Einstein-scalar-wall coupling (roadmap §6.5-6).

Initial data (time-symmetric slice K=0; Mom automatically satisfied)
    R(0,r)=r (areal), φ(0,r)=v·tanh(a_w(r-R0)) (true vacuum -v inside the bubble, +v outside)
    The nonlinear ODE for A(r) from the Hamiltonian constraint R^(3)=2κρ is solved by Newton (tridiagonal):
    inner boundary A'(0)=0 (regularity), outer boundary A(r_max)=1.

Numerics: RK4 + 2nd-order centered differences; regular at r=0 (zero gradient), zero-gradient outer boundary;
    A-Newton projection every 50 steps (the spherical Mom is independent of A, so the projection does not spoil Mom).

Run: python DCC_P2_wall_sph.py
Output: DCC_P2_sph_results.txt / DCC_P2_sph_profiles.png / DCC_P2_sph_frames.npz
"""
import json
import re
import numpy as np
import sympy as sp
from sympy.core.function import AppliedUndef
from sympy.parsing.sympy_parser import parse_expr
from scipy.linalg import solve_banded
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ARG_NAMES = ['A', 'Ax', 'Axx', 'R', 'Rx', 'Rxx',
             'KA', 'KR', 'KAx', 'KRx',
             'phi', 'P', 'Q', 'Qx',
             'dKA', 'dKR', 'lam', 'v', 'eps', 'kappa']
ARG_SYMS = [sp.Symbol(nm) for nm in ARG_NAMES]
_FIELD_NAMES = {'A', 'R', 'phi', 'KA', 'KR', 'dKA', 'dKR', 'P', 'Q', 'Qx'}


def load_json_block(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        txt = fh.read()
    m = re.search(r'<<<EQS-JSON-BEGIN>>>\s*\n(.*?)\n?<<<EQS-JSON-END>>>', txt, re.S)
    if not m:
        raise RuntimeError('EQS-JSON block not found in %s' % path)
    return json.loads(m.group(1).strip())


def flatten(e):
    reps = {}
    for fn in e.atoms(AppliedUndef):
        nm = str(fn.func)
        if nm in _FIELD_NAMES:
            reps[fn] = sp.Symbol(nm)
    for s in e.atoms(sp.Symbol):
        if s.name in ARG_NAMES and s != sp.Symbol(s.name):
            reps[s] = sp.Symbol(s.name)
    return e.xreplace(reps)


def build_func(srepr_str, allow_dK=False):
    e = flatten(parse_expr(srepr_str))
    if not allow_dK:
        for nm in ('dKA', 'dKR'):
            assert not e.has(sp.Symbol(nm)), 'unexpected %s' % nm
    used = [s for s in ARG_SYMS if e.has(s)]
    f = sp.lambdify(used, e, 'numpy')
    idx = [ARG_NAMES.index(str(s)) for s in used]

    def wrapper(vals):
        return f(*[vals[i] for i in idx])
    return wrapper


def D(f, dx):
    return np.gradient(f, dx, edge_order=2)


IDX = dict(lnA=0, lnR=1, KA=2, KR=3, a=4, q=5, phi=6, P=7)
NF = 8


def pack(d):
    u = np.empty((NF,) + d['lnA'].shape)
    for k, i in IDX.items():
        u[i] = d[k]
    return u


class Sim(object):
    def __init__(self, eqs, payload, L=60.0, N=601, kappa=1.0, lam=1.0,
                 v=1.0, eps=0.0, R0=20.0, r_min=1.0):
        self.eqs = eqs
        self.payload = payload
        # The areal gauge R=r is coordinate-singular at r=0 (q=1/r, 1/R² terms) -- the grid starts at r_min
        self.x = np.linspace(r_min, L, N)
        self.dx = self.x[1] - self.x[0]
        self.kappa, self.lam, self.v = kappa, lam, v
        self.eps, self.R0 = eps, R0
        self._ham_op = None

    def _args(self, u):
        A = np.exp(u[IDX['lnA']]); R = np.exp(u[IDX['lnR']])
        KA, KR = u[IDX['KA']], u[IDX['KR']]
        a, q = u[IDX['a']], u[IDX['q']]
        phi, P = u[IDX['phi']], u[IDX['P']]
        Ax = A * a; Rx = R * q
        ax = D(a, self.dx); qx = D(q, self.dx)
        Axx = Ax * a + A * ax
        Rxx = Rx * q + R * qx
        Q = D(phi, self.dx); Qx = D(Q, self.dx)
        KAx = D(KA, self.dx); KRx = D(KR, self.dx)
        zero = np.zeros_like(A)
        vals = [A, Ax, Axx, R, Rx, Rxx, KA, KR, KAx, KRx,
                phi, P, Q, Qx, zero, zero,
                self.lam, self.v, self.eps, self.kappa]
        return vals, dict(A=A, R=R, KA=KA, KR=KR, phi=phi, P=P, Q=Q)

    def rhs(self, u):
        vals, aux = self._args(u)
        Mm = np.empty((2, 2) + vals[0].shape)
        bb = np.empty((2,) + vals[0].shape)
        for i in range(2):
            for j in range(2):
                Mm[i, j] = self.eqs.M[i][j](vals)
            bb[i] = -self.eqs.b[i](vals)   # dK = M^{-1}*(-b)
        dK = np.linalg.solve(np.moveaxis(Mm, 2, 0), bb.T[:, :, None])[:, :, 0].T
        d = np.empty_like(u)
        d[IDX['lnA']], d[IDX['lnR']] = aux['KA'], aux['KR']
        d[IDX['KA']], d[IDX['KR']] = dK[0], dK[1]
        d[IDX['a']], d[IDX['q']] = D(aux['KA'], self.dx), D(aux['KR'], self.dx)
        d[IDX['phi']] = aux['P']
        d[IDX['P']] = self.eqs.phiddot(vals)
        return d

    def constraints(self, u):
        vals, _ = self._args(u)
        return self.eqs.Ham(vals), self.eqs.Mom(vals)

    def kretschmann(self, u):
        vals, _ = self._args(u)
        d = self.rhs(u)
        full = vals[:14] + [d[IDX['KA']], d[IDX['KR']]] + vals[16:]
        return self.eqs.Kret(full)

    def orthonormal_stress(self, u):
        vals, _ = self._args(u)
        rho = self.eqs.T['T00'](vals)
        pr = self.eqs.T['T11'](vals) / vals[0] ** 2
        pth = self.eqs.T['T22'](vals) / vals[3] ** 2
        return rho, pr, pth

    # ---------- Time-symmetric-slice initial data: K=0, Newton solve for A(r) from R^(3)=2κρ ----------
    def _ham_A_ops(self):
        """K=0 form of the machine-generated Ham and its partial derivatives w.r.t. (A, Ax, Axx) (lambdified)."""
        if self._ham_op is not None:
            return self._ham_op
        e = flatten(parse_expr(self.payload['Ham']))
        Ham0 = build_func(self.payload['Ham'])
        JA = build_func(sp.srepr(sp.diff(e, sp.Symbol('A'))))
        JAx = build_func(sp.srepr(sp.diff(e, sp.Symbol('Ax'))))
        JAxx = build_func(sp.srepr(sp.diff(e, sp.Symbol('Axx'))))
        self._ham_op = (Ham0, JA, JAx, JAxx)
        return self._ham_op

    def _set_A(self, u, A):
        u[IDX['lnA']] = np.log(A)
        u[IDX['a']] = D(np.log(A), self.dx)

    def _newton_A(self, u, A, n_iter=200, tol=1e-13):
        dx = self.dx
        Ham0, JA, JAx, JAxx = self._ham_A_ops()
        res_hist = []
        for it in range(n_iter):
            self._set_A(u, A)
            vals, _ = self._args(u)
            res = np.asarray(Ham0(vals), dtype=float)
            res_hist.append(float(np.max(np.abs(res))))
            if not np.all(np.isfinite(res)):
                raise RuntimeError('Newton residual non-finite at it=%d' % it)
            if res_hist[-1] < tol:
                break
            JAv = np.asarray(JA(vals), dtype=float)
            JAxv = np.asarray(JAx(vals), dtype=float)
            JAxxv = np.asarray(JAxx(vals), dtype=float)
            ab = np.zeros((3, len(A)))
            ab[1, :] = JAv - 2 * JAxxv / dx ** 2
            ab[0, 1:] = (JAxxv / dx ** 2 + JAxv / (2 * dx))[:-1]
            ab[2, :-1] = (JAxxv / dx ** 2 - JAxv / (2 * dx))[1:]
            rhs_v = -res
            ab[1, 0] = 1.0; ab[0, 1] = -1.0; ab[2, 0] = 0.0; ab[0, 0] = 0.0
            rhs_v[0] = 0.0                    # r=0: A'(0)=0 (regularity)
            ab[1, -1] = 1.0; ab[0, -1] = 0.0; ab[2, -1] = 0.0
            rhs_v[-1] = 1.0 - A[-1]           # outer boundary A=1
            dA = solve_banded((1, 1), ab, rhs_v)
            # Damped Newton: step limiting (|dA| ≤ 0.3|A|) to suppress overshoot from the linearized first-order ODE
            dA = np.clip(dA, -0.3 * np.abs(A), 0.3 * np.abs(A))
            A = A + dA
        return A, it + 1, res_hist[-3:]

    def initial_data(self):
        x, dx, v, lam = self.x, self.dx, self.v, self.lam
        aw = v * np.sqrt(lam / 2.0)
        phi = v * np.tanh(aw * (x - self.R0))   # -v inside the bubble, +v outside
        z = np.zeros_like(x)
        u = pack(dict(lnA=np.log(np.ones_like(x)), lnR=np.log(x),
                      KA=z.copy(), KR=z.copy(),
                      a=z.copy(), q=1.0 / x,
                      phi=phi, P=z.copy()))
        A0 = np.ones_like(x)
        A, n_it, rh = self._newton_A(u, A0)
        self._set_A(u, A)
        u[IDX['KA']] = z.copy()
        u[IDX['KR']] = z.copy()
        Ham, Mom = self.constraints(u)
        info = dict(newton_iters=n_it, res_hist=rh,
                    Ham0_max=float(np.max(np.abs(Ham))),
                    Mom0_max=float(np.max(np.abs(Mom))),
                    A_center=float(A[0]),
                    A_wall=float(A[int(np.argmin(np.abs(x - self.R0)))]))
        return u, info

    def project_A(self, u, n_iter=2):
        """A-Newton projection (the spherical Mom is independent of A and is unaffected)."""
        dx = self.dx
        A = np.exp(u[IDX['lnA']])
        Ham0, JA, JAx, JAxx = self._ham_A_ops()
        for it in range(n_iter):
            self._set_A(u, A)
            vals, _ = self._args(u)
            res = np.asarray(Ham0(vals), dtype=float)
            JAv = np.asarray(JA(vals), dtype=float)
            JAxv = np.asarray(JAx(vals), dtype=float)
            JAxxv = np.asarray(JAxx(vals), dtype=float)
            ab = np.zeros((3, len(A)))
            ab[1, :] = JAv - 2 * JAxxv / dx ** 2
            ab[0, 1:] = (JAxxv / dx ** 2 + JAxv / (2 * dx))[:-1]
            ab[2, :-1] = (JAxxv / dx ** 2 - JAxv / (2 * dx))[1:]
            rhs_v = -res
            ab[1, 0] = 1.0; ab[0, 1] = -1.0; ab[2, 0] = 0.0; ab[0, 0] = 0.0
            rhs_v[0] = 0.0
            ab[1, -1] = 1.0; ab[0, -1] = 0.0; ab[2, -1] = 0.0
            rhs_v[-1] = 1.0 - A[-1] if it == 0 else 0.0
            A = A + solve_banded((1, 1), ab, rhs_v)
        self._set_A(u, A)
        Ham, Mom = self.constraints(u)
        return Ham, Mom

    def run(self, u0, T, cfl=0.1, rec_every=25, proj_every=50):
        dt = cfl * self.dx
        nsteps = int(round(T / dt))
        u = u0.copy()
        rec = dict(t=[0.0], u=[u.copy()], Ham=[], Mom=[])
        Ham0, Mom0 = self.constraints(u)
        rec['Ham'].append(Ham0); rec['Mom'].append(Mom0)
        maxCH = float(max(np.max(np.abs(Ham0)), np.max(np.abs(Mom0))))
        for n in range(nsteps):
            k1 = self.rhs(u)
            k2 = self.rhs(u + 0.5 * dt * k1)
            k3 = self.rhs(u + 0.5 * dt * k2)
            k4 = self.rhs(u + dt * k3)
            u = u + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            u[:, 0] = u[:, 1]        # regular at r=0
            u[:, -1] = u[:, -2]      # zero-gradient outer boundary
            if (n + 1) % proj_every == 0:
                Ham, Mom = self.project_A(u)
            else:
                Ham, Mom = self.constraints(u)
            maxCH = max(maxCH, float(max(np.max(np.abs(Ham)),
                                         np.max(np.abs(Mom)))))
            if (n + 1) % rec_every == 0 or n == nsteps - 1:
                rec['t'].append((n + 1) * dt)
                rec['u'].append(u.copy())
                rec['Ham'].append(Ham); rec['Mom'].append(Mom)
        rec['t'] = np.array(rec['t'])
        rec['Ham'] = np.array(rec['Ham']); rec['Mom'] = np.array(rec['Mom'])
        rec['maxCH'] = maxCH; rec['dt'] = dt
        return u, rec


def main():
    lines = []

    def w(s=''):
        print(s)
        lines.append(s)

    w('=' * 82)
    w('DCC P2 — Spherically symmetric (B=C=R) coupled solver: spherical bubble wall + geometry')
    w('=' * 82)
    payload = load_json_block('sympy_sph_stdout.txt')
    eqs = type('Eqs', (), {})()
    eqs.Ham = build_func(payload['Ham'])
    eqs.Mom = build_func(payload['Mom'])
    eqs.M = [[build_func(payload['M'][i][j]) for j in range(2)] for i in range(2)]
    eqs.b = [build_func(payload['b'][i]) for i in range(2)]
    eqs.phiddot = build_func(payload['phiddot'])
    eqs.Kret = build_func(payload['Kretschmann'], allow_dK=True)
    eqs.T = {k: build_func(payload[k]) for k in ('T00', 'T01', 'T11', 'T22')}
    w('Machine-generated equations loaded (Ham/Mom/M/b/phiddot/Kretschmann/T)')

    # ------------------------------------------------------------------
    # S1/S2: spherical bubble wall (static / ε expansion)
    # ------------------------------------------------------------------
    cases = [
        dict(name='S1-static', eps=0.0, T=15.0),
        dict(name='S2-expand', eps=0.01, T=15.0),
    ]
    frames_out = {}
    S1 = None
    for cs in cases:
        w('-' * 82)
        w('[%s] eps=%.2f R0=20 r∈[0,60] N=601 T=%.0f' % (cs['name'], cs['eps'], cs['T']))
        sim = Sim(eqs, payload, L=60.0, N=601, eps=cs['eps'], R0=20.0)
        u0, info = sim.initial_data()
        w('  Initial data: Newton %d iterations, residual tail=%s |Ham|=%.2e |Mom|=%.2e A(center)=%.4f A(wall)=%.4f' % (
            info['newton_iters'], ['%.1e' % v for v in info['res_hist']],
            info['Ham0_max'], info['Mom0_max'], info['A_center'], info['A_wall']))
        u, rec = sim.run(u0, cs['T'], cfl=0.1, rec_every=25, proj_every=50)
        w('  t=%.0f: max|Ham|=%.2e max|Mom|=%.2e (overall max=%.2e)' % (
            cs['T'], np.max(np.abs(rec['Ham'][-1])), np.max(np.abs(rec['Mom'][-1])),
            rec['maxCH']))
        iw = int(np.argmin(np.abs(sim.x - 20.0)))
        rw = []
        for fr in rec['u']:
            ph = fr[IDX['phi']]
            idx = np.where(np.diff(np.sign(ph)))[0]
            rw.append(sim.x[idx[0]] if len(idx) else float('nan'))
        rw = np.array(rw)
        KRw = np.array([fr[IDX['KR'], iw] for fr in rec['u']])
        Rw = np.exp(np.array([fr[IDX['lnR'], iw] for fr in rec['u']]))
        rho, pr, pth = sim.orthonormal_stress(u)
        K = sim.kretschmann(u)
        nec = np.minimum(rho + pr, rho + pth)
        w('  Wall position r_w: %.3f -> %.3f (mean velocity≈%.4f)' % (
            rw[0], rw[-1], (rw[-1] - rw[0]) / (rec['t'][-1] - rec['t'][0])))
        w('  KR(t) at the wall: %s' % ['%.4f' % v_ for v_ in KRw[::5]])
        w('  R(t)/R0 at the wall: %s' % ['%.4f' % v_ for v_ in (Rw / Rw[0])[::5]])
        w('  K_max=%.3e @r=%.1f  NEC_min=%.3e  WEC_min=%.3e' % (
            float(np.max(K)), sim.x[int(np.argmax(K))], float(np.min(nec)),
            float(np.min(np.minimum(rho, nec)))))
        frames_out[cs['name']] = dict(t=rec['t'], r=sim.x,
                                      u=np.stack(rec['u'], axis=0),
                                      Ham=rec['Ham'], Mom=rec['Mom'])
        if cs['name'] == 'S1-static':
            S1 = dict(sim=sim, rec=rec, rw=rw)

    np.savez_compressed('DCC_P2_sph_frames.npz', **frames_out)

    # ------------------------------------------------------------------
    # Convergence (S1, T=8, dx halved)
    # ------------------------------------------------------------------
    w('-' * 82)
    w('[CONVs] S1 convergence: N=301/601/1201 (dx=0.2/0.1/0.05), T=8, self-convergence order')
    conv = []
    for N in (301, 601, 1201):
        simc = Sim(eqs, payload, L=60.0, N=N, eps=0.0, R0=20.0)
        u0c, _ = simc.initial_data()
        uc, recc = simc.run(u0c, 8.0, cfl=0.1, rec_every=10 ** 9, proj_every=50)
        conv.append(dict(N=N, dx=simc.dx, u=uc, sim=simc))
        w('  N=%4d dx=%.3f final-frame |Ham|=%.2e |Mom|=%.2e' % (
            N, simc.dx, np.max(np.abs(recc['Ham'][-1])), np.max(np.abs(recc['Mom'][-1]))))

    def interp_to(y, x_src, x_dst):
        return np.interp(x_dst, x_src, y)

    for key, idxx in (('lnR', IDX['lnR']), ('phi', IDX['phi'])):
        u_c, u_m, u_f = conv[0]['u'], conv[1]['u'], conv[2]['u']
        x_c, x_m, x_f = conv[0]['sim'].x, conv[1]['sim'].x, conv[2]['sim'].x
        cm = u_c[idxx] - interp_to(u_m[idxx], x_m, x_c)
        mf = u_m[idxx] - interp_to(u_f[idxx], x_f, x_m)
        nn = min(len(cm), len(mf))
        r_ = float(np.max(np.abs(cm[:nn]))) / (float(np.max(np.abs(mf[:nn]))) + 1e-30)
        order = np.log2(r_) if r_ > 0 else float('nan')
        w('  %s: coarse/fine difference ratio=%.3f  self-convergence order=%.2f' % (key, r_, order))

    # ------------------------------------------------------------------
    # Plots
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    simW = S1['sim']
    recW = S1['rec']
    snaps = [0, len(recW['t']) // 3, 2 * len(recW['t']) // 3, len(recW['t']) - 1]
    for si in snaps:
        fr = recW['u'][si]
        axes[0].plot(simW.x, np.exp(fr[IDX['lnR']]), label='t=%.1f' % recW['t'][si])
        axes[1].plot(simW.x, np.exp(fr[IDX['lnA']]), label='t=%.1f' % recW['t'][si])
        axes[2].plot(simW.x, fr[IDX['phi']], label='t=%.1f' % recW['t'][si])
    axes[0].set_title('S1: R(t,r)'); axes[1].set_title('S1: A(t,r)')
    axes[2].set_title('S1: phi(t,r)')
    for ax in axes:
        ax.set_xlabel('r'); ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig('DCC_P2_sph_profiles.png', dpi=140)
    plt.close(fig)

    with open('DCC_P2_sph_results.txt', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    w('')
    w('Wrote DCC_P2_sph_results.txt / DCC_P2_sph_profiles.png / DCC_P2_sph_frames.npz')


if __name__ == '__main__':
    main()
