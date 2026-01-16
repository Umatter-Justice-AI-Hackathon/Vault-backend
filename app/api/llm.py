"""
LLM API endpoints using Groq.

Provides AI-powered wellness insights and chat functionality.
"""

from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from groq import Groq

from app.database import get_db
from app.models import UserTable, WellnessMetrics
from app.config import settings
from app.schemas import (
    ChatRequest,
    ChatResponse,
    WellnessInsightRequest,
    WellnessInsightResponse
)

router = APIRouter()

# Initialize Groq client
groq_client = Groq(api_key=settings.groq_api_key) if settings.groq_api_key else None


def get_groq_client():
    """Get Groq client or raise error if not configured."""
    if not groq_client:
        raise HTTPException(
            status_code=503,
            detail="Groq API is not configured. Please set GROQ_API_KEY environment variable."
        )
    return groq_client


@router.post("/chat", response_model=ChatResponse)
def chat_with_llm(
    request: ChatRequest,
    db: Session = Depends(get_db),
    client: Groq = Depends(get_groq_client)
):
    """
    Chat with AI for wellness support.

    The AI acts as a supportive wellness companion.
    """
    try:
        # Create chat completion
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are a compassionate wellness companion AI.
Your role is to:
- Listen empathetically to users' concerns
- Provide supportive, non-judgmental responses
- Suggest healthy coping strategies
- Encourage professional help when needed
- Keep responses concise (2-3 paragraphs max)

Never diagnose or provide medical advice. Always prioritize user safety."""
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            model=settings.groq_model or "llama-3.1-70b-versatile",
            temperature=0.7,
            max_tokens=500,
        )

        response_message = chat_completion.choices[0].message.content

        return ChatResponse(
            message=response_message,
            model_used=settings.groq_model or "llama-3.1-70b-versatile"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with Groq API: {str(e)}"
        )


@router.post("/wellness-insight", response_model=WellnessInsightResponse)
def get_wellness_insight(
    request: WellnessInsightRequest,
    db: Session = Depends(get_db),
    client: Groq = Depends(get_groq_client)
):
    """
    Get AI-powered insights about user's wellness trend.

    Analyzes recent wellness scores and provides personalized recommendations.
    """
    # Get user's recent wellness data
    days = request.days or 7
    start_date = datetime.utcnow() - timedelta(days=days)

    metrics = db.query(WellnessMetrics).filter(
        WellnessMetrics.userid == request.userid,
        WellnessMetrics.time >= start_date
    ).order_by(WellnessMetrics.time.asc()).all()

    if not metrics:
        raise HTTPException(
            status_code=404,
            detail=f"No wellness data found for user {request.userid} in the last {days} days"
        )

    # Calculate statistics
    scores = [m.wellness_score for m in metrics]
    avg_score = sum(scores) / len(scores)
    min_score = min(scores)
    max_score = max(scores)

    # Determine trend
    if len(scores) >= 2:
        mid = len(scores) // 2
        first_half_avg = sum(scores[:mid]) / mid
        second_half_avg = sum(scores[mid:]) / (len(scores) - mid)

        if second_half_avg > first_half_avg + 0.5:
            trend = "improving"
        elif second_half_avg < first_half_avg - 0.5:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "insufficient data"

    # Create prompt for LLM
    scores_str = ", ".join([f"{s:.1f}" for s in scores])

    prompt = f"""Analyze this user's wellness journey:

Recent wellness scores (0-10 scale, last {days} days): {scores_str}

Statistics:
- Average: {avg_score:.1f}
- Trend: {trend}
- Range: {min_score:.1f} to {max_score:.1f}
- Number of recordings: {len(scores)}

Provide:
1. A brief, compassionate summary of their wellness pattern (2-3 sentences)
2. 2-3 specific, actionable recommendations to support their wellbeing
3. One encouraging message

Keep it personal, warm, and under 200 words."""

    try:
        # Get AI insight
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a compassionate wellness coach providing personalized insights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=settings.groq_model or "llama-3.1-70b-versatile",
            temperature=0.7,
            max_tokens=400,
        )

        insight = chat_completion.choices[0].message.content

        return WellnessInsightResponse(
            userid=request.userid,
            period_days=days,
            average_score=round(avg_score, 2),
            trend=trend,
            total_entries=len(scores),
            insight=insight,
            model_used=settings.groq_model or "llama-3.1-70b-versatile"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating wellness insight: {str(e)}"
        )


@router.post("/analyze-message", response_model=dict)
def analyze_message_sentiment(
    request: ChatRequest,
    client: Groq = Depends(get_groq_client)
):
    """
    Analyze the sentiment and wellness score of a user's message.

    Returns a wellness score (0-10) and sentiment analysis.
    """
    prompt = f"""Analyze this message and provide:
1. A wellness score from 0-10 (0 = severe distress, 10 = excellent wellbeing)
2. Brief sentiment analysis (1 sentence)
3. Any concerning indicators (if present)

Message: "{request.message}"

Respond in this exact format:
Score: [number]
Sentiment: [one sentence]
Concerns: [none or brief list]"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a mental health assessment AI. Provide objective, clinical analysis."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=settings.groq_model or "llama-3.1-70b-versatile",
            temperature=0.3,
            max_tokens=200,
        )

        analysis = chat_completion.choices[0].message.content

        # Parse the response to extract score
        score = None
        if "Score:" in analysis:
            try:
                score_line = [line for line in analysis.split('\n') if 'Score:' in line][0]
                score = float(score_line.split(':')[1].strip())
                score = max(0.0, min(10.0, score))  # Clamp to 0-10
            except:
                pass

        return {
            "analysis": analysis,
            "estimated_wellness_score": score,
            "message": request.message
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing message: {str(e)}"
        )


@router.get("/test-connection")
def test_groq_connection(client: Groq = Depends(get_groq_client)):
    """
    Test Groq API connection.

    Returns model information if successful.
    """
    try:
        # Simple test request
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Hello! Respond with 'Connection successful'"
                }
            ],
            model=settings.groq_model or "llama-3.1-70b-versatile",
            max_tokens=20,
        )

        return {
            "status": "connected",
            "message": response.choices[0].message.content,
            "model": settings.groq_model or "llama-3.1-70b-versatile",
            "provider": "Groq"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Groq API connection failed: {str(e)}"
        )
