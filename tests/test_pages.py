from fastapi.testclient import TestClient

from app.main import app


def test_homepage_uses_jinja2_template():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.template.name == "index.html"
    assert response.context["app_name"] == "Video Knowledge Hub"


def test_homepage_preserves_html_document():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.template.name == "index.html"

    html = response.text.lower()

    assert html.count("<html") == 1
    assert html.count("<head") == 1
    assert html.count("<body") == 1
    assert "video knowledge hub" in html
