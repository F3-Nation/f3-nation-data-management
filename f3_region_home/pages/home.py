import reflex as rx

from f3_region_home.state.home import State

from ..layouts import default_layout


def home() -> rx.Component:
    # Welcome Page (Index)
    return default_layout(
        rx.flex(
            rx.flex(
                rx.vstack(
                    rx.text(State.region_name, size="4"),
                    rx.heading("Fitness Fellowship Faith", size="9", width="300px"),
                ),
                rx.image(
                    "https://f3stlouis.com/wp-content/uploads/elementor/thumbs/F3-St-Louis-logo-transparent-white-1-p064decbfqkzo2gcgrgsa6g9ethgkxfhh44aoca0u0.png"
                ),
                align="center",
                justify="between",
                width="80%",
            ),
        ),
        home.__name__,
    )
