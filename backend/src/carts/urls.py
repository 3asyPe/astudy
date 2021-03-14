from django.urls import path

from . import views


urlpatterns = [
    path('api/cart/get/', views.load_cart_api),
    path('api/cart/add/', views.add_course_to_cart_api),
    path('api/auth/remove/', views.remove_course_from_cart_api),
    path('api/cart/count/', views.get_cart_courses_count_api),
]
