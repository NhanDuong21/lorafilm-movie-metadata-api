from app.utils.dates import extract_year
from app.utils.genre_mapper import map_genre
from app.utils.image_urls import build_image_url
import pytest

def test_extract_year():
    assert extract_year("2024-05-15") == 2024
    assert extract_year("2019-04-24T12:00:00Z") == 2019
    assert extract_year("1999-invalid") == 1999
    assert extract_year("invalid-date") is None
    assert extract_year(None) is None

def test_map_genre():
    code, name = map_genre(28)
    assert code == "ACTION"
    assert name == "Hành động"
    
    code, name = map_genre(99999)
    assert code == "UNKNOWN"
    assert name == "Unknown Genre"

def test_build_image_url():
    assert build_image_url("/path.jpg", "w500") == "https://image.tmdb.org/t/p/w500/path.jpg"
    assert build_image_url("path.jpg", "original") == "https://image.tmdb.org/t/p/original/path.jpg"
    assert build_image_url(None) is None
    assert build_image_url("") is None
