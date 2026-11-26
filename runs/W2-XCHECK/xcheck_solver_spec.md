PROGRAMME: docs/program/RESEARCH_PROGRAM_v1.md v1.1.1 (sections 4.2.3, 4.2.6, 4.8, 5.1, 6.1, Appendix D).
PROVENANCE: NEITHER
# Solver spec -- W2-XCHECK-01

1. Each authority is read byte-wise; only presence and consistency of named fields are checked.
2. Tier thresholds in the spec are compared with runs/MATRIX/threshold_lock.json to 1e-12.
3. Ladder rung identifiers RL-1..RL-6 and the four price-record fields are counted; a missing price is reported as UNSPECIFIED, never invented.
4. The protocol's WIP and report-only gate statements are located as text; no gate mark is changed.
5. A mismatch is a finding about the programme's citation, not a redefinition of an authority.
