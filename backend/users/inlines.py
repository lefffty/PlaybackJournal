from django.contrib import admin

from albums.models import (
    ListenedAlbum,
    RatedAlbum,
    FavouriteAlbum,
)
from playlist.models import (
    RatedPlaylist,
    FavouritePlaylist,
)
from .constants import UsersConsts


class ListenedAlbumInline(admin.TabularInline):
    model = ListenedAlbum
    extra = UsersConsts.LISTENED_ALBUM_INLINE_EXTRA


class RatedAlbumInline(admin.TabularInline):
    model = RatedAlbum
    extra = UsersConsts.RATED_ALBUM_INLINE_EXTRA


class FavouriteAlbumInline(admin.TabularInline):
    model = FavouriteAlbum
    extra = UsersConsts.FAVOURITE_ALBUM_INLINE_EXTRA


class FavouritePlaylistInline(admin.TabularInline):
    model = FavouritePlaylist


class RatedPlaylistInline(admin.TabularInline):
    model = RatedPlaylist
