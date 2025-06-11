from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Artist


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
