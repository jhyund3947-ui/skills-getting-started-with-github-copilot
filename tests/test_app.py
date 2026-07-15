from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def setup_function():
    activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]


def test_unregistering_a_participant_removes_them_from_the_activity():
    response = client.delete(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
