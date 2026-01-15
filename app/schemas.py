"""
Pydantic schemas for request/response validation.

These schemas define the structure of data sent to and from the API.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

# ============================================================================
# User Schemas
# ============================================================================


class UserBase(BaseModel):
    """Base user information."""

    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    """Schema for creating a new user."""

    provider: str
    provider_user_id: str


class UserResponse(UserBase):
    """Schema for user responses."""

    id: int
    provider: str
    created_at: datetime
    last_login: datetime
    is_active: bool

    class Config:
        from_attributes = True


# ============================================================================
# Session Schemas
# ============================================================================


class SessionCreate(BaseModel):
    """Schema for starting a new session."""

    pass  # Sessions are created automatically when user starts chatting


class SessionResponse(BaseModel):
    """Schema for session responses."""

    id: int
    user_id: int
    started_at: datetime
    ended_at: datetime | None = None
    wellbeing_score: float | None = None
    session_summary: str | None = None
    action_plan: str | None = None

    class Config:
        from_attributes = True


class SessionUpdate(BaseModel):
    """Schema for updating session information."""

    wellbeing_score: float | None = None
    session_summary: str | None = None
    action_plan: str | None = None


# ============================================================================
# Message Schemas
# ============================================================================


class MessageCreate(BaseModel):
    """Schema for creating a new message."""

    content: str = Field(..., min_length=1, max_length=10000)


class MessageResponse(BaseModel):
    """Schema for message responses."""

    id: int
    session_id: int
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True


# ============================================================================
# Chat Schemas
# ============================================================================


class ChatRequest(BaseModel):
    """Schema for chat requests."""

    message: str = Field(..., min_length=1, max_length=10000)
    session_id: int | None = None  # If None, create new session


class ChatResponse(BaseModel):
    """Schema for chat responses."""

    session_id: int
    message: str
    wellbeing_score: float | None = None
    requires_intervention: bool = False
    intervention_type: str | None = None  # breathing, grounding, etc.


# ============================================================================
# Analytics Schemas
# ============================================================================


class AnalyticsResponse(BaseModel):
    """Schema for user analytics data."""

    date: datetime
    average_wellbeing_score: float | None = None
    session_count: int
    total_messages: int

    class Config:
        from_attributes = True


class WellbeingTrendResponse(BaseModel):
    """Schema for wellbeing trend data."""

    data_points: list[AnalyticsResponse]
    trend: str  # improving, declining, stable
    recommendation: str | None = None


# ============================================================================
# Action Plan Schemas
# ============================================================================


class ActionItem(BaseModel):
    """Individual action item in an action plan."""

    title: str
    description: str
    priority: str  # high, medium, low
    category: str  # workplace, personal, professional_help


class ActionPlanResponse(BaseModel):
    """Schema for action plan responses."""

    session_id: int
    generated_at: datetime
    actions: list[ActionItem]
    summary: str


# ============================================================================
# Authentication Schemas
# ============================================================================


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data."""

    user_id: int | None = None
    email: str | None = None
