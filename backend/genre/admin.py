from django.contrib import admin

from .models import (
    Genre,
    FavouriteGenre,
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
    )
    list_display_links = (
        'id',
        'name',
    )
    search_fields = (
        'name',
    )


@admin.register(FavouriteGenre)
class FavouriteGenreAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'genre',
    )
    search_fields = (
        'user__username',
        'genre__name',
    )
