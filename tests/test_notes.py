from app.notes import NoteCreate, NoteStore


def test_create_note():
    store = NoteStore()

    data = NoteCreate(
        start_seconds=750,
        text="Explanation of Linux pipes",
    )

    note = store.add("3CZfol4oswE", data)

    assert note.id == 1
    assert note.video_id == "3CZfol4oswE"
    assert note.start_seconds == 750
    assert note.text == "Explanation of Linux pipes"


def test_list_notes_for_video():
    store = NoteStore()

    store.add(
        "3CZfol4oswE",
        NoteCreate(start_seconds=60, text="First note"),
    )

    store.add(
        "M7lc1UVf-VE",
        NoteCreate(start_seconds=120, text="Other video"),
    )

    notes = store.list_for_video("3CZfol4oswE")

    assert len(notes) == 1
    assert notes[0].text == "First note"


def test_note_id_increment():
    store = NoteStore()

    store.add(
        "3CZfol4oswE",
        NoteCreate(start_seconds=60, text="First note"),
    )

    store.add(
        "M7lc1UVf-VE",
        NoteCreate(start_seconds=120, text="Other video"),
    )

    assert len(store._notes) == 2
    assert store._notes[0].id == 1
    assert store._notes[1].id == 2
