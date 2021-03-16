from django.db import models

from categories.models import Category
from courses.utils import get_course_upload_image_path


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
