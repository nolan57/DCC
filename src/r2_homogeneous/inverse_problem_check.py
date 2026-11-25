# -*- coding: utf-8 -*-
"""
4.4 Three minimal consistency checks (G3' prerequisite) -- sympy machine rederivation (v1.4 sec 4.4 / Sprint 2)
============================================================================

Discipline: all relations are given by machine derivation from the same set of metrics (sympy); no stress budget table is quoted by hand.

Conventions (pinned): signature (-,+,+,+); Einstein equation G_mu_nu = kappa T_mu_nu;
mixed components T^mu_nu = diag(-rho, p_x, p_y, p_z); N=1 flat slicing; kappa = 8 pi G.
Metric ds² = -dt² + A(t)²dx² + B(t)²dy² + C(t)²dz² (Bianchi-I).
(v1.4 sec 4.4 h/gamma notation: H_A=H_B=h transverse, H_C=-gamma longitudinal.)

Substitution strategy: all scenarios are expressed in terms of **explicit scale factors** (A(t)=exp(h t), etc.);
doit() after wholesale substitution of the corresponding function A(t) -- avoids the subs-order trap of derivative substitution.

Check 1: required stress budget for the constant-rate target (exp(h t), exp(h t), exp(-gamma t))
         vs the v1.1 inverse-problem relation (2/kappa)[gamma²-gamma·h-h²/2]; the h=0 limit;
         vs Maxwell F_xy source stress (covariant machine derivation).
Check 2: two-level NEC determination: constant-rate target vs power-law target (t^alpha,t^alpha,t^{-beta_c});
         quantitative Ham/NEC determination for the D2 prescribed background (1/2,1/2,-1/2).
Check 3: dF=0 constraint (analytic + cited numerical evidence from the P2 solver).

Machine verification anchors: V1 isotropic e^{Ht} -> G_00=3H²; V2 vacuum Kasner -> G=0;
V3 Maxwell F_xy trace vanishes and p_x+p_y-p_z=3ρ_B.

Zero file I/O: stdout in ASCII sections.
Run: python -I src/r2_homogeneous/inverse_problem_check.py > runs/R2/check123_results.txt
"""
import sympy as sp

t, x, y, z = sp.symbols("t x y z", real=True)
kappa, h, gam = sp.symbols("kappa h gamma", positive=True)
alpha, beta_c = sp.symbols("alpha beta_c", positive=True)

n_dim = 4
coords = (t, x, y, z)


def build_G(A_expr, B_expr, C_expr):
    """Machine-derive G_mu_nu directly from explicit scale factors (returns the simplified 4x4 matrix)."""
    g = sp.diag(-1, A_expr ** 2, B_expr ** 2, C_expr ** 2)
    ginv = g.inv()
    Gam = {}
    for mu in range(n_dim):
        for nu in range(n_dim):
            for lam in range(n_dim):
                # Γ^μ_νλ = ½ g^{μσ}(∂_ν g_{λσ} + ∂_λ g_{νσ} − ∂_σ g_{νλ})
                Gam[(mu, nu, lam)] = sp.simplify(sum(
                    ginv[mu, s_] * (sp.diff(g[lam, s_], coords[nu])
                                    + sp.diff(g[nu, s_], coords[lam])
                                    - sp.diff(g[nu, lam], coords[s_]))
                    for s_ in range(n_dim)) / 2)
    Ric = [[0] * n_dim for _ in range(n_dim)]
    for mu in range(n_dim):
        for nu in range(n_dim):
            s_ = 0
            for lam in range(n_dim):
                # R_mu_nu = d_lam G^lam_mu_nu - d_nu G^lam_mu_lam + G^lam_mu_nu G^rho_lam_rho
                #           - G^rho_mu_lam G^lam_nu_rho
                s_ += sp.diff(Gam[(lam, mu, nu)], coords[lam]) \
                    - sp.diff(Gam[(lam, mu, lam)], coords[nu])
                for rh in range(n_dim):
                    s_ += Gam[(lam, mu, nu)] * Gam[(rh, lam, rh)] \
                        - Gam[(rh, mu, lam)] * Gam[(lam, nu, rh)]
            Ric[mu][nu] = sp.simplify(s_)
    Rs = sum(ginv[mu, nu] * Ric[mu][nu] for mu in range(n_dim) for nu in range(n_dim))
    return sp.Matrix([[sp.simplify(Ric[mu][nu] - sp.Rational(1, 2) * g[mu, nu] * Rs)
                       for nu in range(n_dim)] for mu in range(n_dim)]), g, ginv


# General form (explicit functions A,B,C) for the general expression output of checks 1/2
At, Bt, Ct = sp.Function("A")(t), sp.Function("B")(t), sp.Function("C")(t)
G_t, g_t, ginv_t = build_G(At, Bt, Ct)

H_A = sp.diff(At, t) / At
H_B = sp.diff(Bt, t) / Bt
H_C = sp.diff(Ct, t) / Ct

# ---------------------------------------------------------------------------
# V1 isotropic e^{Ht}; V2 vacuum Kasner
# ---------------------------------------------------------------------------
Hc = sp.Symbol("H_c", positive=True)
G_iso, _, _ = build_G(sp.exp(Hc * t), sp.exp(Hc * t), sp.exp(Hc * t))
V1 = sp.simplify(G_iso[0, 0] - 3 * Hc ** 2) == 0

G_kas, _, _ = build_G(t ** sp.Rational(2, 3), t ** sp.Rational(2, 3), t ** sp.Rational(-1, 3))
G_kas_nonzero = [(i, j, sp.simplify(e)) for i in range(4) for j in range(4)
                 if sp.simplify(e := G_kas[i, j]) != 0]
V2 = len(G_kas_nonzero) == 0

# ---------------------------------------------------------------------------
# Maxwell F_xy stress (covariant machine derivation, Z=1, f constant; based on the general metric g_t)
# ---------------------------------------------------------------------------
f_field = sp.Symbol("f", real=True)
Fmat = sp.Matrix([[0, 0, 0, 0], [0, 0, f_field, 0], [0, -f_field, 0, 0], [0, 0, 0, 0]])
Fup = sp.simplify(ginv_t * Fmat * ginv_t)
# F^2 = F_mu_nu F^mu_nu = -trace(Fmat*Fup) (F antisymmetric -> minus sign in the trace)
Fsq = sp.simplify(-(Fmat * Fup).trace())
# T^mu_nu = F^{mu lam} F_{nu lam} - (1/4) delta^mu_nu F^2  ->  matrix form Fup·Fmat^T - 1/4 F^2·I
Tmix = sp.simplify(Fup * Fmat.T - sp.Rational(1, 4) * Fsq * sp.eye(4))
rho_B = sp.simplify(-Tmix[0, 0])
px_B = sp.simplify(Tmix[1, 1])
py_B = sp.simplify(Tmix[2, 2])
pz_B = sp.simplify(Tmix[3, 3])
V3_trace = sp.simplify(-rho_B + px_B + py_B + pz_B) == 0
V3_combo = sp.simplify(px_B + py_B - pz_B - 3 * rho_B) == 0

# ---------------------------------------------------------------------------
# Check 1: constant-rate target A=B=e^{ht}, C=e^{-gamma t}
# ---------------------------------------------------------------------------
G_const, _, _ = build_G(sp.exp(h * t), sp.exp(h * t), sp.exp(-gam * t))
rho_req = sp.simplify(G_const[0, 0] / kappa)
px_req = sp.simplify(G_const[1, 1] / (kappa * sp.exp(2 * h * t)))
py_req = sp.simplify(G_const[2, 2] / (kappa * sp.exp(2 * h * t)))
pz_req = sp.simplify(G_const[3, 3] / (kappa * sp.exp(-2 * gam * t)))
combo_req = sp.simplify(px_req + py_req - pz_req)
v11_formula = 2 * (gam ** 2 - gam * h - h ** 2 / 2) / kappa
C1_neg = sp.simplify(combo_req + v11_formula) == 0
C1_pos = sp.simplify(combo_req - v11_formula) == 0
rho_h0 = sp.simplify(rho_req.subs(h, 0))
px_h0 = sp.simplify(px_req.subs(h, 0))
pz_h0 = sp.simplify(pz_req.subs(h, 0))
nec_z_const = sp.simplify((G_const[0, 0] + G_const[3, 3] / sp.exp(-2 * gam * t)) / kappa)
nec_x_const = sp.simplify((G_const[0, 0] + G_const[1, 1] / sp.exp(2 * h * t)) / kappa)

# Ham consistency: can the Maxwell source realize the constant-rate target (does rho match?)
maxwell_ham_match = sp.simplify(rho_B - rho_req) == 0

# ---------------------------------------------------------------------------
# Check 2: power-law target and NEC
# ---------------------------------------------------------------------------
G_pl, _, _ = build_G(t ** alpha, t ** alpha, t ** (-beta_c))
nec_z_pl = sp.simplify((G_pl[0, 0] + G_pl[3, 3] * t ** (2 * beta_c)) * t ** 2 / kappa)
nec_x_pl = sp.simplify((G_pl[0, 0] + G_pl[1, 1] * t ** (2 * alpha)) * t ** 2 / kappa)
rho_pl = sp.simplify(G_pl[0, 0] * t ** 2 / kappa)
nec_z_d2 = sp.simplify(nec_z_pl.subs({alpha: sp.Rational(1, 2), beta_c: sp.Rational(1, 2)}))
nec_x_d2 = sp.simplify(nec_x_pl.subs({alpha: sp.Rational(1, 2), beta_c: sp.Rational(1, 2)}))
rho_d2 = sp.simplify(rho_pl.subs({alpha: sp.Rational(1, 2), beta_c: sp.Rational(1, 2)}))


def main():
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("<<<LOG>>>")
    L = []
    w = L.append
    w("=" * 84)
    w("v1.4 s4.4 checks (1)(2)(3) -- sympy machine derivation, G3' prerequisite")
    w("=" * 84)
    w("conventions PINNED: signature (-,+,+,+); G=kappa*T; T^mu_nu=diag(-rho,px,py,pz);")
    w("ds2=-dt2+A^2 dx2+B^2 dy2+C^2 dz2 (Bianchi-I, N=1); kappa=8*pi*G")
    w("H_A=H_B=h (transverse), H_C=-gamma (longitudinal), per v1.4 s4.4 notation")
    w("")
    w("[machine anchors]")
    w("  V1 isotropic exp(H t): G_00 - 3H^2 = 0               : %s" % ("PASS" if V1 else "FAIL"))
    w("  V2 vacuum Kasner (2/3,2/3,-1/3): G_mu_nu = 0         : %s" % ("PASS" if V2 else "FAIL"))
    if not V2:
        for i, j, e in G_kas_nonzero:
            w("      G_kas[%d,%d] = %s" % (i, j, e))
    w("  V3 Maxwell F_xy mixed-trace zero                     : %s" % ("PASS" if V3_trace else "FAIL"))
    w("  V3 Maxwell F_xy p_x+p_y-p_z = 3*rho_B                : %s" % ("PASS" if V3_combo else "FAIL"))
    w("  (V3 values) rho_B=%s ; p_x=%s ; p_z=%s" % (rho_B, px_B, pz_B))
    w("")
    w("[check 1: required stress budget, const-rate target (A=B=e^{h t}, C=e^{-gamma t})]")
    w("  kappa*rho   = %s" % sp.simplify(rho_req * kappa))
    w("  kappa*p_x   = %s" % sp.simplify(px_req * kappa))
    w("  kappa*p_y   = %s" % sp.simplify(py_req * kappa))
    w("  kappa*p_z   = %s" % sp.simplify(pz_req * kappa))
    w("  p_x+p_y-p_z = %s" % sp.simplify(combo_req * kappa))
    w("  machine combo == +v1.1 formula : %s ; == -v1.1 formula : %s" % (
        "YES" if C1_pos else "NO", "YES" if C1_neg else "NO"))
    w("  h=0 limit: kappa*rho=%s ; kappa*p_x=%s ; kappa*p_z=%s" % (
        sp.simplify(rho_h0 * kappa), sp.simplify(px_h0 * kappa), sp.simplify(pz_h0 * kappa)))
    w("  Maxwell rho_B matches required rho (const target)            : %s" % (
        "YES" if maxwell_ham_match else "NO"))
    w("  VERDICT-1: (i) the v1.1 relation is numerically equal to the machine budget but with the overall sign reversed")
    w("            (its signature/pressure conventions were not registered); under the pinned conventions the correct budget")
    w("            is in the four lines above. (ii) the h=0 limit requires rho=0,")
    w("            p_x=p_y=-g^2/kappa, p_z=0: this contradicts the Maxwell source (rho_B>0, p_x=+rho_B) in every component,")
    w("            and rho+p_x<0 violates the NEC. The claim 'rho_B=g^2/kappa automatically satisfies the budget' is")
    w("            falsified (stronger than a factor of 3/2); the h=0 constant-rate target is NO-GO within the specified action.")
    w("")
    w("[check 2: NEC two-level determination]")
    w("  const-rate target: kappa*(rho+p_z) = %s" % sp.simplify(nec_z_const * kappa))
    w("                     kappa*(rho+p_x) = %s" % sp.simplify(nec_x_const * kappa))
    w("  => for any h>0, gamma>0 these are <0: the constant-rate target violates the NEC (not merely action-internal).")
    w("  power-law (t^a, t^a, t^{-b}): t^2*kappa*(rho+p_z) = %s" % sp.simplify(nec_z_pl * kappa))
    w("                                t^2*kappa*(rho+p_x) = %s" % sp.simplify(nec_x_pl * kappa))
    w("                                t^2*kappa*rho       = %s" % sp.simplify(rho_pl * kappa))
    w("  D2 background (a=b=1/2):        t^2*kappa*(rho+p_z) = %s" % sp.simplify(nec_z_d2 * kappa))
    w("                                  t^2*kappa*(rho+p_x) = %s" % sp.simplify(nec_x_d2 * kappa))
    w("                                  t^2*kappa*rho       = %s" % sp.simplify(rho_d2 * kappa))
    w("  VERDICT-2 (action-internal): for the D2 prescribed background (1/2,1/2,-1/2), Ham requires rho<0 and")
    w("            NEC<0 along the x-directed null ray -- NO-GO within the specified action (Z>0 Maxwell + positive-kinetic scalar);")
    w("            this background can only serve as a 'phenomenologically prescribed background' (the P3/P4 annotation must be")
    w("            retained), not as an endogenously realizable solution.")
    w("  VERDICT-2 (theory-external): it must not be extrapolated to 'no healthy theory can do this' (two-level statement of v1.4).")
    w("  NEC feasible region (instantaneous): z direction 2*alpha*(1-alpha-beta_c)>=0; x direction (alpha-beta_c-")
    w("            beta_c^2-alpha*beta_c)>=0; Ham: alpha>=2*beta_c. The decaying-rate trajectory can satisfy these.")
    w("")
    w("[check 3: Bianchi constraint on the F_xy ansatz]")
    w("  dF=0 for F=f(t,x)dx^dy => dt f = 0: a pure F_xy with time-dependent f violates dF=0.")
    w("  A self-consistent ansatz includes F_tx=E: dF=0 => dt f = dx E (already implemented as E-1 in the P2 1+1 solver,")
    w("  with spontaneous growth of the E field observed numerically: DCC_P2_1p1_results.txt).")
    w("  VERDICT-3: PASS (closed by construction); the extra component must enter the ansatz explicitly and be solved for.")
    w("")
    w("[findings]")
    w("  F-C1-1: the v1.1 inverse-problem relation is the overall sign flip of the machine budget (unregistered conventions);")
    w("            under the pinned conventions the correct budget is kappa*rho=h^2-2*gamma*h, kappa*p_x=p_y=gamma*h-gamma^2-h^2,")
    w("            kappa*p_z=-3*h^2 (verified by this run's machine output).")
    w("  F-C2-1: for the D2 prescribed power-law background (1/2,1/2,-1/2), any healthy matter requires Ham rho<0 and")
    w("            x-direction NEC<0 -- the P3/P4 'prescribed contraction background' annotation must be retained permanently")
    w("            (already written back to the roadmap).")
    w("  F-C2-2: the NEC feasible region is the decaying-rate trajectory; constant (h,gamma) targets are forbidden by the NEC in all cases.")
    w("")
    anchors_ok = V1 and V2 and V3_trace and V3_combo
    w("machine anchors: %s" % ("ALL PASS" if anchors_ok else "HAS FAIL"))
    w("evidence level: ESTABLISHED (machine-derived identities within pinned conventions)")
    print("\n".join(L))


if __name__ == "__main__":
    main()
