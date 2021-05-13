import datetime
import pytest

from django.utils import timezone

from app.errors import ValidationError
from discounts.services import CouponCreator
from discounts.utils import DiscountErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def applicable_to(course_factory):
    applicable_to = []
    applicable_to.append(course_factory())
    applicable_to.append(course_factory())
    return applicable_to


def test_create_valid_coupon(user, applicable_to):
    expires = timezone.now() + datetime.timedelta(days=5)
    coupon = CouponCreator(
        creator=user,
        code="TESTCODE",
        applicable_to=applicable_to,
        discount=10,
        expires=expires,
    )()

    assert coupon.creator == user
    assert coupon.code == "TESTCODE"
    assert list(coupon.applicable_to.all()) == applicable_to
    assert coupon.discount == 10
    assert coupon.expires == expires
    assert coupon.active == True


@pytest.mark.parametrize("code", [
    "",
    None,
    "SOMEREALLYREALLYLONGCOUPON"
])
def test_create_coupon_with_wrong_code(user, applicable_to, code):
    expires = timezone.now() + datetime.timedelta(days=5)
    with pytest.raises(ValidationError) as exc:
        coupon = CouponCreator(
            creator=user,
            code=code,
            applicable_to=applicable_to,
            discount=10,
            expires=expires
        )()

    assert str(exc.value) == DiscountErrorMessages.INVALID_COUPON_INITIALIZATION_DATA_ERROR.value
    

def test_create_coupon_with_anonymous_user(anonymous_user, applicable_to):
    expires = timezone.now() + datetime.timedelta(days=5)
    with pytest.raises(ValidationError) as exc:
        coupon = CouponCreator(
            creator=anonymous_user,
            code="TESTCODE",
            applicable_to=applicable_to,
            discount=10,
            expires=expires
        )()

    assert str(exc.value) == DiscountErrorMessages.INVALID_COUPON_INITIALIZATION_DATA_ERROR.value


def test_create_coupon_with_expired_limit_date(user, applicable_to):
    expires = timezone.now() - datetime.timedelta(days=1)
    with pytest.raises(ValidationError) as exc:
        coupon = CouponCreator(
            creator=user,
            code="TESTCODE",
            applicable_to=applicable_to,
            discount=10,
            expires=expires
        )()
    
    assert str(exc.value) == DiscountErrorMessages.INVALID_COUPON_INITIALIZATION_DATA_ERROR.value


@pytest.mark.parametrize("discount", [-10, 0, 100, 150])
def test_create_coupon_with_wrong_discount_number(user, applicable_to, discount):
    expires = timezone.now() + datetime.timedelta(days=5)
    with pytest.raises(ValidationError) as exc:
        coupon = CouponCreator(
            creator=user,
            code="TESTCODE",
            applicable_to=applicable_to,
            discount=discount,
            expires=expires
        )()

    assert str(exc.value) == DiscountErrorMessages.INVALID_COUPON_INITIALIZATION_DATA_ERROR.value


def test_create_already_coupon_with_already_existing_code(user, applicable_to, coupon):
    expires = timezone.now() + datetime.timedelta(days=5)
    with pytest.raises(ValidationError) as exc:
        new_coupon = CouponCreator(
            creator=user,
            code=coupon.code,
            applicable_to=applicable_to,
            discount=10,
            expires=expires
        )()

    assert str(exc.value) == DiscountErrorMessages.INVALID_COUPON_INITIALIZATION_DATA_ERROR.value