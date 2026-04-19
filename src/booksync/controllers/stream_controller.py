from __future__ import annotations

import asyncio

from PySide6.QtCore import (
    Property,
    QObject,
    QThread,
    Signal,
    Slot,
)

from booksync.models import StreamModel
from booksync.services import StreamChunk, StreamingService


class _StreamWorker(QObject):
    """Runs the async streaming loop in its own thread."""

    chunkArrived = Signal(int, str)
    done = Signal()

    def __init__(self, service: StreamingService) -> None:
        super().__init__()
        self._service = service

    @Slot()
    def run(self) -> None:
        try:
            asyncio.run(self._consume())
        finally:
            self.done.emit()

    async def _consume(self) -> None:
        async for chunk in self._service.stream():
            self.chunkArrived.emit(chunk.id, chunk.content)


class StreamController(QObject):
    """Bridges `StreamingService` and `StreamModel` for QML."""

    started = Signal()
    finished = Signal()
    runningChanged = Signal()

    def __init__(
        self,
        model: StreamModel,
        service: StreamingService,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._model = model
        self._service = service
        self._thread: QThread | None = None
        self._worker: _StreamWorker | None = None
        self._running = False

    @Property(QObject, constant=True)
    def model(self) -> StreamModel:  # noqa: D401
        return self._model

    def _get_running(self) -> bool:
        return self._running

    running = Property(bool, fget=_get_running, notify=runningChanged)

    @Slot()
    def start(self) -> None:
        if self._running:
            return
        self._model.clear()
        self._thread = QThread()
        self._worker = _StreamWorker(self._service)
        self._worker.moveToThread(self._thread)
        self._thread.started.connect(self._worker.run)
        self._worker.chunkArrived.connect(self._on_chunk)
        self._worker.done.connect(self._on_done)
        self._set_running(True)
        self.started.emit()
        self._thread.start()

    @Slot()
    def stop(self) -> None:
        self._service.stop()

    @Slot(int, str)
    def _on_chunk(self, chunk_id: int, content: str) -> None:
        self._model.append(StreamChunk(id=chunk_id, content=content))

    @Slot()
    def _on_done(self) -> None:
        if self._thread is not None:
            self._thread.quit()
            self._thread.wait()
            self._thread.deleteLater()
            self._thread = None
        if self._worker is not None:
            self._worker.deleteLater()
            self._worker = None
        self._set_running(False)
        self.finished.emit()

    def _set_running(self, value: bool) -> None:
        if self._running != value:
            self._running = value
            self.runningChanged.emit()
