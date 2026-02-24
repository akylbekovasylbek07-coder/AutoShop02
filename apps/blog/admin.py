from django.contrib import admin
from apps.blog.models import Tag, Post

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', )
    prepopulated_fields = {'slug': ('title',)}

