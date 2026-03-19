from django.contrib import admin

from .models import (
    Review,
    ReviewComment,
)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'type',
        'author',
        'album',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'type',
        'album',
    )
    search_fields = (
        'title',
        'text',
        'author__username',
        'album__name',
    )
    readonly_fields = (
        'display_comments_count',
    )
    fieldsets = (
        (None, {
            "fields": (
                'author',
                'title',
                'text',
                'type',
                'album',
            ),
        }),
        ("Статистика", {
            'fields': (
                'display_comments_count',
            ),
        }),
    )

    @admin.display(description='Количество комментариев к рецензии')
    def display_comments_count(self, obj: Review):
        return obj.comments.count()


@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'text',
        'author',
        'review',
        'created_at',
    )
    search_fields = (
        'text',
        'author__username',
        'review__title',
    )
    fields = (
        'author',
        'text',
        'review',
    )
