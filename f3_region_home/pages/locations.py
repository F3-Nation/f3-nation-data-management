import reflex as rx
import reflex_map as rx_map

from ..database.queries import LocationExtended
from ..layouts import default_layout
from ..state.locations import LocationState


def locations() -> rx.Component:
    # Locations Page
    return default_layout(
        rx.vstack(
            add_location_dialog(),
            default_marker_map(),
            rx.flex(
                rx.foreach(
                    LocationState.region_data.locations,
                    lambda location: location_card(location),
                ),
                spacing="2",
                flex_wrap="wrap",
                width="100%",
                # direction="column",
            ),
            width="80%",
        ),
        "locations",
    )


def location_card(location: LocationExtended) -> rx.Component:
    return rx.card(
        rx.flex(
            rx.heading(location.name),
            rx.cond(
                LocationState.user_is_admin,
                rx.flex(
                    edit_location_dialog(location),
                    delete_location_dialog(location),
                    direction="row",
                    spacing="3",
                ),
            ),
            justify="between",
            direction="row",
            spacing="3",
        ),
    )


def delete_location_dialog(location: LocationExtended) -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(rx.icon("trash-2")),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Delete Location"),
            rx.alert_dialog.description(f"Are you sure you want to delete {location.name}?"),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button("Cancel", variant="soft", color_scheme="gray"),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Delete",
                        variant="solid",
                        color_scheme="red",
                        on_click=LocationState.handle_delete_location,
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
        on_open_change=LocationState.set_active_location_id(location.id),
    )


def edit_location_dialog(location: LocationExtended) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.icon("pencil")),
        rx.dialog.content(
            rx.dialog.title("Edit Location"),
            rx.form(
                rx.flex(
                    rx.flex(
                        rx.input(
                            placeholder="Location Name",
                            name="name",
                            default_value=location.name,
                            required=True,
                        ),
                        rx.input(
                            placeholder="Description",
                            name="description",
                            default_value=location.description,
                        ),
                        rx.input(
                            placeholder="Latitude",
                            name="lat",
                            default_value=location.lat_str,
                            type="text",
                        ),
                        rx.input(
                            placeholder="Longitude",
                            name="lon",
                            default_value=location.lon_str,
                            type="text",
                        ),
                        rx.input(
                            placeholder="Address",
                            name="address_street",
                            default_value=location.address_street,
                        ),
                        rx.input(
                            placeholder="City",
                            name="address_city",
                            default_value=location.address_city,
                        ),
                        rx.input(
                            placeholder="State",
                            name="address_state",
                            default_value=location.address_state,
                        ),
                        rx.input(
                            placeholder="Zip",
                            name="address_zip",
                            default_value=location.address_zip,
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button("Save", type="submit"),
                        ),
                    ),
                    direction="column",
                    spacing="3",
                ),
                on_submit=lambda c: LocationState.handle_submit_edit_location,
            ),
        ),
        on_open_change=LocationState.set_active_location_id(location.id),
    )


def add_location_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Add Location"),
            rx.form(
                rx.flex(
                    rx.flex(
                        rx.input(
                            placeholder="Location Name",
                            name="name",
                            required=True,
                        ),
                        rx.input(
                            placeholder="Description",
                            name="description",
                        ),
                        rx.input(
                            placeholder="Latitude",
                            name="lat",
                            type="text",
                            value=LocationState.selected_lat,
                        ),
                        rx.input(
                            placeholder="Longitude",
                            name="lon",
                            type="text",
                            value=LocationState.selected_lon,
                        ),
                        rx.input(
                            placeholder="Address",
                            name="address_street",
                        ),
                        rx.input(
                            placeholder="City",
                            name="address_city",
                        ),
                        rx.input(
                            placeholder="State",
                            name="address_state",
                        ),
                        rx.input(
                            placeholder="Zip",
                            name="address_zip",
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button("Save", type="submit"),
                        ),
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                                on_click=LocationState.set_add_location_dialog_open(False),
                            ),
                        ),
                        direction="row",
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="3",
                ),
                on_submit=LocationState.handle_submit_add_location,
            ),
        ),
        open=LocationState.add_location_dialog_open,
    )


def default_marker_map() -> rx.Component:
    return rx_map.map(
        rx.foreach(
            LocationState.region_data.locations,
            lambda location: rx_map.marker(
                latitude=location.lat,
                longitude=location.lon,
            ),
        ),
        rx_map.source(
            rx_map.layer(
                id="background",
                type="background",
                paint={"background-color": "#e0dfdf"},
            ),
            rx_map.layer(
                id="simple-tiles",
                type="raster",
                source="raster-tiles",
            ),
            type="raster",
            id="raster-tiles",
            tiles=["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            attribution="&copy; OpenStreetMap",
            tileSize=256,
            minzoom=0,
            maxzoom=19,
        ),
        rx_map.search_control(),
        zoom=10,
        initialViewState={"latitude": LocationState.center_lat, "longitude": LocationState.center_lon, "zoom": 10},
        on_click=LocationState.handle_map_click,
    )
    # return rx_map.map(
    #     rx_map.source(
    #         rx_map.layer(
    #             source="google_maps",
    #             type="raster",
    #         ),
    #         type="raster",
    #         title="Google Maps",
    #         id="google_maps",
    #         tileSize=256,
    #         tiles=["https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"],
    #         attribution="&copy; Google Maps",
    #     ),
    #     rx_map.search_control(),
    #     rx_map.navigation_control(),
    #     rx_map.fullscreen_control(),
    #     initialViewState=dict(longitude=151.209900, latitude=-33.865143, zoom=10),
    # )
