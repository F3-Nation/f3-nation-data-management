import reflex as rx

from .home import State
from ..database.models import Location


class AddLocationForm(rx.State):
    form_data: dict = {}

    async def handle_submit(self, form_data: dict):
        self.form_data = form_data
        state: State = await self.get_state(State)
        for key, value in form_data.items():
            if value == "":
                form_data[key] = None
        Location.add(state.region_id, form_data)
        rx.toast.success("Location Added!")
        # State.update_locations()
        # rx.redirect("/settings")
        # rx.toast.success("Location Added!")
