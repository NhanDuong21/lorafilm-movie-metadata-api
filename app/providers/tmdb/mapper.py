from typing import Optional
from app.models.movie import (
    MovieSearchResult,
    MovieDetails,
    Genre,
    ProductionCountry,
    ProductionCompany,
    SpokenLanguage,
)
from app.models.credit import MovieCredits, Director, CastMember
from app.models.video import MovieVideos, Trailer
from app.models.image import MovieImages, Image
from app.models.common import PaginatedData
from app.providers.tmdb.models import (
    TMDBSearchResponse,
    TMDBMovieDetailsResponse,
    TMDBCreditsResponse,
    TMDBVideosResponse,
    TMDBImagesResponse,
)
from app.utils.genre_mapper import map_genre
from app.utils.image_urls import build_image_url
from app.utils.dates import extract_year
from app.core.config import settings


class TMDBMapper:
    @staticmethod
    def map_search_response(
        query: str, response: TMDBSearchResponse
    ) -> PaginatedData[MovieSearchResult]:
        results = []
        for item in response.results:
            results.append(
                MovieSearchResult(
                    externalId=str(item.id),
                    title=item.title,
                    originalTitle=item.original_title,
                    overview=item.overview if item.overview else None,
                    releaseDate=item.release_date if item.release_date else None,
                    releaseYear=extract_year(item.release_date),
                    originalLanguage=item.original_language,
                    posterUrl=build_image_url(item.poster_path, "w500"),
                    backdropUrl=build_image_url(item.backdrop_path, "w1280"),
                    adult=item.adult,
                    popularity=item.popularity,
                    voteAverage=item.vote_average,
                    voteCount=item.vote_count,
                )
            )

        return PaginatedData(
            query=query,
            page=response.page,
            totalPages=response.total_pages,
            totalResults=response.total_results,
            results=results,
        )

    @staticmethod
    def map_movie_details(response: TMDBMovieDetailsResponse) -> MovieDetails:
        genres = []
        for g in response.genres:
            code, name = map_genre(g.id)
            genres.append(Genre(externalId=str(g.id), code=code, name=name, originalName=g.name))

        countries = [
            ProductionCountry(code=c.iso_3166_1, name=c.name) for c in response.production_countries
        ]
        companies = [
            ProductionCompany(
                externalId=str(c.id), name=c.name, logoUrl=build_image_url(c.logo_path, "w500")
            )
            for c in response.production_companies
        ]
        languages = [
            SpokenLanguage(code=l.iso_639_1, name=l.name) for l in response.spoken_languages
        ]

        return MovieDetails(
            externalId=str(response.id),
            imdbId=response.imdb_id,
            title=response.title,
            originalTitle=response.original_title,
            tagline=response.tagline if response.tagline else None,
            overview=response.overview if response.overview else None,
            runtimeMinutes=response.runtime,
            releaseDate=response.release_date if response.release_date else None,
            releaseYear=extract_year(response.release_date),
            status=response.status,
            adult=response.adult,
            originalLanguage=response.original_language,
            spokenLanguages=languages,
            genres=genres,
            productionCountries=countries,
            productionCompanies=companies,
            posterUrl=build_image_url(response.poster_path, "w500"),
            backdropUrl=build_image_url(response.backdrop_path, "w1280"),
            homepageUrl=response.homepage if response.homepage else None,
            popularity=response.popularity,
            voteAverage=response.vote_average,
            voteCount=response.vote_count,
        )

    @staticmethod
    def map_credits(response: TMDBCreditsResponse) -> MovieCredits:
        directors = []
        for crew in response.crew:
            if crew.job == "Director":
                directors.append(
                    Director(
                        externalId=str(crew.id),
                        name=crew.name,
                        profileUrl=build_image_url(crew.profile_path, "w500"),
                    )
                )

        cast = []
        sorted_cast = sorted(response.cast, key=lambda x: x.order)
        for c in sorted_cast[: settings.MAX_CAST_MEMBERS]:
            cast.append(
                CastMember(
                    externalId=str(c.id),
                    name=c.name,
                    character=c.character if c.character else None,
                    order=c.order,
                    profileUrl=build_image_url(c.profile_path, "w500"),
                )
            )

        return MovieCredits(directors=directors, cast=cast)

    @staticmethod
    def map_videos(response: TMDBVideosResponse) -> MovieVideos:
        trailers = []
        for v in response.results:
            url = (
                f"https://www.youtube.com/watch?v={v.key}" if v.site.upper() == "YOUTUBE" else v.key
            )
            trailers.append(
                Trailer(
                    externalId=v.id,
                    name=v.name,
                    platform=v.site.upper(),
                    type=v.type.upper(),
                    official=v.official,
                    language=v.iso_639_1,
                    publishedAt=v.published_at,
                    url=url,
                )
            )

        preferred = None
        if trailers:
            # 1. YouTube, 2. Type Trailer, 3. Official, 4. VN, 5. EN, 6. Date
            def score(t: Trailer) -> int:
                s = 0
                if t.platform == "YOUTUBE":
                    s += 1000
                if t.type == "TRAILER":
                    s += 500
                if t.official:
                    s += 200
                if t.language == "vi":
                    s += 100
                elif t.language == "en":
                    s += 50
                return s

            # Date tie-breaker fallback to 0 if none
            trailers.sort(key=lambda x: (score(x), x.publishedAt or ""), reverse=True)
            preferred = trailers[0]

        return MovieVideos(trailers=trailers, preferredTrailer=preferred)

    @staticmethod
    def map_images(response: TMDBImagesResponse) -> MovieImages:
        posters = []
        for p in response.posters[: settings.MAX_POSTERS]:
            posters.append(
                Image(
                    filePath=p.file_path,
                    urlOriginal=build_image_url(p.file_path, "original") or "",
                    urlW500=build_image_url(p.file_path, "w500"),
                    urlW1280=build_image_url(p.file_path, "w1280"),
                    width=p.width,
                    height=p.height,
                    aspectRatio=p.aspect_ratio,
                    language=p.iso_639_1,
                    voteAverage=p.vote_average,
                    voteCount=p.vote_count,
                )
            )

        backdrops = []
        for b in response.backdrops[: settings.MAX_BACKDROPS]:
            backdrops.append(
                Image(
                    filePath=b.file_path,
                    urlOriginal=build_image_url(b.file_path, "original") or "",
                    urlW500=build_image_url(b.file_path, "w500"),
                    urlW1280=build_image_url(b.file_path, "w1280"),
                    width=b.width,
                    height=b.height,
                    aspectRatio=b.aspect_ratio,
                    language=b.iso_639_1,
                    voteAverage=b.vote_average,
                    voteCount=b.vote_count,
                )
            )

        # Sort to prioritize VN -> None -> EN
        def lang_score(lang: Optional[str]) -> int:
            if lang == "vi":
                return 3
            if lang is None:
                return 2
            if lang == "en":
                return 1
            return 0

        posters.sort(key=lambda x: (lang_score(x.language), x.voteAverage), reverse=True)
        backdrops.sort(key=lambda x: (lang_score(x.language), x.voteAverage), reverse=True)

        return MovieImages(posters=posters, backdrops=backdrops)
