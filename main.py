import os
from resume_parser import extract_resume_text
from candidate_extractor import (
    extract_candidate_info,
    generate_profile,
    display_candidate_profile,
    save_profile_to_csv
)

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
RESUME_FOLDER=os.path.join(BASE_DIR,"resumes")
SUPPORTED_EXTENSIONS=(".pdf",".docx",".txt")

def find_resumes():
    if not os.path.exists(RESUME_FOLDER):
        os.makedirs(RESUME_FOLDER)
        return []
    files=[]
    for filename in os.listdir(RESUME_FOLDER):
        full_path=os.path.join(RESUME_FOLDER,filename)
        if not os.path.isfile(full_path):
            continue
        if filename.lower().endswith(SUPPORTED_EXTENSIONS):
            files.append(filename)
    files.sort(key=lambda x:x.lower())
    return files

def process_resume(file_path):
    print("\n"+"="*70)
    print("                 AI SMART HIRING")
    print("="*70)
    print(f"\nResume file: {file_path}")
    print("\n[1/4] Reading resume...")
    text=extract_resume_text(file_path)
    if not text.strip():
        raise ValueError("No text could be extracted from the resume.")
    print("✓ Resume text extracted successfully.")
    print(f"✓ Extracted characters: {len(text)}")
    print(f"✓ Extracted words: {len(text.split())}")
    print("\n[2/4] Analyzing candidate information...")
    candidate_info=extract_candidate_info(text)
    print("✓ Candidate information extracted.")
    print("\n[3/4] Generating structured profile...")
    profile=generate_profile(candidate_info)
    print("✓ Structured profile generated.")
    display_candidate_profile(candidate_info)
    print("\n[4/4] Saving candidate profile...")
    csv_path=os.path.join(BASE_DIR,"candidate_profile.csv")
    save_profile_to_csv(candidate_info,csv_path)
    print("\n✓ Resume processing completed successfully.")
    return profile

def main():
    resume_files=find_resumes()
    if not resume_files:
        print("\n"+"="*70)
        print("ERROR")
        print("="*70)
        print("\nNo resume found inside:")
        print(RESUME_FOLDER)
        print("\nPut a PDF, DOCX, or TXT resume inside the 'resumes' folder.")
        return
    if len(resume_files)>1:
        print("\nAvailable resumes:")
        for index,filename in enumerate(resume_files,start=1):
            print(f"  {index}. {filename}")
        print("\nUsing the first resume automatically:")
    resume_filename=resume_files[0]
    resume_path=os.path.join(RESUME_FOLDER,resume_filename)
    try:
        profile=process_resume(resume_path)
        print("\n")
        print("="*70)
        print("                  PANDAS DATAFRAME")
        print("="*70)
        print(profile.to_string(index=False))
        print("\n")
    except Exception as error:
        print("\n"+"="*70)
        print("ERROR")
        print("="*70)
        print(f"\n{type(error).__name__}: {error}")

if __name__=="__main__":
    main()