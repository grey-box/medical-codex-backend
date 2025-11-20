import logging
import os
from pathlib import Path

from fastapi import UploadFile
from paddleocr import PaddleOCR

from config import LOGGER_NAME
from func.normalize_image import normalize_image

logger = logging.getLogger(LOGGER_NAME)

def _get_model_dir(*segments: str) -> str:
    base_dir = Path(os.environ.get("PADDLE_OCR_BASE_DIR", Path.home() / ".paddleocr"))
    target = base_dir.joinpath(*segments)
    target.mkdir(parents=True, exist_ok=True)
    return str(target)

def extract_text_with_ocr(file: UploadFile):
    """
        Extracts text from an image using PaddleOCR CPU

        Passes a normalized image into the OCR model and then returns extracted information in the form of a list

        Args:
            file (UploadFile): A file uploaded by the frontend through fastAPI

        Returns:
            A List of text, confidence score pairs

        """

    #Call OCR and pass in pre-downloaded models, language and set to CPU mode
    det_model_dir = _get_model_dir("whl", "det", "en", "en_PP-OCRv3_det_infer")
    rec_model_dir = _get_model_dir("whl", "rec", "en", "en_PP-OCRv3_rec_infer")
    cls_model_dir = _get_model_dir("whl", "cls", "ch_ppocr_mobile_v2.0_cls_infer")

    ocr = PaddleOCR(
        use_angle_cls=False,
        use_textline_orientation=False,
        use_doc_unwarping=False,
        use_doc_orientation_classify=False,
        lang='en',
        det_model_dir=det_model_dir,
        rec_model_dir=rec_model_dir,
        cls_model_dir=cls_model_dir,
        enable_mkldnn=True,
        use_gpu=False
    )

    #Normalize file for OCR processing
    image = normalize_image(file)

    if image is None:
        return None

    #extract all text from image and save in List
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
