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

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

if os.path.exists(TESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


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


# from pypdf import PdfReader

# import re


# # =========================================================
# # FUNCTION 1: CLEAN TEXT
# # =========================================================

# def clean_text(text):
#     """
#     Cleans extracted PDF text.

#     Removes:
#     - extra spaces
#     - repeated line breaks
#     - unnecessary whitespace
#     """

#     # Replace multiple spaces/newlines/tabs with one space
#     text = re.sub(r"\s+", " ", text)

#     # Remove spaces from beginning and end
#     text = text.strip()

#     return text


# # =========================================================
# # FUNCTION 2: CHECK TEXT QUALITY
# # =========================================================

# def is_text_useful(text, minimum_length=30):
#     """
#     Checks whether extracted text is useful.

#     OCR fallback may be needed if:
#     - text is None
#     - text is too short
#     - text contains almost no letters
#     """

#     if not text:
#         return False

#     text = text.strip()

#     # Very small text usually means extraction failed
#     if len(text) < minimum_length:
#         return False

#     # Count alphabetic characters
#     letters = sum(character.isalpha() for character in text)

#     # If there are too few letters,
#     # the extracted content may not be meaningful
#     if letters < 10:
#         return False

#     return True


# # =========================================================
# # FUNCTION 3: OCR FALLBACK
# # =========================================================

# def extract_text_with_ocr(pdf_file):
#     """
#     Extracts text from a PDF using OCR.

#     This function is used mainly for scanned PDFs
#     or pages where normal text extraction fails.
#     """

#     try:
#         import fitz
#         import pytesseract
#         from PIL import Image
#         import io

#         # Open PDF using PyMuPDF
#         pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")

#         ocr_pages = []

#         for page_number, page in enumerate(pdf_document):

#             # Convert PDF page into an image
#             pixmap = page.get_pixmap(dpi=200)

#             # Convert pixmap into image bytes
#             image_bytes = pixmap.tobytes("png")

#             # Create PIL image
#             image = Image.open(io.BytesIO(image_bytes))

#             # OCR: Extract text from image
#             page_text = pytesseract.image_to_string(image)

#             # Clean extracted OCR text
#             page_text = clean_text(page_text)

#             # Store text with page number
#             ocr_pages.append(
#                 {
#                     "page": page_number + 1,
#                     "text": page_text
#                 }
#             )

#         # Close PDF
#         pdf_document.close()

#         return ocr_pages

#     except Exception as error:

#         print("OCR extraction failed:")
#         print(error)

#         return []


# # =========================================================
# # FUNCTION 4: CREATE STRUCTURED CHUNKS
# # =========================================================

# def create_chunks(page_data, chunk_size=500, overlap=50):
#     """
#     Creates chunks while keeping page metadata.

#     Each chunk is stored like:

#     {
#         "text": "chunk content",
#         "page": 1
#     }

#     overlap helps preserve context between chunks.
#     """

#     chunks = []

#     for page in page_data:

#         page_number = page["page"]
#         text = page["text"]

#         # Skip empty pages
#         if not text:
#             continue

#         # Split text into sentences
#         sentences = re.split(
#             r"(?<=[.!?])\s+",
#             text
#         )

#         current_chunk = ""

#         for sentence in sentences:

#             # If sentence itself is empty, skip it
#             if not sentence.strip():
#                 continue

#             # Check if sentence can fit in current chunk
#             if len(current_chunk) + len(sentence) <= chunk_size:

#                 current_chunk += " " + sentence

#             else:

#                 # Save the current chunk
#                 if current_chunk.strip():

#                     chunks.append(
#                         {
#                             "text": current_chunk.strip(),
#                             "page": page_number
#                         }
#                     )

#                 # Create overlap from previous chunk
#                 overlap_text = current_chunk[-overlap:]

#                 # Start new chunk
#                 current_chunk = (
#                     overlap_text + " " + sentence
#                 )

#         # Save remaining chunk
#         if current_chunk.strip():

#             chunks.append(
#                 {
#                     "text": current_chunk.strip(),
#                     "page": page_number
#                 }
#             )

#     return chunks


# # =========================================================
# # MAIN FUNCTION: PROCESS PDF
# # =========================================================

# def process_pdf(pdf_file):

#     print("\n========================================")
#     print("STARTING PDF PROCESSING")
#     print("========================================")

#     # Read PDF normally using PyPDF
#     reader = PdfReader(pdf_file)

#     page_data = []

#     pages_needing_ocr = 0

#     # -----------------------------------------------------
#     # STEP 1: TRY NORMAL TEXT EXTRACTION
#     # -----------------------------------------------------

#     for page_number, page in enumerate(reader.pages):

#         extracted_text = page.extract_text()

#         # Clean the extracted text
#         if extracted_text:
#             extracted_text = clean_text(
#                 extracted_text
#             )

#         # Check whether extraction was useful
#         if is_text_useful(extracted_text):

#             print(
#                 f"Page {page_number + 1}: "
#                 "Normal text extraction successful"
#             )

#             page_data.append(
#                 {
#                     "page": page_number + 1,
#                     "text": extracted_text
#                 }
#             )

#         else:

#             print(
#                 f"Page {page_number + 1}: "
#                 "Poor text extraction detected"
#             )

#             pages_needing_ocr += 1

#             page_data.append(
#                 {
#                     "page": page_number + 1,
#                     "text": ""
#                 }
#             )

#     # -----------------------------------------------------
#     # STEP 2: OCR FALLBACK IF NEEDED
#     # -----------------------------------------------------

#     if pages_needing_ocr > 0:

#         print("\nOCR fallback required.")

#         # Reset file pointer before OCR
#         pdf_file.seek(0)

#         ocr_page_data = extract_text_with_ocr(
#             pdf_file
#         )

#         # Replace poor pages with OCR text
#         for index in range(len(page_data)):

#             if not page_data[index]["text"]:

#                 if index < len(ocr_page_data):

#                     page_data[index]["text"] = (
#                         ocr_page_data[index]["text"]
#                     )

#                     print(
#                         f"Page {index + 1}: "
#                         "OCR extraction completed"
#                     )

#     else:

#         print(
#             "\nNormal extraction was sufficient."
#         )

#     # -----------------------------------------------------
#     # STEP 3: CREATE STRUCTURED CHUNKS
#     # -----------------------------------------------------

#     chunks_with_metadata = create_chunks(
#         page_data
#     )

#     print("\n========================================")
#     print("PDF PROCESSING COMPLETED")
#     print("========================================")

#     print(
#         f"Total pages: {len(reader.pages)}"
#     )

#     print(
#         f"Total chunks: "
#         f"{len(chunks_with_metadata)}"
#     )

#     # -----------------------------------------------------
#     # IMPORTANT:
#     # FOR NOW RETURN ONLY TEXT
#     #
#     # This keeps compatibility with your existing
#     # embeddings.py and search.py.
#     # -----------------------------------------------------

#     chunks = [
#         chunk["text"]
#         for chunk in chunks_with_metadata
#     ]

#     return chunks




# from pypdf import PdfReader
# import re

# def process_pdf(pdf_file):

#     reader = PdfReader(pdf_file)

#     text = ""

#     for page in reader.pages:
#         extracted = page.extract_text()

#         if extracted:
#             text += extracted

#     # Clean text
#     text = re.sub(r'[^\x00-\x7F]+', ' ', text)
#     text = re.sub(r'\s+', ' ', text)

#     # Chunk text
#     sentences = re.split(r'(?<=[.!?]) +', text)

#     chunks = []
#     current_chunk = ""

#     chunk_size = 200

#     for sentence in sentences:

#         if len(current_chunk) + len(sentence) <= chunk_size:
#             current_chunk += " " + sentence

#         else:
#             chunks.append(current_chunk.strip())
#             current_chunk = sentence

#     if current_chunk:
#         chunks.append(current_chunk.strip())

#     return chunks