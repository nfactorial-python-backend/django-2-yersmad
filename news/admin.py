from django.contrib import admin

from .models import News, Comment
# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 5


class AdminNews(admin.ModelAdmin):
    field = ["title", "content", "created_at", "has_comments"]
    inlines = [CommentInline]


admin.site.register(News, AdminNews)
