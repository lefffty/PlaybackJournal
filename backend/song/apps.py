from django.apps import AppConfig


class SongConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'song'
    verbose_name = 'Песни'
