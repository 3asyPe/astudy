import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def card(mixer, billing_profile):
    obj = mixer.blend("billing.Card", billing_profile=billing_profile, default=False)
    return obj


@pytest.fixture
def default_card(mixer, billing_profile):
    obj = mixer.blend("billing.Card", billing_profile=billing_profile, default=True)
    return obj


def test_card_set_as_default(card, default_card):
    card.set_as_default()

    card.refresh_from_db()
    default_card.refresh_from_db()

    assert card.default == True
    assert default_card.default == False
