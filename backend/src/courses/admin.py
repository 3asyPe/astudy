from django.contrib import admin

from .models import (
    Course, 
    CourseDurationTime,
    CourseGoal,
    CourseRequirement,
)


admin.site.register(Course)
admin.site.register(CourseDurationTime)
admin.site.register(CourseGoal)
admin.site.register(CourseRequirement)
