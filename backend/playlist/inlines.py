from django.contrib import admin

from .constants import PLAYLIST_SONG_INLINE_EXTRA
from .models import PlaylistSong


class PlaylistSongInline(admin.TabularInline):
    model = PlaylistSong
    extra = PLAYLIST_SONG_INLINE_EXTRA
