import logging
import shutil
import uuid
from io import BytesIO
from pathlib import Path

import clamd
from PIL import Image
from fastapi import UploadFile, HTTPException

from starlette.datastructures import UploadFile as StarletteUploadFile

from config import LOGGER_NAME, settings

logger = logging.getLogger(LOGGER_NAME)


def scan_and_clean_uploadfile(file: UploadFile) -> UploadFile:
    """
        OCR Module.
        Malware Detection and File Handling

        This module provides functionality for isolating, scanning, cleaning and deleting all files
        sent to the OCR via the frontend. Its goal is to ensure that the backend codebase remains clean and malware free

        Args:
            file (UploadFile): File uploaded by the frontend to the OCR

        Returns:
            UploadFile: A cleaned file that can be processed by the OCR.
            Returns None if the parameter file is infected or corrupted.

        Raises:
            HTTPException: If file is dangerous, corrupted or cannot be cleaned.
    """

    #create isolated quarantine temp directory
    temp_dir = Path("/tmp/quarantines") / str(uuid.uuid4())
    temp_dir.mkdir(parents=True, exist_ok=True)

    original_path = temp_dir / file.filename

    try:
        with  original_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            logger.info("Successfully moved file to quarantine")

        clamav_client = None
        if settings.enable_file_scanning:
            try:
                clamav_client = clamd.ClamdNetworkSocket(
                    host=settings.clamav_host,
                    port=settings.clamav_port,
                )
                if not clamav_client.ping():
                    raise RuntimeError("ClamAV daemon not responding")
                logger.info("Connected To ClamAV")
                result = clamav_client.scan(str(original_path))
                if result and any(status[0] == "FOUND" for _, status in result.items()):
                    raise HTTPException(status_code=400, detail="Dangerous file detected")
                logger.info("File scanned successfully")
            except Exception as exc:
                if settings.require_file_scanning:
                    raise HTTPException(status_code=503, detail=f"File scanning failed: {exc}") from exc
                logger.warning(
                    "ClamAV unavailable (%s); skipping malware scan for this file.",
                    exc,
                )
        else:
            logger.debug("File scanning disabled via settings; skipping ClamAV check.")

        img = Image.open(original_path)
        img = img.convert("RGB")

        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        logger.info("Successfully cleaned file")

        cleaned_upload = StarletteUploadFile(
            filename=f"cleaned_{file.filename}",
            file = buffer,
        )
        logger.info("Converted back to Uploadfile")

        return cleaned_upload

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed To Check The File: {str(e)}")

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.info("Directory Removed")
