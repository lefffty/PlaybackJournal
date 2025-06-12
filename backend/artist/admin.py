from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Artist,
    RelatedArtists,
    ArtistGenre,
    ArtistSong
)


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'description',
        'avatar_display',
    )
    search_fields = (
        'username',
    )

    @admin.display(description='Аватар артиста')
    @mark_safe
    def avatar_display(self, artist):
        if artist.avatar:
            return (f'<a href="{artist.avatar.url}" target="_blank"><img '
                    f'src="{artist.avatar.url}" style="max-height:100px;"></a>')
        return 'Пусто'


@admin.register(RelatedArtists)
class RelatedArtistsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'artist',
        'related_artist',
    )
    search_fields = (
        'artist',
        'related_artist',
    )


@admin.register(ArtistGenre)
class ArtistGenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'artist',
        'genre',
    )
    search_fields = (
        'artist',
        'genre',
    )


@admin.register(ArtistSong)
class ArtistSongAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'artist',
        'song',
    )
