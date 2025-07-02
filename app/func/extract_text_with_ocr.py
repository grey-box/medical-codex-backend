import logging
import os

from fastapi import UploadFile
from paddleocr import PaddleOCR
from config import LOGGER_NAME
from func.normalize_image import normalize_image
from sqlalchemy import false

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
        use_angle_cls=False,
        use_textline_orientation=False,
        use_doc_unwarping=False,
        use_doc_orientation_classify=False,
        lang='en',
        det_model_dir="/root/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer",
        rec_model_dir="/root/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer",
        cls_model_dir="/root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer",
        enable_mkldnn=True,
        use_gpu=False
    )

    image = normalize_image(file)
    print("Image Normalized Successfully")

    #extract all text from image and save in List
    print(f"Image shape: {image.shape}, dtype: {image.dtype}, type: {type(image)}")
    if image is None:
        return None

    #extract all text from image and save in List

    print("passing in image")
    try:
        results = ocr.ocr(image, cls=False)
        extracted_texts = []

        for box, (text, score) in results[0]:
            extracted_texts.append({
                "rec_text": text,
                "rec_score": score
            })

        return extracted_texts
    except Exception as e:
        print(f"[EXCEPTION] PaddleOCR failed")
        raise
    #print("getting results")
    #return results

