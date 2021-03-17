from django.contrib import admin
from django.utils.html import format_html

from courses.models import (
    Course,
    CourseGoal, 
    CourseRequirement,
)


class CourseGoalInline(admin.StackedInline):
    model = CourseGoal
    extra = 0
    min_num = 1


class CourseRequirementInline(admin.StackedInline):
    model = CourseRequirement
    extra = 0
    min_num = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "id", 
        "image_tag",
        "title", 
        "price", 
        "students_count",
    ]

    list_display_links = [
        "id", 
        "image_tag",
        "title", 
        "price", 
        "students_count",
    ]

    readonly_fields = [
        "students_count",
        "sections_count",
        "lectures_count",
        "articles_count",
        "resources_count",
        "assignments_count",
        "duration_time",
    ]

    fieldsets = [
        (None, {
            "fields": ["slug", "category", "image"]
        }),
        ("Default information", {
            "fields": [
                "title", 
                "subtitle", 
                "description", 
                "price",
                "duration_time",
            ]
        }),
        ("Counts", {
            "fields": [
                "students_count",
                "sections_count",
                "lectures_count",
                "articles_count",
                "resources_count",
                "assignments_count",
            ]
        }),
    ]

    inlines = [
        CourseGoalInline,
        CourseRequirementInline,
    ]

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.image.url}" width="100px" height="56.25px"/>')

    def sections_count(self, obj):
        return obj.content.sections_count

    def lectures_count(self, obj):
        return obj.content.lectures_count

    def articles_count(self, obj):
        return obj.content.articles_count

    def resources_count(self, obj):
        return obj.content.resources_count

    def assignments_count(self, obj):
        return obj.content.assignments_count

    def duration_time(self, obj):
        duration_time = obj.content.duration_time
        return f"{duration_time.hours:02d}h   {duration_time.minutes:02d}min"
