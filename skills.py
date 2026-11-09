"""
skills.py
The list of skills our program looks for inside job descriptions.
Owner: everyone (add skills as you find them in the data!)

Tips:
- Write every skill in lowercase.
- Multi-word skills are fine ("power bi", "project management").
- Avoid skills that are also common English words (e.g. "go", "r")
  unless you're okay with some false matches.
"""

SKILLS: list[str] = [
    # Data & analytics
    "sql", "python", "excel", "tableau", "power bi", "statistics",
    "data analysis", "data visualization", "machine learning", "looker",
    # Software & IT
    "java", "javascript", "c++", "c#", "html", "css", "aws", "azure",
    "linux", "networking", "cybersecurity", "git", "api",
    # Business tools
    "microsoft office", "word", "powerpoint", "outlook", "salesforce",
    "sap", "quickbooks", "crm", "jira",
    # Business skills
    "project management", "customer service", "sales", "marketing",
    "accounting", "budgeting", "scheduling", "social media", "negotiation",
    # Soft skills
    "communication", "leadership", "teamwork", "problem solving",
    "time management", "attention to detail", "organization",
    # Design
    "photoshop", "adobe", "autocad", "figma",
    # Healthcare
    "patient care", "cpr", "ehr", "bls",
    # Languages
    "spanish", "bilingual",

    # Additional software and IT
"react", "node.js", "typescript", "docker", "kubernetes",
"linux administration", "windows", "powershell", "bash",
"software development", "software engineering",
"database management", "postgresql", "mysql", "mongodb",

# Additional data skills
"pandas", "numpy", "r programming", "data science",
"data engineering", "artificial intelligence",

# Additional cybersecurity skills
"penetration testing", "incident response",
"information security", "risk management",
"vulnerability assessment", "siem"
]
