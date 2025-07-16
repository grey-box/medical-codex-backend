import logging
import os
import shutil
import uuid
from io import BytesIO

import clamd
from PIL import Image
from fastapi import File, UploadFile, HTTPException
from pathlib import Path

from starlette.datastructures import UploadFile as StarletteUploadFile

from config import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def scan_and_clean_uploadfile(file: UploadFile) -> UploadFile:

    #create isolated quarantine temp directory
    temp_dir = Path("/tmp/quarantines") / str(uuid.uuid4())
    temp_dir.mkdir(parents=True, exist_ok=True)

    original_path = temp_dir / file.filename

    try:
        with  original_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            logger.info("Successfully moved file to quarantine")

        cd = clamd.ClamdNetworkSocket(host="127.0.0.1", port=3310)
        if not cd.ping():
            raise HTTPException(status_code=503, detail="ClamAV daemon not responding")
        logger.info("Connected To ClamAV")

        result = cd.scan(str(original_path))
        if result and any(status[0] == 'FOUND' for _, status in result.items()):
            raise HTTPException(status_code=400, detail="Dangerous file detected")
        logger.info("File scanned successfully")

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

