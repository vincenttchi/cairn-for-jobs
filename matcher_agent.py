from dotenv import load_dotenv
import os

def is_bulleted(paragraph):
    """Check whether a docx paragraph has bullet or numbered-list formatting.
    Check happens within raw XML properties to check if the paragraph has
    numbering properties which indicates it is a bullet/numbered list.

    Args:
        paragraph (docx.text.paragraph.Paragraph): A paragraph from a
            python-docx Document.

    Returns:
        bool: True if the paragraph has numbering/bullet formatting applied.
    """
    pPr = paragraph._p.pPr
    return pPr is not None and pPr.numPr is not None

def load_resume(path):
    """
    Extract plaintext from a resume file.
    
    Args:
        path (str): Path to the resume file. Currently supports .pdf and .docx.

    Returns:
        str: The extracted resume text.

    Raises:
        ValueError: If the file extension is not .pdf or .docx.
    """
    if path.endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif path.endswith(".docx"):
        from docx import Document
        doc = Document(path)
        lines = []

        # Adding dash (-) to beginning of paragraphs that are bullet points
        for p in doc.paragraphs:
            if is_bulleted(p):
                lines.append(f"- {p.text}")
            else:
                lines.append(p.text)
        return "\n".join(lines)
    else:
        raise ValueError(f"Unsupported file type: {path}")

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
print("Key loaded" if key else "Key missing; check your .env")

path = "inputs/resume.docx"
resume_text = load_resume(path)
print(resume_text)
