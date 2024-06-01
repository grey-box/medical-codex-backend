from sqlalchemy.orm import Session

import schemas


def translate(db: Session, query: schemas.TranslationQuery):
    return None
