from django.contrib import admin
from django.utils.html import format_html

from ordered_model.admin import OrderedModelAdmin

from courses.models import CourseLecture, CourseLectureDurationTime


class CourseLectureDurationTimeInline(admin.TabularInline):
    verbose_name = "Duration time"
    verbose_name_plural = "Duration time"
    model = CourseLectureDurationTime
    can_delete = False


@admin.register(CourseLecture)
class CourseLectureAdmin(OrderedModelAdmin):
    list_display = [
        "id",
        "title",
        'section',
        'course',
        'course_image_tag',
        'order_in_course',
        'move_up_down_links',
    ]

    list_display_links = [
        "id", 
        "title",
        "section",
        "course",
        "course_image_tag",
    ]

    fields = [
        "course_section",
        "title",
        "description",
        "students_finished_count",
        "free_opened",
    ]

    readonly_fields = [
        "students_finished_count",
    ]

    inlines = [
        CourseLectureDurationTimeInline
    ]

    def section(self, obj):
        return obj.course_section.title

    def course_image_tag(self, obj):
        course = obj.course_section.course_content.course
        return format_html(f'<img src="{course.image.url}" width="100px" height="56.25px"/>')

    def course(self, obj):
        return obj.course_section.course_content.course.title

    def order_in_course(self, obj):
        return obj.order + 1
