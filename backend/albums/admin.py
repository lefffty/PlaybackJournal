from django.contrib import admin

from .models import Album


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
