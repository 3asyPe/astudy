import logging

from rest_framework import serializers

from .models import (
    Course, 
    CourseContent,
    CourseDurationTime,
    CourseGoal,
    CourseLecture,
    CourseLectureDurationTime,
    CourseRequirement,
    CourseSection,
    CourseSectionDurationTime,
)
from.selectors import get_course_duration_time_by_course


logger = logging.getLogger(__name__)


class CourseLectureDurationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLectureDurationTime
        fields = ["hours", "minutes"]


class CourseSectionDurationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSectionDurationTime
        fields = ["hours", "minutes"]


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


class CourseContentSerializer(serializers.ModelSerializer):
    duration_time = CourseDurationTime()

    class Meta:
        model = CourseContent
        fields = ["sections_count", "lectures_count", "articles_count", "resources_count", "assignments_count"]


class CourseSerializer(serializers.ModelSerializer):
    content = CourseContentSerializer()
    goals = CourseGoalSerializer(many=True)
    requirements = CourseRequirementSerializer(many=True)

    class Meta:
        model = Course
        fields = ["slug", "category", "image", "title", "subtitle", "price",
                  "description", "students_count", "lectures_count", "goals", "requirements",
                  "content"]

    def get_duration_time(self, obj):
        try:
            duration_time = get_course_duration_time_by_course(course=obj)
        except CourseContent.DoesNotExist:
            logger.warning("Course content doesn't exist so duration time won't be set to serialized course object")
            return None
        except CourseDurationTime:
            logger.warning("Course duration time doesn't exist and won't be set to serialized course object")
            return None


class CourseSectionSerializer(serializers.ModelSerializer):
    duration_time = CourseSectionDurationTimeSerializer()

    class Meta:
        model = CourseSection
        fields = ["title", "lectures_count", "duration_time"]


class CourseLectureSerializer(serializers.ModelSerializer):
    duration_time = CourseLectureDurationTimeSerializer()

    class Meta:
        model = CourseLecture
        fields = ["free_opened", "title", "description", "students_finished_count"]



class CategoryCourseSerializer(serializers.ModelSerializer):
    duration_time = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ["slug", "image", "title", "subtitle", "price", "lectures_count",
                  "duration_time"]

    def get_duration_time(self, obj):
        try:
            duration_time = get_course_duration_time_by_course(course=obj)
        except CourseContent.DoesNotExist:
            logger.warning("Course content doesn't exist so duration time won't be set to serialized course object")
            return None
        except CourseDurationTime:
            logger.warning("Course duration time doesn't exist and won't be set to serialized course object")
            return None
