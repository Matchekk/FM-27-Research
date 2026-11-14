# MECH-002-SHARPNESS-P0: cold runner preparation

**Offline draft, no scientific release.** This specialist adds only
`analysis/run_sharpness002.py`, `analysis/sharpness002_runner.py`, their tests and
this document. No shared research module, host, DLL, runtime, master route,
historical archive, seed registry or game file is modified. No native match,
new seed reservation, holdout or career operation was run by this specialist.

Scientific design/analysis belongs to `analysis/sharpness002_design.py` and
`analysis/analyse_sharpness002.py`; its separate preregistration is
`experiments/MECH-002-sharpness-pilot.md`. Root must integrate both specialists'
commits before preparing concrete inputs. These new files do not authorize a run.

## Input and identity boundary

Use only readonly observer
`58e05a46ca65014a227ed1bd61da090d326848d20f39744b59e175c8b7c13d32`,
FM27 DLL`8c6971ce0b1c8afe6529ea3f46205a5175aea988a97d7421a980da42e23fe340`,
the unchanged VALID-002 bundled fixture and frozen D00 IP4-2-3-1/OOP4-4-1-1.
Source/header/build manifest, resource fingerprint, fixture, role catalog,
runtime sources, Python base executable and NumPy/SciPy versions are bound in
prepared inputs. Before native execution, own Windows read handles prevent
write/delete races; hashes are checked again while those handles remain held.
No upstream Python initialization, NativeLab, warm worker, server or UI import.

The pure designer factory reads original D00 and original MECH003-R01 inputs.
It restores exactly ten declared Stamina52 values40→60 in R01, requires the
result to differ from D00 only in the single Standard→MoreOften pressing record,
then compiles the historical sharpness7000/10000 codec. Low changes exactly20
profile records16/17 for the ten absolute-lineup starting outfield slots; high
is byte-identical at the same pressing level. Other records, attributes, phases,
roles, PI, roster strength and management remain fixed; kind61 is forbidden.
The real5557-record files contain46Stamina52 records,23per side, not49. Three
inactive carrier-tail players are not encoded attribute records and are not
claimed as native readbacks. All46encoded/active Stamina values remain60.

Preparation requires an actual independently released TECH17 transfer gate:
`data/mech-002-startpolicy-tech/release-gate.json` plus
`docs/night-001/STARTPOLICY-002-RESULTS-REVIEW.md`, exact published result commit
and successful CI. Its original source is checked using archived Git blobs from
the TECH17 registration commit; its historical master is not compared to this
new route's current master. Real7000→cache70 must already be proved. Missing
release evidence blocks preparation; no invented true flags or fallback writer.

## Fresh seeds and immutable publications

Root alone reserves `local/registry/MECH-002-SHARPNESS-P0.reserved.json`:
experiment ID, namespace`MECH-002-SHARPNESS-P0/main-v1`, `main_seeds`64,
`technical_seeds`4 and `seeds`68as their disjoint union. Both groups must be fresh
uint32 values and disjoint from all historical, failed, technical, holdout-reserved
and pending seed metadata. The runner reads this registry file and never writes it.

Root alone adds the master route to `analysis/run_sharpness002.py` after TECH17
has finished. Prepare reserves no native keys and does not create/start the own
native budget. It freezes concrete16setups, original-source hashes, initial
control hashes, software identity, seed plan and executable-code hashes.

The publication sequence deliberately has two initial epochs:

1. Inert prepare; independent input review in
   `docs/night-001/SHARPNESS-REVIEW.md`; reviewer-authored
   `data/mech-002-sharpness-p0/review-gate.json` with experiment ID,
   `approved_for_technical=true`, `inputs_sha256`, `review_sha256`.
   Publish draft contract, inputs, code, seeds and review; require exact CI.
2. `register --publication <draft-sha> --ci-run <ci>` verifies that publication,
   sets registered metadata and creates the CORE manifest and complete33/512job
   plans. Publish these registrations and obtain exact CI again.
3. Root admits only the separate33-probe technical phase with that publication.
   Export/review/publish the result before any main phase.
4. Main additionally requires reviewer-authored `technical-release.json` with
   `approved_for_main=true`, `summary_sha256`, `review_sha256`, and review document
   `docs/night-001/SHARPNESS-TECHNICAL-REVIEW.md`, all in a successful publication.
   Original code remains unchanged. No automatic main, extension or optimizer.

Example operator sequence, **not executed here**:

```powershell
python analysis/night_supervise.py run --study MECH-002-SHARPNESS-P0 --phase prepare
# Review, publish draft inputs/code/seeds; wait for exact successful CI.
python analysis/run_sharpness002.py register --publication <draft-sha> --ci-run <ci>
# Publish registered manifest/plans, obtain exact successful CI.
python analysis/night_supervise.py run --study MECH-002-SHARPNESS-P0 --phase technical --keys-file local/mech-002-sharpness-p0/technical-keys.json -- --publication <registration-sha> --ci-run <ci>
python analysis/run_sharpness002.py export --export-phase technical
# Independent technical review/release, publish all evidence, obtain exact CI.
python analysis/night_supervise.py run --study MECH-002-SHARPNESS-P0 --phase main --keys-file local/mech-002-sharpness-p0/main-keys.json -- --publication <technical-release-sha> --ci-run <ci>
python analysis/run_sharpness002.py export --export-phase main
```

## Bounded cold dispatch and cleanup

TECH: four new context×side seeds, four arms twice=32full cold matches/16A/A pairs,
then one malformed-header negative, exit108/`stage="initial"`, no seed. MAIN:
64independent blocks,32per known context, two sides×four arms=512full matches.
Block grouping is deterministic; main uses eight jobs per context/seed, technical
eight per context/seed/side, negative last. No subsequent block after any failure.

One NativeLease with4workers covers each whole phase. ThreadPoolExecutor has
exactly four threads; atomically persisted claims occur before contained_call.
Each call has its own pending marker and separate Windows Job(max3processes):
capsule, native host parent and one engine child. There is no14-process whole
study job and no change to the frozen containment helper's3..10API.
The native host's one-engine-child job plus at most four in-flight claims gives
an engine upper bound4. The counter measures claims/calls, **not actual engine
PID peaks**. TECH must exercise four concurrent claims and all16exact A/A pairs.

A shared locked stop prevents new claims/blocks after the first detected gate
error. Already claimed jobs, at most four, may finish bounded cleanup and remain
accounted; their host GO can follow a stop set by another worker. The existing
helper's callback is after GO, and no false instantaneous cancellation guarantee
is made. Counter events include stop/claim/completion timestamps. Started,
failed, unresolved and unbegun jobs persist; no retry, refund or replacement seed.

Each command has90s no-progress timeout and a total deadline bounded by remaining
phase/UTC time. The own cumulative supervised-child allowance is900s across both
phases; fixed3600s UTC window starts with technical reservation, not inert prepare.
NIGHT-001's1800s global allowance and23:00UTC deadline still apply. Main requires
at least600sremaining in own allowance/window and global allowance/current outer
deadline immediately before its first native command. Private artifacts≤2GiB,
free disk>20GiB. Job pending markers are removed only after persisted kernel-zero
and capsule-exit proof. Any unknown cleanup retains the global lease/crash state.

## Readback, descriptive fields and publication

Every full match checks seed, loaded DLL, startup, all3174attributes/1058profiles,
44actual phase cells/748PI groups, Stamina60 for46actors, pressing bit0/66,
C90/C7A7000or10000 and starting cache8A70or100 after original preparation and
actual first advance. Cache89=100, condition10000, fatigue0, accumulator1e6 and
penalty0 initially. All46initial nonsharpness fields and rawTF33 must match the
identity-bound D00 gold for that context/side. Final progression is never clamped.

The canonical row is `job_id/context/team_side/seed/arm/status/config_sha256/
setup_sha256/identity/observer_host_sha256/result/native_audit`, plus provenance
and15preregistered descriptive fields. RawTF33 hashes include all-zero as one
pattern; they are not UI familiarity or proof of consumer execution. Missing
finished cache means null with a reason, never a zero or imputation.

Parent success additionally requires complete job accounting, matching raw/dump/
containment hashes, counter hashes, nonhalted reconciled budget, exact reserved
keys, successful parent operation(s), cumulative charge≤900and actual UTC finish
inside the immutable window/night deadline. Private phase budget snapshots and
post-lease-release reconciliation receipts preserve historical phase epochs.
Unknown charge is null; raw recorded charges and redacted operations remain
available. Tokens, argv and private paths are excluded from public budget output.
Incomplete or failed main phases export status/accounting only, not performance
rows or statistical effects. Only a complete, reconciled512-row phase may create
`main.jsonl`; the director must check `main-summary.json.passed` before analysis.

The12current specialist tests pass and are pure thread/data/mocked-admission tests. They
make no native or harmless child-process starts. Full integration, CI, actual
TECH17 release, new TECH32+1 and main permission remain Root/reviewer gates.
