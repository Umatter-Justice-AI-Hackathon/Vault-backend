"""
Pydantic schemas for request/response validation.

Matches simplified database structure:
- user_table: [userid]
- wellness_metrics: [id, userid, time, wellness_score]
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from pydantic import BaseModel, EmailStr, Field

# ============================================================================
# User Schemas
# ============================================================================

class UserResponse(BaseModel):
    """Schema for user responses."""
    userid: int

    class Config:
        from_attributes = True


# ============================================================================
# Wellness Metrics Schemas
# ============================================================================

class WellnessMetricCreate(BaseModel):
    """Schema for creating a new wellness metric entry."""
    userid: int
    wellness_score: float = Field(..., ge=0, le=10, description="Wellness score between 0-10")
    time: Optional[datetime] = None  # If None, will use current time


class WellnessMetricResponse(BaseModel):
    """Schema for wellness metric responses."""
    id: int
    userid: int
    time: datetime
    wellness_score: float

    class Config:
        from_attributes = True


class WellnessHistoryResponse(BaseModel):
    """Schema for wellness history (list of metrics for a user)."""
    userid: int
    metrics: List[WellnessMetricResponse]
    total_count: int
    average_score: Optional[float] = None


# ============================================================================
# Analytics Schemas
# ============================================================================

class WellnessTrendResponse(BaseModel):
    """Schema for wellness trend data."""
    userid: int
    data_points: List[WellnessMetricResponse]
    trend: str  # "improving", "declining", "stable"
    average_score: float
    period_days: int


# ============================================================================
# LLM / Chat Schemas
# ============================================================================


class ChatRequest(BaseModel):
    """Schema for chat requests."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's message")


class ChatResponse(BaseModel):
    """Schema for chat responses."""
    message: str
    model_used: str


class WellnessInsightRequest(BaseModel):
    """Schema for requesting wellness insights."""
    userid: int
    days: Optional[int] = Field(7, ge=1, le=90, description="Number of days to analyze")


class WellnessInsightResponse(BaseModel):
    """Schema for wellness insight responses."""
    userid: int
    period_days: int
    average_score: float
    trend: str
    total_entries: int
    insight: str
    model_used: str
