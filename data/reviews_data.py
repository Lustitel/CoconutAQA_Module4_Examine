from utils.data_generator import DataGenerator

def generate_review():
    return {
      "rating": DataGenerator.generate_rating(),
      "text": DataGenerator.generate_review()
    }