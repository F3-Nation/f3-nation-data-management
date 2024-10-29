import reflex as rx

from ..components import nav_bar


def default_layout(page: rx.Component, tab_name: str) -> rx.Component:
    return rx.container(
        nav_bar(tab=tab_name),
        rx.color_mode.button(position="bottom-right"),
        rx.flex(
            page,
            spacing="5",
            justify="center",
            min_height="85vh",
            align="center",
            # width="100%",
        ),
        rx.logo(),
    )
