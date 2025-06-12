from django.contrib import admin

from .models import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
    )
    list_display_links = (
        'id',
        'name',
    )
    search_fields = (
        'name',
    )
