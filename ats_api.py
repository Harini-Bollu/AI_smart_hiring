# ============================================================
# ats_api.py
# Advanced ATS / Candidate Pipeline Backend
# ============================================================

from datetime import datetime
from copy import deepcopy


# ============================================================
# IN-MEMORY ATS DATABASE
# ============================================================

ats_db = []


# ============================================================
# STATUS OPTIONS
# ============================================================

STATUS_OPTIONS = [
    "New",
    "Screening",
    "Interview",
    "Selected",
    "Rejected"
]


# ============================================================
# ID GENERATOR
# ============================================================

def generate_candidate_id():
    """
    Generate the next candidate ID.
    """

    if not ats_db:
        return 1

    return max(
        candidate.get("id", 0)
        for candidate in ats_db
    ) + 1


# ============================================================
# DATE/TIME
# ============================================================

def current_timestamp():
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ============================================================
# SAFE INTEGER
# ============================================================

def safe_score(value):
    """
    Convert score to integer between 0 and 100.
    """

    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0

    return max(
        0,
        min(
            100,
            round(value)
        )
    )


# ============================================================
# ADD CANDIDATE
# ============================================================

def add_candidate(
    name,
    email,
    job_applied,
    status="New",
    phone="",
    match_score=0,
    ats_score=0,
    skills=None,
    matched_skills=None,
    missing_skills=None,
    notes="",
    source="Resume Upload"
):
    """
    Add a complete candidate profile to the ATS.
    """

    if skills is None:
        skills = []

    if matched_skills is None:
        matched_skills = []

    if missing_skills is None:
        missing_skills = []

    candidate = {
        "id": generate_candidate_id(),

        "name": str(name or "Unknown Candidate").strip(),

        "email": str(email or "Not available").strip(),

        "phone": str(phone or "").strip(),

        "job_applied": str(
            job_applied or "Not specified"
        ).strip(),

        "status": (
            status
            if status in STATUS_OPTIONS
            else "New"
        ),

        "match_score": safe_score(match_score),

        "ats_score": safe_score(ats_score),

        "skills": list(skills),

        "matched_skills": list(
            matched_skills
        ),

        "missing_skills": list(
            missing_skills
        ),

        "notes": str(notes or "").strip(),

        "source": str(
            source or "Resume Upload"
        ).strip(),

        "created_at": current_timestamp(),

        "updated_at": current_timestamp()
    }

    ats_db.append(candidate)

    return deepcopy(candidate)


# ============================================================
# ADD / UPDATE SMART CANDIDATE
# ============================================================

def upsert_candidate(
    name,
    email,
    job_applied,
    status="New",
    phone="",
    match_score=0,
    ats_score=0,
    skills=None,
    matched_skills=None,
    missing_skills=None,
    notes="",
    source="Resume Upload"
):
    """
    If candidate email already exists, update the existing
    candidate. Otherwise create a new candidate.
    """

    existing = find_candidate(email)

    if existing:

        return update_candidate(
            existing["id"],
            name=name,
            email=email,
            job_applied=job_applied,
            status=status,
            phone=phone,
            match_score=match_score,
            ats_score=ats_score,
            skills=skills,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            notes=notes,
            source=source
        )

    return add_candidate(
        name=name,
        email=email,
        job_applied=job_applied,
        status=status,
        phone=phone,
        match_score=match_score,
        ats_score=ats_score,
        skills=skills,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        notes=notes,
        source=source
    )


# ============================================================
# LIST CANDIDATES
# ============================================================

def list_candidates():
    """
    Return all candidates.
    """

    return deepcopy(ats_db)


# ============================================================
# GET CANDIDATE
# ============================================================

def get_candidate(candidate_id):
    """
    Find candidate by numeric ID.
    """

    try:
        candidate_id = int(candidate_id)
    except (TypeError, ValueError):
        return None

    for candidate in ats_db:

        if candidate.get("id") == candidate_id:

            return deepcopy(candidate)

    return None


# ============================================================
# FIND BY EMAIL
# ============================================================

def find_candidate(email):
    """
    Find candidate using email address.
    """

    if not email:
        return None

    target = str(email).strip().lower()

    for candidate in ats_db:

        stored_email = str(
            candidate.get("email", "")
        ).strip().lower()

        if stored_email == target:

            return deepcopy(candidate)

    return None


# ============================================================
# FIND BY NAME
# ============================================================

def find_candidates_by_name(name):
    """
    Search candidates by partial name.
    """

    if not name:
        return []

    target = str(name).strip().lower()

    results = []

    for candidate in ats_db:

        candidate_name = str(
            candidate.get("name", "")
        ).lower()

        if target in candidate_name:

            results.append(
                deepcopy(candidate)
            )

    return results


# ============================================================
# SEARCH CANDIDATES
# ============================================================

def search_candidates(query):
    """
    Search by name, email, job or skills.
    """

    if not query:
        return list_candidates()

    target = str(query).strip().lower()

    results = []

    for candidate in ats_db:

        searchable = " ".join([
            str(candidate.get("name", "")),
            str(candidate.get("email", "")),
            str(candidate.get("job_applied", "")),
            str(candidate.get("status", "")),
            " ".join(
                candidate.get("skills", [])
            )
        ]).lower()

        if target in searchable:

            results.append(
                deepcopy(candidate)
            )

    return results


# ============================================================
# FILTER BY STATUS
# ============================================================

def get_candidates_by_status(status):
    """
    Return candidates with a specific pipeline status.
    """

    if status not in STATUS_OPTIONS:
        return []

    return [
        deepcopy(candidate)
        for candidate in ats_db
        if candidate.get("status") == status
    ]


# ============================================================
# UPDATE STATUS
# ============================================================

def update_status(email, status):
    """
    Update candidate pipeline status using email.
    """

    if status not in STATUS_OPTIONS:
        return None

    if not email:
        return None

    target = str(email).strip().lower()

    for candidate in ats_db:

        if (
            str(
                candidate.get(
                    "email",
                    ""
                )
            ).strip().lower()
            == target
        ):

            candidate["status"] = status
            candidate["updated_at"] = current_timestamp()

            return deepcopy(candidate)

    return None


# ============================================================
# UPDATE STATUS BY ID
# ============================================================

def update_status_by_id(candidate_id, status):
    """
    Update status using candidate ID.
    """

    if status not in STATUS_OPTIONS:
        return None

    try:
        candidate_id = int(candidate_id)
    except (TypeError, ValueError):
        return None

    for candidate in ats_db:

        if candidate.get("id") == candidate_id:

            candidate["status"] = status
            candidate["updated_at"] = current_timestamp()

            return deepcopy(candidate)

    return None


# ============================================================
# UPDATE CANDIDATE
# ============================================================

def update_candidate(
    candidate_id,
    name=None,
    email=None,
    job_applied=None,
    status=None,
    phone=None,
    match_score=None,
    ats_score=None,
    skills=None,
    matched_skills=None,
    missing_skills=None,
    notes=None,
    source=None
):
    """
    Update any available candidate fields.
    """

    try:
        candidate_id = int(candidate_id)
    except (TypeError, ValueError):
        return None

    for candidate in ats_db:

        if candidate.get("id") != candidate_id:
            continue

        if name is not None:
            candidate["name"] = str(
                name
            ).strip()

        if email is not None:
            candidate["email"] = str(
                email
            ).strip()

        if phone is not None:
            candidate["phone"] = str(
                phone
            ).strip()

        if job_applied is not None:
            candidate["job_applied"] = str(
                job_applied
            ).strip()

        if status is not None:

            if status in STATUS_OPTIONS:
                candidate["status"] = status

        if match_score is not None:
            candidate["match_score"] = safe_score(
                match_score
            )

        if ats_score is not None:
            candidate["ats_score"] = safe_score(
                ats_score
            )

        if skills is not None:
            candidate["skills"] = list(
                skills
            )

        if matched_skills is not None:
            candidate["matched_skills"] = list(
                matched_skills
            )

        if missing_skills is not None:
            candidate["missing_skills"] = list(
                missing_skills
            )

        if notes is not None:
            candidate["notes"] = str(
                notes
            ).strip()

        if source is not None:
            candidate["source"] = str(
                source
            ).strip()

        candidate["updated_at"] = current_timestamp()

        return deepcopy(candidate)

    return None


# ============================================================
# DELETE CANDIDATE
# ============================================================

def delete_candidate(candidate_id):
    """
    Delete candidate using ID.
    """

    try:
        candidate_id = int(candidate_id)
    except (TypeError, ValueError):
        return False

    for index, candidate in enumerate(ats_db):

        if candidate.get("id") == candidate_id:

            ats_db.pop(index)

            return True

    return False


# ============================================================
# DELETE BY EMAIL
# ============================================================

def delete_candidate_by_email(email):
    """
    Delete candidate using email.
    """

    if not email:
        return False

    target = str(email).strip().lower()

    for index, candidate in enumerate(ats_db):

        stored_email = str(
            candidate.get("email", "")
        ).strip().lower()

        if stored_email == target:

            ats_db.pop(index)

            return True

    return False


# ============================================================
# CLEAR ATS
# ============================================================

def clear_candidates():
    """
    Delete all ATS candidates.
    """

    ats_db.clear()


# ============================================================
# COUNT CANDIDATES
# ============================================================

def count_candidates():
    return len(ats_db)


# ============================================================
# COUNT BY STATUS
# ============================================================

def count_by_status():
    """
    Return candidate counts for each pipeline stage.
    """

    result = {
        "New": 0,
        "Screening": 0,
        "Interview": 0,
        "Selected": 0,
        "Rejected": 0
    }

    for candidate in ats_db:

        status = candidate.get(
            "status",
            "New"
        )

        if status in result:

            result[status] += 1

    return result


# ============================================================
# AVERAGE MATCH SCORE
# ============================================================

def average_match_score():

    if not ats_db:
        return 0

    total = sum(
        safe_score(
            candidate.get(
                "match_score",
                0
            )
        )
        for candidate in ats_db
    )

    return round(
        total / len(ats_db)
    )


# ============================================================
# AVERAGE ATS SCORE
# ============================================================

def average_ats_score():

    if not ats_db:
        return 0

    total = sum(
        safe_score(
            candidate.get(
                "ats_score",
                0
            )
        )
        for candidate in ats_db
    )

    return round(
        total / len(ats_db)
    )


# ============================================================
# COMBINED HIRING SCORE
# ============================================================

def calculate_combined_score(candidate):
    """
    Combined score:
    60% job match + 40% ATS.
    """

    match = safe_score(
        candidate.get(
            "match_score",
            0
        )
    )

    ats = safe_score(
        candidate.get(
            "ats_score",
            0
        )
    )

    return round(
        match * 0.60 +
        ats * 0.40
    )


# ============================================================
# RANK CANDIDATES
# ============================================================

def ranked_candidates():

    candidates = list_candidates()

    for candidate in candidates:

        candidate["combined_score"] = (
            calculate_combined_score(
                candidate
            )
        )

    candidates.sort(
        key=lambda x: x.get(
            "combined_score",
            0
        ),
        reverse=True
    )

    return candidates


# ============================================================
# TOP CANDIDATES
# ============================================================

def top_candidates(limit=5):

    try:
        limit = int(limit)
    except (TypeError, ValueError):
        limit = 5

    limit = max(
        1,
        limit
    )

    return ranked_candidates()[:limit]


# ============================================================
# STATUS STATISTICS
# ============================================================

def get_statistics():

    total = count_candidates()

    selected = len(
        get_candidates_by_status(
            "Selected"
        )
    )

    interview = len(
        get_candidates_by_status(
            "Interview"
        )
    )

    screening = len(
        get_candidates_by_status(
            "Screening"
        )
    )

    rejected = len(
        get_candidates_by_status(
            "Rejected"
        )
    )

    return {
        "total": total,

        "new": len(
            get_candidates_by_status(
                "New"
            )
        ),

        "screening": screening,

        "interview": interview,

        "selected": selected,

        "rejected": rejected,

        "average_match_score":
            average_match_score(),

        "average_ats_score":
            average_ats_score()
    }


# ============================================================
# SKILL STATISTICS
# ============================================================

def skill_statistics():

    skill_counts = {}

    for candidate in ats_db:

        skills = candidate.get(
            "skills",
            []
        )

        for skill in skills:

            skill = str(
                skill
            ).strip()

            if not skill:
                continue

            skill_counts[skill] = (
                skill_counts.get(
                    skill,
                    0
                ) + 1
            )

    return dict(
        sorted(
            skill_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )


# ============================================================
# MISSING SKILL STATISTICS
# ============================================================

def missing_skill_statistics():

    skill_counts = {}

    for candidate in ats_db:

        skills = candidate.get(
            "missing_skills",
            []
        )

        for skill in skills:

            skill = str(
                skill
            ).strip()

            if not skill:
                continue

            skill_counts[skill] = (
                skill_counts.get(
                    skill,
                    0
                ) + 1
            )

    return dict(
        sorted(
            skill_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
    )


# ============================================================
# PIPELINE CONVERSION
# ============================================================

def pipeline_conversion():

    total = count_candidates()

    if total == 0:

        return {
            "screening_rate": 0,
            "interview_rate": 0,
            "selection_rate": 0
        }

    screening = len(
        get_candidates_by_status(
            "Screening"
        )
    )

    interview = len(
        get_candidates_by_status(
            "Interview"
        )
    )

    selected = len(
        get_candidates_by_status(
            "Selected"
        )
    )

    return {

        "screening_rate": round(
            screening / total * 100
        ),

        "interview_rate": round(
            interview / total * 100
        ),

        "selection_rate": round(
            selected / total * 100
        )
    }


# ============================================================
# EXPORT-READY DATA
# ============================================================

def export_data():

    """
    Return ATS records in a clean list
    suitable for pandas DataFrame/export.
    """

    records = []

    for candidate in ats_db:

        record = {
            "ID": candidate.get(
                "id"
            ),

            "Candidate": candidate.get(
                "name"
            ),

            "Email": candidate.get(
                "email"
            ),

            "Phone": candidate.get(
                "phone"
            ),

            "Job": candidate.get(
                "job_applied"
            ),

            "Match Score": candidate.get(
                "match_score"
            ),

            "ATS Score": candidate.get(
                "ats_score"
            ),

            "Combined Score":
                calculate_combined_score(
                    candidate
                ),

            "Status": candidate.get(
                "status"
            ),

            "Skills": ", ".join(
                candidate.get(
                    "skills",
                    []
                )
            ),

            "Missing Skills": ", ".join(
                candidate.get(
                    "missing_skills",
                    []
                )
            ),

            "Source": candidate.get(
                "source"
            ),

            "Created":
                candidate.get(
                    "created_at"
                ),

            "Updated":
                candidate.get(
                    "updated_at"
                )
        }

        records.append(record)

    return records


# ============================================================
# HEALTH CHECK
# ============================================================

def health_check():

    return {
        "status": "healthy",
        "candidate_count": len(ats_db),
        "available_statuses":
            STATUS_OPTIONS.copy(),
        "timestamp":
            current_timestamp()
    }