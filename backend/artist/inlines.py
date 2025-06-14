from django.contrib import admin

from .models import (
    RelatedArtists,
    ArtistGenre
)
from .constants import (
    RELATED_ARTISTS_INLINE_EXTRA,
    ARTIST_GENRE_INLINE_EXTRA
)


class RelatedArtistsInline(admin.TabularInline):
    model = RelatedArtists
    extra = RELATED_ARTISTS_INLINE_EXTRA
    fk_name = 'related_artist'


class ArtistGenreInline(admin.TabularInline):
    model = ArtistGenre
    extra = ARTIST_GENRE_INLINE_EXTRA
