# Generated by Django 5.1.6 on 2025-03-17 19:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('poster', models.ImageField(blank=True, null=True, upload_to='posters/')),
                ('views', models.PositiveIntegerField(default=0)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('categories', models.ManyToManyField(blank=True, related_name='stories', to='stories.category')),
                ('favorites', models.ManyToManyField(blank=True, related_name='favorite_stories', through='stories.Favorite', to=settings.AUTH_USER_MODEL)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='favorite',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.story'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Nội dung bình luận')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Đang duyệt'), ('approved', 'Đã duyệt'), ('rejected', 'Từ chối')], default='pending', max_length=10)),
                ('violation_reason', models.TextField(blank=True, null=True, verbose_name='Ghi chú')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='stories.story')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter_number', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.story')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together={('user', 'story')},
        ),
    ]
