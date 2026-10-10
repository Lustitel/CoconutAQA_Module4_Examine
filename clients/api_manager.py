from clients.movies_api import MoviesApi
from clients.genres_api import GenresApi

class ApiManager:
    def __init__(self, session):
        self.session = session
        self.movies_api = MoviesApi(session)
        self.genres_api = GenresApi(session)