from database import SessionLocal
from fastapi import HTTPException
import logging

logger = logging.getLogger("db")


def get_db():
    db = SessionLocal()
    try:
        logger.info("DB session created successfully.")
        yield db
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        db.close()
        logger.info("DB session closed.")
