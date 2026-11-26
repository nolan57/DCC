PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 4.2.3, 4.2.6, 4.8, 5.1, 6.1, Appendix D).
PROVENANCE: NEITHER
# Solver spec -- W2-C3TEST-01

1. **What is solved.** No dynamics. `conv.frozen_state()` and `conv.beta_envelope()` supply the registered electron states; no EOS is written here and no tau is scanned.
2. **Convention envelope.** All three MODES are reported; a single-convention number is never used as the answer (conv.py module header; dimensional_conventions_v1.md section 5).
3. **Graph evidence.** The source of `plate_field` and `canvas_field` is scanned for composition tokens. Byte identity of u alone is NOT accepted as proof of non-consumption (section 1.1 / 4.6).
4. **C3 slots.** sigma_s is NOT-MEASURED; t_life is IMPORTED; L_nu is OUT-OF-SCOPE. These are recorded as separate slots, not merged into a PASS.
5. **Verdict vocabulary.** GENERATOR-DOES-NOT-CONSUME requires graph absence; otherwise NO-OBSERVED-EFFECT is recorded.
