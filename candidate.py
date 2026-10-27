"""
candidate.py
The Candidate class: the user's own skills, compared against the job market.
Owner: Samantha
"""
from __future__ import annotations

from job_market import JobMarket
from job_posting import JobPosting


class Candidate:
    """The person using the program: their name and skills."""

    def __init__(self, name: str, skills: set[str] | None = None) -> None:
        self.name = name
        self.skills: set[str] = skills if skills else set()

    def add_skill(self, skill: str) -> None:
        self.skills.add(skill.strip().lower())

    def remove_skill(self, skill: str) -> None:
        self.skills.discard(skill.strip().lower())

    def match_score(self, posting: JobPosting) -> float:
        """
        TODO (Samantha): return the % of this posting's skills that the candidate has (0-100).
        Example: posting needs ["sql", "excel", "tableau"], candidate has sql + excel -> 66.7
        Watch out: if the posting has no skills, avoid dividing by zero (return 0.0).
        """
        raise NotImplementedError("match_score() isn't built yet")

    def best_matches(self, market: JobMarket, n: int = 5) -> list[tuple[JobPosting, float]]:
        """
        TODO (Samantha): return the n postings with the highest match_score, highest first.
        """
        raise NotImplementedError("best_matches() isn't built yet")

    def missing_skills(self, market: JobMarket, n: int = 10) -> list[tuple[str, int]]:
        """
        TODO (Samantha): return the in-demand skills the candidate does NOT have,
        ranked by how many postings ask for them.
        Hint: use market.top_skills(...) and skip the ones in self.skills.
        """
        raise NotImplementedError("missing_skills() isn't built yet")

    def save(self, path: str) -> None:
        """
        TODO (Samantha): save name + skills to a JSON file.
        Hint: json can't save sets, so convert with list(self.skills).
        """
        raise NotImplementedError("save() isn't built yet")

    @classmethod
    def load(cls, path: str) -> Candidate:
        """
        TODO (Samantha): read the JSON file and return a new Candidate.
        Hint: with open(path) as f: data = json.load(f)
        """
        raise NotImplementedError("load() isn't built yet")
