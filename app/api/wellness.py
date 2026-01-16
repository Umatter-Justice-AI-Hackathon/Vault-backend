"""
Wellness metrics API endpoints.

Handles CRUD operations for wellness metrics.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserTable, WellnessMetrics
from app.schemas import (
    WellnessMetricCreate,
    WellnessMetricResponse,
    WellnessHistoryResponse,
    WellnessTrendResponse,
    UserResponse
)

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(db: Session = Depends(get_db)):
    """
    Create a new user.

    Returns the userid of the newly created user.
    """
    new_user = UserTable()
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{userid}", response_model=UserResponse)
def get_user(userid: int, db: Session = Depends(get_db)):
    """Get a user by userid."""
    user = db.query(UserTable).filter(UserTable.userid == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users", response_model=List[UserResponse])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List all users with pagination."""
    users = db.query(UserTable).offset(skip).limit(limit).all()
    return users


@router.post("/wellness-metrics", response_model=WellnessMetricResponse, status_code=201)
def create_wellness_metric(
    metric: WellnessMetricCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new wellness metric entry for a user.

    If time is not provided, current time will be used.
    """
    # Check if user exists
    user = db.query(UserTable).filter(UserTable.userid == metric.userid).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {metric.userid} not found")

    # Create wellness metric
    new_metric = WellnessMetrics(
        userid=metric.userid,
        wellness_score=metric.wellness_score,
        time=metric.time if metric.time else datetime.utcnow()
    )

    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric


@router.get("/wellness-metrics/{metric_id}", response_model=WellnessMetricResponse)
def get_wellness_metric(metric_id: int, db: Session = Depends(get_db)):
    """Get a specific wellness metric by ID."""
    metric = db.query(WellnessMetrics).filter(WellnessMetrics.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Wellness metric not found")
    return metric


@router.get("/users/{userid}/wellness-metrics", response_model=WellnessHistoryResponse)
def get_user_wellness_history(
    userid: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Get wellness history for a specific user.

    - **userid**: The user ID
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **start_date**: Filter metrics from this date onwards
    - **end_date**: Filter metrics up to this date
    """
    # Check if user exists
    user = db.query(UserTable).filter(UserTable.userid == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {userid} not found")

    # Build query
    query = db.query(WellnessMetrics).filter(WellnessMetrics.userid == userid)

    if start_date:
        query = query.filter(WellnessMetrics.time >= start_date)
    if end_date:
        query = query.filter(WellnessMetrics.time <= end_date)

    # Get total count
    total_count = query.count()

    # Get metrics ordered by time (most recent first)
    metrics = query.order_by(WellnessMetrics.time.desc()).offset(skip).limit(limit).all()

    # Calculate average score
    avg_score = None
    if metrics:
        avg_score = sum(m.wellness_score for m in metrics) / len(metrics)

    return WellnessHistoryResponse(
        userid=userid,
        metrics=metrics,
        total_count=total_count,
        average_score=avg_score
    )


@router.get("/users/{userid}/wellness-trend", response_model=WellnessTrendResponse)
def get_user_wellness_trend(
    userid: int,
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    db: Session = Depends(get_db)
):
    """
    Get wellness trend analysis for a user.

    Analyzes the wellness scores over the specified period and determines
    if the trend is improving, declining, or stable.

    - **userid**: The user ID
    - **days**: Number of days to analyze (default: 30)
    """
    # Check if user exists
    user = db.query(UserTable).filter(UserTable.userid == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {userid} not found")

    # Get metrics for the specified period
    start_date = datetime.utcnow() - timedelta(days=days)
    metrics = db.query(WellnessMetrics).filter(
        WellnessMetrics.userid == userid,
        WellnessMetrics.time >= start_date
    ).order_by(WellnessMetrics.time.asc()).all()

    if not metrics:
        raise HTTPException(
            status_code=404,
            detail=f"No wellness metrics found for user {userid} in the last {days} days"
        )

    # Calculate average score
    avg_score = sum(m.wellness_score for m in metrics) / len(metrics)

    # Determine trend (simple analysis based on first half vs second half)
    trend = "stable"
    if len(metrics) >= 4:
        mid_point = len(metrics) // 2
        first_half_avg = sum(m.wellness_score for m in metrics[:mid_point]) / mid_point
        second_half_avg = sum(m.wellness_score for m in metrics[mid_point:]) / (len(metrics) - mid_point)

        diff = second_half_avg - first_half_avg
        if diff > 0.5:
            trend = "improving"
        elif diff < -0.5:
            trend = "declining"

    return WellnessTrendResponse(
        userid=userid,
        data_points=metrics,
        trend=trend,
        average_score=round(avg_score, 2),
        period_days=days
    )


@router.delete("/wellness-metrics/{metric_id}", status_code=204)
def delete_wellness_metric(metric_id: int, db: Session = Depends(get_db)):
    """Delete a wellness metric by ID."""
    metric = db.query(WellnessMetrics).filter(WellnessMetrics.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Wellness metric not found")

    db.delete(metric)
    db.commit()
    return None


@router.delete("/users/{userid}", status_code=204)
def delete_user(userid: int, db: Session = Depends(get_db)):
    """
    Delete a user and all their wellness metrics.

    WARNING: This will cascade delete all wellness metrics for this user.
    """
    user = db.query(UserTable).filter(UserTable.userid == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {userid} not found")

    db.delete(user)
    db.commit()
    return None
