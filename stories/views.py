from django.shortcuts import render, get_object_or_404
from .models import Story
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Category, Comment
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect
from django.contrib import messages
from django.core.paginator import Paginator
from openai import OpenAI
from django.contrib.auth.decorators import user_passes_test
import threading
import time


def toggle_theme(request):
    current_theme = request.session.get('theme', 'light')
    request.session['theme'] = 'dark' if current_theme == 'light' else 'light'
    return redirect(request.META.get('HTTP_REFERER', '/'))

def index(request):
    now = timezone.now()
    recent_days = now - timedelta(days=7)  # 7 ngày gần nhất

    # 🔥 Top truyện được yêu thích nhiều nhất
    top_favorite = Story.objects.annotate(
        fav_count=Count('favorites')
    ).order_by('-fav_count', '-views')[:10]

    # 🔥 Top truyện xem nhiều nhất
    top_views = Story.objects.order_by('-views', '-created_at')[:10]

    # 🔥 Top truyện mới được yêu thích (trong 7 ngày gần đây)
    top_recent_favorite = Story.objects.filter(
        favorites__date_joined__gte=recent_days
    ).annotate(
        recent_fav_count=Count('favorites')
    ).order_by('-recent_fav_count')[:10]

    return render(request, 'stories/index.html', {
        'top_favorite': top_favorite,
        'top_views': top_views,
        'top_recent_favorite': top_recent_favorite,
    })

def story_detail(request, slug):
    story = get_object_or_404(Story, slug=slug)
    chapters = story.chapter_set.all().order_by('chapter_number')

    # 🔥 Tăng lượt xem
    story.views += 1
    story.save(update_fields=['views'])
    print("_______________________________________________________________________________")
    print(request.user)
    print("_______________________________________________________________________________")
    is_favorited = False
    comments_list = []
    if request.user.is_authenticated:
        is_favorited = story.favorites.filter(id=request.user.id).exists()
        comments_list = (story.comments.filter(status='approved') | story.comments.filter(user=request.user)).select_related('user').order_by('-created_at')
    else:
        comments_list = story.comments.filter(status='approved').select_related('user').order_by('-created_at')

    # 👉 Phân trang bình luận
    paginator = Paginator(comments_list, 10)  # 5 bình luận mỗi trang
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

    return render(request, 'stories/story_detail.html', {
        'story': story,
        'chapters': chapters,
        'is_favorited': is_favorited,
        'comments': comments,
    })

def story_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')
    sort = request.GET.get('sort', 'newest')
    page_number = request.GET.get('page')

    stories = Story.objects.all()

    if query:
        stories = stories.filter(title__icontains=query)

    if category_id:
        stories = stories.filter(categories__id=category_id)

    if sort == 'oldest':
        stories = stories.order_by('created_at')
    elif sort == 'most_favorites':
        stories = stories.annotate(fav_count=Count('favorites')).order_by('-fav_count')
    elif sort == 'most_views':
        stories = stories.order_by('-views')
    else:
        stories = stories.order_by('-created_at')

    # 👇 Phân trang ở đây - 12 truyện mỗi trang (tuỳ bạn)
    paginator = Paginator(stories, 24)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'stories/story_list.html', {
        'page_obj': page_obj,
        'stories': page_obj.object_list,
        'categories': categories,
        'query': query,
        'selected_category': category_id or '',
        'sort': sort
    })


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'stories/signup.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # sau khi lưu, quay lại trang hồ sơ
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'stories/profile.html', {'form': form})

@login_required
def toggle_favorite(request, slug):
    story = get_object_or_404(Story, slug=slug)
    user = request.user

    if user in story.favorites.all():
        story.favorites.remove(user)
    else:
        story.favorites.add(user)

    return redirect('story_detail', slug=slug)

@login_required
def add_comment(request, slug):
    story = get_object_or_404(Story, slug=slug)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                user=request.user,
                story=story,
                content=content,
                status='pending'  # Mặc định: đang chờ duyệt
            )
            messages.success(request, 'Bình luận của bạn đã được gửi và đang chờ duyệt.')
    return redirect('story_detail', slug=slug)


def moderate_pending_comments():
    pending_comments = Comment.objects.filter(status='pending')

    for comment in pending_comments:
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            response = client.moderations.create(
                model="omni-moderation-latest",
                input=comment.content,
            )

            result = response.results[0]
            flagged = result.flagged

            if flagged:
                reason_text = "Bình luận này vi phạm "
                comment.status = 'rejected'
                comment.violation_reason = reason_text
                print(f"Đã từ chối bình luận ID {comment.id} - {reason_text}")
            else:
                print(f"Đã duyệt bình luận ID {comment.id}")
                comment.status = 'approved'

            comment.save()

        except Exception as e:
            print(f"Lỗi kiểm duyệt bình luận ID {comment.id}: {str(e)}")

@login_required
def favorite_stories(request):
    from .models import Favorite  # đảm bảo import nếu chưa

    # Lấy danh sách các bản ghi yêu thích của user hiện tại, kèm truyện liên quan
    favorite_records = Favorite.objects.filter(user=request.user).select_related('story').order_by('-created_at')

    # Phân trang: mỗi trang 8 truyện yêu thích
    paginator = Paginator(favorite_records, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'stories/favorite_stories.html', {
        'page_obj': page_obj,
        'favorites': page_obj.object_list,  # danh sách Favorite object có .story
    })


def moderate_pending_comments(api_key):
    from openai import OpenAI
    messages = []

    client = OpenAI(api_key=api_key)
    pending_comments = Comment.objects.filter(status='pending')

    if not pending_comments.exists():
        messages.append("✅ Không có bình luận nào đang chờ duyệt.")
        return messages

    for comment in pending_comments:
        try:
            response = client.moderations.create(
                model="omni-moderation-latest",
                input=comment.content,
            )
            result = response.results[0]

            if result.flagged:
                reasons = [k for k, v in dict(result.categories).items() if v]
                reason_text = "Bình luận này vi phạm " + ", ".join(reasons)
                comment.status = 'rejected'
                comment.violation_reason = reason_text
                messages.append(f"❌ Từ chối ID {comment.id}: {reason_text}")
            else:
                comment.status = 'approved'
                messages.append(f"✅ Duyệt ID {comment.id}")

            comment.save()
        except Exception as e:
            messages.append(f"⚠️ Lỗi kiểm duyệt ID {comment.id}: {str(e)}")

    return messages

moderation_thread_running = False

@user_passes_test(lambda u: u.is_superuser)
def manual_moderation_view(request):
    global moderation_thread_running
    messages = []

    if request.method == "POST":
        api_key = request.POST.get("api_key", "").strip()

        if not api_key:
            messages.append("⚠️ Bạn cần nhập OpenAI API Key.")
        else:
            # ✅ Nếu chưa có thread tự động, khởi động
            if not moderation_thread_running:
                moderation_thread_running = True

                def run_loop():
                    while True:
                        print("[⏳] Kiểm duyệt tự động mỗi 30s...")
                        logs = moderate_pending_comments(api_key)
                        for msg in logs:
                            print(msg)
                        time.sleep(30)

                threading.Thread(target=run_loop, daemon=True).start()
                print("[✅] Luồng kiểm duyệt tự động đã khởi động.")

            # ✅ Duyệt thủ công ngay lập tức
            messages.append("🔍 Đang kiểm duyệt ngay...")
            messages += moderate_pending_comments(api_key)

    return render(request, 'stories/manual_moderation.html', {
        'messages': messages
    })
