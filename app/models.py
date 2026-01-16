"""
Database models for the Umatter application.

Matches existing Render database structure:
- user_table: [userid]
- wellness_metrics: [id, userid, time, wellness_score]
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class UserTable(Base):
    """Simple user table matching existing Render database."""

    __tablename__ = "user_table"

    userid = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # Relationship to wellness metrics
    wellness_metrics = relationship("WellnessMetrics", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<UserTable(userid={self.userid})>"


class WellnessMetrics(Base):
    """Wellness metrics table matching existing Render database."""

    __tablename__ = "wellness_metrics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("user_table.userid"), nullable=False, index=True)
    time = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    wellness_score = Column(Float, nullable=False)  # 0-10 scale

    # Relationship to user
    user = relationship("UserTable", back_populates="wellness_metrics")

    def __repr__(self) -> str:
        return f"<WellnessMetrics(id={self.id}, userid={self.userid}, score={self.wellness_score}, time={self.time})>"
