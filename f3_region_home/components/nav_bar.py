import reflex as rx

from ..state.auth import AuthState
from ..state.base import REGION_LIST, BaseState

TAB_LIST = [
    {"label": "Home", "value": ""},
    {"label": "Locations", "value": "locations"},
    {"label": "Schedule", "value": "aos"},
    {"label": "Calendar", "value": "calendar"},
    # {"label": "New to F3?", "value": "new"},
    # {"label": "Backblasts", "value": "backblasts"},
    # {"label": "Stats", "value": "stats"},
    # {"label": "Settings", "value": "settings"},
    # {"label": "Event Types", "value": "event_types"},
    # test
]


def nav_bar(tab: str) -> rx.Component:
    # Navigation Bar
    return rx.flex(
        rx.hstack(
            rx.tabs.root(
                rx.tabs.list(
                    rx.foreach(
                        TAB_LIST,
                        lambda tab: rx.tabs.trigger(
                            tab["label"],
                            value=tab["value"],
                            on_click=rx.redirect(f"/{tab['value']}"),
                        ),
                    ),
                ),
                value=tab,
                default_value=tab,
            ),
        ),
        rx.flex(
            rx.select.root(
                rx.select.trigger(),
                rx.select.content(
                    rx.foreach(
                        BaseState.region_list,
                        lambda region: rx.select.item(region[0], value=region[1]),
                    ),
                ),
                placeholder="Select Region",
                value=BaseState.region_id_str,
                on_change=BaseState.switch_region,
            ),
            login_dialog(),
            rx.cond(
                BaseState.user_is_admin,
                rx.icon("settings", on_click=rx.redirect("/settings")),
            ),
            rx.theme_panel(),
            spacing="5",
            direction="row",
            align="center",
        ),
        justify="between",
    )


def login_dialog() -> rx.Component:
    return rx.popover.root(
        rx.popover.trigger(
            # rx.tooltip(
            #     rx.box(
            #         rx.avatar(
            #             src=AuthState.user.avatar_url,
            #             fallback="F3",
            #             color_scheme="gray",
            #             variant="soft",
            #             high_contrast=False,
            #             on_click=AuthState.set_login_dialog_open(True),
            #         ),
            #     ),
            #     content="Login",
            # ),
            rx.avatar(
                src=AuthState.user.avatar_url,
                fallback="F3",
                color_scheme="gray",
                variant="soft",
                high_contrast=False,
                on_click=AuthState.set_login_dialog_open(True),
            ),
        ),
        rx.cond(
            BaseState.logged_in,
            rx.popover.content(
                # rx.dialog.title("Profile"),
                # rx.dialog.description(f"Welcome, {BaseState.user.f3_name}!"),
                rx.flex(
                    rx.avatar(
                        src=BaseState.user.avatar_url,
                        color_scheme="gray",
                        variant="soft",
                        high_contrast=False,
                        size="9",
                    ),
                    rx.text(f"@{BaseState.user.f3_name}", weight="bold"),
                    rx.popover.close(rx.button("Logout", on_click=BaseState.full_logout)),
                    direction="column",
                    align="center",
                    spacing="1",
                ),
            ),
            rx.popover.content(
                # rx.dialog.title("Login"),
                # rx.dialog.description("Please login to continue", margin_bottom="16px"),
                rx.flex(
                    rx.cond(
                        BaseState.awaiting_otp,
                        rx.link("Magic Link!", href=AuthState.magic_link),
                        rx.text("Enter your email to log in"),
                    ),
                    rx.form(
                        rx.flex(
                            # rx.text("Email", weight="bold", align="left"),
                            # rx.input(value=AuthState.email, type="email", on_change=AuthState.set_email),
                            rx.input(name="email", placeholder="Email", type="email"),
                            rx.button("Send Magic Link"),
                            # rx.text("Password", weight="bold", align="left"),
                            # rx.input(value=AuthState.password, type="password", on_change=AuthState.set_password),
                            spacing="3",
                            direction="column",
                        ),
                        on_submit=BaseState.handle_submit_login,
                        on_mount=AuthState.get_base_url,
                    ),
                    rx.flex(
                        rx.popover.close(
                            rx.button("Cancel", variant="soft", color_scheme="gray"),
                        ),
                        # rx.popover.close(
                        #     rx.button("Login", on_click=AuthState.login()),
                        # ),
                        spacing="2",
                        direction="row",
                        justify="end",
                    ),
                    direction="column",
                    spacing="3",
                ),
                # rx.flex(
                #     rx.popover.close(
                #         rx.button("Cancel", variant="soft", color_scheme="gray"),
                #     ),
                #     rx.popover.close(
                #         rx.button("Login", on_click=AuthState.login()),
                #     ),
                #     spacing="3",
                #     direction="row",
                #     justify="end",
                #     margin_top="16px",
                # ),
            ),
        ),
        # rx.popover.close(rx.button("Close")),
        # open=AuthState.login_dialog_open,
        # on_mouse_over=AuthState.show_tooltip,
    )
