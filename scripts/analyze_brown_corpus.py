from __future__ import annotations

import os
import random
import re
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

CACHE_DIR = PROJECT_ROOT / ".cache"
CACHE_DIR.mkdir(exist_ok=True)
os.environ.setdefault("XDG_CACHE_HOME", str(CACHE_DIR))
os.environ.setdefault("MPLCONFIGDIR", str(CACHE_DIR / "matplotlib"))

import matplotlib

from nltk import download
from nltk.corpus import brown
from nltk.data import find

from lexical_diversity import lex_div as ld


RESULTS_DIR = PROJECT_ROOT / "results"
TOKEN_PATTERN = re.compile(r"[a-z]+(?:'[a-z]+)?")
RANDOM_SEED = 42
ROBUST_METRICS = ["ttr", "mattr", "hdd", "mtld"]
ALL_METRICS = [
    "ttr",
    "root_ttr",
    "log_ttr",
    "maas_ttr",
    "msttr",
    "mattr",
    "hdd",
    "mtld",
]


def ensure_brown_corpus() -> None:
    try:
        find("corpora/brown")
    except LookupError:
        download("brown", quiet=True)


def normalize_token(token: str) -> str | None:
    match = TOKEN_PATTERN.fullmatch(token.lower())
    if match:
        return match.group(0)

    cleaned = re.sub(r"[^a-z']", "", token.lower()).strip("'")
    return cleaned or None


def load_genre_tokens(category: str) -> list[str]:
    tokens: list[str] = []
    for token in brown.words(categories=category):
        normalized = normalize_token(token)
        if normalized:
            tokens.append(normalized)
    return tokens


def compute_metrics(tokens: list[str]) -> dict[str, float | int | str]:
    return {
        "tokens": len(tokens),
        "types": len(set(tokens)),
        "ttr": ld.ttr(tokens),
        "root_ttr": ld.root_ttr(tokens),
        "log_ttr": ld.log_ttr(tokens),
        "maas_ttr": ld.maas_ttr(tokens),
        "msttr": ld.msttr(tokens),
        "mattr": ld.mattr(tokens),
        "hdd": ld.hdd(tokens),
        "mtld": ld.mtld(tokens),
    }


def build_results() -> pd.DataFrame:
    rows = []
    for category in brown.categories():
        tokens = load_genre_tokens(category)
        row = {"genre": category}
        row.update(compute_metrics(tokens))
        rows.append(row)

    df = pd.DataFrame(rows).sort_values("genre").reset_index(drop=True)
    df["type_token_ratio_pct"] = (df["ttr"] * 100).round(2)
    df["length_rank"] = df["tokens"].rank(method="dense", ascending=False).astype(int)
    df["mtld_rank"] = df["mtld"].rank(method="dense", ascending=False).astype(int)
    df["hdd_rank"] = df["hdd"].rank(method="dense", ascending=False).astype(int)
    df["mattr_rank"] = df["mattr"].rank(method="dense", ascending=False).astype(int)
    return df


def save_results(df: pd.DataFrame) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    csv_path = RESULTS_DIR / "genre_lexical_diversity.csv"
    df.to_csv(csv_path, index=False, float_format="%.6f")


def build_metric_rankings(df: pd.DataFrame) -> pd.DataFrame:
    ranking_rows = []
    for metric in ALL_METRICS:
        top_three = df.nlargest(3, metric)[["genre", metric]]
        bottom_three = df.nsmallest(3, metric)[["genre", metric]]

        for rank, row in enumerate(top_three.itertuples(index=False), start=1):
            ranking_rows.append(
                {
                    "metric": metric,
                    "group": "top",
                    "rank": rank,
                    "genre": row.genre,
                    "score": getattr(row, metric),
                }
            )
        for rank, row in enumerate(bottom_three.itertuples(index=False), start=1):
            ranking_rows.append(
                {
                    "metric": metric,
                    "group": "bottom",
                    "rank": rank,
                    "genre": row.genre,
                    "score": getattr(row, metric),
                }
            )
    return pd.DataFrame(ranking_rows)


def build_metric_correlations(df: pd.DataFrame) -> pd.DataFrame:
    corr = df[["tokens", "types", *ALL_METRICS]].corr(numeric_only=True)
    return corr.round(6)


def build_composite_scores(df: pd.DataFrame) -> pd.DataFrame:
    composite = df[["genre", "tokens", "types", "mattr", "hdd", "mtld"]].copy()
    for metric in ["mattr", "hdd", "mtld"]:
        mean = composite[metric].mean()
        std = composite[metric].std(ddof=0)
        composite[f"{metric}_zscore"] = 0.0 if std == 0 else (composite[metric] - mean) / std

    composite["composite_diversity_score"] = (
        composite["mattr_zscore"] + composite["hdd_zscore"] + composite["mtld_zscore"]
    ) / 3
    composite["composite_rank"] = (
        composite["composite_diversity_score"].rank(method="dense", ascending=False).astype(int)
    )
    return composite.sort_values("composite_rank").reset_index(drop=True)


def build_stability_analysis(
    genre_tokens: dict[str, list[str]], window_size: int = 10000, samples_per_genre: int = 10
) -> pd.DataFrame:
    rng = random.Random(RANDOM_SEED)
    rows = []

    for genre, tokens in genre_tokens.items():
        max_start = len(tokens) - window_size
        for sample_id in range(1, samples_per_genre + 1):
            start_index = 0 if max_start <= 0 else rng.randint(0, max_start)
            sample = tokens[start_index : start_index + window_size]
            rows.append(
                {
                    "genre": genre,
                    "sample_id": sample_id,
                    "window_size": len(sample),
                    "ttr": ld.ttr(sample),
                    "mattr": ld.mattr(sample),
                    "hdd": ld.hdd(sample),
                    "mtld": ld.mtld(sample),
                }
            )

    sample_df = pd.DataFrame(rows)
    summary_rows = []
    for metric in ROBUST_METRICS:
        grouped = sample_df.groupby("genre")[metric]
        metric_summary = grouped.agg(["mean", "std", "min", "max"]).reset_index()
        metric_summary["metric"] = metric
        metric_summary["range"] = metric_summary["max"] - metric_summary["min"]
        metric_summary["coefficient_of_variation"] = (
            metric_summary["std"] / metric_summary["mean"]
        ).fillna(0.0)
        summary_rows.append(metric_summary)

    stability_df = pd.concat(summary_rows, ignore_index=True)
    return sample_df, stability_df[
        ["genre", "metric", "mean", "std", "min", "max", "range", "coefficient_of_variation"]
    ].sort_values(["metric", "coefficient_of_variation", "genre"]).reset_index(drop=True)


def build_summary(df: pd.DataFrame) -> str:
    highest_mtld = df.nlargest(3, "mtld")[["genre", "mtld"]]
    highest_hdd = df.nlargest(3, "hdd")[["genre", "hdd"]]
    lowest_mtld = df.nsmallest(3, "mtld")[["genre", "mtld"]]
    correlation = df["tokens"].corr(df["ttr"])
    composite = build_composite_scores(df).head(3)

    summary_lines = [
        "# Brown Corpus Lexical Diversity Summary",
        "",
        "## Dataset",
        f"- Genres analysed: {len(df)}",
        f"- Total tokens analysed: {int(df['tokens'].sum())}",
        "- Corpus source: NLTK Brown Corpus",
        "",
        "## Key Findings",
        (
            f"- Highest MTLD genres: "
            + ", ".join(
                f"{row.genre} ({row.mtld:.2f})" for row in highest_mtld.itertuples(index=False)
            )
        ),
        (
            f"- Highest HDD genres: "
            + ", ".join(
                f"{row.genre} ({row.hdd:.3f})" for row in highest_hdd.itertuples(index=False)
            )
        ),
        (
            f"- Lowest MTLD genres: "
            + ", ".join(
                f"{row.genre} ({row.mtld:.2f})" for row in lowest_mtld.itertuples(index=False)
            )
        ),
        (
            f"- Token count vs TTR correlation: {correlation:.3f}. "
            "This negative relationship shows why raw TTR is length-sensitive."
        ),
        (
            "- Short genres such as humor and science_fiction look unusually strong on plain TTR, "
            "while MTLD, MATTR, and HDD give a more stable comparison across unequal genre lengths."
        ),
        (
            "- Composite score leaders (MATTR + HDD + MTLD z-scores): "
            + ", ".join(
                f"{row.genre} ({row.composite_diversity_score:.3f})"
                for row in composite.itertuples(index=False)
            )
        ),
        "",
        "## Interpretation",
        (
            "- Reviews and humor show the strongest lexical variety on the more robust metrics, "
            "suggesting denser vocabulary reuse patterns and broader word choice within shorter texts."
        ),
        (
            "- Government and learned writing score lower on MTLD despite large token counts, "
            "which is consistent with more repetitive technical and topic-focused vocabulary."
        ),
        (
            "- For an NLP classroom project, MATTR, HDD, and MTLD are the best headline metrics "
            "because they are less distorted by document length than simple TTR."
        ),
    ]
    return "\n".join(summary_lines) + "\n"


def save_summary(summary: str) -> None:
    summary_path = RESULTS_DIR / "summary.md"
    summary_path.write_text(summary, encoding="utf-8")


def save_tables(
    df: pd.DataFrame,
    rankings_df: pd.DataFrame,
    corr_df: pd.DataFrame,
    composite_df: pd.DataFrame,
    stability_samples_df: pd.DataFrame,
    stability_summary_df: pd.DataFrame,
) -> None:
    df.to_csv(RESULTS_DIR / "genre_lexical_diversity.csv", index=False, float_format="%.6f")
    rankings_df.to_csv(RESULTS_DIR / "metric_rankings.csv", index=False, float_format="%.6f")
    corr_df.to_csv(RESULTS_DIR / "metric_correlations.csv", float_format="%.6f")
    composite_df.to_csv(RESULTS_DIR / "composite_diversity_scores.csv", index=False, float_format="%.6f")
    stability_samples_df.to_csv(RESULTS_DIR / "stability_samples.csv", index=False, float_format="%.6f")
    stability_summary_df.to_csv(
        RESULTS_DIR / "stability_summary.csv", index=False, float_format="%.6f"
    )


def save_plots(df: pd.DataFrame, composite_df: pd.DataFrame, stability_summary_df: pd.DataFrame) -> None:
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    top_mtld = df.sort_values("mtld", ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(top_mtld["genre"], top_mtld["mtld"], color="#2f6f9f")
    ax.set_title("Brown Corpus Genres by MTLD")
    ax.set_xlabel("Genre")
    ax.set_ylabel("MTLD")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "mtld_by_genre.png", dpi=200)
    plt.close(fig)

    compare_df = df.sort_values("mattr", ascending=False)
    fig, ax = plt.subplots(figsize=(12, 6))
    x = range(len(compare_df))
    ax.plot(x, compare_df["mattr"], marker="o", linewidth=2, label="MATTR", color="#d95f02")
    ax.plot(x, compare_df["hdd"], marker="s", linewidth=2, label="HDD", color="#1b9e77")
    ax.set_title("MATTR and HDD Comparison Across Genres")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Score")
    ax.set_xticks(list(x))
    ax.set_xticklabels(compare_df["genre"], rotation=45)
    ax.legend()
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "mattr_hdd_comparison.png", dpi=200)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(
        composite_df["genre"],
        composite_df["composite_diversity_score"],
        color="#6a4c93",
    )
    ax.set_title("Composite Lexical Diversity Score by Genre")
    ax.set_xlabel("Genre")
    ax.set_ylabel("Composite score")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "composite_diversity_score.png", dpi=200)
    plt.close(fig)

    variability = (
        stability_summary_df.groupby("metric")["coefficient_of_variation"].mean().reset_index()
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(variability["metric"], variability["coefficient_of_variation"], color="#3a7d44")
    ax.set_title("Average Relative Variability Across Repeated 10k-Token Samples")
    ax.set_xlabel("Metric")
    ax.set_ylabel("Mean coefficient of variation")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "metric_stability_comparison.png", dpi=200)
    plt.close(fig)


def main() -> None:
    ensure_brown_corpus()
    genre_tokens = {category: load_genre_tokens(category) for category in brown.categories()}
    df = pd.DataFrame(
        [{"genre": genre, **compute_metrics(tokens)} for genre, tokens in genre_tokens.items()]
    ).sort_values("genre").reset_index(drop=True)
    df["type_token_ratio_pct"] = (df["ttr"] * 100).round(2)
    df["length_rank"] = df["tokens"].rank(method="dense", ascending=False).astype(int)
    df["mtld_rank"] = df["mtld"].rank(method="dense", ascending=False).astype(int)
    df["hdd_rank"] = df["hdd"].rank(method="dense", ascending=False).astype(int)
    df["mattr_rank"] = df["mattr"].rank(method="dense", ascending=False).astype(int)

    rankings_df = build_metric_rankings(df)
    corr_df = build_metric_correlations(df)
    composite_df = build_composite_scores(df)
    stability_samples_df, stability_summary_df = build_stability_analysis(genre_tokens)

    save_tables(df, rankings_df, corr_df, composite_df, stability_samples_df, stability_summary_df)
    save_summary(build_summary(df))
    save_plots(df, composite_df, stability_summary_df)
    print(f"Saved analysis outputs to {RESULTS_DIR}")


if __name__ == "__main__":
    main()
