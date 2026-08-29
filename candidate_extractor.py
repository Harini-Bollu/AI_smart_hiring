import re
import pandas as pd
from datetime import datetime

SKILLS_LIST=[
"Python",
"Java",
"C++",
"C#",
"C",
"JavaScript",
"TypeScript",
"R",
"MATLAB",
"HTML",
"CSS",
"React",
"React.js",
"Node.js",
"Django",
"Flask",
"SQL",
"MySQL",
"PostgreSQL",
"SQLite",
"MongoDB",
"Oracle",
"PL/SQL",
"Machine Learning",
"Deep Learning",
"Artificial Intelligence",
"Data Science",
"Data Analytics",
"Natural Language Processing",
"NLP",
"Computer Vision",
"Pandas",
"NumPy",
"Matplotlib",
"Seaborn",
"TensorFlow",
"PyTorch",
"Scikit-learn",
"OpenCV",
"BeautifulSoup",
"Scrapy",
"Selenium",
"Git",
"GitHub",
"Jupyter",
"Jupyter Notebook",
"Visual Studio",
"Microsoft Excel",
"Microsoft Word",
"Microsoft PowerPoint",
"Linux",
"Unix",
"Windows",
"HTTP",
"HTTPS",
"TLS",
"REST API",
"Socket Programming",
"Operating Systems",
"DBMS",
"Data Structures",
"Algorithms",
"Computer Networks"
]

SECTION_NAMES={
"summary":[
"summary",
"professional summary",
"profile",
"career objective",
"objective",
"about me"
],
"education":[
"education",
"educational background",
"academic background",
"academic qualifications",
"qualifications"
],
"skills":[
"skills",
"technical skills",
"technical expertise",
"technical competencies",
"core skills",
"technologies",
"skills and technologies"
],
"experience":[
"experience",
"work experience",
"professional experience",
"employment history",
"work history",
"career history",
"internship experience"
],
"projects":[
"projects",
"technical projects",
"academic projects",
"personal projects",
"project experience",
"key projects"
],
"certifications":[
"certifications",
"certificates",
"professional certifications",
"courses",
"training",
"courses and certifications"
],
"awards":[
"awards",
"achievements",
"accomplishments",
"honors",
"awards and achievements"
]
}

def clean_text(text):
    if not text:
        return ""
    text=text.replace("\r\n","\n")
    text=text.replace("\r","\n")
    text=text.replace("\t"," ")
    text=re.sub(r"([A-Za-z]{2,})\n([a-z]{2,})",r"\1\2",text)
    text=re.sub(r"[ ]{2,}"," ",text)
    text=re.sub(r"\n{3,}","\n\n",text)
    return text.strip()

def clean_line(line):
    if not line:
        return ""
    line=line.strip()
    line=re.sub(r"^[•●▪◦■□◆◇*\\\-–—]+\s*","",line)
    line=line.replace("","")
    line=re.sub(
        r"\b([A-Za-z]{2,})\s+([a-z]{2,})\b",
        lambda m:m.group(1)+m.group(2)
        if len(m.group(1))>=3 and len(m.group(2))<=4
        else m.group(0),
        line
    )
    line=re.sub(r"\s+"," ",line)
    return line.strip()

def normalize_heading(line):
    line=clean_line(line)
    line=re.sub(r"^\d+\s*[.)\-:]\s*","",line)
    line=line.rstrip(":")
    return line.lower().strip()

def detect_section(line):
    normalized=normalize_heading(line)
    if not normalized:
        return None
    for section,names in SECTION_NAMES.items():
        for name in names:
            if normalized==name.lower():
                return section
    return None

def extract_sections(text):
    text=clean_text(text)
    lines=text.split("\n")
    sections={key:[] for key in SECTION_NAMES}
    current_section=None
    for raw_line in lines:
        line=clean_line(raw_line)
        if not line:
            continue
        detected=detect_section(line)
        if detected:
            current_section=detected
            continue
        if current_section:
            sections[current_section].append(line)
    for section in sections:
        sections[section]="\n".join(sections[section]).strip()
    return sections

def extract_email(text):
    pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match=re.search(pattern,text)
    if match:
        return match.group(0)
    return None

def extract_phone(text):
    patterns=[
        r"\+\d{1,3}[\s.-]?\d{5}[\s.-]?\d{5}",
        r"\+\d{1,3}[\s.-]?\d{10}",
        r"\b[6-9]\d{4}[\s.-]\d{5}\b",
        r"\b[6-9]\d{9}\b",
        r"\b[6-9]\d{4}-\d{5}\b"
    ]
    for pattern in patterns:
        match=re.search(pattern,text)
        if match:
            phone=match.group(0)
            digits=re.sub(r"\D","",phone)
            if digits.startswith("91") and len(digits)==12:
                return "+91 "+digits[2:7]+" "+digits[7:]
            if len(digits)==10:
                return "+91 "+digits[:5]+" "+digits[5:]
            return phone
    return None

def is_valid_name(line):
    if not line:
        return False
    line=clean_line(line)
    if "@" in line:
        return False
    if re.search(r"(linkedin|github|https?://|www\.)",line,re.IGNORECASE):
        return False
    if re.search(r"\d{5,}",line):
        return False
    if re.search(r"\b(address|city|province|country)\b",line,re.IGNORECASE):
        return False
    words=re.findall(r"[A-Za-z]+(?:['-][A-Za-z]+)?",line)
    if not 2<=len(words)<=4:
        return False
    blocked={
        "python",
        "java",
        "javascript",
        "typescript",
        "html",
        "css",
        "sql",
        "mysql",
        "postgresql",
        "github",
        "git",
        "skills",
        "technical",
        "projects",
        "experience",
        "education",
        "certifications",
        "awards",
        "university",
        "college",
        "department",
        "science",
        "engineering",
        "visual",
        "studio",
        "microsoft",
        "intern",
        "internship",
        "resume",
        "curriculum",
        "vitae"
    }
    lower_words={word.lower() for word in words}
    if lower_words.intersection(blocked):
        return False
    if not all(
        re.fullmatch(r"[A-Za-z]+(?:['-][A-Za-z]+)?",word)
        for word in words
    ):
        return False
    return True

def extract_name(text):
    lines=[
        clean_line(line)
        for line in text.split("\n")
        if clean_line(line)
    ]
    for line in lines[:12]:
        if is_valid_name(line):
            return line
    for line in lines[:20]:
        words=line.split()
        if 2<=len(words)<=4:
            if all(word[0].isupper() for word in words if word):
                if is_valid_name(line):
                    return line
    return None

def extract_skills(text):
    sections=extract_sections(text)
    skills_text=sections["skills"]
    if not skills_text:
        skills_text=text
    found=[]
    skills_sorted=sorted(SKILLS_LIST,key=len,reverse=True)
    for skill in skills_sorted:
        pattern=r"(?<![A-Za-z0-9])"+re.escape(skill)+r"(?![A-Za-z0-9])"
        if re.search(pattern,skills_text,re.IGNORECASE):
            if not any(existing.lower()==skill.lower() for existing in found):
                found.append(skill)
    return found

def extract_education(text):
    sections=extract_sections(text)
    education_text=sections["education"]
    if not education_text:
        return []
    result=[]
    for line in education_text.split("\n"):
        line=clean_line(line)
        if not line:
            continue
        if line not in result:
            result.append(line)
    return result

def looks_like_project_title(line):
    line_lower=line.lower()
    description_words=[
        "developed",
        "implemented",
        "performed",
        "created",
        "used",
        "analyzed",
        "designed",
        "built",
        "responsible",
        "worked",
        "project involved"
    ]
    if any(line_lower.startswith(word) for word in description_words):
        return False
    if re.search(
        r"\b(system|application|website|platform|prediction|analysis|analyzer|management|using|detection)\b",
        line_lower
    ):
        if len(line.split())<=15:
            return True
    if len(line.split())<=10:
        words=line.split()
        capital_count=sum(
            1
            for word in words
            if word and word[0].isupper()
        )
        if capital_count>=max(2,len(words)//2):
            return True
    return False

def extract_projects(text):
    sections=extract_sections(text)
    project_text=sections["projects"]
    if not project_text:
        return []
    lines=[
        clean_line(line)
        for line in project_text.split("\n")
        if clean_line(line)
    ]
    projects=[]
    current_title=None
    current_description=[]

    def save_current():
        nonlocal current_title
        nonlocal current_description
        if not current_title:
            return
        result=current_title
        if current_description:
            description=" ".join(current_description)
            result+=" | "+description
        result=re.sub(r"\s+"," ",result).strip()
        if result not in projects:
            projects.append(result)
        current_title=None
        current_description=[]

    for line in lines:
        if re.fullmatch(
            r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
            line,
            re.IGNORECASE
        ):
            continue
        if looks_like_project_title(line):
            save_current()
            current_title=line
        else:
            if current_title:
                current_description.append(line)
            else:
                current_title=line
    save_current()
    return projects

def extract_experience(text):
    sections=extract_sections(text)
    experience_text=sections["experience"]
    if not experience_text:
        return []
    lines=[
        clean_line(line)
        for line in experience_text.split("\n")
        if clean_line(line)
    ]
    result=[]
    for line in lines:
        if line.lower() in [
            "experience",
            "work experience",
            "professional experience"
        ]:
            continue
        if line not in result:
            result.append(line)
    return result

def extract_certifications(text):
    sections=extract_sections(text)
    cert_text=sections["certifications"]
    if not cert_text:
        return []
    lines=[
        clean_line(line)
        for line in cert_text.split("\n")
        if clean_line(line)
    ]
    result=[]
    current=None
    for line in lines:
        if re.fullmatch(
            r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
            line,
            re.IGNORECASE
        ):
            if current:
                current+=" - "+line
            continue
        if current:
            current+=" - "+line
        else:
            current=line
    if current:
        result.append(re.sub(r"\s+"," ",current).strip())
    final=[]
    for item in result:
        if item not in final:
            final.append(item)
    return final

def extract_awards(text):
    sections=extract_sections(text)
    award_text=sections["awards"]
    if not award_text:
        return []
    lines=[
        clean_line(line)
        for line in award_text.split("\n")
        if clean_line(line)
    ]
    awards=[]
    current=None
    award_start_pattern=re.compile(
        r"\b(secured|won|winner|position|award|achievement|honor|hackathon|first|second|third)\b",
        re.IGNORECASE
    )
    for line in lines:
        if re.fullmatch(
            r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
            line,
            re.IGNORECASE
        ):
            continue
        if award_start_pattern.search(line):
            if current:
                awards.append(current.strip())
            current=line
        else:
            if current:
                current+=" "+line
    if current:
        awards.append(current.strip())
    cleaned=[]
    for award in awards:
        award=re.sub(r"\s+"," ",award).strip()
        if award and award not in cleaned:
            cleaned.append(award)
    return cleaned

def calculate_experience_years(text):
    sections=extract_sections(text)
    experience_text=sections["experience"]
    if not experience_text:
        return None
    text_lower=experience_text.lower()

    patterns=[
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+of\s+experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*years?\s+experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*yrs?\s+of\s+experience",
        r"(\d+(?:\.\d+)?)\s*\+?\s*yrs?\s+experience"
    ]

    values=[]
    for pattern in patterns:
        matches=re.findall(pattern,text_lower)
        for value in matches:
            try:
                values.append(float(value))
            except ValueError:
                pass

    if values:
        return max(values)

    year_pattern=r"\b(20\d{2})\s*(?:-|–|—|to)\s*(20\d{2}|present|current)\b"
    matches=re.findall(year_pattern,text_lower)
    durations=[]
    current_year=datetime.now().year

    for start,end in matches:
        try:
            start_year=int(start)
            if end in ["present","current"]:
                end_year=current_year
            else:
                end_year=int(end)
            duration=end_year-start_year
            if 0<duration<=50:
                durations.append(float(duration))
        except ValueError:
            continue

    if durations:
        return max(durations)

    month_pattern=(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+(20\d{2})\s*(?:-|–|—|to)\s*"
        r"(January|February|March|April|May|June|July|August|September|October|November|December)"
        r"\s+(20\d{2}|present|current)"
    )

    matches=re.findall(month_pattern,text_lower)

    months={
        "january":1,
        "february":2,
        "march":3,
        "april":4,
        "may":5,
        "june":6,
        "july":7,
        "august":8,
        "september":9,
        "october":10,
        "november":11,
        "december":12
    }

    durations=[]
    current_date=datetime.now()

    for start_month,start_year,end_month,end_year in matches:
        try:
            start_date=int(start_year)*12+months[start_month]
            if end_year in ["present","current"]:
                end_date=current_date.year*12+current_date.month
            else:
                end_date=int(end_year)*12+months[end_month]
            duration_months=end_date-start_date
            if 0<duration_months<=600:
                durations.append(round(duration_months/12,1))
        except Exception:
            continue

    if durations:
        return max(durations)

    return None

def extract_candidate_info(text):
    text=clean_text(text)
    candidate={
        "name":extract_name(text),
        "email":extract_email(text),
        "phone":extract_phone(text),
        "education":extract_education(text),
        "skills":extract_skills(text),
        "experience":extract_experience(text),
        "experience_years":calculate_experience_years(text),
        "projects":extract_projects(text),
        "certifications":extract_certifications(text),
        "awards":extract_awards(text)
    }
    return candidate

def generate_profile(candidate):
    data={
        "Name":candidate["name"],
        "Email":candidate["email"],
        "Phone":candidate["phone"],
        "Education":" | ".join(candidate["education"]),
        "Skills":", ".join(candidate["skills"]),
        "Experience":" | ".join(candidate["experience"]),
        "Experience Years":candidate["experience_years"],
        "Projects":" | ".join(candidate["projects"]),
        "Certifications":" | ".join(candidate["certifications"]),
        "Awards":" | ".join(candidate["awards"])
    }
    return pd.DataFrame([data])

def display_candidate_profile(candidate):
    print("\n")
    print("="*70)
    print("              STRUCTURED CANDIDATE PROFILE")
    print("="*70)
    print(f"\nName             : {candidate['name'] or 'Not detected'}")
    print(f"Email            : {candidate['email'] or 'Not detected'}")
    print(f"Phone            : {candidate['phone'] or 'Not detected'}")
    print("\nEducation:")
    if candidate["education"]:
        for item in candidate["education"]:
            print(f"  • {item}")
    else:
        print("  Not detected")
    print("\nSkills:")
    if candidate["skills"]:
        print("  "+", ".join(candidate["skills"]))
    else:
        print("  Not detected")
    print("\nExperience:")
    if candidate["experience"]:
        for item in candidate["experience"]:
            print(f"  • {item}")
    else:
        print("  Not detected")
    print("\nExperience Duration:")
    if candidate["experience_years"] is not None:
        print(f"  {candidate['experience_years']} years")
    else:
        print("  Not detected")
    print("\nProjects:")
    if candidate["projects"]:
        for item in candidate["projects"]:
            print(f"  • {item}")
    else:
        print("  Not detected")
    print("\nCertifications:")
    if candidate["certifications"]:
        for item in candidate["certifications"]:
            print(f"  • {item}")
    else:
        print("  Not detected")
    print("\nAwards:")
    if candidate["awards"]:
        for item in candidate["awards"]:
            print(f"  • {item}")
    else:
        print("  Not detected")
    print("\n"+"="*70)

def save_profile_to_csv(candidate,filename="candidate_profile.csv"):
    df=generate_profile(candidate)
    df.to_csv(filename,index=False)
    print(f"\nStructured profile saved to: {filename}")