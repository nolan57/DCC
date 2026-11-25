#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DCC P2 — Standalone output of the L2 quantity Cddot/C
=================================

Roadmap §4.4 L2 / G3 requires P2 to output Cddot/C in its first round. This script uses
the same equations and initial data as `DCC_P2_homogeneous.py`, run separately with the shorter t_end=400,
It outputs max|Cddot/C|, Cddot/C at the minimum of H_C, and the constraint residual for each case.

Definition:
    Cddot/C = dH_C/dt + H_C^2
(H_C = dot C / C)

Parameters and the wall profile follow `DCC_P1_metadata.md`; this script takes only the two asymptotic values of the P1 profile
(phi0=0 and phi0=-v) and does not use the x-dependent profile.

Run: python DCC_P2_L2.py
"""

import numpy as np
import DCC_P2_homogeneous as m

CASES = [
    ("magnetic-only [shear]", 0.25, -1.0, 0.7, 0.0, "shear"),
    ("true-vac [shear]",      0.25, -1.0, 0.7, 0.01, "shear"),
    ("baseline [shear]",      0.25,  0.0, 0.7, 0.01, "shear"),
    ("magnetic-only [iso]",   0.0,  -1.0, 0.7, 0.0, "isotropic"),
    ("baseline [iso]",        0.0,   0.0, 0.7, 0.01, "isotropic"),
    ("baseline [iso] f=3",    0.0,   0.0, 3.0, 0.01, "isotropic"),
]

T_END = 400.0


def main():
    lines = []
    def w(s=""):
        print(s)
        lines.append(s)

    w("=" * 78)
    w("DCC P2 — L2: Cddot/C (standalone short run, t_end=400)")
    w("=" * 78)
    w(f"rtol={m.RTOL}, atol={m.ATOL}, t_end={T_END}")
    w("Cddot/C = dH_C/dt + H_C^2")
    w("")
    w(f"{'case':24s} {'H_C min':>12s} {'t(H_C min)':>11s} "
      f"{'max|CddC|':>12s} {'CddC@min':>12s} {'D2':>5s} {'D3r':>5s} "
      f"{'C/A fin':>10s} {'C_H max':>10s}")
    w("-" * 100)

    for label, H0, phi0, f, eps, mode in CASES:
        sol, rho0 = m.run_case(H0, phi0, 0.0, f, eps, mode=mode, t_end=T_END)
        r = m.summarize(sol, f, eps, label)
        if r["status"] != "OK":
            w(f"{label:24s} FAIL: {r.get('msg','')}")
            continue
        i = int(np.argmin(r["HC"]))
        w(f"{label:24s} {r['HC_min']:12.4e} {r['t'][i]:11.4f} "
          f"{r['CddC_max']:12.4e} {r['CddC_at_HCmin']:12.4e} "
          f"{str(r['D2']):>5s} {str(r['D3_ratio']):>5s} "
          f"{r['CA_final']:10.3e} {r['CH_max']:10.2e}")
    w("-" * 100)
    w("")
    w("How to read:")
    w("* For D2 cases Cddot/C>0 at the H_C minimum: C is turning from contraction to expansion;")
    w("* max|Cddot/C| is finite, with no C->0-type acceleration divergence;")
    w("* Strict D3 requires C->0; D3r in this table only means C/A<1e-2, not D3-strict.")

    with open("DCC_P2_L2_results.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\nWrote DCC_P2_L2_results.txt")


if __name__ == "__main__":
    main()
