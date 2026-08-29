import streamlit as st
import pandas as pd
import tempfile
import os

from resume_parser import extract_text_from_pdf, extract_text_from_docx
from candidate_extractor import extract_candidate_info


st.set_page_config(
    page_title="AI Smart Hiring",
    layout="wide"
)

if "candidate" not in st.session_state:
    st.session_state.candidate = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "filename" not in st.session_state:
    st.session_state.filename = ""

if "processed_count" not in st.session_state:
    st.session_state.processed_count = 0
with st.sidebar:

    st.title("Smart Hiring")

    st.divider()

    st.subheader("MAIN MENU")

    st.button(
        "Dashboard",
        use_container_width=True
    )

    st.button(
        "Resume Parsing",
        use_container_width=True
    )

    st.button(
        "Candidates",
        use_container_width=True
    )

    st.button(
        "Analytics",
        use_container_width=True
    )

    st.divider()

    st.subheader("SYSTEM")

    st.button(
        "Settings",
        use_container_width=True
    )

    st.divider()

    st.caption("AI-powered recruitment")
    st.caption("Milestone 1 • Resume Profiling")
st.title("Resume Parsing & Candidate Profiling")

st.write(
    "Upload resumes and automatically extract candidate "
    "information using NLP and AI-powered processing."
)


st.divider()


upload_col, progress_col = st.columns([1.4, 1])


with upload_col:

    st.subheader("Upload Resume")

    st.caption(
        "Upload a candidate resume to generate a structured profile."
    )

    uploaded_file = st.file_uploader(
        "Choose a resume",
        type=["pdf", "docx"]
    )

    if uploaded_file is not None:

        st.success(
            f"Selected file: {uploaded_file.name}"
        )

        analyze_button = st.button(
            "Analyze Resume",
            type="primary",
            use_container_width=True
        )


        if analyze_button:

            file_extension = os.path.splitext(
                uploaded_file.name
            )[1].lower()

            temp_path = None

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getbuffer()
                )

                temp_path = temp_file.name


            try:
                if file_extension == ".pdf":

                    with st.spinner(
                        "Reading PDF resume..."
                    ):

                        resume_text = extract_text_from_pdf(
                            temp_path
                        )


                elif file_extension == ".docx":

                    with st.spinner(
                        "Reading DOCX resume..."
                    ):

                        resume_text = extract_text_from_docx(
                            temp_path
                        )

                else:

                    st.error(
                        "Unsupported file format."
                    )

                    st.stop()

                with st.spinner(
                    "Extracting candidate information..."
                ):

                    candidate = extract_candidate_info(
                        resume_text
                    )

                st.session_state.candidate = candidate

                st.session_state.resume_text = resume_text

                st.session_state.filename = uploaded_file.name

                st.session_state.processed_count += 1


                st.success(
                    "Resume processed successfully!"
                )


            except Exception as error:

                st.error(
                    f"Error processing resume: {error}"
                )


            finally:

                if (
                    temp_path
                    and os.path.exists(temp_path)
                ):

                    os.remove(temp_path)

with progress_col:

    st.subheader("Parsing Progress")

    st.caption(
        "Candidate profile extraction status"
    )


    candidate = st.session_state.candidate

    if candidate:

        fields = [

            bool(
                candidate.get("name")
            ),

            bool(
                candidate.get("email")
            ),

            bool(
                candidate.get("phone")
            ),

            bool(
                candidate.get("education")
            ),

            bool(
                candidate.get("skills")
            ),

            bool(
                candidate.get("experience")
            ),

            bool(
                candidate.get("certifications")
            ),

            bool(
                candidate.get("projects")
            )
        ]

        completed = sum(fields)

    else:

        completed = 0

    if candidate:

        if completed == 8:

            # Maximum displayed parsing confidence
            percentage = 0.95

        else:

            percentage = (
                completed / 8
            ) * 0.95

    else:

        percentage = 0.0

    st.metric(
        "Profile Completeness",
        f"{int(percentage * 100)}%"
    )
    st.progress(
        percentage
    )

    st.write(
        f"{completed} / 8 fields extracted"
    )


    st.divider()
    if candidate:

        skills_count = len(
            candidate.get(
                "skills",
                []
            )
        )

        projects_count = len(
            candidate.get(
                "projects",
                []
            )
        )

        experience_count = len(
            candidate.get(
                "experience",
                []
            )
        )

        education_count = len(
            candidate.get(
                "education",
                []
            )
        )

    else:

        skills_count = 0
        projects_count = 0
        experience_count = 0
        education_count = 0
    s1, s2 = st.columns(2)

    with s1:

        st.metric(
            "Skills",
            skills_count
        )
    with s2:

        st.metric(
            "Projects",
            projects_count
        )

    s3, s4 = st.columns(2)
    with s3:

        st.metric(
            "Experience",
            experience_count
        )
    with s4:

        st.metric(
            "🎓 Education",
            education_count
        )
if st.session_state.candidate:

    candidate = st.session_state.candidate


    st.divider()

    st.header(
        "Candidate Profile"
    )

    st.caption(
        "Information extracted from the uploaded resume."
    )

    profile_col1, profile_col2 = st.columns(
        [1, 2]
    )


    with profile_col1:

        st.subheader(
            candidate.get(
                "name"
            ) or "Name not detected"
        )

        st.write(
            candidate.get(
                "email"
            ) or "Email not detected"
        )

        st.write(
            candidate.get(
                "phone"
            ) or "Phone not detected"
        )
    with profile_col2:

        st.subheader(
            "Skills"
        )

        skills = candidate.get(
            "skills",
            []
        )


        if skills:

            for skill in skills:

                st.info(
                    skill
                )

        else:

            st.write(
                "No skills detected."
            )
    st.divider()

    education_col, experience_col = st.columns(2)
    with education_col:

        st.subheader(
            "🎓 Education"
        )

        education = candidate.get(
            "education",
            []
        )


        if education:

            for item in education:

                st.write(
                    "•",
                    item
                )

        else:

            st.write(
                "No education detected."
            )
    with experience_col:

        st.subheader(
            "Experience"
        )

        experience = candidate.get(
            "experience",
            []
        )
        if experience:

            for item in experience:

                st.write(
                    "•",
                    item
                )
        else:

            st.write(
                "No experience detected."
            )
    st.divider()

    cert_col, project_col = st.columns(2)

    with cert_col:

        st.subheader(
            "Certifications"
        )

        certifications = candidate.get(
            "certifications",
            []
        )
        if certifications:

            for item in certifications:

                st.write(
                    "•",
                    item
                )

        else:

            st.write(
                "No certifications detected."
            )

    with project_col:

        st.subheader(
            "Projects"
        )

        projects = candidate.get(
            "projects",
            []
        )


        if projects:

            for item in projects:

                st.write(
                    "•",
                    item
                )

        else:

            st.write(
                "No projects detected."
            )
    st.divider()

    st.header(
        "Structured Candidate Profile"
    )

    st.caption(
        "Candidate information stored in structured format."
    )

    profile_data = {

        "Name": [
            candidate.get(
                "name"
            )
        ],

        "Email": [
            candidate.get(
                "email"
            )
        ],

        "Phone": [
            candidate.get(
                "phone"
            )
        ],

        "Education": [
            ", ".join(
                candidate.get(
                    "education",
                    []
                )
            )
        ],

        "Skills": [
            ", ".join(
                candidate.get(
                    "skills",
                    []
                )
            )
        ],

        "Experience": [
            ", ".join(
                candidate.get(
                    "experience",
                    []
                )
            )
        ],

        "Certifications": [
            ", ".join(
                candidate.get(
                    "certifications",
                    []
                )
            )
        ],

        "Projects": [
            ", ".join(
                candidate.get(
                    "projects",
                    []
                )
            )
        ]
    }
    df = pd.DataFrame(
        profile_data
    )
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    csv_data = df.to_csv(
        index=False
    ).encode(
        "utf-8"
    )
    st.download_button(
        label="⬇ Download Candidate Profile",
        data=csv_data,
        file_name="candidate_profile.csv",
        mime="text/csv"
    )
    st.divider()

    with st.expander(
        "View Extracted Resume Text"
    ):

        st.text(
            st.session_state.resume_text
        )
else:

    st.divider()

    st.info(
        "Upload a PDF or DOCX resume above "
        "to generate the candidate profile."
    )