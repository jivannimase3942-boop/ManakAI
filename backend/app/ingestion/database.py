from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

DATABASE_URL = "sqlite:///./pending_knowledge.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBIngestionRecord(Base):
    __tablename__ = "ingestion_records"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    standard_number = Column(String, index=True, nullable=True)
    topic = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    applicability = Column(String, nullable=False)
    requirements = Column(JSON, default=list)
    testing_information = Column(JSON, default=dict)
    certification_information = Column(JSON, default=dict)
    required_documents = Column(JSON, default=list)
    next_actions = Column(JSON, default=list)
    keywords = Column(JSON, default=list)
    source_name = Column(String, nullable=False)
    source_url = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    verification_status = Column(String, nullable=False, default="PENDING")
    collected_at = Column(DateTime, default=datetime.utcnow)
    last_verified = Column(DateTime, nullable=True)
    revision = Column(Integer, default=1)
    supersedes_id = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
