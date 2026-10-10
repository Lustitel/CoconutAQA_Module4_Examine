from faker import Faker
from random import randint
from datetime import datetime, timezone

fake = Faker('en_US')

class DataGenerator:

    @staticmethod
    def generate_film_name():
        return fake.sentence(3).rstrip('.')

    @staticmethod
    def generate_film_description():
        return fake.sentence(10).rstrip('.')

    @staticmethod
    def generate_price():
        return randint(1, 20000)

    @staticmethod
    def generate_genre_name():
        return fake.sentence(2).rstrip('.')

    @staticmethod
    def generate_creation_date():
        now = datetime.now(timezone.utc)
        return now.isoformat(timespec='milliseconds').replace("+00:00", "Z")

    @staticmethod
    def generate_review():
       return fake.sentence(5).rstrip('.')