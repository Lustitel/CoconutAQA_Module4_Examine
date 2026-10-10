import pytest
import requests
from data.film_data import generate_film_data
from data.reviews_data import generate_review
from clients.api_manager import ApiManager


@pytest.fixture(scope='session')
def session():
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture(scope='session')
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope='function')
def test_film():
    return generate_film_data()

@pytest.fixture(scope='function')
def test_review():
    return generate_review()

@pytest.fixture(scope='function')
def invalid_payload():
    pass

