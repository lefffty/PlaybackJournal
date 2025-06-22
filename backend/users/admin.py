from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User
from .inlines import (
    RatedAlbumInline,
    ListenedAlbumInline,
    FavouriteAlbumInline,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username',
        'first_name', 'last_name',
        'email', 'registration_date',
        'display_avatar',
    )
    search_fields = (
        'username', 'first_name',
        'last_name', 'email',
    )
    readonly_fields = (
        'registration_date',
        'display_avatar',
        'display_favorites',
        'display_listens',
        'display_rated',
    )
    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'avatar', 'registration_date')
        }),
        ('Статистика', {
            'fields': ('display_favorites', 'display_listens', 'display_rated'),
        }),
    )
    inlines = (RatedAlbumInline, ListenedAlbumInline, FavouriteAlbumInline)

    @admin.display(description='Аватар пользователя')
    @mark_safe
    def display_avatar(self, user):
        if user.avatar:
            return (f'<a href="{user.avatar.url}" target="_blank"><img '
                    f'src="{user.avatar.url}" style="max-height:100px;"></a>')
        return 'Нет изображения'

    @admin.display(description='Количество прослушанных альбомов')
    def display_listens(self, obj):
        return obj.listenedalbums.count()

    @admin.display(description='Количество альбомов в "Любимое"')
    def display_favorites(self, obj):
        return obj.favouritealbums.count()

    @admin.display(description='Количество оценок альбомов')
    def display_rated(self, obj):
        return obj.ratedalbums.count()
