from django.contrib import admin

from .models import Category, Location, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'category',
        'location',
        'created_at',
        'is_published'
    )

    list_editable = (
        'is_published',
        'category'
    )


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Location)
