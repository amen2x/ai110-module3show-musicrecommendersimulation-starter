# 🎵 Music Recommender Simulation

## Project Summary

This project builds a small content-based music recommender. It loads songs from the dataset in [data/songs.csv](data/songs.csv), compares each song to a user profile, and ranks songs by how well they match the user’s preferred genre, mood, energy, tempo, valence, danceability, and acousticness. The system is designed for classroom use and simple experimentation, not for production-level music discovery.

The recommender solves a simple problem: given a user’s taste preferences, it can suggest songs that are likely to feel similar. It is meant to show how recommenders turn human-facing features into a numeric score and then into ranked suggestions.

---

## How The System Works

### Dataset

The dataset originally contained 10 songs and was later expanded by 9 more songs, for a total of 19 songs. The added songs introduced a wider range of genres, including hip-hop, R&B, EDM, country, reggae, Afrobeats, classical, indie folk, and alternative.

### User Taste Profile

A simple example user profile might look like this:

```python
user_profile = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.80,
    "tempo_bpm": 115,
    "valence": 0.80,
    "danceability": 0.80,
    "acousticness": 0.20
}
```

Each song is represented with the following features:

- genre
- mood
- energy
- tempo_bpm
- valence
- danceability
- acousticness

The recommender compares each song to the user profile and gives it a weighted score. Genre and mood receive the highest weights because they are strong signals of a song’s general feel, while the other features contribute smaller amounts.

### Algorithm Recipe

The recommender uses a weighted scoring recipe. The exact feature weights are:

- Genre: 0.35
- Mood: 0.25
- Energy: 0.15
- Tempo: 0.10
- Valence: 0.08
- Danceability: 0.04
- Acousticness: 0.03

Genre and mood use exact matching:

- 1.0 when the value matches
- 0.0 when it does not match

Numerical features use the following similarity rule:

```python
similarity = max(0.0, 1.0 - abs(song_value - user_value))
```

The system then:

1. Computes a match score for each song.
2. Sorts songs from highest score to lowest score.
3. Returns the top recommendations.

Tempo is normalized to a 0–1 scale so it can be compared fairly with features like energy and valence.

### Data Flow

User Preferences → Load Songs → Score Each Song → Sort Scores → Return Top K Recommendations

Every song is evaluated using the same scoring rule before the results are ranked.

### Expected Bias

Because genre and mood have the largest weights, the recommender may repeatedly suggest similar songs and reduce discovery of other genres. It may also overlook songs that match the user well through energy, tempo, valence, danceability, or acousticness but do not match the preferred genre or mood.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

The current project has 2 tests and they pass in the current environment.

---

## Sample Recommendation Output

Example output for an upbeat pop profile:

```text
User profile: genre=pop, mood=happy, energy=0.8
Top recommendations:
1. Sunrise City - Score: 0.9875
Because: matched genre; matched mood; energy is close; tempo is close; valence is close; danceability is close; acousticness is close

2. Gym Hero - Score: 0.7057
Because: matched genre; valence is close; danceability is close
```

---

## Experiments You Tried

I tested the recommender with three different user profiles:

- Upbeat pop listener
- Calm/chill listener
- High-energy rock listener

The system gave strong results for the first two and seemed to work well for obvious genre and mood matches. It also revealed some surprising results, such as Gym Hero ranking highly for a rock listener because its high energy and intense feel matched some numeric features even though its genre was different.

---

## Limitations and Risks

This recommender is intentionally simple. It only works on a small catalog of songs, uses manually chosen weights, and does not use real listening history. It may over-recommend songs that are similar in genre or mood and may miss more surprising or creative recommendations.

You can read a deeper discussion in [model_card.md](model_card.md).

---

## Reflection

I learned that recommendation systems are really about turning simple features into useful predictions. In this project, genre and mood help a lot, but the numeric features like energy and tempo also change which songs feel relevant.

I also learned that even a simple system can introduce bias. If the model strongly favors one genre or mood, it may keep showing similar songs and reduce discovery. Testing multiple user profiles helped show both the strengths and the limits of this approach.



