import logging

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from carts.serializers import (
    CartSerializer, 
    CartOnlyInfoSerializer,
    WishlistSerializer, 
    SavedForLaterSerializer,
)
from carts.services import (
    CartToolkit, 
    CartListsToolkit,
    CartListsSelector,
    WishlistToolkit, 
    SavedForLaterToolkit,
)
from carts.utils import CartErrorMessages


logger = logging.getLogger(__name__)


@api_view(["GET"])
def load_cart_api(request, *args, **kwargs):
    user = request.user
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart_lists = CartListsSelector.get_cart_lists_by_user_and_ids(user=request.user, ids=ids)
    cart = cart_lists["cart"]
    serializer = CartSerializer(instance=cart)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def load_wishlist_api(request, *args, **kwargs):
    user = request.user
    wishlist = WishlistToolkit.load_wishlist(user=user)
    serializer = WishlistSerializer(instance=wishlist)
    return Response(serializer.data, status=200)


@api_view(["GET"])
def load_saved_for_later_api(request, *args, **kwargs):
    data = request.GET
    saved_for_later_id = int(data.get("saved_for_later_id")) if data.get("saved_for_later_id") is not None else None
    user = request.user
    saved_for_later = SavedForLaterToolkit.load_saved_for_later(user=user, saved_for_later_id=saved_for_later_id)
    serializer = SavedForLaterSerializer(instance=saved_for_later)
    return Response(serializer.data, status=200)


@api_view(["GET"])
def get_cart_info_api(request, *args, **kwargs):
    user = request.user
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart = CartToolkit.load_cart(user=user, cart_id=ids["cart_id"])
    serializer = CartOnlyInfoSerializer(instance=cart)
    return Response(serializer.data, status=400)


@api_view(["POST"])
def add_course_to_cart_api(request, *args, **kwargs):
    try:
        course_slug = request.POST["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    user = request.user
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart_lists = CartListsSelector.get_cart_lists_by_user_and_ids(user=request.user, ids=ids)

    cart = CartToolkit.add_course_to_cart(cart=cart_lists["cart"], course_slug=course_slug)
    CartListsToolkit.delete_duplicates_excluding_instance(course_slug=course_slug, instance=cart, **cart_lists)

    serializer = CartOnlyInfoSerializer(instance=cart)
    return Response(serializer.data, status=200)


@api_view(["POST"])
def add_course_to_wishlist_api(request, *args, **kwargs):
    try:
        course_slug = request.POST["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)

    user = request.user
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart_lists = CartListsSelector.get_cart_lists_by_user_and_ids(user=request.user, ids=ids)

    wishlist = WishlistToolkit.add_course_to_wishlist(wishlist=cart_lists["wishlist"], course_slug=course_slug)
    CartListsToolkit.delete_duplicates_excluding_instance(course_slug=course_slug, instance=wishlist, **cart_lists)

    serializer = CartOnlyInfoSerializer(instance=cart_lists["cart"])
    return Response(serializer.data, status=200)


@api_view(["POST"])
def add_course_to_saved_for_later_api(request, *args, **kwargs):
    try:
        course_slug = request.POST["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)

    user = request.user
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart_lists = CartListsSelector.get_cart_lists_by_user_and_ids(user=request.user, ids=ids)

    saved_for_later = SavedForLaterToolkit.add_course_to_saved_for_later(s_list=cart_lists["saved_for_later"], course_slug=course_slug)
    CartListsToolkit.delete_duplicates_excluding_instance(course_slug=course_slug, instance=saved_for_later, **cart_lists)

    serializer = CartOnlyInfoSerializer(instance=cart_lists["cart"])
    return Response(serializer.data, status=200)


@api_view(["POST"])
def remove_course_from_cart_api(request, *args, **kwargs):
    try:
        course_slug = request.POST["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    user = request.user
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart_lists = CartListsSelector.get_cart_lists_by_user_and_ids(user=request.user, ids=ids)

    CartToolkit.remove_course_from_cart(cart=cart_lists["cart"], course_slug=course_slug)

    serializer = CartOnlyInfoSerializer(instance=cart_lists["cart"])
    return Response(serializer.data, status=200)


@api_view(["POST"])
def remove_course_from_wishlist(request, *args, **kwargs):
    try:
        course_slug = request.POST["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)

    user = request.user
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart_lists = CartListsSelector.get_cart_lists_by_user_and_ids(user=request.user, ids=ids)

    WishlistToolkit.remove_course_from_wishlist(wishlist=cart_lists["wishlist"], course_slug=course_slug)

    return Response({}, status=200)


@api_view(["POST"])
def remove_course_from_saved_for_later(request, *args, **kwargs):
    try:
        course_slug = request.POST["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    user = request.user
    ids = CartListsToolkit.get_cart_lists_ids_from_request(request)
    cart_lists = CartListsSelector.get_cart_lists_by_user_and_ids(user=request.user, ids=ids)

    SavedForLaterToolkit.remove_course_from_saved_for_later(s_list=cart_lists["saved_for_later"], course_slug=course_slug)

    return Response({}, status=200)


@api_view(["GET"])
def get_cart_courses_count_api(request, *args, **kwargs):
    data = request.GET
    cart_id = int(data.get("cart_id")) if data.get("cart_id") is not None else None
    user = request.user
    cart = CartToolkit.load_cart(user=user, cart_id=cart_id)
    return Response({
        "cart_courses_count": cart.get_courses_count(), 
        "cart_id": cart.id,
    }, status=200)


@api_view(["GET"])
def check_on_course_already_in_cart_api(request, *args, **kwargs):
    try:
        data = request.GET
        cart_id = int(data.get("cart_id")) if data.get("cart_id") is not None else None
        course_slug = data["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)
    
    user = request.user
    cart = CartToolkit.load_cart(user=user, cart_id=cart_id)
    course_already_in_cart = CartToolkit.check_on_course_in_cart(cart=cart, course_slug=course_slug)
    return Response({"course_already_in_cart": course_already_in_cart}, status=200)


@api_view(["GET"])
def check_on_course_already_in_wishlist_api(request, *args, **kwargs):
    try:
        data = request.GET
        course_slug = data["course_slug"]
    except KeyError:
        logger.error("Request object doesn't have a slug field")
        return Response({"error": CartErrorMessages.REQUEST_FIELDS_ERROR.value}, status=400)

    user = request.user
    wishlist = WishlistToolkit.load_wishlist(user=user)
    course_already_in_wishlist = WishlistToolkit.check_on_course_in_wishlist(wishlist=wishlist, course_slug=course_slug)
    return Response({"course_already_in_wishlist": course_already_in_wishlist}, status=200)
