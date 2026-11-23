"""
main.py
Starts the program and shows the menu.
Owner: everyone
Run with:  python3 main.py
"""
from __future__ import annotations

import os

from candidate import Candidate
from job_market import JobMarket
from skills import SKILLS

DATA_PATH = "data/postings_sample.csv"   # first 5,000 rows of the Kaggle postings.csv
PROFILE_PATH = "output/profile.json"
SAMPLE_SIZE = 5000   # how many postings to load (the full file is very large)

MENU = """
=== Job Market Analyzer ===
1) Show top skills
2) Salary by skill
3) Jobs by location
4) Enter or edit my skills
5) My match report
6) Save and quit
"""


def ask_number(prompt: str, low: int, high: int) -> int:
    """Keep asking until the user types a whole number between low and high."""
    while True:
        answer = input(prompt).strip()
        if answer.isdigit() and low <= int(answer) <= high:
            return int(answer)
        print(f"Please enter a number from {low} to {high}.")


def edit_skills(candidate: Candidate) -> None:
    """Let the user add or remove skills."""
    print(f"Your skills: {', '.join(sorted(candidate.skills)) or '(none yet)'}")
    print("Type a skill to add it, '-skill' to remove it, or press Enter when done.")
    while True:
        entry = input("> ").strip().lower()
        if entry == "":
            break
        if entry.startswith("-"):
            candidate.remove_skill(entry[1:])
            print(f"Removed {entry[1:]}")
        else:
            candidate.add_skill(entry)
            print(f"Added {entry}")


def main() -> None:
    os.makedirs("output", exist_ok=True)

    print("Loading job postings...")
    market = JobMarket()
    market.load_from_csv(DATA_PATH, nrows=SAMPLE_SIZE)
    market.extract_all_skills(SKILLS)
    print(f"Loaded {len(market.postings)} postings.")

    # Load the saved profile if there is one, otherwise start a new one
    try:
        candidate = Candidate.load(PROFILE_PATH)
        print(f"Welcome back, {candidate.name}!")
    except (FileNotFoundError, NotImplementedError):
        candidate = Candidate(input("What's your name? ").strip() or "Student")

    while True:
        print(MENU)
        choice = ask_number("Choose an option (1-6): ", 1, 6)
        try:
            if choice == 1:
                for skill, count in market.top_skills(10):
                    print(f"{skill:<25} {count}")
                print(f"Chart saved to {market.plot_top_skills(10)}")
            elif choice == 2:
                ranked = sorted(market.salary_by_skill().items(), key=lambda item: item[1], reverse=True)
                for skill, salary in ranked:
                    print(f"{skill:<25} ${salary:,.0f}")
            elif choice == 3:
                for location, count in market.jobs_by_location(10):
                    print(f"{location:<30} {count}")
            elif choice == 4:
                edit_skills(candidate)
            elif choice == 5:
                print("\nYour best matches:")
                for posting, score in candidate.best_matches(market, 5):
                    print(f"{score:5.1f}%  {posting}")
                print("\nTop skills you're missing:")
                for skill, count in candidate.missing_skills(market, 10):
                    print(f"{skill:<25} asked for in {count} postings")
            elif choice == 6:
                candidate.save(PROFILE_PATH)
                print("Profile saved. Goodbye!")
                break
        except NotImplementedError as error:
            print(f"(Not built yet: {error})")
            if choice == 6:
                break


if __name__ == "__main__":
    main()
