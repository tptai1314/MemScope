from dataclasses import replace

import pytest

from memscope.methods.retrieval import MemScopeService, RetrievalDenied
from memscope.models.ranking import LexicalRanker

from conftest import make_context, make_item, make_label


def test_filtering_precedes_ranking(store, issuer) -> None:
    allowed = make_item("allowed", "shopping preference blue", label=make_label(purposes=("ads",), tools=("ads",)))
    secret = make_item("secret", "allergy allergy allergy", label=make_label(purposes=("health",), tools=("health",)))
    store.commit(allowed)
    store.commit(secret)
    context = make_context(purpose="ads", tool="ads")
    token = issuer.issue(context, 30.0, store.policy_epoch)
    service = MemScopeService(store, issuer, clock=lambda: 20.0)
    result = service.retrieve(token, "allergy blue", 1, "assistant.pkg", ("ads",))
    assert [item.item_id for item in result.items] == ["allowed"]
    assert result.candidate_count == 1


def test_expired_item_never_returned(store, issuer) -> None:
    store.commit(make_item(label=make_label(expires_at=19.0)))
    context = make_context()
    token = issuer.issue(context, 30.0, store.policy_epoch)
    result = MemScopeService(store, issuer, clock=lambda: 20.0).retrieve(
        token, "calendar", 5, "assistant.pkg", ("calendar.read",)
    )
    assert result.items == ()


def test_integrity_tampering_excludes_item(store, issuer) -> None:
    item = make_item()
    item.payload = "tampered"
    store.commit(item)
    token = issuer.issue(make_context(), 30.0, store.policy_epoch)
    result = MemScopeService(store, issuer, clock=lambda: 20.0).retrieve(
        token, "tampered", 5, "assistant.pkg", ("calendar.read",)
    )
    assert result.items == ()


def test_stale_epoch_denied(store, issuer) -> None:
    token = issuer.issue(make_context(), 30.0, store.policy_epoch)
    store.increment_epoch()
    with pytest.raises(RetrievalDenied):
        MemScopeService(store, issuer, clock=lambda: 20.0).retrieve(
            token, "calendar", 1, "assistant.pkg", ("calendar.read",)
        )
