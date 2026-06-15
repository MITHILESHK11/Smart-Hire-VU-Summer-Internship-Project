# models.py
# SQLAlchemy Models for AI-Powered Resume Ranking System

from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    jd_text = Column(Text, nullable=False)
    status = Column(String, default="PENDING")  # PENDING, PROCESSING, COMPLETED, FAILED

    resumes = relationship("Resume", back_populates="session", cascade="all, delete-orphan")
    results = relationship("Result", back_populates="session", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"

    resume_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False)
    filename = Column(String, nullable=False)
    raw_text = Column(Text, nullable=False)
    parsed_skills = Column(Text)        # Stored as serialized JSON string
    parsed_education = Column(Text)     # Stored as serialized JSON string
    parsed_experience = Column(Text)    # Stored as serialized JSON string

    session = relationship("Session", back_populates="resumes")
    result = relationship("Result", uselist=False, back_populates="resume", cascade="all, delete-orphan")


class Result(Base):
    __tablename__ = "results"

    result_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False)
    resume_id = Column(String, ForeignKey("resumes.resume_id", ondelete="CASCADE"), nullable=False)
    tfidf_score = Column(Float, nullable=False)
    sbert_score = Column(Float, nullable=False)
    final_score = Column(Float, nullable=False)
    missing_keywords = Column(Text)     # Stored as serialized JSON string
    rank_position = Column(Integer, nullable=False)

    session = relationship("Session", back_populates="results")
    resume = relationship("Resume", back_populates="result")
