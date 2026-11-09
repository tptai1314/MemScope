"""MemScope Algorithm 2: conservative source-cited derived-memory admission."""

from __future__ import annotations

from typing import Callable, Optional, Sequence

from ..data.schemas import (
    AdmissionResult,
    DerivationProposal,
    ItemState,
    MemoryItem,
    Provenance,
    RetrievalToken,
)
from ..models.attribution import AttributionVerifier, ExtractiveAttributionVerifier
from .integrity import content_digest
from .policy import authorize, empty_required_scope, label_no_more_permissive, meet_labels
from .store import InMemoryStore
from .tokens import TokenError, TokenIssuer
from .writes import build_item


def admit_derivation(
    store: InMemoryStore,
    issuer: TokenIssuer,
    token: RetrievalToken,
    proposal: DerivationProposal,
    binder_caller: str,
    tool_chain: Sequence[Optional[str]],
    now: float,
    verifier: Optional[AttributionVerifier] = None,
) -> AdmissionResult:
    """Implement Algorithm 2 and Equation (9).

    Deterministic label checks establish non-widening. Attribution only decides
    admission versus quarantine and is never permitted to modify policy.
    """

    verifier = verifier or ExtractiveAttributionVerifier()
    if not proposal.parent_ids:
        return AdmissionResult("REJECT", None, "empty parent set")
    try:
        context = issuer.verify(
            token,
            binder_caller,
            tool_chain,
            now,
            store.policy_epoch,
            consume=True,
        )
    except TokenError:
        return AdmissionResult("REJECT", None, "invalid token or caller binding")

    epoch, parents = store.read_parents(proposal.parent_ids)
    if len(parents) != len(proposal.parent_ids):
        return AdmissionResult("REJECT", None, "one or more parents are missing")
    for parent in parents:
        if not authorize(parent, context, now, token.expires_at):
            return AdmissionResult("REJECT", None, "parent is not visible to derivation token")
        expected_version = proposal.expected_versions.get(parent.item_id, parent.version)
        expected_digest = proposal.expected_digests.get(parent.item_id, parent.integrity_digest)
        if parent.version != expected_version or parent.integrity_digest != expected_digest:
            return AdmissionResult("REJECT", None, "stale parent version or digest")

    try:
        meet = meet_labels([parent.label for parent in parents])
    except ValueError:
        return _commit_quarantine(
            store, issuer, token, proposal, parents, now, "empty temporal intersection"
        )
    if not label_no_more_permissive(proposal.proposed_label, meet):
        return AdmissionResult("REJECT", None, "proposed label is broader than parent meet")
    if empty_required_scope(meet):
        return _commit_quarantine(
            store, issuer, token, proposal, parents, now, "empty required scope intersection"
        )
    decision = verifier.verify(proposal.payload, parents, proposal.transformation)
    if decision.status != "supported":
        return _commit_quarantine(
            store,
            issuer,
            token,
            proposal,
            parents,
            now,
            "attribution %s: %s" % (decision.status, decision.reason),
        )
    if epoch != store.policy_epoch:
        return AdmissionResult("REJECT", None, "policy epoch changed during derivation")
    item = _derived_item(issuer, token, proposal, parents, now, ItemState.ADMITTED)
    store.commit(item)
    return AdmissionResult("ADMITTED", item, "deterministic and attribution checks passed")


def _derived_item(
    issuer: TokenIssuer,
    token: RetrievalToken,
    proposal: DerivationProposal,
    parents: Sequence[MemoryItem],
    now: float,
    state: ItemState,
) -> MemoryItem:
    provenance = Provenance(
        source_app=token.context.app_id,
        source_certificate_digest="reference-model",
        source_tool=token.context.tool_id,
        source_channel="derived",
        acquisition_token_digest=issuer.digest(token),
        created_at=now,
        parent_ids=tuple(parent.item_id for parent in parents),
        parent_digests=tuple(parent.integrity_digest for parent in parents),
        transformation=proposal.transformation,
        content_digest=content_digest(proposal.payload),
    )
    return build_item(
        proposal.item_id,
        proposal.payload,
        proposal.proposed_label,
        provenance,
        state=state,
    )


def _commit_quarantine(
    store: InMemoryStore,
    issuer: TokenIssuer,
    token: RetrievalToken,
    proposal: DerivationProposal,
    parents: Sequence[MemoryItem],
    now: float,
    reason: str,
) -> AdmissionResult:
    item = _derived_item(
        issuer, token, proposal, parents, now, ItemState.QUARANTINED
    )
    store.commit(item)
    return AdmissionResult("QUARANTINED", item, reason)
