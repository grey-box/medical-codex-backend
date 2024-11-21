from sqlalchemy import Column
from sqlalchemy.types import String, Integer

from app.database import Base, engine

# Create all tables
Base.metadata.create_all(engine)




class UniqueTranslationsORM(Base):
    """
        The "unique_translation_table" model is used to build a single
        translation table that is the first and main source to
        query for translation results.
    """
    __tablename__ = "unique_translation_table"

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


class LanguagePairs(Base):
    """
        View for language pairs from the 'unique_translation_table' table.
        View is named: 'available_languages_view'

        Excludes odd names like
    """
    __tablename__ = "available_languages_view"

    source_language = Column(String, nullable=False, primary_key=True)
    target_language = Column(String, nullable=False, primary_key=True)

    __table_args__ = {'autoload_with': engine}

    def __repr__(self):
        return f'\
<Language(\n\
    source_language={self.source_language},\n\
    target_language={self.target_language}\n\
)>'


