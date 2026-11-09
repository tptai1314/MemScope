from memscope.data.schemas import DerivationProposal, ItemState, Sensitivity
from memscope.methods.derivation import admit_derivation
from memscope.models.attribution import AlwaysAcceptVerifier

from conftest import make_context, make_item, make_label


def _setup(store, issuer):
    label1 = make_label(
        purposes=("scheduling", "health"),
        tools=("shared",),
        sensitivity=Sensitivity.SENSITIVE,
        expires_at=80,
    )
    label2 = make_label(
        purposes=("scheduling",), tools=("shared",), sensitivity=Sensitivity.HEALTH_SENSITIVE, expires_at=70
    )
    p1 = make_item("p1", "Riverside Clinic", label=label1)
    p2 = make_item("p2", "Tuesday 10 AM", label=label2)
    store.commit(p1)
    store.commit(p2)
    context = make_context(tool="shared")
    token = issuer.issue(context, 50.0, store.policy_epoch)
    return p1, p2, token, label2


def test_admitted_derivation_is_no_broader(store, issuer) -> None:
    p1, p2, token, meet_label = _setup(store, issuer)
    proposal = DerivationProposal(
        "d1",
        "Tuesday 10 AM",
        ("p1", "p2"),
        meet_label,
        "extractive",
        {"p1": 1, "p2": 1},
        {"p1": p1.integrity_digest, "p2": p2.integrity_digest},
    )
    result = admit_derivation(store, issuer, token, proposal, "assistant.pkg", ("shared",), 20.0)
    assert result.status == "ADMITTED"
    assert result.item is not None and result.item.state == ItemState.ADMITTED
    assert result.item.label.sensitivity == Sensitivity.HEALTH_SENSITIVE


def test_broadened_derivation_rejected(store, issuer) -> None:
    p1, p2, token, meet_label = _setup(store, issuer)
    broad = make_label(purposes=("scheduling", "ads"), tools=("shared",), expires_at=70)
    proposal = DerivationProposal("d2", "Tuesday 10 AM", ("p1", "p2"), broad, "extractive")
    result = admit_derivation(store, issuer, token, proposal, "assistant.pkg", ("shared",), 20.0)
    assert result.status == "REJECT"
    assert "broader" in result.reason


def test_unsupported_abstraction_quarantined(store, issuer) -> None:
    p1, p2, token, meet_label = _setup(store, issuer)
    proposal = DerivationProposal("d3", "invented diagnosis", ("p1", "p2"), meet_label, "abstractive")
    result = admit_derivation(store, issuer, token, proposal, "assistant.pkg", ("shared",), 20.0)
    assert result.status == "QUARANTINED"
    assert result.item is not None and result.item.state == ItemState.QUARANTINED
