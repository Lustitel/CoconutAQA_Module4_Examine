from utils.data_generator import DataGenerator
from random import randint, choice

def generate_film_data(**kwargs):
    return {
          "movies": [
            {
              "id": randint(1, 1000),
              "name": DataGenerator.generate_film_name(),
              "price": DataGenerator.generate_price(),
              "description": DataGenerator.generate_film_description(),
              "imageUrl": "https://image.url",
              "location": choice(['MSK', "SPB"]),
              "published": choice([True, False]),
              "genreId": randint(1, 10),
              "genre": {
                "name": DataGenerator.generate_genre_name()
              },
              "createdAt": DataGenerator.generate_creation_date(),
              "rating": randint(0,5)
            }
          ]
    }