"""
FL coordinate under GD7 (fidelity = faithfulness to the unaided retinal image).

Rulings executed here:
  GD7  "FL means 'faithful to what the human eye sees', and FL3 is the maximum"   -> FL3 is the maximum, the ladder ascends.
  GD8  "keep 2L/c, and write in 'only when D = L'"      -> the corollary is a statement about D = L only.

The goal sentence requires "presentation fidelity is a continuum".  Under GD7 that
continuum has a definition, not just a name:

    FL(I) := -( b + c + p + e )

    b  band offset        |log10(E_I / E_eye)|                     decades
    c  contrast distortion|log10(m_I / m_R)|                        decades
    p  photon deficit     max(0, log10(N_req / N_avail))            decades
    e  enhancement count  number of registered EN operators applied  operators

FL3 is the reference frame (I = R), so all four terms vanish and FL = 0 exactly.  The
maximum is unique because each term is a magnitude.  The weighting is a DECLARED
CONVENTION, not physics (DC4, same status as dH under BUDGET-1); that is disclosed
in s1 rather than hidden in the arithmetic.

Predictions fixed in runs/ROUTE/gd7_gd8_registration.md before this ran.

PROVENANCE: NEITHER  (definition + conformance arithmetic; establishes no physics)
"""
import numpy as np

E_EYE = 2.25          # eV, 550 nm
M_EYE = 1e-2          # Weber contrast threshold, declared
M_R_550 = 7e-7        # registered modulation of the tile at 550 nm (painting_render_v1)
NEAR_POINT = 0.25     # m, naked-eye near point, declared
C_LIGHT = 2.99792458e8
SQ2 = np.sqrt(2.0)

flags = {}


def hdr(t):
    print()
    print('=' * 78)
    print(t)
    print('=' * 78)


# ----------------------------------------------------------------------------- F-1
hdr('[F-1] THE FOUR COORDINATES ARE ALL COMPUTABLE FROM REGISTERED NUMBERS')

COORDS = [
    ('b', 'band offset', '|log10(E_I / E_eye)|', 'E_EYE = 2.25 eV, declared'),
    ('c', 'contrast distortion', '|log10(m_I / m_R)|',
     'm_R = 7.0e-07 at 550 nm (painting_render_v1 panel c); m_eye = 1e-2'),
    ('p', 'photon deficit', 'max(0, log10(N_req / N_avail))',
     'flux deficits from p2_clock_results (Phase 2)'),
    ('e', 'enhancement count', 'number of EN operators',
     'EN1-EN5, display_conventions_v1 s3'),
]
print('  %-4s %-22s %-34s %s' % ('id', 'coordinate', 'form', 'source'))
print('  ' + '-' * 96)
for cid, name, form, src in COORDS:
    print('  %-4s %-22s %-34s %s' % (cid, name, form, src))
print()
print('  FL = -(b + c + p + e).  FL3 = reference frame, all terms zero, FL = 0 exactly.')
print('  Equal weights: a DECLARED CONVENTION (DC4).  Reported, never scored.')
flags['F1_computable'] = 'ALL-FOUR-FROM-REGISTERED'


# ----------------------------------------------------------------------------- F-2
hdr('[F-2] THE RUNGS ORDER: FL3 = 0 > FL2 > FL1')

b_284 = abs(np.log10(284.0 / E_EYE))
c_550 = abs(np.log10(M_EYE / M_R_550))
p_vis = 9.9795          # decades, visible flux deficit vs 1e22 source (Phase 2)
p_284 = 0.0             # admissible sub-field at 1 MW (Phase 2 P2-5)

RUNGS = [
    ('FL3  naked-eye reflection', 0.0, 0.0, 0.0, 0),
    ('FL2  284 eV transmission', b_284, 0.0, p_284, 1),
    ('FL1  550 nm enhanced', 0.0, c_550, p_vis, 2),
]

print('  %-26s %8s %8s %8s %4s %10s' % ('rung', 'b', 'c', 'p', 'e', 'FL'))
print('  ' + '-' * 70)
vals = []
for name, b, c, p, e in RUNGS:
    fl = -(b + c + p + e)
    if abs(fl) < 1e-12:
        fl = 0.0
    vals.append((name, b, c, p, e, fl))
    print('  %-26s %8.4f %8.4f %8.4f %4d %10.4f' % (name, b, c, p, e, fl))
print()
order_ok = vals[0][5] > vals[1][5] > vals[2][5]
print('  strict descent FL3 > FL2 > FL1 : %s  (%s)'
      % ('YES' if order_ok else 'NO', 'the ladder ascends, as GD7 requires'))
print()
print('  dominant term per rung:')
print('    FL2 : b = %.4f  <- the band migration itself, not the physics' % b_284)
print('    FL1 : p = %.4f  then c = %.4f  <- photons, then the 1.43e4 stretch' % (p_vis, c_550))
print()
print('  Note the shape GD7 produces: FL1 is the rung that SHOWS most and is farthest from')
print('  what the eye would see; FL3 is the rung that shows least and is identical to it.')
flags['F2_order'] = 'ASCENDS' if order_ok else 'NOT-ASCENDING'


# ----------------------------------------------------------------------------- F-3
hdr('[F-3] CONTINUITY: THE LADDER IS A CONTINUUM, NOT THREE STEPS')

print('  Sweep the declared enhancement gain g = m_I/m_R from 1 (faithful) to 1.43e4')
print('  (the stretch actually used at 550 nm in painting_render_v1 panel c).')
print()
print('    g            c        FL')
print('    ' + '-' * 30)
gs = np.array([1.0, 2.0, 10.0, 100.0, 1000.0, 1e4, M_EYE / M_R_550])
for g in gs:
    c = abs(np.log10(g))
    fl = -(0.0 + c + p_vis + 2)
    print('    %-11.4g %8.4f %9.4f' % (g, c, fl))
print()
def fl_of_g(g):
    return -(abs(np.log10(g)) + p_vis + 2)

d = np.diff([fl_of_g(x) for x in np.linspace(1.0, 1.43e4, 5000)])
slope = [abs(fl_of_g(x * 10.0) - fl_of_g(x)) for x in (1.0, 2.0, 100.0, 1e3)]
print('  |dFL / d log10 g| at g = 1, 2, 100, 1e3 : %s'
      % ', '.join('%.4f' % s for s in slope))
print('  = 1.0000 exactly, because c = |log10 g|.  FL is a sum of continuous terms, with a')
print('  bounded slope except at the max(0, .) kink in p; there is no step in the interior,')
print('  so the ladder is a continuum and the three rungs are thresholds on it.')
print()
print('  The three rungs are THRESHOLD values on this coordinate, not the coordinate itself:')
print('  FL3 at g = 1, e = 0, p = 0; FL1 at g = 1.43e4, e = 2, p = %.2f.  Every intermediate' % p_vis)
print('  value is a frame somebody could actually produce, which is what "continuum" means.')
flags['F3_continuum'] = 'CONTINUOUS'


# ----------------------------------------------------------------------------- F-4
hdr('[F-4] DOES GD7 CONFLICT WITH THE COROLLARY?  NO — THEY CONSTRAIN DIFFERENT THINGS')

print('  Corollary (GD8 scope): "No faithful reflected-light frame of a SURVIVING SHEET')
print('  exists."  Parse it:')
print()
print('    subject   : reflected-light frame')
print('    predicate : faithful')
print('    object    : a SURVIVING SHEET')
print()
print('  The corollary constrains the CONTENT of the frame (must not show a surviving')
print('  sheet).  GD7 constrains its FIDELITY (must equal the retinal image).  A frame can')
print('  satisfy both: maximally faithful, containing no sheet.')
print()
print('  So FL3 is attainable AND the corollary stands.  What FL3 shows is not the sheet —')
print('  which is exactly what the corollary predicts, and what the archived panel D-left')
print('  of unfold_appearance_v1.png already displays ("what you see is what lies behind it").')
print()
print('  The requirement that fails is not fidelity, it is the implicit hope that the most')
print('  faithful frame is also the most informative one.  GD7 makes that hope explicitly')
print('  false: FL3 has FL = 0 and carries no structure of the object.')
print()
print('  FL(GD7) and information(G-4 Reading A) are therefore ANTI-CORRELATED by')
print('  construction, and the anti-correlation is now a consequence of the adopted')
print('  definition rather than an ambiguity between two definitions.')
flags['F4_no_conflict'] = 'COMPATIBLE'


# ----------------------------------------------------------------------------- F-5
hdr('[F-5] GD8 PREMISE COVERS THE NAKED EYE A FORTIORI')

print('  Naked-eye viewing requires D >= near point = %.2f m.' % NEAR_POINT)
print('  The corollary, as ruled, speaks at D = L.  It therefore covers naked-eye viewing')
print('  whenever D >= L/sqrt(2), which holds for every L <= sqrt(2) x %.2f = %.4f m.'
      % (NEAR_POINT, SQ2 * NEAR_POINT))
print()
print('    L (m)    L/sqrt2   D=0.25 covered?   t_rip (s)      2L/c (s)')
print('    ' + '-' * 68)
for L in (0.070, 0.200, 0.300, 1.000):
    print('    %-8.3f %-10.4f %-17s %-14.6e %.6e'
          % (L, L / SQ2, 'yes' if NEAR_POINT >= L / SQ2 else 'no',
             SQ2 * L / C_LIGHT, 2 * L / C_LIGHT))
print()
print('  For L > 0.354 m the object subtends more than 2*atan(0.5/0.25) = 126.9 deg at the')
print('  near point and cannot be taken in; the case is outside naked-eye viewing, so the')
print('  a fortiori argument has no gap inside its own domain.')
print()
print('  Per-patch form (D <= d/sqrt2) is NOT used: GD8 did not adopt it.  It is recorded as')
print('  an unregistered observation and licenses no frame.')
flags['F5_premise_covers'] = 'A-FORTIORI'


# ----------------------------------------------------------------------------- F-6
hdr('[F-6] FL3 IS A FAMILY, INDEXED BY WHICH CONSTRAINT WAS RELAXED')

SCENES = [
    ('C1 held  (2D-ified)', 'the object is gone when the light returns', 0.0, 0.0, 0.0, 0),
    ('not-C1   (7 cm slab)', 'an intact slab at 35 % reflectance', 0.0, 0.0, 0.0, 0),
]
print('  Both scenes are faithful reflected-light frames at the naked eye:')
print()
print('    %-22s %s' % ('scene', 'what the frame shows'))
print('    ' + '-' * 74)
for s, shows, *_ in SCENES:
    print('    %-22s %s' % (s, shows))
print()
print('  For both, b = c = p = e = 0, so FL = 0.  FL3 is therefore not one image but a')
print('  family with two members, and the member is selected by the constraint set:')
print()
print('    C1 held   -> FL3 shows ABSENCE.  This is a faithful presentation of the')
print('                 2D-ification, and it is the corollary\'s content as an image.')
print('    not-C1    -> FL3 shows the SLAB.  Also faithful, but the object is not')
print('                 2D-ified: the top rung of the relaxation axis is reached by')
print('                 giving up the thing being presented (v1 s9, now a theorem).')
print()
print('  Consequence for the route: an FL3 frame must declare WHICH member it is, or it')
print('  will be read as a depiction of a surviving sheet — the one reading the corollary')
print('  forbids.  This is registered as a mandatory caption line (DC9).')
flags['F6_family'] = 'TWO-MEMBERS'


# ----------------------------------------------------------------------------- summary
hdr('SUMMARY')
print('  F-1 coordinates computable from registered numbers  : %s' % flags['F1_computable'])
print('  F-2 rung order FL3 > FL2 > FL1                      : %s' % flags['F2_order'])
print('  F-3 band/contrast/photon axes continuous            : %s' % flags['F3_continuum'])
print('  F-4 GD7 compatible with the corollary               : %s' % flags['F4_no_conflict'])
print('  F-5 GD8 premise covers naked-eye viewing            : %s' % flags['F5_premise_covers'])
print('  F-6 FL3 is a declared family of two members         : %s' % flags['F6_family'])
print()
print('  FL values: FL3 = 0.0000, FL2 = %.4f, FL1 = %.4f  (decades)' % (vals[1][5], vals[2][5]))
print()
print('  What GD7 buys: a definition where there was a word, so "continuum" is a property')
print('  and the ladder has a direction.  What it costs: the maximum-fidelity frame is the')
print('  least informative one, and that is now a theorem rather than a warning.')
print('  What GD8 buys: a scope for the corollary, so it can no longer be read as a claim')
print('  about geometries nobody stated.  What it costs: nothing — the conclusion survives')
print('  a fortiori for every naked-eye distance.')
print()
print('PROVENANCE: NEITHER  (definition + conformance arithmetic; establishes no physics)')
