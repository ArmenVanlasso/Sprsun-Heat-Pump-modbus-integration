from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

from .binary_sensor_cgk_025v3l import BINARY_SENSORS_CGK_025V3L
from .binary_sensor_cgk_030v3l import BINARY_SENSORS_CGK_030V3L
from .binary_sensor_cgk_040v3l import BINARY_SENSORS_CGK_040V3L
from .binary_sensor_cgk_050v3l import BINARY_SENSORS_CGK_050V3L
from .binary_sensor_cgk_060v3l import BINARY_SENSORS_CGK_060V3L


BINARY_SENSOR_MAP = {
    "cgk_025v3l": BINARY_SENSORS_CGK_025V3L,
    "cgk_030v3l": BINARY_SENSORS_CGK_030V3L,
    "cgk_040v3l": BINARY_SENSORS_CGK_040V3L,
    "cgk_050v3l": BINARY_SENSORS_CGK_050V3L,
    "cgk_060v3l": BINARY_SENSORS_CGK_060V3L,
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up binary sensors for Sprsun integration."""
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator = data["coordinator"]
    model = entry.data.get("model")

    sensors_for_model = BINARY_SENSOR_MAP.get(model)

    if not sensors_for_model:
        return

    entities = [
        SprsunBinarySensor(coordinator, entry.entry_id, model, key, cfg)
        for key, cfg in sensors_for_model.items()
    ]

    async_add_entities(entities)


class SprsunBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Sprsun binary sensor."""

    def __init__(self, coordinator, entry_id, model, key, cfg):
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._model = model
        self._key = key
        self._cfg = cfg

        self._attr_unique_id = f"{DOMAIN}_{model}_{key}"
        self._attr_name = f"{model.upper()} {cfg['name']}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "Sprsun Heat Pump",
            "manufacturer": "Sprsun",
            "model": self._model,
        }

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        data = self.coordinator.data or {}
        value = data.get(self._cfg["register"])

        if value is None:
            return False

        if "bit" in self._cfg:
            bit = (value >> self._cfg["bit"]) & 1
            return bit == self._cfg.get("on_value", 1)

        return value == self._cfg.get("on_value", 1)

    @property
    def icon(self):
        """Return dynamic icon based on state."""
        if self.is_on:
            return self._cfg.get("icon_on", "mdi:check-circle")
        return self._cfg.get("icon_off", "mdi:close-circle")

    @property
    def available(self) -> bool:
        data = self.coordinator.data or {}
        return self._cfg["register"] in data and data[self._cfg["register"]] is not None
