import PyPDF2
import docx


def extract_text_from_pdf(file_path):
    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        text = f"Error reading PDF: {str(e)}"

    return text


def extract_text_from_docx(file_path):
    text = ""

    try:
        doc = docx.Document(file_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

    except Exception as e:
        text = f"Error reading DOCX: {str(e)}"

    return text


def extract_resume_text(file_path):

    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)

    else:
        return "Unsupported file format"