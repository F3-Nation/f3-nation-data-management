from datetime import datetime, timedelta

import reflex as rx

from .base import BaseState
from ..constants import DAYS_OF_WEEK, INTERVAL_MAP, RECURRENCE_MAP
from ..database.db_manager import DbManager
from ..database.models import Event, Org
from ..database.queries import EventExtended, OrgExtended, RegionData
from ..utilities import clear_form_blanks, safe_get_convert


class ScheduleState(BaseState):
    add_series_dialog_open: bool = False
    edit_series_dialog_open: bool = False
    delete_series_dialog_open: bool = False
    active_series: Event = None
    add_ao_dialog_open: bool = False
    edit_ao_dialog_open: bool = False
    delete_ao_dialog_open: bool = False
    active_org: OrgExtended = None

    def handle_add_series(self, org: Org):
        self.active_org_id = org.id
        self.add_series_dialog_open = True

    def handle_submit_edit_event(self, form_data: dict):
        pass

    def handle_delete_series(self):
        pass

    def handle_delete_org(self):
        Org.deactivate(self.active_org_id)
        self.active_org = None
        self.region_data = RegionData(self.region.id)

    def handle_submit_ao_form(self, form_data: dict[str, str]):
        for key, value in form_data.items():
            if value == "":
                form_data[key] = None
        if form_data.get("default_location_id"):
            form_data["default_location_id"] = int(form_data["default_location_id"])
        if self.active_org_id:
            Org.update(self.active_org_id, form_data)
            self.active_org_id = None
        else:
            Org.add_ao(self.region.id, form_data)
        self.region_data = RegionData(self.region.id)
        self.add_location_dialog_open = False
        self.edit_location_dialog_open = False
        yield

    def handle_submit_add_series(self, form_data: dict[str, str]):
        form_data = clear_form_blanks(form_data)

        days_of_week: list[int] = []
        for i, day in enumerate(DAYS_OF_WEEK):
            if form_data.get(day):
                days_of_week.append(i + 1)

        end_time = safe_get_convert(form_data, "end_time", conversion=datetime.strptime, args=["%H:%M"])
        if not end_time:
            form_data["end_time"] = (
                safe_get_convert(form_data, "start_time", conversion=datetime.strptime, args=["%H:%M"])
                + timedelta(hours=1)
            ).time()
        else:
            form_data["end_time"] = end_time.time()

        name = form_data.get("name")
        if not name:
            form_data["name"] = "TBD Name"  # TODO: make this ao.name + event_type.name

        recurrence_pattern = RECURRENCE_MAP[form_data.get("recurrence_pattern")]
        recurrence_interval = INTERVAL_MAP[form_data.get("recurrence_interval")]

        series_list = [
            Event(
                org_id=safe_get_convert(form_data, "org_id", conversion=int),
                location_id=safe_get_convert(form_data, "location_id", conversion=int),
                event_type_id=safe_get_convert(form_data, "event_type_id", conversion=int),
                start_date=safe_get_convert(form_data, "start_date", conversion=datetime.strptime, args=["%Y-%m-%d"]),
                end_date=safe_get_convert(form_data, "end_date", conversion=datetime.strptime, args=["%Y-%m-%d"]),
                start_time=safe_get_convert(
                    form_data, "start_time", conversion=datetime.strptime, args=["%H:%M"]
                ).time(),
                end_time=end_time,
                day_of_week=day,
                recurrence_pattern=recurrence_pattern,
                recurrence_interval=recurrence_interval,
                index_within_interval=safe_get_convert(form_data, "index", conversion=int),
                name=form_data.get("name"),
                description=form_data.get("description"),
                highlight=form_data.get("highlight") is not None,
                is_active=True,
                is_series=True,
            )
            for day in days_of_week
        ]
        DbManager.create_records(series_list)
        self.region_data = RegionData(self.region.id)
        self.add_series_dialog_open = False
        self.edit_series_dialog_open = False
        self.active_series = None
        yield

    def cancel_series_form(self):
        self.add_series_dialog_open = False
        self.edit_series_dialog_open = False
        self.delete_series_dialog_open = False
        self.active_series = None
        yield

    def cancel_ao_form(self):
        self.add_ao_dialog_open = False
        self.edit_ao_dialog_open = False
        self.delete_ao_dialog_open = False
        self.active_org = None
        yield

    def edit_ao_trigger(self, org: dict):
        self.active_org = OrgExtended(**org)
        self.edit_ao_dialog_open = True
        yield

    def delete_ao_trigger(self, org: dict):
        self.active_org = OrgExtended(**org)
        self.delete_ao_dialog_open = True
        yield

    def edit_series_trigger(self, series: dict):
        self.active_series = Event(**series["event"])
        self.edit_series_dialog_open = True
        yield

    def delete_series_trigger(self, series: dict):
        self.active_series = Event(**series["event"])
        self.delete_series_dialog_open = True
        yield
