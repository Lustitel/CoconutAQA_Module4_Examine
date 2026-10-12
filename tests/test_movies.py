from utils.number_type import is_int, is_number, is_str
import pytest

class TestGetMovies:

    @pytest.mark.api
    @pytest.mark.smoke
    def test_check_necessary_fields(self, api_manager):
        global_necessary_keys = { "movies", "count",
                                    "page", "pageSize",
                                    "pageCount"
                                   }
        movies_necessary_keys = {
                                    "id", "name","price",
                                    "description","imageUrl","location",
                                    "published","genreId","genre",
                                    "createdAt","rating"
                                    }

        response = api_manager.movies_api.get_movies()
        response_data = response.json()

        assert global_necessary_keys.issubset(response_data.keys()), "Отсутствуют необходимые поля в ответе"
        assert len(response_data["movies"]) > 0, "Список фильмов пуст"
        assert movies_necessary_keys.issubset(response_data["movies"][0].keys()), "Отсутствуют необходимые поля в 'movies'"

    @pytest.mark.api
    @pytest.mark.smoke
    def test_response_fields_type(self, api_manager):
        response_data = api_manager.movies_api.get_movies().json()

        global_number_fields_values = ["count", "page", "pageSize","pageCount"]

        assert isinstance(response_data["movies"], list)
        assert all(is_int(response_data[field]) for field in global_number_fields_values), "Не все указанные поля имеют тип int"

    @pytest.mark.api
    @pytest.mark.smoke
    def test_response_movies_fields_type(self, api_manager):
        response_data = api_manager.movies_api.get_movies().json()

        assert len(response_data["movies"]) > 0, "Список фильмов пуст"

        movie = response_data["movies"][0]
        str_fields_values = ["name","description","imageUrl","location","createdAt"]

        invalid_str_fields = {
            field: type(movie.get(field)).__name__ for field in str_fields_values
            if not is_str(movie.get(field))
        }

        assert all(is_int(movie[k]) for k in ("id", "genreId"))
        assert all(is_number(movie[k]) for k in ("price", "rating"))
        assert not invalid_str_fields, f"Ошибочные текстовые поля: {invalid_str_fields}"
        assert type(movie["published"]) is bool
        assert type(movie["genre"]) is dict
        assert len(movie["genre"]) > 0
        assert "name" in movie["genre"]

class TestGetMoviesFiltersPositive:

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_no_filter(self, api_manager):
        test_filters = {}
        response = api_manager.movies_api.get_movies(params=test_filters)
        response_data = response.json()

        assert "movies" in response_data
        assert type(response_data["movies"]) is list

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_filter_page_size(self, api_manager):
        page_size = 1
        test_filters = {"pageSize": page_size}
        response_data = api_manager.movies_api.get_movies(params=test_filters).json()

        assert len(response_data["movies"]) > 0
        assert response_data["pageSize"] == page_size
        assert len(response_data["movies"]) == page_size

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_filter_page_number(self, api_manager):
        page_number = 10
        test_filters = {"page": page_number}
        response_data = api_manager.movies_api.get_movies(params=test_filters).json()

        assert len(response_data["movies"]) > 0
        assert response_data["page"] == page_number

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_filter_price(self, api_manager):
        min_price = 1
        max_price = 2000
        test_filters = {"minPrice": min_price, "maxPrice": max_price}
        response_data = api_manager.movies_api.get_movies(params=test_filters).json()
        movies = response_data["movies"]

        assert len(movies) > 0
        assert all(min_price <= movie["price"] <= max_price for movie in movies)

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_filter_locations(self, api_manager):
        locations = "MSK"
        test_filters = {"locations": locations}
        response_data = api_manager.movies_api.get_movies(params=test_filters).json()
        movies = response_data["movies"]

        assert len(movies) > 0
        assert all(movie["location"] == locations for movie in movies)

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_filter_published_true(self, api_manager):
        response_data = api_manager.movies_api.get_movies(params={"published": "true"}).json()
        movies = response_data["movies"]

        assert len(movies) > 0, "Опубликованные фильмы не найдены"
        assert all(movie["published"] is True for movie in movies)

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_filter_published_false(self, api_manager):
        response_data = api_manager.movies_api.get_movies(params={"published": "false"}).json()
        movies = response_data["movies"]

        assert len(movies) > 0, "Неопубликованные фильмы не найдены"
        assert all(movie["published"] is False for movie in movies)

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_filter_genre_id(self, api_manager):
        genre_id = 5
        response_data = api_manager.movies_api.get_movies(params={"genreId": genre_id}).json()
        movies = response_data["movies"]

        assert len(movies) > 0, f"Фильмы с id жанра: {genre_id} не найдены"
        assert all(movie["genreId"] == genre_id for movie in movies)

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_filter_show_order_asc(self, api_manager):
        created_at = 'asc'
        response_data = api_manager.movies_api.get_movies(params={"createdAt": created_at}).json()
        movies = response_data["movies"]
        movies_id = [movie["id"] for movie in movies]

        assert len(movies) > 0, f"Фильмы не найдены"
        assert movies_id == sorted(movies_id)

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_filter_show_order_desc(self, api_manager):
        created_at = 'desc'
        response_data = api_manager.movies_api.get_movies(params={"createdAt": created_at}).json()
        movies = response_data["movies"]
        movies_id = [movie["id"] for movie in movies]

        assert len(movies) > 0, f"Фильмы не найдены"
        assert movies_id == sorted(movies_id, reverse=True)

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.positive
    def test_max_price_max_value(self, api_manager):
        max_int = 2**31-1
        response_data = api_manager.movies_api.get_movies(params={"maxPrice": max_int})

        assert response_data.json() != {'error': 'Bad Request', 'message': 'Некорректные данные', 'statusCode': 400}
        assert len(response_data.json()["movies"]) > 0

class TestGetMoviesFiltersNegative:

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.negative
    def test_page_size_min_boundary(self, api_manager):
        response_data = api_manager.movies_api.get_movies(params={"pageSize": 0}, expected_status=400)

        assert response_data.json() == {'message': ['Поле pageSize имеет минимальную величину 1'], 'error': 'Bad Request', 'statusCode': 400}

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.negative
    def test_page_size_invalid_value(self, api_manager):
        response_data = api_manager.movies_api.get_movies(params={"pageSize": -1}, expected_status=400)

        assert response_data.json() == {'message': ['Поле pageSize имеет минимальную величину 1'], 'error': 'Bad Request', 'statusCode': 400}


    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.negative
    def test_page_size_max_boundary(self, api_manager):
        response_data = api_manager.movies_api.get_movies(params={"pageSize": 21}, expected_status=400)

        assert response_data.json() == {'message': ['Поле pageSize имеет максимальную величину 20'], 'error': 'Bad Request', 'statusCode': 400}

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.negative
    def test_min_price_min_boundary(self, api_manager):
        response_data = api_manager.movies_api.get_movies(params={"minPrice": 0}, expected_status=400)

        assert response_data.json() == {'message': ['Поле minPrice имеет минимальную величину 1'], 'error': 'Bad Request', 'statusCode': 400}

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.negative
    def test_min_price_max_boundary_without_max_price(self, api_manager):
        response_data = api_manager.movies_api.get_movies(params={"minPrice": 1000}, expected_status=400)

        assert response_data.json() == {
                                          "message": "minPrice must be less than maxPrice",
                                          "error": "Bad Request",
                                          "statusCode": 400
                                        }, "Значение minPrice не должно превышать или равняться дефолтному значению maxPrice=1000"

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.negative
    def test_max_price_min_boundary(self, api_manager):
        response_data = api_manager.movies_api.get_movies(params={"maxPrice": 0}, expected_status=400)

        assert response_data.json() == {'message': 'minPrice must be less than maxPrice', 'error': 'Bad Request', 'statusCode': 400}

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.negative
    def test_max_price_less_min_price(self, api_manager):
        response_data = api_manager.movies_api.get_movies(params={"minPrice": 2, "maxPrice": 1}, expected_status=400)

        assert response_data.json() == {'message': 'minPrice must be less than maxPrice', 'error': 'Bad Request', 'statusCode': 400}

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.filters
    @pytest.mark.negative
    def test_max_price_max_boundary(self, api_manager):
        over_max_int = 2**31
        response_data = api_manager.movies_api.get_movies(params={"maxPrice": over_max_int}, expected_status=400)

        assert response_data.json() == {'error': 'Bad Request', 'message': 'Некорректные данные', 'statusCode': 400}

class TestCreateMovies:

    @pytest.mark.api
    @pytest.mark.smoke
    def test_create_film(self, api_manager, auth_super_admin, test_film):
        movies_necessary_keys = {
                                    "id", "name","price",
                                    "description", "imageUrl","location",
                                    "published","genreId","genre",
                                    "createdAt","rating"
                                    }
        response = api_manager.movies_api.create_movie(test_film)
        response_data = response.json()

        assert movies_necessary_keys.issubset(response_data.keys()), "Отсутствуют необходимые поля в 'movies'"