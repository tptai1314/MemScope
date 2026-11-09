import random

from memscope.data.schemas import Sensitivity
from memscope.methods.policy import label_no_more_permissive, meet_labels

from conftest import make_label


def test_meet_monotonicity_property() -> None:
    rng = random.Random(123)
    universe = ["a", "b", "c", "d"]
    for _ in range(100):
        labels = []
        for _parent in range(rng.randint(1, 5)):
            purposes = tuple(x for x in universe if rng.random() < 0.7) or ("a",)
            apps = tuple(x for x in universe if rng.random() < 0.7) or ("a",)
            tools = tuple(x for x in universe if rng.random() < 0.7) or ("a",)
            consumers = tuple(x for x in universe if rng.random() < 0.7) or ("a",)
            labels.append(
                make_label(
                    purposes=purposes,
                    apps=apps,
                    tools=tools,
                    consumers=consumers,
                    sensitivity=Sensitivity(rng.randrange(4)),
                    not_before=rng.uniform(0, 10),
                    expires_at=rng.uniform(20, 40),
                )
            )
        meet = meet_labels(labels)
        assert all(label_no_more_permissive(meet, parent) for parent in labels)
