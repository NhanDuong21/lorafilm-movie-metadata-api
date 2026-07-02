# Kiến trúc LoraFilm Movie Metadata API

Tài liệu này mô tả chi tiết về mặt kiến trúc phần mềm, luồng xử lý và cách ứng dụng này tương tác với thế giới bên ngoài.

## Mục tiêu kiến trúc
1. **Phân tách trách nhiệm (Separation of Concerns)**: API chỉ dùng để tra cứu metadata, không chịu trách nhiệm lưu trữ phim, tạo suất chiếu hay bán vé. Đó là nhiệm vụ của `LoraFilm Movie Service`.
2. **Khả năng mở rộng nhà cung cấp**: Hệ thống cung cấp `MovieMetadataProvider` interface để tương lai có thể đổi từ TMDB sang IMDB hoặc một dịch vụ khác mà không ảnh hưởng tới API contract nội bộ.
3. **Hiệu suất & Ổn định**: Hệ thống sử dụng Redis Cache để giảm thiểu lời gọi tới API bên thứ 3 (TMDB), đồng thời có fallback xuống Memory Cache nếu Redis gặp sự cố.

## Sơ đồ luồng tìm kiếm phim (Search Flow)
```mermaid
sequenceDiagram
    participant Frontend as Admin Frontend
    participant API as Movie Metadata API
    participant Cache as Redis
    participant Provider as TMDB

    Frontend->>API: GET /movies/search?query=Avengers
    API->>Cache: Check cache (movie-metadata:v1:search:vi-VN:VN:1:hash)
    alt Cache HIT
        Cache-->>API: Trả về dữ liệu đã cache
    else Cache MISS
        API->>Provider: Gửi request tìm kiếm
        Provider-->>API: Raw TMDB JSON
        API->>API: Normalization & Mapping
        API->>Cache: Lưu kết quả chuẩn hóa vào Redis
    end
    API-->>Frontend: Trả về dữ liệu chuẩn hóa LoraFilm Contract
```

## Sơ đồ luồng lấy Import Preview
Đóng vai trò quan trọng trong việc hiển thị một màn hình duy nhất cho quản trị viên trước khi đưa phim vào hệ thống.

```mermaid
sequenceDiagram
    participant Frontend as Admin Frontend
    participant API as Movie Metadata API
    participant Provider as TMDB
    participant MovieSvc as LoraFilm Movie Service

    Frontend->>API: GET /movies/299534/import-preview
    
    par Lấy Details
        API->>Provider: Lấy Movie Details
    and Lấy Credits
        API->>Provider: Lấy Movie Credits
    and Lấy Videos
        API->>Provider: Lấy Videos
    end
    
    Provider-->>API: Raw Data
    API->>API: Mapper / Chuẩn hóa dữ liệu
    API->>API: Gộp dữ liệu thành Preview
    API->>API: Thêm các cảnh báo (Warnings)
    
    API-->>Frontend: Import Preview Object
    
    Frontend->>Frontend: Quản trị viên bổ sung dữ liệu rạp (giá, suất chiếu, rating)
    Frontend->>MovieSvc: POST /movies (Lưu phim chính thức)
```

## Giải thích thêm về giới hạn
Dịch vụ này KHÔNG trực tiếp tạo dữ liệu (persist) vào `LoraFilm Movie Service` DB. Dữ liệu được trả về Frontend, Frontend hiển thị lên form và yêu cầu Admin hoàn tất các thông tin đặc thù của rạp chiếu phim (Ticket Price, LoraFilm Internal ID, Showtime, Age Rating) rồi mới gọi lên `Movie Service` để lưu trữ chính thức.
