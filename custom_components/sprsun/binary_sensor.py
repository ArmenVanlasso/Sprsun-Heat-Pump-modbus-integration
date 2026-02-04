from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

# Import list binary sensorów z osobnych plików
from .binary_sensor_cgk_025v3l import BINARY_SENSORS_CGK_025V3L
from .binary_sensor_cgk_030v3l import BINARY_SENSORS_CGK_030V3L
from .binary_sensor_cgk_040v3l import BINARY_SENSORS_CGK_040V3L
from .binary_sensor_cgk_050v3l import BINARY_SENSORS_CGK_050V3L
from .binary_sensor_cgk_060v3l import BINARY_SENSORS_CGK_060V3L


# Mapowanie model → lista binary sensorów
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

    # Pobierz listę binary sensorów dla danego modelu
    sensors_for_model = BINARY_SENSOR_MAP.get(model)

    # Jeśli model nieobsługiwany → nie tworzymy encji
    if not sensors_for_model:
        return

    entities = [
        SprsunBinarySensor(coordinator, model, key, cfg)
        for key, cfg in sensors_for_model.items()
    ]

    async_add_entities(entities)


class SprsunBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Sprsun binary sensor."""

    def __init__(self, coordinator, model, key, cfg):
        super().__init__(coordinator)
        self._model = model
        self._key = key
        self._cfg = cfg

        # Unikalne ID encji
        self._attr_unique_id = f"{DOMAIN}_{model}_{key}"

        # Nazwa encji
        self._attr_name = f"{model.upper()} {cfg['name']}"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        value = self.coordinator.data.get(self._cfg["register"])

        if value is None:
            return False

        # Obsługa bitów
        if "bit" in self._cfg:
            bit = (value >> self._cfg["bit"]) & 1
            return bit == self._cfg.get("on_value", 1)

        return value == self._cfg.get("on_value", 1)
