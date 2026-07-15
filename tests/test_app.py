import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def reset_activities():
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    yield
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_adds_participant(client):
    response = client.post(
        "/activities/Chess Club/signup?email=alex@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up alex@mergington.edu for Chess Club"
    assert "alex@mergington.edu" in activities["Chess Club"]["participants"]


def test_unregistering_a_participant_removes_them_from_the_activity(client):
    response = client.delete(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
