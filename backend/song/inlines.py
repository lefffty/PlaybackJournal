from django.contrib import admin

from artist.models import ArtistSong
from .constants import SongConsts


class SongArtistInline(admin.TabularInline):
    model = ArtistSong
    extra = SongConsts.ARTIST_SONG_INLINE_EXTRA
