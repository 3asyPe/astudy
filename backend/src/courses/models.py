import datetime
import logging

from categories.models import Category

from django.core.validators import MaxValueValidator
from django.db import models

from ordered_model.models import OrderedModel

from .utils import (
    get_course_upload_image_path,
    update_duration_time_hours_minutes,
    update_duration_time_hours_minutes_seconds,
)


logger = logging.getLogger(__name__)


class Course(models.Model):
    slug = models.SlugField(max_length=70, unique=True, blank=True)
    category = models.ForeignKey(Category, related_name="courses", on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to=get_course_upload_image_path)
    title = models.CharField(max_length=70)
    subtitle = models.CharField(max_length=150)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=39.99)
    description = models.TextField(max_length=5000)
    students_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class CourseContent(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE,related_name="content")
    sections_count = models.PositiveIntegerField(default=0)
    lectures_count = models.PositiveIntegerField(default=0)
    articles_count = models.PositiveIntegerField(default=0)
    resources_count = models.PositiveIntegerField(default=0)
    assignments_count = models.PositiveIntegerField(default=0)

    def recalculate_sections(self):
        self.sections_count = self.sections.all().count()
        self.save()

    def recalculate_lectures(self):
        lectures_count = 0
        for section in self.sections.all():
            lectures_count += section.lectures_count
        self.lectures_count = lectures_count
        self.save()

    def recalculate_duration_time(self):
        self.duration_time.recalculate()

    def __str__(self):
        return f"{self.course.__str__()} | Content"


class CourseSection(OrderedModel):
    course_content = models.ForeignKey(CourseContent, on_delete=models.CASCADE, related_name="sections")
    order_with_respect_to = 'course_content'
    title = models.CharField(max_length=50)
    lectures_count = models.PositiveIntegerField(default=0)

    def recalculate_lectures(self):
        self.lectures_count = self.lectures.all().count()
        self.save()

    def recalculate_duration_time(self):
        self.duration_time.recalculate()

    def __str__(self):
        return f"{self.course_content.__str__()} | Section - {self.title}"


class CourseLecture(OrderedModel):
    course_section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name="lectures")
    order_with_respect_to = "course_section"
    free_opened = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)
    students_finished_count = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def recalculate_duration_time(self):
        self.duration_time.recalculate()

    def __str__(self):
        return f"{self.course_section.__str__()} | Lecture - {self.title}"


class CourseLectureDurationTime(models.Model):
    course_lecture = models.OneToOneField(CourseLecture, on_delete=models.CASCADE, related_name="duration_time")
    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(60)])
    seconds = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(60)])

    def recalculate(self):
        pass

    def __str__(self):
        return f"{self.course_lecture.__str__()} | duration time"


class CourseSectionDurationTime(models.Model):
    course_section = models.OneToOneField(CourseSection, on_delete=models.CASCADE, related_name="duration_time")
    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(60)])

    def recalculate(self):
        lectures = self.course_section.lectures.all()
        duration_times = CourseLectureDurationTime.objects.filter(course_lecture__in=lectures)
        hours, minutes, seconds = 0, 0, 0
        for duration_time in duration_times:
            hours, minutes, seconds = update_duration_time_hours_minutes_seconds(
                hours, minutes, seconds, 
                duration_time.hours, duration_time.minutes, duration_time.seconds
            )
        self.hours, self.minutes = hours, minutes
        self.save()

    def __str__(self):
        return f"{self.course_section.__str__()} | duration time"


class CourseDurationTime(models.Model):
    course_content = models.OneToOneField(CourseContent, on_delete=models.CASCADE, related_name="duration_time")
    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(60)])

    def recalculate(self):
        sections = self.course_content.sections.all()
        duration_times = CourseSectionDurationTime.objects.filter(course_section__in=sections)
        hours, minutes = 0, 0
        for duration_time in duration_times:
            hours, minutes = update_duration_time_hours_minutes(hours, minutes, duration_time.hours, duration_time.minutes)
        self.hours, self.minutes = hours, minutes
        self.save()

    def __str__(self):
        return f"{self.course_content.__str__()} | duration time"


class CourseGoal(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="goals")
    goal = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course.__str__()} - {self.goal}"


class CourseRequirement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="requirements")
    requirement = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course.__str__()} - {self.requirement}"
