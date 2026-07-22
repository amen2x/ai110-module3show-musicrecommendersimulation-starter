"""Command line entry point for the music recommender demo."""

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.80,
        "tempo_bpm": 115,
        "valence": 0.80,
        "danceability": 0.80,
        "acousticness": 0.20,
    }

    print(f"Loaded songs: {len(songs)}")
    print("User profile:")
    for key, value in user_prefs.items():
        print(f"- {key}: {value}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:")
    for song, score, explanation in recommendations:
        print(f"- {song['title']} | Score: {score:.4f} | Reasons: {explanation}")


if __name__ == "__main__":
    main()
