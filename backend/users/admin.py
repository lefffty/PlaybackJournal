from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User


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

    @admin.display(description='Аватар пользователя')
    @mark_safe
    def display_avatar(self, user):
        if user.avatar:
            return (f'<a href="{user.avatar.url}" target="_blank"><img '
                    f'src="{user.avatar.url}" style="max-height:100px;"></a>')
        return 'Нет изображения'
