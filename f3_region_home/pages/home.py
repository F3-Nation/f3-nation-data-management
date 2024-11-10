import reflex as rx
from reflex_magic_link_auth import MagicLinkAuthState

from ..layouts import default_layout
from ..state.base import BaseState


def login_controls() -> rx.Component:
    return rx.vstack(
        rx.input(name="email", placeholder="Email", type="email", width="100%"),
        # rx.cond(
        #     State.is_prod_mode,
        #     reflex_google_recaptcha_v2.google_recaptcha_v2(),
        # ),
        rx.button("Send Magic Link", width="100%"),
    )


def login_form() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Enter your email to log in", size="8", margin_bottom="10px"),
            rx.cond(
                BaseState.login_error,
                rx.callout.root(
                    rx.callout.text(BaseState.login_error, color="red"),
                    width="100%",
                ),
            ),
            rx.form(
                login_controls(),
                on_submit=BaseState.handle_submit_login,
                on_mount=MagicLinkAuthState.get_base_url,
            ),
            align="center",
        ),
        margin="25px",
    )


def home() -> rx.Component:
    # Welcome Page (Index)
    return rx.cond(
        BaseState.is_hydrated,
        default_layout(
            rx.flex(
                rx.flex(
                    rx.vstack(
                        rx.text(BaseState.region.name, size="4"),
                        rx.heading("Fitness Fellowship Faith", size="9", width="300px"),
                    ),
                    rx.image(
                        "https://f3stlouis.com/wp-content/uploads/elementor/thumbs/F3-St-Louis-logo-transparent-white-1-p064decbfqkzo2gcgrgsa6g9ethgkxfhh44aoca0u0.png"
                    ),
                    align="center",
                    justify="between",
                    width="80%",
                ),
                align="center",
                direction="column",
            ),
            "",
        ),
    )
