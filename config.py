"""
Configuration file for team members and their roles/skills
"""
TEAM_MEMBERS = [
    {
        "name": "Sakshi",
        "role": "Frontend Developer",
        "skills": ["React", "JavaScript", "UI bugs", "frontend", "login", "bug", "bugs"]
    },
    {
        "name": "Mohit",
        "role": "Backend Engineer",
        "skills": ["Database", "APIs", "Performance optimization", "backend", "database", "api", "documentation", "optimization"]
    },
    {
        "name": "Arjun",
        "role": "UI/UX Designer",
        "skills": ["Figma", "User flows", "Mobile design", "UI", "UX", "design", "onboarding", "screens"]
    },
    {
        "name": "Lata",
        "role": "QA Engineer",
        "skills": ["Testing", "QA", "unit tests", "test", "testing", "quality assurance"]
    }
]

PRIORITY_KEYWORDS = {
    "critical": ["critical", "urgent", "blocking", "immediately", "asap"],
    "high": ["high priority", "important", "needs to be done", "should tackle", "before release"],
    "medium": ["medium", "can wait", "plan", "next sprint"],
    "low": ["low", "nice to have", "optional"]
}

DEADLINE_PATTERNS = [
    r"till\s+(?:next\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
    r"until\s+(?:next\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
    r"by\s+(tomorrow|today|friday|monday|wednesday|thursday|tuesday|sunday)",
    r"(tomorrow|today|friday|monday|wednesday|thursday|tuesday|sunday)\s+(evening|morning|afternoon|night)",
    r"end\s+of\s+(this\s+week|next\s+week|the\s+week)",
    r"before\s+(friday|monday|wednesday|thursday|tuesday|sunday|release)",
    r"next\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
    r"by\s+(\d{1,2}[/-]\d{1,2})", 
]

