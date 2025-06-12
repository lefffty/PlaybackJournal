from django.contrib import admin

from .models import Song
from .constants import SONG_LIST_PER_PAGE


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration',)
    search_fields = ('name',)
    list_per_page = SONG_LIST_PER_PAGE
    ordering = (
        'id',
    )
