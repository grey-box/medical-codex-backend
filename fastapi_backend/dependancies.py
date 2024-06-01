from database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
    finally:
        db.close()
