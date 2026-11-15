import pytest

from app.youtube import build_embed_url, build_watch_url, parse_youtube_url


def test_short_url_with_timestamp():
    url = "https://youtu.be/3CZfol4oswE?t=60s"

    result = parse_youtube_url(url)

    assert result == ("3CZfol4oswE", 60)


def test_short_url_without_timestamp():
    url = "https://youtu.be/3CZfol4oswE"

    result = parse_youtube_url(url)

    assert result == ("3CZfol4oswE", 0)


def test_short_url_with_invalid_path():
    url = "https://youtu.be/3CZfol4oswE/extra"

    with pytest.raises(ValueError):
        parse_youtube_url(url)


def test_build_watch_url():
    url = build_watch_url("3CZfol4oswE")

    assert url == ("https://www.youtube.com/watch?v=3CZfol4oswE")


def test_build_watch_url_with_timestamp():
    url = build_watch_url("3CZfol4oswE", 60)

    assert url == ("https://www.youtube.com/watch?v=3CZfol4oswE&t=60s")


def test_different_formats_produce_same_url():
    standard = "https://www.youtube.com/watch?v=3CZfol4oswE&t=60s"
    short = "https://youtu.be/3CZfol4oswE?t=60s"

    standard_data = parse_youtube_url(standard)
    short_data = parse_youtube_url(short)

    assert build_watch_url(*standard_data) == build_watch_url(*short_data)


def test_build_embed_url():
    url = build_embed_url("3CZfol4oswE")

    assert url == ("https://www.youtube-nocookie.com/embed/3CZfol4oswE")


def test_build_embed_url_with_timestamp():
    url = build_embed_url("3CZfol4oswE", 60)

    assert url == ("https://www.youtube-nocookie.com/embed/3CZfol4oswE?start=60")


def test_embed_url_rejects_invalid_timestamp():
    with pytest.raises(ValueError):
        build_embed_url("3CZfol4oswE", -5)
