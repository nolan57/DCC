# Submission (verbatim) — governor, 2026-11-22 21:01 +08

> Archived verbatim for the record. This is the acceptance of `PARTIALLY ADOPTED` plus four sharpenings and one
> decision. Ruling: `docs/decisions/sc2_lineshape_ruling_v1.md`.

---

This ruling is very important. I think it does more than revise the previous recommendation; it further narrows down the true blocking mechanism of G6/DC2.
**I accept this** `PARTIALLY ADOPTED` **ruling. In particular, it must be explicitly acknowledged: in my previous round I treated a "yield-strength misreading" that never existed in the record as an issue to be corrected, which was a wrong attribution of the problem.** The `REPAIR-ABSENT` judgment is reasonable.

I see four most important outcomes of this work.

## 1. The real problem has shifted from a definitional issue to a problem of physical closure

Previously, the problem was easily understood as:

\[ \text{how to construct a self-consistent }\sigma_s(\omega) \]

A more accurate formulation now is:

\[ \boxed{ \text{how to obtain a microscopically grounded, relaxation-time-solved, spectrally legitimate } \sigma_s(\omega) } \]

All three requirements are indispensable:

- The material state must actually exist;
- The relaxation time \(\tau\) must be determined by a physical mechanism, not by scanning a parameter;
- The Drude and interband responses must share a legitimate spectral-weight budget and satisfy causal dispersion relations.

The third point in particular means that even if the existing module performs well numerically in the low-energy optical range, that does not justify concluding that the full response function is valid.

## 2. The two genuine defects found are of different natures

### FSUM-SPLIT: spectral-weight misallocation

You found that:

\[ W_{\rm intra}=W_{\rm total} \]

and then added interband spectral weight on top of it.

This is not an ordinary numerical error but a double-counting of the budget in the response model.
What should be established is:

\[ \boxed{ W_{\rm intra}+W_{\rm inter}=W_{\rm total} } \]

But one theoretical detail must be noted here: the total spectral weight must be determined by the actually chosen microscopic Hamiltonian and its current operator; f-sum formulas from different models must not be patched together.

### KK-UV: causality problem

This issue deserves more attention than the low-energy residual.
A step-like real-part response:

\[ \operatorname{Re}\sigma(\omega) =A\Theta(\omega-\omega_g) \]

produces a corresponding logarithmic imaginary part:

\[ \operatorname{Im}\sigma(\omega) \propto -\frac{A}{\pi} \ln\left| \frac{\omega_g+\omega}{\omega_g-\omega} \right| \]

Therefore, it is not enough to correct the amplitude.
The lineshape of the response must be modified so that it has physically reasonable threshold broadening and high-frequency falloff, and the Kramers–Kronig relation must be re-verified.

I agree with you listing this as a model defect rather than eliminating it by tuning parameters.

## 3. I consider TAU-OBLIGATION the most important new constraint in this round

This point deserves particular emphasis.
The previous Kubo route tended to invite a dangerous simplification:

\[ \sigma(\omega) = \frac{ne^2\tau/m^\*}{1-i\omega\tau} +\sigma_{\rm inter}(\omega) \]

and then scan different \(\tau\) values and select one that matches expectations.
That does not actually solve the problem.
What is truly needed is:

\[ \boxed{ \tau=\tau_{\rm micro} (\text{material composition, interactions, temperature, density, and geometric state}) } \]

But a further distinction is needed:
**The Kubo formula itself does not guarantee the existence of a unique scalar relaxation time.**
For complex many-body systems, the current correlation function may have multiple relaxation modes, non-exponential decay, or a frequency-dependent effective relaxation time.
Therefore, I recommend adding an explicit requirement to future specifications:

- If the response can genuinely be reduced to a Drude form, the regime of validity of this approximation must be demonstrated;
- If it cannot be reduced to a single Drude pole, compute the full current response function directly;
- It must not be allowed to scan \(\tau\) in order to select favorable optical results;
- \(\tau\) must be traceable to a specific microscopic scattering mechanism or to a response-function pole width.

Only in this way will a model that formally passes tests not remain, in practice, dependent on ad hoc parameters.

## 4. The correct project decision at present: do not bypass R1-B1

### Current blocking chain for G6/DC2

**R1-B1** → determine the actual material state and equilibrium EOS → **microscopic scattering and current response** (determine the relaxation mechanism and the full response function) →
**spectral-weight allocation + Kramers–Kronig** (resolve FSUM-SPLIT and KK-UV) → **self-consistent \(\sigma_s(\omega)\)** (G6 prerequisite) →
**G6 / DC2** (material optics, radiative transfer, and observer predictions)

Here I support the decision you have already made:

- Do not disguise a compliance specification as a reconstruction specification;
- Do not bypass N7 prematurely;
- Do not manufacture self-consistent results by scanning \(\tau\);
- Do not presuppose transparency or opacity in order to pass G6.

## My final judgment

This ruling has in fact advanced the research question by one step:
Previously, what was missing was a complete surface-conductivity model.
It is now known that the existing candidate models have at least two genuine defects—spectral-weight misallocation and high-frequency causality—and that the relaxation time itself has not been solved microscopically.

I recommend keeping the current `surface_conductivity_v1.md` and not rushing to create a second specification. Once R1-B1 provides a usable material state, the real reconstruction work can begin.

**Most importantly: do not treat passing G6 as the research goal; treat obtaining an optical response that does not depend on ad hoc tuning and satisfies all physical constraints as the goal.**

If the final calculation shows that no stable material state satisfying the conditions exists, or that no response function meeting the requirements exists, that is likewise a valid physical conclusion, not a project failure.
