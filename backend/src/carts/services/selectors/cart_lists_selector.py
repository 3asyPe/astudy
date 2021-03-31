from django.conf import settings

from carts.services import CartToolkit, WishlistToolkit, SavedForLaterToolkit


User = settings.AUTH_USER_MODEL


class CartListsSelector:
    @classmethod
    def get_cart_lists_by_user_and_ids(cls, user: User, ids: dict, *args, **kwargs) -> dict:
        cart = CartToolkit.load_cart(user=user, cart_id=ids["cart_id"])
        saved_for_later = SavedForLaterToolkit.load_saved_for_later(user=user, saved_for_later_id=ids["saved_for_later_id"])
        if user.is_authenticated:
            wishlist = WishlistToolkit.load_wishlist(user=user)
        else:
            wishlist = None
        return {
            "cart": cart,
            "saved_for_later": saved_for_later,
            "wishlist": wishlist,
        }
