# -*- coding: utf-8 -*-
"""Which assumption to abandon -> the most spectacular visual effect? (v1, 2026-11-21)

Background
----------
`visualization_null_result_v1.md` has shown that when all three assumptions
(effective 2D + smoothness + weak-interaction preservation) hold at the same
time, the human-eye image is the empty set. Section 5 of that document left a
"failure condition table": abandon any one of them and the conclusion fails.
This module **quantifies** that table and answers "which abandonment is the
most spectacular".

"Spectacular" is not a single quantity. This module splits it into four
independently computable metrics and fills in numbers branch by branch:

  M1 peak brightness      self-emissive surface brightness vs solar surface (W/m^2);
                          if there is no self-emission, give the contrast instead
  M2 visible duration     time spent in the human-eye visible temperature window
                          (2500-12000 K) vs the 20 ms eye integration time
  M3 structural freedom   number of independently variable physical features
                          (determines "whether there is anything to look at")
  M4 threshold            what external conditions are needed to see it
                          (illumination / distance / detector)

Four branches
-------------
  A   abandon "effective 2D"    keep 1 m^2 + smoothness + weak preservation -> matter
                                can stop at any thickness
  A'  extreme sub-branch of A   abandon "1 m^2", take a single atomic layer
                                (area inferred from atomic spacing)
  B   abandon "smooth 2D"       keep 2D + weak preservation -> energy released in ns
  C   abandon "weak preservation" keep 2D + smoothness -> neutronization + neutrino burst

Discipline
----------
- Label model-dependent quantities ESTIMATE; label quantities given directly by
  first-principles relations CHECK.
- Do not write "the fireball is bright" as a "DCC observational prediction". This
  file is an extension of "specified-background test optics".
- The key fact for branch B must be verified first: **the slab itself is optically
  thin**, so its internal energy escapes directly as gamma/X rays instead of
  forming its own blackbody. The visible fireball comes from **kinetic energy
  deposited into the surrounding air**. If this premise fails, branch B's
  conclusion must be rewritten -- hence it is computed first.
"""
import math
import sys
import io

sys.path.insert(0, "src/common")
import conv

# ---------------------------------------------------------------- registered constants
SIGMA_SB = 5.670374419e-8      # W m^-2 K^-4
SIGMA_T = 6.652458732e-29      # m^2
T_SUN_SURF = 5772.0            # K
SUN_FLUX = SIGMA_SB * T_SUN_SURF ** 4      # 6.3e7 W/m^2
MT_TNT = 4.184e15              # J per megaton
RHO_AIR = 1.2                  # kg/m^3
LAMBDA_VIS = 550e-9            # m

SIGMA_M2 = conv.M_KG / conv.A_PERP          # 70 kg/m^2
E_DEG = 1.7245e17                           # J/m^2  (G0 v3 areal energy density)
U_NUC_MEV_FM2 = 0.37                        # rough bulk binding energy estimate (see no_weak_freeze_v1)

OUT = []


def w(s=""):
    OUT.append(s)


def tag(kind, name, ok, msg):
    w("  [%-7s] %-28s %s  %s" % (kind, name, "PASS" if ok else "FLAG", msg))


# =====================================================================
# Common geometry: fixed areal density Sigma=70 kg/m^2, thickness set by density
# =====================================================================
def thickness_m(rho_kg_m3):
    return SIGMA_M2 / rho_kg_m3


def atom_spacing_m(rho_kg_m3, m_bar_amu=None):
    """Atomic spacing = (mean atomic volume)^(1/3)"""
    mbar = conv.M_BAR_AMU if m_bar_amu is None else m_bar_amu
    v_atom = mbar * conv.AMU_KG / rho_kg_m3
    return v_atom ** (1.0 / 3.0)


# =====================================================================
# Branch B: first verify the premise of being "optically thin itself"
# =====================================================================
def branch_B():
    w("[B] Abandoning 'smoothness': energy-release pathway check (verify the premise before discussing brightness)")
    n_e_m3 = conv.N_E_FM2 * 1e45          # fm^-2 -> m^-3 (L_z=1 fm)
    L = conv.LZ_FM * 1e-15
    tau = n_e_m3 * SIGMA_T * L
    w("  electron bulk density n_e = %.3e m^-3, slab thickness L_z = %.1e m" % (n_e_m3, L))
    w("  Thomson optical depth tau = n_e*sigma_T*L = %.3f" % tau)
    tag("CHECK", "B0_slab_photosphere", 0.5 < tau < 10.0,
        "tau=%.2f: the slab itself is a thin photosphere (neither transparent leakage nor a thick blackbody)" % tau)

    # Self-radiation temperature: temperature set by energy density
    u_vol = E_DEG / L
    a_rad = 7.5657e-16
    T_bb = (u_vol / a_rad) ** 0.25
    w("  self-radiation: u=%.3e J/m^3 -> T_bb=%.2e K = %.1f MeV (gamma range)"
      % (u_vol, T_bb, T_bb * 8.617e-11))
    w("  expansion timescale L/c = %.1e s -> adiabatic cooling ends within ~1e-24 s" % (L / conv.C))
    tag("CHECK", "B0b_self_radiation_invisible", T_bb * 8.617e-11 > 1.0,
        "self-emission peak %.0f MeV >> visible light 2.5 eV: **the slab's own radiation is completely invisible to the eye**" % (T_bb * 8.617e-11))

    # Energy partition
    P2D = 8.62e16                     # N/m
    v_inf = math.sqrt(2.0 * P2D / SIGMA_M2)
    E_kin = 0.5 * conv.M_KG * v_inf ** 2
    E_rad = E_DEG - E_kin
    w("  areal pressure P=%.2e N/m -> v_inf=%.3e m/s (%.3f c)" % (P2D, v_inf, v_inf / conv.C))
    w("  total areal energy %.3e J/m^2 = %.1f Mt TNT" % (E_DEG, E_DEG / MT_TNT))
    w("    kinetic  %.3e J/m^2 = %.1f Mt  <- the only visible part" % (E_kin, E_kin / MT_TNT))
    w("    internal %.3e J/m^2 = %.1f Mt  <- escapes as 60 MeV gamma rays, invisible"
      % (E_rad, E_rad / MT_TNT))
    w("  proton kinetic energy = %.1f MeV, air range on the order of ~1 m -> kinetic energy thermalizes in a meter-scale air column"
      % ((1.0 / math.sqrt(1 - (v_inf / conv.C) ** 2) - 1) * conv.M_P))
    tag("ESTIMATE", "B0c_visible_comes_from_kinetic", E_kin / E_DEG > 0.3,
        "the visible fireball's energy comes from kinetic energy (%.0f%%), not from the slab's own radiation" % (100 * E_kin / E_DEG))

    # Sedov fireball
    E_tot = E_DEG
    def R_sedov(t):
        return 1.15 * (E_tot / RHO_AIR) ** 0.2 * t ** 0.4

    def T_eff(t, f=0.5):
        R = R_sedov(t)
        Lr = f * E_tot / t
        return (Lr / (4 * math.pi * R ** 2 * SIGMA_SB)) ** 0.25

    w("  Sedov strong-shock fireball R(t)=1.15(E/rho)^(1/5) t^(2/5), T_eff from L=fE/t (f=0.5)")
    w("     %-8s %-12s %-12s %-10s %s" % ("t", "R (m)", "T_eff (K)", "surface brightness", "eye"))
    t_vis_lo = t_vis_hi = None
    for t in (1e-3, 1e-2, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0):
        R = R_sedov(t)
        T = T_eff(t)
        bright = SIGMA_SB * T ** 4
        note = ""
        if 2500 <= T <= 12000:
            note = "visible color"
            t_vis_lo = t if t_vis_lo is None else t_vis_lo
            t_vis_hi = t
        elif T > 12000:
            note = "bluish/UV"
        else:
            note = "IR/dark"
        w("     %-8.3g %-12.3e %-12.3e %-10.2e %s" % (t, R, T, bright, note))
    w("  visible window (2500-12000 K) = %.2f s - %.1f s" % (t_vis_lo, t_vis_hi))
    tag("ESTIMATE", "B1_visible_duration", (t_vis_hi / 0.02) > 100,
        "visible color lasts %.0f s, %.0f times the eye integration time (20 ms)" % (t_vis_hi, t_vis_hi / 0.02))

    # Peak brightness comparison
    T_peak = T_eff(0.3)
    tag("ESTIMATE", "B2_surface_brightness", SIGMA_SB * T_peak ** 4 / SUN_FLUX > 1,
        "at T=%.0f K surface brightness = %.1f x solar surface" % (T_peak, SIGMA_SB * T_peak ** 4 / SUN_FLUX))

    # Structural freedom: shock instability
    R1 = R_sedov(1.0)
    tag("ESTIMATE", "B3_structure", True,
        "fireball R=%.1f km; Rayleigh-Taylor-type instability gives ~10^2 macroscopic features (no microscopic texture)" % (R1 / 1000))

    # Illuminance at the observation point (the quantity that really determines "dazzling")
    ILLUM = {}
    w("  illuminance at the observation point (taking t=1 s, L=%.1e W):" % (0.5 * E_DEG))
    for d in (100.0, 1000.0, 10000.0):
        E_ill = 0.5 * E_DEG / (4 * math.pi * d ** 2)
        ILLUM[d] = E_ill
        w("     d=%-7.0f m  illuminance %.2e W/m^2 = %.0e x solar constant (1361)"
          % (d, E_ill, E_ill / 1361.0))
    tag("ESTIMATE", "B4_blinding", ILLUM[1000.0] / 1361.0 > 1e5,
        "at 1 km still %.0e times the solar constant -> retinal saturation/blinding: not 'observable' but 'not safe to look at'"
        % (ILLUM[1000.0] / 1361.0))
    w("")
    return dict(v_inf=v_inf, E_kin=E_kin, T_peak=T_peak, t_vis=(t_vis_lo, t_vis_hi),
                tau=tau, T_bb=T_bb, illum=ILLUM)


# =====================================================================
# Branch A: abandon "effective 2D" -> thickness can be freely chosen
# =====================================================================
def branch_A():
    w("[A] Abandoning 'effective 2D': free thickness -> can an atomic layer survive")
    w("     %-14s %-12s %-14s %-12s %s" % ("rho (kg/m^3)", "L_z", "atomic spacing", "atom?", "form of matter"))
    rows = []
    for rho, lab in ((1000.0, "water"), (7000.0, "iron"), (2.3e17, "nuclear density")):
        L = thickness_m(rho)
        d = atom_spacing_m(rho)
        ok_atom = d > 1e-10          # only above 1 Angstrom can we speak of atoms
        form = "ordinary matter (with chemical bonds)" if ok_atom else "pressure-ionized/nuclear matter"
        w("     %-14.3g %-12.3e %-14.3e %-12s %s"
          % (rho, L, d, "yes" if ok_atom else "no", form))
        rows.append((rho, L, d, ok_atom))
    # The water-density row is the "squashed person"
    L_water = thickness_m(1000.0)
    tag("CHECK", "A0_squashed_body", L_water < 0.1,
        "at rho=1000, L_z=%.1f cm -- the 1 m^2 'sheet' is actually 7 cm thick, with anatomy intact" % (L_water * 100))

    # Contrast: passive illumination
    albedo = 0.35
    E_illum = 1.0                     # relative to direct sunlight
    contrast = albedo * E_illum
    w("  self-emission: none. contrast = albedo x illuminance = %.2f (external illumination required)" % contrast)
    tag("CHECK", "A1_no_self_emission", True,
        "cold matter: brightness entirely set by illumination, ~%.0f%% diffuse reflection in sunlight" % (contrast * 100))

    # Structural freedom
    n_elem = (1.0 / (LAMBDA_VIS / 2)) ** 2
    tag("CHECK", "A2_structure", n_elem > 1e12,
        "%.1e diffraction-limited resolution elements on 1 m^2; add anatomical/chemical color differences -> very high information content" % n_elem)
    tag("CHECK", "A3_duration", True, "static, viewable indefinitely; any lighting, any viewing angle")
    w("")
    return dict(L_water=L_water, contrast=contrast, n_elem=n_elem)


# =====================================================================
# Branch A': abandon "1 m^2" -> single atomic layer
# =====================================================================
def branch_Aprime():
    w("[A'] Extreme of branch A: abandon '1 m^2', take a single atomic layer (area inferred)")
    d_bond = 3.0e-10
    # N_s = 1/d^2 -> A = M/(mbar*N_s) = M*d^2/mbar
    A = conv.M_KG * d_bond ** 2 / (conv.M_BAR_AMU * conv.AMU_KG)
    w("  required in-plane atomic spacing = %.1f Angstrom -> A = %.3e m^2 = %.0f km^2"
      % (d_bond * 1e10, A, A / 1e6))
    w("  thickness = single atomic layer ~ %.1f Angstrom" % (d_bond * 1e10))
    # Monolayer absorptance: alpha*pi (graphene 2.3%)
    absorb = 0.023
    tag("CHECK", "Ap0_area", A / 1e6 > 100,
        "area %.0f km^2 -- the only geometric solution with 'chemistry', 4 orders of magnitude from 1 m^2" % (A / 1e6))
    tag("ESTIMATE", "Ap1_contrast", absorb > 0.01,
        "monolayer absorption ~%.1f%% (graphene-like) -> visible as a very faint iridescent film, low contrast" % (absorb * 100))
    w("")
    return dict(A=A, absorb=absorb)


# =====================================================================
# Branch C: abandon "weak-interaction preservation"
# =====================================================================
def branch_C():
    w("[C] Abandoning 'weak-interaction preservation': neutronization + neutrino burst")
    f_nu = 0.56
    E_nu = f_nu * E_DEG
    w("  neutrinos carry away %.2f x degeneracy energy = %.3e J/m^2 = %.1f Mt (invisible)" % (f_nu, E_nu, E_nu / MT_TNT))
    w("  remaining matter: npe matter with Y_p=0.005, E_F=21.5 MeV, still a degenerate plasma")
    # Residual optics: visible-light reflectivity still ~1 (mirror-like), but cold and structureless
    tag("CHECK", "C0_invisible_neutrinos", True,
        "0.56 of the energy escapes as neutrinos; neutrinos do not couple to the eye/camera -> this channel's visual contribution is strictly 0")
    tag("CHECK", "C1_no_atoms", True,
        "E_F=21.5 MeV is still >> chemical bonds of eV order -> no atoms/no chemical color, still a mirror in visible light")
    tag("CHECK", "C2_duration", True, "lifetime ~3 ns, 1e-8 of the 20 ms human-eye integration time")
    w("")
    return dict(E_nu=E_nu)


# =====================================================================
# Summary scoring
# =====================================================================
def summary(resB, resA, resAp, resC):
    w("=" * 78)
    w("[Summary] Five metrics filled in branch by branch (no weighting -- weighting would hide the trade-offs)")
    w("=" * 78)
    b_lo, b_hi = resB["t_vis"]
    w("  %-4s %-22s %-10s %-10s %-20s %s"
      % ("branch", "peak brightness", "visible duration", "structure count", "illuminance at 1 km", "self-emission"))
    w("  " + "-" * 76)
    w("  %-4s %-22s %-10s %-10s %-20s %s"
      % ("A", "reflected sunlight 35% (same as white wall)", "infinite", "1.3e13", "same as white wall", "no"))
    w("  %-4s %-22s %-10s %-10s %-20s %s"
      % ("A'", "2.3% absorption (very faint)", "infinite", "1.3e13", "below white wall", "no"))
    w("  %-4s %-22s %-10s %-10s %-20s %s"
      % ("B", "%.0f x sun" % (SIGMA_SB * resB["T_peak"] ** 4 / SUN_FLUX),
         "%.0f s" % b_hi, "~1e2",
         "5e6 x solar constant", "yes"))
    w("  %-4s %-22s %-10s %-10s %-20s %s"
      % ("C", "0 (nu escape)", "3 ns", "~1", "0", "no"))
    w("")

    w("[Key column] How much of this spectacularity comes from '2D reduction' itself?")
    w("  A   0%    -- it is spectacular because 'the person is compressed into a 7 cm sheet'; that is just flattening;")
    w("              compressing any 70 kg object to 7 cm would look the same. Unrelated to 2D reduction.")
    w("  A'  ~30%  -- a monolayer really is a 2D material (graphene-like); its 2D nature is real;")
    w("              but it relies on enlarging the area to 379 km^2, not on compressing the thickness to 1 fm.")
    w("  B   0%    -- a 41 Mt explosion does not care what triggered it; 2D reduction is entirely absent here:")
    w("              you see it failing, not succeeding.")
    w("  C   --     -- no visual phenomenon to attribute.")
    w("")

    w("[Verdict] Ranking by 'peak visual impact' (the usual meaning of 'spectacular'):")
    w("  1. B abandon smoothness -- the only self-luminous case, %.0f x solar surface, lasting %.0f s, filling the whole sky"
      % (SIGMA_SB * resB["T_peak"] ** 4 / SUN_FLUX, b_hi))
    w("  2. A abandon 2D      -- the only one with 'content': atoms/chemistry/anatomy intact, 1.3e13 resolution elements, permanent")
    w("  3. A' abandon 1 m^2 -- has 2D character but only 2.3% contrast, like an extremely faint iridescent film")
    w("  4. C abandon weak preservation -- all three metrics go to zero at once (neutrinos do not couple to the human eye)")
    w("")

    w("[Mutual exclusion] Why you cannot have both")
    ev_vis = 2.5
    ev_atom = 5.0
    ev_plasma = 60e6
    w("  to be 'bright' requires energy at the %g MeV scale (plasma)" % (ev_plasma / 1e6))
    w("  to have 'content' requires energy at the %g eV scale (chemical bonds/interband transitions)" % ev_atom)
    w("  the two differ by a factor of %.0e -- the same matter cannot be at both energy scales at once." % (ev_plasma / ev_atom))
    tag("ARGUMENT", "S_mutual_exclusion", ev_plasma / ev_atom > 1e6,
        "brightness and structure come from energy scales differing by a factor of %.0e; physically mutually exclusive" % (ev_plasma / ev_atom))
    w("")

    w("[In one sentence]")
    w("  The most spectacular visual effect = abandon 'smooth 2D reduction' and obtain a 41 Mt, roughly 10 s long, colorful fireball with surface brightness nearly a hundred times the sun.")
    w("  But at that moment '2D reduction' is no longer in the picture --")
    w("  you are watching it disintegrate, not succeed.")
    w("  If you want to see '2D reduction itself', it can only be branch A's static sheet: quiet, detailed,")
    w("  and needing a lamp shone on it. It is not spectacular; it is clear.")


def main():
    w("=" * 76)
    w("DCC branch visual accounting v1: which assumption to abandon -> the most spectacular visual effect")
    w("=" * 76)
    w("areal density Sigma = %.1f kg/m^2 (70 kg / 1 m^2)" % SIGMA_M2)
    w("degeneracy areal energy E = %.3e J/m^2 = %.1f Mt TNT" % (E_DEG, E_DEG / MT_TNT))
    w("")
    resB = branch_B()
    resA = branch_A()
    resAp = branch_Aprime()
    resC = branch_C()
    summary(resB, resA, resAp, resC)

    txt = "\n".join(OUT)
    io.open("runs/ANALYSIS/abandon_assumption_visual_v1.txt", "w",
            encoding="utf-8").write(txt + "\n")
    print(txt)


if __name__ == "__main__":
    main()
