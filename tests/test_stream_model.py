from PySide6.QtCore import Qt

from booksync.models import StreamModel
from booksync.services import StreamChunk


def test_model_is_initially_empty(qtbot):
    model = StreamModel()
    assert model.rowCount() == 0


def test_append_chunk_increases_row_count(qtbot):
    model = StreamModel()
    model.append(StreamChunk(id=0, content="hi"))
    assert model.rowCount() == 1


def test_model_exposes_content_via_role(qtbot):
    model = StreamModel()
    model.append(StreamChunk(id=0, content="hello"))
    index = model.index(0, 0)
    role = StreamModel.ContentRole
    assert model.data(index, role) == "hello"
    assert model.data(index, Qt.DisplayRole) == "hello"


def test_role_names_exposed_to_qml(qtbot):
    model = StreamModel()
    roles = {bytes(v).decode(): k for k, v in model.roleNames().items()}
    assert "content" in roles
    assert "chunkId" in roles


def test_clear_resets_model(qtbot):
    model = StreamModel()
    model.append(StreamChunk(id=0, content="a"))
    model.append(StreamChunk(id=1, content="b"))
    model.clear()
    assert model.rowCount() == 0
