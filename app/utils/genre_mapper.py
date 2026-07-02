from typing import Tuple

GENRE_MAP = {
    28: ("ACTION", "Hành động"),
    12: ("ADVENTURE", "Phiêu lưu"),
    16: ("ANIMATION", "Hoạt hình"),
    35: ("COMEDY", "Hài"),
    80: ("CRIME", "Tội phạm"),
    99: ("DOCUMENTARY", "Tài liệu"),
    18: ("DRAMA", "Chính kịch"),
    10751: ("FAMILY", "Gia đình"),
    14: ("FANTASY", "Kỳ ảo"),
    36: ("HISTORY", "Lịch sử"),
    27: ("HORROR", "Kinh dị"),
    10402: ("MUSIC", "Âm nhạc"),
    9648: ("MYSTERY", "Bí ẩn"),
    10749: ("ROMANCE", "Tình cảm"),
    878: ("SCIENCE_FICTION", "Khoa học viễn tưởng"),
    10770: ("TV_MOVIE", "Phim truyền hình"),
    53: ("THRILLER", "Giật gân"),
    10752: ("WAR", "Chiến tranh"),
    37: ("WESTERN", "Viễn Tây"),
}


def map_genre(provider_id: int) -> Tuple[str, str]:
    return GENRE_MAP.get(provider_id, ("UNKNOWN", "Unknown Genre"))
