CONSTRAINT RELAXATION RECORD — RR-DT-01
========================================
Date: 2026-11-24T03:52:00Z
Authority: governor directive G-71-01 §3.2
Pre-registration: runs/RR-DT/rr_dt_01_record_repair_registration.md
Instrument: src/rr_dt/rr_dt_01_record_repair.py
PROVENANCE: NEITHER (arithmetic on archived constants; no new physics derived)
Result class: RELAXATION LOG. No survival, visibility, gate, price or route claim.

Track A baseline (state before relaxation)
------------------------------------------
Adiabaticity is carried as WORKING-HYPOTHESIS, not as a proved premise and not as a blocking
prerequisite. Under it the smooth 2D-ization branch proceeds and any step that needs it cites
"[WORKING-HYPOTHESIS: adiabaticity; see RR-DT-01 §3.1]". The baseline numbers the ladder relaxes
from are the archived ones, unchanged:

  L_z               1.0 fm (density-inferred normalisation)
  d_parallel        15.40194 fm (in-plane column pitch, N_s^-1/2)
  atomic spacing    0.3 nm
  RL-6 price        2e4 x atomic spacing (printed); 1.94805e4 exact; 3.000e5 if L_z is used
                    as the independent thickness
  E_F (frozen)      73.37 MeV;  dE_z(1 fm) = pi*hbar*c/L_z = 619.921 MeV
  Phi               -4.505 orders at C = 3.3166 in a named E/G
  adiabaticity      1.92e4x before t_rip (thickness), 2.18e4x after (in-plane), ratio 4.19e8
  G0' row 1         NO-GO, basis d_parallel = 15.40 fm = 2.91e-4 a0 (conditional form, rr-dt 1.2)

The ladder below relaxes one premise at a time, in order, cumulatively. "Cumulative" matters: a
level is evaluated with every earlier relaxation still switched on. No level is skipped. Each level
re-evaluates the three objects G-71-01 names: the RL-6 price, the G0' clause status, and the
effective-2D criterion.

The boundary test was fixed before the run (registration §4): a level is HARD-SCI-FI-LIMIT when the
relaxed premise, together with something the record already asserts, yields A and not-A about the
same object at the same time. Weakening a claim is not a contradiction. Making a criterion false is
not a contradiction. Costing more is not a contradiction.

------------------------------------------------------------------------------
B1 — Lambda != 0
------------------------------------------------------------------------------
  - Relaxed: the undeclared cosmological term. Phase 1's constraint equations were solved with
    Lambda = 0 and never said so (AX-01 AX-D05).
  - Degree: quantified against the observed value. Lambda_obs = 3H0^2/c^2 = 1.5926e-52 m^-2 =
    1.5926e-82 fm^-2 at H0 = 67.4 km/s/Mpc, i.e. rho_Lambda = 7.669e-10 J/m^3 = 3.2e-44 of the
    nuclear energy density. The constraint picks up Lambda additively:
        kappa*rho_req = -f_xx/f + Lambda
    so the printed form is the Lambda -> 0 slice, and the size of the omission is set by
    Lambda/(f_xx/f). For any curvature the programme actually uses (|f_xx/f| >= 1e-3 fm^-2 in
    AX-01's own sensitivity probe) the cosmological value is 78.8 orders below the probe's scale.
  - Self-consistent: YES. A Lambda term is a constant in the Hamiltonian constraint and drops out of
    the momentum constraint identically (AX-01 C-010), so no equation is violated and no solution
    is lost. Nothing in the record is asserted with a precision that could detect it.
  - Hard boundary reached: NO.
  - Notes: the relaxation is real but numerically inert. What it corrects is a *declaration*, not a
    number: from here the constraint must be written with Lambda and specialised afterwards. RL-6:
    unchanged (a ratio of lengths; Lambda enters no length). G0' row 1: unchanged (d_parallel is
    independent of Lambda). Effective-2D criterion: unchanged, since dE_z = pi*hbar*c/L_z has no
    Lambda dependence and E_F is fixed by the areal density.

------------------------------------------------------------------------------
B2 — T != 0
------------------------------------------------------------------------------
  - Relaxed: the frozen state's T = 0 (AX-01 AX-G10). The Fermi sea is now allowed to be warm.
  - Degree: at kT = 1 MeV, kT/E_F = 1.36% at the frozen baseline (E_F = 73.373 MeV) and 16.1% at
    the ALL2D endpoint (E_F = 6.2221 MeV). The chemical potential shifts by
    (pi^2/12)(kT)^2/E_F = 0.0112 MeV and 0.1322 MeV respectively. The 2D ultra-relativistic sound
    speed c_s = c/sqrt(2) = 2.1199e8 m/s is set by the density, not by T, in the degenerate limit,
    so the two settling timescales of the unfolding record are unchanged: 4.30e-13 s and 1.80e-4 s,
    ratio 4.19e8.
  - Self-consistent: YES. The archived row 7 margin at the ALL2D endpoint is 0.342 MeV (E1 erratum),
    which is smaller than kT at 1 MeV -- so the row's endpoint comparison becomes T-conditional
    rather than false. A conditional statement is not a contradiction.
  - Hard boundary reached: NO.
  - Notes: what B2 does NOT do is make the branch adiabatic. The timescale ratio is unchanged, so
    temperature is not the missing knob, and Track A's hypothesis is neither supported nor
    undermined by it. RL-6: unchanged. G0' row 1: unchanged. G0' row 7: the endpoint comparison
    acquires a T-condition (recorded, not acted on -- row 7 is a deferred-adjacent MEDIUM subject
    under AX-01 F-008's sibling F-005..F-010 list and is not edited this round). Effective-2D:
    E_occ = max(E_F, kT) - at L_z = 1 fm, dE_z = 619.921 MeV, so kT = 1 MeV leaves the internal slot
    true; at the external-bound edge L_z = 250 nm, dE_z = 2.4797 eV and the slot was already false
    at T = 0 (E_F = 6.22 MeV >> 2.48 eV), so temperature adds no new failure mode.

------------------------------------------------------------------------------
B3 — L_z is not an external control parameter
------------------------------------------------------------------------------
  - Relaxed: the assumption that L_z can be held fixed from outside with no back-reaction (AX-01
    AX-S03). L_z is now allowed to couple to the matter it contains.
  - Degree: two numbers, both from constants already on file.
    (i) The object's own 2D degeneracy pressure is P_2D = 8.6227e16 N/m (G0' §2). If nothing holds
        it, the sheet's areal mass Sigma = 70 kg/m^2 accelerates at P/Sigma = 1.232e15 m/s^2, and
        over t_rip = 8.2553e-9 s the thickness grows by 0.5*a*t^2 = 4.20e-2 m. L_z is therefore not
        a parameter that survives one conversion time unless a confining stress of order P_2D acts.
    (ii) Read the other way -- what stress does a *relief* L_z(x) need? Phase 1's own solution
        answers it: kappa*rho_req = -f_xx/f. For f = L_z(1 + eps cos kx) with the measured
        eps = 1.7e-4 at a 1 mm relief wavelength, k^2*eps = 6.711e3 m^-2, and
        rho_req = (c^4/8*pi*G)(k^2*eps) = 3.232e46 J/m^3 = 2.02e14 MeV/fm^3 = 1.3e12 of the nuclear
        energy density. At a 1 m relief wavelength the same formula gives 1.3e6 nuclear densities.
        The sign alternates with cos kx: crests need positive rho, troughs need negative rho of the
        same order.
  - Self-consistent: YES. Nothing is contradicted; what happens is that L_z stops being an input
    and becomes an output, and the constraint supplies the stress that sets it. That stress is not
    assigned to any field in the record (Phase 1's own NOT-a-joint-solution caveat), which is a gap
    in the model, not an inconsistency in the algebra.
  - Hard boundary reached: NO.
  - Notes: this level is where the ladder stops being free. The relief branch of RL-2 is not
    expensive in optics (eps = 1.7e-4); it is expensive in stress, and half of that stress is
    negative. RL-6: unchanged as a ratio of lengths, but its denominator is now an output, so the
    price is a *measured* ratio only after the confinement branch is chosen. G0' row 1: unchanged;
    its basis d_parallel is an in-plane quantity and does not depend on what holds L_z. Effective-2D:
    the criterion's L_z is now a dynamical variable, so the conditional can no longer be evaluated
    from the deposition alone -- it must be evaluated at the realised thickness, which at B3's
    unconfined estimate is 4.2 cm and fails both slots. Effective 2D therefore survives B3 only on
    the confined branch, i.e. it inherits R1/K2 rather than the map.

------------------------------------------------------------------------------
B4 — adiabaticity is relaxed
------------------------------------------------------------------------------
  - Relaxed: Track A's WORKING-HYPOTHESIS itself. Non-adiabatic transitions in the z direction are
    allowed; the conversion need not be quasi-static.
  - Degree: qualitative in the record's own terms, and already priced. Dropping S moves the object
    from the {E,S,W} corner to {E,not-S,W}, which is the third row of the assumption matrix: "1 fm
    disintegration -> thermalization in meter-scale gas column", 41.2 Mt fireball, 99x the solar
    surface brightness, 1-10 s of colour. The archived exclusivity (scifi_boundary §4: W requires a
    non-equilibrium frozen transient, S requires reversible quasi-static behaviour, W6 carries
    0.56x the degeneracy energy away as neutrinos) says the two cannot hold together, so the
    relaxation does not create a new branch -- it selects the branch the record already contains.
  - Self-consistent: YES, and more comfortably than Track A: B4 is the branch in which the record's
    own exclusivity argument is satisfied rather than assumed away.
  - Hard boundary reached: NO.
  - Notes: does the system still reach effective 2D? Transiently and then not at all -- the 1 fm
    sheet exists at t_rip and thermalises into a metre-scale column, so E holds at the instant of
    conversion and the object that survives is 3D. That is the fireball, and it is what "abandoning
    smoothness" was always priced at. RL-6: unchanged. G0' row 1: unchanged (it is a statement about
    atoms at fixed area, and the fireball does not restore them). Effective-2D: the internal slot is
    evaluated on a state that no longer has a well-defined L_z, so the criterion is not false but
    inapplicable -- the referent is gone, which is the same failure mode N7 records for carriers.
    Track A is retained as the ideal limit (registration §4; unfolding record §12).

------------------------------------------------------------------------------
B5 — d_parallel is decoupled from the thickness
------------------------------------------------------------------------------
  - Relaxed: the identification that made RL-6's denominator the in-plane pitch (AX-01 HIGH-1,
    repaired in the ladder's §2 qualification this round). The two lengths are now independent
    parameters.
  - Degree: exactly the factor 15.4. RL-6 = 0.3 nm / 15.40194 fm = 1.94805e4 stays the in-plane
    reading; RL-6 = 0.3 nm / 1.0 fm = 3.000e5 is the thickness reading; 0.3 nm / 6.742 fm =
    4.4497e4 is the alternative carrier length. The price spans 15.4x and the NO-GO does not move.
  - Self-consistent: YES. This is the only level on the ladder that is a *correction* rather than a
    relaxation: the two quantities were never the same length, and the record already said so in
    crosswalk §8.1/§8.2.
  - Hard boundary reached: NO.
  - Notes: B5 is what makes B3's output readable. Once L_z is dynamical, the thickness the price is
    denominated in is whatever the confinement branch produces, and the in-plane pitch is untouched
    by it. RL-6: 2e4 -> 3.000e5 on the thickness reading; still NO-GO by 4.5 orders of magnitude.
    G0' row 1: unchanged, because its basis is the in-plane quantity, which is why the row survives
    B5 at all. Effective-2D: unchanged (the criterion never used d_parallel).

------------------------------------------------------------------------------
B6 — coordinate-independence is no longer required of claims
------------------------------------------------------------------------------
  - Relaxed: the requirement that a programme statement hold in every frame (AX-01's DERIVED-COORD
    class becomes acceptable as a final form). Claims may now be true only in a named frame.
  - Degree: not quantifiable; it is a change in what counts as a claim. Its measurable content is
    the list of statements that were only frame-valid: kappa*rho_req and kappa*j_x,req (ansatz
    gauge), K = -f_t/f, Phi (observer frame; a beta = 0.5 z-boost moves the 2.25 eV probe to
    3.375 eV, outside the declared 1.65-3.26 eV band), L_z = 1 fm (a normalisation), and the
    effective-2D conditional itself, which flips at gamma = 1.1021 at its own L_z = 250 nm edge.
  - Self-consistent: YES, in the weak sense: the equations do not change, because Einstein's
    equations are covariant whatever the programme requires of its prose.
  - Hard boundary reached: NO.
  - Notes: the cost of B6 is not inconsistency but the loss of a refutation tool. Phase 1b's
    dismissal of f = 0 rested on "coordinate degeneration, not curvature singularity" -- a
    distinction that requires exactly the invariance B6 gives up. Under B6 a coordinate artifact
    becomes indistinguishable from a solution, so the programme can no longer tell a solved geometry
    from a badly chosen chart. That is a loss of discriminating power, and the record should say so
    plainly rather than dress it as a contradiction. RL-6: unchanged (a ratio of proper lengths at
    one point, invariant under transverse diffeos, but beta = 0.5 along x sends eps -> 1.155 eps, so
    even the relief ratio is frame-relative). G0' row 1: now a frame-relative statement -- true in
    the plate's rest frame, which is the frame the object defines. Effective-2D: unchanged in form,
    exposed in content: it has no frame slot (AX-01 F-008), and B6 makes that omission explicit
    rather than fatal.

------------------------------------------------------------------------------
B7 — energy conditions are relaxed
------------------------------------------------------------------------------
  - Relaxed: the weak energy condition, never explicitly declared (AX-01 flags no energy-condition
    statement anywhere in the record). Negative energy density becomes admissible as a source.
  - Degree: B3 already computed what the relief branch needs: rho_req alternating in sign at
    1.3e12 nuclear energy densities for mm-scale relief (1.3e6 at metre scale). Before B7 that
    alternating sign is a defect -- half the cell needs a source no ordinary matter supplies. After
    B7 it is a specification: the branch is built from a positive-negative stress pattern, i.e. an
    exotic-matter distribution, and the constraint equations are satisfied by construction.
  - Self-consistent: YES. Exotic matter is a consistent source in general relativity; what it is not
    is ordinary matter. The record contains no theorem that forbids it, only theorems that assume
    its absence.
  - Hard boundary reached: NO.
  - Notes: B7 does not *create* an inconsistency, it *removes* an obstruction -- and the removal is
    the interesting part. RL-5's S branch (the 2D pocket) is priced by "a singularity (Geroch)", and
    Geroch's topology-change theorem assumes the energy conditions and global hyperbolicity. Under
    B7 the first assumption fails, so that specific prohibition is no longer established. The
    measured branch (Schwinger flux, 1.22e40 W/m^2, 26.5 orders) is untouched by B7: it never rested
    on an energy condition.

------------------------------------------------------------------------------
B8 — causal structure is relaxed
------------------------------------------------------------------------------
  - Relaxed: global hyperbolicity. Closed timelike curves and propagation outside the light cone
    become admissible.
  - Degree: not a magnitude but a topological admission: the spacetime is allowed to contain a
    closed causal curve through, or causally connected to, the object's world-tube.
  - Self-consistent: NO.
  - Hard boundary reached: YES — HARD-SCI-FI-LIMIT.
  - Contradiction form: the record's scene is defined by a tuple theta = (aperture, gate <= 3 ns,
    band, distance, environment E, camera G), and by a sequence -- formation at t = 0, a 3-5 ns
    transient, a decay that "follows 15 orders later" than the switch-off burst (ladder E4 item 4).
    Two of the record's own assertions are then simultaneously made and unmade about the same
    object at the same time:
      A  the scene at theta is well defined: there is a definite time at which the object is
         observed, a definite duration it lasts, and an environment radiance independent of the
         object (the imaging equation I = R * L is used throughout the optics rungs);
      not-A  a closed causal curve through the scene removes the global time function that makes
         "before" and "after" meaningful, and makes the environment radiance depend on the object's
         own reflectance, so L is not independent of R.
    The record already treats this class of failure as fatal rather than as a gap: N7 calls the
    loss of a referent "not an insufficient gap but a referential failure". B8 is the first level
    that produces one.
  - Which relaxation caused it: B8's own, and only B8's. B1-B7 each weaken, cost, or re-scope; none
    of them makes a sentence about the scene both true and unsayable.
  - Avoidable by modifying other assumptions: YES. Two routes, both cheap and both already in the
    record. (i) Confine the relaxation: admit CTCs only in a region spacelike-separated from the
    observer's causal patch, which restores global hyperbolicity where the scene lives. (ii) Drop
    the transient and the imaged scene: carry the steady-state S branch only (RL-5's zero-flux
    pocket), where no duration and no reflected-light image is claimed, so no ordering and no
    radiance-independence is asserted. Neither route is recommended here; both are recorded because
    the directive asks whether the contradiction is avoidable, not which repair to adopt.
  - Notes: this is a *referential* contradiction, not a strict propositional
    one. If the boundary test is read as requiring a literal A and not-A over the same proposition,
    then no level from B1 to B9 supplies one, and the wall sits at B10 by construction -- which is
    what "B10 is non-relaxable" means. Both readings are recorded; the level at which the programme
    stops being hard SF is B8 under the record's own referential standard, and B10 under the
    strict-propositional one. RL-6: unchanged (a ratio of lengths survives any causal structure).
    G0' row 1: unchanged as an arithmetic statement; unsayable as a scene statement. Effective-2D:
    the conditional's E_probe slot presupposes a probe with a definite energy observed at a definite
    time; under B8 that slot has no referent, so the criterion is not false but undefined.

------------------------------------------------------------------------------
B9 — unitarity
------------------------------------------------------------------------------
Status: NOT EVALUATED-BEYOND-BOUNDARY. The boundary was reached at B8; relaxing information loss
after the scene has lost its referent would be evaluating a claim the record can no longer state.
Recorded, not guessed. What can be said without evaluating it: the programme's capture thresholds,
Gamma_e and tau_T are perturbative QFT outputs that assume unitarity, so B9 would re-open them rather
than contradict them; whether it would produce a contradiction of its own is unknown and is not
claimed here.

------------------------------------------------------------------------------
B10 — logical consistency
------------------------------------------------------------------------------
Status: NEVER RELAXED, per G-71-01 §4 and §3.2. This level is the definition of the boundary, not a
rung on it. A record that may assert A and not-A has no content, so no relaxation here can be
evaluated for self-consistency: the test would be the thing being relaxed.

------------------------------------------------------------------------------
HARD-SCI-FI-LIMIT
------------------------------------------------------------------------------
  Level:                B8 (referential reading); B10 by construction under the strict-propositional
                        reading. Both stated; neither is a recommendation.
  Contradiction form:   "the scene at theta is well defined" together with "a closed causal curve
                        passes through the scene", about the same object at the same time. The
                        tuple's time, its duration and its environment-independence all fail at
                        once, and the record's own standard for that failure is N7's referential
                        one, not a numerical shortfall.
  Avoidable by modifying other assumptions:
                        YES -- by confining the CTC to a causally disconnected region, or by carrying
                        only the steady-state S branch with no transient and no imaged scene. The two
                        routes are written out in B8; neither is adopted here.

------------------------------------------------------------------------------
Summary table
------------------------------------------------------------------------------
  level  relaxed premise                     self-consistent  boundary  RL-6        G0' row 1   eff-2D
  B1     Lambda = 0                          YES              NO        2e4          unchanged   unchanged
  B2     T = 0                               YES              NO        2e4          unchanged   unchanged (internal slot holds at 1 fm)
  B3     L_z external, no back-reaction      YES              NO        ratio, but  unchanged   inherits R1, not the map
                                                                         L_z is output
  B4     adiabaticity                        YES              NO        2e4          unchanged   transient only; referent lost after
  B5     d_parallel = thickness              YES              NO        3.000e5      unchanged   unchanged
  B6     coordinate-independence required    YES (weak)       NO        frame-rel.   frame-rel.  exposed, not broken
  B7     energy conditions                   YES              NO        2e4          unchanged   unchanged
  B8     global hyperbolicity                NO               YES (limit)  2e4       unsayable   undefined
  B9     unitarity                           NOT EVALUATED-BEYOND-BOUNDARY
  B10    logical consistency                 NEVER RELAXED

------------------------------------------------------------------------------
What this record does not do
------------------------------------------------------------------------------
  - It does not adopt any relaxation level. No level is recommended, and the fact that B3-B7 are
    self-consistent is not an argument for using them.
  - It does not move a gate, threshold, terminal class, D-state, V/Phi price or queue item.
  - It does not claim the object survives, is visible, or is 2D. B4's fireball is an archived
    branch being re-used as a consistency check, not a result of this round.
  - It does not prove or disprove adiabaticity, in either track (G-71-01 §4).
  - It does not re-derive kappa*rho_req = -f_xx/f; B3 and B7 evaluate that archived equation at two
    declared relief amplitudes and nothing more.

Content generated by AI
