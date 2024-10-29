"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from .pages import (
    # settings,
    add_location_form,
    aos,
    calendar,
    home,
    # backblasts,
    # region_stats,
    # new,
    locations,
)

TAB_LIST = [
    {"label": "Home", "value": "home", "load": home},
    # {"label": "Locations", "value": "locations", "load": locations},
    {"label": "Calendar", "value": "calendar", "load": calendar},
    # {"label": "New to F3?", "value": "new", "load": new},
    # {"label": "Backblasts", "value": "backblasts", "load": backblasts},
    # {"label": "Stats", "value": "stats", "load": region_stats},
    {"label": "Locations", "value": "locations", "load": locations},
    # {"label": "Settings", "value": "settings", "load": settings},
    {"label": "AOs", "value": "aos", "load": aos},
]

style = {
    ".maplibregl-canvas-container": {"minHeight": "400px"},
    "canvas": {"height": "400px"},
    ".mapboxgl-control-container": {"position": "absolute", "bottom": "4px"},
    "pre": {"maxWidth": "calc(100svw - 66px)", "overflowX": "auto"},
}

app = rx.App(style=style)
for tab in TAB_LIST:
    app.add_page(tab["load"], route=f"/{tab['value']}", title=tab["label"])

app.add_page(add_location_form, route="/settings/locations/add", title="Add Location")
