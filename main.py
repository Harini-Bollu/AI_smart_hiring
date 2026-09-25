import os
import pandas as pd

from resume_parser import extract_resume_text

from candidate_extractor import (
    extract_candidate_info,
    generate_profile,
    display_candidate_profile
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

RESUME_FOLDER = os.path.join(
    BASE_DIR,
    "resumes"
)

CSV_FILE = os.path.join(
    BASE_DIR,
    "candidate_profile.csv"
)

SUPPORTED_EXTENSIONS = (
    ".pdf",
    ".docx",
    ".txt"
)


# ============================================================
# FIND RESUMES
# ============================================================

def find_resumes():

    if not os.path.exists(
        RESUME_FOLDER
    ):

        os.makedirs(
            RESUME_FOLDER
        )

        return []

    files = []

    for filename in os.listdir(
        RESUME_FOLDER
    ):

        full_path = os.path.join(
            RESUME_FOLDER,
            filename
        )

        # Ignore folders
        if not os.path.isfile(
            full_path
        ):
            continue

        # Check extension
        if filename.lower().endswith(
            SUPPORTED_EXTENSIONS
        ):

            files.append(
                filename
            )

    files.sort(
        key=lambda x: x.lower()
    )

    return files


# ============================================================
# PROCESS ONE RESUME
# ============================================================

def process_resume(file_path):

    print("\n")
    print("-" * 70)

    print(
        f"Processing: {os.path.basename(file_path)}"
    )

    print("-" * 70)

    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    text = extract_resume_text(
        file_path
    )

    if not text.strip():

        print(
            "ERROR: No text extracted from resume."
        )

        return None

    # --------------------------------------------------------
    # Extract candidate information
    # --------------------------------------------------------

    candidate_info = extract_candidate_info(
        text
    )

    # --------------------------------------------------------
    # Validate name
    # --------------------------------------------------------

    candidate_name = candidate_info.get(
        "name"
    )

    if not candidate_name:

        print(
            "WARNING: Candidate name could not be detected."
        )

        print(
            "Skipping this resume."
        )

        return None

    # --------------------------------------------------------
    # Display profile
    # --------------------------------------------------------

    display_candidate_profile(
        candidate_info
    )

    # --------------------------------------------------------
    # Generate DataFrame
    # --------------------------------------------------------

    profile = generate_profile(
        candidate_info
    )

    return profile


# ============================================================
# REMOVE OLD CSV
# ============================================================

def remove_old_csv():

    if os.path.exists(
        CSV_FILE
    ):

        try:

            os.remove(
                CSV_FILE
            )

            print(
                "\nOld candidate_profile.csv removed."
            )

        except Exception as error:

            print(
                f"\nCould not remove old CSV: {error}"
            )


# ============================================================
# REMOVE DUPLICATES
# ============================================================

def remove_duplicates(df):

    if df.empty:
        return df

    # --------------------------------------------------------
    # Clean Email
    # --------------------------------------------------------

    if "Email" in df.columns:

        df["Email"] = (
            df["Email"]
            .fillna("")
            .astype(str)
            .str.strip()
            .str.lower()
        )

        # Keep valid emails unique
        valid_email_mask = (
            df["Email"] != ""
        ) & (
            df["Email"] != "not found"
        )

        valid_email_df = df[
            valid_email_mask
        ]

        invalid_email_df = df[
            ~valid_email_mask
        ]

        valid_email_df = (
            valid_email_df
            .drop_duplicates(
                subset=["Email"],
                keep="first"
            )
        )

        df = pd.concat(
            [
                valid_email_df,
                invalid_email_df
            ],
            ignore_index=True
        )

    # --------------------------------------------------------
    # Remove duplicate names
    # --------------------------------------------------------

    if "Name" in df.columns:

        df["Name"] = (
            df["Name"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df = df.drop_duplicates(
            subset=["Name"],
            keep="first"
        )

    # --------------------------------------------------------
    # Reset index
    # --------------------------------------------------------

    df = df.reset_index(
        drop=True
    )

    return df


# ============================================================
# SAVE ALL PROFILES
# ============================================================

def save_all_profiles(profiles):

    if not profiles:

        print(
            "\nNo valid candidate profiles found."
        )

        return None

    # Combine all candidates
    final_df = pd.concat(
        profiles,
        ignore_index=True
    )

    # Remove duplicates
    final_df = remove_duplicates(
        final_df
    )

    # Save
    final_df.to_csv(
        CSV_FILE,
        index=False
    )

    print("\n")
    print("=" * 70)

    print(
        f"Final candidate CSV saved to:"
    )

    print(
        CSV_FILE
    )

    print("=" * 70)

    return final_df


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("             AI SMART HIRING")
    print("             RESUME PARSER")
    print("=" * 70)

    # --------------------------------------------------------
    # Find resumes
    # --------------------------------------------------------

    resume_files = find_resumes()

    if not resume_files:

        print("\nNo resumes found.")

        print(
            f"\nPut PDF/DOCX/TXT resumes inside:"
        )

        print(
            RESUME_FOLDER
        )

        return

    print(
        f"\nFound {len(resume_files)} resume(s)."
    )

    print("\nResume files:")

    for index, filename in enumerate(
        resume_files,
        start=1
    ):

        print(
            f"  {index}. {filename}"
        )

    # --------------------------------------------------------
    # Remove previous CSV
    # --------------------------------------------------------

    remove_old_csv()

    # --------------------------------------------------------
    # Process all resumes
    # --------------------------------------------------------

    profiles = []

    for filename in resume_files:

        file_path = os.path.join(
            RESUME_FOLDER,
            filename
        )

        try:

            profile = process_resume(
                file_path
            )

            if profile is not None:

                profiles.append(
                    profile
                )

        except Exception as error:

            print(
                f"\nERROR processing {filename}:"
            )

            print(
                error
            )

    # --------------------------------------------------------
    # Save final CSV
    # --------------------------------------------------------

    final_df = save_all_profiles(
        profiles
    )

    # --------------------------------------------------------
    # Display final results
    # --------------------------------------------------------

    if final_df is not None:

        print("\n")
        print("=" * 70)
        print("             FINAL CANDIDATE LIST")
        print("=" * 70)

        print(
            final_df.to_string(
                index=False
            )
        )

        print("\n")
        print(
            f"Total unique candidates: {len(final_df)}"
        )

        print("=" * 70)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()