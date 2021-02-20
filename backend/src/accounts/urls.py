from django.urls import path

from . import views


urlpatterns = [
    path('api/auth/', views.token_auth_api),
    path('api/registration/', views.create_account_api),
]
