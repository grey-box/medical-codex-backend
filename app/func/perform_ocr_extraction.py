import logging

from paddleocr import PaddleOCR
from app.config import LOGGER_NAME
from app.func.normalize_image import normalize_image

logger = logging.getLogger(LOGGER_NAME)

def perform_ocr_extraction(image_path: str):
    """
        Extracts text from an image using PaddleOCR CPU

        Passes a normalized image into the OCR model and then returns extracted information in the form of a list

        Args:
            image_path (str): File Path To The Input Image

        Returns:
            A List of text, confidence score pairs

        """

    ocr = PaddleOCR(
        use_textline_orientation= False,
        use_doc_unwarping= False,
        use_doc_orientation_classify=False,
    )

    image = normalize_image(image_path)

    #extract all text from image and save in List
    if image is None:
        return None

    results = ocr.ocr(image)

    #extract all text from image and save in List
    results = ocr.ocr(image_path)
    return results

