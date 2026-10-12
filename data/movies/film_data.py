from utils.data_generator import DataGenerator
from random import randint, choice

def generate_film_data(**kwargs):
    return {
              "name": DataGenerator.generate_film_name(),
              "price": DataGenerator.generate_price(),
              "description": DataGenerator.generate_film_description(),
              "imageUrl": "https://image.url",
              "location": choice(['MSK', "SPB"]),
              "published": choice([True, False]),
              "genreId": randint(5,10),
    }