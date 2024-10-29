from typing import Any, Dict

import reflex as rx


class CurrencyInput(rx.Component):
    library = "react-currency-input-field"
    tag = "CurrencyInput"
    is_default = True

    default_value: rx.Var[float]
    prefix: rx.Var[str]
    suffix: rx.Var[str]
    name: rx.Var[str]

    def get_event_triggers(self) -> Dict[str, Any]:
        return super().get_event_triggers() | {
            "on_blur": lambda e: [e.target.value],
            "on_value_change": lambda value, name, values: [value, name, values],
        }
