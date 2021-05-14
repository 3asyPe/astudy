import pytest

from carts.models import Wishlist


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def cart(cart, api, course_factory):
    cart.user = api.user
    cart.save()
    cart.courses.add(course_factory())
    return cart


@pytest.fixture
def wishlist(cart, course_factory):
    user = cart.user
    wishlist = Wishlist.objects.get_or_create(user=user)[0]
    wishlist.courses.add(course_factory())
    return wishlist


@pytest.fixture
def saved_for_later(saved_for_later, api, course_factory):
    saved_for_later.user = api.user
    saved_for_later.save()
    saved_for_later.courses.add(course_factory())
    return saved_for_later
