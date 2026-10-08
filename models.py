from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

# ORM Class
class Word(Base):
    __tablename__ = "word"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)