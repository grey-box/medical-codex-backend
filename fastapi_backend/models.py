from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer
from database import Base, engine

# Create all tables
Base.metadata.create_all(engine)


'''
    The "Translation" Table models are used to build a single
    translation table that is the first and main source to 
    query for translation results.
'''
class UniqueTranslationsORM(Base):
    __tablename__ = "unique_translation"

    id = Column(Integer, primary_key=True)  
    source_language = Column(String, nullable=False)
    target_language = Column(String, nullable=False)
    source_text = Column(String, nullable=False)
    target_text = Column(String, nullable=False)
    table_name = Column(String, nullable=False)
    source_comment = Column(String, nullable=True)
    weight = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Translation( \
                    source_language={self.source_language}, \
                    target_language={self.target_language}, \
                    source_text={self.source_text}, \
                    target_text={self.target_text}, \
                    table_name={self.table_name}, \
                    weight={self.weight} \
                )>"
    


