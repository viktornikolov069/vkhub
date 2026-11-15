from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_valid_url():
    response = client.post(
        "/api/videos/parse",
        json={"url": "https://www.youtube.com/watch?v=3CZfol4oswE&t=60s"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "video_id": "3CZfol4oswE",
        "start_seconds": 60,
        "video_url": "https://www.youtube.com/watch?v=3CZfol4oswE",
        "playback_url": "https://www.youtube.com/watch?v=3CZfol4oswE&t=60s",
        "embed_url": "https://www.youtube-nocookie.com/embed/3CZfol4oswE?start=60",
    }


def test_rejects_wrong_host():
    response = client.post(
        "/api/videos/parse",
        json={"url": "https://youtube.com.evil.org/watch?v=3CZfol4oswE"},
    )

    assert response.status_code == 400


def test_rejects_invalid_video_id():
    response = client.post(
        "/api/videos/parse",
        json={"url": "https://youtube.com/watch?v=invalid"},
    )

    assert response.status_code == 400


def test_rejects_missing_url():
    response = client.post(
        "/api/videos/parse",
        json={},
    )

    assert response.status_code == 422


def test_api_accepts_short_url():
    response = client.post(
        "/api/videos/parse",
        json={"url": "https://youtu.be/3CZfol4oswE?t=60s"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "video_id": "3CZfol4oswE",
        "start_seconds": 60,
        "video_url": "https://www.youtube.com/watch?v=3CZfol4oswE",
        "playback_url": "https://www.youtube.com/watch?v=3CZfol4oswE&t=60s",
        "embed_url": "https://www.youtube-nocookie.com/embed/3CZfol4oswE?start=60",
    }
