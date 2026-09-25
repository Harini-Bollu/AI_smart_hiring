# ============================================================
# AI SMART HIRING
# ROBUST CANDIDATE INFORMATION EXTRACTOR
# ============================================================

import re


# ============================================================
# SKILLS
# ============================================================

SKILLS_LIST = [
    # Programming
    "Python", "Java", "C", "C++", "C#", "R",
    "JavaScript", "TypeScript", "Go", "PHP", "Ruby",
    "Kotlin", "Swift",

    # Web
    "HTML", "CSS", "React", "React.js", "Angular",
    "Vue", "Node.js", "Express.js", "Django", "Flask",
    "FastAPI", "Bootstrap", "Tailwind",

    # Database
    "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "SQLite", "Oracle", "Redis", "Firebase",

    # Data Science / AI
    "Machine Learning", "Deep Learning",
    "Artificial Intelligence", "Data Science",
    "Natural Language Processing", "NLP",
    "Computer Vision", "Generative AI",
    "TensorFlow", "PyTorch", "Scikit-learn",
    "Keras", "Pandas", "NumPy",
    "Matplotlib", "Seaborn",
    "OpenCV", "Hugging Face",
    "Transformers",

    # Cloud / DevOps
    "AWS", "Azure", "Google Cloud", "GCP",
    "Docker", "Kubernetes", "Jenkins",
    "Git", "GitHub", "GitLab",
    "CI/CD",

    # Tools
    "Jupyter", "Jupyter Notebook",
    "VS Code", "Postman",
    "Linux", "Power BI", "Tableau",
    "Excel",

    # Concepts
    "OOP", "Object Oriented Programming",
    "Data Structures", "Algorithms",
    "REST API", "API",
    "Agile", "Scrum",
    "Cybersecurity",
    "Computer Networks",
    "Operating Systems"
]


# ============================================================
# SECTION HEADINGS
# ============================================================

SECTION_ALIASES = {

    "summary": [
        "summary",
        "professional summary",
        "profile",
        "professional profile",
        "career objective",
        "objective",
        "about me",
        "about"
    ],

    "education": [
        "education",
        "academic background",
        "educational background",
        "academic qualifications",
        "qualifications"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills",
        "key skills",
        "skills & technologies",
        "technical competencies",
        "technologies",
        "technology stack",
        "tools & technologies"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "internship",
        "internships",
        "industrial experience",
        "professional experience"
    ],

    "projects": [
        "projects",
        "project",
        "academic projects",
        "academic project",
        "personal projects",
        "personal project",
        "key projects",
        "major projects",
        "project experience"
    ],

    "certifications": [
        "certifications",
        "certification",
        "certificates",
        "certificate",
        "professional certifications",
        "courses",
        "courses & certifications"
    ],

    "achievements": [
        "achievements",
        "awards",
        "honors",
        "accomplishments",
        "extra curricular",
        "extracurricular",
        "activities"
    ]
}


# ============================================================
# BLOCKED NAME WORDS
# ============================================================

NAME_BLOCKED_WORDS = {
    "resume",
    "curriculum",
    "vitae",
    "curriculum vitae",
    "cv",
    "career",
    "objective",
    "career objective",
    "summary",
    "professional summary",
    "profile",
    "about",
    "education",
    "skills",
    "technical skills",
    "experience",
    "work experience",
    "professional experience",
    "internship",
    "internships",
    "projects",
    "project",
    "certifications",
    "certification",
    "certificates",
    "achievements",
    "contact",
    "contact information",
    "phone",
    "email",
    "address",
    "references",
    "declaration"
}


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):

    if not text:
        return ""

    text = text.replace(
        "\x00",
        " "
    )

    text = text.replace(
        "\r",
        "\n"
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def clean_line(line):

    line = re.sub(
        r"\s+",
        " ",
        line
    )

    return line.strip()


def get_lines(text):

    return [
        clean_line(line)
        for line in text.splitlines()
        if clean_line(line)
    ]


# ============================================================
# NAME EXTRACTION
# ============================================================

def extract_name(text):

    lines = get_lines(text)

    # --------------------------------------------------------
    # First: look at the first 20 lines
    # --------------------------------------------------------

    for line in lines[:20]:

        candidate = line.strip()

        if not candidate:
            continue

        if "@" in candidate:
            continue

        if re.search(
            r"\d{3,}",
            candidate
        ):
            continue

        lower = candidate.lower()

        if lower in NAME_BLOCKED_WORDS:
            continue

        # Remove labels such as Name:
        candidate = re.sub(
            r"^(name|full name)\s*:\s*",
            "",
            candidate,
            flags=re.I
        ).strip()

        words = candidate.split()

        if not (
            2 <= len(words) <= 5
        ):
            continue

        valid = True

        for word in words:

            word = word.strip(
                ".,:-"
            )

            if not word:
                valid = False
                break

            if not re.match(
                r"^[A-Za-z][A-Za-z.'-]*$",
                word
            ):
                valid = False
                break

            if word.lower() in NAME_BLOCKED_WORDS:
                valid = False
                break

        if not valid:
            continue

        # Don't accept long sentence-like lines
        if len(candidate) > 45:
            continue

        # Good candidate
        return candidate.title()

    # --------------------------------------------------------
    # Look for explicit "Name:"
    # --------------------------------------------------------

    for line in lines[:40]:

        match = re.search(
            r"^(?:name|full name)\s*:\s*(.+)$",
            line,
            flags=re.I
        )

        if match:

            name = match.group(1).strip()

            if name:
                return name.title()

    return "Not detected"


# ============================================================
# EMAIL
# ============================================================

def extract_email(text):

    match = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text
    )

    if match:
        return match.group(0)

    return ""


# ============================================================
# PHONE
# ============================================================

def extract_phone(text):

    patterns = [
        r"\+91[\s-]?\d{5}[\s-]?\d{5}",
        r"\+91[\s-]?\d{10}",
        r"\b\d{10}\b",
        r"\b\d{5}[\s-]\d{5}\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            phone = match.group(0)

            digits = re.sub(
                r"\D",
                "",
                phone
            )

            if len(digits) == 10:

                return phone

            if len(digits) == 12 and digits.startswith("91"):

                return "+" + digits

    return ""


# ============================================================
# SECTION DETECTION
# ============================================================

def normalize_heading(line):

    value = line.lower().strip()

    value = re.sub(
        r"^[•●▪■*#\-\d.)]+\s*",
        "",
        value
    )

    value = re.sub(
        r"[:\-|]+$",
        "",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def detect_section(line):

    normalized = normalize_heading(
        line
    )

    if len(normalized) > 60:
        return None

    for section, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            if normalized == alias:

                return section

    return None


def extract_sections(text):

    lines = get_lines(text)

    sections = {
        key: []
        for key in SECTION_ALIASES
    }

    current_section = None

    for line in lines:

        detected = detect_section(
            line
        )

        if detected:

            current_section = detected

            continue

        if current_section:

            sections[
                current_section
            ].append(line)

    return sections


# ============================================================
# SKILLS EXTRACTION
# ============================================================

def extract_skills(text):

    found = []

    text_lower = text.lower()

    # Sort longer skills first so that
    # "Machine Learning" is checked before "Learning"
    skills_sorted = sorted(
        SKILLS_LIST,
        key=len,
        reverse=True
    )

    for skill in skills_sorted:

        pattern = re.escape(
            skill.lower()
        )

        if re.search(
            r"(?<![a-z0-9])"
            + pattern +
            r"(?![a-z0-9])",
            text_lower
        ):

            if skill not in found:

                found.append(skill)

    return found


# ============================================================
# EXPERIENCE EXTRACTION
# ============================================================

def extract_experience(text, sections):

    experience = []

    # --------------------------------------------------------
    # First use EXPERIENCE section
    # --------------------------------------------------------

    section_lines = sections.get(
        "experience",
        []
    )

    if section_lines:

        current_entry = []

        for line in section_lines:

            if not line:
                continue

            # New entry indicators:
            # company names, job titles, dates etc.
            date_match = re.search(
                r"\b(?:19|20)\d{2}\b.*\b(?:19|20)\d{2}\b",
                line
            )

            title_match = re.search(
                r"\b("
                r"intern|internship|developer|engineer|"
                r"analyst|developer|designer|manager|"
                r"trainee|associate|consultant"
                r")\b",
                line,
                re.I
            )

            if (
                current_entry
                and (
                    date_match
                    or title_match
                )
            ):

                experience.append(
                    " ".join(
                        current_entry
                    )
                )

                current_entry = []

            current_entry.append(
                line
            )

        if current_entry:

            experience.append(
                " ".join(
                    current_entry
                )
            )

    # --------------------------------------------------------
    # Fallback keyword scanning
    # --------------------------------------------------------

    if not experience:

        lines = get_lines(text)

        keywords = [
            "intern",
            "internship",
            "worked as",
            "working as",
            "developer",
            "software engineer",
            "data scientist",
            "data analyst",
            "machine learning engineer",
            "research intern",
            "web developer",
            "python developer",
            "full stack"
        ]

        for i, line in enumerate(lines):

            lower = line.lower()

            if any(
                keyword in lower
                for keyword in keywords
            ):

                block = []

                for x in range(
                    max(0, i - 1),
                    min(
                        len(lines),
                        i + 4
                    )
                ):

                    block.append(
                        lines[x]
                    )

                value = " ".join(
                    block
                )

                if value not in experience:

                    experience.append(
                        value
                    )

    return experience[:10]


# ============================================================
# EXPERIENCE YEARS
# ============================================================

def extract_experience_years(
    text,
    experience
):

    values = []

    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+(?:of\s+)?experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+in",
        r"(\d+(?:\.\d+)?)\s*\+?\s*yrs?\s+(?:of\s+)?experience"
    ]

    for pattern in patterns:

        for match in re.finditer(
            pattern,
            text.lower()
        ):

            try:

                values.append(
                    float(
                        match.group(1)
                    )
                )

            except Exception:
                pass

    if values:

        return max(values)

    # Internship / experience date ranges
    date_ranges = re.findall(
        r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"[a-z]*\s+)?"
        r"(20\d{2})"
        r"\s*[-–]\s*"
        r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"[a-z]*\s+)?"
        r"(20\d{2}|Present|Current)",
        text,
        flags=re.I
    )

    if date_ranges:

        years = []

        for item in date_ranges:

            try:

                start_year = int(
                    item[1]
                )

                end_value = item[3]

                if end_value.lower() in [
                    "present",
                    "current"
                ]:

                    import datetime

                    end_year = datetime.datetime.now().year

                else:

                    end_year = int(
                        end_value
                    )

                difference = end_year - start_year

                if 0 <= difference <= 50:

                    years.append(
                        float(difference)
                    )

            except Exception:
                pass

        if years:

            return max(
                years
            )

    return 0.0


# ============================================================
# EDUCATION
# ============================================================

def extract_education(
    text,
    sections
):

    education = []

    section_lines = sections.get(
        "education",
        []
    )

    if section_lines:

        for line in section_lines:

            if line not in education:

                education.append(
                    line
                )

    # Fallback
    if not education:

        lines = get_lines(text)

        education_keywords = [
            "b.tech",
            "btech",
            "b.e",
            "b.e.",
            "bachelor",
            "m.tech",
            "mtech",
            "m.e",
            "master",
            "mca",
            "mba",
            "bca",
            "bsc",
            "m.sc",
            "msc",
            "intermediate",
            "higher secondary",
            "junior college",
            "school"
        ]

        for i, line in enumerate(lines):

            lower = line.lower()

            if any(
                keyword in lower
                for keyword in education_keywords
            ):

                block = []

                for x in range(
                    i,
                    min(
                        len(lines),
                        i + 4
                    )
                ):

                    block.append(
                        lines[x]
                    )

                value = " | ".join(
                    block
                )

                if value not in education:

                    education.append(
                        value
                    )

    return education[:20]


# ============================================================
# PROJECTS
# ============================================================

def extract_projects(
    text,
    sections
):

    projects = []

    section_lines = sections.get(
        "projects",
        []
    )

    if section_lines:

        current = []

        for line in section_lines:

            if not line:
                continue

            # New project often begins with a title
            # followed by technologies or description
            if (
                current
                and (
                    line.startswith("•")
                    or line.startswith("-")
                    or re.match(
                        r"^[A-Z][A-Za-z0-9 &:/()_-]{3,60}$",
                        line
                    )
                )
            ):

                projects.append(
                    " ".join(
                        current
                    )
                )

                current = []

            current.append(
                line
            )

        if current:

            projects.append(
                " ".join(
                    current
                )
            )

    # --------------------------------------------------------
    # Fallback project detection
    # --------------------------------------------------------

    if not projects:

        lines = get_lines(text)

        project_keywords = [
            "developed",
            "built",
            "created",
            "implemented",
            "designed",
            "project",
            "application",
            "platform",
            "system"
        ]

        technology_words = [
            "python",
            "java",
            "react",
            "flask",
            "django",
            "machine learning",
            "deep learning",
            "mongodb",
            "mysql",
            "postgresql",
            "tensorflow",
            "pytorch"
        ]

        for i, line in enumerate(lines):

            lower = line.lower()

            has_project_word = any(
                x in lower
                for x in project_keywords
            )

            has_technology = any(
                x in lower
                for x in technology_words
            )

            if (
                has_project_word
                and (
                    has_technology
                    or len(line) > 50
                )
            ):

                block = []

                for x in range(
                    max(0, i - 1),
                    min(
                        len(lines),
                        i + 5
                    )
                ):

                    block.append(
                        lines[x]
                    )

                value = " ".join(
                    block
                )

                if value not in projects:

                    projects.append(
                        value
                    )

    return projects[:15]


# ============================================================
# CERTIFICATIONS
# ============================================================

def extract_certifications(
    text,
    sections
):

    certifications = []

    section_lines = sections.get(
        "certifications",
        []
    )

    if section_lines:

        for line in section_lines:

            if line not in certifications:

                certifications.append(
                    line
                )

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    if not certifications:

        lines = get_lines(text)

        certificate_keywords = [
            "certified",
            "certification",
            "certificate",
            "coursera",
            "udemy",
            "nptel",
            "aws certified",
            "microsoft certified",
            "google certified",
            "oracle certified",
            "hackerrank",
            "skillrack"
        ]

        for i, line in enumerate(lines):

            lower = line.lower()

            if any(
                keyword in lower
                for keyword in certificate_keywords
            ):

                value = line

                if value not in certifications:

                    certifications.append(
                        value
                    )

    return certifications[:15]


# ============================================================
# SUMMARY
# ============================================================

def extract_summary(
    sections
):

    summary = sections.get(
        "summary",
        []
    )

    if summary:

        return " ".join(
            summary[:8]
        )

    return ""


# ============================================================
# MAIN EXTRACTION FUNCTION
# ============================================================

def extract_candidate_info(
    text
):

    text = clean_text(
        text
    )

    sections = extract_sections(
        text
    )

    experience = extract_experience(
        text,
        sections
    )

    candidate = {

        "name": extract_name(
            text
        ),

        "email": extract_email(
            text
        ),

        "phone": extract_phone(
            text
        ),

        "education": extract_education(
            text,
            sections
        ),

        "skills": extract_skills(
            text
        ),

        "experience": experience,

        "experience_years": extract_experience_years(
            text,
            experience
        ),

        "certifications": extract_certifications(
            text,
            sections
        ),

        "projects": extract_projects(
            text,
            sections
        ),

        "summary": extract_summary(
            sections
        )
    }

    return candidate


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def extract_candidate(
    text
):

    return extract_candidate_info(
        text
    )


def analyze_resume(
    text
):

    return extract_candidate_info(
        text
    )