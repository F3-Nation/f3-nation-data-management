import reflex as rx
from reflex_calendar import calendar as rx_calendar

# from ..components.calendar import calendar as full_calendar
from ..database.models import Event
from ..layouts import default_layout
from ..state.calendar import CalendarState


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
                    value=CalendarState.selected_date_set,
                    on_change=CalendarState.switch_selected_date(),
                ),
                # full_calendar(
                #     events=CalendarState.events,
                # ),
                rx.text(f"Selected Date: {CalendarState.selected_date_str}"),
                rx.foreach(CalendarState.calendar_events, lambda event: event_card(event)),
                spacing="3",
            ),
        ),
        calendar.__name__,
    )
