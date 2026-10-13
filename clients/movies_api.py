from custom_requester.custom_requester import CustomRequester
from config.base_urls import API_BASE_URL

MOVIES = "/movies"
REVIEWS = "/reviews"
GENRES = "/genres"

class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def get_movies(self, expected_status=200, params=None, **kwargs):
        return self.send_request("GET", MOVIES, params=params, expected_status=expected_status, **kwargs)

    def get_movies_id(self, movie_id=None, expected_status=200, params=None, **kwargs):
        return self.send_request("GET", f"{MOVIES}/{movie_id}", params=params, expected_status=expected_status, **kwargs)

    def create_movie(self, film_data, expected_status=201, params=None, **kwargs):
        return self.send_request("POST", MOVIES, data=film_data, params=params, expected_status=expected_status, **kwargs)

    def delete_movie(self, movie_id, expected_status=200, params=None, **kwargs):
        return self.send_request("DELETE", f"{MOVIES}/{movie_id}", params=params, expected_status=expected_status, **kwargs)

    def patch_movie(self, movie_id, film_data, expected_status=200, params=None, **kwargs):
        return self.send_request("PATCH", f"{MOVIES}/{movie_id}", data=film_data, params=params, expected_status=expected_status, **kwargs)

