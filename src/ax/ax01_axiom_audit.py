"""AX-01 axiom audit of the DCC programme.

Reports epistemic labels, derivation chains, coordinate-dependence tests and blast radii for
every premise the programme currently treats as fixed.  This instrument NEVER vetoes, never
repairs a product, never advances a gate, threshold, terminal class or D-state, and never
interprets its own findings.

Run:  python -I src/ax/ax01_axiom_audit.py           # dry run -> stdout
      python -I src/ax/ax01_axiom_audit.py --write   # emit runs/AX/ax01_axiom_audit_results.txt
"""
import datetime
import hashlib
import math
import os
import sys

import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PRODUCT = os.path.join(ROOT, 'runs', 'AX', 'ax01_axiom_audit_results.txt')
REGISTRATION = os.path.join(ROOT, 'runs', 'AX', 'ax01_axiom_audit_registration.md')
REG_SHA_REGISTERED = 'a2c39364620cdce67cf3bfaa251a19163fad6b506d5ac975694be64f6ecd9059'

A = []
WRITES = []


def a(line=''):
    A.append(line)


# ----------------------------------------------------------------- constants
A0_BOHR = 5.29177210903e-11          # m, CODATA
HBARC_MEV_FM = 197.3269804
M_OBJ, A_PERP, MBAR_AMU = 70.0, 1.0, 10.0
N_S = 4.2155e27                      # m^-2, v3 baseline
N_2D_ELECTRON = 2.2000e28            # m^-2, carrier areal density
L_Z_FM = 1.0
SPACING_NM = 0.3
SHORTFALL = 3.4387e10                # ladder E1
C_MEASURED = 3.3166                  # ladder E3, narrow-environment contrast
C_EYE = 0.01                         # Weber
PHI_MEV = 2.25                       # declared band centre
BAND_EV = (1.65, 3.26)
SUN_FLUX = 2.7740e21                 # m^-2 s^-1 at 2.25 eV

# ----------------------------------------------------------------- items
# id, label, subject, one-line description, root citation, blast radius
ITEMS = [
    ('AX-G01', 'MEASURED', 'a0 = 5.2917721e-11 m',
     'Bohr radius used as the denominator of 2.91e-4 a0; the standard CODATA value, not a '
     'model-specific effective radius, although the record does apply m* corrections elsewhere '
     '(omega_p) and not here',
     'G0p_seven_row_verdict_v3.md:47; constraint_crosswalk_v1.md:217',
     ['G0p-row-1', 'RL-6']),

    ('AX-G02', 'DERIVED-COVARIANT', 'N_s = M/(mbar A_perp) = 4.2155e27 m^-2',
     'nuclear column density; identity from particle-number conservation at fixed projected area',
     'dimensional_conventions_v1.md:16',
     ['AX-G03', 'C1', 'n_2D']),

    ('AX-G03', 'DERIVED-COORD', 'd_parallel = 15.40 fm = N_s^-1/2',
     'mean in-plane nuclear column pitch quoted as a length; equals 2.911e-4 a0 for the '
     'registered object',
     'constraint_crosswalk_v1.md:215-222; G0p_seven_row_verdict_v3.md:47',
     ['G0p-row-1', 'RL-6', 'ME1', 'C1', 'terminal-answer']),

    ('AX-G04', 'CONVENTION', 'metric ansatz ds^2 = -dt^2+dx^2+dy^2+f(t,x)^2 dz^2',
     'N=1, beta=0, g_xx=g_yy=1, c=1; forbids shift, transverse conformal factor and lapse '
     'variation',
     'phase1_symbolic_constraint_results.txt:5',
     ['AX-D01', 'AX-D02', 'AX-D04', 'G5p']),

    ('AX-G05', 'CONVENTION', 'L_z = 1.0 fm (density-inferred)',
     'normalisation fixed by 70 kg / (1 m^2 x 0.026 n_nuc); sets E_sub and the optics column, '
     'not the 2D claim itself',
     'dimensional_conventions_v1.md:18,110',
     ['E_sub', 'RL-4', 'AX-L01', 'n_B']),

    ('AX-G06', 'CONVENTION', 'atomic spacing 0.3 nm',
     'representative molecular/atomic spacing (3 A); not measured for the object',
     'scifi_boundary_v1.md:88; meff_boundary_disposition_v1.md:168',
     ['RL-6', 'G0p-row-1']),

    ('AX-G07', 'ASSUMPTION', 'd_parallel used as the plate thickness',
     'RL-6 denominator and ME1/C1b thickness identify the in-plane pitch with the z-thickness; '
     'the crosswalk calls this a modelling choice, the ladder does not carry the qualification',
     'constraint_crosswalk_v1.md:227-236; relaxation_ladder_v1.md:41',
     ['RL-6', 'ME1', 'C1', 'AX-T04']),

    ('AX-G08', 'CONVENTION', 'reference object (70 kg, 1 m^2, 10 amu)',
     'd_parallel scales as (A_perp/M)^1/2; without it 2.91e-4 a0 is incomplete',
     'dimensional_conventions_v1.md:12',
     ['AX-G02', 'AX-G03', 'RL-6', 'A_min']),

    ('AX-G09', 'CONVENTION', 'Z/A = 0.522',
     'frozen-state composition; fixes n_2D, E_F and every capture margin',
     'dimensional_conventions_v1.md:12',
     ['n_2D', 'EF', 'G0p-row-7']),

    ('AX-G10', 'ASSUMPTION', 'T = 0 for the frozen state',
     'Fermi sea taken at zero temperature; no argument that the transient is cold',
     'G0p_seven_row_verdict_v3.md:32',
     ['EF', 'G0p-row-7']),

    ('AX-D01', 'DERIVED-COORD', 'kappa*rho_req = -f_xx/f',
     'Hamiltonian constraint solved for the required energy density in the ansatz gauge; takes '
     'this form only with Lambda=0 and j=0',
     'phase1_symbolic_constraint_results.txt:21',
     ['G5p', 'AX-S03']),

    ('AX-D02', 'DERIVED-COORD', 'kappa*j_x,req = d_x(f_t/f)',
     'momentum constraint solved for the required x-flux; same gauge conditions, Lambda drops out',
     'phase1_symbolic_constraint_results.txt:22',
     ['G5p', 'AX-S03']),

    ('AX-D03', 'DERIVED-COVARIANT', 'j_y = j_z = 0',
     'consequence of the d_y, d_z Killing vectors of the ansatz, not an extra physical assumption',
     'phase1_symbolic_constraint_results.txt:29',
     ['G5p']),

    ('AX-D04', 'DERIVED-COVARIANT', 'K^2 - K_ij K^ij = 0',
     'identity of the ansatz (K_xx=K_yy=0, K_zz=-f f_t), not an independently imposed constraint',
     'phase1_symbolic_constraint_results.txt:20',
     ['G5p', 'AX-D01']),

    ('AX-D05', 'ASSUMPTION', 'Lambda = 0',
     'no cosmological term appears in either constraint equation; the omission is nowhere '
     'declared',
     'phase1_symbolic_constraint_results.txt:21-22 (no Lambda term)',
     ['AX-D01', 'AX-D02', 'G5p']),

    ('AX-D06', 'CONVENTION', 'c=1, G, hbar unit fixing',
     'unit choice only; every audited ratio is dimensionless',
     'phase1_symbolic_constraint_results.txt:5',
     ['NO-DOWNSTREAM']),

    ('AX-T01', 'DERIVED-COORD', 'Phi = -4.5 orders',
     '3.4387e10 x (1e-7/3.3166)^2 = 3.126e-5, log10 = -4.505; consumes a scene-measured '
     'contrast, a band, a Weber constant and an environment',
     'relaxation_ladder_v1.md:233-236; DCC_terminal_answer_v1.md:5',
     ['D8', 'RL-1', 'RL-2', 'terminal-answer']),

    ('AX-T02', 'CONVENTION', 'V = epsilon',
     'the violation currency is defined to equal the relief ratio; no derivation that this is '
     'the violation magnitude',
     'relaxation_ladder_v1.md:37',
     ['RL-2', 'D8', 'terminal-answer']),

    ('AX-T03', 'UNVERIFIED', 'the value of epsilon',
     'epsilon is a dial; E2 measured that C is not a function of relief/pitch and that useful '
     'travel is 5e-4 of range',
     'relaxation_ladder_v1.md:176-193',
     ['RL-2', 'D8']),

    ('AX-T04', 'DERIVED-COORD', 'RL-6 = 2e4 x atomic spacing',
     '0.3 nm / 15.402 fm = 1.948e4 rounded to 2e4 (2.60%); recomputed with the other candidate '
     'lengths the price spans 15.4x',
     'relaxation_ladder_v1.md:41,289',
     ['RL-6', 'G0p-row-1', 'terminal-answer']),

    ('AX-T05', 'CONVENTION', 'purchasable / not purchasable',
     'binary relative to an undeclared budget; two incommensurable currencies are ordered '
     'ordinally, not summed',
     'relaxation_ladder_v1.md:13-29',
     ['RL-5', 'RL-6', 'PG-03', 'terminal-answer']),

    ('AX-T06', 'MEASURED', 'full sun 2.7740e21 m^-2 s^-1 at 2.25 eV',
     'solar irradiance converted to photon flux in the declared band',
     'relaxation_ladder_v1.md:56',
     ['AX-T01', 'D8']),

    ('AX-T07', 'CONVENTION', 'declared band 2.25 eV (1.65-3.26 eV)',
     'instrument band; the whole Phi line is denominated in it',
     'relaxation_ladder_v1.md:36',
     ['AX-T01', 'RL-1', 'RL-4']),

    ('AX-L01', 'CONVENTION', 'effective-2D four-slot conditional',
     'model ^ subsystem ^ E_occ<dE_z ^ E_probe<dE_z => z not excitable; a stipulated definition '
     'carrying no frame slot',
     'effective_2d_definition_v1.md:21-30',
     ['G5p', 'N7', 'AX-L03']),

    ('AX-L02', 'CONVENTION', 'observation scale (theta tuple)',
     'aperture, gate, band, distance, plus environment E and camera G; set by the experimenter',
     'relaxation_ladder_v1.md:84; theta_environment_v1.md',
     ['RL-1', 'RL-2', 'Q3', 'AX-T01']),

    ('AX-L03', 'ASSUMPTION', "'frozen' degrees of freedom",
     'freezing is defined relative to the frame in which the well is static; no frame is named',
     'effective_2d_definition_v1.md:84',
     ['AX-L01', 'G5p', 'E_sub']),

    ('AX-L04', 'CONVENTION', 'Kasner f=t as the negative control',
     'chosen because it is the p=1 power law with K=0; the flat sector is exactly f affine in '
     '(t,x)',
     'phase1b_singularity_results.txt:29',
     ['G0p-row-1', 'AX-L05']),

    ('AX-L05', 'UNVERIFIED', "row 1 reverse-on: 'none stated (geometric, convention-independent)'",
     'd_parallel is fixed only once (M, A_perp, mbar) are fixed, so the parenthetical has no '
     'derivation on file',
     'G0p_seven_row_verdict_v3.md:47; DCC_terminal_answer_v1.md:9; '
     'constraint_crosswalk_v1.md:215-222',
     ['G0p-row-1', 'terminal-answer']),

    ('AX-S01', 'ASSUMPTION', 'existence of a continuous controlled 3D->2D route',
     'the deposit is a kinematic map; no dynamical mechanism is on file, and C1 has no '
     'non-degenerate test',
     'constraint_crosswalk_v1.md:100-115',
     ['D8', 'PG-03', 'terminal-answer']),

    ('AX-S02', 'ASSUMPTION', 'adiabaticity of the smooth 2D-ization branch',
     'never stated as a condition; the record measures thickness returning 1.9e4x before t_rip '
     'and in-plane settling 2.2e4x after, ratio 4.19e8',
     'kinematic_vs_dynamic_unfolding_v1.md:153-159',
     ['C2', 'D8', 'terminal-answer']),

    ('AX-S03', 'ASSUMPTION', 'L_z as external control parameter (no back-reaction)',
     'holding L_z needs a stress source; Phase 1 finds the required source and assigns it to no '
     'field',
     'phase1_symbolic_constraint_results.txt:35-42',
     ['RL-2', 'RL-5', 'AX-D01', 'terminal-answer']),

    ('AX-X01', 'CONVENTION', 'C_eye = 0.01 (Weber)',
     'physiological contrast constant; sets every Q3 and the 3e-2 L3 threshold',
     'intrinsic_structure_tiers_v1.md:139',
     ['Q3', 'L3', 'RL-2']),

    ('AX-X02', 'CONVENTION', 'Q3 = log2(1 + C/C_eye)',
     'legibility law; monotone in C, with no derivation of the log form',
     'intrinsic_structure_tiers_v1.md:149',
     ['Q3', 'RL-1', 'RL-2', 'RL-3']),

    ('AX-X03', 'CONVENTION', 'lambda = 500 nm',
     'the wavelength at which C1 optical test is vacuous (lambda/d_parallel = 3.2e7)',
     'constraint_crosswalk_v1.md:105',
     ['C1', 'ME1']),

    ('AX-X04', 'ASSUMPTION', 'neglected pair-plasma back-reaction in RL-5',
     'E4 records it as ignored and as helping the rung; no error bound is on file',
     'relaxation_ladder_v1.md:266-271',
     ['RL-5', 'D8']),
]

PARENTS = {
    'AX-G01': ['EXT:codata-a0'],
    'AX-G02': ['EXT:particle-number-conservation', 'AX-G08'],
    'AX-G03': ['AX-G02', 'AX-G01'],
    'AX-G04': ['EXT:gauge-choice'],
    'AX-G05': ['AX-G08', 'EXT:n-nuc-0.026'],
    'AX-G06': ['EXT:molecular-resolution'],
    'AX-G07': ['AX-G03', 'AX-G05'],
    'AX-G08': ['EXT:object-definition'],
    'AX-G09': ['AX-G08'],
    'AX-G10': ['EXT:frozen-state'],
    'AX-D01': ['AX-G04', 'AX-D05', 'AX-D03', 'AX-D04'],
    'AX-D02': ['AX-G04', 'AX-D05', 'AX-D03'],
    'AX-D03': ['AX-G04'],
    'AX-D04': ['AX-G04'],
    'AX-D05': ['EXT:vacuum-choice'],
    'AX-D06': ['EXT:unit-system'],
    'AX-T01': ['AX-T06', 'AX-T07', 'AX-X01', 'EXT:measured-contrast'],
    'AX-T02': ['EXT:currency-definition'],
    'AX-T03': ['AX-T02', 'EXT:relief-measurement'],
    'AX-T04': ['AX-G03', 'AX-G06', 'AX-G07'],
    'AX-T05': ['AX-T02', 'AX-T01', 'EXT:budget'],
    'AX-T06': ['EXT:solar-irradiance'],
    'AX-T07': ['EXT:instrument-band'],
    'AX-L01': ['AX-G05', 'AX-L03'],
    'AX-L02': ['EXT:experimenter-tuple'],
    'AX-L03': ['AX-G05', 'EXT:preferred-frame'],
    'AX-L04': ['EXT:power-law-family'],
    'AX-L05': ['AX-G03', 'AX-G08'],
    'AX-S01': ['AX-G03', 'EXT:kinematic-map'],
    'AX-S02': ['AX-S01', 'EXT:front-sweep-measurement'],
    'AX-S03': ['AX-D01', 'AX-G05'],
    'AX-X01': ['EXT:psychophysics'],
    'AX-X02': ['AX-X01'],
    'AX-X03': ['EXT:visible-band'],
    'AX-X04': ['EXT:pair-production-rate'],
}

TOKENS = {
    'G0p-row-1', 'G0p-row-7', 'terminal-answer', 'D8', 'PG-03', 'G5p', 'C1', 'C2', 'N7',
    'ME1', 'Q3', 'L3', 'RL-1', 'RL-2', 'RL-3', 'RL-4', 'RL-5', 'RL-6', 'EF', 'n_2D', 'n_B',
    'E_sub', 'A_min', 'NO-DOWNSTREAM',
}

# ----------------------------------------------------------------- computed quantities
D_PAR = 1.0 / math.sqrt(N_S)                       # m
D_PAR_FM = D_PAR / 1e-15
D_PAR_A0 = D_PAR / A0_BOHR
D_PAR_V3_FM = 1.0 / math.sqrt(N_2D_ELECTRON) / 1e-15
R_154 = (SPACING_NM * 1e-9) / (15.402e-15)
R_674 = (SPACING_NM * 1e-9) / (D_PAR_V3_FM * 1e-15)
R_1FM = (SPACING_NM * 1e-9) / (L_Z_FM * 1e-15)
PHI = SHORTFALL * (1e-7 / C_MEASURED) ** 2
PHI_LOG = math.log10(PHI)
Q3 = math.log2(1 + C_MEASURED / C_EYE)
Q3_DBL = math.log2(1 + C_MEASURED / (2 * C_EYE))
DEZ_FM = math.pi * HBARC_MEV_FM / L_Z_FM                # MeV at L_z = 1 fm
DEZ_250NM_EV = (math.pi * HBARC_MEV_FM / 250e6) * 1e6   # MeV -> eV
GAMMA_FLIP = DEZ_250NM_EV / PHI_MEV
ESUB_1NM_EV = (math.pi * HBARC_MEV_FM / 1e6) * 1e6
EF_SHIFT_ZA = 6.2221 * (math.sqrt(0.500 / 0.522) - 1)

# ----------------------------------------------------------------- symbolic
t, x, eps = sp.symbols('t x epsilon', real=True)
f = sp.Function('f')(t, x)
ft, fx = sp.diff(f, t), sp.diff(f, x)
ftt, fxx, ftx = sp.diff(f, t, 2), sp.diff(f, x, 2), sp.diff(f, t, x)
K = -ft / f
KijKij = ft ** 2 / f ** 2
IDENT_D04 = sp.simplify(K ** 2 - KijKij)
F_EXT = t + eps * x ** 2
K_EXT = sp.simplify(
    (4 * (sp.diff(F_EXT, t, 2) ** 2 + sp.diff(F_EXT, x, 2) ** 2
          - 2 * sp.diff(sp.diff(F_EXT, t), x) ** 2)) / F_EXT ** 2)
K_EXT_TARGET = 16 * eps ** 2 / F_EXT ** 2

# ----------------------------------------------------------------- tests
# (item, transformation, survives, note)
TESTS = [
    ('AX-G03', 'area-preserving transverse diffeo x->Lx, y->y/L; then reinterpret as z-thickness',
     'PARTIAL',
     'd_parallel survives as a derived length from an invariant areal density (%.5f fm under the '
     'diffeo) but not as a thickness: the same plate is L_z=%.0f fm thick, a factor %.1f apart'
     % (D_PAR_FM, L_Z_FM, D_PAR_FM / L_Z_FM)),

    ('AX-G04', 'restore beta != 0 and a transverse conformal factor g_xx=g_yy=Omega^2',
     'NO',
     'a non-zero lapse divides out of H=0 and is immaterial; the restriction is beta=0 and the '
     'unit transverse metric. With beta != 0 the momentum constraint gains a j_x source and the '
     'Hamiltonian the shift scalar, so K=-f_t/f and kappa*rho_req=-f_xx/f are gauge-fixed. '
     'K_ijK^ij=(f_t/f)^2 is intrinsic to the slice and survives, so AX-D04 survives while the '
     'printed equations do not'),

    ('AX-G05', 'z -> z/lambda with f -> lambda f (proper length invariant); then L_z = 1 nm',
     'PARTIAL',
     'L_z as a proper length is diffeo-invariant; the number 1.0 fm is a normalisation chosen to '
     'reproduce n_nuc = 0.026 fm^-3. At L_z = 1 nm, E_sub falls %.1f MeV -> %.3f eV (1e6) and '
     'the internal bound E_F < dE_z fails' % (DEZ_FM, ESUB_1NM_EV)),

    ('AX-G06', 'spacing 0.3 nm -> 0.15 nm, and -> 1 nm',
     'NO',
     'RL-6 ratio scales as 1/spacing: %.3e, %.3e, %.3e. Ordering against the 1x bar is '
     'unaffected in all three' % (R_154, R_154 * 2, R_154 * 10 / 3)),

    ('AX-G07', 'replace d_parallel by L_z = 1 fm as the thickness',
     'NO',
     'RL-6 becomes %.3e (%.1fx larger); ME1 ratios 6.49e12 and 4.5e12 move by the same factor. '
     'The ordering sheet PASS / stack PASS / slab FAIL at 100 um is unchanged'
     % (R_1FM, R_1FM / R_154)),

    ('AX-G08', 'scale the object M -> 10M at fixed A_perp, and M -> 0.1M',
     'NO',
     'd_parallel ~ (A/M)^1/2: 15.402 fm -> %.3f fm at 10x mass and %.3f fm at 0.1x; the RL-6 '
     'ratio spans %.2e..%.2e' % (D_PAR_FM / math.sqrt(10), D_PAR_FM * math.sqrt(10),
                                 R_154 / math.sqrt(10), R_154 * math.sqrt(10))),

    ('AX-G09', 'Z/A 0.522 -> 0.500',
     'PARTIAL',
     'n_2D -4.2%%, E_F -2.1%% (6.2221 -> %.4f MeV at the ALL2D endpoint); the O16 margin at '
     'that endpoint grows from 0.342 to %.3f MeV. No classification flips'
     % (6.2221 + EF_SHIFT_ZA, 7.12 - (6.2221 + EF_SHIFT_ZA))),

    ('AX-G10', 'T -> 1 MeV',
     'NO',
     'E_F is the T=0 value. kT/E_F is 1.4% at 73.37 MeV but 16% at the ALL2D endpoint 6.22 MeV, '
     'and the 0.342 MeV endpoint margin is smaller than kT at 1 MeV, so the row-7 endpoint '
     'comparison is not T-robust'),

    ('AX-D01', 'add Lambda, and add j_x != 0',
     'NO',
     'kappa*rho_req = -f_xx/f + Lambda - (momentum terms); the printed form is the Lambda=0, '
     'j=0 slice. With Lambda the residual is exactly Lambda in the same units'),

    ('AX-D02', 'add Lambda; then add beta != 0',
     'PARTIAL',
     'Lambda is a constant and drops out of the momentum constraint, so D02 is Lambda-robust; '
     'with beta != 0 the required flux mixes into rho_req and the printed separation fails'),

    ('AX-D05', 'Lambda = 1e-3 fm^-2 against Lambda = 0',
     'NO',
     'rho_req shifts by Lambda/kappa, i.e. by exactly 1e-3 fm^-2 in the printed units; no bound '
     'on Lambda is on file, so the omission is not numerically negligible by record'),

    ('AX-D06', 'switch MeV/fm to GeV/fm',
     'YES',
     'every audited ratio is dimensionless; only printed values change'),

    ('AX-T01', 'boost beta = 0.5 along z: 2.25 eV -> %.3f eV' % (PHI_MEV * 1.5),
     'NO',
     '%.3f eV lies outside the declared %.2f-%.2f eV band, so the declared channel ceases to '
     'exist. Phi is an observer-frame number, not a scalar'
     % (PHI_MEV * 1.5, BAND_EV[0], BAND_EV[1])),

    ('AX-T02', 'boost along x: the pitch contracts by gamma, the relief does not',
     'PARTIAL',
     'epsilon = relief/pitch is a ratio of proper lengths at one point (invariant under '
     'transverse diffeos) but a beta=0.5 x-boost sends epsilon -> 1.155 epsilon'),

    ('AX-T03', 'none available',
     'N/A (justified)',
     'no value of epsilon is on file, so there is nothing to transform; E2 tested the dependence '
     'at the level of C, not epsilon, and found C independent of relief/pitch'),

    ('AX-T04', 'recompute with thickness 6.742 fm (v3 carrier spacing), then 1 fm (L_z)',
     'NO',
     'the ratio is %.4e at 15.402 fm, %.4e at 6.742 fm, %.4e at 1 fm: a %.1fx spread in the '
     'printed price, all with the same rounding to 2e4'
     % (R_154, R_674, R_1FM, R_1FM / R_154)),

    ('AX-T05', 'double the declared budget; move the observer to 1 AU',
     'NO',
     'the binary is a comparison against a declared budget and scene. RL-5 26.5-order overrun is '
     'measured against that budget and moves with it; RL-6 2e4 is a ratio of lengths and does '
     'not, so the two rungs are not on one axis even before the budget is chosen'),

    ('AX-T07', 'band centre 2.25 eV -> 3.00 eV',
     'NO',
     'the 9.539e31 requirement is band-independent while the solar flux in band falls, so the '
     'ratio Phi is denominated in the band and is not invariant under a band change'),

    ('AX-L01', 'z-boost at fixed dE_z, evaluated at both ends of the L_z domain',
     'PARTIAL',
     'at L_z = 1 fm, dE_z = %.1f MeV and the flip needs gamma = %.2e; at the external-bound edge '
     'L_z = 250 nm, dE_z = %.4f eV and the flip needs gamma = %.4f (beta = %.3f). The conditional '
     'has no frame slot, so its truth value is observer-dependent where its own domain ends'
     % (DEZ_FM, DEZ_FM * 1e6 / PHI_MEV, DEZ_250NM_EV, GAMMA_FLIP,
        math.sqrt(1 - 1 / GAMMA_FLIP ** 2))),

    ('AX-L02', 'aperture x10, gate x10 at fixed scene',
     'NO',
     'the observation scale is stipulated by the experimenter; it has no invariant content and '
     'the Q3 numbers move with it'),

    ('AX-L03', 'boost to a frame moving along z',
     'NO',
     "'frozen' presupposes the frame in which the well is static; the occupation distribution is "
     'not frame-independent, so the predicate is frame-relative'),

    ('AX-L04', 'extend the control to f = t + eps*x^2',
     'PARTIAL',
     'K = %s -> infinity as f -> 0, so the flat sector is exactly f affine in (t,x), a '
     'codimension-2 slice of (f_tt, f_xx, f_tx) space. The control is representative of a '
     'measure-zero set, not of the generic class; the Phase 1b qualitative conclusion is '
     'strengthened, not weakened' % K_EXT),

    ('AX-L05', 'substitute the frozen, charged and equilibrium objects in turn',
     'NO',
     'the same symbol resolves to 15.402 fm = 1/sqrt(N_s) (nuclear column) or 6.742 fm = '
     '1/sqrt(n_2D) (electron areal density), and both scale as (A_perp/M)^1/2; the parenthetical '
     'does not survive'),

    ('AX-S01', 'none available',
     'N/A (justified)',
     'a dynamical existence claim admits no coordinate test; the record contains no evolution '
     'solution (Phase 1 reports NOT an evolution solution, NOT a joint solution)'),

    ('AX-S02', 'compare the three settling timescales',
     'NO',
     'thickness returns in 2*delta/c_s = 4.30e-13 s, 1.9e4x before t_rip = 8.2553e-9 s; the '
     'in-plane arrangement settles at R/c_s = 1.8e-4 s, 2.2e4x after; R/(2 delta) = 4.19e8. No '
     'window exists in which the map is adiabatic'),

    ('AX-S03', 'ask what holds L_z fixed, pointwise under RL-2 relief',
     'NO',
     'the constraint returns a required source and Phase 1 assigns it to no field; controlled '
     'L_z therefore needs an unassigned stress, and RL-2 L_z(x) needs it pointwise'),

    ('AX-X01', 'C_eye 0.01 -> 0.02',
     'NO',
     'Q3(3.3166) %.5f -> %.5f; the L3 threshold moves from C=3e-2 to 6e-2, so RL-2 zero-margin '
     'pass at 3e-2 fails while Q3 stays above 2' % (Q3, Q3_DBL)),

    ('AX-X02', 'replace log2(1+C/C_eye) by C/C_eye',
     'NO',
     'Q3(3.3166) %.5f -> %.2f; every Q3 number and the L3 crossing move, the ordering does not'
     % (Q3, C_MEASURED / C_EYE)),

    ('AX-X03', 'lambda 500 nm -> 0.1 nm',
     'NO',
     'lambda/d_parallel = %.2e -> %.2e, still vacuous; making the test bite needs lambda ~ 15.4 '
     'fm. E = hc/lambda = %.1f MeV there; the crosswalk prints 80.5 MeV, which is 2*pi*hbar*c/d '
     'on the same length, so the two differ by 2*pi and the record does not state which is meant'
     % (500e-9 / D_PAR, 0.1e-9 / D_PAR, 197.3269804 / 15.402)),

    ('AX-X04', 'include the pair drain',
     'NO',
     'no error bound is on file; E4 states the omission helps the rung, so including it can only '
     'raise the 1.22e40 W/m^2 price'),

    # positive controls on the covariant items
    ('AX-G02', 'area-preserving transverse diffeo x->Lx, y->y/L',
     'YES',
     'N_s is particles per unit proper area; 4.2155e27 m^-2 is unchanged'),
    ('AX-D03', 'rotate in x-y; boost along z',
     'YES',
     'j_y=j_z=0 follows from the d_y, d_z Killing vectors; a z-boost preserves both'),
    ('AX-D04', 'arbitrary f(t,x): symbolic simplification',
     'YES',
     'K^2-K_ijK^ij simplifies to %s identically' % IDENT_D04),
]

FINDINGS = [
    ('HIGH',
     'd_parallel appears in the record in two roles: an in-plane column pitch (%.5f fm) and the '
     'plate thickness used by RL-6, ME1 and C1b. Replacing it by L_z = 1 fm moves the RL-6 ratio '
     'from %.3e to %.3e (%.1fx). constraint_crosswalk_v1.md 8.2 calls the identification a '
     'modelling choice; relaxation_ladder_v1.md 2 does not carry that qualification'
     % (D_PAR_FM, R_154, R_1FM, R_1FM / R_154)),

    ('HIGH',
     "row 1's reverse-on reads 'none stated (geometric, convention-independent)'. The same "
     'record states d_parallel is fixed only once (M, A_perp, mbar) are fixed and scales as '
     '(A_perp/M)^1/2 (constraint_crosswalk_v1.md 8.1). No derivation of convention-independence '
     'is on file'),

    ('HIGH',
     'K^2 - K_ijK^ij = 0 is an identity of the ansatz, not a separately imposed constraint: '
     'K_xx=K_yy=0 and K_zz=-f f_t make the two sides equal for every f(t,x) (symbolic residual '
     '%s). The term therefore cannot fail and carries no constraint information: the Hamiltonian '
     'constraint reduces to R^(3) = 2*kappa*rho. Phase 1 self-test SY2 already labels this IDENT, '
     'and IDENT is explicitly not counted as evidence' % IDENT_D04),

    ('HIGH',
     'adiabaticity is the unstated premise of the smooth 2D-ization branch. The record measures '
     'the opposite ordering: thickness returns 1.9e4x before t_rip, in-plane settles 2.2e4x '
     'after, ratio R/(2 delta) = 4.19e8 (kinematic_vs_dynamic_unfolding_v1.md:153-159)'),

    ('MEDIUM',
     'Lambda = 0 is nowhere declared and is not idle: it appears additively in kappa*rho_req and '
     'is absent from kappa*j_x,req only because it is a constant'),

    ('MEDIUM',
     'Phi = -4.5 is not a scalar. It consumes a scene-measured contrast (3.3166), a band '
     '(2.25 eV), a Weber constant (0.01) and an environment E; a beta=0.5 z-boost moves the '
     'probe to 3.375 eV, outside the declared 1.65-3.26 eV band'),

    ('MEDIUM',
     'L_z = 1 fm is a normalisation, but it does physical work: E_sub = %.1f MeV supplies the '
     'internal 2D argument, and the internal bound L_z <~ 2 fm is a bound on this normalisation. '
     'At L_z = 1 nm, E_sub = %.1f eV and the internal bound fails' % (DEZ_FM, ESUB_1NM_EV)),

    ('MEDIUM',
     'the effective-2D conditional has no frame slot. At the external-bound edge L_z = 250 nm the '
     'truth value flips at gamma = %.4f (beta = %.3f), inside the domain the definition itself '
     'admits' % (GAMMA_FLIP, math.sqrt(1 - 1 / GAMMA_FLIP ** 2))),

    ('LOW',
     'the Kasner control occupies a codimension-2 slice: for f = t + eps*x^2, K = %s diverges as '
     'f -> 0, and flatness requires f affine in (t,x). The Phase 1b generic-singular conclusion '
     'is strengthened; the control is not representative of the generic class' % K_EXT),

    ('LOW',
     'the printed RL-6 price 2e4 is a 2.60%% rounding of %.4e; disclosed already in '
     'runs/P1/phase1c_repricing_results.txt and listed here so the blast map is closed' % R_154),
]

# ----------------------------------------------------------------- checks
def sha256(path):
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def closure(items, parents, blasts):
    ids = [it[0] for it in items]
    idset = set(ids)
    errs = []
    for it in items:
        if it[1] not in ('MEASURED', 'DERIVED-COVARIANT', 'DERIVED-COORD',
                         'CONVENTION', 'ASSUMPTION', 'UNVERIFIED'):
            errs.append(('unlabelled', it[0]))
        if not it[4] or not str(it[4]).strip():
            errs.append(('no-root', it[0]))
        if not blasts.get(it[0]):
            errs.append(('no-blast', it[0]))
    for i in ids:
        if not parents.get(i):
            errs.append(('rootless', i))
    for i, ps in parents.items():
        for p in ps:
            if p.startswith('EXT:'):
                continue
            if p not in idset:
                errs.append(('dangling-parent', i, p))
    for i, bs in blasts.items():
        for b in bs:
            if b.startswith('AX-'):
                if b not in idset:
                    errs.append(('dangling-blast', i, b))
            elif b not in TOKENS:
                errs.append(('dangling-blast', i, b))
    return errs


def coverage(items, tests):
    need = [it[0] for it in items
            if it[1] in ('DERIVED-COORD', 'CONVENTION', 'ASSUMPTION', 'UNVERIFIED')]
    have = {t[0] for t in tests}
    missing = [i for i in need if i not in have]
    # covariant items must also carry a positive control
    cov = [it[0] for it in items if it[1] == 'DERIVED-COVARIANT']
    ctrl_missing = [i for i in cov if i not in have]
    return need, missing, cov, ctrl_missing


def run():
    items = ITEMS
    blasts = {it[0]: it[5] for it in items}
    errs = closure(items, PARENTS, blasts)
    need, missing, cov, ctrl_missing = coverage(items, TESTS)

    counts = {}
    for it in items:
        counts[it[1]] = counts.get(it[1], 0) + 1
    predicted = {'MEASURED': 2, 'DERIVED-COVARIANT': 3, 'DERIVED-COORD': 5,
                 'CONVENTION': 15, 'ASSUMPTION': 8, 'UNVERIFIED': 2}

    # negative controls on deep copies
    n1 = closure(items + [('AX-ZZ1', '', 'x', 'd', 'r', ['D8'])], PARENTS,
                 dict(blasts, **{'AX-ZZ1': ['D8']}))
    n1n = len([e for e in n1 if e[0] == 'unlabelled'])
    n2 = closure(items + [('AX-ZZ2', 'CONVENTION', 'x', 'd', 'r', ['NOT-A-TOKEN'])],
                 dict(PARENTS, **{'AX-ZZ2': ['EXT:x']}),
                 dict(blasts, **{'AX-ZZ2': ['NOT-A-TOKEN']}))
    n2n = len([e for e in n2 if e[0] == 'dangling-blast' and e[2] == 'NOT-A-TOKEN'])
    n3 = coverage(items + [('AX-ZZ3', 'DERIVED-COVARIANT', 'x', 'd', 'r', ['D8'])], TESTS)
    n3n = len([i for i in n3[3] if i == 'AX-ZZ3'])
    n4 = closure(items + [('AX-ZZ4', 'CONVENTION', 'x', 'd', 'r', ['D8'])],
                 dict(PARENTS, **{'AX-ZZ4': []}), dict(blasts, **{'AX-ZZ4': ['D8']}))
    n4n = len([e for e in n4 if e[0] == 'rootless' and e[1] == 'AX-ZZ4'])

    checks = [
        ('CK1', 'item count = 35 and labels equal the pre-registered distribution',
         len(items) == 35 and counts == predicted, '%d items' % len(items)),
        ('CK2', 'closure: %d error(s)' % len(errs), len(errs) == 0, ', '.join(map(str, errs[:4]))),
        ('CK3', 'test coverage: %d/%d test-requiring items; %d/%d covariant controls'
         % (len(need) - len(missing), len(need), len(cov) - len(ctrl_missing), len(cov)),
         not missing and not ctrl_missing, ','.join(missing + ctrl_missing)),
        ('CK4', 'd_parallel = %.5f fm = %.4e a0 (pred 15.40194, 2.911e-4)'
         % (D_PAR_FM, D_PAR_A0),
         abs(D_PAR_FM - 15.40194) < 0.5e-3 and abs(D_PAR_A0 / 2.911e-4 - 1) < 5e-3,
         ''),
        ('CK5', 'RL-6 ratios %.4e / %.4e / %.4e (pred 1.948e4 / 4.450e4 / 3.000e5)'
         % (R_154, R_674, R_1FM),
         all(abs(v / p - 1) < 5e-3 for v, p in
             [(R_154, 1.948e4), (R_674, 4.450e4), (R_1FM, 3.000e5)]), ''),
        ('CK6', 'Phi = %.5f (pred -4.50499); Q3 = %.5f (pred 8.37790); Q3(2C_eye) = %.5f'
         % (PHI_LOG, Q3, Q3_DBL),
         abs(PHI_LOG + 4.50499) < 1e-3 and abs(Q3 - 8.37790) < 1e-3
         and abs(Q3_DBL - 7.38223) < 1e-3, ''),
        ('CK7', 'dE_z(250 nm) = %.4f eV (pred 2.4797); gamma_flip = %.4f (pred 1.1021)'
         % (DEZ_250NM_EV, GAMMA_FLIP),
         abs(DEZ_250NM_EV - 2.4797) < 1e-3 and abs(GAMMA_FLIP - 1.1021) < 1e-3, ''),
        ('CK8', 'K^2 - K_ijK^ij simplifies to 0 for arbitrary f(t,x)',
         IDENT_D04 == 0, str(IDENT_D04)),
    ('CK9', 'extended control f=t+eps*x^2 gives K = %s' % K_EXT,
     sp.simplify(K_EXT - K_EXT_TARGET) == 0, str(sp.simplify(K_EXT - K_EXT_TARGET))),
    ('CK10', 'no file opened for writing during emission (procedural)', not WRITES,
     str(WRITES[:3])),
    ]
    negs = [
        ('N1', 'unlabelled item detected once', n1n == 1, str(n1n)),
        ('N2', 'dangling blast token detected once', n2n == 1, str(n2n)),
        ('N3', 'untested covariant item detected once', n3n == 1, str(n3n)),
        ('N4', 'rootless item detected once', n4n == 1, str(n4n)),
    ]
    return items, blasts, counts, predicted, checks, negs, errs


# ----------------------------------------------------------------- emission
def emit():
    items, blasts, counts, predicted, checks, negs, errs = run()
    reg_sha = sha256(REGISTRATION)

    a('=' * 78)
    a('AXIOM AUDIT AX-01')
    a('=' * 78)
    a('Date: %s' % datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'))
    a('Instrument: src/ax/ax01_axiom_audit.py')
    a('Pre-registration: runs/AX/ax01_axiom_audit_registration.md')
    a('  registration sha256   %s' % reg_sha)
    a('  frozen-at-registration %s' % ('MATCH' if reg_sha == REG_SHA_REGISTERED else 'CHANGED'))
    a('  PROVENANCE: NEITHER (structural audit; derives no physics, adjudicates no gate)')
    a('  scope: labels, derivation chains, coordinate tests, blast radii. No repair, no re-seal,')
    a('         no gate/threshold/terminal/D-state movement, no interpretation, no recommendation.')
    a('')
    a('  Label schema')
    a('    MEASURED          from experiment, model-independent')
    a('    DERIVED-COVARIANT derived; scalar/invariant')
    a('    DERIVED-COORD     derived; value/form depends on coordinates or gauge')
    a('    CONVENTION        fixed by fiat inside the programme')
    a('    ASSUMPTION        used as a premise, never justified or derived')
    a('    UNVERIFIED        claimed true; no derivation, measurement or citation on file')
    a('')
    a('-' * 78)
    a('SECTION A: ITEM INVENTORY')
    a('-' * 78)
    for it in items:
        a('%-8s %-17s %-46s' % (it[0], it[1], it[2]))
        a('         %s' % it[3])
        a('         root: %s' % it[4])
    a('')

    a('-' * 78)
    a('SECTION B: DERIVATION CHAINS')
    a('-' * 78)
    for n, it in enumerate(items, 1):
        a('[B-%03d] %s -> %s' % (n, it[0], ', '.join(PARENTS[it[0]])))
    a('')
    a('  Recurrence is resolved: every parent that is itself an audited item appears in this table')
    a('  as its own row, so the chains close at EXT: roots only.')
    a('')

    a('-' * 78)
    a('SECTION C: COORDINATE-DEPENDENCE TESTS')
    a('-' * 78)
    for n, (iid, tr, sv, note) in enumerate(TESTS, 1):
        a('[C-%03d] %s  survives: %-13s %s' % (n, iid, sv, tr))
        a('         %s' % note)
    a('')

    a('-' * 78)
    a('SECTION D: BLAST RADIUS MAP')
    a('-' * 78)
    for n, it in enumerate(items, 1):
        a('[D-%03d] %s -> affects: %s' % (n, it[0], ', '.join(it[5])))
    a('')
    a('  Closure: each target is either an audited id or a registered downstream token. Tokens')
    a('  denote recorded artefacts, not audited premises; their own status is unchanged here.')
    a('')

    a('-' * 78)
    a('SECTION E: SUMMARY STATISTICS')
    a('-' * 78)
    a('Total items audited: %d' % len(items))
    for k in ('MEASURED', 'DERIVED-COVARIANT', 'DERIVED-COORD', 'CONVENTION',
              'ASSUMPTION', 'UNVERIFIED'):
        a('%-17s : %2d   (predicted %2d)' % (k, counts.get(k, 0), predicted[k]))
    a('')
    a('no_test_possible  : %d   (C-row with an explicit justification, directive 7)'
      % len([t for t in TESTS if t[2].startswith('N/A')]))
    a('test_rows         : %d   (%d test-requiring + %d covariant controls)'
      % (len(TESTS), len(TESTS) - 3, 3))
    a('closure_errors    : %d' % len(errs))
    a('')

    a('-' * 78)
    a('SECTION F: CRITICAL FINDINGS')
    a('-' * 78)
    for n, (sev, txt) in enumerate(FINDINGS, 1):
        a('[F-%03d] [%s] %s' % (n, sev, txt))
        a('')
    hi = len([f for f in FINDINGS if f[0] == 'HIGH'])
    me = len([f for f in FINDINGS if f[0] == 'MEDIUM'])
    lo = len([f for f in FINDINGS if f[0] == 'LOW'])
    a('  Counts: HIGH %d, MEDIUM %d, LOW %d' % (hi, me, lo))
    a('  These are descriptions of dependency, not assessments of the programme. No finding')
    a('  changes a gate, threshold, terminal class, price or queue state.')
    a('')

    a('=' * 78)
    a('[SELF-TESTS]')
    a('=' * 78)
    okc = 0
    for cid, what, passed, extra in checks:
        a('  %-6s %-58s %s' % (cid, what[:58], 'PASS' if passed else 'FAIL'))
        if extra:
            a('         %s' % extra)
        okc += bool(passed)
    a('  %-6s %-58s %s' % ('IDENT', 'label counts sum to the item count (partition, not evidence)',
                           'PASS' if sum(counts.values()) == len(items) else 'FAIL'))
    okn = 0
    for cid, what, passed, extra in negs:
        a('  %-6s %-58s %s' % ('NEGCTRL-' + cid, what[:51], 'PASS' if passed else 'FAIL'))
        okn += bool(passed)
    a('')

    a('=' * 78)
    a('[VERDICTS]')
    a('=' * 78)
    a('  CHECK    %d/%d' % (okc, len(checks)))
    a('  IDENT    1/1  (partition identity, not evidence)')
    a('  NEGCTRL  %d/%d' % (okn, len(negs)))
    a('  Findings: HIGH %d / MEDIUM %d / LOW %d' % (hi, me, lo))
    a('  No prior MET or PASS was accepted as evidence of DERIVED-COVARIANT: each covariant item')
    a('  carries its own C-row, and IDENT labels were counted separately throughout.')
    ok = okc == len(checks) and okn == len(negs) and not errs
    a('  OVERALL: %s' % ('PASS-WITH-FINDINGS' if ok else 'FAIL'))
    a('  evidence level: STRUCTURAL AUDIT / NOT GATE EVIDENCE')
    a('  PROVENANCE: NEITHER')
    a('')
    a('Content generated by AI')
    return '\n'.join(A) + '\n', ok


def main():
    text, ok = emit()
    if '--write' in sys.argv:
        os.makedirs(os.path.dirname(PRODUCT), exist_ok=True)
        WRITES.append(PRODUCT)
        with open(PRODUCT, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        print('wrote %s  (%d bytes)' % (os.path.relpath(PRODUCT, ROOT), len(text)))
        print('overall', 'PASS-WITH-FINDINGS' if ok else 'FAIL')
    else:
        sys.stdout.write(text)
        print('DRY RUN - nothing written; overall', 'PASS-WITH-FINDINGS' if ok else 'FAIL')


if __name__ == '__main__':
    main()
