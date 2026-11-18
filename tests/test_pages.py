from html.parser import HTMLParser

from fastapi.testclient import TestClient

from app.main import app


class TagCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)


def test_homepage_uses_jinja2_template():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.template.name == "index.html"
    assert response.context["app_name"] == "VKHub"


def test_homepage_preserves_html_document():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200

    parser = TagCollector()
    parser.feed(response.text)

    assert parser.tags.count("html") == 1
    assert parser.tags.count("head") == 1
    assert parser.tags.count("body") == 1
    assert parser.tags.count("header") == 1

    assert "<h1>VKHub</h1>" in response.text
