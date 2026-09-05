
import os
import re
import tempfile

from pypdf import PdfReader
import fitz
from PIL import Image
import pytesseract


# --------------------------------------------------
# WINDOWS TESSERACT CONFIGURATION
# --------------------------------------------------

# TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# if os.path.exists(TESSERACT_PATH):
#     pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
# --------------------------------------------------
# TESSERACT CONFIGURATION
# --------------------------------------------------

# Windows path for local development
WINDOWS_TESSERACT_PATH = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# If running on Windows and Tesseract exists there,
# use the Windows executable.
#
# In Docker/Linux, Tesseract is installed system-wide
# and does not need an explicit path.

if os.path.exists(WINDOWS_TESSERACT_PATH):

    pytesseract.pytesseract.tesseract_cmd = (
        WINDOWS_TESSERACT_PATH
    )


# --------------------------------------------------
# CHECK WHETHER NORMAL PDF TEXT IS USEFUL
# --------------------------------------------------

def is_text_useful(text):

    if not text:
        return False

    text = text.strip()

    # If almost no text was extracted,
    # it is probably a scanned/image PDF.
    if len(text) < 100:
        return False

    # Count actual letters
    letters = sum(char.isalpha() for char in text)

    # Too few letters usually means bad extraction
    if letters < 30:
        return False

    return True


# --------------------------------------------------
# NORMAL TEXT EXTRACTION
# --------------------------------------------------

def extract_normal_text(pdf_path):

    extracted_text = []

    try:

        reader = PdfReader(pdf_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                extracted_text.append(page_text)

    except Exception as e:

        print("Normal PDF extraction error:")
        print(e)

        return ""

    return "\n".join(extracted_text)


# --------------------------------------------------
# OCR EXTRACTION FOR SCANNED PDFs
# --------------------------------------------------

def extract_ocr_text(pdf_path):

    extracted_text = []

    try:

        pdf_document = fitz.open(pdf_path)

        print("Using OCR fallback...")

        for page_number in range(len(pdf_document)):

            page = pdf_document[page_number]

            # Render PDF page as image
            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2)
            )

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            # OCR the image
            page_text = pytesseract.image_to_string(
                image,
                config="--psm 6"
            )

            if page_text:
                extracted_text.append(page_text)

        pdf_document.close()

    except Exception as e:

        print("OCR extraction error:")
        print(e)

        return ""

    return "\n".join(extracted_text)


# --------------------------------------------------
# CLEAN EXTRACTED TEXT
# --------------------------------------------------

def clean_text(text):

    if not text:
        return ""

    # Remove repeated spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive empty lines
    text = re.sub(r"\n\s*\n+", "\n", text)

    # Remove spaces at beginning/end
    text = text.strip()

    return text


# --------------------------------------------------
# CREATE STRUCTURED CHUNKS
# --------------------------------------------------

def create_chunks(text, chunk_size=500, overlap=100):

    if not text:
        return []

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(
            start + chunk_size,
            text_length
        )

        chunk = text[start:end]

        # Try to avoid cutting in the middle of a line
        if end < text_length:

            last_newline = chunk.rfind("\n")

            if last_newline > chunk_size // 2:
                end = start + last_newline
                chunk = text[start:end]

        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)

        # Stop if we reached the end
        if end >= text_length:
            break

        # Move forward with overlap
        start = end - overlap

    return chunks


# --------------------------------------------------
# MAIN FUNCTION USED BY THE PROJECT
# --------------------------------------------------

def process_pdf(uploaded_file):

    # Create temporary PDF file
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(
            uploaded_file.getvalue()
        )

        temp_pdf_path = temp_file.name


    try:

        print("\n===================================")
        print("STARTING PDF PROCESSING")
        print("===================================\n")


        # --------------------------------
        # STEP 1: NORMAL TEXT EXTRACTION
        # --------------------------------

        normal_text = extract_normal_text(
            temp_pdf_path
        )

        normal_text = clean_text(
            normal_text
        )


        # --------------------------------
        # STEP 2: DECIDE EXTRACTION METHOD
        # --------------------------------

        if is_text_useful(normal_text):

            print("Normal text extraction successful.")

            final_text = normal_text

            extraction_method = "NORMAL TEXT EXTRACTION"


        else:

            print(
                "Normal extraction not sufficient."
            )

            print(
                "Switching to OCR fallback..."
            )

            ocr_text = extract_ocr_text(
                temp_pdf_path
            )

            ocr_text = clean_text(
                ocr_text
            )

            final_text = ocr_text

            extraction_method = "OCR"


        # --------------------------------
        # STEP 3: VALIDATE EXTRACTION
        # --------------------------------

        if not is_text_useful(final_text):

            print(
                "WARNING: No useful text could be extracted."
            )

            return []


        # --------------------------------
        # STEP 4: CREATE CHUNKS
        # --------------------------------

        chunks = create_chunks(
            final_text,
            chunk_size=500,
            overlap=100
        )


        # --------------------------------
        # DEBUG INFORMATION
        # --------------------------------

        print("\n===================================")
        print("PDF PROCESSING COMPLETE")
        print("===================================")

        print(
            f"Extraction method: "
            f"{extraction_method}"
        )

        print(
            f"Total characters extracted: "
            f"{len(final_text)}"
        )

        print(
            f"Total chunks created: "
            f"{len(chunks)}"
        )


        print("\n--- EXTRACTED TEXT ---\n")

        print(final_text)


        print("\n--- CHUNKS ---\n")

        for index, chunk in enumerate(chunks):

            print(
                f"\nCHUNK {index + 1}:"
            )

            print(chunk)


        return chunks


    finally:

        # Delete temporary PDF
        if os.path.exists(temp_pdf_path):

            os.remove(
                temp_pdf_path
            )


