from django.contrib import admin

from categories.models import Category
from courses.models import Course


class CourseInline(admin.StackedInline):
    model = Course
    fields = ["slug", "title", "subtitle"]
    show_change_link = True
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CourseInline
    ]
