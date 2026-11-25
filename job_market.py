"""
job_market.py
The JobMarket class: loads ALL the postings and analyzes them.
Owner: Renad (clean() owned by Madi)
"""
from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pandas as pd

from job_posting import JobPosting


def _value_or_none(value: object) -> object | None:
    """pandas uses NaN for missing values; turn those into None so they're easier to check."""
    return None if pd.isna(value) else value


class JobMarket:
    """Holds a list of JobPosting objects and answers questions about them."""

    def __init__(self) -> None:
        """Start with an empty list of postings; load_from_csv() fills it."""
        self.postings: list[JobPosting] = []

    # ---------- Loading & cleaning ----------

    def load_from_csv(self, path: str, nrows: int | None = 5000) -> None:
        """Read the CSV with pandas, clean it, and create one JobPosting per row."""
        df = pd.read_csv(path, nrows=nrows)
        df = self.clean(df)

        for row in df.itertuples(index=False):
            posting = JobPosting(
                job_id=row.job_id,
                title=row.title,
                company=_value_or_none(row.company_name),
                location=row.location,
                description=row.description,
                min_salary=_value_or_none(row.min_salary),
                max_salary=_value_or_none(row.max_salary),
                med_salary=_value_or_none(row.med_salary),
                pay_period=_value_or_none(row.pay_period),
                experience_level=_value_or_none(row.formatted_experience_level),
                remote=row.remote_allowed == 1,
            )
            self.postings.append(posting)

    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the raw LinkedIn job posting data.
        Removes duplicates, missing information, and invalid salary values.
        """

        original_count = len(df)

        # Remove duplicate job postings
        df = df.drop_duplicates(subset="job_id")
        duplicates_removed = original_count - len(df)

        # Remove jobs without a description or title
        before_missing = len(df)
        df = df.dropna(subset=["description", "title"])
        missing_removed = before_missing - len(df)

        # Remove extra spaces from job titles
        df["title"] = df["title"].str.strip()

        # Remove rows with empty titles or descriptions
        before_empty = len(df)
        df = df[
            (df["title"] != "") &
            (df["description"].str.strip() != "")
        ]
        empty_removed = before_empty - len(df)

        # Remove invalid salary values
        salary_columns = ["min_salary", "max_salary", "med_salary"]

        for column in salary_columns:
            if column in df.columns:
                df.loc[df[column] <= 0, column] = None

        # Print cleaning results
        print("Data Cleaning Results")
        print("---------------------")
        print(f"Duplicate jobs removed: {duplicates_removed}")
        print(f"Missing information removed: {missing_removed}")
        print(f"Empty titles/descriptions removed: {empty_removed}")
        print(f"Original rows: {original_count}")
        print(f"Remaining rows: {len(df)}")

        return df

    def extract_all_skills(self, skill_list: list[str]) -> None:
        """Run the skill extractor on every posting."""
        for posting in self.postings:
            posting.extract_skills(skill_list)

    # ---------- Analysis ----------

    def top_skills(self, n: int = 10) -> list[tuple[str, int]]:
        """
        Return the n most-requested skills and how many postings mention each,
        e.g. [("communication", 812), ("sales", 540), ...]
        """
        # Step 1: count how many postings mention each skill.
        # counts looks like {"excel": 412, "communication": 812, ...}
        counts: dict[str, int] = {}
        for posting in self.postings:
            for skill in posting.skills:
                # .get(skill, 0) gives 0 the first time we see a skill, so we can always add 1
                counts[skill] = counts.get(skill, 0) + 1

        # Step 2: sort the (skill, count) pairs by count, biggest first.
        # pair[1] is the count; reverse=True means highest to lowest.
        ranked = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)

        # Step 3: keep only the top n
        return ranked[:n]

    def salary_by_skill(self, min_postings: int = 10) -> dict[str, float]:
        """
        Return the average YEARLY salary for postings that mention each skill,
        e.g. {"python": 118000.0, "sales": 71000.0, ...}
        Only skills with at least min_postings salaries are included, so one or two
        unusual jobs can't make a skill look much better or worse than it really is.
        """
        # Step 1: add up the salaries for each skill, and count how many we added.
        # totals = {"excel": 4_250_000, ...}   counts = {"excel": 61, ...}
        totals: dict[str, float] = {}
        counts: dict[str, int] = {}
        for posting in self.postings:
            salary = posting.yearly_salary()   # Madi's method: yearly amount or None
            if salary is None:
                continue                       # no salary listed, so skip this posting
            for skill in posting.skills:
                totals[skill] = totals.get(skill, 0) + salary
                counts[skill] = counts.get(skill, 0) + 1

        # Step 2: average = total / count, but only for skills with enough salaries
        averages: dict[str, float] = {}
        for skill in totals:
            if counts[skill] >= min_postings:
                averages[skill] = totals[skill] / counts[skill]

        return averages

    def jobs_by_location(self, n: int = 10) -> list[tuple[str, int]]:
        """
        Return the n locations with the most postings, e.g. [("New York, NY", 210), ...]
        Same counting pattern as top_skills(), but each posting has one location.
        """
        # Step 1: count postings per location, e.g. {"New York, NY": 210, ...}
        counts: dict[str, int] = {}
        for posting in self.postings:
            counts[posting.location] = counts.get(posting.location, 0) + 1

        # Step 2: sort by count, biggest first, and keep the top n
        ranked = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)
        return ranked[:n]

    # ---------- Charts ----------

    def plot_top_skills(self, n: int = 10, folder: str = "output") -> str:
        """
        Draw a horizontal bar chart of top_skills(n) with matplotlib,
        save it as a PNG in the output folder, and return the file path.
        """
        os.makedirs(folder, exist_ok=True)   # make the folder if it doesn't exist yet

        # Step 1: get the data and split the pairs into two lists
        ranked = self.top_skills(n)
        names = [skill for skill, count in ranked]
        counts = [count for skill, count in ranked]

        # barh draws the first item at the bottom, so reverse the lists to put #1 on top
        names.reverse()
        counts.reverse()

        # Step 2: draw the bars
        fig, ax = plt.subplots(figsize=(8, 0.45 * len(names) + 1.5))
        ax.set_facecolor("#fcfcfb")   # same off-white as the saved background
        bars = ax.barh(names, counts, color="#2a78d6", height=0.7)

        # Write the count at the end of each bar so readers don't have to guess from the axis
        for bar, count in zip(bars, counts):
            ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f" {count:,}",
                    va="center", fontsize=9, color="#52514e")

        # Step 3: titles and a clean, simple look
        ax.set_title(f"Top {len(names)} skills in {len(self.postings):,} job postings",
                     loc="left", fontsize=13, color="#0b0b0b")
        ax.set_xlabel("Number of postings that mention the skill", color="#52514e")
        ax.spines[["top", "right"]].set_visible(False)       # hide the box around the chart
        ax.grid(axis="x", color="#e5e4e0", linewidth=0.8)    # light guide lines
        ax.set_axisbelow(True)                               # keep guide lines behind the bars
        ax.margins(x=0.1)                                    # leave room for the count labels

        # Step 4: save the chart as a PNG and close it to free memory
        path = os.path.join(folder, "top_skills.png")
        fig.tight_layout()
        fig.savefig(path, dpi=150, facecolor="#fcfcfb")
        plt.close(fig)
        return path
