import re
from urllib.parse import parse_qs, urlencode, urlsplit

# https://youtu.be/3CZfol4oswE?t=60s'


def parse_youtube_url(url: str) -> tuple[str, int]:
    parts = urlsplit(url)

    if parts.scheme != "https":
        raise ValueError("Only HTTPS YouTube watch URLs are supported")

    host = parts.netloc.lower()
    params = parse_qs(parts.query, keep_blank_values=True)

    if host in {"youtube.com", "www.youtube.com"}:
        if parts.path != "/watch":
            raise ValueError("Unsupported YouTube path")

        video_ids = params.get("v", [])

    elif host == "youtu.be":
        video_ids = [parts.path.removeprefix("/")]

    else:
        raise ValueError("Unsupported YouTube hostname")

    if len(video_ids) != 1 or not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_ids[0]):
        raise ValueError("Invalid video ID")

    times = params.get("t", ["0"])

    if len(times) != 1 or not re.fullmatch(r"\d+s?", times[0]):
        raise ValueError("Timestamp must be in seconds (e.g. 60s)")

    return video_ids[0], int(times[0].removesuffix("s"))


def build_watch_url(video_id: str, start_seconds: int = 0) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        raise ValueError("Invalid video ID")

    if start_seconds < 0:
        raise ValueError("Timestamp cannot be negative")

    params = {"v": video_id}

    if start_seconds > 0:
        params["t"] = f"{start_seconds}s"

    query = urlencode(params)

    return f"https://www.youtube.com/watch?{query}"


def build_embed_url(video_id: str, start_seconds: int = 0) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        raise ValueError("Invalid video ID")

    if start_seconds < 0:
        raise ValueError("Timestamp cannot be negative")

    base_url = f"https://www.youtube-nocookie.com/embed/{video_id}"

    if start_seconds > 0:
        return f"{base_url}?start={start_seconds}"

    return base_url
