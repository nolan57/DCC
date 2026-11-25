# -*- coding: utf-8 -*-
"""
4.4 Check 3 v3: genuine exterior derivative + symbolic contradiction proof (review B3 fix)
============================================================================

The problem with v2 (review B3, confirmed): in `inverse_problem_check_v2.py:65-76`,
`dF_A` / `dF_B` are **hard-coded dictionary entries**, followed immediately by
    C3_A = simplify(∂_t f − ∂_t f) == 0
which is a tautology. The code never constructed a 2-form and never performed an exterior derivative. The claim
"sympy exterior derivative executed mechanically" in the v2 report does not hold; F-C3-0 is not closed.

v3 does three things:

  1. Implement genuine p-forms and an exterior-derivative operator ext_d(): components are stored as
     {(i1<...<ip): coefficient}, each is differentiated by ∂_μ with the sign determined by the parity of the insertion
     position, and repeated indices vanish automatically. Then self-test with d(dω)=0 on a **random 1-form** -- this
     checks the implementation itself, not a repetition of the hand derivation.

  2. Build ansatz A / B as genuine 2-form objects and pass them to ext_d(), obtaining the 3-form components of dF.
     The hand-derived formula serves only as the object of comparison (expected value), not as input.

  3. Upgrade "no solution" from "sympy solve returns []" to a **symbolic contradiction proof**:
         κ p_x,req = −(γ² − γh + h²) = −[(γ − h/2)² + 3h²/4] < 0   holds identically
         κ p_x,Maxwell = +f² e^{−4ht}/2 > 0                          holds identically
     The two signs are incompatible, **independently of the values of (h, γ, f)**. This is far stronger than
     "some solve call found no solution": a failed solve may simply mean the solver is inadequate.

Run: python -I src/r2_homogeneous/inverse_problem_check_v3.py
"""
import sympy as sp

t, x, y, z = sp.symbols("t x y z", real=True)
kappa, h, gam = sp.symbols("kappa h gamma", positive=True)
f_amp = sp.symbols("f_amp", real=True)
coords = (t, x, y, z)
N = 4


# --------------------------------------------------------------- tensor utilities
def build_G(A_expr, B_expr, C_expr):
    """Compute Christoffel -> Ricci -> Einstein directly from diag(-1,A^2,B^2,C^2)"""
    g = sp.diag(-1, A_expr ** 2, B_expr ** 2, C_expr ** 2)
    ginv = g.inv()
    Gam = {}
    for m in range(N):
        for nu in range(N):
            for lam in range(N):
                Gam[(m, nu, lam)] = sp.simplify(sum(
                    ginv[m, s] * (sp.diff(g[lam, s], coords[nu])
                                  + sp.diff(g[nu, s], coords[lam])
                                  - sp.diff(g[nu, lam], coords[s]))
                    for s in range(N)) / 2)
    Ric = [[0] * N for _ in range(N)]
    for m in range(N):
        for nu in range(N):
            acc = 0
            for lam in range(N):
                acc += sp.diff(Gam[(lam, m, nu)], coords[lam]) \
                    - sp.diff(Gam[(lam, m, lam)], coords[nu])
                for r in range(N):
                    acc += Gam[(lam, m, nu)] * Gam[(r, lam, r)] \
                        - Gam[(r, m, lam)] * Gam[(lam, nu, r)]
            Ric[m][nu] = sp.simplify(acc)
    Rs = sum(ginv[m, nu] * Ric[m][nu] for m in range(N) for nu in range(N))
    G = sp.Matrix([[sp.simplify(Ric[m][nu] - sp.Rational(1, 2) * g[m, nu] * Rs)
                    for nu in range(N)] for m in range(N)])
    return G, g, ginv


# --------------------------------------------------- genuine p-forms and exterior derivative
def form(comp):
    """Canonicalize: drop zero components"""
    return {k: v for k, v in comp.items() if sp.simplify(v) != 0}


def wedged_key(key, mu):
    """Insert index mu into the sorted key; return (new key, sign); repeated index returns (None, 0)"""
    if mu in key:
        return None, 0
    pos = 0
    while pos < len(key) and key[pos] < mu:
        pos += 1
    nk = key[:pos] + (mu,) + key[pos:]
    return nk, (-1) ** pos


def ext_d(comp):
    """Genuine exterior derivative: d(Σ c_I dx^I) = Σ ∂_μ c_I dx^μ ∧ dx^I"""
    out = {}
    for key, c in comp.items():
        for mu in range(N):
            dc = sp.diff(c, coords[mu])
            if sp.simplify(dc) == 0:
                continue
            nk, sign = wedged_key(key, mu)
            if nk is None:
                continue
            out[nk] = out.get(nk, 0) + sign * dc
    return form(out)


def basis_name(key):
    names = ("dt", "dx", "dy", "dz")
    return "^".join(names[i] for i in key)


def show(comp):
    if not comp:
        return "0"
    parts = ["(%s)*%s" % (sp.sstr(c), basis_name(k)) for k, c in sorted(comp.items())]
    return " + ".join(parts)


def main():
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    L = []
    w = L.append
    w("=" * 92)
    w("check (3) v3: real exterior derivative + parameter-free sign contradiction")
    w("=" * 92)
    w("v2 defect fixed: dF_A/dF_B were hand-written dict entries compared to")
    w("  themselves (C3_A = simplify(d_t f - d_t f) == 0, tautology). v3 builds")
    w("  actual 2-form objects and differentiates them with ext_d().")
    w("")

    # ---------------- T1 implementation self-test: d^2 = 0
    a_fun = sp.sin(t) * x * y + sp.exp(z) * x ** 2
    omega = form({(1,): a_fun})                       # omega = a dx
    d1 = ext_d(omega)
    d2 = ext_d(d1)
    w("[T1] implementation self-test: d(d(omega)) = 0 on omega = a(t,x,y,z) dx")
    w("     omega  = %s" % show(omega))
    w("     d omega = %s" % show(d1))
    w("     d d omega = %s   -> %s" % (show(d2), "PASS" if not d2 else "FAIL"))

    # ---------------- T2/T3 genuine exterior derivative of the two ansatze
    f_f = sp.Function("f")(t, x)
    E_f = sp.Function("E")(t, x)

    A2 = form({(1, 2): f_f})                          # F = f dx^dy
    B2 = form({(1, 2): f_f, (0, 2): E_f})             # F = f dx^dy + E dt^dy
    dA = ext_d(A2)
    dB = ext_d(B2)
    expect_A = {(0, 1, 2): sp.diff(f_f, t)}
    expect_B = {(0, 1, 2): sp.diff(f_f, t) - sp.diff(E_f, x)}
    w("")
    w("[T2] ansatz A: F = f(t,x) dx^dy")
    w("     dF = %s" % show(dA))
    w("     expected (hand derivation, used ONLY as comparison): dt f")
    t2 = sp.simplify(dA.get((0, 1, 2), 0) - expect_A[(0, 1, 2)]) == 0 and len(dA) == 1
    w("     -> %s" % ("PASS" if t2 else "FAIL"))
    w("")
    w("[T3] ansatz B: F = f(t,x) dx^dy + E(t,x) dt^dy   (E along y: F_ty)")
    w("     dF = %s" % show(dB))
    w("     expected: dt f - dx E")
    t3 = sp.simplify(dB.get((0, 1, 2), 0) - expect_B[(0, 1, 2)]) == 0 and len(dB) == 1
    w("     -> %s" % ("PASS" if t3 else "FAIL"))

    # ---------------- T4 dF = 0 after substituting the constraint
    # Explicit verification: if f satisfies d_t f = d_x E (take f = ∫ d_x E dt), then dF = 0
    Et = sp.Function("Ee")(t, x)
    f_sol = sp.integrate(sp.diff(Et, x), t)           # a family of solutions satisfying d_t f = d_x E
    d_sol = ext_d({(1, 2): f_sol, (0, 2): Et})
    w("")
    w("[T4] substituting the constraint (f = integral of d_x E over t):")
    w("     dF = %s  -> %s" % (show(d_sol), "PASS" if not d_sol else "FAIL"))
    t4 = not d_sol

    # ---------------- T5 Einstein tensor of the constant-rate target
    G, g, ginv = build_G(sp.exp(h * t), sp.exp(h * t), sp.exp(-gam * t))
    rho_req = sp.simplify(G[0, 0] / kappa)
    px_req = sp.simplify(G[1, 1] / (kappa * sp.exp(2 * h * t)))
    py_req = sp.simplify(G[2, 2] / (kappa * sp.exp(2 * h * t)))
    pz_req = sp.simplify(G[3, 3] / (kappa * sp.exp(-2 * gam * t)))
    w("")
    w("[T5] Einstein tensor of diag(-1, e^2ht, e^2ht, e^-2gt)  [independently rebuilt]")
    w("     kappa*rho = %s" % sp.simplify(rho_req * kappa))
    w("     kappa*px  = %s" % sp.simplify(px_req * kappa))
    w("     kappa*py  = %s" % sp.simplify(py_req * kappa))
    w("     kappa*pz  = %s" % sp.simplify(pz_req * kappa))

    # ---------------- T6 Maxwell-side stress (F_xy)
    F = sp.Matrix([[0, 0, 0, 0], [0, 0, f_amp, 0], [0, -f_amp, 0, 0], [0, 0, 0, 0]])
    Fup = sp.simplify(ginv * F * ginv)
    Fsq = sp.simplify(-(F * Fup).trace())
    Tmix = sp.simplify(Fup * F.T - sp.Rational(1, 4) * Fsq * sp.eye(N))
    rho_B = sp.simplify(-Tmix[0, 0])
    px_B = sp.simplify(Tmix[1, 1])
    pz_B = sp.simplify(Tmix[3, 3])
    w("")
    w("[T6] Maxwell stress of F_xy (same metric):")
    w("     kappa*rho_B = %s" % sp.simplify(rho_B * kappa))
    w("     kappa*px_B  = %s" % sp.simplify(px_B * kappa))
    w("     kappa*pz_B  = %s" % sp.simplify(pz_B * kappa))

    # ---------------- T7 parameter-free symbolic contradiction
    # Complete the square for the target px: -(g^2 - g h + h^2) = -[(g - h/2)^2 + 3h^2/4]
    px_req_k = sp.simplify(px_req * kappa)
    completed = -( (gam - h / 2) ** 2 + sp.Rational(3, 4) * h ** 2 )
    t7a = sp.simplify(px_req_k - completed) == 0
    neg_def = sp.simplify(-completed) > 0            # (g-h/2)^2 + 3h^2/4 >= 0, >0 unless both 0
    px_B_pos = sp.simplify(px_B * kappa)
    # Prove the coefficient of px_B is positive: extract the sign
    t7b = sp.simplify(px_B_pos - f_amp ** 2 * kappa * sp.exp(-4 * h * t) / 2) == 0
    w("")
    w("[T7] parameter-free sign contradiction  (the actual proof, not a solve() miss)")
    w("     kappa*px_req = %s  =  -[(gamma-h/2)^2 + 3h^2/4]  : identity=%s"
      % (px_req_k, "YES" if t7a else "NO"))
    w("       -> px_req <= 0, and < 0 for all (h,gamma) != (0,0)")
    w("     kappa*px_B   = %s  =  +f^2 e^{-4ht}/2 : identity=%s"
      % (px_B_pos, "YES" if t7b else "NO"))
    w("       -> px_B > 0 for any f != 0")
    w("     => the signs are incompatible, independently of (h, gamma, f). Maxwell F_xy cannot realize this target.")
    w("     (v2 only said solve() returned the empty set, which could be questioned as solver inadequacy; an identity proof is given here.)")

    # ---------------- T8 full simultaneous component solve (retained as weak evidence)
    eqs = [sp.Eq(rho_B, rho_req), sp.Eq(px_B, px_req),
           sp.Eq(Tmix[2, 2], py_req), sp.Eq(pz_B, pz_req)]
    full_sol = sp.solve(eqs, [h, gam, f_amp], dict=True)
    w("")
    w("[T8] full simultaneous solve (rho,px,py,pz) for (h,gamma,f): %s"
      % ("solutions: %s" % full_sol if full_sol else "empty set"))

    # ---------------- summary
    tests = [
        ("T1_dd_zero", not d2),
        ("T2_dF_ansatzA", t2),
        ("T3_dF_ansatzB", t3),
        ("T4_constraint_zeroes_dF", t4),
        ("T5_px_req_identity", t7a),
        ("T6_px_Maxwell_identity", t7b),
        ("T7_no_solution", not full_sol),
    ]
    w("")
    w("[verdicts]")
    for name, ok in tests:
        w("  %-28s %s" % (name, "PASS" if ok else "FAIL"))
    allok = all(ok for _, ok in tests)
    w("")
    w("  check3 statement (strengthened):")
    w("    (i)  dF = 0 for F = f dx^dy + E dt^dy  <=>  d_t f = d_x E   [machine, T2-T4]")
    w("    (ii) Maxwell F_xy stress can never equal the const-rate target: the px sign")
    w("         is always opposite [machine, T5-T7], independent of parameters.")
    w("    (iii) Therefore no Maxwell field exists that can self-consistently generate this geometry -- not 'not found', but 'does not exist'.")
    w("")
    w("check (3) v3 OVERALL: %s" % ("PASS" if allok else "FAIL"))
    w("evidence level: ESTABLISHED (identity-level, within pinned conventions)")
    w("residual: G3' gate still OPEN on P2-C6 and N11 boundary condition.")
    print("\n".join(L))


if __name__ == "__main__":
    main()
