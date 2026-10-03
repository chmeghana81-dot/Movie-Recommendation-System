from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import load_data, preprocess_data


class MovieRecommender:

    def __init__(self):

        # Load dataset
        self.movies = load_data()

        # Preprocess dataset
        self.movies = preprocess_data(self.movies)

        # Create TF-IDF matrix
        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(
            self.movies["combined_features"]
        )

        # Calculate cosine similarity
        self.similarity_matrix = cosine_similarity(
            self.tfidf_matrix
        )

    def recommend(self, movie_name, number_of_recommendations=5):

        # Remove extra spaces and convert to lowercase
        movie_name = movie_name.strip().lower()

        # Find matching movie
        matches = self.movies[
            self.movies["title"].str.lower() == movie_name
        ]

        if matches.empty:
            return []

        # Get movie index
        movie_index = matches.index[0]

        # Get similarity scores
        similarity_scores = list(
            enumerate(self.similarity_matrix[movie_index])
        )

        # Sort movies by similarity
        similarity_scores = sorted(
            similarity_scores,
            key=lambda x: x[1],
            reverse=True
        )

        # Remove the selected movie itself
        similarity_scores = similarity_scores[1:]

        # Get top recommendations
        top_movies = similarity_scores[
            :number_of_recommendations
        ]

        recommendations = []

        for index, score in top_movies:

            recommendations.append({
                "title": self.movies.iloc[index]["title"],
                "genre": self.movies.iloc[index]["genre"],
                "rating": self.movies.iloc[index]["rating"],
                "similarity": round(score * 100, 2)
            })

        return recommendations


if __name__ == "__main__":

    recommender = MovieRecommender()

    movie = input("Enter movie name: ")

    results = recommender.recommend(movie)

    if not results:

        print("\nMovie not found.")

    else:

        print("\nRecommended Movies:")
        print("-" * 40)

        for i, movie in enumerate(results, start=1):

            print(
                f"{i}. {movie['title']} "
                f"(Similarity: {movie['similarity']}%)"
            )
