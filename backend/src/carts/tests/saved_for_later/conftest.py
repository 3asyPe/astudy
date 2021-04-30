import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def saved_for_later(mixer, user):
    return mixer.blend("carts.SavedForLater", user=user)
