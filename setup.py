from pathlib import Path

from setuptools import find_packages, setup


PROJECT_ROOT = Path(__file__).resolve().parent
README_PATH = PROJECT_ROOT / "README.md"
REQUIREMENTS_PATH = PROJECT_ROOT / "requirements.txt"


def read_requirements() -> list[str]:
    return [
        line.strip()
        for line in REQUIREMENTS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


setup(
    name="lexical-diversity-project",
    version="1.0.0",
    author="Ashish Singh",
    author_email="ashish2628singh@gmail.com",
    description="NLP project for measuring lexical diversity across Brown Corpus genres",
    long_description=README_PATH.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=find_packages(include=["lexical_diversity", "lexical_diversity.*"]),
    include_package_data=True,
    install_requires=read_requirements(),
    python_requires=">=3.9",
    license="MIT",
    project_urls={
        "Dataset": "https://www.kaggle.com/datasets/nltkdata/brown-corpus",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
    ],
)
