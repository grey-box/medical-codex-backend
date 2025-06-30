import cv2
import numpy as np
import os

from fastapi import UploadFile


def normalize_image(file:UploadFile, target_max_dimensions: int = 1024):
    """
            Retrieves an image file through the path and normalizes it for OCR processing.

            This function ensures that all valid images are formated properly. This avoids crashes later on
            when being processed by the OCR.

            Args:
                file(UploadFile): A file uploaded by the frontend through fastAPI
                target_max_dimensions (int): Maximum dimensions of an input image. Resolution is reduced if
                    the current input exceeds this value. Defaults to 1024.

            Returns:
                A normalized image to feed into the OCR. Returns None in the case of failure such as invalid file format.

    """
    try:
        #ensures that the file can be read as an image
        contents = file.file.read()
        np_array = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if image is None:
            print("Failed to decode image")
            return None

        #set image to proper rgb values preferred by PaddleOCR
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        #Check image resolution and refactor if needed
        height, width = image.shape[:2]
        max_dimensions = max(height, width)
        if max_dimensions > target_max_dimensions:
            scale = target_max_dimensions / max_dimensions
            image = cv2.resize(image,(int(width * scale), int(height * scale)), interpolation=cv2.INTER_AREA)

        #ensure that image contains safe numerical values for the OCR
        if not np.isfinite(image).all():
            print("Image contains invalid values")
            return None

        return image

    except Exception as e:
        print(f"[ERROR] Exception reading image {file.filename}: {e}")
        return None