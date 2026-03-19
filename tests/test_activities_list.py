"""
Tests for the GET /activities endpoint.

This module contains tests for retrieving the list of all available activities.
All tests use the AAA (Arrange-Act-Assert) pattern for clarity and maintainability.
"""


def test_get_activities_returns_success(client):
    """Test that GET /activities returns HTTP 200."""
    # Arrange
    # (No special setup needed; client fixture is ready)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all initialized activities."""
    # Arrange
    # (Activities initialized by reset_activities fixture)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities


def test_get_activities_response_structure(client):
    """Test that each activity has the correct response structure."""
    # Arrange
    expected_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    chess_club = activities["Chess Club"]
    
    # Assert
    for field in expected_fields:
        assert field in chess_club, f"Missing field: {field}"
    assert isinstance(chess_club["participants"], list)


def test_get_activities_shows_current_participants(client):
    """Test that current participants are correctly returned."""
    # Arrange
    expected_participants = {"michael@mergington.edu", "daniel@mergington.edu"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    chess_club = activities["Chess Club"]
    actual_participants = set(chess_club["participants"])
    
    # Assert
    assert len(chess_club["participants"]) == 2
    assert actual_participants == expected_participants
