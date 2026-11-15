from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_homepage_returns_html():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "VKHub" in response.text
    assert 'id="url-form"' in response.text
    assert 'id="video-player"' in response.text


def test_homepage_contains_notes_interface():
    response = client.get("/")

    assert response.status_code == 200

    html = response.text

    assert 'id="notes-panel"' in html
    assert 'id="note-form"' in html
    assert 'id="note-timestamp"' in html
    assert 'id="note-text"' in html
    assert 'id="notes-list"' in html
    assert 'id="notes-status"' in html
