"""
Tests for the POST /activities/{activity_name}/signup endpoint.

This module contains tests for student signup functionality.
All tests use the AAA (Arrange-Act-Assert) pattern for clarity and maintainability.
"""

import pytest


def test_signup_valid_activity_and_email(client):
    """Test successful signup for an existing activity."""
    # Arrange
    email = "alice@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity."""
    # Arrange
    new_participant = "bob@mergington.edu"
    activity = "Chess Club"
    
    # Act
    client.post(
        f"/activities/{activity}/signup",
        params={"email": new_participant}
    )
    response = client.get("/activities")
    
    # Assert
    activities = response.json()
    assert new_participant in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == 3  # 2 initial + 1 new


def test_signup_duplicate_email_fails(client):
    """Test that signing up with duplicate email returns 400 error."""
    # Arrange
    duplicate_email = "michael@mergington.edu"  # Already signed up for Chess Club
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": duplicate_email}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_nonexistent_activity_fails(client):
    """Test that signup for non-existent activity returns 404 error."""
    # Arrange
    nonexistent_activity = "Nonexistent Activity"
    new_email = "alice@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_multiple_different_activities(client):
    """Test that same student can sign up for multiple different activities."""
    # Arrange
    alice = "alice@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    
    # Act
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": alice}
    )
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": alice}
    )
    verify_response = client.get("/activities")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities = verify_response.json()
    assert alice in activities[activity1]["participants"]
    assert alice in activities[activity2]["participants"]


def test_signup_response_message_format(client):
    """Test that signup response contains expected message format."""
    # Arrange
    email = "carol@mergington.edu"
    activity = "Gym Class"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
