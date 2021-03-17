from django.contrib import admin
from django.utils.html import format_html

from ordered_model.admin import OrderedModelAdmin

from courses.models import CourseSection, CourseLecture


class CourseLectureInline(admin.TabularInline):
    model = CourseLecture
    show_change_link = True
    fields = [
        "title",
        "_duration_time",
        "students_finished_count",
        "free_opened"
    ]
    readonly_fields = [
        "_duration_time",
        "students_finished_count",
    ]
    extra = 0

    def _duration_time(self, obj):
        duration_time = obj.duration_time
        return f"{duration_time.hours:02d}:{duration_time.minutes:02d}:{duration_time.seconds:02d}"

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(CourseSection)
class CourseSectionAdmin(OrderedModelAdmin):
    list_display = [
        'id',
        'title', 
        'course',
        'course_image_tag',
        'order_in_course',
        'move_up_down_links',
    ]

    list_display_links = [
        'id',
        'title',
        'course',
        'course_image_tag',
    ]

    list_filter = [
        'course_content__course',
    ]

    readonly_fields = [
        "lectures_count",
        "_duration_time",
    ]

    inlines = [
        CourseLectureInline
    ]

    def course_image_tag(self, obj):
        course = obj.course_content.course
        return format_html(f'<img src="{course.image.url}" width="100px" height="56.25px"/>')

    def course(self, obj):
        return obj.course_content.course.title

    def order_in_course(self, obj):
        return obj.order + 1

    def _duration_time(self, obj):
        duration_time = obj.duration_time
        return f"{duration_time.hours:02d}h   {duration_time.minutes:02d}min"
