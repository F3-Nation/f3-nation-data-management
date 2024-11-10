from datetime import datetime

import reflex as rx

from ..components.cards import item_card
from ..database.queries import EventExtended, OrgExtended, OrgSeries
from ..layouts import default_layout
from ..state.schedule import ScheduleState

# TODO: rename to "schedule"


def aos() -> rx.Component:
    return default_layout(
        rx.flex(
            rx.foreach(
                ScheduleState.region_data.org_series,
                lambda org_series: ao_section(org_series),
            ),
            rx.cond(
                ScheduleState.region is not None,
                rx.cond(
                    ScheduleState.user_is_admin,
                    add_ao_card(),
                    # rx.text("You must be logged in as an admin to manage the schedule."),
                ),
                rx.text("Select a region to view AOs."),
            ),
            add_ao_dialog(),
            edit_ao_dialog(),
            delete_ao_dialog(),
            add_series_dialog(),
            edit_series_dialog(),
            delete_series_dialog(),
            direction="column",
            spacing="3",
            align="center",
        ),
        "aos",
    )


def add_ao_dialog() -> rx.Component:
    return rx.dialog.root(
        # rx.dialog.trigger(add_ao_card()),
        rx.dialog.content(
            rx.dialog.title("Add AO"),
            ao_form(),
        ),
        open=ScheduleState.add_ao_dialog_open,
    )


def edit_ao_dialog() -> rx.Component:
    return rx.dialog.root(
        # rx.dialog.trigger(rx.icon("pencil"), on_click=ScheduleState.set_active_org_id(org.id)),
        rx.dialog.content(
            rx.dialog.title("Edit AO"),
            ao_form(),
        ),
        open=ScheduleState.edit_ao_dialog_open,
    )


def delete_ao_dialog() -> rx.Component:
    return rx.alert_dialog.root(
        # rx.alert_dialog.trigger(rx.icon("trash-2")),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Delete AO"),
            rx.alert_dialog.description(f"Are you sure you want to delete {ScheduleState.active_org.name}?"),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button("Cancel", variant="soft", color_scheme="gray", on_click=ScheduleState.cancel_ao_form),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Delete",
                        variant="solid",
                        color_scheme="red",
                        on_click=ScheduleState.handle_delete_org,
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
        open=ScheduleState.delete_ao_dialog_open,
    )


def add_ao_card() -> rx.Component:
    return rx.button(
        rx.flex(
            rx.icon("plus"),
            rx.heading("Add AO"),
            direction="row",
            spacing="3",
        ),
        on_click=ScheduleState.set_add_ao_dialog_open(True),
    )


def ao_section(org_series: OrgSeries) -> rx.Component:
    return rx.flex(
        ao_card(org_series.org),
        rx.foreach(
            org_series.series,
            lambda series: event_card(series),
        ),
        rx.cond(
            ScheduleState.user_is_admin,
            add_series_dialog(),
        ),
        rx.divider(),
        align="center",
        direction="column",
        spacing="3",
    )


def ao_card(org: OrgExtended) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.heading(org.name),
            rx.cond(
                ScheduleState.user_is_admin,
                rx.flex(
                    # rx.icon("pencil", on_click=ScheduleState.edit_ao_trigger(org)),
                    rx.icon("pencil", on_click=ScheduleState.edit_ao_trigger(org)),
                    rx.icon("trash-2", on_click=ScheduleState.delete_ao_trigger(org)),
                    direction="row",
                    spacing="3",
                ),
            ),
            direction="row",
            spacing="3",
        ),
        variant="ghost",
    )


def event_card(event_extended: EventExtended):
    label = f"{event_extended.day_of_week} {event_extended.event_type.name} @ {event_extended.start_time}"
    # return item_card(
    #     state=ScheduleState,
    #     item=event_extended.event,
    #     item_title=event_extended.event.name,
    #     item_name="event",
    #     label_component=rx.heading(label),
    #     form=series_form(),
    #     thing_label="Series",
    #     admin=ScheduleState.user_is_admin,
    # )
    return rx.card(
        rx.flex(
            rx.heading(label),
            rx.cond(
                ScheduleState.user_is_admin,
                rx.flex(
                    rx.icon("pencil", on_click=ScheduleState.edit_series_trigger(event_extended)),
                    rx.icon("trash-2", on_click=ScheduleState.delete_series_trigger(event_extended)),
                    direction="row",
                    spacing="3",
                ),
            ),
            direction="row",
            spacing="3",
        ),
        # variant="ghost",
    )


def add_series_dialog() -> rx.Component:
    return rx.dialog.root(
        # rx.dialog.trigger(add_series_card()),
        rx.dialog.content(
            rx.dialog.title("Add Series"),
            series_form(),
        ),
        open=ScheduleState.add_series_dialog_open,
    )


def edit_series_dialog() -> rx.Component:
    return rx.dialog.root(
        # rx.dialog.trigger(rx.icon("pencil"), on_click=ScheduleState.set_active_org_id(org.id)),
        rx.dialog.content(
            rx.dialog.title("Edit Series"),
            series_form(),
        ),
        open=ScheduleState.edit_series_dialog_open,
    )


def delete_series_dialog() -> rx.Component:
    return rx.alert_dialog.root(
        # rx.alert_dialog.trigger(rx.icon("trash-2")),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Delete series"),
            rx.alert_dialog.description(f"Are you sure you want to delete {ScheduleState.active_series.name}?"),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button("Cancel", variant="soft", color_scheme="gray", on_click=ScheduleState.cancel_series_form),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Delete",
                        variant="solid",
                        color_scheme="red",
                        on_click=ScheduleState.handle_delete_series,
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
        open=ScheduleState.delete_series_dialog_open,
    )


def add_series_card() -> rx.Component:
    return rx.button(
        rx.flex(
            rx.icon("plus"),
            rx.heading("Add Series"),
            direction="row",
            spacing="3",
        ),
        on_click=ScheduleState.set_add_series_dialog_open(True),
    )


def series_form() -> rx.Component:
    return rx.form(
        rx.flex(
            rx.text("AO", weight="bold", align="left"),
            rx.select.root(
                rx.select.trigger(),
                rx.select.content(
                    rx.foreach(ScheduleState.region_data.orgs_select, lambda org: rx.select.item(org[0], value=org[1])),
                ),
                required=True,
                name="org_id",
                default_value=rx.Var.to_string(ScheduleState.active_series.org_id),
            ),
            rx.text("Default Location", weight="bold", align="left"),
            rx.select.root(
                rx.select.trigger(),
                rx.select.content(
                    rx.foreach(
                        ScheduleState.region_data.locations_select,
                        lambda location: rx.select.item(location[0], value=location[1]),
                    ),
                ),
                required=True,
                name="location_id",
                default_value=rx.Var.to_string(ScheduleState.active_series.location_id),
            ),
            rx.text("Default Event Type", weight="bold", align="left"),
            rx.select.root(
                rx.select.trigger(),
                rx.select.content(
                    rx.foreach(
                        ScheduleState.region_data.event_types_select,
                        lambda event_type: rx.select.item(event_type[0], value=event_type[1]),
                    ),
                ),
                required=True,
                name="event_type_id",
                default_value=rx.Var.to_string(ScheduleState.active_series.event_type_id),
            ),
            rx.flex(
                rx.text("Start Date", weight="bold", align="left"),
                rx.input(
                    type="date",
                    required=True,
                    name="start_date",
                ),
                rx.flex(
                    rx.text("End Date", weight="bold", align="left"),
                    rx.text("[Optional]", align="left"),
                    direction="row",
                    spacing="1",
                ),
                rx.input(
                    type="date",
                    required=False,
                    name="end_date",
                ),
                direction="row",
                spacing="3",
                align="center",
            ),
            rx.flex(
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
                    spacing="1",
                ),
                rx.input(
                    type="time",
                    required=False,
                    name="end_time",
                ),
                direction="row",
                spacing="3",
                align="center",
            ),
            rx.flex(
                rx.heading("Days of the Week"),
                rx.checkbox("Sunday", name="Sunday"),
                rx.checkbox("Monday", name="Monday"),
                rx.checkbox("Tuesday", name="Tuesday"),
                rx.checkbox("Wednesday", name="Wednesday"),
                rx.checkbox("Thursday", name="Thursday"),
                rx.checkbox("Friday", name="Friday"),
                rx.checkbox("Saturday", name="Saturday"),
                direction="column",
                spacing="3",
            ),
            rx.text("Repeats", weight="bold", align="left"),
            rx.radio_group(
                ["Every", "Every Other", "Every Third", "Every Fourth"],
                name="recurrence_interval",
            ),
            rx.radio_group(
                ["Week", "Month"],
                name="recurrence_pattern",
            ),
            rx.text("Index (1st Tuesday of the month, 2nd Tuesday of the month, etc.)", weight="bold", align="left"),
            rx.input(
                type="number",
                name="index_within_interval",
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
                        on_click=ScheduleState.cancel_series_form,
                    ),
                ),
                direction="row",
                spacing="3",
                justify="end",
            ),
            direction="column",
            spacing="3",
        ),
        on_submit=ScheduleState.handle_submit_add_series,
    )


def ao_form() -> rx.Component:
    return rx.form(
        rx.flex(
            rx.text("AO Name", weight="bold", align="left"),
            rx.input(
                placeholder="AO Name",
                name="name",
                required=True,
                default_value=getattr(ScheduleState.active_org, "name", ""),
            ),
            rx.text("Description", weight="bold", align="left"),
            rx.text_area(
                placeholder="Description",
                name="description",
                required=False,
                default_value=getattr(ScheduleState.active_org, "description", ""),
            ),
            rx.text("Default Location", weight="bold", align="left"),
            rx.select.root(
                rx.select.trigger(),
                rx.select.content(
                    rx.foreach(
                        ScheduleState.region_data.locations_select,
                        lambda location: rx.select.item(location[0], value=location[1]),
                    ),
                ),
                required=False,
                name="default_location_id",
                default_value=getattr(ScheduleState.active_org, "default_location_id_str", ""),  # this is not respected
            ),
            # rx.text("Default Event Type", weight="bold", align="left"),
            # rx.select.root(
            #     rx.select.trigger(),
            #     rx.select.content(
            #         rx.foreach(
            #             BaseState.region_data.event_types,
            #             lambda event_type: rx.select.item(event_type.name, value=str(event_type.id)),
            #         ),
            #     ),
            #     required=False,
            #     name="event_type_id",
            # ),
            # rx.text("AO Logo", weight="bold", align="left"),
            # rx.upload(),
            rx.flex(
                rx.dialog.close(
                    rx.button("Save", type="submit"),
                ),
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                        type="button",
                        on_click=ScheduleState.cancel_ao_form,
                    ),
                ),
                direction="row",
                spacing="3",
                justify="end",
            ),
            direction="column",
            spacing="3",
        ),
        on_submit=ScheduleState.handle_submit_ao_form,
    )
