# TruyenWeb - Website Đọc Truyện Online

TruyenWeb là một nền tảng đọc truyện online được xây dựng bằng Django. Dự án này hỗ trợ các chức năng cơ bản như đăng ký, đăng nhập, xem truyện, đánh dấu đã đọc, yêu thích, bình luận, và hệ thống quản trị nội dung dành cho admin.

## Tính năng chính

- Đăng ký / Đăng nhập / Đăng xuất
- Xem danh sách truyện, tìm kiếm và lọc theo thể loại / thời gian
- Đọc từng chương truyện
- Đánh dấu chương đã đọc
- Yêu thích truyện
- Bình luận (có kiểm duyệt AI)
- Quản trị truyện, chương, người dùng thông qua Django Admin
- Trang hồ sơ cá nhân

## Công nghệ sử dụng

- Python 3.x
- Django 4.x
- SQLite (mặc định, có thể đổi sang PostgreSQL hoặc MySQL)
- Bootstrap 5 (giao diện người dùng)
- OpenAI API (lọc bình luận)

## Cài đặt

1. **Clone project:**

```bash
git clone https://github.com/vantu03/TruyenWeb.git
cd TruyenWeb
```

2. **Tạo virtual environment và cài đặt dependencies:**

```bash
python -m venv venv
source venv/bin/activate   # Hoặc .\venv\Scripts\activate trên Windows
pip install -r requirements.txt
```

3. **Tạo file `.env` để chứa biến môi trường (nếu có):**

```
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_django_secret_key
```

4. **Chạy migrate database:**

```bash
python manage.py migrate
```

5. **Tạo tài khoản admin:**

```bash
python manage.py createsuperuser
```

6. **Chạy ứng dụng:**

```bash
python manage.py runserver
```

Truy cập trang web tại `http://127.0.0.1:8000/`

## Thư mục chính

| Thư mục/File         | Mô tả                              |
|----------------------|-------------------------------------|
| `stories/`           | App chính quản lý truyện, chương   |
| `templates/`         | Giao diện HTML                     |
| `static/`            | CSS, JS, ảnh tĩnh                  |
| `users/`             | Quản lý đăng ký, đăng nhập, hồ sơ |
| `comments/`          | Xử lý bình luận và lọc AI         |

## Góp ý / Đóng góp

Bạn có thể fork dự án và gửi pull request hoặc tạo issue để thảo luận thêm.

## License

[MIT License](LICENSE)
