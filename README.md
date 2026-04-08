# Lexical Diversity Measurement Across Genres

This repository has been adapted into a complete NLP course project based on the Brown Corpus. The project compares lexical diversity across genres, includes a literature-backed survey section, and adds a stability experiment to show why robust metrics such as MATTR, HDD, and MTLD are more reliable than simple Type-Token Ratio (TTR).

## Project Overview

- **Title:** Lexical Diversity Measurement Across Genres
- **Subject Area:** Natural Language Processing
- **Objective:** Measure and compare lexical diversity across Brown Corpus genres
- **Dataset:** Brown Corpus from NLTK, also available from Kaggle: https://www.kaggle.com/datasets/nltkdata/brown-corpus

## Research Goal

The project answers the following question:

**How does lexical diversity vary across genres, and which metrics provide the most reliable comparison when genre sizes are different?**

## Methodology

1. Load each Brown Corpus genre.
2. Normalize tokens by lowercasing and removing non-word noise.
3. Compute lexical diversity metrics for every genre.
4. Compare the genres using both classic and more stable metrics.
5. Build deeper analysis tables such as rankings, correlations, and composite scores.
6. Run an innovation experiment using repeated equal-length sampling.
7. Save the outputs as CSV tables, charts, and a short written summary.

## Metrics Used

The analysis script calculates the following metrics:

- TTR
- Root TTR
- Log TTR
- Maas TTR
- MSTTR
- MATTR
- HDD
- MTLD

## Project Structure

```text
lexical_diversity/
├── lexical_diversity/                 # Original lexical diversity metric package
├── scripts/
│   └── analyze_brown_corpus.py        # Main project analysis script
├── results/                           # Generated CSV, summary, and plots
├── ABSTRACT.md
├── PROJECT_REPORT.md
├── README.md
├── requirements.txt
├── TITLE_PAGE.txt
├── LITERATURE_REVIEW.txt
└── PPT_OUTLINE.txt
```

## How To Run

Install the dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run the project:

```bash
python3 scripts/analyze_brown_corpus.py
```

The script will:

- download the Brown Corpus through NLTK if it is not already installed
- generate a CSV file with lexical diversity scores for each genre
- generate ranking, correlation, composite-score, and stability-analysis tables
- generate a short text summary
- generate comparison plots in the `results/` folder

## Output Files

After running the script, you will find:

- `results/genre_lexical_diversity.csv`
- `results/metric_rankings.csv`
- `results/metric_correlations.csv`
- `results/composite_diversity_scores.csv`
- `results/stability_samples.csv`
- `results/stability_summary.csv`
- `results/summary.txt`
- `results/mtld_by_genre.png`
- `results/mattr_hdd_comparison.png`
- `results/composite_diversity_score.png`
- `results/metric_stability_comparison.png`
- `LITERATURE_REVIEW.txt`
- `PROJECT_REPORT.md`
- `ABSTRACT.md`
- `TITLE_PAGE.txt`
- `PPT_OUTLINE.txt`

## Initial Findings

From the generated Brown Corpus results in this repository:

- `reviews` and `humor` score highest on robust diversity measures such as MTLD and MATTR
- `government` and `learned` score lower on MTLD, showing heavier vocabulary repetition
- simple TTR favors shorter genres such as `humor` and `science_fiction`, so it should not be used alone for fair comparison
- the new composite ranking places `humor`, `reviews`, and `science_fiction` at the top overall
- the stability experiment shows that `HDD` and `MATTR` are more stable than `TTR` across repeated equal-length samples

## Conclusion

This project shows that lexical diversity changes meaningfully across genres, but the interpretation depends strongly on the metric used. MATTR, HDD, and MTLD are better choices than raw TTR when comparing corpora of unequal lengths.

## Note About The Original Repo

This repository started as a cloned lexical-diversity package. It has now been reshaped into a course-project repo by adding:

- Brown Corpus genre analysis
- literature review with citations
- assignment-focused documentation
- stronger analysis tables and generated visualizations
- an innovation feature based on repeated-sampling stability analysis
- small package cleanup for compatibility
