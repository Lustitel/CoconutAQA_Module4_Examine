from custom_requester.custom_requester import CustomRequester
from config.base_urls import API_BASE_URL

class GenresApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

