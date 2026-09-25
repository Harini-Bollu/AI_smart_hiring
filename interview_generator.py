# interview_generator.py
# ============================================================
# AI SMART HIRING - INTERVIEW QUESTION GENERATOR
# ============================================================

import re
import random


# ============================================================
# TECHNICAL QUESTION BANK
# ============================================================

TECHNICAL_QUESTIONS = {

    "Python": [
        "Explain the difference between a list, tuple, set, and dictionary in Python.",
        "What is the difference between shallow copy and deep copy in Python?",
        "Explain Python decorators with a practical example.",
        "What are lambda functions and where would you use them?",
        "Explain exception handling in Python.",
        "What is the difference between == and is in Python?",
        "Explain list comprehension with an example.",
        "What are generators in Python and why are they useful?",
        "How does object-oriented programming work in Python?",
        "What is the difference between *args and **kwargs in Python?"
    ],

    "Java": [
        "Explain the four main principles of object-oriented programming in Java.",
        "What is the difference between an interface and an abstract class?",
        "Explain method overloading and method overriding.",
        "What is exception handling in Java?",
        "Explain the difference between ArrayList and LinkedList.",
        "What is the Java Virtual Machine?",
        "Explain inheritance in Java with an example.",
        "What is garbage collection in Java?",
        "Explain the difference between == and equals() in Java.",
        "What are Java collections?"
    ],

    "C++": [
        "Explain the main features of C++.",
        "What is the difference between a pointer and a reference?",
        "Explain inheritance in C++.",
        "What is a virtual function?",
        "Explain constructors and destructors in C++.",
        "What is function overloading?",
        "Explain memory management in C++.",
        "What is polymorphism in C++?",
        "Explain the difference between stack and heap memory.",
        "What are templates in C++?"
    ],

    "C": [
        "Explain pointers in C with an example.",
        "What is the difference between malloc() and calloc()?",
        "Explain structures and unions in C.",
        "What are arrays and pointers in C?",
        "Explain dynamic memory allocation in C.",
        "What is a segmentation fault?",
        "Explain functions and recursion in C.",
        "What is the difference between call by value and call by reference?",
        "Explain file handling in C.",
        "What are storage classes in C?"
    ],

    "JavaScript": [
        "Explain the difference between var, let, and const.",
        "What is hoisting in JavaScript?",
        "Explain closures in JavaScript.",
        "What is the difference between == and ===?",
        "Explain promises and async/await.",
        "What is the DOM?",
        "Explain event bubbling and event capturing.",
        "What are arrow functions?",
        "Explain callback functions in JavaScript.",
        "What is the difference between synchronous and asynchronous JavaScript?"
    ],

    "TypeScript": [
        "What is TypeScript and why is it used?",
        "Explain the difference between TypeScript and JavaScript.",
        "What are interfaces in TypeScript?",
        "What are types and type aliases?",
        "Explain generics in TypeScript.",
        "What is type inference?",
        "Explain enums in TypeScript.",
        "What are optional properties?",
        "How does TypeScript improve code maintainability?",
        "Explain union and intersection types."
    ],

    "React": [
        "What is React and why is it used?",
        "Explain React components.",
        "What is the difference between props and state?",
        "Explain the React useState hook.",
        "What is useEffect and when is it used?",
        "What is the virtual DOM?",
        "Explain React component lifecycle.",
        "What is conditional rendering in React?",
        "How do you handle forms in React?",
        "What is React Router?"
    ],

    "Node.js": [
        "What is Node.js?",
        "Why is Node.js useful for backend development?",
        "Explain the Node.js event loop.",
        "What is npm?",
        "How do you create an API using Node.js?",
        "What is Express.js?",
        "Explain middleware in Node.js.",
        "How does asynchronous programming work in Node.js?",
        "How do you handle errors in Node.js?",
        "How can Node.js connect to a database?"
    ],

    "SQL": [
        "What is SQL and why is it used?",
        "Explain the difference between WHERE and HAVING.",
        "What is a primary key?",
        "What is a foreign key?",
        "Explain different types of SQL joins.",
        "What is normalization?",
        "Explain GROUP BY with an example.",
        "What is a subquery?",
        "Explain the difference between DELETE, DROP, and TRUNCATE.",
        "What are indexes in SQL?"
    ],

    "MySQL": [
        "What is MySQL?",
        "Explain primary keys and foreign keys in MySQL.",
        "What are MySQL joins?",
        "Explain normalization in MySQL.",
        "How do you optimize a MySQL query?",
        "What are indexes in MySQL?",
        "Explain stored procedures.",
        "What are views in MySQL?",
        "Explain transactions in MySQL.",
        "What is the difference between CHAR and VARCHAR?"
    ],

    "PostgreSQL": [
        "What is PostgreSQL?",
        "What are the advantages of PostgreSQL?",
        "Explain PostgreSQL indexing.",
        "What are PostgreSQL schemas?",
        "Explain transactions in PostgreSQL.",
        "What is a CTE?",
        "Explain window functions.",
        "How is PostgreSQL different from MySQL?",
        "What are PostgreSQL views?",
        "How would you optimize a PostgreSQL query?"
    ],

    "MongoDB": [
        "What is MongoDB?",
        "How is MongoDB different from relational databases?",
        "What is a document in MongoDB?",
        "Explain collections in MongoDB.",
        "What is MongoDB aggregation?",
        "Explain indexing in MongoDB.",
        "What is replication in MongoDB?",
        "What is sharding?",
        "How do you update a MongoDB document?",
        "What are the advantages of NoSQL databases?"
    ],

    "Machine Learning": [
        "What is machine learning?",
        "Explain supervised and unsupervised learning.",
        "What is overfitting?",
        "What is underfitting?",
        "Explain the bias-variance tradeoff.",
        "What is cross-validation?",
        "Explain classification and regression.",
        "What is feature engineering?",
        "How do you handle missing values?",
        "How do you evaluate a machine learning model?"
    ],

    "Deep Learning": [
        "What is deep learning?",
        "What is an artificial neural network?",
        "Explain the architecture of a neural network.",
        "What is backpropagation?",
        "What is an activation function?",
        "Explain CNNs.",
        "Explain RNNs.",
        "What is dropout?",
        "What is batch normalization?",
        "What is gradient descent?"
    ],

    "NLP": [
        "What is Natural Language Processing?",
        "Explain tokenization.",
        "What is stemming?",
        "What is lemmatization?",
        "Explain POS tagging.",
        "What are stop words?",
        "What is named entity recognition?",
        "Explain TF-IDF.",
        "What are word embeddings?",
        "What is sentiment analysis?"
    ],

    "AI": [
        "What is artificial intelligence?",
        "What is the difference between AI and machine learning?",
        "Explain expert systems.",
        "What is knowledge representation?",
        "What is an intelligent agent?",
        "Explain search algorithms in AI.",
        "What is reinforcement learning?",
        "What are the applications of AI?",
        "What are the challenges of AI?",
        "Explain the difference between narrow AI and general AI."
    ],

    "Pandas": [
        "What is Pandas?",
        "What is a DataFrame?",
        "What is a Series in Pandas?",
        "How do you handle missing values using Pandas?",
        "Explain groupby() in Pandas.",
        "How do you merge DataFrames?",
        "How do you filter rows in Pandas?",
        "How do you remove duplicate records?",
        "How do you read a CSV file using Pandas?",
        "How do you sort a DataFrame?"
    ],

    "NumPy": [
        "What is NumPy?",
        "What is a NumPy array?",
        "Explain broadcasting in NumPy.",
        "What is vectorization?",
        "How is NumPy different from Python lists?",
        "How do you reshape an array?",
        "Explain NumPy indexing.",
        "How do you perform matrix multiplication?",
        "What are NumPy data types?",
        "Why is NumPy useful for data science?"
    ],

    "Scikit-learn": [
        "What is Scikit-learn?",
        "How do you train a machine learning model using Scikit-learn?",
        "Explain train_test_split().",
        "What is StandardScaler?",
        "How do pipelines work in Scikit-learn?",
        "How do you evaluate a classification model?",
        "How do you perform cross-validation?",
        "What is GridSearchCV?",
        "How do you handle categorical variables?",
        "What are preprocessing techniques in Scikit-learn?"
    ],

    "TensorFlow": [
        "What is TensorFlow?",
        "What is a tensor?",
        "Explain TensorFlow models.",
        "What is Keras?",
        "How do you train a neural network using TensorFlow?",
        "What is an optimizer?",
        "Explain epochs and batch size.",
        "How do you prevent overfitting in TensorFlow?",
        "What is model evaluation?",
        "Explain TensorFlow datasets."
    ],

    "PyTorch": [
        "What is PyTorch?",
        "What is a tensor in PyTorch?",
        "Explain autograd in PyTorch.",
        "What is a PyTorch Dataset?",
        "What is a DataLoader?",
        "How do you define a neural network in PyTorch?",
        "Explain optimizers in PyTorch.",
        "What is GPU acceleration?",
        "How do you save a PyTorch model?",
        "Explain the PyTorch training loop."
    ],

    "AWS": [
        "What is AWS?",
        "What is EC2?",
        "What is S3?",
        "Explain AWS Lambda.",
        "What is IAM?",
        "What is Amazon RDS?",
        "Explain cloud scalability.",
        "What is AWS CloudWatch?",
        "How would you deploy a web application on AWS?",
        "Explain the difference between EC2 and Lambda."
    ],

    "Azure": [
        "What is Microsoft Azure?",
        "What is Azure Virtual Machine?",
        "What is Azure Blob Storage?",
        "Explain Azure Functions.",
        "What is Azure SQL Database?",
        "What is Azure Active Directory?",
        "How would you deploy an application on Azure?",
        "What is Azure DevOps?",
        "Explain cloud computing.",
        "What are the advantages of Azure?"
    ],

    "Docker": [
        "What is Docker?",
        "What is a Docker container?",
        "What is a Docker image?",
        "Explain Dockerfile.",
        "What is Docker Compose?",
        "What is the difference between a container and a virtual machine?",
        "How do you expose ports in Docker?",
        "How do you persist data in Docker?",
        "What are Docker volumes?",
        "How would you containerize a Python application?"
    ],

    "Git": [
        "What is Git?",
        "What is the difference between Git and GitHub?",
        "Explain git clone, pull, and fetch.",
        "What is a Git branch?",
        "Explain merge conflicts.",
        "What is git rebase?",
        "How do you undo a commit?",
        "What is git stash?",
        "Explain Git workflow.",
        "How do you resolve a merge conflict?"
    ],

    "GitHub": [
        "What is GitHub?",
        "What is a GitHub repository?",
        "Explain pull requests.",
        "What are GitHub Actions?",
        "How do you manage branches on GitHub?",
        "What is a fork?",
        "How do you resolve merge conflicts?",
        "What are GitHub Issues?",
        "How do you collaborate using GitHub?",
        "What is CI/CD?"
    ],

    "HTML": [
        "What is HTML?",
        "Explain semantic HTML.",
        "What are HTML forms?",
        "What is the difference between div and span?",
        "Explain HTML5 features.",
        "What are meta tags?",
        "What is accessibility in HTML?",
        "Explain tables in HTML.",
        "What are lists in HTML?",
        "How do HTML forms submit data?"
    ],

    "CSS": [
        "What is CSS?",
        "Explain the CSS box model.",
        "What is Flexbox?",
        "What is CSS Grid?",
        "Explain responsive web design.",
        "What are CSS selectors?",
        "Explain position properties in CSS.",
        "What is the difference between margin and padding?",
        "What are media queries?",
        "How do you center an element using CSS?"
    ],

    "Flask": [
        "What is Flask?",
        "Why is Flask called a microframework?",
        "How do you create routes in Flask?",
        "What are Flask templates?",
        "How do you handle forms in Flask?",
        "How do you connect Flask to a database?",
        "What are Flask extensions?",
        "How do you create REST APIs using Flask?",
        "Explain Flask request and response objects.",
        "How do you deploy a Flask application?"
    ],

    "Django": [
        "What is Django?",
        "Explain Django's MVT architecture.",
        "What are Django models?",
        "What are Django views?",
        "What are Django templates?",
        "Explain Django ORM.",
        "What are Django migrations?",
        "How do you create APIs in Django?",
        "What is Django middleware?",
        "How do you secure a Django application?"
    ],

    "Streamlit": [
        "What is Streamlit?",
        "Why is Streamlit useful for data science applications?",
        "How do you create widgets in Streamlit?",
        "Explain Streamlit session state.",
        "How do you upload files in Streamlit?",
        "How do you display charts in Streamlit?",
        "How do you create multiple pages in Streamlit?",
        "How would you deploy a Streamlit application?",
        "How do you cache data in Streamlit?",
        "How do you handle user input in Streamlit?"
    ],

    "Data Science": [
        "What is data science?",
        "Explain the data science lifecycle.",
        "How do you handle missing data?",
        "What is exploratory data analysis?",
        "What is feature engineering?",
        "Explain data normalization.",
        "What is data visualization?",
        "How do you detect outliers?",
        "How do you evaluate a machine learning model?",
        "Explain the difference between correlation and causation."
    ],

    "Power BI": [
        "What is Power BI?",
        "What are dashboards in Power BI?",
        "What is Power Query?",
        "What is DAX?",
        "Explain calculated columns and measures.",
        "What are Power BI relationships?",
        "How do you create visualizations in Power BI?",
        "What is data modeling?",
        "How do you publish a Power BI report?",
        "How do you optimize a Power BI dashboard?"
    ],

    "Excel": [
        "What are Excel pivot tables?",
        "Explain VLOOKUP and XLOOKUP.",
        "What are Excel formulas?",
        "How do you remove duplicate data in Excel?",
        "What is conditional formatting?",
        "How do you create charts in Excel?",
        "What are Excel functions commonly used for data analysis?",
        "How do you filter and sort data?",
        "What is data validation?",
        "How would you analyze a large dataset in Excel?"
    ],

    "Linux": [
        "What is Linux?",
        "Explain common Linux file commands.",
        "What is the difference between chmod and chown?",
        "Explain Linux file permissions.",
        "What is a process in Linux?",
        "How do you monitor processes?",
        "What is SSH?",
        "Explain grep, awk, and sed.",
        "How do you manage packages in Linux?",
        "What is shell scripting?"
    ],

    "Cybersecurity": [
        "What is cybersecurity?",
        "What is the CIA triad?",
        "Explain authentication and authorization.",
        "What is encryption?",
        "What is a firewall?",
        "Explain common web application vulnerabilities.",
        "What is phishing?",
        "What is penetration testing?",
        "What is vulnerability assessment?",
        "Explain the principle of least privilege."
    ],

    "Networking": [
        "Explain the OSI model.",
        "What is the TCP/IP model?",
        "Explain the difference between TCP and UDP.",
        "What is an IP address?",
        "What is DNS?",
        "What is DHCP?",
        "Explain routers and switches.",
        "What is a subnet?",
        "What is HTTP and HTTPS?",
        "Explain MAC addresses."
    ]
}


# ============================================================
# GENERAL QUESTIONS
# ============================================================

GENERAL_QUESTIONS = [
    "Tell me about yourself.",
    "Why are you interested in this position?",
    "What do you know about this role?",
    "Why should we hire you?",
    "What are your strongest technical skills?",
    "What are your career goals?",
    "How do you keep your technical skills updated?",
    "What type of work environment do you prefer?",
    "What motivates you to learn new technologies?",
    "What are your strengths?"
]


# ============================================================
# BEHAVIORAL QUESTIONS
# ============================================================

BEHAVIORAL_QUESTIONS = [
    "Tell me about a challenging problem you solved.",
    "Describe a situation where you worked as part of a team.",
    "Tell me about a time you had to meet a tight deadline.",
    "Describe a situation where you made a mistake and how you handled it.",
    "Tell me about a time you had a disagreement with a teammate.",
    "How do you handle pressure?",
    "How do you prioritize multiple tasks?",
    "Tell me about a time you learned something quickly.",
    "Describe a situation where you showed leadership.",
    "How do you handle constructive feedback?",
    "Tell me about a time when a project did not go as planned.",
    "How do you communicate technical information to non-technical people?"
]


# ============================================================
# EXPERIENCE QUESTIONS
# ============================================================

EXPERIENCE_QUESTIONS = [
    "Walk me through your previous work or internship experience.",
    "What were your main responsibilities in your previous role?",
    "What was the most important project you worked on?",
    "What technical skills did you use in your previous experience?",
    "What was the biggest challenge you faced during your internship?",
    "What did you learn from your previous experience?",
    "How did you contribute to your previous team?",
    "Which technology did you use most frequently?",
    "Describe a problem you solved during your experience.",
    "What achievement are you most proud of?",
    "How did you measure the success of your work?",
    "What would you do differently in your previous project?"
]


# ============================================================
# PROJECT QUESTIONS
# ============================================================

PROJECT_QUESTIONS = [
    "Explain one of the projects mentioned in your resume.",
    "What problem does your project solve?",
    "Why did you choose the technologies used in your project?",
    "What was your specific contribution to the project?",
    "What was the biggest technical challenge in the project?",
    "How did you test your project?",
    "How did you handle errors in your project?",
    "How would you improve this project in the future?",
    "How would you scale this project for more users?",
    "What database did you use and why?",
    "How did you design the architecture of the project?",
    "How would you deploy this project in production?"
]


# ============================================================
# SKILL GAP QUESTIONS
# ============================================================

SKILL_GAP_QUESTIONS = [
    "Your profile shows limited experience with {skill}. How would you approach learning it?",
    "How would you use {skill} to solve a real-world problem?",
    "What do you currently know about {skill}?",
    "If this role requires {skill}, how would you become productive with it quickly?",
    "What is your understanding of the fundamentals of {skill}?",
    "Can you explain where {skill} would fit into a software project?",
    "How would you evaluate your current proficiency in {skill}?",
    "Have you worked with technologies similar to {skill}?"
]


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {

    "python": "Python",
    "py": "Python",

    "java": "Java",

    "c++": "C++",
    "cpp": "C++",

    "c#": "C#",
    "csharp": "C#",

    "javascript": "JavaScript",
    "js": "JavaScript",

    "typescript": "TypeScript",
    "ts": "TypeScript",

    "react": "React",
    "react.js": "React",

    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",

    "sql": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",

    "mongodb": "MongoDB",
    "mongo": "MongoDB",

    "machine learning": "Machine Learning",
    "machine-learning": "Machine Learning",
    "ml": "Machine Learning",

    "deep learning": "Deep Learning",
    "deep-learning": "Deep Learning",
    "dl": "Deep Learning",

    "natural language processing": "NLP",
    "nlp": "NLP",

    "artificial intelligence": "AI",
    "ai": "AI",

    "pandas": "Pandas",
    "numpy": "NumPy",

    "scikit-learn": "Scikit-learn",
    "sklearn": "Scikit-learn",

    "tensorflow": "TensorFlow",
    "pytorch": "PyTorch",

    "aws": "AWS",
    "amazon web services": "AWS",

    "azure": "Azure",
    "microsoft azure": "Azure",

    "docker": "Docker",

    "git": "Git",
    "github": "GitHub",

    "html": "HTML",
    "html5": "HTML",

    "css": "CSS",
    "css3": "CSS",

    "flask": "Flask",
    "django": "Django",

    "streamlit": "Streamlit",

    "data science": "Data Science",
    "datascience": "Data Science",

    "power bi": "Power BI",
    "powerbi": "Power BI",

    "excel": "Excel",

    "linux": "Linux",

    "cybersecurity": "Cybersecurity",
    "cyber security": "Cybersecurity",

    "networking": "Networking"
}


# ============================================================
# NORMALIZATION
# ============================================================

def normalize_text(value):
    """
    Convert any value to clean lowercase text.
    """

    if value is None:
        return ""

    if isinstance(value, (list, tuple, set)):
        return " ".join(
            str(x) for x in value
            if x is not None
        ).lower()

    if isinstance(value, dict):
        return " ".join(
            str(v)
            for v in value.values()
            if v is not None
        ).lower()

    return str(value).lower()


# ============================================================
# CONVERT VALUE TO LIST
# ============================================================

def to_list(value):
    """
    Convert strings, lists, tuples, sets, or dictionaries
    into a simple list of strings.
    """

    if value is None:
        return []

    if isinstance(value, dict):
        value = list(value.values())

    if isinstance(value, (list, tuple, set)):
        result = []

        for item in value:

            if item is None:
                continue

            text = str(item).strip()

            if text:
                result.append(text)

        return result

    text = str(value).strip()

    if not text:
        return []

    parts = re.split(
        r"[,;\n|]+",
        text
    )

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


# ============================================================
# CANONICAL SKILL NAME
# ============================================================

def canonical_skill(skill):
    """
    Convert a skill into the standard skill name.
    """

    if not skill:
        return None

    text = str(skill).strip()

    key = text.lower()

    if key in SKILL_ALIASES:
        return SKILL_ALIASES[key]

    for known_skill in TECHNICAL_QUESTIONS.keys():

        if key == known_skill.lower():
            return known_skill

    return text


# ============================================================
# EXTRACT SKILLS FROM TEXT
# ============================================================

def extract_skills_from_text(text):
    """
    Find known technical skills inside resume/JD text.
    """

    if not text:
        return []

    text = normalize_text(text)

    found = []

    # Check aliases first
    for alias, standard_name in SKILL_ALIASES.items():

        pattern = r"(?<![a-zA-Z0-9])" + re.escape(alias) + r"(?![a-zA-Z0-9])"

        if re.search(pattern, text):

            if standard_name not in found:
                found.append(standard_name)

    # Check technical bank
    for skill in TECHNICAL_QUESTIONS.keys():

        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill.lower()) + r"(?![a-zA-Z0-9])"

        if re.search(pattern, text):

            if skill not in found:
                found.append(skill)

    return found


# ============================================================
# EXTRACT SKILLS FROM CANDIDATE
# ============================================================

def extract_candidate_skills(candidate):
    """
    Extract skills from different possible candidate
    dictionary formats.
    """

    if not isinstance(candidate, dict):
        return []

    possible_fields = [
        "skills",
        "technical_skills",
        "skill_set",
        "technologies",
        "technology",
        "keywords"
    ]

    skills = []

    for field in possible_fields:

        value = candidate.get(field)

        for item in to_list(value):

            skill = canonical_skill(item)

            if skill and skill not in skills:
                skills.append(skill)

    # Also search complete candidate object
    candidate_text = normalize_text(candidate)

    detected = extract_skills_from_text(
        candidate_text
    )

    for skill in detected:

        if skill not in skills:
            skills.append(skill)

    return skills


# ============================================================
# EXTRACT JOB SKILLS
# ============================================================

def extract_job_skills(job):
    """
    Extract required skills from job description.
    """

    if not isinstance(job, dict):
        return []

    skills = []

    possible_fields = [
        "required_skills",
        "skills",
        "technical_skills",
        "requiredSkills",
        "technologies",
        "keywords"
    ]

    for field in possible_fields:

        value = job.get(field)

        for item in to_list(value):

            skill = canonical_skill(item)

            if skill and skill not in skills:
                skills.append(skill)

    # Search complete job description
    job_text = normalize_text(job)

    detected = extract_skills_from_text(
        job_text
    )

    for skill in detected:

        if skill not in skills:
            skills.append(skill)

    return skills


# ============================================================
# GET FIELD FROM DICTIONARY
# ============================================================

def get_first_field(data, fields, default=None):

    if not isinstance(data, dict):
        return default

    for field in fields:

        value = data.get(field)

        if value is None:
            continue

        if isinstance(value, str) and not value.strip():
            continue

        return value

    return default


# ============================================================
# QUESTIONS FOR SKILL
# ============================================================

def questions_for_skill(skill):

    standard_skill = canonical_skill(skill)

    if not standard_skill:
        return []

    return list(
        TECHNICAL_QUESTIONS.get(
            standard_skill,
            []
        )
    )


# ============================================================
# QUESTION TYPE NORMALIZATION
# ============================================================

def normalize_question_type(question_type):

    if not question_type:
        return "Mixed"

    value = str(question_type).strip().lower()

    mapping = {

        "technical": "Technical",
        "tech": "Technical",

        "behavioral": "Behavioral",
        "behavioural": "Behavioral",
        "behavior": "Behavioral",

        "project": "Project",
        "projects": "Project",

        "experience": "Experience",
        "experiences": "Experience",

        "skill gap": "Skill Gap",
        "skillgap": "Skill Gap",
        "gap": "Skill Gap",

        "general": "General",

        "mixed": "Mixed",
        "all": "Mixed"
    }

    return mapping.get(
        value,
        "Mixed"
    )


# ============================================================
# CREATE QUESTION DICTIONARY
# ============================================================

def make_question(
    question,
    category="General",
    skill="",
    difficulty="Medium"
):

    return {
        "question": str(question),
        "category": category,
        "skill": skill,
        "difficulty": difficulty
    }


# ============================================================
# DIFFICULTY
# ============================================================

def get_difficulty(index):

    if index % 5 == 0:
        return "Hard"

    if index % 3 == 0:
        return "Easy"

    return "Medium"


# ============================================================
# GENERATE SKILL GAP QUESTIONS
# ============================================================

def generate_skill_gap_questions(
    candidate,
    job=None,
    number_of_questions=5
):

    candidate_skills = set(
        canonical_skill(skill)
        for skill in extract_candidate_skills(candidate)
    )

    required_skills = set(
        canonical_skill(skill)
        for skill in extract_job_skills(job)
    ) if job else set()

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in candidate_skills
    ]

    questions = []

    if not missing_skills:

        fallback = [
            "Which technical skill would you like to improve next?",
            "Which technology in this job description would you like to learn more deeply?",
            "How do you plan to improve your technical skills?",
            "Which area of your technical knowledge needs further development?",
            "How would you learn a new technology required for a project?"
        ]

        for i, question in enumerate(
            fallback[:number_of_questions]
        ):

            questions.append(
                make_question(
                    question,
                    "Skill Gap",
                    "",
                    get_difficulty(i + 1)
                )
            )

        return questions

    while len(questions) < number_of_questions:

        for skill in missing_skills:

            templates = SKILL_GAP_QUESTIONS

            template = templates[
                len(questions) % len(templates)
            ]

            question = template.format(
                skill=skill
            )

            questions.append(
                make_question(
                    question,
                    "Skill Gap",
                    skill,
                    get_difficulty(
                        len(questions) + 1
                    )
                )
            )

            if len(questions) >= number_of_questions:
                break

    return questions


# ============================================================
# GENERATE PROJECT QUESTIONS
# ============================================================

def generate_project_questions(
    candidate,
    number_of_questions=5
):

    projects = get_first_field(
        candidate,
        [
            "projects",
            "project",
            "project_details"
        ],
        ""
    )

    questions = []

    candidate_text = normalize_text(
        projects
    )

    project_skills = extract_skills_from_text(
        candidate_text
    )

    # Project-specific skill questions
    for skill in project_skills:

        if len(questions) >= number_of_questions:
            break

        questions.append(
            make_question(
                f"How did you use {skill} in your project?",
                "Project",
                skill,
                "Medium"
            )
        )

    # General project questions
    index = 0

    while len(questions) < number_of_questions:

        question = PROJECT_QUESTIONS[
            index % len(PROJECT_QUESTIONS)
        ]

        questions.append(
            make_question(
                question,
                "Project",
                "",
                get_difficulty(
                    len(questions) + 1
                )
            )
        )

        index += 1

    return questions


# ============================================================
# GENERATE TECHNICAL QUESTIONS
# ============================================================

def generate_technical_questions(
    candidate,
    job=None,
    number_of_questions=5
):

    candidate_skills = extract_candidate_skills(
        candidate
    )

    job_skills = extract_job_skills(
        job
    ) if job else []

    # Candidate + job matching skills
    combined_skills = []

    for skill in candidate_skills + job_skills:

        standard_skill = canonical_skill(
            skill
        )

        if (
            standard_skill
            and standard_skill not in combined_skills
            and standard_skill in TECHNICAL_QUESTIONS
        ):
            combined_skills.append(
                standard_skill
            )

    questions = []

    # First use candidate skills
    for skill in combined_skills:

        skill_questions = questions_for_skill(
            skill
        )

        for question in skill_questions:

            questions.append(
                make_question(
                    question,
                    "Technical",
                    skill,
                    get_difficulty(
                        len(questions) + 1
                    )
                )
            )

            if len(questions) >= number_of_questions:
                return questions

    # Fallback technical questions
    if len(questions) < number_of_questions:

        fallback_skills = list(
            TECHNICAL_QUESTIONS.keys()
        )

        for skill in fallback_skills:

            for question in TECHNICAL_QUESTIONS[
                skill
            ]:

                if len(questions) >= number_of_questions:
                    break

                questions.append(
                    make_question(
                        question,
                        "Technical",
                        skill,
                        get_difficulty(
                            len(questions) + 1
                        )
                    )
                )

            if len(questions) >= number_of_questions:
                break

    return questions[:number_of_questions]


# ============================================================
# GENERATE BEHAVIORAL QUESTIONS
# ============================================================

def generate_behavioral_questions(
    number_of_questions=5
):

    questions = []

    for i in range(
        number_of_questions
    ):

        question = BEHAVIORAL_QUESTIONS[
            i % len(BEHAVIORAL_QUESTIONS)
        ]

        questions.append(
            make_question(
                question,
                "Behavioral",
                "",
                get_difficulty(i + 1)
            )
        )

    return questions


# ============================================================
# GENERATE EXPERIENCE QUESTIONS
# ============================================================

def generate_experience_questions(
    number_of_questions=5
):

    questions = []

    for i in range(
        number_of_questions
    ):

        question = EXPERIENCE_QUESTIONS[
            i % len(EXPERIENCE_QUESTIONS)
        ]

        questions.append(
            make_question(
                question,
                "Experience",
                "",
                get_difficulty(i + 1)
            )
        )

    return questions


# ============================================================
# GENERATE GENERAL QUESTIONS
# ============================================================

def generate_general_questions(
    number_of_questions=5
):

    questions = []

    for i in range(
        number_of_questions
    ):

        question = GENERAL_QUESTIONS[
            i % len(GENERAL_QUESTIONS)
        ]

        questions.append(
            make_question(
                question,
                "General",
                "",
                get_difficulty(i + 1)
            )
        )

    return questions


# ============================================================
# GENERATE MIXED QUESTIONS
# ============================================================

def generate_mixed_questions(
    candidate,
    job=None,
    number_of_questions=15
):

    questions = []

    # --------------------------------------------------------
    # TECHNICAL
    # --------------------------------------------------------

    technical_count = max(
        1,
        round(number_of_questions * 0.40)
    )

    technical = generate_technical_questions(
        candidate,
        job,
        technical_count
    )

    questions.extend(
        technical
    )

    # --------------------------------------------------------
    # BEHAVIORAL
    # --------------------------------------------------------

    behavioral_count = max(
        1,
        round(number_of_questions * 0.20)
    )

    behavioral = generate_behavioral_questions(
        behavioral_count
    )

    questions.extend(
        behavioral
    )

    # --------------------------------------------------------
    # PROJECT
    # --------------------------------------------------------

    project_count = max(
        1,
        round(number_of_questions * 0.20)
    )

    project = generate_project_questions(
        candidate,
        project_count
    )

    questions.extend(
        project
    )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    experience_count = max(
        1,
        round(number_of_questions * 0.10)
    )

    experience = generate_experience_questions(
        experience_count
    )

    questions.extend(
        experience
    )

    # --------------------------------------------------------
    # SKILL GAP
    # --------------------------------------------------------

    skill_gap_count = max(
        1,
        number_of_questions
        - len(questions)
    )

    skill_gap = generate_skill_gap_questions(
        candidate,
        job,
        skill_gap_count
    )

    questions.extend(
        skill_gap
    )

    # --------------------------------------------------------
    # IF TOO MANY
    # --------------------------------------------------------

    questions = questions[
        :number_of_questions
    ]

    # --------------------------------------------------------
    # IF TOO FEW
    # --------------------------------------------------------

    if len(questions) < number_of_questions:

        remaining = (
            number_of_questions
            - len(questions)
        )

        extra = generate_general_questions(
            remaining
        )

        questions.extend(
            extra
        )

    return questions[
        :number_of_questions
    ]


# ============================================================
# MAIN INTERVIEW GENERATOR
# ============================================================

def generate_interview_questions(
    candidate,
    job=None,
    number_of_questions=15,
    question_type="Mixed",
    **kwargs
):

    # --------------------------------------------------------
    # SAFETY
    # --------------------------------------------------------

    try:
        number_of_questions = int(
            number_of_questions
        )
    except Exception:
        number_of_questions = 15

    if number_of_questions < 1:
        number_of_questions = 1

    if number_of_questions > 100:
        number_of_questions = 100

    question_type = normalize_question_type(
        question_type
    )

    # --------------------------------------------------------
    # TECHNICAL
    # --------------------------------------------------------

    if question_type == "Technical":

        questions = generate_technical_questions(
            candidate,
            job,
            number_of_questions
        )

    # --------------------------------------------------------
    # BEHAVIORAL
    # --------------------------------------------------------

    elif question_type == "Behavioral":

        questions = generate_behavioral_questions(
            number_of_questions
        )

    # --------------------------------------------------------
    # PROJECT
    # --------------------------------------------------------

    elif question_type == "Project":

        questions = generate_project_questions(
            candidate,
            number_of_questions
        )

    # --------------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------------

    elif question_type == "Experience":

        questions = generate_experience_questions(
            number_of_questions
        )

    # --------------------------------------------------------
    # SKILL GAP
    # --------------------------------------------------------

    elif question_type == "Skill Gap":

        questions = generate_skill_gap_questions(
            candidate,
            job,
            number_of_questions
        )

    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    elif question_type == "General":

        questions = generate_general_questions(
            number_of_questions
        )

    # --------------------------------------------------------
    # MIXED
    # --------------------------------------------------------

    else:

        questions = generate_mixed_questions(
            candidate,
            job,
            number_of_questions
        )

    # --------------------------------------------------------
    # FINAL SAFETY LIMIT
    # --------------------------------------------------------

    questions = list(
        questions
    )[:number_of_questions]

    return questions


# ============================================================
# STRING-ONLY API
# ============================================================

def generate_questions(
    candidate,
    job=None,
    number_of_questions=15,
    question_type="Mixed"
):

    structured_questions = generate_interview_questions(
        candidate=candidate,
        job=job,
        number_of_questions=number_of_questions,
        question_type=question_type
    )

    return [
        item["question"]
        if isinstance(item, dict)
        else str(item)
        for item in structured_questions
    ]


# ============================================================
# INTERVIEW SUMMARY
# ============================================================

def generate_interview_summary(
    candidate,
    job=None
):

    candidate_name = get_first_field(
        candidate,
        [
            "name",
            "candidate_name",
            "full_name"
        ],
        "Unknown Candidate"
    )

    job_title = get_first_field(
        job,
        [
            "title",
            "job_title",
            "position"
        ],
        "Selected Job"
    )

    candidate_skills = extract_candidate_skills(
        candidate
    )

    required_skills = extract_job_skills(
        job
    ) if job else []

    missing_skills = [
        skill
        for skill in required_skills
        if skill not in candidate_skills
    ]

    return {
        "candidate": candidate_name,
        "job": job_title,
        "candidate_skills": candidate_skills,
        "required_skills": required_skills,
        "skill_gaps": missing_skills,
        "candidate_skill_count": len(
            candidate_skills
        ),
        "required_skill_count": len(
            required_skills
        ),
        "skill_gap_count": len(
            missing_skills
        )
    }


# ============================================================
# BACKWARD COMPATIBILITY FUNCTIONS
# ============================================================

def create_interview_questions(
    candidate,
    job=None,
    number_of_questions=15,
    question_type="Mixed",
    **kwargs
):

    return generate_interview_questions(
        candidate=candidate,
        job=job,
        number_of_questions=number_of_questions,
        question_type=question_type,
        **kwargs
    )


def get_interview_questions(
    candidate,
    job=None,
    number_of_questions=15,
    question_type="Mixed",
    **kwargs
):

    return generate_interview_questions(
        candidate=candidate,
        job=job,
        number_of_questions=number_of_questions,
        question_type=question_type,
        **kwargs
    )


def generate_candidate_interview(
    candidate,
    job=None,
    number_of_questions=15,
    question_type="Mixed",
    **kwargs
):

    return generate_interview_questions(
        candidate=candidate,
        job=job,
        number_of_questions=number_of_questions,
        question_type=question_type,
        **kwargs
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    test_candidate = {

        "name": "Test Candidate",

        "email": "test@example.com",

        "skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Pandas",
            "Streamlit"
        ],

        "projects": [
            "AI Smart Hiring Platform"
        ],

        "experience": [
            "Machine Learning Intern"
        ]
    }

    test_job = {

        "title": "AI / Data Science Developer",

        "description": """
        We are looking for a Data Science Developer
        with Python, SQL, Machine Learning, Pandas,
        Streamlit, Docker and AWS skills.
        """,

        "required_skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Pandas",
            "Streamlit",
            "Docker",
            "AWS"
        ]
    }

    print("\n" + "=" * 60)
    print("AI SMART HIRING - INTERVIEW GENERATOR TEST")
    print("=" * 60)

    print("\n--- TECHNICAL ---")

    technical_questions = generate_interview_questions(
        test_candidate,
        test_job,
        5,
        "Technical"
    )

    for i, question in enumerate(
        technical_questions,
        1
    ):

        print(
            f"{i}. {question['question']}"
        )

    print("\n--- MIXED ---")

    mixed_questions = generate_interview_questions(
        test_candidate,
        test_job,
        10,
        "Mixed"
    )

    for i, question in enumerate(
        mixed_questions,
        1
    ):

        print(
            f"{i}. {question['question']}"
        )

    print("\n--- SKILL GAP ---")

    gap_questions = generate_interview_questions(
        test_candidate,
        test_job,
        5,
        "Skill Gap"
    )

    for i, question in enumerate(
        gap_questions,
        1
    ):

        print(
            f"{i}. {question['question']}"
        )

    print("\n" + "=" * 60)
    print("TEST COMPLETED")
    print("=" * 60)