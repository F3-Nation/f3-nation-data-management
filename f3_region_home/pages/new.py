import reflex as rx

from ..layouts import default_layout


def new() -> rx.Component:
    # New to F3 Page
    return default_layout(
        rx.flex(
            rx.heading("New to F3?", size="9"),
            rx.text("F3 is a national network of free, peer led workouts", size="5"),
            justify="center",
            direction="column",
        ),
        new.__name__,
    )
