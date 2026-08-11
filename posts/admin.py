from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Comment, Post, Tag


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "author", "created_at")
    list_filter = ("category", "is_published", "tags")
    search_fields = ("title", "content")
    filter_horizontal = ("tags",)
    inlines = [CommentInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")