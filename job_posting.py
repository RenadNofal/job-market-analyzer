"""
job_posting.py
The JobPosting class: stores ONE job posting from the dataset.
Owner: Madi
"""
from __future__ import annotations

# Yearly salaries outside this range are treated as data errors and ignored
MIN_YEARLY_SALARY = 15_000
MAX_YEARLY_SALARY = 500_000

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
        """Store one posting's details. Skills start empty until extract_skills() runs."""
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
        word_set = set(words)                         # every word in the description, for a quick lookup

        # 2) Look for each skill as a sequence of whole words
        found: list[str] = []
        for skill in skill_list:
            skill_words = skill.lower().split()      # "power bi" -> ["power", "bi"]
            if skill_words[0] not in word_set:       # the skill's first word isn't in the text at all,
                continue                              # so it can't match: skip it (this makes it ~7x faster)
            n = len(skill_words)
            for i in range(len(words) - n + 1):
                if words[i:i + n] == skill_words:
                    found.append(skill)
                    break                             # count each skill once per posting

        self.skills = found
        return found
    
    def yearly_salary(self) -> float | None:
        """Return this job's salary converted to a yearly amount."""

        # Step 1: Determine which salary to use
        if self.min_salary is not None and self.max_salary is not None:
            salary = (self.min_salary + self.max_salary) / 2
        else:
            salary = self.med_salary

        # Step 2: If no salary information exists, return None
        if salary is None:
            return None

        # Step 3: Conversion factors for each pay period
        conversion = {
            "HOURLY": 2080,
            "WEEKLY": 52,
            "BIWEEKLY": 26,
            "MONTHLY": 12,
            "YEARLY": 1
        }

        # Step 4: Convert the salary to yearly
        factor = conversion.get(self.pay_period)

        if factor is None:
            return None

        yearly = salary * factor

        # Step 5: Skip unrealistic salaries. Some postings say YEARLY but list an hourly
        # wage (e.g. "$16-20 per year"), and a few list huge partner payouts.
        if yearly < MIN_YEARLY_SALARY or yearly > MAX_YEARLY_SALARY:
            return None

        return yearly

    def __str__(self) -> str:
        """Return a readable one-line summary, e.g. 'Data Analyst at Acme (Cleveland, OH)'."""
        company = self.company if self.company else "Unknown company"
        return f"{self.title} at {company} ({self.location})"
