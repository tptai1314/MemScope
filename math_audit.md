# Mathematical audit

Audit date: 2026-10-03. Formal scope: deterministic safety of the MemScope service interface under explicit trusted-system assumptions. No theorem claims semantic non-inference, truthfulness of generated text, side-channel freedom, or protection after authorized disclosure.

| Result | Exact statement summary | Required assumptions | Proof status | External theorem/citation | Gap / dimensional check / strength | Required revision |
|---|---|---|---|---|---|---|
| Lemma 1 (`lem:meet`) | The meet of a nonempty source set is no more permissive than every source label. | Defined product order; finite nonempty source set. | Complete, main text. | Lattice background only: Denning; Myers--Liskov. | Set/time/sensitivity coordinates match; no undefined constants. Claim is elementary and appropriately narrow. | None. |
| Lemma 2 (`lem:view`) | Every member of the authorized view satisfies the authorization predicate at the release snapshot. | Authentic token; integrity-protected state; atomic/revalidated snapshot. | Complete, main text. | None. | Tautological at specification level; implementation obligation is final epoch/time recheck. | Keep property-based and race tests. |
| Theorem 1 (`thm:admission`) | Every plaintext item returned by MemScope is authorized for the verified context at release. | Assumptions 1--4: identity/token authenticity, complete mediation, state/time integrity, ranker confinement. | Complete; expanded proof in Appendix A. | No imported theorem. | Domains defined; statement is API-level, not semantic privacy. Complete mediation is strong but explicit. | Validate assumptions in prototype. |
| Theorem 2 (`thm:derived`) | An admitted derived label is no more permissive than every parent label. | Nonempty parent set; atomic parent snapshot; deterministic proposed-label check; transitivity of product order. | Complete, main text and appendix. | No imported theorem. | Independent of semantic-verifier accuracy; truth is not claimed. | None. |
| Corollary 1 (`cor:expiry-inherit`) | Derived expiry is no later than every parent expiry, excluding separate declassification. | Theorem 2; expiry coordinate of meet. | Complete. | None. | Time domain consistent. Separate widening path clearly excluded. | None. |
| Theorem 3 (`thm:crossscope`) | An item unauthorized in context q2 is not returned as stored plaintext in q2, directly or via ordinary derivations. | Assumptions 1--4; finite acyclic provenance graph; no separate declassification. | Complete; induction/path argument in Appendix A. | No imported theorem. | Phrase deliberately says “returned-plaintext”; it does not cover inference or independently equivalent content. | Preserve wording in abstract/conclusion. |
| Theorem 4 (`thm:expiry`) | Once trusted time reaches item expiry, its plaintext is not returned even before physical compaction. | Authentic token; complete mediation; trusted monotonic time; final release check. | Complete, main text and appendix. | None. | Strict boundary is `tau < e_i`; units all in the same trusted time domain. | Test rollback and race countermodels. |
| Proposition 1 (`prop:complexity`) | Indexed retrieval costs index lookup plus O(c) authorization, O(cd) exact dense scoring, and O(c log k) heap selection; label storage scales with mean set sizes. | Hashed/bounded set membership; dense exact scoring; heap top-k; c candidates, d dimensions, k results. | Complete. | None. | Dependencies are explicit. It is not a measured latency or optimal bound. | Report real constants after implementation. |
| Lemma A.1 (`lem:path`) | Restrictiveness is monotone along every ordinary derivation path. | Theorem 2; acyclic finite DAG; transitive order. | Complete, appendix. | None. | No dimensional issue. | None. |
| Lemma A.2 (final-check freshness) | Expiry after filtering but before release prevents release under the expired snapshot. | Trusted monotonic time; final item/token check; restart/deny semantics. | Complete, appendix. | None. | Implementation must actually perform item expiry recheck, not only token check. | Add integration race test. |

## Audit conclusions

- Complete proofs: 10 results (counting four theorems, one proposition, one corollary, and four lemmas).
- Proof sketches: 0.
- Incomplete/conjectured theorems: 0.
- Empirical hypotheses are not stated as theorems.
- No use of “sharp,” “matching,” “optimal,” or “first” remains in a formal claim.
- The eviction heuristic explicitly lacks an approximation/optimality theorem.
