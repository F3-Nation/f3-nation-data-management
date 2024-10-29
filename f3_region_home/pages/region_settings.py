import reflex as rx
from ..layouts import default_layout
# from ..state.home import State


def default_setting_button(
    icon_id: str, text: str, page: str, text2: str
) -> rx.Component:
    return rx.button(
        rx.flex(
            rx.icon(icon_id, size=50),
            rx.box(
                rx.heading(text),
                rx.text(text2),
            ),
            spacing="2",
        ),
        on_click=rx.redirect(f"/settings/{page}"),
        variant="ghost",
    )


def default_setting_menu(
    icon_id: str, button_text: str, thing: str, page: str, description: str
) -> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.flex(
                    rx.icon(icon_id, size=50),
                    rx.box(
                        rx.heading(button_text),
                        rx.text(description),
                    ),
                    spacing="2",
                ),
                variant="ghost",
            ),
        ),
        rx.menu.content(
            rx.menu.item(
                f"Add {thing}",
                on_click=rx.redirect(f"/settings/{page}/add"),
            ),
            rx.menu.item(
                f"Edit {thing}",
                on_click=rx.redirect(f"/settings/{page}/edit"),
            ),
            rx.menu.item(
                f"Delete {thing}",
                on_click=rx.redirect(f"/settings/{page}/delete"),
            ),
            align="end",
        ),
    )


def settings() -> rx.Component:
    # Locations Page
    return default_layout(
        rx.flex(
            default_setting_menu(
                "map-pinned",
                "Manage Locations",
                "a Location",
                "locations",
                "Add, Edit, or Delete Locations",
            ),
            default_setting_menu(
                "trees",
                "Manage AOs",
                "an AO",
                "aos",
                "Add, Edit, or Delete AOs",
            ),
            default_setting_menu(
                "calendar-days",
                "Manage Series",
                "a Series",
                "series",
                "Add, Edit, or Delete Series",
            ),
            default_setting_menu(
                "calendar-plus",
                "Manage Single Events",
                "an Event",
                "events",
                "Add, Edit, or Delete Single Events",
            ),
            default_setting_menu(
                "dumbbell",
                "Manage Event Types",
                "an Event Type",
                "event_types",
                "Add, Edit, or Delete Custom Event Types",
            ),
            direction="column",
            spacing="5",
        ),
        settings.__name__,
    )
