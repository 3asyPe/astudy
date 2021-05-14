import pytest

from app.errors import ValidationError
from discounts.utils import DiscountErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def apply_coupon(api, **kwargs):
    return lambda **kwargs: api.post(
        "/api/coupon/apply/", {
            **kwargs,
        },
        format='multipart',
        expected_status_code=kwargs.pop("expected_status_code", 200),
    )


def test_apply_coupon_api(apply_coupon, cart, wishlist, saved_for_later, small_coupon):
    small_coupon.applicable_to.add(cart.courses.first())
    response = apply_coupon(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        coupon_code=small_coupon.code
    )

    cart.refresh_from_db()

    assert response["id"] == cart.id
    assert float(response["subtotal"]) == float(cart.subtotal) == float(cart.courses.first().price)
    assert float(response["total"]) == float(cart.total) == round(float(cart.courses.first().price) * 0.9, 2)
    assert response["wishlist_discounts"] == []
    assert response["saved_for_later_discounts"] == []
    assert "cart_discounts" in response


def test_apply_coupon_discount_serializers(apply_coupon, cart, wishlist, saved_for_later, small_coupon):
    small_coupon.applicable_to.add(cart.courses.first())
    small_coupon.applicable_to.add(wishlist.courses.first())
    small_coupon.applicable_to.add(saved_for_later.courses.first())

    response = apply_coupon(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        coupon_code=small_coupon.code
    )

    for item, name in zip([cart, wishlist, saved_for_later], ["cart", "wishlist", "saved_for_later"]):
        item.refresh_from_db()

        course = item.courses.first()
        discount = response[f"{name}_discounts"][0]

        assert discount["course_slug"] == course.slug
        assert float(discount["new_price"]) == round(float(course.price) * 0.9, 2)
        assert discount["applied_coupon"] == small_coupon.code


def test_apply_coupon_api_call_methods(mocker, apply_coupon, cart, wishlist, saved_for_later, small_coupon):
    apply_coupon_method = mocker.patch("discounts.services.CouponToolkit.apply_coupon")

    response = apply_coupon(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        coupon_code=small_coupon.code
    )

    apply_coupon_method.assert_called_with(code=small_coupon.code, cart=cart)


def test_apply_wrong_coupon(apply_coupon, cart, wishlist, saved_for_later):
    response = apply_coupon(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        coupon_code="WRONGCODE",
        expected_status_code=400
    )

    assert response["error"] == DiscountErrorMessages.INVALID_APPLIED_COUPON_ERROR.value


def test_apply_coupon_api_without_coupon_field(apply_coupon, cart, wishlist, saved_for_later):
    response = apply_coupon(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        expected_status_code=400
    )

    assert response["error"] == DiscountErrorMessages.REQUEST_FIELDS_ERROR.value
