import os
import pytesseract


TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


print(
    "Tesseract exists:",
    os.path.exists(TESSERACT_PATH)
)


pytesseract.pytesseract.tesseract_cmd = (
    TESSERACT_PATH
)


print(
    "Tesseract version:"
)


print(
    pytesseract.get_tesseract_version()
)