from django.contrib import admin

from app.admin import UserFilter
from carts.models import SavedForLater


@admin.register(SavedForLater)
class SavedForLaterAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'user',
    ]

    list_display_links = [
        'id',
        'user',
    ]

    list_filter = [
        UserFilter
    ]
