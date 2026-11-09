# Mathematics-to-code audit

| Paper location | Object | Implementation interpretation | Edge cases / consistency |
|---|---|---|---|
| Eq. 1, Sec. 3.1 | Task context | Immutable validated dataclass; trusted time is supplied by a clock at verification/release | Paper writes `tau_q` in the signed context while also requiring a trusted current time. Code treats signed `task_time` as issuance context and evaluates current monotonic time separately. This conservative distinction avoids a frozen-time token. |
| Eqs. 2-3 | Label and authorization | Exact membership across purpose/app/tool/consumer, inclusive not-before, exclusive item/token expiry, valid provenance | Empty scope denies. `None` is a real tool identity only when explicitly authorized. NaN/infinite times reject. Internally consistent. |
| Eq. 4 | Meet | Set intersection, max sensitivity, max not-before, min expiry | Parent set must be nonempty. Empty required intersections cause quarantine. If `max(b) >= min(e)`, label is unusable and quarantined. Internally consistent. |
| Eq. 5 | Authorized view | Recheck every projected candidate before ranking | Projection may over-approximate but never authorizes. Under-approximation affects utility only. Internally consistent. |
| Eqs. 6-7 | Violations and misses | Counts over query outputs and ground-truth entitled IDs | Duplicate returned IDs are deduplicated per query to avoid inflated counts. Missing ground truth is a validation error. |
| Eq. 8 | Entitled Recall@k | Mean per-query recall over eligible ground truth | The paper does not define `|G(q)|=0`. Code excludes empty-ground-truth queries by default and can return 0 by policy; audit metadata records the denominator. |
| Eq. 9 | Derived validity | Proposed label must be no more permissive than meet and content must pass attribution policy | Label monotonicity remains guaranteed even if attribution is wrong. Parent version/digest checks implement the prose requirement omitted from Eq. 9. |
| Eqs. 10-11 | Retention objective | Greedy value-density heuristic and exact dynamic-programming oracle for small integer budgets | The paper explicitly claims no greedy approximation ratio. Negative-value items are evicted first. Zero-sized items are validated out. Hard pins exceeding budget raise `ResourceConflict`. |
| Eq. 12 | Token attenuation | Child has the same app/consumer/purpose, one active tool permitted by parent, no later expiry, no larger query budget | The paper gives a scope relation without a full token algebra. Code chooses the narrow, fail-closed interpretation and records this as requiring Android-author confirmation. |
| Algorithm 1 | Retrieval | Verification, projection, trusted recheck, ranking, epoch/time recheck, bounded restart, audit | The pseudocode final check mentions token time/epoch but the proof additionally requires item expiry in the release snapshot. Code reauthorizes ranked items at release, which is the mathematically conservative implementation. |
| Algorithm 2 | Derived admission | Atomic parent snapshot, authorization/version/digest checks, meet, label order, empty-scope and attribution handling | The PDF body references Algorithm 2 but the rendered placement is absent from extracted page text; the algorithm exists in the manuscript source and its prose fully specifies the same steps. Marked as a paper rendering inconsistency, not a semantic conflict. |
| Algorithm 2 vs. App. C scheduling example | Cross-token derivation | Reference implementation requires one derivation token to authorize every parent, exactly as Algorithm 2 states | The scheduling example gives parents with disjoint tool sets and says no token/tool is authorized for both, yet expects a meet-derived item. Such parents cannot both pass Algorithm 2's per-parent `Auth(m_j,q)` under one active tool. Code fails closed and rejects this cross-token case. A system-level composition authority or multi-token derivation rule requires author specification. **Paper inconsistency detected.** |
| Algorithm 3 | Compaction | Expire/revoke first, hard-pin feasibility, then ascending density | Equation numbering in Sec. 7.6 calls the objective “Equation (11)” although objective spans Eqs. 10-11. Code maps both. Minor cross-reference inconsistency. |
| Statistical plan | Wilson/bootstrap/Holm | Deterministic seeded bootstrap, Wilson score interval, Holm-adjusted p-values | No statistical result is run on real data. Implementations reject malformed inputs and do not invent confidence values. |

## Conservative corrections requiring author confirmation

1. Retrieval performs a final per-item authorization/integrity check after ranking, not only the token-expiry/epoch check shown on Algorithm 1 lines 14-16. This is required by the appendix's final-check-freshness lemma.
2. Token attenuation uses equality for app, consumer, and purpose and membership for the child active tool. A broader delegation algebra is not specified.
3. Entitled Recall@k excludes tasks with empty entitled ground truth; callers can request a zero contribution explicitly.
4. Cross-token derivation with disjoint tool scopes is not implemented because it conflicts with Algorithm 2. Author confirmation must define a trusted composition principal and prove that it does not widen policy.

These choices are surfaced in the README and TODO file. No theorem or guarantee is silently strengthened.
