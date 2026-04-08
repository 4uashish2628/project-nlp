# Project Report

## Title

Lexical Diversity Measurement Across Genres

## Objective

The objective of this NLP project is to measure lexical diversity across Brown Corpus genres and evaluate which metrics are most reliable when texts differ in length. The project also includes an innovation component that tests metric stability through repeated equal-length sampling.

## Dataset

- **Corpus:** Brown Corpus
- **Source:** NLTK Brown Corpus
- **Reference dataset page:** https://www.kaggle.com/datasets/nltkdata/brown-corpus
- **Genres analysed:** 15
- **Total normalized tokens analysed:** 1,005,119

## Survey Of Prior Work

Lexical diversity is widely used in corpus linguistics, NLP, and discourse analysis, but the literature warns that not all diversity measures behave equally well. The Brown Corpus is an appropriate benchmark because it was designed as a balanced, genre-diverse corpus of edited American English, making it useful for genre comparison [1].

The classic Type-Token Ratio (TTR) is easy to calculate, but it is strongly affected by text length. Covington and McFall introduced MATTR specifically to address this issue by averaging TTR across a moving window [2]. McCarthy and Jarvis validated MTLD and HD-D as stronger alternatives to older diversity measures and reported that MTLD was notably resistant to length effects in their validation study [3]. Fergadiotis, Wright, and Green later showed that MTLD and MATTR performed strongly in psychometric evaluation, again highlighting the need to move beyond raw TTR [4]. Jarvis further argued that lexical diversity should be treated as a broader construct, not as a single formula, which supports using several complementary metrics together [5].

This project follows that literature directly by using multiple indices and by testing whether the more robust metrics remain stable under controlled sample sizes.

## Method

1. Load all Brown Corpus genres.
2. Normalize tokens by lowercasing and removing token noise.
3. Compute lexical diversity scores for each genre.
4. Rank the genres using classic and robust metrics.
5. Generate analysis tables, plots, and a written summary.
6. Run an innovation experiment using repeated 10,000-token windows from each genre.

## Metrics Used

- TTR
- Root TTR
- Log TTR
- Maas TTR
- MSTTR
- MATTR
- HDD
- MTLD

## Core Results

### Top Genres On Robust Measures

| Metric | Rank 1 | Rank 2 | Rank 3 |
|---|---|---|---|
| MATTR | humor (0.827) | reviews (0.827) | adventure (0.819) |
| HDD | science_fiction (0.881) | humor (0.878) | romance (0.877) |
| MTLD | reviews (120.40) | humor (113.98) | adventure (105.34) |

### Lowest Genres On Robust Measures

| Metric | Lowest 1 | Lowest 2 | Lowest 3 |
|---|---|---|---|
| MATTR | government (0.767) | learned (0.776) | religion (0.787) |
| HDD | government (0.852) | learned (0.855) | religion (0.858) |
| MTLD | government (65.43) | learned (69.58) | religion (76.71) |

### Composite Diversity Ranking

To avoid depending on one metric alone, the project also computes a composite diversity score by averaging z-scores from MATTR, HDD, and MTLD.

| Rank | Genre | Composite Score |
|---|---|---|
| 1 | humor | 1.172 |
| 2 | reviews | 1.080 |
| 3 | science_fiction | 0.872 |
| 4 | adventure | 0.646 |
| 5 | news | 0.542 |

## Analysis

The strongest practical result is that raw TTR remains highly length-sensitive in this corpus. The correlation between token count and TTR is `-0.764`, which confirms that longer genres are unfairly penalized when TTR is used alone. This matches the literature and justifies shifting the interpretation toward MATTR, HDD, and MTLD.

The genre patterns are also meaningful. `reviews` and `humor` consistently rank near the top across the robust measures, suggesting broader vocabulary variety and less repetitive lexical reuse. By contrast, `government` and `learned` stay near the bottom, which is consistent with dense topic-specific and technical vocabulary.

The correlation table also shows that MATTR and MSTTR are almost identical in this dataset (`0.9995` correlation), while MATTR and MTLD are also strongly aligned (`0.9757`). This supports the conclusion that the robust measures are capturing a similar signal, even though they are computed differently.

## Innovation Feature

The innovation in this project is a **metric stability experiment**. Instead of only computing lexical diversity once per genre, the script repeatedly samples 10,000-token windows from each genre and recomputes TTR, MATTR, HDD, and MTLD. This makes it possible to compare the relative stability of different metrics under controlled text lengths.

### Stability Results

Average coefficient of variation across repeated samples:

| Metric | Mean CV |
|---|---|
| HDD | 0.0071 |
| MATTR | 0.0093 |
| TTR | 0.0462 |
| MTLD | 0.0678 |

These results show that HDD and MATTR are the most stable in the repeated-sampling experiment, while TTR varies much more. This is a strong empirical justification for preferring robust measures when comparing genres.

## Conclusion

This project demonstrates that lexical diversity differs clearly across Brown Corpus genres, but the interpretation depends strongly on the chosen metric. MATTR, HDD, and MTLD are better choices than raw TTR for cross-genre comparison, and the added stability experiment strengthens that claim using direct evidence from the project dataset itself.

## Files Produced

- `results/genre_lexical_diversity.csv`
- `results/metric_rankings.csv`
- `results/metric_correlations.csv`
- `results/composite_diversity_scores.csv`
- `results/stability_samples.csv`
- `results/stability_summary.csv`
- `results/summary.md`
- `results/mtld_by_genre.png`
- `results/mattr_hdd_comparison.png`
- `results/composite_diversity_score.png`
- `results/metric_stability_comparison.png`

## References

[1] Francis, W. N., & Kucera, H. Brown Corpus description. CoRD Brown Corpus page. https://varieng.helsinki.fi/CoRD/corpora/BROWN/

[2] Covington, M. A., & McFall, J. D. (2010). *Cutting the Gordian Knot: The Moving-Average Type-Token Ratio (MATTR).* Journal of Quantitative Linguistics, 17(2), 94-100. https://doi.org/10.1080/09296171003643098

[3] McCarthy, P. M., & Jarvis, S. (2010). *MTLD, vocd-D, and HD-D: A validation study of sophisticated approaches to lexical diversity assessment.* Behavior Research Methods, 42(2), 381-392. https://doi.org/10.3758/BRM.42.2.381

[4] Fergadiotis, G., Wright, H. H., & Green, S. B. (2015). *Psychometric evaluation of lexical diversity indices: Assessing length effects.* Journal of Speech, Language, and Hearing Research, 58(3), 840-852. https://doi.org/10.1044/2015_JSLHR-L-14-0280

[5] Jarvis, S. (2013). *Capturing the Diversity in Lexical Diversity.* Language Learning, 63(S1), 87-106. https://doi.org/10.1111/j.1467-9922.2012.00739.x
