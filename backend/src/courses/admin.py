from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

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


class CourseSectionAdmin(OrderedModelAdmin):
    list_display = ('__str__', 'move_up_down_links')


class CourseLecturesAdmin(OrderedModelAdmin):
    list_display = ('__str__', 'move_up_down_links')


admin.site.register(Course)
admin.site.register(CourseContent)
admin.site.register(CourseDurationTime)
admin.site.register(CourseGoal)
admin.site.register(CourseLecture, CourseLecturesAdmin)
admin.site.register(CourseLectureDurationTime)
admin.site.register(CourseRequirement)
admin.site.register(CourseSection, CourseSectionAdmin)
admin.site.register(CourseSectionDurationTime)
