import reflex as rx


def set_active_id(state_object: rx.State, model_name: str, id: int):
    method = getattr(state_object, f"set_active_{model_name}_id")
    return method(id)


def item_card(
    state: rx.State,
    item: rx.Model,
    item_title: str,
    item_name: str,
    label_component: rx.Component,
    form: rx.Component,
    thing_label: str,
    admin: bool = False,
) -> rx.Component:
    return rx.card(
        rx.flex(
            label_component,
            rx.cond(
                admin,
                rx.flex(
                    edit_item_dialog(state, item, item_name, form, thing_label),
                    delete_item_dialog(state, item, item_title, item_name, thing_label),
                    direction="row",
                    spacing="3",
                ),
            ),
            justify="between",
            direction="row",
            spacing="3",
        ),
    )


def delete_item_dialog(
    state: rx.State, item: rx.Model, item_title: str, item_name: str, thing_label: str
) -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(rx.icon("trash-2")),
        rx.alert_dialog.content(
            rx.alert_dialog.title(f"Delete {thing_label}"),
            rx.alert_dialog.description(f"Are you sure you want to delete {item_title}?"),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button("Cancel", variant="soft", color_scheme="gray"),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Delete",
                        variant="solid",
                        color_scheme="red",
                        on_click=getattr(state, f"handle_delete_{item_name}"),
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
        on_open_change=getattr(state, f"set_active_{item_name}")(item),
    )


def edit_item_dialog(
    state: rx.State, item: rx.Model, item_name: str, form: rx.Component, thing_label: str
) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.icon("pencil")),
        rx.dialog.content(
            rx.dialog.title(f"Edit {thing_label}"),
            form,
        ),
        on_open_change=getattr(state, f"set_active_{item_name}")(item),
    )
