import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5, weights: Optional[Dict[str, float]] = None) -> List[Song]:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "acousticness": 0.8 if user.likes_acoustic else 0.2,
        }
        scored_songs = []
        for song in self.songs:
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "tempo_bpm": song.tempo_bpm,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            }
            score, reasons = score_song(user_prefs, song_dict, weights=weights)
            scored_songs.append((song, score, reasons))

        scored_songs.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _, _ in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "acousticness": 0.8 if user.likes_acoustic else 0.2,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }
        _, reasons = score_song(user_prefs, song_dict)
        return "; ".join(reasons) if reasons else "No explanation available."


def load_songs(csv_path: str) -> List[Dict[str, Any]]:
    """Load songs from a CSV file into a list of dictionaries."""
    path = Path(csv_path)
    songs: List[Dict[str, Any]] = []

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                }
            )

    print(f"Loading songs from {csv_path}...")
    return songs


def _normalize_tempo(tempo_bpm: float, min_bpm: float = 50.0, max_bpm: float = 200.0) -> float:
    """Map tempo from BPM to a 0-1 scale for simple scoring."""
    if max_bpm <= min_bpm:
        return 0.5
    value = (tempo_bpm - min_bpm) / (max_bpm - min_bpm)
    return max(0.0, min(1.0, value))


def _get_pref(user_prefs: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Return a preference value while supporting common alternate key names."""
    if key in user_prefs:
        return user_prefs[key]
    if key == "tempo" and "tempo_bpm" in user_prefs:
        return user_prefs["tempo_bpm"]
    if key == "tempo_bpm" and "tempo" in user_prefs:
        return user_prefs["tempo"]
    if key == "genre" and "favorite_genre" in user_prefs:
        return user_prefs["favorite_genre"]
    if key == "mood" and "favorite_mood" in user_prefs:
        return user_prefs["favorite_mood"]
    if key == "energy" and "target_energy" in user_prefs:
        return user_prefs["target_energy"]
    if key == "acousticness" and "likes_acoustic" in user_prefs:
        return 0.8 if user_prefs["likes_acoustic"] else 0.2
    return default


def score_song(user_prefs: Dict[str, Any], song: Dict[str, Any], weights: Optional[Dict[str, float]] = None) -> Tuple[float, List[str]]:
    """Score a single song against a user profile and return reasons."""
    effective_weights = {
        "genre": 0.35,
        "mood": 0.25,
        "energy": 0.15,
        "tempo": 0.10,
        "valence": 0.08,
        "danceability": 0.04,
        "acousticness": 0.03,
    }
    if weights:
        effective_weights.update(weights)

    reasons: List[str] = []
    score = 0.0

    preferred_genre = str(_get_pref(user_prefs, "genre", "")).lower()
    song_genre = str(song.get("genre", "")).lower()
    genre_match = 1.0 if preferred_genre and preferred_genre == song_genre else 0.0
    score += genre_match * effective_weights["genre"]
    if genre_match:
        reasons.append("matched genre")

    preferred_mood = str(_get_pref(user_prefs, "mood", "")).lower()
    song_mood = str(song.get("mood", "")).lower()
    mood_match = 1.0 if preferred_mood and preferred_mood == song_mood else 0.0
    score += mood_match * effective_weights["mood"]
    if mood_match:
        reasons.append("matched mood")

    preferred_energy = float(_get_pref(user_prefs, "energy", 0.5))
    song_energy = float(song.get("energy", 0.5))
    energy_similarity = max(0.0, 1.0 - abs(song_energy - preferred_energy))
    score += energy_similarity * effective_weights["energy"]
    if energy_similarity > 0.9:
        reasons.append("energy is close")

    preferred_tempo = _get_pref(user_prefs, "tempo", _get_pref(user_prefs, "tempo_bpm", 0.5))
    if isinstance(preferred_tempo, (int, float)):
        preferred_tempo_norm = _normalize_tempo(float(preferred_tempo))
    else:
        preferred_tempo_norm = 0.5
    song_tempo_norm = _normalize_tempo(float(song.get("tempo_bpm", 0.0)))
    tempo_similarity = max(0.0, 1.0 - abs(song_tempo_norm - preferred_tempo_norm))
    score += tempo_similarity * effective_weights["tempo"]
    if tempo_similarity > 0.9:
        reasons.append("tempo is close")

    preferred_valence = float(_get_pref(user_prefs, "valence", 0.5))
    song_valence = float(song.get("valence", 0.5))
    valence_similarity = max(0.0, 1.0 - abs(song_valence - preferred_valence))
    score += valence_similarity * effective_weights["valence"]
    if valence_similarity > 0.9:
        reasons.append("valence is close")

    preferred_dance = float(_get_pref(user_prefs, "danceability", 0.5))
    song_dance = float(song.get("danceability", 0.5))
    dance_similarity = max(0.0, 1.0 - abs(song_dance - preferred_dance))
    score += dance_similarity * effective_weights["danceability"]
    if dance_similarity > 0.9:
        reasons.append("danceability is close")

    preferred_acoustic = float(_get_pref(user_prefs, "acousticness", 0.5))
    song_acoustic = float(song.get("acousticness", 0.5))
    acoustic_similarity = max(0.0, 1.0 - abs(song_acoustic - preferred_acoustic))
    score += acoustic_similarity * effective_weights["acousticness"]
    if acoustic_similarity > 0.9:
        reasons.append("acousticness is close")

    return round(score, 4), reasons


def recommend_songs(user_prefs: Dict[str, Any], songs: List[Dict[str, Any]], k: int = 5, weights: Optional[Dict[str, float]] = None) -> List[Tuple[Dict[str, Any], float, str]]:
    """Return the top-k scored songs with their scores and explanations."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights=weights)
        explanation = "; ".join(reasons) if reasons else "Basic match based on content features"
        scored_songs.append((song, score, explanation))

    scored_songs.sort(key=lambda item: item[1], reverse=True)
    return scored_songs[:k]
