# Provenance tags — separating boundary data from validation evidence

**Created**: 2026-11-22
**Status**: **ACTIVE.** Governs all run products from this date.
**Authority**: governor ruling D-A, `docs/decisions/meff_boundary_disposition_v1.md` §2
**Enforcement**: `src/common/provenance_lint.py` → `runs/CONVENTIONS/provenance_lint_results.txt`

---

## 0. Why this exists

The ledger's original rule ("products of the S3→S4 branch may not be cited as evidence for the chain") was
too blunt, because the S2 solve *needs* numbers at its outer boundary and refusing them makes S2
unsolvable. Ruling D-A replaced it with a two-category split. A split that lives only in prose is not a
control — every future result file is a fresh opportunity to relabel. Hence a tag on the product itself.

## 1. The tags

Exactly one `PROVENANCE:` line per product, inside the banner block:

| Tag | Meaning | Admissible as |
| --- | --- | --- |
| `PROVENANCE: CHAIN-EVIDENCE` | produced inside the S0→S2 chain (C1+C2+C3 held, D2 carried or discharged) | validation-ledger evidence for the chain |
| `PROVENANCE: BOUNDARY-INPUT` | produced by the S3→S4 branch (a constraint relaxed) | **typed boundary data only**, under PROV-3 |
| `PROVENANCE: NEITHER` | definitional / arithmetic / audit / convention products | nothing — it audits, it does not establish |

`NEITHER` is not a demotion. Most of the record's most useful products are `NEITHER`: symbol audits,
definitional probes, convention documents. They are honest about what they are.

## 2. Rules

**P1 — one tag, always.** Every new product under `runs/` declares its tag in the banner block. No
default, no inference from location.

**P2 — the branch cannot self-certify.** No file under a branch directory (`runs/S45/`, and any future
`runs/S4*/`) may carry `CHAIN-EVIDENCE`. If a branch product is genuinely chain evidence, it was not
produced by the branch and belongs elsewhere — which is itself the signal that something is mislabelled.

**P3 — citation is directional.** A `CHAIN-EVIDENCE` product may consume a `BOUNDARY-INPUT` product only
as declared, typed input (`PROV-3`), never as support for a conclusion. Mechanically: a chain product
citing a branch file must name it under an `INPUTS:` field; a citation in a *conclusion* is a violation.

**P4 — `BOUNDARY-INPUT` carries the three PROV-3 fields.**

```
TYPE: <Dirichlet|Neumann|Robin|asymptotic> on <field> at <surface>; regularity <assumed>
OVERDETERMINATION: n_data = <int>, n_dof_predicted = <int>, surplus = <int>
DERIVATION: <source> ; C1 assumed: no ; C2 assumed: no
```

- **TYPE** — well-posedness is a property of *(operator, boundary type, function space)*, independent of
  the values. A number without a type is not boundary data. Supplying values does **not** confer
  well-posedness; it only chooses a closure.
- **OVERDETERMINATION** — if `n_data` fixes the interior entirely (`surplus ≤ 0`), the run is a
  *reconstruction* of the data, and any agreement with the branch is a theorem about the data, not a test
  of the model. Such a run must be labelled `RECONSTRUCTION` and may not be reported as validation.
- **DERIVATION** — the data must be obtained without assuming C1 or C2, since those are the hypotheses
  under test. An exact solution, an asymptotic expansion at infinity, or a full-3D calculation that
  nowhere imposes a column structure qualifies. A 2D-reduced calculation does not.

**P5 — a solve using branch data is conditional.** It reports "solution given data D", never
"confirmation of D". The conditionality survives into every downstream citation.

**P6 — legacy products are not retro-edited.** Products dated before 2026-11-22 are classified
`LEGACY-UNTAGGED` by the linter and left byte-identical (§9.1). The linter's count of them is the measure
of how much of the record predates the split, not a defect list.

**P7 — a binary product declares itself through its sidecar.** A `.png`, `.jpg`, `.npz`, `.npy`, `.pdf` or
`.mp4` cannot carry a text line, so its declaration is the sidecar `<file>.display.txt` written under
`display_conventions_v1.md` — which already contains a `PROVENANCE` field. A binary with no sidecar is
`MISSING` unless it is in the frozen baseline. Added 2026-11-22, when the first binary product of the route
(a frame) made the gap visible; negative-tested by planting an unsided binary.

## 3. What the tag does and does not buy

**Buys.** A mechanical test for the one error that would invalidate the chain: a branch product promoted
to evidence. And a mechanical requirement that boundary data declare their type, their over-determination
status, and their independence from C1/C2.

**Does not buy.** Correctness of the derivation. A `CHAIN-EVIDENCE` tag on a wrong result is still a wrong
result. The tag records *provenance*, and provenance is necessary, not sufficient.

## 4. Grandfathering boundary

| Directory | Class |
| --- | --- |
| `runs/CONVENTIONS/` | `NEITHER` (convention enforcement reports) |
| `runs/S45/` | branch — `BOUNDARY-INPUT` or `NEITHER` only |
| `runs/ANALYSIS/` | mixed; each product's own tag decides, legacy by date |
| `runs/{R1A,R1B,R2,R3,R4,R5,G0,P1}` | mixed; legacy by date |

---

## 5. P8 — a hash-locked declaration is exempt from P1, but only on proof

Registered 2026-11-22, forced by `runs/MATRIX/threshold_lock.json`.

A lock file is the one artifact that **cannot carry a PROVENANCE comment**: any comment changes its digest, and the
digest is the entire evidence that the declaration preceded the data. Requiring the tag would therefore destroy what
the tag exists to document — the same structural conflict as P7 (a PNG cannot carry a text line), resolved the same
way, by a sidecar.

**Rule.** Given a product `P` and a sidecar `P.sha256` holding a SHA-256 digest, if the digest of `P` matches then
`P` is classified **`LOCKED-ARTIFACT`** — non-blocking — with the reason "digest verified, cannot be annotated".
If the digest does **not** match, `P` is a **`VIOLATION`** ("lock digest mismatch"). If the sidecar is absent, the
normal rule applies and `P` is `MISSING`.

**Why this is stronger than a comment, not weaker.** A comment asserts that a declaration was written; it carries no
evidence that the file was not edited afterwards. A matching digest *proves* the file was not edited. The exemption
is therefore granted on strictly better evidence than the rule it replaces — which is the only condition under which
extending a linter to excuse one's own file is legitimate rather than self-serving.

**Negative-tested** (`src/common/provenance_lint.py`, 2026-11-22): untouched copy → `LOCKED-ARTIFACT`; one
threshold altered by `0.05` → `VIOLATION` (`5f324e15… != b4e7f35e…`); sidecar deleted → `MISSING`. The exemption
cannot be obtained by deleting the sidecar or by editing the file — only by a genuine matching digest.

**Does not buy.** That the locked content is *correct*. A well-locked wrong threshold is still a wrong threshold;
`P8` records integrity, not truth.

---

## 6. P9 — a named exemption, honoured only while it cannot be extended

Registered 2026-11-23, forced by `BN-04`: twelve products had been blocking the commit gate for six rounds.

**The deadlock.** `P6` grandfathers by manifest, and the manifest was frozen at adoption. Twelve products by the
same production lines (`runs/OPTICS/sc*.txt`, `runs/R1B/r1b1_p{1,2,3,4}_*.txt`) are not in it, and they cannot
be tagged: a tag is an **edit** to an archived product (`s9.1`), and a tag written *today* would assert a
provenance judgement made *after* the numbers — the retro-declaration problem of
`docs/specs/theta_camera_v1.md` §0, one level down. So `P1` and `P6` together produced a state where the files
were neither taggable nor grandfathered, and the gate could not go green without a lie.

**The rule.** A product `P` listed in `runs/CONVENTIONS/provenance_exemption_bn04.txt` is classified
**`EXEMPT-LEGACY`** — non-blocking — if and only if both hold:

1. the manifest's own digest verifies against `provenance_exemption_bn04.txt.sha256`, **and**
2. `P`'s digest matches the digest recorded beside its path.

If (2) fails, `P` is a **`VIOLATION`** ("exempt file edited after exemption"). If (1) fails, the **entire list
is void** and every product named in it returns to `MISSING`.

**Why condition (2) is the whole rule.** Without it the manifest would be a place to put files and then edit
them — new text under an old name, with the linter's blessing. With it, the exemption asserts exactly one
thing: *this file is the file that was written*. This is `P8`'s structure (a digest proves non-editing; a
comment cannot) applied to a different conflict, and it is the same trade: the weaker claim, which happens to
be the true one.

**Why the list must be closed.** An exemption that can be extended is a policy, and `P1` is already the policy.
The closure is mechanical rather than procedural: appending a thirteenth line changes the manifest's bytes,
breaks the sidecar, and voids all twelve. Re-signing is always possible, and the friction is the point — it
requires deliberately recomputing and rewriting a sidecar, which is a recorded act rather than a quiet append.

**Negative-tested** (`src/common/provenance_lint.py --selftest`, 5/5): untouched file → `EXEMPT-LEGACY`; one
byte appended → `VIOLATION`; a thirteenth line appended to the manifest → both files `MISSING` (list void);
sidecar deleted → `MISSING`; a list member that genuinely carries a tag → `OK`, because a `PROVENANCE:` line
is scanned first and an exemption never shadows a tag.

**Does not buy.** Standing. `EXEMPT-LEGACY` is **not** `OK`: it says no provenance judgement has been made, so
a citation of one of the twelve may not be read as though its provenance were declared. Their numbers are not
withdrawn — the SC route is closed by its own rulings and the `R1B` substance now lives in
`g6_dc2_ruling_v1.md` (ratified, `PG-01`) — but the files themselves stay undated.

---

*Content generated by AI*
