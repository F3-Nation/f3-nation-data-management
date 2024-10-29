import reflex as rx

from ..components.charts import double_bar_chart
from ..layouts import default_layout
from ..state.stats import RegionStats


def region_stats() -> rx.Component:
    # Stats Page
    return default_layout(
        page=rx.flex(
            rx.heading("Region Stats", size="9"),
            rx.text("Here are some dummy stats, click to randomize!", size="5"),
            double_bar_chart(
                RegionStats.data,
                RegionStats.randomize_data,
                "total_posts",
                "unique_pax",
                "month",
            ),
            justify="center",
            direction="column",
            align="center",
        ),
        tab_name="stats",
    )
