from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer
from database import Base, engine

# Create all tables
Base.metadata.create_all(engine)


class Languages(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    code = Column(String, unique=True)


class Words(Base):
    __tablename__ = 'available_words'
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, unique=True)
    language_id = Column(Integer, ForeignKey('languages.id'))
    source_id = Column(Integer, ForeignKey('source.id'))


class Source(Base):
    __tablename__ = 'source'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    quality = Column(Integer)


class Translations(Base):
    __tablename__ = 'translations'
    id = Column(Integer, primary_key=True, index=True)
    word1_id = Column(Integer, ForeignKey('available_words.id'))
    word2_id = Column(Integer, ForeignKey('available_words.id'))
    source_id = Column(Integer, ForeignKey('source.id'))


class TypeNormalizedIdentifiers(Base):
    __tablename__ = 'type_normalized_identifiers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


class NormalizedIdentifiers(Base):
    __tablename__ = 'normalized_identifiers'
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('available_words.id'))
    type_normalized_identifiers_id = Column(Integer, ForeignKey('type_normalized_identifiers.id'))
    normalized_id = Column(String, unique=True)
