# Tài liệu API Contract - LoraFilm Movie Metadata

Tất cả các endpoint trả về định dạng chuẩn:
```json
{
  "success": true,
  "message": "Thông báo thành công",
  "errorCode": null,
  "data": { ... }
}
```
Lỗi:
```json
{
  "success": false,
  "message": "Chi tiết lỗi",
  "errorCode": "MÃ_LỖI",
  "data": null
}
```

## 1. Health Check
- **Purpose**: Kiểm tra trạng thái dịch vụ và dependencies.
- **Method**: GET
- **Path**: `/api/v1/health`
- **Query Parameters**: None
- **Success Response**: 200 OK
- **Example Curl**: `curl http://localhost:8090/api/v1/health`

## 2. Tìm kiếm phim
- **Purpose**: Tìm phim bằng từ khóa, hỗ trợ phân trang.
- **Method**: GET
- **Path**: `/api/v1/movies/search`
- **Query Parameters**:
  - `query` (string, required): Từ khóa tìm kiếm (min 2 ký tự)
  - `page` (int, optional): Trang hiện tại (mặc định 1)
  - `language` (string, optional): Ngôn ngữ (mặc định vi-VN)
  - `region` (string, optional): Khu vực (mặc định VN)
  - `includeAdult` (boolean, optional): Phim 18+ (mặc định false)
- **Success Response**: 200 OK với mảng `results`
- **Example Curl**: `curl "http://localhost:8090/api/v1/movies/search?query=Avengers"`
- **Caching**: 1 giờ.

## 3. Chi tiết phim
- **Purpose**: Lấy thông tin cơ bản về một bộ phim.
- **Method**: GET
- **Path**: `/api/v1/movies/{externalId}`
- **Query Parameters**:
  - `language` (string, optional)
- **Success Response**: 200 OK
- **Example Curl**: `curl http://localhost:8090/api/v1/movies/299534`
- **Caching**: 24 giờ.

## 4. Danh sách diễn viên & đạo diễn
- **Purpose**: Lấy danh sách Cast và Crew.
- **Method**: GET
- **Path**: `/api/v1/movies/{externalId}/credits`
- **Query Parameters**:
  - `language` (string, optional)
- **Success Response**: 200 OK
- **Example Curl**: `curl http://localhost:8090/api/v1/movies/299534/credits`
- **Caching**: 24 giờ.

## 5. Danh sách video
- **Purpose**: Lấy danh sách Trailer/Teaser.
- **Method**: GET
- **Path**: `/api/v1/movies/{externalId}/videos`
- **Query Parameters**:
  - `language` (string, optional)
- **Success Response**: 200 OK
- **Example Curl**: `curl http://localhost:8090/api/v1/movies/299534/videos`
- **Caching**: 6 giờ.

## 6. Danh sách hình ảnh
- **Purpose**: Lấy danh sách Poster và Backdrop.
- **Method**: GET
- **Path**: `/api/v1/movies/{externalId}/images`
- **Query Parameters**:
  - `language` (string, optional)
- **Success Response**: 200 OK
- **Example Curl**: `curl http://localhost:8090/api/v1/movies/299534/images`
- **Caching**: 24 giờ.

## 7. Import Preview
- **Purpose**: Endpoint tổng hợp dữ liệu để xem trước khi import vào DB.
- **Method**: GET
- **Path**: `/api/v1/movies/{externalId}/import-preview`
- **Query Parameters**:
  - `language` (string, optional)
- **Success Response**: 200 OK
- **Example Curl**: `curl http://localhost:8090/api/v1/movies/299534/import-preview`
- **Caching**: 6 giờ.
