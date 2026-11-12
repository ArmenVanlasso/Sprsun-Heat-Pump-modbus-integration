import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

FAILURE_SYMBOL_1 = {
    0: "Hotwater temp.",
    1: "Ambi temp.",
    2: "Coil temp.",
    3: "Invalid",
    4: "Outlet temp.",
    5: "High pressure sensor failure",
    6: "Invalid",
    7: "Phase sequence",
}


class SprsunFailureSymbol1Sensor(CoordinatorEntity, SensorEntity):
    """Failure Symbol 1 decoder."""

    _attr_should_poll = False

    def __init__(self, coordinator, entry_id, model):
        super().__init__(coordinator)

        self._entry_id = entry_id
        self._model = model

        self._attr_name = "Failure Symbol 1"
        self._attr_unique_id = f"sprsun_{model}_failure_symbol_1"
        self._attr_entity_category = "diagnostic"

    @property
    def icon(self):
        raw = self.coordinator.data.get(7, 0)

        if raw == 0:
            return "mdi:check-circle"

        return "mdi:alert"

    @property
    def native_value(self):
        raw = self.coordinator.data.get(7, 0)

        if raw == 0:
            return "Off"

        active_faults = []

        for bit, description in FAILURE_SYMBOL_1.items():
            if raw & (1 << bit):
                active_faults.append(description)

        return ", ".join(active_faults)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }
