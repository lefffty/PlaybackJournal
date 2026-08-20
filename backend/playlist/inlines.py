from django.contrib import admin

from .constants import PlaylistsConsts
from .models import PlaylistSong


class PlaylistSongInline(admin.TabularInline):
    model = PlaylistSong
    extra = PlaylistsConsts.SONG_INLINE_EXTRA
