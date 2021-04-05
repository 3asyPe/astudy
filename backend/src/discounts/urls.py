from django.urls import path

from . import views


urlpatterns = [
    path('api/coupon/apply/', views.apply_coupon_api),
    path('api/coupon/cancel/', views.remove_applied_coupon_api),    
]
