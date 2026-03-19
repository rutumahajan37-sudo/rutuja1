"""
Pytest configuration and fixtures for FastAPI tests.

This module provides fixtures for testing the Mergington High School Activities API.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provides a TestClient instance for testing the FastAPI application.
    
    The client allows us to make requests to the API without running a live server.
    """
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities(client):
    """
    Reset activities to initial state before each test.
    
    This ensures test isolation by resetting the in-memory database
    to a known state before each test runs.
    """
    # Reset to initial state
    from src.app import activities
    
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    })
    
    yield
