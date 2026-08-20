from django.contrib import admin

from .models import (
    AlbumArtist,
    AlbumGenre,
    AlbumSong,
)
from .constants import AlbumConsts


class AlbumSongInline(admin.TabularInline):
    model = AlbumSong
    extra = AlbumConsts.SONG_INLINE_EXTRA


class AlbumGenreInline(admin.TabularInline):
    model = AlbumGenre
    extra = AlbumConsts.GENRE_INLINE_EXTRA


class AlbumArtistInline(admin.TabularInline):
    model = AlbumArtist
    extra = AlbumConsts.ARTIST_INLINE_EXTRA
