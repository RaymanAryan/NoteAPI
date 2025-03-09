from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

# SQLAlchemy base
Base = declarative_base()

# SQLAlchemy ORM model
class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

# Pydantic schema for API responses
class NoteSchema(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True  # This allows Pydantic to work with SQLAlchemy models

class NoteCreate(BaseModel):
    title: str
    content: str
    class Config:
        from_attributes = True  # This allows Pydantic to work with SQLAlchemy models

# Create the engine (SQLite automatically creates the file if it doesn’t exist)
engine = create_engine('sqlite:///notes.db', echo=False)

# Ensure tables are created
Base.metadata.create_all(engine)

# Create a sessionmaker instance
SessionLocal = sessionmaker(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()  # Create a new session for each request
    try:
        yield db
    finally:
        db.close()
