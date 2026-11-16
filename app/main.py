from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Request
from fastapi import Path as PathParam
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.notes import Note, NoteCreate, NoteStore
from app.youtube import (
    build_embed_url,
    build_watch_url,
    parse_youtube_url,
)

app = FastAPI(title="VKHub")
app.state.note_store = NoteStore()

# Configure Jinja2
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class ParseRequest(BaseModel):
    url: str


class ParseResponse(BaseModel):
    video_id: str
    start_seconds: int
    video_url: str
    playback_url: str
    embed_url: str


@app.post("/api/videos/parse", response_model=ParseResponse)
def parse_video(request: ParseRequest) -> ParseResponse:
    try:
        video_id, start_seconds = parse_youtube_url(request.url)

        return ParseResponse(
            video_id=video_id,
            start_seconds=start_seconds,
            video_url=build_watch_url(video_id),
            playback_url=build_watch_url(video_id, start_seconds),
            embed_url=build_embed_url(video_id, start_seconds),
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


# TODO: To be removed
# @app.get("/", response_class=FileResponse)
# def homepage() -> FileResponse:
#     file_path = Path(__file__).resolve().parent / "static" / "index.html"
#     return FileResponse(file_path)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"app_name": "Video Knowledge Hub"},
    )


VideoId = Annotated[
    str,
    PathParam(pattern=r"^[A-Za-z0-9_-]{11}$"),
]


@app.post(
    "/api/videos/{video_id}/notes",
    response_model=Note,
    status_code=201,
)
def create_note(video_id: VideoId, payload: NoteCreate) -> Note:
    return app.state.note_store.add(video_id, payload)


@app.get(
    "/api/videos/{video_id}/notes",
    response_model=list[Note],
)
def list_notes(video_id: VideoId) -> list[Note]:
    return app.state.note_store.list_for_video(video_id)
