import reflex as rx


def make_plugin_var(name, lib, is_default=False):
    imports = {lib: rx.ImportVar(name, is_default=is_default)}
    return rx.Var(name, _var_data=rx.vars.VarData(imports=imports))  # type: ignore


dayGridPlugin = make_plugin_var("dayGridPlugin", "@fullcalendar/daygrid", is_default=True)
timeGridPlugin = make_plugin_var("timeGridPlugin", "@fullcalendar/timegrid", is_default=True)
interactionPlugin = make_plugin_var("interactionPlugin", "@fullcalendar/interaction", is_default=True)


class FullCalendar(rx.Component):
    library: str = "@fullcalendar/react"

    tag: str = "FullCalendar"

    is_default = True

    initial_view: str = "dayGridWeek"

    plugins: list[rx.Var] = [dayGridPlugin, timeGridPlugin, interactionPlugin]

    lib_dependencies: list[str] = ["@fullcalendar/core", "@fullcalendar/daygrid"]

    header_toolbar: dict[str, str] = {
        "left": "prev,next",
        "center": "title",
        "right": "dayGridMonth,timeGridWeek,timeGridDay",
    }


calendar = FullCalendar.create
