"""Command line entry point for the music recommender demo."""

from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.recommender import load_songs, recommend_songs


DEFAULT_WEIGHTS = {
    "genre": 0.35,
    "mood": 0.25,
    "energy": 0.15,
    "tempo": 0.10,
    "valence": 0.08,
    "danceability": 0.04,
    "acousticness": 0.03,
}

TEMP_WEIGHTS = {
    "genre": 0.175,
    "mood": 0.25,
    "energy": 0.30,
    "tempo": 0.10,
    "valence": 0.08,
    "danceability": 0.04,
    "acousticness": 0.03,
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        (
            "High-Energy Pop",
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.90,
                "tempo_bpm": 125,
                "valence": 0.85,
                "danceability": 0.90,
                "acousticness": 0.10,
            },
        ),
        (
            "Calm Chill",
            {
                "genre": "lofi",
                "mood": "chill",
                "energy": 0.35,
                "tempo_bpm": 75,
                "valence": 0.60,
                "danceability": 0.55,
                "acousticness": 0.85,
            },
        ),
        (
            "High-Energy Rock",
            {
                "genre": "rock",
                "mood": "intense",
                "energy": 0.90,
                "tempo_bpm": 150,
                "valence": 0.45,
                "danceability": 0.70,
                "acousticness": 0.10,
            },
        ),
        (
            "Adversarial Conflicting",
            {
                "genre": "alternative",
                "mood": "sad",
                "energy": 0.90,
                "tempo_bpm": 140,
                "valence": 0.20,
                "danceability": 0.75,
                "acousticness": 0.15,
            },
        ),
    ]

    print(f"Loaded songs: {len(songs)}")

    for profile_name, user_prefs in profiles:
        print(f"\nProfile: {profile_name}")
        print("User profile:")
        for key, value in user_prefs.items():
            print(f"- {key}: {value}")

        recommendations = recommend_songs(user_prefs, songs, k=5, weights=DEFAULT_WEIGHTS)

        print("\nTop recommendations:")
        for song, score, explanation in recommendations:
            print(f"- {song['title']} | Score: {score:.4f} | Reasons: {explanation}")

    print("\nTemporary weight experiment (genre reduced, energy increased):")
    for profile_name, user_prefs in profiles:
        print(f"\nProfile: {profile_name}")
        recommendations = recommend_songs(user_prefs, songs, k=5, weights=TEMP_WEIGHTS)
        print("Top recommendations:")
        for song, score, explanation in recommendations:
            print(f"- {song['title']} | Score: {score:.4f} | Reasons: {explanation}")


if __name__ == "__main__":
    main()
