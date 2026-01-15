"""
Database models for the Umatter application.

Defines the schema for users, sessions, and analytics data.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User account information from OAuth providers."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    provider = Column(String, nullable=False)  # google, github, microsoft
    provider_user_id = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    analytics = relationship("UserAnalytics", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, provider={self.provider})>"


class Session(Base):
    """Individual chat sessions with wellbeing scores."""

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    wellbeing_score = Column(Float, nullable=True)  # 0-10 scale
    session_summary = Column(Text, nullable=True)
    action_plan = Column(Text, nullable=True)  # JSON stored as text
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, user_id={self.user_id}, score={self.wellbeing_score})>"


class Message(Base):
    """Individual messages within a chat session."""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    role = Column(String, nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    session = relationship("Session", back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, role={self.role}, session_id={self.session_id})>"


class UserAnalytics(Base):
    """
    Anonymized aggregated user wellbeing data for analytics.
    
    This stores anonymized data that can be used for trends and insights
    without revealing personal information.
    """

    __tablename__ = "user_analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    average_wellbeing_score = Column(Float, nullable=True)
    session_count = Column(Integer, default=0, nullable=False)
    total_messages = Column(Integer, default=0, nullable=False)
    
    # Anonymized demographic info (optional, added later if needed)
    # industry = Column(String, nullable=True)
    # team_size = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="analytics")

    def __repr__(self) -> str:
        return f"<UserAnalytics(id={self.id}, date={self.date}, score={self.average_wellbeing_score})>"
