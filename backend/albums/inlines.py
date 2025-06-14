from django.contrib import admin

from .models import (
    AlbumArtist,
    AlbumGenre,
    AlbumSong,
)
from .constants import (
    ALBUM_SONG_INLINE_EXTRA,
    ALBUM_ARTIST_INLINE_EXTRA,
    ALBUM_GENRE_INLINE_EXTRA,
)


class AlbumSongInline(admin.TabularInline):
    model = AlbumSong
    extra = ALBUM_SONG_INLINE_EXTRA


class AlbumGenreInline(admin.TabularInline):
    model = AlbumGenre
    extra = ALBUM_GENRE_INLINE_EXTRA


class AlbumArtistInline(admin.TabularInline):
    model = AlbumArtist
    extra = ALBUM_ARTIST_INLINE_EXTRA
