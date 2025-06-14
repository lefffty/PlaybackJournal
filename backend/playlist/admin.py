from django.contrib import admin

from .models import (
    Playlist,
    PlaylistSong
)
from .inlines import PlaylistSongInline


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
    inlines = (PlaylistSongInline,)


@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    pass