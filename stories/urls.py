from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Trang chủ
    path('story/<slug:slug>/', views.story_detail, name='story_detail'),  # Trang chi tiết truyện
    path('profile/', views.profile_view, name='profile'),  # 👈 Thêm dòng này
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('story/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('favorites/', views.favorite_stories, name='favorite_stories'),
    path('moderate/', views.manual_moderation_view, name='manual_moderation'),
]
