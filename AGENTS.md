# DCC agent notes

DCC is a research record, not an application. `docs/` holds authority, `src/` holds standalone instruments, `runs/` holds products, `reports/` holds dated readings. There is no build system, package manifest, or test runner; run scripts individually from the repo root.

## Authority and current goal

- Current programme authority is `docs/program/RESEARCH_PROGRAM_v1.md` (v1.1.1, O0). Older roadmap/verdict goal statements are retained as records, not authority. `reports/DCC_research_progress_v1.md` explicitly says "authority: none"; cite the record, not the report.
- Rule sources: `docs/conventions/symbol_registry.md`, `docs/conventions/provenance_tags_v1.md`, `docs/conventions/display_conventions_v1.md`, `docs/program/COMPLETION_PROTOCOL_v1.md`.
- Since G-64-01 the audit/commit instruments are **report-only** (exit 0 always). `commit_gate.py`, `program_audit.py --check-*`, and the linters do not veto a product. Unmarked `[ ]` governor blocks are not approval; never fill them as executor.

## Setup and exact commands

- Install deps before running anything substantive: `python -m pip install -r requirements.txt`. The verified interpreter/dependency versions are recorded at the bottom of that file; do not assume the current interpreter has them.
- Scripts commonly use isolated mode and expect CWD = repo root, e.g. `python -I src/g0_analytic/scale_budget_v3.py`, `python -I src/common/conv.py`. Read the script header for its run line and whether it needs `--write`.
- Verification instruments:
  ```sh
  python src/common/commit_gate.py
  python src/common/program_audit.py                  # board + DoD, stdout only
  python src/common/program_audit.py --write          # regenerates runs/PROGRAM/*
  python src/common/program_audit.py --check-locks
  python src/common/program_audit.py --check-citations
  python src/common/provenance_lint.py
  python src/common/provenance_lint.py --selftest
  python src/common/symbol_lint.py
  python src/common/display_lint.py
  python src/common/locked_path_guard.py              # only this returns 1 on BLOCK
  ```
- Round ledger is append-only and hash-chained: `python src/common/program_audit.py --ledger-append N --id ID --verdict VERDICT --registration runs/... --product runs/...`. Never hand-edit `runs/PROGRAM/round_ledger.jsonl`; `mtime` is unreliable (a bulk copy reset it), the ledger is the ordering proof.
- Emit results with the script's `--write` path or shell redirection to `runs/...` as the registration declares. Never hand-transcribe numbers or invent/copy retyped digests; copy hashes from the file that produced them.

## Product discipline

- Before a new instrument: write pre-registration with a numeric prediction and kill condition, lock thresholds/constants first, and measure the instrument floor before setting a bar. Do not introduce and evaluate a threshold in the same round; keep `CHECK`/`IDENT`/`NEGCTRL` counts separate.
- Archived stdout and products are immutable. Corrections are appended errata (`E1`, `E2`, …) in the same file; failed runs are kept, not cleaned up. Linter hits under `runs/` are archived facts, not cleanup targets.
- Every measured number is quoted with its product by file and line. A number carried across ledgers by paraphrase is not evidence.
- Every new text product under `runs/` carries exactly one `PROVENANCE:` line: `CHAIN-EVIDENCE`, `BOUNDARY-INPUT`, or `NEITHER`. `runs/S45/` may not claim `CHAIN-EVIDENCE`; `BOUNDARY-INPUT` must include `TYPE`, `OVERDETERMINATION`, and `DERIVATION`. Binary products need `<file>.display.txt` sidecars. Lock files are exempt only while their `.sha256` verifies; do not extend the closed P9 exemption manifest.
- Frames need the nine-field `DISPLAY-DECLARATION` block; visible-band chromatic colour is `DECLARED-CONVENTION`, not `PHYSICAL`. `display_lint.py` only walks existing sidecars, so an image with no sidecar is silently non-citable — check images manually.

## Naming traps that have already caused defects

- `C1`–`C3` are the only single-letter enumeration owner; new label sets need a ≥2-letter prefix. Bare `τ` is the Drude relaxation time; the conversion clock is `τ_conv`. Use `FL1`–`FL3` for fidelity (bare `L1`–`L3` has three owners); `ME1` is vacated alias of `CM5`; `ME3` is retired.
- `G4` has two referents; the governing chain is roadmap v1.4's. `d_∥ = 15.40 fm` and `d_par = 6.7420 fm` are different baselines. Qualify `S1`/`S5` etc. by namespace (`σ_s` spec vs registry rules vs scene stages).
- Never claim visibility/transparency before `G6`, use unqualified "lossless", scan `τ` as a response, or re-open a closed line except through its reverse-on clause.

## Repository map

- `src/common/` = enforcement/report instruments; `src/route/`, `src/analysis/`, `src/g0_analytic/`, `src/r1_*`, etc. = round-specific instruments; root-level `DCC_*.py` and `sympy_*_stdout.txt` = legacy P1–P4 derivation layer.
- `configs/*.json` and `runs/*/*lock*.json` are authority inputs read by instruments (thresholds, demo/serial locks, locked paths), not scratch configuration. Editing a lock or its sidecar breaks the evidence that a declaration predated the data.
- `runs/PROGRAM/program_audit_results.txt` and `governor_digest.txt` are generated snapshots; regenerate with `--write` instead of trusting a stale copy.
