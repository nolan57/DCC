#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DCC P2 — Local planar bubble wall (separate-universe / gradient approximation) spatial D2 plot
================================================================

Positioning
----
This script uses a **local planar approximation**, not a full 1+1 ADM solution:
* At each x, solve the homogeneous Bianchi I equations with the local rho(x), p_i(x);
* Keep the scalar field's phi'' spatial coupling (the wall's gradient energy);
* Neglect the dynamical terms of metric gradients (A',B',C' are used only to diagnose constraint residuals);
* Fix H_C by projecting onto the local Hamiltonian constraint, so that H_A H_B+H_B H_C+H_C H_A=kappa rho;
* Do not enforce the momentum constraint; output its residual pointwise as a reliability indicator of the gradient approximation.

This allows us to give the following without resolving the planar Lichnerowicz asymptotic behavior:
1. Which regions of the wall reach D2 (H_C<0);
2. The respective contributions of magnetic pressure and wall gradient energy to D2;
3. The gradient-approximation error (R/2 and the momentum residual).

Metric (N=1, beta=0, locally homogeneous)
    ds^2 = -dt^2 + A(t,x)^2 dx^2 + B(t,x)^2 dy^2 + C(t,x)^2 dz^2

Matter
    phi(t,x), V(phi)=lam/4(phi^2-v^2)^2+eps(phi+v)/(2v)+eps^2/(16 lam v^4)
    f(x)=f0 sech^2(a x), Z(phi)=exp(alpha phi/v), E=0

Output
    DCC_P2_local_planar_results.txt
    DCC_P2_local_planar.png

Run: python DCC_P2_local_planar.py
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Parameters
# ----------------------------------------------------------------------
V_VAC = 1.0
LAM = 1.0
A_WALL = V_VAC * np.sqrt(LAM / 2.0)
ALPHA = 0.5
EPS = 0.01
KAPPA = 1.0
F0 = 0.7

L = 40.0
N = 401
DX = 2.0 * L / (N - 1)
DT = 0.2 * DX
T_END = 40.0
N_OUT = 200

X = np.linspace(-L, L, N)
V_OFF = EPS**2 / (16.0 * LAM * V_VAC**4)


def V(phi):
    return (0.25 * LAM * (phi**2 - V_VAC**2) ** 2
            + EPS * (phi + V_VAC) / (2.0 * V_VAC) + V_OFF)


def Vp(phi):
    return LAM * phi * (phi**2 - V_VAC**2) + EPS / (2.0 * V_VAC)


def Z(phi):
    return np.exp(ALPHA * phi / V_VAC)


def Zp(phi):
    return (ALPHA / V_VAC) * Z(phi)


def f_profile(x):
    return F0 / np.cosh(A_WALL * x) ** 2


F = f_profile(X)


def unpack(y):
    phi, Pi, lnA, lnB, lnC, HA, HB, HC = y
    return phi, Pi, np.exp(lnA), np.exp(lnB), np.exp(lnC), HA, HB, HC


def matter_fields(phi, Pi, A, B, f):
    """Return rho, p_x, p_y, p_z, rho_B, g, p0."""
    phix = np.gradient(phi, DX, edge_order=2)
    g = 0.5 * phix**2 / A**2
    p0 = 0.5 * Pi**2 - V(phi)
    rho_B = Z(phi) * f**2 / (2.0 * A**2 * B**2)
    rho = p0 + g + V(phi) + rho_B
    px = p0 + g + rho_B
    py = p0 - g + rho_B
    pz = p0 - g - rho_B
    return rho, px, py, pz, rho_B, g, p0, phix


def rhs(y):
    phi, Pi, lnA, lnB, lnC, HA, HB, HC = unpack(y)
    A, B, C = np.exp(lnA), np.exp(lnB), np.exp(lnC)

    rho, px, py, pz, rho_B, g, p0, phix = matter_fields(phi, Pi, A, B, F)
    phixx = np.gradient(phix, DX, edge_order=2)

    HA_d = (-HA**2 - 0.5 * HA * (HB + HC) + 0.5 * HB * HC
            - 0.5 * KAPPA * (py + pz - px))
    HB_d = (-HB**2 - 0.5 * HB * (HA + HC) + 0.5 * HA * HC
            - 0.5 * KAPPA * (px + pz - py))
    HC_d = (-HC**2 - 0.5 * HC * (HA + HB) + 0.5 * HA * HB
            - 0.5 * KAPPA * (px + py - pz))

    # Local approximation: keep only phi'' and neglect metric-gradient terms
    Pi_d = (-(HA + HB + HC) * Pi + phixx / A**2
            - Vp(phi) - (ALPHA / V_VAC) * rho_B)

    return np.array([Pi, Pi_d, HA, HB, HC, HA_d, HB_d, HC_d])


def project_constraint(y):
    """Reset H_C using the local Hamiltonian constraint: H_A H_B + (H_A+H_B) H_C = kappa rho."""
    phi, Pi, lnA, lnB, lnC, HA, HB, HC = unpack(y)
    A, B, C = np.exp(lnA), np.exp(lnB), np.exp(lnC)
    rho, _, _, _, _, _, _, _ = matter_fields(phi, Pi, A, B, F)
    denom = HA + HB
    ok = np.abs(denom) > 1e-10
    HC_new = np.where(ok, (KAPPA * rho - HA * HB) / np.where(ok, denom, 1.0), HC)
    y2 = y.copy()
    y2[7] = HC_new
    return y2


def initial_state():
    phi = V_VAC * np.tanh(A_WALL * X)
    Pi = np.zeros_like(X)
    lnA = np.zeros_like(X)
    lnB = np.zeros_like(X)
    lnC = np.zeros_like(X)
    A = np.ones_like(X)
    B = np.ones_like(X)
    rho, _, _, _, _, _, _, _ = matter_fields(phi, Pi, A, B, F)
    H0 = np.maximum(np.sqrt(np.maximum(KAPPA * rho / 3.0, 0.0)), 1e-6)
    HA = H0.copy(); HB = H0.copy(); HC = H0.copy()
    y = np.array([phi, Pi, lnA, lnB, lnC, HA, HB, HC])
    return project_constraint(y)


def apply_bc(y):
    """Fixed boundary: the wall/field already approaches vacuum at the boundary, so freeze the boundary values."""
    y2 = y.copy()
    for i in (0, -1):
        y2[0, i] = V_VAC * np.tanh(A_WALL * X[i])
        y2[1, i] = 0.0
        y2[2, i] = 0.0
        y2[3, i] = 0.0
        y2[4, i] = 0.0
        # The boundary expansion rate is determined by the local vacuum energy (given by the projection)
    return project_constraint(y2)


def rk4_step(y, dt):
    k1 = rhs(y)
    k2 = rhs(apply_bc(y + 0.5 * dt * k1))
    k3 = rhs(apply_bc(y + 0.5 * dt * k2))
    k4 = rhs(apply_bc(y + dt * k3))
    y_new = y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    y_new[:, 0] = y[:, 0]
    y_new[:, -1] = y[:, -1]
    return apply_bc(y_new)


def diagnostics(y):
    phi, Pi, lnA, lnB, lnC, HA, HB, HC = unpack(y)
    A, B, C = np.exp(lnA), np.exp(lnB), np.exp(lnC)
    rho, px, py, pz, rho_B, g, p0, phix = matter_fields(phi, Pi, A, B, F)
    H_con = HA * HB + HB * HC + HC * HA - KAPPA * rho

    # 3D Ricci scalar (SymPy result)
    Ax = np.gradient(A, DX, edge_order=2)
    Bx = np.gradient(B, DX, edge_order=2)
    Cx = np.gradient(C, DX, edge_order=2)
    Axx = np.gradient(Ax, DX, edge_order=2)
    Bxx = np.gradient(Bx, DX, edge_order=2)
    Cxx = np.gradient(Cx, DX, edge_order=2)
    R3 = -2.0 * (A * B * Cxx + A * C * Bxx + A * Bx * Cx
                 - B * Ax * Cx - C * Ax * Bx) / (A**3 * B * C)

    # Direct G_tx (in terms of H): G_tx = -[d_x(H_C C)/C + d_x(H_B B)/B
    #                                     - H_A (C_x/C + B_x/B)]
    dHC = np.gradient(HC * C, DX, edge_order=2)
    dHB = np.gradient(HB * B, DX, edge_order=2)
    Gtx = -(dHC / C + dHB / B - HA * (Cx / C + Bx / B))
    Ttx = Pi * phix
    M_res = Gtx - KAPPA * Ttx

    nec = np.minimum.reduce([rho + px, rho + py, rho + pz])
    wec = np.minimum(rho, nec)

    return dict(phi=phi, Pi=Pi, A=A, B=B, C=C, HA=HA, HB=HB, HC=HC,
                rho=rho, px=px, py=py, pz=pz, rho_B=rho_B, g=g,
                H_con=H_con, R3=R3, Gtx=Gtx, Ttx=Ttx, M_res=M_res,
                nec=nec, wec=wec,
                H_res_full=H_con + 0.5 * R3,
                D2=(HC < 0),
                D3_ratio=(C / A < 1e-2),
                CA=C / A, CB=C / B, RH=HC / np.where(np.abs(HA) > 1e-14, HA, np.nan))


def main():
    lines = []
    def w(s=""):
        print(s)
        lines.append(s)

    w("=" * 84)
    w("DCC P2 — Local planar bubble wall (separate-universe / gradient approximation)")
    w("=" * 84)
    w(f"Parameters: v={V_VAC}, lam={LAM}, a={A_WALL:.6f}, alpha={ALPHA}, eps={EPS}, kappa={KAPPA}, f0={F0}")
    w(f"Grid: N={N}, L={L}, dx={DX:.5f}, dt={DT:.5e}, t_end={T_END}")
    w("Positioning: keep the phi'' spatial coupling and local constraint projection; metric gradients are used only for diagnostics, not a full 1+1 ADM solution.")
    w("")

    y = initial_state()
    times = np.linspace(0.0, T_END, N_OUT)
    snapshots = []
    dt = DT
    t = 0.0
    next_out = 0

    # t=0 output
    for k in range(N_OUT):
        if k == 0:
            snapshots.append((0.0, y.copy()))
    for k in range(1, N_OUT):
        t_target = times[k]
        while t < t_target - 1e-12:
            y = rk4_step(y, min(dt, t_target - t))
            t += min(dt, t_target - t)
        snapshots.append((t, y.copy()))

    # Diagnostics
    d0 = diagnostics(snapshots[0][1])
    scale0 = 2.0 * KAPPA * np.max(np.abs(d0["rho"])) + 1e-30
    w("Initial diagnostics (globally normalized):")
    w(f"  max|H_con| = {np.max(np.abs(d0['H_con'])):.3e}")
    w(f"  max|R3|/scale = {np.max(np.abs(d0['R3']))/scale0:.3e}")
    w(f"  max|M_res|/scale = {np.max(np.abs(d0['M_res']))/scale0:.3e}")
    w("")

    w(f"{'t':>7} {'max|H_con|':>12} {'max|R3|/scale':>14} {'max|M|/scale':>13} "
      f"{'min H_C':>11} {'D2 frac':>9} {'C/A min':>10} {'rhoB max':>10}")
    last_ratio = None
    for (tt, yy) in snapshots:
        d = diagnostics(yy)
        scale = 2.0 * KAPPA * np.max(np.abs(d['rho'])) + 1e-30
        last_ratio = np.max(np.abs(d['M_res'])) / scale
        w(f"{tt:7.2f} {np.max(np.abs(d['H_con'])):12.3e} "
          f"{np.max(np.abs(d['R3']))/scale:14.3e} "
          f"{last_ratio:13.3e} "
          f"{np.min(d['HC']):11.3e} {np.mean(d['D2']):9.3f} "
          f"{np.min(d['CA']):10.3e} {np.max(d['rho_B']):10.3e}")
    w("")
    if last_ratio is not None:
        if last_ratio < 1.0:
            w("VALIDITY: gradient approximation marginally valid (|M_res|/scale < 1).")
        else:
            w("VALIDITY: INVALID — gradient approximation fails "
              f"(|M_res|/scale = {last_ratio:.2e} >> 1). Do not use for D2 claims.")
    w("")

    # Select profiles at several times
    idxs = [0, N_OUT // 4, N_OUT // 2, 3 * N_OUT // 4, N_OUT - 1]
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    ax = axes.ravel()

    for idx in idxs:
        tt, yy = snapshots[idx]
        d = diagnostics(yy)
        ax[0].plot(X, d['HC'], label=f"t={tt:.1f}")
        ax[1].plot(X, d['CA'], label=f"t={tt:.1f}")
        ax[2].plot(X, d['phi'], label=f"t={tt:.1f}")
        ax[3].plot(X, d['rho_B'], label=f"t={tt:.1f}")
        ax[4].plot(X, d['D2'].astype(float), label=f"t={tt:.1f}")

    ax[0].axhline(0, color="k", lw=0.5)
    ax[0].set_xlabel("x"); ax[0].set_ylabel(r"$H_C$")
    ax[0].set_title("local expansion rate in z"); ax[0].legend(fontsize=7); ax[0].grid(alpha=0.3)

    ax[1].set_xlabel("x"); ax[1].set_ylabel("C/A")
    ax[1].set_title("relative scale"); ax[1].legend(fontsize=7); ax[1].grid(alpha=0.3)

    ax[2].set_xlabel("x"); ax[2].set_ylabel(r"$\phi$")
    ax[2].set_title("wall profile"); ax[2].legend(fontsize=7); ax[2].grid(alpha=0.3)

    ax[3].set_xlabel("x"); ax[3].set_ylabel(r"$\rho_B$")
    ax[3].set_title("magnetic energy"); ax[3].legend(fontsize=7); ax[3].grid(alpha=0.3)

    ax[4].set_xlabel("x"); ax[4].set_ylabel("D2 mask")
    ax[4].set_title("H_C<0 region"); ax[4].legend(fontsize=7); ax[4].grid(alpha=0.3)

    dlast = diagnostics(snapshots[-1][1])
    ax[5].plot(X, dlast['M_res'] / (KAPPA * np.abs(dlast['rho']) + 1e-30))
    ax[5].set_xlabel("x"); ax[5].set_ylabel("M_res/(kappa rho)")
    ax[5].set_title("momentum residual (gradient error)"); ax[5].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig("DCC_P2_local_planar.png", dpi=140)
    plt.close(fig)

    w("Wrote DCC_P2_local_planar_results.txt")
    w("Wrote DCC_P2_local_planar.png")

    with open("DCC_P2_local_planar_results.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
