from django.urls import path

from accounts.api import views


urlpatterns = [
    path('api/auth/', views.token_auth_api),
    path('api/registration/', views.create_account_api),
    path('api/auth/test/', views.test_authentication),
]
