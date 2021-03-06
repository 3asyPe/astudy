from django.urls import path

from . import views


urlpatterns = [
    path('api/category/get', views.get_category_api),
]
