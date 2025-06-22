from django.contrib import admin
from django.utils.safestring import mark_safe

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
        'display_cover',
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
    readonly_fields = (
        'display_cover',
        'author',
    )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'author',
                'description',
                'cover',
                'display_cover'
            )
        }),
    )
    inlines = (PlaylistSongInline,)

    @admin.display(description='Обложка альбома')
    @mark_safe
    def display_cover(self, playlist):
        if playlist.cover:
            return (f'<a href="{playlist.cover.url}" target="_blank"><img '
                    f'src="{playlist.cover.url}" style="max-height:100px;"></a>')
        return '-'


@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    list_display = (
        'playlist',
        'song',
    )
