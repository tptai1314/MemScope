# TODO before real experiments

No item below is optional for any real experimental cell that depends on it.

## Author decisions

- [ ] Resolve Algorithm 2 versus the disjoint-tool scheduling example: specify a trusted composition principal or multi-token rule and update the proof.
- [ ] Confirm final per-item release reauthorization as the intended Algorithm 1 contract.
- [ ] Freeze the purpose taxonomy, AppFunction mapping, policy precedence, wildcard policy, and declassification rules.
- [ ] Define the exact empty-ground-truth convention for entitled Recall@k.

## Android implementation

- [ ] Pin AOSP/AppSearch/AppFunctions revisions and implement `MemScopeManagerService` plus SDK.
- [ ] Bind Binder UID, package certificate, active AppFunction/tool chain, Android user/profile, task, nonce, epoch, TTL, and query budget.
- [ ] Implement system-owned AppSearch schema/projection and a final trusted policy recheck.
- [ ] Implement compartment AEAD, Keystore/StrongBox wrapping, rotation/destruction, and integrity-associated labels/provenance.
- [ ] Implement durable replay state, snapshot/version transactions, write-ahead recovery, revocation epochs, compaction, and audit roots.
- [ ] Add correction/invalidation, declassification, user review, policy explanation, and resource-conflict UI.
- [ ] Audit/disable shadow memories, caches, logs, and unmediated cloud stores in the evaluated build.

## Real data

- [ ] Manually obtain and license LoCoMo, LongMemEval, Memora, PA-Bench, and any ProfileFoundry/PersonaChat/AndroidWorld inputs.
- [ ] Record source/version/license/checksums and normalize to `docs/data_format.md`.
- [ ] Write/freeze the policy annotation handbook; double-annotate a stratified sample; report agreement and adjudication.
- [ ] Freeze splits before final runs and keep pilot traces separate.
- [ ] Implement and validate each benchmark-specific answer/FAMA/abstention scorer.

## External baselines and attacks

- [ ] Pin and reproduce AppSearch visibility, GAAP, Audience-Bound Memory, and MNC where artifacts are available; record unsupported policy dimensions.
- [ ] Pin/reproduce or clearly label reimplementations of MEXTRA, ADAM, SPORE, MINJA, both MemPoison settings, and MemEvoBench-style drift.
- [ ] Implement always-allow, no-memory, shadow-cache, stale-token, always-accept, and authorized-copy negative controls in the device harness.
- [ ] Freeze attack budgets, knowledge, success strata, and connector-only deviations.

## Attribution and policies

- [ ] Build the claim/span-labeled derivation corpus with faithful, unsupported, contradictory, cross-scope, stale, expired, and omitted-qualifier cases.
- [ ] Validate extractive, local NLI, and optional cloud NLI verifiers; freeze thresholds without test tuning.
- [ ] Implement source/task/data-class policy defaults and signed policy compilation.

## Devices, statistics, and release

- [ ] Provision Pixel 8, Pixel 9, and eligible Samsung device; record build, battery, thermal, and hardware-key metadata.
- [ ] Implement Binder/signature/projection/ranking/decryption/audit latency instrumentation and external/device power measurement.
- [ ] Complete prospective power analysis, restart/repetition counts, Holm families, effect sizes, thermal rerun rule, and exclusion policy.
- [ ] Implement raw trace manifests linking every table cell and plot point to hashes.
- [ ] Run `python -m pytest -q`, then configured lint/type checks on Python 3.11/3.12 CI.
- [ ] Run the full matched harness only on EC2/devices after all relevant boxes above are complete.
