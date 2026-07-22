# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

---

## 2. Goal / Task

This system recommends and ranks songs based on how closely their features match a user’s taste profile.

It is a manually weighted content-based recommender. It is not a trained machine-learning model.

---

## 3. Data Used

The recommender uses 19 fictional songs from [data/songs.csv](data/songs.csv). The dataset was expanded from 10 songs by adding 9 more.

The main features are:

- genre
- mood
- energy
- tempo_bpm
- valence
- danceability
- acousticness

ID, title, and artist are used for identification and display. They are not used directly in the scoring rule.

This small fictional dataset does not represent the full variety of real music.

---

## 4. Algorithm Summary

The system compares a user profile to each song and gives the song a final score.

Genre and mood use exact matching. A match gives full credit, and a mismatch gives no credit for that feature.

Numerical features receive higher similarity when they are closer to the user’s target value. Tempo is normalized before comparison so it can be compared fairly with the other numeric features.

The feature weights are:

- genre: 0.35
- mood: 0.25
- energy: 0.15
- tempo: 0.10
- valence: 0.08
- danceability: 0.04
- acousticness: 0.03

Each song receives one score. The songs are sorted from highest score to lowest score. The top-k songs are returned with short explanations.

---

## 5. Observed Behavior / Biases

Genre and mood can dominate the results. This can push the recommender toward similar songs and reduce discovery.

The system may create filter bubbles. Similar songs can appear repeatedly in the top results.

Songs can match numerically without matching stylistically. Exact matching also does not recognize related genres or moods.

The small dataset affects variety. Manually selected weights also reflect human assumptions. Conflicting preferences can produce unexpected results.

---

## 6. Evaluation Process

I tested the recommender with four profiles:

- High-Energy Pop
- Calm Chill
- High-Energy Rock
- An adversarial profile with conflicting preferences

I compared the top five recommendations for each profile.

### High-Energy Pop

```text
Top recommendations:
- Sunrise City | Score: 0.9757 | Reasons: matched genre; matched mood; energy is close; tempo is close; valence is close; acousticness is close
- Gym Hero | Score: 0.7321 | Reasons: matched genre; energy is close; tempo is close; valence is close; danceability is close; acousticness is close
- Rooftop Lights | Score: 0.6144 | Reasons: matched mood; tempo is close; valence is close; danceability is close
- Neon Skyline | Score: 0.3838 | Reasons: energy is close; tempo is close; danceability is close; acousticness is close
- Midnight Streets | Score: 0.3474 | Reasons: danceability is close; acousticness is close
```

### Calm Chill

```text
Top recommendations:
- Library Rain | Score: 0.9965 | Reasons: matched genre; matched mood; energy is close; tempo is close; valence is close; danceability is close; acousticness is close
- Midnight Coding | Score: 0.9773 | Reasons: matched genre; matched mood; energy is close; tempo is close; valence is close; danceability is close
- Focus Flow | Score: 0.7343 | Reasons: matched genre; energy is close; tempo is close; valence is close; danceability is close; acousticness is close
- Spacewalk Thoughts | Score: 0.6178 | Reasons: matched mood; energy is close; valence is close; acousticness is close
- Coffee Shop Stories | Score: 0.3766 | Reasons: energy is close; danceability is close; acousticness is close
```

### High-Energy Rock

```text
Top recommendations:
- Storm Runner | Score: 0.9932 | Reasons: matched genre; matched mood; energy is close; tempo is close; valence is close; danceability is close; acousticness is close
- Gym Hero | Score: 0.5992 | Reasons: matched mood; energy is close; acousticness is close
- Neon Skyline | Score: 0.3583 | Reasons: energy is close; acousticness is close
- Night Drive Loop | Score: 0.3428 | Reasons: valence is close; danceability is close
- Signal Bloom | Score: 0.3349 | Reasons: danceability is close
```

### Adversarial profile

```text
Top recommendations:
- Signal Bloom | Score: 0.6710 | Reasons: matched genre; danceability is close
- Winter Glass | Score: 0.4728 | Reasons: matched mood
- Storm Runner | Score: 0.3630 | Reasons: energy is close; tempo is close; danceability is close; acousticness is close
- Neon Skyline | Score: 0.3455 | Reasons: energy is close; tempo is close; acousticness is close
- Gym Hero | Score: 0.3364 | Reasons: energy is close; tempo is close
```

The recommendations felt accurate for the strongest matches. Sunrise City did well for High-Energy Pop, Library Rain did well for Calm Chill, and Storm Runner did well for High-Energy Rock.

One surprising result was Gym Hero appearing for the rock profile. Its energy and danceability helped it score well even though it was not a rock song.

I also ran a temporary weight experiment. I reduced genre weight from 0.35 to 0.175 and increased energy weight from 0.15 to 0.30. The temporary weights added to 0.975, so the raw maximum score changed slightly, but songs could still be ranked. High-energy songs became more competitive. I restored the original weights after the experiment.

The plain-language comparisons were also useful. High-Energy Pop and Calm Chill split mainly on energy, mood, tempo, and acousticness. High-Energy Pop and High-Energy Rock shared high energy, but the pop profile favored happier mood and brighter valence. Calm Chill and High-Energy Rock diverged most strongly in genre, mood, and acousticness.

The project also includes 2 tests, and the current implementation passed them.

---

## 7. Intended Use

This system is appropriate for:

- classroom learning
- showing how content-based recommendation works
- practicing scoring, ranking, testing, and documentation
- small fictional music catalogs

---

## 8. Non-Intended Use

This system should not be used for:

- real commercial music recommendations
- making claims about a person’s full musical identity
- high-stakes decisions
- recommendations that require real listening history or large-scale user behavior
- replacing real streaming-platform recommendation systems

---

## 9. Ideas for Improvement

Several improvements would make this system more useful.

- Add more songs, artists, genres, and moods.
- Learn weights from user feedback instead of choosing them manually.
- Add diversity rules so the results are less repetitive.
- Use listening history, skips, likes, and replays.
- Combine content-based filtering with collaborative filtering.
- Recognize related genres and moods instead of requiring exact matches.

---

## 10. Personal Reflection

My biggest learning moment was seeing how raw song features and user preferences can be turned into scores and rankings. It was helpful to watch the math turn simple inputs into something that looked personal.

AI tools helped me brainstorm formulas, generate diverse song ideas, explain the code, and point out possible bias. I still double-checked the math, the weights, the CSV formatting, the terminal output, the Git changes, and the test results.

What surprised me most was how a simple weighted formula could feel personal at all. I also saw that small weight changes could noticeably change the rankings. Next, I would try collaborative filtering, listening history, learned weights, larger datasets, and diversity-aware rankings.

