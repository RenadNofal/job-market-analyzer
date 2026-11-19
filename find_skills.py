"""
find_skills.py
Helper script: finds skills that job ads ask for but that are NOT in SKILLS yet.

Idea: job ads usually name skills right after phrases like
"experience with ...", "proficient in ...", "knowledge of ...".
So we grab the 1-2 words after those phrases and count them.
Read the output and copy any real skills into skills.py.

Run:  python3 find_skills.py
"""

import pandas as pd

from skills import SKILLS

# ---- Settings you can change ----
ROWS_TO_LOAD = 20000       # how many postings to read (more = slower but more results)
TITLE_FILTER = ""          # e.g. "data analyst" to only look at those jobs; "" = all jobs
HOW_MANY_TO_SHOW = 50      # how many top results to print

# Phrases that usually come right before a skill name.
TRIGGERS = [
    "experience with", "experience in", "experience using",
    "proficient in", "proficient with", "proficiency in", "proficiency with",
    "knowledge of", "familiarity with", "familiar with",
    "expertise in", "skilled in", "skills in",
]

# Words that often follow the triggers but are never skills.
STOP_WORDS = {
    "the", "and", "a", "an", "of", "in", "with", "to", "for", "or", "on", "at",
    "all", "any", "other", "various", "basic", "advanced", "strong", "general",
    "working", "relevant", "related", "similar", "common", "standard", "current",
    "using", "use", "managing", "developing", "building", "working", "this",
    "our", "your", "their", "its", "these", "such", "both", "one", "least",
    "experience", "knowledge", "skills", "ability", "industry", "year", "years",
    "minimum", "preferred", "required", "plus", "etc", "including", "e.g", "i.e",
    "how", "what", "best", "modern", "multiple", "large", "complex", "new",
}


def clean_words(text: str) -> list[str]:
    """Lowercase the text and split it into words, keeping letters, digits, + # . only."""
    text = text.lower()
    cleaned = ""
    for ch in text:
        if ch.isalnum() or ch in "+#.":
            cleaned += ch
        else:
            cleaned += " "
    # strip dots at the ends ("sql." -> "sql") but keep "node.js"
    return [w.strip(".") for w in cleaned.split() if w.strip(".")]


def is_useful(word: str) -> bool:
    """Not a stop word, not a number, at least 2 letters."""
    return word not in STOP_WORDS and not word.isdigit() and len(word) >= 2


# 1) Load the data
df = pd.read_csv("data/postings.csv", nrows=ROWS_TO_LOAD)
if TITLE_FILTER:
    df = df[df["title"].str.contains(TITLE_FILTER, case=False, na=False)]
descriptions = df["description"].dropna()
print(f"Looking at {len(descriptions)} job descriptions...\n")

trigger_words = [t.split() for t in TRIGGERS]   # "knowledge of" -> ["knowledge", "of"]
known = set(SKILLS)
counts: dict[str, int] = {}

# 2) For each posting, find every trigger and grab the 1-2 words after it
for text in descriptions:
    words = clean_words(text)
    seen_in_this_posting = set()   # count each term once per posting

    for i in range(len(words)):
        for trig in trigger_words:
            n = len(trig)
            if words[i:i + n] != trig:
                continue
            after = words[i + n:i + n + 2]      # the next 2 words
            if after and is_useful(after[0]):
                seen_in_this_posting.add(after[0])                     # e.g. "snowflake"
                if len(after) == 2 and is_useful(after[1]):
                    seen_in_this_posting.add(after[0] + " " + after[1])  # e.g. "google analytics"

    for term in seen_in_this_posting:
        if term not in known:
            counts[term] = counts.get(term, 0) + 1

# 3) Sort biggest first and print
top = sorted(counts.items(), key=lambda pair: pair[1], reverse=True)[:HOW_MANY_TO_SHOW]

print(f"{'term':<30} postings")
print("-" * 40)
for term, n in top:
    print(f"{term:<30} {n}")
