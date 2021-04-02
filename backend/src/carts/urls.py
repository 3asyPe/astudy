from django.urls import path

from . import views


urlpatterns = [
    path('api/cart/get/', views.load_cart_api),
    path('api/cart/add/', views.add_course_to_cart_api),
    path('api/cart/remove/', views.remove_course_from_cart_api),
    path('api/cart/count/', views.get_cart_courses_count_api),
    path('api/cart/checkalreadyin/', views.check_on_course_already_in_cart_api),
    path('api/cart/info/', views.get_cart_info_api),

    path('api/wishlist/get/', views.load_wishlist_api),
    path('api/wishlist/add/', views.add_course_to_wishlist_api),
    path('api/wishlist/remove/', views.remove_course_from_wishlist),
    path('api/wishlist/checkalreadyin/', views.check_on_course_already_in_wishlist_api),

    path('api/savedforlater/get/', views.load_saved_for_later_api),
    path('api/savedforlater/add/', views.add_course_to_saved_for_later_api),
    path('api/savedforlater/remove/', views.remove_course_from_saved_for_later),
]
