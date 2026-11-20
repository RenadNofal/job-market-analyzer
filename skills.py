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
    "linux", "networking", "cybersecurity", "git", "api", "cloud computing",
    "cloud platforms", "autocad", "revit", "computer-aided design", "sketchup",
    "rhino","3ds max",
    # Business tools
    "microsoft office", "word", "powerpoint", "outlook", "salesforce",
    "sap", "quickbooks", "crm", "jira", "microsoft excel"
    # Business skills
    "project management", "customer service", "sales", "marketing",
    "accounting", "budgeting", "scheduling", "social media", "negotiation", "product management", "financial management",
    "financial planning"
    # Soft skills
    "communication", "leadership", "teamwork", "problem solving",
    "time management", "attention to detail", "organization", "project coordination"
    # Design
    "photoshop", "adobe", "autocad", "figma", "product design", "cad"
    # Healthcare
    "patient care", "cpr", "ehr", "bls", "medical terminology"
    # Languages
    "spanish", "bilingual",

    # Additional software and IT
"react", "node.js", "typescript", "docker", "kubernetes",
"linux administration", "windows", "powershell", "bash",
"software development", "software engineering",
"database management", "postgresql", "mysql", "mongodb",

# Additional data skills
"pandas", "numpy", "r programming", "data science",
"data engineering", "artificial intelligence", "data management"

# Additional cybersecurity skills
"penetration testing", "incident response",
"information security", "risk management",
"vulnerability assessment", "siem"
]
