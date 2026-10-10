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

