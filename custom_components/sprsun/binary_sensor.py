from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    BINARY_SENSORS,
)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors from config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        SprsunBinarySensor(coordinator, description)
        for description in BINARY_SENSORS
    ]

    async_add_entities(entities)


class SprsunBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Modbus-based binary sensor."""

    def __init__(self, coordinator, description):
        super().__init__(coordinator)

        self._register = description["register"]
        self._attr_name = description["name"]
        self._attr_device_class = description.get("device_class")

        # entity_id = nazwa stałej bez REG_
        self._attr_unique_id = f"{DOMAIN}_{description['key']}"
        self.entity_id = f"binary_sensor.{description['key']}"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        value = self.coordinator.data.get(self._register)
        return bool(value)
