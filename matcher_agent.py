import os
from dotenv import load_dotenv
from openai import OpenAI
import openai
from prompts import MATCHER_SYSTEM_PROMPT


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


def load_post(path):
    """Load job posting text from a plain text file.

    Args:
        path (str): Path to the job posting text file.

    Returns:
        str: The job posting text.

    Raises:
        FileNotFoundError: If the file doesn't exist at the given path.
        ValueError: If the file is empty or contains only whitespace.
    """
    with open(path) as f:
        posting_text = f.read().strip()
        if len(posting_text) == 0:
            raise ValueError(f"No job description passed in: {path}")
        return posting_text


def get_completion(system_prompt, user_message, model="gpt-4o-mini"):
    """Send a system prompt and user message to the LLM, return the response text.

    Args:
        system_prompt (str): The system-level instructions for the model.
        user_message (str): The user-role content (resume + posting, combined).
        model (str): Which model to call.

    Returns:
        str: The model's response text.
    """
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content


def main():
    load_dotenv()
    key = os.getenv("OPENAI_API_KEY")
    print("Key loaded" if key else "Key missing; check your .env")

    resume_path = "inputs/resume.docx"
    resume_text = load_resume(resume_path)

    post_path = "inputs/posting.txt"
    post_text = load_post(post_path)

    user_message = f"""Resume:\n{resume_text}\n\nJob Posting:\n{post_text}"""
    try:
        assessment = get_completion(MATCHER_SYSTEM_PROMPT, user_message, "gpt-4o")
        print(assessment)
    except openai.AuthenticationError as e:
        print("Authentication failed; check that your API key is correct:", e)
    except openai.RateLimitError as e:
        print("Rate limit or credits depleted; check your credits:", e)
    except openai.APIConnectionError as e:
        print("Could not reach OpenAI's servers; check your internet connection:", e)
    except openai.APIStatusError as e:
        print(f"OpenAI API returned an error (status {e.status_code}):", e)


if __name__ == "__main__":
    main()
