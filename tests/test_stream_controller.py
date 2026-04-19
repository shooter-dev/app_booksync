import pytest

from booksync.controllers import StreamController
from booksync.models import StreamModel
from booksync.services import StreamingService


def test_controller_exposes_model(qtbot):
    model = StreamModel()
    service = StreamingService(source=[], delay=0)
    controller = StreamController(model=model, service=service)
    assert controller.model is model


def test_start_populates_model(qtbot):
    model = StreamModel()
    service = StreamingService(source=["x", "y"], delay=0)
    controller = StreamController(model=model, service=service)

    with qtbot.waitSignal(controller.finished, timeout=2000):
        controller.start()

    assert model.rowCount() == 2


def test_running_property_toggles(qtbot):
    model = StreamModel()
    service = StreamingService(source=["x"], delay=0)
    controller = StreamController(model=model, service=service)

    assert controller.running is False
    with qtbot.waitSignal(controller.finished, timeout=2000):
        controller.start()
    assert controller.running is False


def test_stop_interrupts_stream(qtbot):
    model = StreamModel()
    service = StreamingService(source=list("abcdefgh"), delay=0.05)
    controller = StreamController(model=model, service=service)

    controller.start()
    qtbot.wait(60)
    controller.stop()

    with qtbot.waitSignal(controller.finished, timeout=2000):
        pass

    assert model.rowCount() < 8
