import os
import re

def clean_extracted_text(text):
    if not text:
        return ""
    text=text.replace("\r\n","\n")
    text=text.replace("\r","\n")
    text=re.sub(r"([A-Za-z]{2,})-\s*\n\s*([a-z]{2,})",r"\1\2",text)
    text=re.sub(r"([A-Za-z]{2,})\s*\n\s*([a-z]{2,})",r"\1 \2",text)
    text=text.replace("\t"," ")
    text=re.sub(r"(?<=[a-z])(?=[A-Z])"," ",text)
    text=re.sub(r"\s+([,.;:])",r"\1",text)
    text=re.sub(r"[ ]{2,}"," ",text)
    text=re.sub(r" *\n *","\n",text)
    text=re.sub(r"\n{3,}","\n\n",text)
    return text.strip()

def extract_from_pdf(file_path):
    try:
        import pymupdf
        document=pymupdf.open(file_path)
    except ImportError:
        try:
            import fitz
            document=fitz.open(file_path)
        except ImportError:
            raise ImportError("PyMuPDF is not installed. Run: pip install PyMuPDF")
    pages=[]
    for page in document:
        try:
            page_text=page.get_text()
            if page_text:
                pages.append(page_text)
        except Exception:
            continue
    document.close()
    text="\n".join(pages)
    return clean_extracted_text(text)

def extract_from_docx(file_path):
    try:
        from docx import Document
    except ImportError:
        raise ImportError("python-docx is not installed. Run: pip install python-docx")
    document=Document(file_path)
    paragraphs=[]
    for paragraph in document.paragraphs:
        text=paragraph.text.strip()
        if text:
            paragraphs.append(text)
    return clean_extracted_text("\n".join(paragraphs))

def extract_from_txt(file_path):
    with open(file_path,"r",encoding="utf-8",errors="ignore") as file:
        text=file.read()
    return clean_extracted_text(text)

def extract_resume_text(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Resume not found: {file_path}")
    extension=os.path.splitext(file_path)[1].lower()
    print("\nReading resume...")
    if extension==".pdf":
        print("Reading PDF resume...")
        return extract_from_pdf(file_path)
    elif extension==".docx":
        print("Reading DOCX resume...")
        return extract_from_docx(file_path)
    elif extension==".txt":
        print("Reading TXT resume...")
        return extract_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported resume format: {extension}")

def extract_text_from_pdf(file_path):
    return extract_from_pdf(file_path)

def extract_text_from_docx(file_path):
    return extract_from_docx(file_path)

def extract_text_from_txt(file_path):
    return extract_from_txt(file_path)