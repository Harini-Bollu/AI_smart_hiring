"""
matching_engine.py

Milestone 2:
Candidate-Job Matching Engine

Scoring:
    Skills      = 60%
    Experience  = 25%
    Education   = 15%

Final Hiring Score = 0 to 100
"""

import re


# =========================
# SCORING WEIGHTS
# =========================

SKILL_WEIGHT = 0.60
EXPERIENCE_WEIGHT = 0.25
EDUCATION_WEIGHT = 0.15


# =========================
# EDUCATION LEVELS
# =========================

DEGREE_LEVELS = [
    (
        3,
        [
            r"\bph\.?d\b",
            r"\bdoctorate\b",
            r"\bdoctoral\b"
        ]
    ),
    (
        2,
        [
            r"\bm\.?tech\b",
            r"\bm\.?e\b",
            r"\bm\.?sc\b",
            r"\bmsc\b",
            r"\bmaster'?s?\b",
            r"\bmba\b"
        ]
    ),
    (
        1,
        [
            r"\bb\.?tech\b",
            r"\bb\.?e\b",
            r"\bb\.?sc\b",
            r"\bbsc\b",
            r"\bbca\b",
            r"\bbachelor'?s?\b",
            r"\bundergraduate\b"
        ]
    )
]


# =========================
# EDUCATION LEVEL
# =========================

def _degree_level(text):
    """
    Returns:
        3 = PhD
        2 = Master's
        1 = Bachelor's
        0 = Unknown
    """

    if not text:
        return 0

    text = str(text).lower()

    for level, patterns in DEGREE_LEVELS:
        for pattern in patterns:
            if re.search(pattern, text):
                return level

    return 0


# =========================
# EDUCATION SCORE
# =========================

def _education_score(
    candidate_education,
    required_education
):
    """
    Calculates education compatibility.

    Returns value between 0 and 1.
    """

    if not required_education:
        return 1.0

    candidate_text = " ".join(
        map(str, candidate_education)
    )

    required_text = str(
        required_education
    )

    candidate_level = _degree_level(
        candidate_text
    )

    required_level = _degree_level(
        required_text
    )

    if required_level == 0:
        return 1.0

    if candidate_level >= required_level:
        return 1.0

    if candidate_level == required_level - 1:
        return 0.5

    return 0.0


# =========================
# EXPERIENCE SCORE
# =========================

def _experience_score(
    candidate_experience,
    required_experience
):
    """
    Calculates experience compatibility.

    Example:
        Candidate = 3 years
        Required  = 2 years

        Score = 1.0
    """

    try:
        candidate_experience = float(
            candidate_experience or 0
        )
    except:
        candidate_experience = 0.0

    try:
        required_experience = float(
            required_experience or 0
        )
    except:
        required_experience = 0.0

    if required_experience <= 0:
        return 1.0

    score = (
        candidate_experience /
        required_experience
    )

    return min(score, 1.0)


# =========================
# NORMALIZE SKILLS
# =========================

def _normalize_skill_set(skills):
    """
    Converts skills into a clean lowercase set.
    """

    if not skills:
        return set()

    if isinstance(skills, str):
        skills = re.split(
            r"[,;\n|]+",
            skills
        )

    normalized = set()

    for skill in skills:
        skill = str(skill).strip().lower()

        if skill:
            normalized.add(skill)

    return normalized


# =========================
# CALCULATE MATCH
# =========================

def calculate_match(
    candidate,
    job
):
    """
    Calculate compatibility between
    one candidate and one job.

    Returns:
        hiring_score
        skill_score
        experience_score
        education_score
        matched_skills
        missing_skills
        recommendations
    """

    candidate_skills = _normalize_skill_set(
        candidate.get("skills", [])
    )

    required_skills = _normalize_skill_set(
        job.get("required_skills", [])
    )

    # -------------------------
    # SKILL SCORE
    # -------------------------

    if not required_skills:
        skill_score = 1.0
        matched_skills = []
        missing_skills = []

    else:
        matched = (
            candidate_skills &
            required_skills
        )

        missing = (
            required_skills -
            candidate_skills
        )

        matched_skills = sorted(
            matched
        )

        missing_skills = sorted(
            missing
        )

        skill_score = (
            len(matched) /
            len(required_skills)
        )

    # -------------------------
    # EXPERIENCE SCORE
    # -------------------------

    experience_score = _experience_score(
        candidate.get(
            "experience_years",
            0
        ),
        job.get(
            "experience_required",
            0
        )
    )

    # -------------------------
    # EDUCATION SCORE
    # -------------------------

    education_score = _education_score(
        candidate.get(
            "education",
            []
        ),
        job.get(
            "education_required",
            ""
        )
    )

    # -------------------------
    # FINAL SCORE
    # -------------------------

    hiring_score = (
        skill_score * SKILL_WEIGHT
        +
        experience_score * EXPERIENCE_WEIGHT
        +
        education_score * EDUCATION_WEIGHT
    ) * 100

    hiring_score = round(
        hiring_score,
        2
    )

    # -------------------------
    # RECOMMENDATIONS
    # -------------------------

    recommendations = []

    if missing_skills:
        recommendations.append(
            "Develop missing skills: "
            + ", ".join(missing_skills)
        )

    required_experience = job.get(
        "experience_required",
        0
    )

    candidate_experience = candidate.get(
        "experience_years",
        0
    )

    try:
        experience_gap = (
            float(required_experience or 0)
            -
            float(candidate_experience or 0)
        )
    except:
        experience_gap = 0

    if experience_gap > 0:
        recommendations.append(
            f"Gain approximately "
            f"{experience_gap:.1f} more years "
            f"of relevant experience."
        )

    if education_score < 1.0:
        recommendations.append(
            "Consider obtaining the "
            "required educational qualification."
        )

    if not recommendations:
        recommendations.append(
            "Candidate meets the major "
            "job requirements."
        )

    return {
        "hiring_score": hiring_score,
        "skill_score": round(
            skill_score * 100,
            2
        ),
        "experience_score": round(
            experience_score * 100,
            2
        ),
        "education_score": round(
            education_score * 100,
            2
        ),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "recommendations": recommendations
    }


# =========================
# SKILL GAP ANALYSIS
# =========================

def skill_gap_analysis(
    candidate,
    job
):
    """
    Returns detailed skill-gap information.
    """

    candidate_skills = _normalize_skill_set(
        candidate.get("skills", [])
    )

    required_skills = _normalize_skill_set(
        job.get("required_skills", [])
    )

    matched_skills = sorted(
        candidate_skills &
        required_skills
    )

    missing_skills = sorted(
        required_skills -
        candidate_skills
    )

    extra_skills = sorted(
        candidate_skills -
        required_skills
    )

    if required_skills:
        coverage = (
            len(matched_skills) /
            len(required_skills)
        ) * 100
    else:
        coverage = 100.0

    recommendations = []

    if missing_skills:
        recommendations.append(
            "Learn or improve: "
            + ", ".join(missing_skills)
        )

    if extra_skills:
        recommendations.append(
            "Additional candidate skills: "
            + ", ".join(extra_skills)
        )

    if not recommendations:
        recommendations.append(
            "No major skill gaps identified."
        )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "extra_skills": extra_skills,
        "skill_coverage": round(
            coverage,
            2
        ),
        "recommendations": recommendations
    }


# =========================
# MATCH ALL CANDIDATES
# =========================

def match_candidates_to_job(
    candidates,
    job
):
    """
    Match every candidate against a job
    and return candidates ranked by
    hiring score.
    """

    results = []

    for candidate in candidates:

        match = calculate_match(
            candidate,
            job
        )

        skill_gap = skill_gap_analysis(
            candidate,
            job
        )

        result = {
            "candidate_id": candidate.get(
                "id"
            ),
            "candidate_name": candidate.get(
                "name",
                "Unknown"
            ),
            "job_id": job.get(
                "id"
            ),
            "job_title": job.get(
                "title",
                ""
            ),

            "hiring_score": match[
                "hiring_score"
            ],

            "skill_score": match[
                "skill_score"
            ],

            "experience_score": match[
                "experience_score"
            ],

            "education_score": match[
                "education_score"
            ],

            "matched_skills": skill_gap[
                "matched_skills"
            ],

            "missing_skills": skill_gap[
                "missing_skills"
            ],

            "recommendations": match[
                "recommendations"
            ],

            "skill_coverage": skill_gap[
                "skill_coverage"
            ]
        }

        results.append(result)

    # Highest score first
    results.sort(
        key=lambda x: x["hiring_score"],
        reverse=True
    )

    return results