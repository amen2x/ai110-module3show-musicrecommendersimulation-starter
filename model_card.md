# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeMatch 1.0**

This is a simple, manually weighted content-based music recommender for a small classroom dataset.

---

## 2. Intended Use

This recommender is designed to suggest songs that seem to match a user’s stated musical preferences. It is intended for educational use, small demonstrations, and simple experimentation with recommender ideas.

It is appropriate for:

- Showing how a recommender can turn song features into a ranked list
- Comparing different taste profiles such as upbeat pop, calm chill, or high-energy rock
- Explaining why a song was recommended

It should not be relied on for:

- Real-world music discovery at scale
- Personalized recommendations for actual users without additional data
- Decisions about music taste, identity, or long-term listening habits

---

## 3. How the Model Works

The recommender uses content-based filtering. It loads songs from the dataset and compares each song to a user profile using the song’s genre, mood, energy, tempo, valence, danceability, and acousticness.

The system uses a weighted scoring rule. Genre and mood receive the largest weights because they are the strongest simple clues about a song’s general feel. The other features add smaller amounts of support. The score is higher when a song’s numerical features are closer to the user’s preferred values.

The model also separates two steps:

- Scoring: It calculates how well one song matches the user profile.
- Ranking: It sorts all songs from highest score to lowest score and returns the best matches.

Tempo is normalized to a 0–1 scale so it can be compared more fairly with other features that already range from 0 to 1. This makes the scoring logic easier to implement and explain.

The system does not directly use the song ID, title, or artist in the score. Those fields help identify the song, but they do not describe its musical qualities in the same way that genre, mood, and the numeric audio-like features do.

---

## 4. Data

The recommender uses the dataset in [data/songs.csv](data/songs.csv). The catalog contains 10 songs with the following fields:

- genre
- mood
- energy
- tempo_bpm
- valence
- danceability
- acousticness

The dataset includes a small mix of styles such as pop, lofi, rock, ambient, jazz, synthwave, and indie pop. The moods include happy, chill, intense, relaxed, moody, and focused.

This dataset is small and hand-built. It does not capture the full range of modern music, and it does not include real listening-history data, lyrics, vocals, or detailed production information.

---

## 5. Strengths

The system works reasonably well for the clearest cases. It gives strong results when the user profile and the song share the same genre and mood. For example:

- An upbeat pop listener is well matched by songs such as Sunrise City and Gym Hero.
- A calm/chill listener is well matched by Midnight Coding and Library Rain.
- A high-energy rock listener is well matched by Storm Runner.

The scoring rule also produces understandable explanations. This makes it easy for beginners to see why a song was recommended.

---

## 6. Limitations and Bias

This recommender has several important limitations. The dataset is small, with only 19 songs, so the recommendations are limited to a narrow catalog and can feel repetitive. The feature weights are manually chosen rather than learned from real user feedback, so the behavior is easy to explain but not necessarily optimal. The model uses exact matches for genre and mood, which makes it simpler but also means it can miss songs that are stylistically appropriate but do not share the exact label. Because genre and mood carry the largest weights, the recommender can repeatedly suggest similar songs and create a filter-bubble effect. It can also recommend songs that match numerically but not stylistically, especially when the user has conflicting preferences such as a strong genre request combined with an energy profile that points elsewhere.

---

## 7. Evaluation

I evaluated the recommender by testing three main profiles and one adversarial profile:

- High-Energy Pop
- Calm Chill
- High-Energy Rock
- Adversarial Conflicting

### Main profile results

High-Energy Pop:

```text
Top recommendations:
- Sunrise City | Score: 0.9757 | Reasons: matched genre; matched mood; energy is close; tempo is close; valence is close; acousticness is close
- Gym Hero | Score: 0.7321 | Reasons: matched genre; energy is close; tempo is close; valence is close; danceability is close; acousticness is close
- Rooftop Lights | Score: 0.6144 | Reasons: matched mood; tempo is close; valence is close; danceability is close
- Neon Skyline | Score: 0.3838 | Reasons: energy is close; tempo is close; danceability is close; acousticness is close
- Midnight Streets | Score: 0.3474 | Reasons: danceability is close; acousticness is close
```

Calm Chill:

```text
Top recommendations:
- Library Rain | Score: 0.9965 | Reasons: matched genre; matched mood; energy is close; tempo is close; valence is close; danceability is close; acousticness is close
- Midnight Coding | Score: 0.9773 | Reasons: matched genre; matched mood; energy is close; tempo is close; valence is close; danceability is close
- Focus Flow | Score: 0.7343 | Reasons: matched genre; energy is close; tempo is close; valence is close; danceability is close; acousticness is close
- Spacewalk Thoughts | Score: 0.6178 | Reasons: matched mood; energy is close; valence is close; acousticness is close
- Coffee Shop Stories | Score: 0.3766 | Reasons: energy is close; danceability is close; acousticness is close
```

High-Energy Rock:

```text
Top recommendations:
- Storm Runner | Score: 0.9932 | Reasons: matched genre; matched mood; energy is close; tempo is close; valence is close; danceability is close; acousticness is close
- Gym Hero | Score: 0.5992 | Reasons: matched mood; energy is close; acousticness is close
- Neon Skyline | Score: 0.3583 | Reasons: energy is close; acousticness is close
- Night Drive Loop | Score: 0.3428 | Reasons: valence is close; danceability is close
- Signal Bloom | Score: 0.3349 | Reasons: danceability is close
```

### Adversarial profile results

Adversarial Conflicting:

```text
Top recommendations:
- Signal Bloom | Score: 0.6710 | Reasons: matched genre; danceability is close
- Winter Glass | Score: 0.4728 | Reasons: matched mood
- Storm Runner | Score: 0.3630 | Reasons: energy is close; tempo is close; danceability is close; acousticness is close
- Neon Skyline | Score: 0.3455 | Reasons: energy is close; tempo is close; acousticness is close
- Gym Hero | Score: 0.3364 | Reasons: energy is close; tempo is close
```

The adversarial profile revealed that the model can still produce sensible results when the user’s requested genre and mood conflict with a very different energy profile. In this case, Signal Bloom ranked first because it matched the requested alternative genre exactly, while Winter Glass ranked second because it matched the requested sad mood exactly. The other songs were boosted by shared energy or tempo values.

### What felt accurate

The recommendations felt accurate for the clear matches. High-Energy Pop ranked Sunrise City first, Calm Chill ranked Library Rain first, and High-Energy Rock ranked Storm Runner first. Those results matched the intended genre and mood well.

A surprising result was that Gym Hero appeared in the top results for the rock profile. Its high energy and strong danceability helped it score well even though its genre was pop, which shows the model can overvalue numeric similarity over genre differences.

### Why one song ranked first using the weights

Storm Runner ranked first for the High-Energy Rock profile because it matched both the requested genre and mood exactly. With the original weights, genre and mood together contribute 0.60 of the total score, so an exact match on both features is very powerful. Its energy and tempo also matched closely, which pushed the final score even higher.

### Temporary weight experiment

I also tested a temporary weight change where genre was reduced from 0.35 to 0.175 and energy was increased from 0.15 to 0.30. The temporary weights summed to 0.975, so the maximum raw score changed slightly, but songs could still be ranked and compared normally. The biggest effect was that energy-heavy songs became more competitive, especially for profiles that valued intensity or movement over exact genre matching.

### Plain-language comparisons

- High-Energy Pop compared with Calm Chill: the pop profile favored songs with brighter energy, happier mood, and more upbeat tempo, while the chill profile favored lower energy, calmer mood, and more acoustic qualities.
- High-Energy Pop compared with High-Energy Rock: both profiles liked high energy, but the pop profile favored happier mood and more upbeat valence, while the rock profile favored intense mood and a stronger rock-style match.
- Calm Chill compared with High-Energy Rock: these profiles diverged most strongly in genre, mood, and acousticness. The chill profile preferred lower-energy, more acoustic songs, while the rock profile preferred higher-energy and more intense tracks.

The project also includes 2 tests, and the current implementation passed them.

---

## 8. Future Work

Several improvements would make this system more useful and less repetitive.

- Add more songs and more genres to the catalog.
- Learn feature weights from user feedback instead of using hand-picked values.
- Add diversity to the ranking so the top results do not all look too similar.
- Use listening history, skips, replays, and likes if available.
- Combine content-based filtering with collaborative filtering to improve discovery and personalization.

---

## 9. Personal Reflection

This project taught me that recommendation systems are really about turning simple data into useful predictions. I learned that genre and mood are very helpful signals, but numeric features such as energy and tempo also matter for how a song feels.

The biggest challenge was balancing simplicity with usefulness. The current system is easy to explain, but it is also limited. Testing multiple profiles helped show where the system works well and where it can be too narrow or too dependent on a few features. With more time, I would improve the ranking with diversity and add more data so the recommendations could feel more realistic and less repetitive.

