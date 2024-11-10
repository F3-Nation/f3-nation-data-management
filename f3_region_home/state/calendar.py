import re
from datetime import datetime, timedelta

import reflex as rx

from .base import BaseState
from ..database.models import Event

# from ..components.calendar import calendar


class CalendarState(BaseState):
    selected_date: datetime = datetime.today()
    calendar_events: list[Event] = []

    def _reformat_date(self, date_str: str) -> datetime:
        date_str = date_str.replace(".toDateString()", "").strip()
        date_str = re.sub(r"\s*\(.*\)$", "", date_str)
        date_format = "%a %b %d %Y %H:%M:%S GMT%z"
        return datetime.strptime(date_str, date_format)

    @rx.var
    def selected_date_str(self) -> str:
        date_format = "%Y-%m-%d"
        return datetime.strftime(self.selected_date, date_format)

    @rx.var
    def selected_date_set(self) -> str:
        return (self.selected_date + timedelta(1)).strftime("%Y-%m-%d")

    def switch_selected_date(self, date_str: str):
        self.selected_date = self._reformat_date(date_str)
        self.calendar_events = Event.get_week(region_id=self.region.id, start_date=self.selected_date)
        yield
