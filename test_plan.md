# План автоматизации тестирования Movies API (Cinescope)

> [!NOTE]
> Данный тест-план адаптирован под архитектуру проекта **`CustomRequester`** с трехуровневым разделением ответственности (BaseClient $\rightarrow$ API-клиенты $\rightarrow$ APIManager). Все проверки контрактов и структуры данных строятся на стандартных возможностях Python (`dict`, `isinstance`, `set`) без сторонних библиотек вроде Pydantic.

---

## 1. Архитектура и сетевой слой (`BaseClient` / `CustomRequester`)

Реализация базового клиента поверх `requests.Session` с наследованием наработок из вашего `CustomRequester`.

* **Инициализация (`__init__`):**
  * Принимает `base_url`, опциональный `timeout` (по умолчанию 5–10 сек) и опциональную сессию `requests.Session` (если не передана — создаёт новую).
  * Инициализирует базовые заголовки (`Content-Type: application/json`, `Accept: application/json`).
  * Настраивает логгер `logging.getLogger(__name__)`.

* **Центральный метод отправки запросов (`send_request`):**
  * **Обязательные параметры:** `method: str`, `endpoint: str`.
  * **Опциональные параметры:** `data=None`, `json=None`, `params=None`, `headers=None`, `expected_status: int = None`, `need_logging: bool = True`, `**kwargs`.
  * **Логирование в стиле cURL:**
    * Формирование полной команды cURL перед отправкой (метод, URL, заголовки, тело).
    * Замер времени выполнения (`execution_time` в миллисекундах).
    * Форматированный вывод ответа сервера (Status Code, Response Time, форматированный JSON-body).
  * **Проверка статуса ответа:**
    * Если передан `expected_status`, проверяет условие `response.status_code == expected_status`.
    * При несовпадении выбрасывает понятный `ValueError` или `AssertionError` с указанием ожидаемого/фактического статуса и тела ответа сервера.
  * **Проброс `**kwargs`:**
    * Позволяет передавать любые специфичные параметры (`timeout`, `files`, `verify`) напрямую в `session.request`.

* **Управление заголовками сессии:**
  * Метод `update_headers(headers: dict)` — дополняет/обновляет заголовки сессии (`self.session.headers.update(...)`).
  * Метод `reset_headers()` — сбрасывает заголовки сессии до базовых дефолтных значений.

---

## 2. API-Сервисы и Менеджер (Service Layer)

Разделение эндпоинтов по изолированным доменным классам, наследующим `CustomRequester`.

* **`MoviesClient` (работа с фильмами):**
  * `get_movies_list(params=None, expected_status=200)` (GET `/movies`)
  * `get_movie(movie_id, expected_status=200)` (GET `/movies/{id}`)
  * `create_movie(payload, expected_status=201)` (POST `/movies`)
  * `update_movie(movie_id, payload, expected_status=200)` (PATCH `/movies/{id}`)
  * `delete_movie(movie_id, expected_status=200)` (DELETE `/movies/{id}`)

* **`ReviewsClient` (работа с отзывами к фильмам):**
  * `get_movie_reviews(movie_id, params=None, expected_status=200)` (GET `/movies/{movieId}/reviews`)
  * `create_review(movie_id, payload, expected_status=201)` (POST `/movies/{movieId}/reviews`)
  * `update_review(movie_id, payload, expected_status=200)` (PUT `/movies/{movieId}/reviews`)
  * `delete_review(movie_id, expected_status=200)` (DELETE `/movies/{movieId}/reviews`)
  * `hide_review(movie_id, user_id, expected_status=200)` (PATCH `/movies/{movieId}/reviews/hide/{userId}`)
  * `show_review(movie_id, user_id, expected_status=200)` (PATCH `/movies/{movieId}/reviews/show/{userId}`)

* **`GenresClient` (работа со справочником жанров):**
  * `get_genres_list(expected_status=200)` (GET `/genres`)
  * `get_genre(genre_id, expected_status=200)` (GET `/genres/{id}`)
  * `create_genre(payload, expected_status=201)` (POST `/genres`)
  * `delete_genre(genre_id, expected_status=200)` (DELETE `/genres/{id}`)

* **`APIManager` (Паттерн Фасад):**
  * Единая точка входа, хранящая общую сессию `requests.Session` (Shared Session State).
  * Инициализирует все сервисы, обеспечивая сквозную авторизацию:
  ```python
  api = APIManager(session=session)
  api.movies.get_movie(1)
  api.reviews.get_movie_reviews(movie_id=1)
  api.genres.get_genres_list()
  ```

---

## 3. Конфигурация и Генерация данных

* **Конфигурация эндпоинтов (`endpoints.py`):**
  * `MOVIES = "/movies"`
  * `MOVIE_ITEM = "/movies/{id}"`
  * `REVIEWS = "/movies/{movie_id}/reviews"`
  * `REVIEW_HIDE = "/movies/{movie_id}/reviews/hide/{user_id}"`
  * `REVIEW_SHOW = "/movies/{movie_id}/reviews/show/{user_id}"`
  * `GENRES = "/genres"`
  * `GENRE_ITEM = "/genres/{id}"`

* **Конфигурация базовых URL (`config.py` или `base_urls.py`):**
  * `API_BASE_URL = os.getenv("API_BASE_URL", "https://api.dev-cinescope.coconutqa.ru")`
  * `AUTH_BASE_URL = os.getenv("AUTH_BASE_URL", "https://auth.dev-cinescope.coconutqa.ru")`

* **Генератор тестовых данных (`data_generator.py`):**
  * На базе стандартных библиотек (`random`, `uuid`, `datetime`) или `Faker`:
  * `generate_movie_data(**kwargs)` — генерация словаря с полями `name`, `price`, `description`, `genreId` и переопределением любых полей через `**kwargs`.
  * `generate_review_data(**kwargs)` — генерация отзыва (`text`, `rating` от 1 до 10).
  * Удобное создание невалидных данных для негативных тестов (передача пустых строк, невалидных типов, граничных значений).

---

## 4. Фикстуры и Управление окружением (`conftest.py`)

* **Фикстура сессии (`session`):**
  * `scope="session"`: создание единого объекта `requests.Session` и гарантированное закрытие в teardown (`session.close()`).

* **Фикстура фасада (`api_manager`):**
  * Инициализирует `APIManager(session)` для использования во всех тестах.

* **Фикстуры авторизации (`auth_user_api_manager`):**
  * Регистрирует и логинит пользователя через `AuthApi`, записывая `Authorization: Bearer <token>` в сессию `api_manager`. Необходима для тестирования создания/удаления отзывов.

* **Фикстуры сущностей с автоочисткой (Cleanup / Teardown):**
  * Фикстура `created_movie` (при наличии прав): создаёт фильм, отдаёт в тест через `yield`, а в блоке финализатора удаляет через `api.movies.delete_movie(movie_id)`.
  * Фикстура `existing_movie_id`: возвращает `id` первого доступного фильма из общего списка `api.movies.get_movies_list()`. Гарантирует стабильность тестов, не зависящих от прав на создание фильмов.

---

## 5. Структура тестов (`tests/`)

### Модуль `tests/test_movies.py`:
* **GET `/movies` (список):**
  * Проверка получения списка фильмов (200 OK).
  * Проверка структуры элементов списка: наличие обязательных ключей (`id`, `name`, `price`), соответствие типов.
  * Пагинация и фильтрация: проверка работы параметров `page`, `pageSize`, `genreId`.
* **GET `/movies/{id}` (детальная информация):**
  * Получение существующего фильма: совпадение полей с ожидаемыми.
  * Запрос несуществующего фильма (например, `id=99999999`): ожидание 404 Not Found.
  * Запрос с невалидным форматом id: ожидание 400 Bad Request / 422 Unprocessable Entity.
* **POST / PATCH / DELETE `/movies`:**
  * Позитивные тесты (при наличии доступа администратора).
  * Негативные тесты на разграничение прав доступа (RBAC): попытка создания/удаления фильма обычным пользователем или без авторизации возвращает `401 Unauthorized` / `403 Forbidden`.

### Модуль `tests/test_reviews.py`:
* **GET `/movies/{movieId}/reviews`:**
  * Получение списка отзывов к существующему фильму (200 OK).
* **POST `/movies/{movieId}/reviews`:**
  * Успешное создание отзыва авторизованным пользователем (201 Created).
  * Проверка обязательности авторизации: создание отзыва неавторизованным клиентом (401 Unauthorized).
  * Валидация рейтинга: отправка граничных значений (`rating=0` или `rating=11`, ожидание ошибки 400).
* **DELETE / PUT `/movies/{movieId}/reviews`:**
  * Редактирование и удаление своего отзыва.

### Модуль `tests/test_genres.py`:
* **GET `/genres`:**
  * Получение списка всех жанров (200 OK).
  * Проверка контракта списка: ответ является списком, каждый объект содержит `id: int` и `name: str`.
* **GET `/genres/{id}`:**
  * Получение конкретного жанра по существующему `id`.
  * Негативный тест с несуществующим `id` (404 Not Found).

---

## 6. Важные замечания и отличия от базового плана (на основе анализа CustomRequester)

> [!IMPORTANT]
> **1. Ролевая модель бэкенда Cinescope (RBAC):**
> * На реальном бэкенде Cinescope эндпоинты `POST /movies` и `DELETE /movies/{id}` требуют роль **SUPER_ADMIN**.
> * Для обычных тестов чтения (GET) авторизация **не требуется**.
> * Для создания отзывов (`POST reviews`) требуется роль **USER**.
> * В тест-плане создание фильмов вынесено в изолированные проверки, а тесты отзывов опираются на существующие фильмы в базе (`existing_movie_id`).

> [!TIP]
> **2. Проверка контрактов без сторонних библиотек (на чистом Python):**
> Проверку структуры ответа удобно делать через `issubset` и `isinstance`:
> ```python
> data = response.json()
> required_keys = {"id", "name", "price"}
> assert required_keys.issubset(data.keys()), f"Отсутствуют ключи: {required_keys - set(data.keys())}"
> assert isinstance(data["id"], int)
> assert isinstance(data["name"], str)
> ```

> [!TIP]
> **3. Изоляция сессий:**
> Чтобы авторизация одного теста не влияла на другие, сессия очищается либо используется фабрика/фикстура со сбросом заголовков `api_manager.auth_api._reset_headers()`.
