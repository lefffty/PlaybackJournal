from django.contrib import admin

from .models import (
    RelatedArtists,
    ArtistGenre
)
from .constants import ArtistConsts


class RelatedArtistsInline(admin.TabularInline):
    model = RelatedArtists
    extra = ArtistConsts.RELATED_ARTISTS_INLINE_EXTRA
    fk_name = 'related_artist'


class ArtistGenreInline(admin.TabularInline):
    model = ArtistGenre
    extra = ArtistConsts.GENRE_INLINE_EXTRA
