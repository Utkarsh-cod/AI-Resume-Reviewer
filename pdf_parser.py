import fitz  # PyMuPDF library

def parse_pdf_text(file_bytes):
    """
    Extracts all text from the bytes of an uploaded PDF file.

    Args:
        file_bytes: The raw bytes of the PDF file from st.file_uploader.

    Returns:
        A string containing all the text from the PDF, or None if an error occurs.
    """
    try:
        # Open the PDF directly from the in-memory bytes
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        # Initialize an empty string to hold the text
        full_text = ""
        # Loop through each page and extract its text
        for page in pdf_document:
            full_text += page.get_text()
        return full_text
    except Exception as e:
        # If anything goes wrong, we return None and print an error
        print(f"Error parsing PDF: {e}")
        return None

