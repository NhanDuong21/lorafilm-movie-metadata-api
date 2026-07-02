from app.providers.tmdb.mapper import TMDBMapper
from app.providers.tmdb.models import TMDBMovieDetailsResponse, TMDBVideosResponse


def test_mapper_details():
    raw = {
        "id": 123,
        "title": "Test",
        "original_title": "Original Test",
        "release_date": "2024-01-01",
        "adult": False,
        "genres": [{"id": 28, "name": "Action"}],
        "production_countries": [],
        "production_companies": [],
        "spoken_languages": [],
    }
    model = TMDBMovieDetailsResponse(**raw)
    res = TMDBMapper.map_movie_details(model)
    assert res.title == "Test"
    assert res.releaseYear == 2024
    assert len(res.genres) == 1
    assert res.genres[0].code == "ACTION"
    assert res.genres[0].name == "Hành động"


def test_mapper_unknown_genre():
    raw = {
        "id": 123,
        "title": "Test",
        "original_title": "Test",
        "adult": False,
        "genres": [{"id": 9999, "name": "Fake Genre"}],
        "production_countries": [],
        "production_companies": [],
        "spoken_languages": [],
    }
    model = TMDBMovieDetailsResponse(**raw)
    res = TMDBMapper.map_movie_details(model)
    assert res.genres[0].code == "UNKNOWN"


def test_mapper_videos_preferred():
    raw = {
        "results": [
            {
                "id": "1",
                "key": "vid1",
                "name": "Teaser",
                "site": "YouTube",
                "type": "Teaser",
                "official": False,
            },
            {
                "id": "2",
                "key": "vid2",
                "name": "Trailer",
                "site": "YouTube",
                "type": "Trailer",
                "official": True,
                "iso_639_1": "vi",
            },
        ]
    }
    model = TMDBVideosResponse(**raw)
    res = TMDBMapper.map_videos(model)
    assert res.preferredTrailer is not None
    assert res.preferredTrailer.externalId == "2"
