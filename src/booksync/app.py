from __future__ import annotations

import sys
from importlib import resources
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from booksync.controllers import StreamController
from booksync.models import StreamModel
from booksync.services import StreamingService


def _default_source() -> list[str]:
    return [f"chunk numéro {i}" for i in range(50)]


def _qml_entry_path() -> Path:
    return Path(resources.files("booksync").joinpath("qml/Main.qml"))


def build_controller() -> StreamController:
    model = StreamModel()
    service = StreamingService(source=_default_source(), delay=0.15)
    return StreamController(model=model, service=service)


def run(argv: list[str] | None = None) -> int:
    app = QGuiApplication(argv if argv is not None else sys.argv)
    engine = QQmlApplicationEngine()

    controller = build_controller()
    controller.setParent(engine)
    engine.rootContext().setContextProperty("controller", controller)

    qml = _qml_entry_path()
    engine.load(str(qml))
    if not engine.rootObjects():
        return 1
    return app.exec()
