# TODO before submission

## Blocking empirical work

- Implement the Android emulator prototype (Binder service, Agent SDK, token issuer, encrypted service store, label propagator, compactor, audit path, recovery) and complete the typed Python reference model used for matched experiments.
- Audit the mediation boundary and document private caches, logs, and cloud stores; do not claim complete mediation on a commercial device.
- Run RQ1--RQ7 on the Android emulator and the Python reference model; no physical-device energy, thermal, or StrongBox claims.
- Replace Tables 3--4 and Figure 6 with raw-data-backed results and confidence intervals.
- Reproduce or clearly label reimplementations of MEXTRA, MINJA, ADAM, SPORE, and both MemPoison settings.
- Implement and validate the synthetic multi-app workload and policy oracle; optional GUI subsets (MemGUI-Bench, AndroidWorld) only after core results are frozen.
- Release raw traces, analysis scripts, build manifests, device metadata, prompts, seeds, and checksums.

## Citations and concurrent work

- Refresh the literature search immediately before submission.
- Replace 2026 arXiv citations with archival versions where available.
- Add exact versioned Mem0/Letta references if used as executable baselines.
- Resolve MemGUI-Bench only if retained in experiments.
- Pin AOSP/AppSearch/AppFunctions documentation to the implementation version.

## Theory and security validation

- Map every formal assumption to code and an integration test.
- Add property-based tests for label meets, derivation paths, and expiry.
- Run negative controls for token forgery/replay, confused deputy, shadow cache, clock rollback, ranker bypass, and authorized-recipient copying.
- Empirically measure attribution false acceptance/rejection, especially for high-sensitivity items.
- Do not strengthen the interface theorem into semantic non-inference.

## Author and venue metadata

- Replace anonymous author/affiliation placeholders.
- Confirm author order, corresponding author, ORCIDs, acknowledgments, funding, conflicts, and ethics approval.
- Select the actual venue. Venue is fixed as the Journal of Systems Architecture (rolling); convert author/affiliation metadata as needed and confirm journal-specific declarations.
- Add highlights/graphical abstract declarations only if required by the chosen Elsevier journal.

## Figures and LaTeX

- Replace conceptual plot coordinates; never submit them as measurements.
- Regenerate figure previews after result insertion and rerun the overlap audit.
- Fix or accept remaining minor overfull/underfull box warnings under the final venue template.
- Investigate the Tectonic cached `algorithm.sty` invalid-UTF-8 warning or compile with a clean TeX Live distribution.
- Add verified page/article numbers to proceedings entries when available to remove BibTeX empty-page warnings.

## Assumptions requiring real validation

- Binder/AppFunction identity is trustworthy across nested and legacy tool adapters.
- Policy epochs and item expiry are rechecked atomically at release.
- No ranker/model path can access unauthorized plaintext or embeddings.
- StrongBox/Keystore behavior is not tested; the emulator uses software-backed keys, and vendor secure-hardware behavior remains future work.
- Hard-pinned safety items fit realistic storage budgets.
- Purpose defaults are understandable and do not cause unacceptable denial or prompt fatigue.

Current status: design manuscript plus typed reference implementation and emulator prototype plan; empirical submission blockers remain.
