import reflex as rx


def double_bar_chart(
    data: list[dict], on_click, left_y: str, right_y: str, x: str
) -> rx.Component:
    left_y_label = left_y.replace("_", " ").title()
    right_y_label = right_y.replace("_", " ").title()

    return rx.recharts.bar_chart(
        rx.recharts.bar(
            data_key=left_y,
            stroke=rx.color("accent", 9),
            fill=rx.color("accent", 8),
            x_axis_id="primary",
            y_axis_id="left",
            name=left_y_label,
        ),
        rx.recharts.bar(
            data_key=right_y,
            stroke=rx.color("green", 9),
            fill=rx.color("green", 8),
            x_axis_id="primary",
            y_axis_id="left",
            name=right_y_label,
        ),
        rx.recharts.x_axis(data_key=x, x_axis_id="primary"),
        rx.recharts.y_axis(data_key=left_y, y_axis_id="left"),
        # rx.recharts.y_axis(data_key=right_y, orientation="right", y_axis_id="right"),
        rx.recharts.graphing_tooltip(),
        rx.recharts.legend(),
        on_click=on_click,
        data=data,
        width=600,
        height=300,
    )
