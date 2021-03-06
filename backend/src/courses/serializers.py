from rest_framework import serializers

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["slug", "category", "image", "title", "subtitle", "price",
                  "description", "students_count", "lections_count", "duration_time"]


class CategoryCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["slug", "image", "title", "subtitle", "price", "lections_count",
                  "duration_time"]
