from __future__ import annotations

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt

from booksync.services import StreamChunk


class StreamModel(QAbstractListModel):
    ContentRole = Qt.UserRole + 1
    IdRole = Qt.UserRole + 2

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._chunks: list[StreamChunk] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # noqa: N802
        if parent.isValid():
            return 0
        return len(self._chunks)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._chunks)):
            return None
        chunk = self._chunks[index.row()]
        if role in (Qt.DisplayRole, self.ContentRole):
            return chunk.content
        if role == self.IdRole:
            return chunk.id
        return None

    def roleNames(self):  # noqa: N802
        return {
            self.ContentRole: b"content",
            self.IdRole: b"chunkId",
        }

    def append(self, chunk: StreamChunk) -> None:
        row = len(self._chunks)
        self.beginInsertRows(QModelIndex(), row, row)
        self._chunks.append(chunk)
        self.endInsertRows()

    def clear(self) -> None:
        if not self._chunks:
            return
        self.beginResetModel()
        self._chunks.clear()
        self.endResetModel()
