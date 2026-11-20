from fastapi.testclient import TestClient
from html.parser import HTMLParser

from app.main import app

class TagCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)


def test_notes_preview_returns_html_fragment():
    with TestClient(app) as client:
        response = client.get("/ui/notes/preview")

    parser = TagCollector()
    parser.feed(response.text)

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert response.template.name == (
        "partials/notes_preview.html"
    )
    assert "Notes panel loaded successfully." in response.text
    assert parser.tags.count("html") == 0