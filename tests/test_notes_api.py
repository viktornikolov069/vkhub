import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.notes import NoteStore

VIDEO_ID = "3CZfol4oswE"


@pytest.fixture
def client():
    app.state.note_store = NoteStore()
    return TestClient(app)


def test_create_and_list_notes(client):
    response = client.post(
        f"/api/videos/{VIDEO_ID}/notes",
        json={
            "start_seconds": 750,
            "text": "Explanation of Linux pipes",
        },
    )

    assert response.status_code == 201

    created_note = response.json()

    assert created_note == {
        "id": 1,
        "video_id": VIDEO_ID,
        "start_seconds": 750,
        "text": "Explanation of Linux pipes",
    }

    response = client.get(f"/api/videos/{VIDEO_ID}/notes")

    assert response.status_code == 200
    assert response.json() == [created_note]


def test_notes_belong_to_specific_video(client):
    client.post(
        f"/api/videos/{VIDEO_ID}/notes",
        json={
            "start_seconds": 60,
            "text": "First note",
        },
    )

    response = client.get("/api/videos/M7lc1UVf-VE/notes")

    assert response.status_code == 200
    assert response.json() == []


def test_negative_timestamp_is_rejected(client):
    response = client.post(
        f"/api/videos/{VIDEO_ID}/notes",
        json={
            "start_seconds": -10,
            "text": "Invalid timestamp",
        },
    )

    assert response.status_code == 422
