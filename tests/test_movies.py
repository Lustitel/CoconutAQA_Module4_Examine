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

        assert response_data.json() in [{'error': 'Bad Request', 'message': 'Некорректные данные', 'statusCode': 400}, {'message': 'Bad Request', 'statusCode': 400}]

class TestCreateMoviesPositive:

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.positive
    @pytest.mark.creation
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
        assert all(response_data[k] == test_film[k] for k in test_film), "Данные в ответе не совпадают с отправленными"
        assert "name" in response_data["genre"]

class TestCreateMoviesNegative:

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.creation
    def test_create_film_missing_name(self, api_manager, auth_super_admin, test_film):
        test_film.pop("name")
        response = api_manager.movies_api.create_movie(test_film, expected_status=400)

        assert response.json() == {'error': 'Bad Request', 'message': ['name should not be empty', 'Поле name должно быть строкой'], 'statusCode': 400}

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.creation
    def test_create_film_duplicate_name(self, api_manager, auth_super_admin, test_film):
        api_manager.movies_api.create_movie(test_film)
        test_film["price"] = 300
        response = api_manager.movies_api.create_movie(test_film, expected_status=409)

        assert response.json() == {'message': 'Фильм с таким названием уже существует', 'error': 'Conflict', 'statusCode': 409}

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.negative
    @pytest.mark.creation
    def test_create_film_invalid_type_name(self, api_manager, auth_super_admin, test_film):
        test_film["name"] = 12
        response = api_manager.movies_api.create_movie(test_film, expected_status=400)

        assert response.json() == {
                                    "message": [
                                        "Поле name должно быть строкой"
                                    ],
                                    "error": "Bad Request",
                                    "statusCode": 400
                                }

class TestGetMovieViaId:

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_get_film_via_id(self, api_manager, created_film):
        movies_necessary_keys = {
                                    "id", "name","price",
                                    "description","imageUrl","location",
                                    "published","genreId","genre",
                                    "createdAt","rating", "reviews"
                                    }
        movie_id = created_film["id"]
        response_data = api_manager.movies_api.get_movies_id(movie_id, timeout=5).json()

        assert len(response_data) > 0
        assert movies_necessary_keys.issubset(response_data)
        assert movie_id == response_data["id"]

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_get_film_invalid_id(self, api_manager):
        response_data = api_manager.movies_api.get_movies_id(0, expected_status=404)

        assert response_data.json() in [{'message': 'Фильм не найден', 'error': 'Not Found', 'statusCode': 404},
                                 {'message': 'Not Found',
                                  'statusCode': 404}]


    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_get_film_invalid_id_type(self, api_manager):
        response_data = api_manager.movies_api.get_movies_id("uwu", expected_status=500)

        assert response_data.json() == {'message': 'Internal server error', 'statusCode': 500}

class TestDeleteMovie:

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_delete_film_ok(self, api_manager, created_film):
        movie_id = created_film["id"]
        api_manager.movies_api.delete_movie(movie_id, timeout=5)
        response_data = api_manager.movies_api.get_movies_id(movie_id, timeout=5, expected_status=404).json()

        assert response_data in [{'message': 'Фильм не найден', 'error': 'Not Found', 'statusCode': 404}, {'message': 'Not Found', 'statusCode': 404}], f"Неожиданный ответ сервера: {response_data}"

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_delete_film_invalid_id(self, api_manager, created_film):
        movie_id = 0
        response=api_manager.movies_api.delete_movie(movie_id, expected_status=404)

        assert response.json() in [{'message': 'Фильм не найден', 'error': 'Not Found', 'statusCode': 404},
                                 {'message': 'Not Found',
                                  'statusCode': 404}]

class TestPatchMovie:

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.positive
    def test_patch_movie(self, api_manager, created_film, test_film):
        movies_necessary_keys = {
            "id", "name", "price",
            "description", "imageUrl", "location",
            "published", "genreId", "genre",
            "createdAt", "rating"
        }
        movie_id = created_film["id"]
        test_film["name"] = f"{test_film["name"]} 2"
        response_data = api_manager.movies_api.patch_movie(movie_id, test_film).json()

        assert movies_necessary_keys.issubset(response_data.keys()), "Отсутствуют необходимые поля в 'movies'"
        assert all(response_data[k] == test_film[k] for k in test_film), "Данные в ответе не совпадают с отправленными"
        assert "name" in response_data["genre"]
        assert response_data["id"] == movie_id

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_patch_movie_invalid_id(self, api_manager, created_film, test_film):
        test_film["name"] = f"{test_film["name"]} 2"
        response = api_manager.movies_api.patch_movie(0, test_film, expected_status=404)

        assert response.json() in [{'message': 'Фильм не найден', 'error': 'Not Found', 'statusCode': 404},
                                 {'message': 'Not Found',
                                  'statusCode': 404}]

    @pytest.mark.api
    @pytest.mark.smoke
    @pytest.mark.negative
    def test_patch_movie_invalid_payload(self, api_manager, created_film, test_film):
        movie_id = created_film["id"]
        test_film["name"] = 67
        response_data = api_manager.movies_api.patch_movie(movie_id, test_film, expected_status=400).json()

        assert response_data == {'error': 'Bad Request', 'message': ['Поле name должно быть строкой'], 'statusCode': 400}