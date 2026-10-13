import pytest
import requests
from data.movies.film_data import generate_film_data
from data.movies.reviews_data import generate_review
from clients.api_manager import ApiManager
from data.auth.register_data import get_register_payload

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

@pytest.fixture()
def test_user():
    return get_register_payload()

@pytest.fixture
def generate_registered_user(api_manager):
    def _create():
        test_user = get_register_payload()
        response = api_manager.auth_api.register_user(test_user).json()
        test_user["id"] = response["id"]
        api_manager.auth_api.authenticate(test_user["email"], test_user["password"])

        return test_user

    return _create

@pytest.fixture(scope="function")
def registered_user(api_manager, generate_registered_user):
    return generate_registered_user()

@pytest.fixture(scope="session")
def unauthenticated_api_manager(registered_user):
    session = requests.Session()
    yield ApiManager(session)
    session.close()

@pytest.fixture(scope="function")
def authenticated_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    api_manager.auth_api.authenticate(email=test_user["email"], password=test_user["password"])
    return test_user

@pytest.fixture(scope="session")
def auth_super_admin(api_manager):
    api_manager.auth_api.authenticate(email="api1@gmail.com", password="asdqwe123Q", expected_status=201)
    yield
    api_manager.auth_api._reset_headers()

@pytest.fixture(scope="function")
def created_film(api_manager, auth_super_admin, test_film):
    response = api_manager.movies_api.create_movie(test_film)
    return response.json()

