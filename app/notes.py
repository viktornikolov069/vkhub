from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    start_seconds: int = Field(ge=0)
    text: str = Field(min_length=1, max_length=2000)


class Note(BaseModel):
    id: int
    video_id: str
    start_seconds: int
    text: str


class NoteStore:
    def __init__(self) -> None:
        self._notes: list[Note] = []
        self._next_id = 1

    def add(self, video_id: str, data: NoteCreate) -> Note:
        note = Note(
            id=self._next_id,
            video_id=video_id,
            start_seconds=data.start_seconds,
            text=data.text,
        )
        self._notes.append(note)
        self._next_id += 1
        return note

    def list_for_video(self, video_id: str) -> list[Note]:
        return [note for note in self._notes if note.video_id == video_id]
