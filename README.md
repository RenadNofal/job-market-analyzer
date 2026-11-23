# Job Market Analyzer

DSA/CIS 230/492 Final Project · Group 11 · Renad Nofal, Madi Elliott, Samantha Gogol

Analyzes real LinkedIn job postings to find the most in-demand skills, average salary by skill, and where jobs are located. Users enter their own skills to get a match score and a list of skills to learn next.

## Setup

1. Install the libraries: `python3 -m pip install -r requirements.txt`
2. That's it. The data is included: `data/postings_sample.csv` holds the first 5,000 postings from the Kaggle dataset [LinkedIn Job Postings (2023–2024)](https://www.kaggle.com/datasets/arshkon/linkedin-job-postings). The full `postings.csv` (about 490 MB) is too large for GitHub, so it is not uploaded.

## Run

```
python3 main.py
```

## Files

| File | What it does | Owner |
|---|---|---|
| `main.py` | Menu and user input | Everyone |
| `job_posting.py` | `JobPosting` class: one posting + skill extractor + salary conversion | Madi |
| `job_market.py` | `JobMarket` class: loads, cleans and analyzes all postings, makes charts | Renad |
| `candidate.py` | `Candidate` class: user's skills, match score, missing skills, save/load | Samantha |
| `skills.py` | List of skills to search for | Everyone |
| `explore.py` | One-off data exploration script | |
| `find_skills.py` | Helper that finds skills in job ads that aren't in `skills.py` yet | Renad |
| `data/postings_sample.csv` | First 5,000 postings from the Kaggle dataset | |
| `output/` | Saved charts and the user profile | |

## Notes about the data (first 5,000 rows)

- `description` is never missing, so every posting can be searched for skills.
- About 69% of postings have no salary. Salary analysis only uses postings that have one.
- Salaries come in different pay periods (HOURLY, WEEKLY, MONTHLY, YEARLY), so they are converted to yearly before comparing.
- `skills_desc` is almost always empty, which is why we extract skills from the description ourselves.
- Data is from 2023–2024, so salaries may be lower than today's.
