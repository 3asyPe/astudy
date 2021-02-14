from django.urls import path

from rest_framework.authtoken import views as rest_views


urlpatterns = [
    path('api/auth/', rest_views.obtain_auth_token),
]
