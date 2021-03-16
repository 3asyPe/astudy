from django.core.validators import MaxValueValidator
from django.db import models

from courses.models import CourseSection


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
