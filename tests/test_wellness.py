"""
Tests for wellness API endpoints.
"""

from datetime import datetime
from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    """Test creating a new user."""
    response = client.post("/api/v1/wellness/users")

    assert response.status_code == 201
    data = response.json()
    assert "userid" in data
    assert isinstance(data["userid"], int)


def test_get_user(client: TestClient):
    """Test getting a user by ID."""
    # First create a user
    create_response = client.post("/api/v1/wellness/users")
    userid = create_response.json()["userid"]

    # Then get the user
    response = client.get(f"/api/v1/wellness/users/{userid}")

    assert response.status_code == 200
    data = response.json()
    assert data["userid"] == userid


def test_get_nonexistent_user(client: TestClient):
    """Test getting a user that doesn't exist."""
    response = client.get("/api/v1/wellness/users/99999")
    assert response.status_code == 404


def test_create_wellness_metric(client: TestClient):
    """Test creating a wellness metric."""
    # First create a user
    user_response = client.post("/api/v1/wellness/users")
    userid = user_response.json()["userid"]

    # Create wellness metric
    metric_data = {
        "userid": userid,
        "wellness_score": 7.5
    }
    response = client.post("/api/v1/wellness/wellness-metrics", json=metric_data)

    assert response.status_code == 201
    data = response.json()
    assert data["userid"] == userid
    assert data["wellness_score"] == 7.5
    assert "id" in data
    assert "time" in data


def test_create_wellness_metric_invalid_score(client: TestClient):
    """Test creating a wellness metric with invalid score."""
    # First create a user
    user_response = client.post("/api/v1/wellness/users")
    userid = user_response.json()["userid"]

    # Try to create metric with invalid score (> 10)
    metric_data = {
        "userid": userid,
        "wellness_score": 15.0
    }
    response = client.post("/api/v1/wellness/wellness-metrics", json=metric_data)

    assert response.status_code == 422  # Validation error


def test_create_wellness_metric_nonexistent_user(client: TestClient):
    """Test creating a wellness metric for non-existent user."""
    metric_data = {
        "userid": 99999,
        "wellness_score": 7.5
    }
    response = client.post("/api/v1/wellness/wellness-metrics", json=metric_data)

    assert response.status_code == 404


def test_get_user_wellness_history(client: TestClient):
    """Test getting wellness history for a user."""
    # Create user
    user_response = client.post("/api/v1/wellness/users")
    userid = user_response.json()["userid"]

    # Add multiple wellness metrics
    scores = [6.0, 7.5, 8.0]
    for score in scores:
        client.post("/api/v1/wellness/wellness-metrics", json={
            "userid": userid,
            "wellness_score": score
        })

    # Get history
    response = client.get(f"/api/v1/wellness/users/{userid}/wellness-metrics")

    assert response.status_code == 200
    data = response.json()
    assert data["userid"] == userid
    assert data["total_count"] == 3
    assert len(data["metrics"]) == 3
    assert data["average_score"] is not None


def test_get_user_wellness_trend(client: TestClient):
    """Test getting wellness trend analysis."""
    # Create user
    user_response = client.post("/api/v1/wellness/users")
    userid = user_response.json()["userid"]

    # Add multiple wellness metrics
    scores = [5.0, 6.0, 7.0, 8.0, 9.0]
    for score in scores:
        client.post("/api/v1/wellness/wellness-metrics", json={
            "userid": userid,
            "wellness_score": score
        })

    # Get trend
    response = client.get(f"/api/v1/wellness/users/{userid}/wellness-trend?days=30")

    assert response.status_code == 200
    data = response.json()
    assert data["userid"] == userid
    assert data["trend"] in ["improving", "declining", "stable"]
    assert data["average_score"] > 0
    assert data["period_days"] == 30
    assert len(data["data_points"]) == 5


def test_delete_wellness_metric(client: TestClient):
    """Test deleting a wellness metric."""
    # Create user and metric
    user_response = client.post("/api/v1/wellness/users")
    userid = user_response.json()["userid"]

    metric_response = client.post("/api/v1/wellness/wellness-metrics", json={
        "userid": userid,
        "wellness_score": 7.5
    })
    metric_id = metric_response.json()["id"]

    # Delete metric
    response = client.delete(f"/api/v1/wellness/wellness-metrics/{metric_id}")
    assert response.status_code == 204

    # Verify it's deleted
    get_response = client.get(f"/api/v1/wellness/wellness-metrics/{metric_id}")
    assert get_response.status_code == 404


def test_delete_user_cascade(client: TestClient):
    """Test that deleting a user also deletes their metrics."""
    # Create user
    user_response = client.post("/api/v1/wellness/users")
    userid = user_response.json()["userid"]

    # Add metrics
    metric_response = client.post("/api/v1/wellness/wellness-metrics", json={
        "userid": userid,
        "wellness_score": 7.5
    })
    metric_id = metric_response.json()["id"]

    # Delete user
    response = client.delete(f"/api/v1/wellness/users/{userid}")
    assert response.status_code == 204

    # Verify user is deleted
    user_get_response = client.get(f"/api/v1/wellness/users/{userid}")
    assert user_get_response.status_code == 404

    # Verify metrics are also deleted (cascade)
    metric_get_response = client.get(f"/api/v1/wellness/wellness-metrics/{metric_id}")
    assert metric_get_response.status_code == 404
