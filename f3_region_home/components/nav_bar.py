import reflex as rx

from ..state.home import REGION_LIST, State

TAB_LIST = [
    {"label": "Home", "value": "home"},
    {"label": "Calendar", "value": "calendar"},
    # {"label": "New to F3?", "value": "new"},
    # {"label": "Backblasts", "value": "backblasts"},
    # {"label": "Stats", "value": "stats"},
    {"label": "Locations", "value": "locations"},
    # {"label": "Settings", "value": "settings"},
    {"label": "AOs", "value": "aos"},
    # {"label": "Series", "value": "series"},
    # {"label": "Events", "value": "events"},
    # {"label": "Event Types", "value": "event_types"},
    # test
]


def nav_bar(tab: str) -> rx.Component:
    # Navigation Bar
    return rx.flex(
        rx.hstack(
            rx.tabs.root(
                rx.tabs.list(
                    rx.foreach(
                        TAB_LIST,
                        lambda tab: rx.tabs.trigger(
                            tab["label"],
                            value=tab["value"],
                            on_click=rx.redirect(f"/{tab['value']}"),
                        ),
                    ),
                ),
                value=tab,
                default_value=tab,
            ),
        ),
        rx.select(
            list(REGION_LIST.keys()),
            placeholder="Select Region",
            value=State.region_name,
            on_change=State.switch_region(),
        ),
        justify="between",
    )
