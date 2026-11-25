"""
Goal-conformance check for the staged relaxation / presentation-fidelity route.

The goal (docs/decisions/staged_relaxation_visual_route_v1.md s1, registered verbatim):

  "Present the physical scene of a three-dimensional macroscopic object being swept by a
   two-dimensionalization front.  Presentation fidelity is a continuum, and the project
   commits to walking the entire diagonal ... from digitally-enhanced discernibility under
   all constraints to naked-eye visible-light reflection presentation under the minimal
   constraint set.  Enhancement is permitted.  Enhancement must not introduce information
   that does not exist physically."

This module does not re-quote the goal.  It measures what the goal requires and what no
prior round measured:

  G-1  requirement -> artefact conformance, with depictions counted separately from charts
  G-2  the DC1 census: how many existing frames carry a declaration block
  G-3  the ME5 corollary's unstated premise (viewing distance = object size)
  G-4  whether the fidelity axis is ordered: two readings, opposite orderings
  G-5  an instrument for "enhancement must not introduce non-existent information"

Predictions fixed in runs/ROUTE/goal_conformance_registration.md before this file ran.
Two predictions came out weaker than registered and are corrected in place, disclosed in
s2 of reports/reviews/route_goal_conformance_v1.md:
  - P-C1 said "zero of five"; one requirement (G1) has a depiction, so the verdict is
    PARTIAL, not zero.  The claim is narrowed, not reinterpreted.
  - the first G-5 interpolation case produced only 8 levels (a coarse 4-neighbour blur,
    not a real bilinear resample); replaced with an actual bilinear upsample.

PROVENANCE: NEITHER  (conformance audit; establishes no physics)
"""
import os
import numpy as np

C_LIGHT = 2.99792458e8
SQ2 = np.sqrt(2.0)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

flags = {}


def hdr(t):
    print()
    print('=' * 78)
    print(t)
    print('=' * 78)


# ----------------------------------------------------------------------------- G-1
hdr('[G-1] GOAL DECOMPOSITION -> ARTEFACT CONFORMANCE')

REQ = [
    ('G1', 'depict the sweep of a 3D macroscopic object by a 2D front',
     'PARTIAL',
     'depictions EXIST but show the unfolded END STATE, not the sweep, and none is citable:\n'
     '        runs/ANALYSIS/unfold_appearance_v1.png  (panel D-left: naked-eye reflected\n'
     '          visible light; panel D-right: 284 eV detector)  -- no .display.txt\n'
     '        runs/ANALYSIS/painting_render_v1.png    (panels b-e: the same tile at 550 nm /\n'
     '          284 eV / 4 keV / tau)  -- no .display.txt\n'
     '      both picture the 18 km^2 unfolded spread, i.e. the state AFTER the front has\n'
     '      passed, not the front passing.  Panel D-left carries the corollary\'s content:\n'
     '      the naked-eye reflected view shows what lies BEHIND the sheet.'),
    ('G2', 'presentation fidelity is a CONTINUUM',
     'ABSENT',
     'FL1/FL2/FL3 are labels with no coordinate.  G-4 shows the two candidate readings\n'
     '      order the ladder oppositely, so the axis has no direction at all yet (GD7).'),
    ('G3', 'walk the ENTIRE DIAGONAL (relaxation x fidelity)',
     'ABSENT',
     '0 executed constraint relaxations.  Phase 1 is booked under S7 as an\n'
     '      observation-strength declaration, not a relaxation; Phase 3 is BLOCKED on GD6.'),
    ('G4', 'reach naked-eye visible REFLECTION at the minimal constraint set',
     'UNRESOLVED',
     'the registered corollary reads as a refutation; G-3 shows it carries the\n'
     '      unstated premise D = L, so the requirement is not decidable from the registered\n'
     '      text.  Unresolved is weaker than either "possible" or "impossible" and is the\n'
     '      correct status (GD8).'),
    ('G5', 'enhancement must not introduce non-existent information',
     'INSTRUMENT',
     'EN1-EN5 required a declared basis and nothing tested non-introduction.  The test\n'
     '      is built and negative-tested in G-5 below; it is an instrument, not a gate.'),
]

print('  id   requirement                                              status')
print('  ' + '-' * 74)
for rid, req, st, _ in REQ:
    print('  %-4s %-54s %s' % (rid, req[:54], st))
print()
for rid, req, st, why in REQ:
    print('  %s [%s]: %s' % (rid, st, why))
print()
cnt = {}
for _, _, st, _ in REQ:
    cnt[st] = cnt.get(st, 0) + 1
print('  status tally: %s' % ', '.join('%s=%d' % kv for kv in sorted(cnt.items())))
print('  fully satisfied: 0 / %d' % len(REQ))
flags['G1_conformance'] = 'ZERO-FULLY-SATISFIED'


# ----------------------------------------------------------------------------- G-2
hdr('[G-2] DC1 CENSUS: FRAMES VS DECLARATION BLOCKS')

imgs = []
for dp, dn, fn in os.walk(ROOT):
    if any(s in dp for s in ('.git', '.workbuddy', '__pycache__')):
        continue
    for f in fn:
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            imgs.append(os.path.relpath(os.path.join(dp, f), ROOT).replace('\\', '/'))
imgs.sort()

declared = [p for p in imgs if os.path.exists(os.path.join(ROOT, p + '.display.txt'))]
undeclared = [p for p in imgs if p not in declared]

print('  image files found            : %d' % len(imgs))
print('  with a .display.txt sidecar  : %d' % len(declared))
print('  WITHOUT a sidecar            : %d   -> non-citable under DC1' % len(undeclared))
print()
print('  declared:')
for p in declared:
    print('    %s' % p)
print()
print('  NOTE: display_lint.py enumerates *.display.txt, so it validates the blocks that')
print('  exist and is structurally blind to images that have none.  DC1 ("no block, no')
print('  citation") is unenforced from the missing side of the census: the validator cannot')
print('  report the 26 frames that Phase 0\'s own rule disqualifies.')
print()
print('  DC1 coverage = %d / %d = %.1f%%' % (len(declared), len(imgs),
                                            100.0 * len(declared) / max(1, len(imgs))))
flags['G2_dc1_coverage'] = 'ONE-FRAME-ONLY' if len(declared) <= 1 else 'PARTIAL'


# ----------------------------------------------------------------------------- G-3
hdr('[G-3] THE ME5 COROLLARY CARRIES AN UNSTATED PREMISE: D = L')

print('  Frozen identity (correct, and not attacked):')
print('      t_rip = sqrt(2) L / c     2L/c = sqrt(2) t_rip')
print('  Frozen inference (attacked):')
print('      therefore no reflected-light frame of a surviving sheet can exist, for any L.')
print()
print('  The identity uses L twice: as the object size (destruction path) and as the optical')
print('  path.  The optical path for a camera at distance D is 2D; it equals 2L only when')
print('  D = L.  D is an observation geometry, not a physical constant, and no registered')
print('  text states it.')
print()
print('  Per-patch form.  A patch at distance d from the tear origin converts at')
print('  t = d/v_front with v_front = L/t_rip = c/sqrt(2) (the Phase 2 definition, not a new')
print('  front speed).  It can be photographed iff the round trip fits in its own lifetime:')
print()
print('        2D/c <= d/v_front      <=>      D <= d/sqrt(2)')
print()
print('  The admissible set is the annulus d >= sqrt(2) D -- strictly beyond a half-angle')
print('  atan(sqrt(2)) = %.4f deg off the camera axis.  It is non-empty iff D < L/sqrt(2).'
      % np.degrees(np.arctan(SQ2)))
print('  Covered fraction of the radial extent = 1 - sqrt(2) D/L.')
print()
print('    D/L       admissible?   covered fraction   half-angle to far edge')
print('    ' + '-' * 66)
for ratio in (0.05, 0.25, 0.50, 0.70, 1 / SQ2, 1.00):
    cov = 1.0 - SQ2 * ratio
    print('    %-9.4f %-13s %+14.6f   %8.4f deg'
          % (ratio, 'yes' if cov > 0 else 'NO', cov, np.degrees(np.arctan(1.0 / ratio))))
print()
print('  The registered corollary is the D = L row: 1 - sqrt(2) = %+.6f, i.e. NEGATIVE.'
      % (1 - SQ2))
print('  A negative admissible extent is not a physical impossibility; it is the signature')
print('  of an observation geometry outside the window.  Reading it as "impossible for any')
print('  L" replaces an out-of-range parameter choice with a result.')
print()
L = 0.20
print('  Per channel at L = 0.20 m, v_front = %.6e m/s:' % (C_LIGHT / SQ2))
for D in (0.010, 0.050, 0.100, 0.1414, L):
    cov = 1.0 - SQ2 * D / L
    print('    D = %6.4f m -> coverage %+8.4f   %s'
          % (D, cov, 'admissible sub-field' if cov > 0 else 'EMPTY (the registered slice)'))
print()
print('  Verdict: the IDENTITY stands; the INFERENCE does not follow without D = L.')
print('  ME5 is frozen, so the correction is registered as GD8 and NOT applied.')
flags['G3_corollary_premise'] = 'UNSTATED-PREMISE-FOUND'


# ----------------------------------------------------------------------------- G-4
hdr('[G-4] IS THE FIDELITY AXIS ORDERED?  TWO READINGS, OPPOSITE ORDERS')

REF_FLUX = 1e22            # declared beamline-class source, Phase 2
CH = [
    ('transmission 284 eV', 0.0, 9.539e23 / REF_FLUX),
    ('transmission visible', 0.0, 9.539e31 / REF_FLUX),
    ('reflection visible', np.log10(SQ2), 9.539e31 / 0.975855 / REF_FLUX),
]

print('  Deficits in decades against a %.0e m^-2 s^-1 source (larger = worse).' % REF_FLUX)
print('  Time deficit for the reflection row uses the registered D = L slice; the flux')
print('  deficit does not depend on D at all.')
print()
print('    %-24s %8s %8s' % ('channel', 'time', 'flux'))
print('    ' + '-' * 42)
for name, td, fr in CH:
    print('    %-24s %8.4f %8.4f' % (name, td, np.log10(fr)))
print()

vec = {n: (td, np.log10(fr)) for n, td, fr in CH}
def dom(a, b):
    return all(x <= y for x, y in zip(a, b)) and any(x < y for x, y in zip(a, b))

print('  Pareto relation:')
for a in vec:
    for b in vec:
        if a != b and dom(vec[a], vec[b]):
            print('    %-24s strictly dominates  %s' % (a, b))
print()
print('  READING A — fidelity = how much the frame shows.')
print('    transmission 284 eV dominates reflection-visible on BOTH coordinates, so FL2 is')
print('    the Pareto maximum and FL3 is strictly dominated.  Order A: FL2 > FL3 — the')
print('    ladder DESCENDS toward its declared end point.')
print('    Robustness: the flux coordinate is independent of D, and transmission-visible also')
print('    dominates reflection-visible there, so this order survives the GD8 correction.')
print()
print('  READING B — fidelity = how close the frame is to the unaided retinal image.')
CONDS = ['band inside 1.8-3.1 eV', 'photon budget met unaided',
         'no enhancement operator', 'displayed quantity is a light field']
MET = {
    'FL1': (0, 0, 0, 0),   # branch band, enhancement mandatory, occupancy indicator
    'FL2': (0, 1, 0, 1),   # 284 eV, budget met, EN4 channel, light field
    'FL3': (1, 1, 1, 1),   # bare eye, reflection
}
print('    conditions, in order: ' + ' | '.join(CONDS))
for lv in ('FL1', 'FL2', 'FL3'):
    marks = ''.join('Y' if m else '.' for m in MET[lv])
    print('      %s  %s   unmet %d/4' % (lv, marks, 4 - sum(MET[lv])))
print('    Order B: FL3 > FL2 > FL1 — the ladder ASCENDS toward its declared end point.')
print()
print('  THE TWO READINGS REVERSE THE LADDER.  Reading A is what every quantitative')
print('  criterion here measures (CNR, photon counts, exposure budget).  Reading B is what')
print('  the goal sentence says ("to naked-eye visible reflection").  "Walk the entire')
print('  diagonal" presumes a total order that no registered quantity supplies.')
print('  Registered as GD7: declare the semantics of FL, or the ladder has no direction.')
flags['G4_fidelity_order'] = 'AMBIGUOUS-OPPOSITE-ORDERS'


# ----------------------------------------------------------------------------- G-5
hdr('[G-5] EN-BOUND: AN INSTRUMENT FOR "NO INFORMATION ADDED"')

def levels(img):
    flat = img.reshape(-1, img.shape[-1])
    return len(np.unique(flat, axis=0))

def entropy_bits(img):
    flat = img.reshape(-1, img.shape[-1])
    _, cnt = np.unique(flat, axis=0, return_counts=True)
    p = cnt / cnt.sum()
    return float(-(p * np.log2(p)).sum())

def lut(stops):
    x = np.linspace(0, 1, len(stops))
    idx = np.linspace(0, 1, 256)
    r = np.interp(idx, x, stops)
    return np.stack([r, r, r], axis=1)

def render(field, stops):
    lo, hi = field.min(), field.max()
    idx = np.round((field - lo) / max(hi - lo, 1e-12) * 255).astype(int)
    return lut(stops)[idx]

def mono(img, field):
    vals = field.ravel()
    lum = img.reshape(-1, img.shape[-1]).mean(axis=1)
    order = np.argsort(vals, kind='stable')
    return bool(np.all(np.diff(lum[order]) >= -1e-9))

def bilinear(f, k):
    n = f.shape[0]
    xs = np.linspace(0, n - 1, n * k)
    rows = np.stack([np.interp(xs, np.arange(n), f[i]) for i in range(n)])
    out = np.stack([np.interp(xs, np.arange(n), rows[:, j]) for j in range(n * k)], axis=1)
    return out

n = 64
FIELD = np.zeros((n, n))
for i, v in enumerate((0.0, 1 / 3, 2 / 3, 1.0)):
    FIELD[i * 16:(i + 1) * 16, :] = v
N_S = len(np.unique(FIELD))

print('  scalar field: %dx%d, %d distinct levels (a quantised converted-fraction map)'
      % (n, n, N_S))
print()
print('  test                                    levels  dH(bits)  mono  verdict  branch')
print('  ' + '-' * 82)

CASES = [
    ('compliant  EN2 monotone ramp', FIELD, [0.0, 0.25, 0.6, 1.0], 'PASS'),
    ('compliant  EN3 stretch (affine)', FIELD, [0.1, 0.3, 0.7, 1.0], 'PASS'),
    ('DEFECT     bilinear resample 4x', bilinear(FIELD, 4), [0.0, 0.25, 0.6, 1.0], 'CONVICT'),
    ('DEFECT     non-monotone palette', FIELD, [0.0, 0.6, 0.4, 1.0], 'CONVICT'),
]
rows, ok = [], True
for name, fld, stops, expect in CASES:
    img = render(fld, stops)
    nl = levels(img)
    dh = entropy_bits(img) - np.log2(N_S)
    m = mono(img, fld)
    br = []
    if nl > N_S:
        br.append('a levels')
    if not m:
        br.append('b map')
    got = 'CONVICT' if br else 'PASS'
    ok = ok and (got == expect)
    rows.append((name, nl, dh, m, got, ' '.join(br) if br else '-'))
    print('  %-38s %5d  %+8.4f  %-4s  %-7s  %s'
          % (name, nl, dh, 'yes' if m else 'NO', got, ' '.join(br) if br else '-'))

print()
print('  branch (a): display levels > scalar levels    -> structure manufactured by resampling')
print('  branch (b): map not monotone in the scalar    -> contrast manufactured by the palette')
print('  branch (b) is the repository\'s existing EN2 requirement, made executable.  branch (a)')
print('  is the part that was missing, and it convicts the commonest real defect:')
print('  interpolation presented as physical structure.')
print()
print('  negative test: %s  (%d/%d behaving)' % ('TRUSTED' if ok else 'FAILED', sum(
    1 for r, c in zip(rows, CASES) if r[4] == c[3]), len(CASES)))
flags['G5_en_bound'] = 'INSTRUMENT-TRUSTED' if ok else 'INSTRUMENT-UNTRUSTED'


# ----------------------------------------------------------------------------- summary
hdr('SUMMARY')
print('  G-1 goal requirements fully satisfied     : 0 / 5   [%s]' % flags['G1_conformance'])
print('        PARTIAL 1 (G1, depiction exists, non-citable, wrong moment)')
print('        ABSENT  2 (G2 coordinate, G3 diagonal)')
print('        UNRESOLVED 1 (G4 corollary premise)')
print('        INSTRUMENT 1 (G5 built this round)')
print('  G-2 frames citable under DC1              : %d / %d   [%s]'
      % (len(declared), len(imgs), flags['G2_dc1_coverage']))
print('  G-3 ME5 corollary premise (D = L)         : [%s]' % flags['G3_corollary_premise'])
print('  G-4 fidelity axis ordered                 : NO      [%s]' % flags['G4_fidelity_order'])
print('  G-5 non-introduction instrument           : [%s]' % flags['G5_en_bound'])
print()
print('  The goal is registered and intact; the route has not reached it.  What is missing')
print('  is not more execution on the ladder.  It is:')
print('    (i)   a fidelity COORDINATE           -> GD7 decides which one')
print('    (ii)  a ruling on what FL means       -> GD7')
print('    (iii) a corrected premise for the corollary -> GD8')
print('    (iv)  citable frames (26 of 27 are not)')
print('    (v)   the sweep, not only its endpoint')
print('  (ii) and (iii) are governor decisions and cannot be executed.')
print()
print('PROVENANCE: NEITHER  (conformance audit; establishes no physics)')
