from django.contrib import admin

from artist.models import ArtistSong
from .constants import ARTIST_SONG_INLINE_EXTRA


class SongArtistInline(admin.TabularInline):
    model = ArtistSong
    extra = ARTIST_SONG_INLINE_EXTRA
