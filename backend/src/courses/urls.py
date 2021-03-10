from django.urls import path

from . import views


urlpatterns = [
    path('api/course/get/', views.get_course_info_api),
]
