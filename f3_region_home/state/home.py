import re
from datetime import datetime, timedelta

import reflex as rx

from ..database.models import Event, Location, Org
from ..database.queries import RegionData

REGION_LIST = Org.get_all_regions()


class State(rx.State):
    region_name: str
    region_id: int
    center_lat: float = 38.54659713100793
    center_lon: float = -90.99680423957764
    selected_date: datetime = datetime.today()
    selected_date_str: str = selected_date.strftime("%Y-%m-%d")
    selected_date_set: str = (selected_date + timedelta(1)).strftime("%Y-%m-%d")
    calendar_events: list[Event] = []
    location_form_data: dict = {}
    active_location_id: int
    add_location_dialog_open: bool = False
    selected_lat: float
    selected_lon: float
    region_data: RegionData = None
    active_event_id: int
    active_org_id: int
    add_series_dialog_open: bool = False
    active_series: Event = None
    add_ao_dialog_open: bool = False

    def switch_region(self, region_name: str):
        self.region_name = region_name
        self.region_id = REGION_LIST[region_name]
        self.region_data = RegionData(self.region_id)
        if len(self.region_data.locations) > 0:
            self.center_lat = sum([loc.lat for loc in self.region_data.locations]) / len(self.region_data.locations)
            self.center_lon = sum([loc.lon for loc in self.region_data.locations]) / len(self.region_data.locations)

    def _reformat_date(self, date_str: str) -> datetime:
        date_str = date_str.replace(".toDateString()", "").strip()
        date_str = re.sub(r"\s*\(.*\)$", "", date_str)
        date_format = "%a %b %d %Y %H:%M:%S GMT%z"
        return datetime.strptime(date_str, date_format)

    def switch_selected_date(self, date_str: str):
        self.selected_date = self._reformat_date(date_str)
        self.selected_date_str = self.selected_date.strftime("%Y-%m-%d")
        self.calendar_events = Event.get_week(region_id=self.region_id, start_date=self.selected_date)

    def update_locations(self):
        self.region_data.locations = Location.get_all(region_id=self.region_id)

    @rx.background
    async def send_toast(self, message: str):
        print("Sending Toast")
        yield rx.toast.success(message)
        return

    def handle_submit_add_location(self, form_data: dict):
        self.location_form_data = form_data
        for key, value in form_data.items():
            if value == "":
                form_data[key] = None
        Location.add(self.region_id, form_data)
        self.region_data = RegionData(self.region_id)
        self.add_location_dialog_open = False
        yield

    async def handle_map_click(self, data: dict):
        print("Map Clicked")
        print(data)
        self.selected_lat = data["lngLat"]["lat"]
        self.selected_lon = data["lngLat"]["lng"]
        self.add_location_dialog_open = True
        yield
        return

    def handle_submit_edit_location(self, form_data: dict):
        self.location_form_data = form_data
        for key, value in form_data.items():
            if value == "":
                form_data[key] = None
        Location.update(self.active_location_id, form_data)
        self.region_data = RegionData(self.region_id)

    def handle_delete_location(self):
        Location.deactivate(self.active_location_id)
        self.region_data = RegionData(self.region_id)

    def handle_submit_edit_event(self, form_data: dict):
        pass

    def handle_delete_event(self):
        pass

    def handle_add_series(self, org: Org):
        self.active_org_id = org.id
        # self.active_series = series
        self.add_series_dialog_open = True

    def handle_add_ao(self):
        # self.active_org_id = org.id
        # self.active_series = series
        self.add_ao_dialog_open = True

    def handle_submit_add_ao(self, form_data: dict):
        for key, value in form_data.items():
            if value == "":
                form_data[key] = None
        if form_data.get("location_id"):
            form_data["default_location_id"] = int(form_data["default_location_id"])
        Org.add_ao(self.region_id, form_data)
        self.region_data = RegionData(self.region_id)
        self.add_location_dialog_open = False
        yield

    @rx.var
    def region_selected(self):
        return self.region_id is not None
