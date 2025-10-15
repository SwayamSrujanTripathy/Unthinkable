import fitz  # PyMuPDF
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts text from a given PDF file stream.
    """
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_txt(txt_file) -> str:
    """
    Extracts text from a given TXT file stream.
    """
    return txt_file.read().decode("utf-8")

def get_text_chunks(text: str) -> List[str]:
    """
    Splits a long text into smaller chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks
