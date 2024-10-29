import calendar
import random

import reflex as rx

CALENDAR_MONTHS = list(calendar.month_name)[1:]


class RegionStats(rx.State):
    data: list[dict] = [{"month": m, "total_posts": 0, "unique_pax": 0} for m in CALENDAR_MONTHS]

    def randomize_data(self):
        for i in range(len(self.data)):
            self.data[i]["total_posts"] = random.randint(500, 1000)
            self.data[i]["unique_pax"] = random.randint(100, 200)
