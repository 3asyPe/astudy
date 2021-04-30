import pytest


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def saved_for_later(mixer, user):
    return mixer.blend("carts.SavedForLater", user=user)


@pytest.fixture
def another_saved_for_later(mixer, another_user):
    return mixer.blend("carts.SavedForLater", user=another_user)


@pytest.fixture
def saved_for_later_without_user(mixer):
    return mixer.blend("carts.SavedForLater", user=None)
