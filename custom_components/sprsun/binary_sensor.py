import logging
from datetime import timedelta

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.config_entries import ConfigEntry

from .const import (
    DOMAIN,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)
from .modbus_client import HeatPumpModbusClient

from .models.CGK025V3L.binary_sensors import BINARY_SENSORS as BINARY_025
from .models.CGK030V3L.binary_sensors import BINARY_SENSORS as BINARY_030
from .models.CGK040V3L.binary_sensors import BINARY_SENSORS as BINARY_040
from .models.CGK050V3L.binary_sensors import BINARY_SENSORS as BINARY_050
from .models.CGK060V3L.binary_sensors import BINARY_SENSORS as BINARY_060

_LOGGER = logging.getLogger(__name__)

MODEL_BINARY_MAP = {
    "cgk_025v3l": BINARY_025,
    "cgk_030v3l": BINARY_030,
    "cgk_040v3l": BINARY_040,
    "cgk_050v3l": BINARY_050,
    "cgk_060v3l": BINARY_060,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    data = hass.data[DOMAIN][entry.entry_id]
    client: HeatPumpModbusClient = data["client"]
    model: str = data["model"]

    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    sensors_def = MODEL_BINARY_MAP.get(model)
    if sensors_def is None:
        _LOGGER.error("Brak zdefiniowanych binary sensorów dla modelu: %s", model)
        return

    entities: list[BinarySensorEntity] = [
        SprsunBinarySensor(client, entry.entry_id, model, definition)
        for definition in sensors_def
    ]

    hass.data[DOMAIN][entry.entry_id]["binary_entities"] = entities

    async_add_entities(entities)

    if model == "cgk_025v3l":
        from .models.CGK025V3L.sensor_alarm import SprsunActiveAlarmsSensor
    elif model == "cgk_030v3l":
        from .models.CGK030V3L.sensor_alarm import SprsunActiveAlarmsSensor
    elif model == "cgk_040v3l":
        from .models.CGK040V3L.sensor_alarm import SprsunActiveAlarmsSensor
    elif model == "cgk_050v3l":
        from .models.CGK050V3L.sensor_alarm import SprsunActiveAlarmsSensor
    else:
        from .models.CGK060V3L.sensor_alarm import SprsunActiveAlarmsSensor

    # UWAGA: zakładam, że SprsunActiveAlarmsSensor ma __init__(client, entry_id, model)
    active_alarm_sensor = SprsunActiveAlarmsSensor(client, entry.entry_id, model)
    async_add_entities([active_alarm_sensor])

    async def _periodic_update(now):
        for entity in entities:
            try:
                await entity.async_update()
                entity.async_write_ha_state()
            except Exception as err:
                _LOGGER.error("Błąd aktualizacji binary sensora %s: %s", entity.name, err)

        try:
            await active_alarm_sensor.async_update()
            active_alarm_sensor.async_write_ha_state()
        except Exception as err:
            _LOGGER.error("Błąd aktualizacji sensora aktywnych alarmów: %s", err)

    async_track_time_interval(
        hass,
        _periodic_update,
        timedelta(seconds=scan_interval),
    )


class SprsunBinarySensor(BinarySensorEntity):
    _attr_should_poll = False

    def __init__(self, client, entry_id, model, definition):
        self._client = client
        self._entry_id = entry_id
        self._model = model
        self._def = definition
        self._attr_available = False
        self._attr_is_on = False

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{self._model}_di_{self._def['address']}"

        slug = (
            f"sprsun_{self._model}_{definition['name']}"
            .lower()
            .replace(" ", "_")
            .replace("ą", "a")
            .replace("ć", "c")
            .replace("ę", "e")
            .replace("ł", "l")
            .replace("ń", "n")
            .replace("ó", "o")
            .replace("ś", "s")
            .replace("ź", "z")
            .replace("ż", "z")
        )
        self.entity_id = f"binary_sensor.{slug}"

        self._attr_device_class = definition.get("device_class")

        self._icon_on = definition.get("icon_on", "mdi:alert-circle")
        self._icon_off = definition.get("icon_off", "mdi:check-circle")

        self._mapping = definition.get("mapping", {})

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }

    @property
    def icon(self):
        return self._icon_on if self.is_on else self._icon_off

    @property
    def extra_state_attributes(self):
        if not self._mapping:
            return None

        value = 1 if self.is_on else 0
        return {
            "description": self._mapping.get(value, "Nieznany")
        }

    async def async_update(self):
        address = self._def["address"]
        index = self._def.get("index", 0)

        bits = await self._client.read_discrete_inputs(address, 1)
        if not bits:
            self._attr_available = False
            return

        try:
            state = bool(bits[index])
        except Exception:
            self._attr_available = False
            return

        self._attr_is_on = state
        self._attr_available = True
