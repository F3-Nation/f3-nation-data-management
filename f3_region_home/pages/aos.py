from datetime import datetime

import reflex as rx

from .home import State
from ..components.cards import item_card
from ..database.models import Event, Org
from ..database.queries import EventExtended, OrgSeries
from ..layouts import default_layout


def event_card(event_extended: EventExtended):
    label = f"{event_extended.day_of_week} {event_extended.event_type.name} @ {event_extended.start_time}"
    return item_card(
        state=State,
        item=event_extended.event,
        item_title=event_extended.event.name,
        item_name="event",
        label_component=rx.heading(label),
        form=series_form(),
        thing_label="Series",
    )


def ao_card(org: Org) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.heading(org.name),
            rx.flex(
                rx.icon("pencil"),
                rx.icon("trash-2"),
                direction="row",
                spacing="3",
            ),
            direction="row",
            spacing="3",
        ),
        variant="ghost",
    )


def ao_section(org_series: OrgSeries) -> rx.Component:
    return rx.flex(
        ao_card(org_series.org),
        rx.foreach(
            org_series.series,
            lambda series: event_card(series),
        ),
        add_series_dialog(),
        rx.divider(),
        align="center",
        direction="column",
        spacing="3",
    )


def add_series_card() -> rx.Component:
    return rx.button(
        rx.flex(
            rx.icon("plus"),
            rx.heading("Add Series"),
            direction="row",
            spacing="3",
        ),
        on_click=State.set_add_series_dialog_open(True),
    )


def add_series_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(add_series_card()),
        rx.dialog.content(
            rx.dialog.title("Add Series"),
            series_form(),
        ),
        open=State.add_series_dialog_open,
    )


def aos() -> rx.Component:
    return default_layout(
        rx.flex(
            rx.foreach(
                State.region_data.org_series,
                lambda org_series: ao_section(org_series),
            ),
            direction="column",
            spacing="3",
        ),
        "aos",
    )


def series_form() -> rx.Component:
    return rx.form(
        rx.flex(
            rx.text("AO", weight="bold", align="left"),
            rx.select.root(
                rx.select.trigger(),
                rx.select.content(
                    rx.foreach(State.region_data.orgs, lambda org: rx.select.item(org.name, value=str(org.id))),
                ),
                required=True,
                name="org_id",
            ),
            rx.text("Default Location", weight="bold", align="left"),
            rx.select.root(
                rx.select.trigger(),
                rx.select.content(
                    rx.foreach(
                        State.region_data.locations,
                        lambda location: rx.select.item(location.name, value=str(location.id)),
                    ),
                ),
                required=True,
                name="default_location_id",
            ),
            rx.text("Default Event Type", weight="bold", align="left"),
            rx.select.root(
                rx.select.trigger(),
                rx.select.content(
                    rx.foreach(
                        State.region_data.event_types,
                        lambda event_type: rx.select.item(event_type.name, value=str(event_type.id)),
                    ),
                ),
                required=True,
                name="default_event_type_id",
            ),
            rx.text("Start Date", weight="bold", align="left"),
            rx.input(
                type="date",
                required=True,
                name="start_date",
            ),
            rx.text("End Date", weight="bold", align="left"),
            rx.input(
                type="date",
                required=False,
                name="end_date",
            ),
            rx.text("Start Time", weight="bold", align="left"),
            rx.input(
                type="time",
                required=True,
                name="start_time",
            ),
            rx.flex(
                rx.text("End Time", weight="bold", align="left"),
                rx.text("[Optional]", align="left"),
                direction="row",
                spacing="3",
            ),
            rx.input(
                type="time",
                required=False,
                name="end_time",
            ),
            rx.flex(
                rx.heading("Days of the Week"),
                rx.checkbox("Sunday", name="sunday"),
                rx.checkbox("Monday", name="monday"),
                rx.checkbox("Tuesday", name="tuesday"),
                rx.checkbox("Wednesday", name="wednesday"),
                rx.checkbox("Thursday", name="thursday"),
                rx.checkbox("Friday", name="friday"),
                rx.checkbox("Saturday", name="saturday"),
                direction="column",
                spacing="3",
            ),
            rx.text("Repeats", weight="bold", align="left"),
            rx.radio_group(
                ["Every", "Every Other", "Every Third", "Every Fourth"],
                name="frequency",
            ),
            rx.radio_group(
                ["Week", "Month"],
                name="repeats",
            ),
            rx.text("Index (1st Tuesday of the month, 2nd Tuesday of the month, etc.)", weight="bold", align="left"),
            rx.input(
                type="number",
                name="index",
            ),
            rx.text("Series Name", weight="bold", align="left"),
            rx.input(
                name="name",
            ),
            rx.text("Description", weight="bold", align="left"),
            rx.text_area(
                name="description",
            ),
            rx.checkbox("Highlight on Special Events Page", name="highlight"),
            rx.flex(
                rx.dialog.close(
                    rx.button("Save", type="submit"),
                ),
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                        on_click=State.set_add_series_dialog_open(False),
                    ),
                ),
                direction="row",
                spacing="3",
                justify="end",
            ),
            direction="column",
            spacing="3",
        ),
    )
