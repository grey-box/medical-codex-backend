import logging

from fastapi import UploadFile
from paddleocr import PaddleOCR
from app.config import LOGGER_NAME
from app.func.normalize_image import normalize_image

logger = logging.getLogger(LOGGER_NAME)

def extract_text_with_ocr(file: UploadFile):
    """
        Extracts text from an image using PaddleOCR CPU

        Passes a normalized image into the OCR model and then returns extracted information in the form of a list

        Args:
            file (UploadFile): A file uploaded by the frontend through fastAPI

        Returns:
            A List of text, confidence score pairs

        """

    ocr = PaddleOCR(
        use_textline_orientation= False,
        use_doc_unwarping= False,
        use_doc_orientation_classify=False,
    )

    image = normalize_image(file)

    #extract all text from image and save in List
    if image is None:
        return None

    results = ocr.ocr(image)

    #extract all text from image and save in List
    results = ocr.ocr(file)
    return results

