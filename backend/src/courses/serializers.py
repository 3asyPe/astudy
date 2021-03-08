from rest_framework import serializers

from .models import (
    Course, 
    CourseDurationTime,
    CourseGoal,
    CourseRequirement,
)


class CourseDurationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseDurationTime
        fields = ["hours", "minutes"]


class CourseGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseGoal
        fields = ["goal"]


class CourseRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequirement
        fields = ["requirement"]


class CourseSerializer(serializers.ModelSerializer):
    duration_time = CourseDurationTimeSerializer()
    goals = CourseGoalSerializer(many=True)
    requirements = CourseRequirementSerializer(many=True)

    class Meta:
        model = Course
        fields = ["slug", "category", "image", "title", "subtitle", "price",
                  "description", "students_count", "lectures_count", "duration_time",
                  "goals", "requirements"]


class CategoryCourseSerializer(serializers.ModelSerializer):
    duration_time = CourseDurationTimeSerializer()

    class Meta:
        model = Course
        fields = ["slug", "image", "title", "subtitle", "price", "lectures_count",
                  "duration_time"]
