import reflex as rx

from ..layouts import default_layout
from ..state.base import BaseState

# def settings() -> rx.Component:
#     # Locations Page
#     return default_layout(
#         rx.flex(
#             rx.flex(
#                 rx.text("Admin Users", size="4"),
#                 rx.container(
#                     rx.foreach(
#                         BaseState.region_data.admin_users,
#                         lambda user: rx.card(
#                             rx.text(user.email),
#                         ),
#                     ),
#                     background_color="var(--gray-3)",
#                     padding="10px",
#                 ),
#                 direction="column",
#                 align="start",
#                 width="80%",
#             ),
#             align="center",
#             direction="column",
#         ),
#         tab_name="settings",
#     )


def create_section_heading(text):
    """Create a section heading with specified styling."""
    return rx.heading(
        text,
        font_weight="600",
        margin_bottom="1.5rem",
        font_size="1.5rem",
        line_height="2rem",
        text_align="center",
        as_="h2",
    )


def create_form_label(label_text):
    """Create a form label with specified styling."""
    return rx.el.label(
        label_text,
        display="block",
        font_weight="500",
        margin_bottom="0.5rem",
        font_size="0.875rem",
        line_height="1.25rem",
    )


def create_delete_icon():
    """Create a delete icon with specified styling."""
    return rx.icon(
        alt="Delete",
        # class_name="dark:text-gray-400",
        tag="trash-2",
        height="1.5rem",
        # color="#6B7280",
        width="1.5rem",
    )


def create_list_item(item_text):
    """Create a list item with hover effects and styling."""
    return rx.el.li(
        item_text,
        # class_name="dark:hover:bg-gray-600",
        cursor="pointer",
        transition_duration="300ms",
        # _hover={"background-color": "#F3F4F6"},
        padding_left="1rem",
        padding_right="1rem",
        padding_top="0.75rem",
        padding_bottom="0.75rem",
        transition_property="color, background-color, border-color, text-decoration-color, fill, stroke",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
    )


def create_horizontal_divider():
    """Create a horizontal divider with flex grow."""
    return rx.box(
        # class_name="dark:border-gray-600",
        # border_color="#D1D5DB",
        border_top_width="1px",
        flex_grow="1",
    )


def create_avatar_image(alt_text, image_src):
    """Create an avatar image with specified styling."""
    return rx.image(
        alt=alt_text,
        src=image_src,
        height="3rem",
        object_fit="cover",
        border_radius="9999px",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        width="3rem",
    )


def create_primary_text(text_content):
    """Create primary text with specified styling."""
    return rx.text(
        text_content,
        font_weight="500",
        font_size="1.125rem",
        line_height="1.75rem",
    )


def create_secondary_text(text_content):
    """Create secondary text with specified styling."""
    return rx.text(
        text_content,
        font_size="0.875rem",
        line_height="1.25rem",
    )


def create_text_container(primary_text, secondary_text):
    """Create a container with primary and secondary text."""
    return rx.box(
        create_primary_text(text_content=primary_text),
        create_secondary_text(text_content=secondary_text),
        margin_left="1rem",
    )


def create_user_info_flex(avatar_alt, avatar_src, name, email):
    """Create a flex container with user avatar and information."""
    return rx.flex(
        create_avatar_image(alt_text=avatar_alt, image_src=avatar_src),
        create_text_container(primary_text=name, secondary_text=email),
        display="flex",
        align_items="center",
    )


def create_delete_button():
    """Create a delete button with hover effects."""
    return rx.el.button(
        create_delete_icon(),
        # class_name="dark:hover:bg-gray-700",
        transition_duration="300ms",
        # _hover={"background-color": "#E5E7EB"},
        padding="0.5rem",
        border_radius="9999px",
        transition_property="color, background-color, border-color, text-decoration-color, fill, stroke",
        transition_timing_function="cubic-bezier(0.4, 0, 0.2, 1)",
    )


def create_user_list_item(avatar_alt, avatar_src, name, email):
    """Create a list item for a user with avatar, info, and delete button."""
    return rx.el.li(
        create_user_info_flex(
            avatar_alt=avatar_alt,
            avatar_src=avatar_src,
            name=name,
            email=email,
        ),
        create_delete_button(),
        display="flex",
        align_items="center",
        justify_content="space-between",
        padding_top="1.5rem",
        padding_bottom="1.5rem",
    )


def create_search_input():
    """Create a search input field with specified styling."""
    return rx.el.input(
        # class_name="dark:bg-gray-700 dark:border-gray-600",
        id="existing-user-search",
        name="existing-user-search",
        placeholder="Search by name or email",
        type="text",
        # background_color="#ffffff",
        # border_color="#D1D5DB",
        _focus={
            "box-shadow": "var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color)",
            "--ring-opacity": "0.5",
        },
        padding_left="2.5rem",
        padding_top="0.75rem",
        padding_bottom="0.75rem",
        border_radius="0.5rem",
        box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
        width="100%",
        on_change=rx.set_value("existing-user-search"),
    )


def create_search_icon():
    """Create a search icon for the search input field."""
    return rx.flex(
        rx.icon(
            alt="Search icon",
            # class_name="dark:text-gray-500",
            tag="search",
            height="1.25rem",
            # color="#9CA3AF",
            width="1.25rem",
        ),
        position="absolute",
        display="flex",
        top="0",
        bottom="0",
        align_items="center",
        left="0",
        padding_left="0.75rem",
        pointer_events="none",
    )


def create_user_list():
    """Create a list of users with specified styling."""
    return rx.list(
        create_list_item(item_text="John Smith (john.smith@example.com)"),
        create_list_item(item_text="Emma Johnson (emma.johnson@example.com)"),
        create_list_item(item_text="Michael Brown (michael.brown@example.com)"),
        create_list_item(item_text="Sarah Davis (sarah.davis@example.com)"),
        create_list_item(item_text="David Wilson (david.wilson@example.com)"),
        # class_name="dark:bg-gray-700 dark:border-gray-600 max-h-60",
        # background_color="#ffffff",
        border_width="1px",
        # border_color="#D1D5DB",
        margin_top="0.5rem",
        overflow="auto",
        border_radius="0.5rem",
        box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    )


def create_or_divider():
    """Create an 'OR' divider with horizontal lines."""
    return rx.flex(
        create_horizontal_divider(),
        rx.text.span(
            "OR",
            # class_name="dark:bg-gray-800",
            # background_color="#ffffff",
            font_weight="500",
            padding_left="1rem",
            padding_right="1rem",
            font_size="0.875rem",
            line_height="1.25rem",
        ),
        create_horizontal_divider(),
        display="flex",
        align_items="center",
        justify_content="center",
    )


def create_email_input():
    """Create an email input field for new user invitation."""
    return rx.input(
        placeholder="Enter email to invite",
        type="email",
        name="new-user-email",
    )
    # rx.el.input(
    #     # class_name="dark:bg-gray-700 dark:border-gray-600",
    #     id="new-user-email",
    #     name="new-user-email",
    #     placeholder="Enter email to invite",
    #     type="email",
    #     # background_color="#ffffff",
    #     # border_color="#D1D5DB",
    #     _focus={
    #         "box-shadow": "var(--tw-ring-inset) 0 0 0 calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color)",
    #         "--ring-opacity": "0.5",
    #     },
    #     padding_top="0.75rem",
    #     padding_bottom="0.75rem",
    #     border_radius="0.5rem",
    #     box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    #     width="100%",
    # )


def create_add_user_button():
    return rx.button(" Add User ")


def create_user_form():
    """Create a form for adding new admin users."""
    return rx.form(
        rx.box(
            create_form_label(label_text="Search Existing User"),
            rx.box(
                create_search_input(),
                create_search_icon(),
                position="relative",
            ),
            create_user_list(),
        ),
        create_or_divider(),
        rx.box(
            create_form_label(label_text="New User Email"),
            create_email_input(),
        ),
        create_add_user_button(),
        display="flex",
        flex_direction="column",
        gap="1.5rem",
    )


def create_add_user_section():
    """Create a section for adding new admin users."""
    return rx.box(
        create_section_heading(text="Add New Admin User"),
        create_user_form(),
        margin_bottom="2rem",
        padding="2rem",
        border_radius="0.75rem",
        box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
        # background_color="var(--gray-3)",
    )


def create_current_admins_section():
    """Create a section displaying current admin users."""
    return rx.box(
        create_section_heading(text="Current Admin Users"),
        rx.list(
            create_user_list_item(
                avatar_alt="John Doe avatar",
                avatar_src="https://replicate.delivery/xezq/G3KrJPw9aOZbJ5OXkd2NCXyamiPAZDYzffX7Z5VkAOS8R7uTA/out-0.webp",
                name="John Doe",
                email="john.doe@example.com",
            ),
            create_user_list_item(
                avatar_alt="Jane Smith avatar",
                avatar_src="https://replicate.delivery/xezq/PxZTlrjnWWLPJBW1a7Oxrr4w82cbdbzXdfaTOeIlf8W5j2dnA/out-0.webp",
                name="Jane Smith",
                email="jane.smith@example.com",
            ),
            create_user_list_item(
                avatar_alt="Robert Johnson avatar",
                avatar_src="https://replicate.delivery/xezq/s3VlIgh9ggqgGlUTFCQC197wL5Q1dYKTC54Tjz0R7zPfod3JA/out-0.webp",
                name="Robert Johnson",
                email="robert.johnson@example.com",
            ),
            # class_name="dark:divide-gray-700",
            # border_color="#E5E7EB",
            border_top_width="1px",
        ),
        # class_name="dark:bg-gray-800",
        # background_color="#ffffff",
        padding="2rem",
        border_radius="0.75rem",
        box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
        # backround_color="var(--gray-3)",
    )


def create_main_content():
    """Create the main content area for admin user management."""
    return rx.box(
        rx.heading(
            "Admin User Management",
            font_weight="700",
            margin_bottom="2rem",
            font_size="2.25rem",
            line_height="2.5rem",
            text_align="center",
            as_="h1",
        ),
        create_add_user_section(),
        create_current_admins_section(),
        width="100%",
        style=rx.breakpoints(
            {
                "640px": {"max-width": "640px"},
                "768px": {"max-width": "768px"},
                "1024px": {"max-width": "1024px"},
                "1280px": {"max-width": "1280px"},
                "1536px": {"max-width": "1536px"},
            }
        ),
        margin_left="auto",
        margin_right="auto",
        padding_left="1rem",
        padding_right="1rem",
        padding_top="2rem",
        padding_bottom="2rem",
    )


def settings():
    """Create the complete admin user management page."""
    return default_layout(
        rx.box(
            create_main_content(),
            width="100%",
        ),
        tab_name="settings",
    )
