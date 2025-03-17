from django.contrib import admin
from .models import Story, Chapter, Category, Comment, Favorite

# 🟡 Tùy chọn: Giao diện quản lý Category đơn giản
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Tự sinh slug từ tên

# 🟢 Quản lý Story
@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'uploader', 'created_at')
    exclude = ('uploader',)
    filter_horizontal = ('categories',)  # 👉 Cho phép chọn danh mục đẹp hơn (checkbox ngang)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.uploader = request.user
        super().save_model(request, obj, form, change)

# 🔵 Quản lý Favorite
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('story', 'user', 'created_at')

# 🔵 Quản lý Chapter
@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('story', 'chapter_number', 'title', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'story', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'story__title', 'content')
    readonly_fields = ('created_at',)