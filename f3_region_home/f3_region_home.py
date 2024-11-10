"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from .pages import (
    aos,
    calendar,
    home,
    # backblasts,
    # region_stats,
    # new,
    locations,
    settings,
)
from .state.base import BaseState

TAB_LIST = [
    {"label": "Home", "value": "", "load": home},
    {"label": "Locations", "value": "locations", "load": locations},
    {"label": "Schedule", "value": "aos", "load": aos},
    {"label": "Calendar", "value": "calendar", "load": calendar},
    # {"label": "Locations", "value": "locations", "load": locations},
    # {"label": "New to F3?", "value": "new", "load": new},
    # {"label": "Backblasts", "value": "backblasts", "load": backblasts},
    # {"label": "Stats", "value": "stats", "load": region_stats},
    # {"label": "Settings", "value": "settings", "load": settings},
]

style = {
    ".maplibregl-canvas-container": {"minHeight": "400px"},
    "canvas": {"height": "400px"},
    ".mapboxgl-control-container": {"position": "absolute", "bottom": "4px"},
    "pre": {"maxWidth": "calc(100svw - 66px)", "overflowX": "auto"},
}

app = rx.App(style=style)
app.add_page(home, route="/", title="Home", on_load=BaseState.check_login)
app.add_page(locations, route="/locations", title="Locations")
app.add_page(calendar, route="/calendar", title="Calendar")
app.add_page(aos, route="/aos", title="Schedule")
app.add_page(settings, route="/settings", title="Settings")
# for tab in TAB_LIST:
#     app.add_page(tab["load"], route=f"/{tab['value']}", title=tab["label"])
