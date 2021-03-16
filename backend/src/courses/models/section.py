from django.core.validators import MaxValueValidator
from django.db import models

from courses.models import CourseContent, CourseLectureDurationTime
from courses.utils import update_duration_time_hours_minutes_seconds


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
