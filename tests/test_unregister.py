"""
Tests for the DELETE /activities/{activity_name}/signup endpoint.

This module contains tests for student unregistration functionality.
All tests use the AAA (Arrange-Act-Assert) pattern for clarity and maintainability.
"""

import pytest


def test_unregister_valid_participant(client):
    """Test successful unregistration of an existing participant."""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity}" in response.json()["message"]


def test_unregister_removes_participant_from_activity(client):
    """Test that unregister actually removes the participant from the activity."""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Act
    client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    response = client.get("/activities")
    
    # Assert
    activities = response.json()
    assert email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == 1  # Only Daniel left


def test_unregister_nonexistent_participant_fails(client):
    """Test that unregistering a non-existent participant returns 400 error."""
    # Arrange
    nonexistent_participant = "alice@mergington.edu"  # Never signed up
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": nonexistent_participant}
    )
    
    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up"


def test_unregister_nonexistent_activity_fails(client):
    """Test that unregister for non-existent activity returns 404 error."""
    # Arrange
    nonexistent_activity = "Nonexistent Activity"
    email = "michael@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_then_signup_again(client):
    """Test that after unregistering, a student can sign up again."""
    # Arrange
    participant = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Act - Unregister
    response1 = client.delete(
        f"/activities/{activity}/signup",
        params={"email": participant}
    )
    
    # Act - Sign up again
    response2 = client.post(
        f"/activities/{activity}/signup",
        params={"email": participant}
    )
    
    verify_response = client.get("/activities")
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities = verify_response.json()
    assert participant in activities[activity]["participants"]


def test_unregister_response_message_format(client):
    """Test that unregister response contains expected message format."""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]
