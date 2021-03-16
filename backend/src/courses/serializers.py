import logging

from rest_framework import serializers

from courses.models import (
    Course, 
    CourseContent, 
    CourseDurationTime, 
    CourseGoal,
    CourseLecture, 
    CourseLectureDurationTime,
    CourseRequirement, 
    CourseSection,
    CourseSectionDurationTime
)
from courses.services import CourseSelector


logger = logging.getLogger(__name__)


class CourseLectureDurationTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLectureDurationTime
        fields = ["hours", "minutes", "seconds"]


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


class CourseLectureSerializer(serializers.ModelSerializer):
    duration_time = CourseLectureDurationTimeSerializer()

    class Meta:
        model = CourseLecture
        fields = ["free_opened", "title", "description", "duration_time"]


class CourseSectionSerializer(serializers.ModelSerializer):
    lectures = CourseLectureSerializer(many=True)
    duration_time = CourseSectionDurationTimeSerializer()

    class Meta:
        model = CourseSection
        fields = ["title", "lectures_count", "duration_time", "lectures"]


class CourseContentSerializer(serializers.ModelSerializer):
    sections = CourseSectionSerializer(many=True)
    duration_time = CourseDurationTimeSerializer()

    class Meta:
        model = CourseContent
        fields = ["sections_count", "lectures_count", "articles_count", "resources_count", "assignments_count", "sections",
                  "duration_time"]


class CourseSerializer(serializers.ModelSerializer):
    """ Contains full information for the first page of the course
        without any real lecture content like video/article/assignment
    """
    content = CourseContentSerializer()
    goals = CourseGoalSerializer(many=True)
    requirements = CourseRequirementSerializer(many=True)

    class Meta:
        model = Course
        fields = [
            "slug", 
            "category", 
            "image", 
            "title", 
            "subtitle", 
            "price",
            "description", 
            "students_count", 
            "goals", 
            "requirements",
            "content"
        ]


class CategoryCourseSerializer(serializers.ModelSerializer):
    duration_time = serializers.SerializerMethodField()
    lectures_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "slug", 
            "image", 
            "title", 
            "subtitle", 
            "price", 
            "lectures_count",
            "duration_time"
        ]

    def get_duration_time(self, obj):
        try:
            return CourseDurationTimeSerializer(
                CourseSelector.get_course_duration_time_by_course(course=obj)
            ).data
        except CourseContent.DoesNotExist:
            logger.warning("Course content doesn't exist so duration time won't be set to serialized course object")
        except CourseDurationTime.DoesNotExist:
            logger.warning("Course duration time doesn't exist and won't be set to serialized course object")
        return None

    def get_lectures_count(self, obj):
        try:
            return CourseSelector.get_course_lectures_count_by_course(course=obj)
        except CourseContent.DoesNotExist:
            logger.warning("Course content doesn't exist so lectures count field won't be set to serialized course object")
        return None


class CartCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = [
            "slug", 
            "image", 
            "title", 
            "subtitle", 
            "price",
        ]