from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Story(models.Model):
    title = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='stories', blank=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE) 
    author = models.CharField(max_length=255)  # 👉 Tên tác giả thực
    description = models.TextField()
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    favorites = models.ManyToManyField(
        User,
        through='Favorite',
        related_name='favorite_stories',
        blank=True
    )

    views = models.PositiveIntegerField(default=0)  # 👈 Lượt xem
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            counter = 1
            slug = base_slug
            while Story.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Comment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Đang duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    story = models.ForeignKey('Story', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name="Nội dung bình luận")
    created_at = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    violation_reason = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    def __str__(self):
        return f"Bình luận của {self.user.username} về '{self.story.title}'"


class Chapter(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    chapter_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.story.title} - Chapter {self.chapter_number}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    story = models.ForeignKey('Story', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'story')  # Mỗi user chỉ được yêu thích 1 lần với 1 truyện

    def __str__(self):
        return f"{self.user.username} yêu thích '{self.story.title}'"
        
class ChapterView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'chapter')  # mỗi chương chỉ lưu 1 lần đọc với mỗi user

    def __str__(self):
        return f"{self.user.username} đã đọc {self.chapter}"
