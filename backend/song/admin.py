from django.contrib import admin

from .models import Song, RatedSong
from .constants import SONG_LIST_PER_PAGE
from .inlines import SongArtistInline


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'duration',
    )
    search_fields = (
        'name',
    )
    list_per_page = SONG_LIST_PER_PAGE
    ordering = (
        'id',
    )
    inlines = [SongArtistInline]


@admin.register(RatedSong)
class RatedSongAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'song',
        'rating'
    )
    search_fields = (
        'user__username',
        'song__name',
    )
