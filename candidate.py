"""
candidate.py
The Candidate class: the user's own skills, compared against the job market.
Owner: Samantha
"""
from __future__ import annotations
import json

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
        (Samantha): return the % of this posting's skills that the candidate has (0-100).
        Example: posting needs ["sql", "excel", "tableau"], candidate has sql + excel -> 66.7
        Watch out: if the posting has no skills, avoid dividing by zero (return 0.0).
        """
        matching_skills = len(self.skills & set(posting.skills))
        total_skills = len(posting.skills)
        if total_skills == 0:
            return 0.0
        return(matching_skills / total_skills)*100

    

    def best_matches(self, market: JobMarket, n: int = 5) -> list[tuple[JobPosting, float]]:
        """
        (Samantha): return the n postings with the highest match_score, highest first.
        """
        matches = []

        for posting in market.postings:
            score = self.match_score(posting)
            matches.append((posting, score))

        # Sort by how many skills the posting shares with the candidate first, then by score.
        # Sorting by score alone ranks a job that only mentions "communication" as a 100% match.
        matches.sort(key=lambda match: (len(self.skills & set(match[0].skills)), match[1]),
                     reverse=True)
        return matches[:n]
        

    def missing_skills(self, market: JobMarket, n: int = 10) -> list[tuple[str, int]]:
        """
        (Samantha): return the in-demand skills the candidate does NOT have,
        ranked by how many postings ask for them.
        Hint: use market.top_skills(...) and skip the ones in self.skills.
        """
        top_skills = market.top_skills(n + len(self.skills))
        
        missing = [] 

        for skill, count in top_skills:
            if skill not in self.skills:
                missing.append((skill, count))
        return missing[:n]
        

    def save(self, path: str) -> None:
        """
         (Samantha): save name + skills to a JSON file.
        Hint: json can't save sets, so convert with list(self.skills).
        """
        data = {
            "name": self.name,
            "skills": list(self.skills)
        }
        with open(path, "w") as f:
            json.dump(data,f, indent=5)

    @classmethod
    def load(cls, path: str) -> Candidate:
        """
         (Samantha): read the JSON file and return a new Candidate.
        Hint: with open(path) as f: data = json.load(f)
        """ 
        with open(path, "r") as f:
            data = json.load(f)
        return cls(data["name"], set(data["skills"]))
