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


def _value_or_none(value):
    """pandas uses NaN for missing values; turn those into None so they're easier to check."""
    return None if pd.isna(value) else value


class JobMarket:
    """Holds a list of JobPosting objects and answers questions about them."""

    def __init__(self) -> None:
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
        Owner: Madi. Clean the raw data before we turn it into objects.
        Already done: drop duplicate jobs and rows with no description.
        TODO (Madi) ideas: strip extra spaces in titles, check for weird salary values
        (like 0 or huge numbers), and print how many rows were removed at each step.
        """
        df = df.drop_duplicates(subset="job_id")
        df = df.dropna(subset=["description", "title"])
        return df

    def extract_all_skills(self, skill_list: list[str]) -> None:
        """Run the skill extractor on every posting."""
        for posting in self.postings:
            posting.extract_skills(skill_list)

    # ---------- Analysis ----------

    def top_skills(self, n: int = 10) -> list[tuple[str, int]]:
        """
        TODO (Renad): return the n most-requested skills and how many postings mention each,
        e.g. [("communication", 812), ("sales", 540), ...]
        Hint: loop over self.postings and count with a dictionary, then sort by the count.
        """
        raise NotImplementedError("top_skills() isn't built yet")

    def salary_by_skill(self, min_postings: int = 10) -> dict[str, float]:
        """
        TODO (Renad): return the average YEARLY salary for postings that mention each skill.
        Use posting.yearly_salary() (Madi's method) and skip postings where it returns None.
        Only include skills that have at least min_postings salaries, so averages are fair.
        """
        raise NotImplementedError("salary_by_skill() isn't built yet")

    def jobs_by_location(self, n: int = 10) -> list[tuple[str, int]]:
        """
        TODO (Renad): return the n locations with the most postings, e.g. [("New York, NY", 210), ...]
        """
        raise NotImplementedError("jobs_by_location() isn't built yet")

    # ---------- Charts ----------

    def plot_top_skills(self, n: int = 10, folder: str = "output") -> str:
        """
        TODO (Renad): draw a bar chart of top_skills(n) with matplotlib,
        save it as a PNG in the output folder, and return the file path.
        Hint: plt.barh(names, counts), plt.tight_layout(), plt.savefig(path), plt.close()
        """
        os.makedirs(folder, exist_ok=True)
        raise NotImplementedError("plot_top_skills() isn't built yet")
