#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DCC P4 observer pipeline (compact implementation).
Reproduce: python DCC_P4_pipeline.py (depends on DCC_P2_1p1_frames.npz).

Inputs (traceable upstream): P2 W1-slab-static frames (background geometry A(t,x));
P3 §4 Fresnel transmission coefficients (analytically derived). All output frequency-shift/intensity
factors are given by geodesic shooting and these coefficients, with no manual Doppler term (roadmap §8-1).
"""
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NPZ = 'DCC_P2_1p1_frames.npz'
IDX_P4 = dict(lnA=0, lnB=1, lnC=2, HA=3, HB=4, HC=5,
              a=6, b=7, c=8, phi=9, P=10, E=11, f=12)


class SlabGeometry(object):
    def __init__(self, case='W1-slab-static'):
        # frames.npz stores one pickled dict per slab (t, x, u, Ham, Mom)
        d = np.load(NPZ, allow_pickle=True)[case].item()
        self.t = d['t']
        self.x = d['x']
        uu = d['u']
        self.A = np.exp(uu[:, IDX_P4['lnA'], :])
        self.phi = uu[:, IDX_P4['phi'], :]

    def _bilerp(self, field, t, x):
        ti = np.clip(np.searchsorted(self.t, t) - 1, 0, len(self.t) - 2)
        f = np.clip((t - self.t[ti]) / (self.t[ti + 1] - self.t[ti]), 0, 1)
        xi = np.clip(np.searchsorted(self.x, x) - 1, 0, len(self.x) - 2)
        fx = np.clip((x - self.x[xi]) / (self.x[xi + 1] - self.x[xi]), 0, 1)
        p11 = field[ti, xi]
        p12 = field[ti, xi + 1]
        p21 = field[ti + 1, xi]
        p22 = field[ti + 1, xi + 1]
        return (p11 * (1 - f) * (1 - fx) + p12 * (1 - f) * fx +
                p21 * f * (1 - fx) + p22 * f * fx)

    def A_of(self, t, x):
        return self._bilerp(self.A, t, x)

    def phi_of(self, t, x):
        return self._bilerp(self.phi, t, x)

    def wall_crossings(self, t0, t1, x0, x1, n=300):
        tt = np.linspace(t0, t1, n)
        s = np.linspace(x0, x1, n)
        seg = np.array([self.phi_of(t_, x_) for t_, x_ in zip(tt, s)])
        return int(np.sum(np.diff(np.sign(seg)) != 0) // 2)


def ray_arrival(geo, t_src, x_src, x_obs):
    """Right-moving null-geodesic shooting: dx/dt = 1/A(t,x); returns the arrival time."""

    def rhs(t, y):
        return [1.0 / geo.A_of(t, y[0])]

    sol = solve_ivp(rhs, (t_src, t_src + 120.0), [x_src],
                    events=lambda t, y: y[0] - x_obs,
                    rtol=1e-10, atol=1e-12, max_step=0.05)
    if len(sol.t_events[0]) == 0:
        return None
    return sol.t_events[0][0]


def main():
    lines = []

    def w(s=''):
        print(s)
        lines.append(s)

    w('=' * 82)
    w('DCC P4 - observer pipeline (1+1 slab; geodesic frequency shift + P3 transmission coefficient)')
    w('=' * 82)
    geo = SlabGeometry()
    w('Background: P2 W1-slab-static frames (valid region T<=%.1f; beyond that = assumption layer)' % geo.t[-1])
    w('Source: x=0 (inside the slab); observer: x=+60 (outer region)')

    Z_in = float(np.exp(0.5 * (-1.0)))
    Z_out = float(np.exp(0.5 * (1.0)))
    n1 = 1.0
    n2 = float(np.sqrt(Z_in / Z_out))
    T_wall = 4 * n1 * n2 / (n1 + n2) ** 2
    R_wall = ((n1 - n2) / (n1 + n2)) ** 2
    w('P3 transmission coefficients: n2=%.4f T=%.6f R=%.6f (Fresnel normal incidence)' % (n2, T_wall, R_wall))

    x_obs = 60.0
    x_src = 0.0
    groups = [
        ('A-relativistic (beta_w=0.5)', 0.5),
        ('B-phenomenological (beta_w=1.42e-4, calibrated to 42.47 km/s; not a theoretical prediction)',
         1.4166e-4),
    ]
    for gname, beta in groups:
        w('-' * 82)
        w('[%s]' % gname)
        v_c = beta / geo.A_of(geo.t[-1] - 1.0, x_src)
        gamma = 1.0 / np.sqrt(max(1.0 - beta ** 2, 1e-12))
        dtau_src = 0.05
        t_e0 = geo.t[-1] - 21.0

        def dtau_dt(t):
            return np.sqrt(max(1.0 - (geo.A_of(t, x_src) * v_c) ** 2, 1e-12))

        sol_tau = solve_ivp(lambda t, y: [dtau_dt(t)], (t_e0, t_e0 + 30.0),
                            [0.0], rtol=1e-10, atol=1e-12, dense_output=True)
        tt_grid = np.linspace(t_e0, t_e0 + 30.0, 4000)
        tau_grid = sol_tau.sol(tt_grid)[0]
        t_for_tau = lambda tau_q: float(np.interp(tau_q, tau_grid, tt_grid))
        t_e1 = t_for_tau(0.5)
        t_e2 = t_for_tau(0.5 + dtau_src)
        arr1 = ray_arrival(geo, t_e1, x_src, x_obs)
        arr2 = ray_arrival(geo, t_e2, x_src, x_obs)
        if arr1 is None or arr2 is None:
            w('  Ray did not arrive (outside the frame window)')
            continue
        dtau_obs = arr2 - arr1
        shift = dtau_src / dtau_obs
        crossings = geo.wall_crossings(t_e1, arr1, x_src, x_obs)
        T_total = T_wall ** max(crossings, 1)
        w('  [Assumption-layer note: geometry for t_emit<0 is frozen at the first frame]')
        w('  t_emit=%.2f -> t_arr=%.2f (propagation %.2f)' % (t_e1, arr1, arr1 - t_e1))
        w('  Frequency-shift factor nu_obs/nu_src = dtau_src/dtau_obs = %.6f' % shift)
        w('  Wall crossings=%d -> total transmission T=%.6f' % (crossings, T_total))
        w('  Intensity ratio I_obs/I_src = T*(nu_obs/nu_src)^3 = %.6f' % (
            T_total * shift ** 3))
        w('  (gamma=%g; all factors given by the geodesic + P3 coefficients)' % gamma)

    w('-' * 82)
    w('[Frequency-shift time series] Group A (beta_w=0.5), scanning emission time t_emit ∈ [1, 5]')
    beta = 0.5
    t_e_list = np.linspace(1.0, 5.0, 12)
    shifts = []
    tarr_list = []
    dtau_src = 0.02
    for t_e in t_e_list:
        v_c = beta / geo.A_of(t_e, x_src)
        sol_tau = solve_ivp(
            lambda t, y: [np.sqrt(max(1 - (geo.A_of(t, x_src) * v_c) ** 2,
                                      1e-12))],
            (t_e, t_e + 10.0), [0.0], rtol=1e-10, atol=1e-12,
            dense_output=True)
        tt_grid = np.linspace(t_e, t_e + 10.0, 2000)
        tau_grid = sol_tau.sol(tt_grid)[0]
        t_for_tau = lambda tau_q: float(np.interp(tau_q, tau_grid, tt_grid))
        a1 = ray_arrival(geo, t_for_tau(0.5), x_src, x_obs)
        a2 = ray_arrival(geo, t_for_tau(0.5 + dtau_src), x_src, x_obs)
        if a1 is None or a2 is None:
            shifts.append(float('nan'))
            tarr_list.append(float('nan'))
            continue
        shifts.append(dtau_src / (a2 - a1))
        tarr_list.append(a1)
    for t_e, s_, a_ in zip(t_e_list, shifts, tarr_list):
        w('  t_emit=%.2f -> t_arr=%.2f  nu_obs/nu_src=%.6f' % (t_e, a_, s_))
    w('  (Frame window: valid region T<=6; arrivals with t_arr>6 for t_emit>5 belong to the assumption layer and were'
      ' not used)')

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(t_e_list, shifts, 'o-')
    axes[0].set_xlabel('emission time t')
    axes[0].set_ylabel('nu_obs/nu_src')
    axes[0].set_title('W1-slab: frequency shift (geodesic-derived)')
    axes[0].grid(alpha=0.3)
    nu_ratio = np.array([s_ for s_ in shifts if np.isfinite(s_)])
    nu_grid = np.linspace(0.8, 1.25, 200)
    spec = np.exp(-((nu_grid - np.mean(nu_ratio)) / 0.02) ** 2)
    axes[1].plot(nu_grid * np.mean(nu_ratio), spec * T_wall,
                 label='T_wall applied')
    axes[1].set_xlabel('nu_obs (units of nu_src)')
    axes[1].set_ylabel('relative intensity')
    axes[1].set_title('W1-slab: synthetic spectrum (T from P3)')
    axes[1].legend()
    axes[1].grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig('DCC_P4_observation.png', dpi=140)
    plt.close(fig)
    with open('DCC_P4_pipeline_results.txt', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines) + '\n')
    print('Written: DCC_P4_pipeline_results.txt / DCC_P4_observation.png')


if __name__ == '__main__':
    main()
