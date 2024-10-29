import reflex as rx

from ..layouts import default_layout


def backblasts() -> rx.Component:
    # Backblasts Page
    return default_layout(
        rx.flex(
            rx.heading("Backblasts", size="9"),
            rx.text("Coming soon...", size="5"),
            justify="center",
            direction="column",
        ),
        backblasts.__name__,
    )
