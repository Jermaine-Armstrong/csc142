import random


class Review:
    def __init__(self, rating, text):
        if rating < 0 or rating > 5:
            raise ValueError("rating must be between 0 and 5")
        self.rating = rating
        self.text = text

    def __str__(self):
        return f"{self.rating}/5 - {self.text}"


class Movie:
    def __init__(self, title):
        self.title = title
        self.reviews = []

    def add_review(self, rating, text):
        self.reviews.append(Review(rating, text))

    def average_rating(self):
        if not self.reviews:
            return 0
        total = sum(review.rating for review in self.reviews)
        return total / len(self.reviews)

    def display_reviews(self):
        for review in self.reviews:
            print(review)

    def best_review(self):
        if not self.reviews:
            return None
        max_rating = max(review.rating for review in self.reviews)
        best = [review for review in self.reviews if review.rating == max_rating]
        return random.choice(best)

    def worst_review(self):
        if not self.reviews:
            return None
        min_rating = min(review.rating for review in self.reviews)
        worst = [review for review in self.reviews if review.rating == min_rating]
        return random.choice(worst)


if __name__ == "__main__":
    movie = Movie("The Grand Train Heist")
    movie.add_review(5, "A fun ride with clever twists.")
    movie.add_review(3, "Good action, thin story.")
    movie.add_review(4, "Great pacing and solid performances.")
    movie.add_review(5, "Loved the ending.")
    movie.add_review(2, "Not my style.")

    print(f"Movie: {movie.title}")
    print(f"Average rating: {movie.average_rating():.2f}")
    print("All reviews:")
    movie.display_reviews()
    print(f"Best review: {movie.best_review()}")
    print(f"Worst review: {movie.worst_review()}")
