# Abstract

This project studies lexical diversity across genres using the Brown Corpus, a balanced collection of American English texts. The main goal is to compare how vocabulary variation changes from one genre to another and to determine which lexical diversity metrics provide the most reliable comparison when text lengths are unequal.

The implementation uses Python with NLTK for corpus access and applies multiple lexical diversity measures, including TTR, Root TTR, Log TTR, Maas TTR, MSTTR, MATTR, HDD, and MTLD. In addition to computing genre-level scores, the project generates ranking tables, correlation tables, composite diversity scores, and visualizations for interpretation.

The analysis shows that raw TTR is strongly length-sensitive, with a token-count correlation of `-0.764`, making it unreliable for fair comparison across genres. More robust measures such as MATTR, HDD, and MTLD provide more meaningful results. Genres such as `humor` and `reviews` show consistently high lexical diversity, while `government` and `learned` show lower diversity due to more repetitive and topic-specific vocabulary.

As an innovation feature, the project introduces a repeated equal-length sampling experiment using 10,000-token windows from each genre. This stability analysis demonstrates that HDD and MATTR are more stable than TTR under controlled sample lengths, strengthening the practical justification for using robust lexical diversity metrics in genre-based NLP studies.
