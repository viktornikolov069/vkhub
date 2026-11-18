from app.main import templates


def test_site_header_renders_application_name():
    template = templates.env.get_template(
        "partials/site_header.html"
    )

    html = template.render(app_name="Test Hub")

    assert "<h1>Test Hub</h1>" in html