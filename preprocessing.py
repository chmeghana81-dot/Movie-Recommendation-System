import pandas as pd


def load_data():
    """Load the movie dataset."""
    file_path = "dataset/movies.csv"

    df = pd.read_csv(file_path)

    return df


def preprocess_data(df):
    """Clean the dataset and create combined features."""

    # Replace missing values with empty strings
    df = df.fillna("")

    # Convert columns to string
    columns = ["genre", "cast", "description", "director"]

    for column in columns:
        df[column] = df[column].astype(str)

    # Combine important movie information
    df["combined_features"] = (
        df["genre"] + " "
        + df["cast"] + " "
        + df["description"] + " "
        + df["director"]
    )

    return df


if __name__ == "__main__":

    movies = load_data()
    movies = preprocess_data(movies)

    print("Dataset loaded successfully!")
    print("Total movies:", len(movies))

    print("\nColumns:")
    print(movies.columns.tolist())

    print("\nFirst movie:")
    print(movies.iloc[0])
