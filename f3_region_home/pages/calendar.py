import reflex as rx
from f3_region_home.state.home import State
from reflex_calendar import calendar as rx_calendar
from ..layouts import default_layout
from ..database.models import Event


def event_card(event: Event) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.box(
                rx.heading(event.name),
                rx.text(f"Start: {event.start_time}"),
                rx.text(f"Org: {event.org_id}"),
            ),
            direction="column",
            spacing="3",
        ),
    )


def calendar() -> rx.Component:
    # Calendar Page
    return default_layout(
        rx.flex(
            rx.vstack(
                rx_calendar(
                    value=State.selected_date_set,
                    on_change=State.switch_selected_date(),
                ),
                rx.text(f"Selected Date: {State.selected_date_str}"),
                rx.foreach(State.calendar_events, lambda event: event_card(event)),
            ),
        ),
        calendar.__name__,
    )
