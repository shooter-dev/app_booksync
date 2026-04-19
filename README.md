# booksync

Squelette d'application **PySide6 + QML** avec streaming de données, construit en **TDD**.

## Architecture

```
src/booksync/
├── __main__.py          # Point d'entrée
├── app.py               # Démarrage QGuiApplication + QQmlApplicationEngine
├── models/
│   └── stream_model.py  # QAbstractListModel pour la vue QML
├── services/
│   └── streaming_service.py  # Producteur de données (async, indépendant de Qt)
├── controllers/
│   └── stream_controller.py  # QObject exposé à QML, orchestre service ↔ model
└── qml/
    └── Main.qml         # Interface

tests/
├── test_streaming_service.py
├── test_stream_model.py
└── test_stream_controller.py
```

## Cycle TDD

1. **Red** — écrire un test qui échoue (`pytest`).
2. **Green** — écrire le minimum pour passer.
3. **Refactor** — nettoyer sans casser les tests.

La logique métier (`services/`) est **découplée de Qt** pour être testable sans GUI.
Les adaptateurs Qt (`models/`, `controllers/`) sont testés via `pytest-qt`.

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
```

## Lancer

```bash
python -m booksync
```

## Tester

```bash
pytest
```
