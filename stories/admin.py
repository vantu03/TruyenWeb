from django.contrib import admin
from .models import Story, Chapter, Category, Comment, Favorite
from ckeditor.widgets import CKEditorWidget
from django.db import models

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'uploader', 'created_at')
    exclude = ('uploader',)
    filter_horizontal = ('categories',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.uploader = request.user
        super().save_model(request, obj, form, change)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('story', 'user', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'story__title', 'content')
    readonly_fields = ('created_at',)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('story', 'chapter_number', 'title', 'created_at')
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
