from django.contrib import admin

from .models import Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
    )
    search_fields = (
        'name',
    )
    list_display_links = (
        'id',
        'name',
    )
    list_filter = (
        'id',
        'name',
    )
