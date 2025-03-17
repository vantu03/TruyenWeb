from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from stories import views as stories_views
from django.conf import settings
from django.conf.urls.static import static
from stories.views import toggle_favorite
from stories import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stories.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='stories/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', stories_views.signup, name='signup'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('story/<slug:slug>/yeu-thich/', toggle_favorite, name='toggle_favorite'),
    path('stories/', views.story_list, name='story_list'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
