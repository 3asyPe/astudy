import datetime

from categories.models import Category

from django.core.validators import MaxValueValidator
from django.db import models

from ordered_model.models import OrderedModel

from .utils import get_course_upload_image_path


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
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name="content")
    sections_count = models.PositiveIntegerField(default=0)
    lectures_count = models.PositiveIntegerField(default=0)
    articles_count = models.PositiveIntegerField(default=0)
    resources_count = models.PositiveIntegerField(default=0)
    assignments_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.course.__str__()} | Content"


class CourseSection(OrderedModel):
    course_content = models.ForeignKey(CourseContent, on_delete=models.CASCADE, related_name="sections")
    order_with_respect_to = 'course_content'
    title = models.CharField(max_length=50)
    lectures_count = models.PositiveIntegerField(default=0)

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

    def __str__(self):
        return f"{self.course_section.__str__()} | Lecture - {self.title}"


class CourseLectureDurationTime(models.Model):
    course_lecture = models.OneToOneField(CourseLecture, on_delete=models.CASCADE, related_name="duration_time")
    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(60)])
    seconds = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(60)])

    def __str__(self):
        return f"{self.course_lecture.__str__()} | duration time"


class CourseSectionDurationTime(models.Model):
    course_section = models.OneToOneField(CourseSection, on_delete=models.CASCADE, related_name="duration_time")
    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(60)])

    def __str__(self):
        return f"{self.course_section.__str__()} | duration time"


class CourseDurationTime(models.Model):
    course_content = models.OneToOneField(CourseContent, on_delete=models.CASCADE, related_name="duration_time")
    hours = models.PositiveIntegerField(default=0)
    minutes = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(60)])

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
