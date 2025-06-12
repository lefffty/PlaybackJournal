from django.contrib import admin

from .models import (
    Album,
    RatedAlbum,
    FavouriteAlbum,
    ListenedAlbum,
    AlbumArtist,
    AlbumGenre,
    AlbumSong,
)
from .tabular_inlines import (
    AlbumSongInline,
    AlbumArtistInline,
    AlbumGenreInline,
)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'publication_date',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'id',
        'name',
    )
    inlines = (AlbumSongInline, AlbumGenreInline, AlbumArtistInline)


class AbstractUserAlbumAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'album',
    )
    search_fields = (
        'user',
        'album',
    )


@admin.register(RatedAlbum)
class RatedAlbumAdmin(AbstractUserAlbumAdmin):
    pass


@admin.register(FavouriteAlbum)
class FavouriteAlbumAdmin(AbstractUserAlbumAdmin):
    pass


@admin.register(ListenedAlbum)
class ListenedAlbumAdmin(AbstractUserAlbumAdmin):
    pass


@admin.register(AlbumSong)
class AlbumSong(admin.ModelAdmin):
    list_display = (
        'id',
        'album',
        'song',
    )
    search_fields = (
        'album',
        'song',
    )


@admin.register(AlbumArtist)
class AlbumArtistAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'album',
        'artist',
    )
    search_fields = (
        'album',
        'artist',
    )


@admin.register(AlbumGenre)
class AlbumGenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'album',
        'genre',
    )
    search_fields = (
        'album',
        'genre',
    )
