# Implementation gaps

This file records every gap between the executable Python reference model and a paper-level MemScope artifact. None is hidden behind a dummy implementation.

## System implementation

1. **AOSP service and SDK:** `MemScopeManagerService`, Binder API, AppFunctions interception, UID/package/certificate binding, cross-user profiles, replay persistence, and public SDK objects require a named AOSP revision and patch series.
2. **AppSearch:** system-UID database ownership, indexable keyed-hash projection, privileged global session, ranking integration, transaction/version behavior, and native-index variant are not implemented on this host.
3. **Cryptography:** the Python HMAC token issuer is a reference protocol only. Production canonical encoding, Keystore/StrongBox signing, per-compartment AEAD, wrapped key lifecycle, rotation/destruction, and offline-database tests require Android.
4. **Complete mediation:** this repository cannot disable or instrument shadow vector stores, caches, logs, and cloud-memory APIs. The formal assumption is tested only as a model property.
5. **Trusted time and recovery:** Android monotonic high-water persistence, reboot replay state, write-ahead recovery, idempotent compaction, and audit-root durability remain device work.
6. **Audit/UI:** user explanations, narrowing/widening confirmation, review of quarantine, correction/revocation UI, storage-conflict UI, and content-minimized persistent audit partition remain unimplemented.

## Mathematical/paper ambiguity

The appendix scheduling example composes two parents whose tool sets have empty intersection and says no single tool can read both. Algorithm 2 simultaneously requires every parent to satisfy `Auth(m_j,q)` for one derivation token. Under Equation (3), both cannot hold. The reference code follows Algorithm 2 and rejects the operation. The authors must define a system composition principal or multi-token rule, its caller/tool semantics, audit behavior, and a corresponding proof before cross-token derivation can be implemented.

Algorithm 1 abbreviates the final check to policy epoch and token expiry, while the appendix requires item-expiry authorization at the release snapshot. The reference implementation performs the stronger final item recheck; author confirmation is requested.

## Semantic and policy components

- Abstractive attribution needs a version-pinned local/cloud NLI or structured verifier, frozen thresholds, high-sensitivity policy, and human-labeled evaluation corpus.
- The actual policy compiler needs canonical IDs, rule inheritance/conflict resolution, signing, wildcard rules, user/enterprise precedence, readable explanations, and formal validation.
- Purpose taxonomy, AppFunction mappings, compound-task decomposition, and confirmation UI need a reviewed policy corpus.
- Direct-write label defaults currently enter as already policy-capped input; the production source/task/data-class compiler is absent.
- Declassification is deliberately out of the ordinary derivation path and has no implementation.

## Data and benchmarks

No real files are included for LoCoMo, LongMemEval, Memora, PA-Bench, ProfileFoundry, PersonaChat, AndroidWorld, or the multi-app mobile workload. Licenses/registration, versions, checksums, normalized schemas, policy annotation handbook, two-annotator agreement/adjudication, split hashes, and benchmark-specific scorers must be supplied manually.

## Baselines and attacks

AppSearch visibility, GAAP-style IFC, Audience-Bound Memory, and MNC require version-pinned external artifacts and verified connectors. MEXTRA, ADAM, SPORE, MINJA, both MemPoison formulations, MemEvoBench-style drift, always-allow/no-memory controls, and ToolPrivacyBench-style atom scoring require the same. No external API or result is simulated under those names.

## Measurement and analysis

- Pixel 8, Pixel 9, and Samsung device builds, matched agent/model/ranker prompts, battery/thermal protocol, power rails, CPU/NPU instrumentation, storage accounting, and key-operation timing are unavailable.
- Benchmark accuracy/FAMA, abstention, tool-argument atoms, attack success strata, annotation agreement, energy, compaction pause, and thermal throttling require real traces.
- Prospective power analysis, three restarts, paired bootstrap, exact binomial/Wilson selection, Holm families, effect sizes, device blocking, failed-run logs, and exclusion handling must be finalized before real execution.
- The real runner deliberately stops after normalized-schema preflight until the benchmark mapper/scorer and Android transport are author-verified.

## Packaging/verification environment

The project declares Python 3.11+. Local lightweight verification used the available Python 3.9.6 interpreter with syntax kept compatible; EC2 CI must repeat tests on supported Python 3.11/3.12. `ruff` and `mypy` were not available locally, so no lint or static-type pass is claimed.
