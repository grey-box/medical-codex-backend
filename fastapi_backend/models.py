from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import String, Integer
from database import Base, engine

# Create all tables
Base.metadata.create_all(engine)
