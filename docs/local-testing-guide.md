# Hướng Dẫn Kiểm Thử Nội Bộ (Local Testing Guide)

Dưới đây là hướng dẫn chi tiết từng bước để thiết lập, chạy và kiểm thử ứng dụng trên môi trường nội bộ.

## 1. Thiết lập môi trường

### Windows PowerShell
```powershell
# Copy file môi trường
Copy-Item .env.example .env

# Tạo và kích hoạt môi trường ảo
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Cài đặt thư viện
pip install -e ".[dev]"
```

### Linux/macOS
```bash
# Copy file môi trường
cp .env.example .env

# Tạo và kích hoạt môi trường ảo
python3 -m venv .venv
source .venv/bin/activate

# Cài đặt thư viện
pip install -e ".[dev]"
```

> Thêm `TMDB_BEARER_TOKEN=<token_của_bạn>` vào file `.env`.

## 2. Kiểm thử tự động & Chất lượng Code
Trong môi trường ảo đã kích hoạt:
```bash
# Chạy Unit & Integration Tests với coverage
pytest --cov=app --cov-report=term-missing

# Kiểm tra Linter
ruff check .

# Định dạng code tự động
ruff format .

# Kiểm tra Type Hints
mypy app
```

## 3. Chạy API cục bộ (Không Docker)
```powershell
# Bật Redis bằng Docker (tuỳ chọn nhưng khuyến khích)
docker run -d --name redis-local -p 6379:6379 redis:7-alpine

# Chạy ứng dụng
uvicorn app.main:app --reload --port 8090
```
Swagger UI: [http://localhost:8090/docs](http://localhost:8090/docs)

## 4. Kiểm thử qua cURL
```bash
# Health check
curl "http://localhost:8090/api/v1/health"

# Tìm kiếm phim Avengers
curl "http://localhost:8090/api/v1/movies/search?query=Avengers&page=1"

# Lấy chi tiết phim Endgame (ID 299534)
curl "http://localhost:8090/api/v1/movies/299534"

# Lấy danh sách diễn viên phim Endgame
curl "http://localhost:8090/api/v1/movies/299534/credits"

# Lấy video trailer phim Endgame
curl "http://localhost:8090/api/v1/movies/299534/videos"

# Lấy poster phim Endgame
curl "http://localhost:8090/api/v1/movies/299534/images"

# Lấy Import Preview
curl "http://localhost:8090/api/v1/movies/299534/import-preview"
```

## 5. Chạy toàn bộ ứng dụng qua Docker Compose
```powershell
# Khởi chạy toàn bộ hệ thống
docker compose up --build -d

# Dừng hệ thống và xoá container
docker compose down
```
Ứng dụng sẽ có sẵn ở cổng 8090. Redis chạy ở cổng 6379.
