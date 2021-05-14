import pytest


from discounts.utils import DiscountErrorMessages


pytestmark = [pytest.mark.django_db]


@pytest.fixture
def remove_coupon(api, **kwargs):
    return lambda **kwargs: api.post(
        "/api/coupon/cancel/", {
            **kwargs
        },
        format="multipart",
        expected_status_code=kwargs.pop("expected_status_code", 200)
    )


@pytest.fixture
def cart(mixer, cart, small_coupon, big_coupon):
    small = mixer.blend("discounts.AppliedCoupon", coupon=small_coupon, cart=cart)
    big = mixer.blend("discounts.AppliedCoupon", coupon=big_coupon, cart=cart)
    return cart


def test_remove_applied_coupon_api(remove_coupon, cart, wishlist, saved_for_later, small_coupon, big_coupon):
    small_coupon.applicable_to.add(cart.courses.first())
    small_coupon.applicable_to.add(wishlist.courses.first())
    big_coupon.applicable_to.add(saved_for_later.courses.first())

    response = remove_coupon(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        coupon_code=small_coupon.code
    )

    cart.refresh_from_db()

    assert response["id"] == cart.id
    assert float(response["subtotal"]) == float(response["total"]) == float(cart.total) == float(cart.subtotal) == float(cart.courses.first().price)
    assert response["wishlist_discounts"] == []
    assert response["cart_discounts"] == []
    assert "saved_for_later_discounts" in response


def test_remove_applied_coupon_api_discounts_serializers(remove_coupon, cart, wishlist, saved_for_later, small_coupon, big_coupon):
    small_coupon.applicable_to.add(cart.courses.first())
    small_coupon.applicable_to.add(wishlist.courses.first())
    small_coupon.applicable_to.add(saved_for_later.courses.first())
    big_coupon.applicable_to.add(saved_for_later.courses.first())

    response = remove_coupon(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        coupon_code=big_coupon.code
    )

    cart.refresh_from_db()

    
    for item, name in zip([cart, wishlist, saved_for_later], ["cart", "wishlist", "saved_for_later"]):
        item.refresh_from_db()

        course = item.courses.first()
        discount = response[f"{name}_discounts"][0]

        assert discount["course_slug"] == course.slug
        assert float(discount["new_price"]) == round(float(course.price) * 0.9, 2)
        assert discount["applied_coupon"] == small_coupon.code


def test_remove_applied_coupon_api_call_methods(mocker, remove_coupon, cart, wishlist, saved_for_later, small_coupon):
    remove_coupon_method = mocker.patch("discounts.services.CouponToolkit.remove_applied_coupon")

    response = remove_coupon(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        coupon_code=small_coupon.code
    )

    remove_coupon_method.assert_called_with(code=small_coupon.code, cart=cart)


def test_remove_wrong_coupon(remove_coupon, cart, wishlist, saved_for_later):
    response = remove_coupon(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        coupon_code="WRONGCODE",
    )

    assert response['id'] == cart.id
    assert "subtotal" in response
    assert "total" in response
    assert "wishlist_discounts" in response
    assert "cart_discounts" in response
    assert "saved_for_later_discounts" in response


def test_remove_coupon_api_without_coupon_field(remove_coupon, cart, wishlist, saved_for_later):
    response = remove_coupon(
        cart_id=cart.id,
        saved_for_later_id=saved_for_later.id,
        expected_status_code=400
    )

    assert response["error"] == DiscountErrorMessages.REQUEST_FIELDS_ERROR.value
    