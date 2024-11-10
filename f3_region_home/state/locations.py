import reflex as rx

from .base import BaseState
from ..database.models import Location
from ..database.queries import RegionData


class LocationState(BaseState):
    location_form_data: dict = {}
    active_location_id: int
    add_location_dialog_open: bool = False
    selected_lat: float
    selected_lon: float

    def handle_submit_add_location(self, form_data: dict[str, str]):
        self.location_form_data = form_data
        for key, value in form_data.items():
            if value == "":
                form_data[key] = None
        Location.add(self.region.id, form_data)
        self.region_data = RegionData(self.region.id)
        self.add_location_dialog_open = False
        yield

    def handle_map_click(self, data: dict[str, str]):
        self.selected_lat = data["lngLat"]["lat"]
        self.selected_lon = data["lngLat"]["lng"]
        self.add_location_dialog_open = self.user_is_admin

    def handle_submit_edit_location(self, form_data: dict[str, str]):
        for key, value in form_data.items():
            if value == "":
                form_data[key] = None
        Location.update(self.active_location_id, form_data)
        self.region_data = RegionData(self.region.id)

    def handle_delete_location(self):
        Location.deactivate(self.active_location_id)
        self.region_data = RegionData(self.region.id)

    @rx.var
    def center_lat(self) -> float:
        if len(getattr(self.region_data, "locations", [])) > 0:
            return sum([loc.lat for loc in self.region_data.locations]) / len(self.region_data.locations)
        else:
            return 38.54659713100793

    @rx.var
    def center_lon(self) -> float:
        if len(getattr(self.region_data, "locations", [])) > 0:
            return sum([loc.lon for loc in self.region_data.locations]) / len(self.region_data.locations)
        else:
            return -90.99680423957764
