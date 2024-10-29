import reflex as rx

from ...layouts import default_layout
from ...state.home import State


def add_location_form() -> rx.Component:
    # Add Location Form
    return default_layout(
        rx.flex(
            rx.card(
                rx.vstack(
                    rx.heading("Add Location"),
                    rx.form(
                        rx.flex(
                            rx.input(placeholder="Location Name", name="name", required=True),
                            rx.input(placeholder="Description", name="description"),
                            rx.input(placeholder="Latitude", name="lat", type="text"),
                            rx.input(placeholder="Longitude", name="lon", type="text"),
                            rx.input(placeholder="Address", name="address_street"),
                            rx.input(placeholder="City", name="address_city"),
                            rx.input(placeholder="State", name="address_state"),
                            rx.input(placeholder="Zip", name="address_zip"),
                            rx.button("Submit", type="submit"),
                            direction="column",
                            spacing="3",
                        ),
                        on_submit=State.handle_submit_add_location,
                        # on_submit=rx.toast.success("Location Added!"),
                    ),
                )
            ),
        ),
        "settings",
    )
