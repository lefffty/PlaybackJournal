from django.contrib import admin

from albums.models import (
    ListenedAlbum,
    RatedAlbum,
    FavouriteAlbum,
)
from .constants import (
    RATED_ALBUM_INLINE_EXTRA,
    LISTENED_ALBUM_INLINE_EXTRA,
    FAVOURITE_ALBUM_INLINE_EXTRA
)


class ListenedAlbumInline(admin.TabularInline):
    model = ListenedAlbum
    extra = LISTENED_ALBUM_INLINE_EXTRA


class RatedAlbumInline(admin.TabularInline):
    model = RatedAlbum
    extra = RATED_ALBUM_INLINE_EXTRA


class FavouriteAlbumInline(admin.TabularInline):
    model = FavouriteAlbum
    extra = FAVOURITE_ALBUM_INLINE_EXTRA
