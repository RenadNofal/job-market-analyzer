"""
job_posting.py
The JobPosting class: stores ONE job posting from the dataset.
Owner: Madi
"""
from __future__ import annotations


class JobPosting:
    """One job posting: its basic info, salary, and the skills found in it."""

    def __init__(
        self,
        job_id: int,
        title: str,
        company: str | None,
        location: str,
        description: str,
        min_salary: float | None,
        max_salary: float | None,
        med_salary: float | None,
        pay_period: str | None,
        experience_level: str | None,
        remote: bool,
    ) -> None:
        self.job_id = job_id
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.med_salary = med_salary
        self.pay_period = pay_period          # "HOURLY", "WEEKLY", "BIWEEKLY", "MONTHLY", "YEARLY" or None
        self.experience_level = experience_level  # e.g. "Entry level", "Mid-Senior level"
        self.remote = remote
        self.skills: list[str] = []           # filled in by extract_skills()

    def extract_skills(self, skill_list: list[str]) -> list[str]:
        """
        FROM-SCRATCH ALGORITHM: find which skills appear in the description.
        Matches whole words only, so "excel" does not match "excellent".
        Saves the result in self.skills and also returns it.
        """
        # 1) Clean the text: keep letters, numbers, + and # (for c++ / c#), turn everything else into spaces
        cleaned = ""
        for char in self.description.lower():
            if char.isalnum() or char in "+#":
                cleaned += char
            else:
                cleaned += " "
        words = cleaned.split()

        # 2) Look for each skill as a sequence of whole words
        found: list[str] = []
        for skill in skill_list:
            skill_words = skill.lower().split()      # "power bi" -> ["power", "bi"]
            n = len(skill_words)
            for i in range(len(words) - n + 1):
                if words[i:i + n] == skill_words:
                    found.append(skill)
                    break                             # count each skill once per posting

        self.skills = found
        return found

    def yearly_salary(self) -> float | None:
        """
        TODO (Madi): return this job's salary converted to a YEARLY amount, or None if there's no salary.

        Steps:
        1. Pick one number: the midpoint of min_salary and max_salary if both exist,
           otherwise med_salary. If none exist, return None.
        2. Convert it to yearly using pay_period, e.g.:
           HOURLY -> x 2080 (40 hrs x 52 weeks), WEEKLY -> x 52, BIWEEKLY -> x 26,
           MONTHLY -> x 12, YEARLY -> x 1
        Tip: a dictionary like {"HOURLY": 2080, ...} makes this easy.
        """
        raise NotImplementedError("yearly_salary() isn't built yet")

    def __str__(self) -> str:
        company = self.company if self.company else "Unknown company"
        return f"{self.title} at {company} ({self.location})"
