"""Entry point:  python main.py   ->  http://localhost:8080"""
from nicegui import ui

import gui  # noqa: F401  (registers the page)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="Fitness Activity Summary", reload=False, show=True)
