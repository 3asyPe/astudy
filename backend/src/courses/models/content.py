from django.core.validators import MaxValueValidator
from django.db import models

from courses.models import Course, CourseSectionDurationTime
from courses.utils import update_duration_time_hours_minutes


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
