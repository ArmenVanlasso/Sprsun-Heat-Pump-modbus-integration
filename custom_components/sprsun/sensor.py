# sensor.py
import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
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

# importy list sensorów per model
from .sensor_cgk_025v3l import SENSORS_CGK_025V3L
from .sensor_cgk_030v3l import SENSORS_CGK_030V3L
# z czasem dodasz:
# from .sensor_cgk_040v3l import SENSORS_CGK_040V3L
# from .sensor_cgk_050v3l import SENSORS_CGK_050V3L
# from .sensor_cgk_060v3l import SENSORS_CGK_060V3L

_LOGGER = logging.getLogger(__name__)

MODEL_SENSORS_MAP = {
    "cgk_025v3l": SENSORS_CGK_025V3L,
    "cgk_030v3l": SENSORS_CGK_030V3L,
    # "cgk_040v3l": SENSORS_CGK_040V3L,
    # "cgk_050v3l": SENSORS_CGK_050V3L,
    # "cgk_060v3l": SENSORS_CGK_060V3L,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    data = hass.data[DOMAIN][entry.entry_id]
    client: HeatPumpModbusClient = data["client"]
    model: str = data["model"]  # np. "cgk_025v3l"

    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    sensors_def = MODEL_SENSORS_MAP.get(model)
    if sensors_def is None:
        _LOGGER.error("Brak zdefiniowanych sensorów dla modelu: %s", model)
        return

    entities = [
        SprsunGenericSensor(client, entry.entry_id, model, definition)
        for definition in sensors_def
    ]

    async_add_entities(entities)

    async def _periodic_update(now):
        for entity in entities:
            await entity.async_update()
            entity.async_write_ha_state()

    async_track_time_interval(
        hass,
        _periodic_update,
        timedelta(seconds=scan_interval),
    )


class SprsunGenericSensor(SensorEntity):
    _attr_should_poll = False

    def __init__(self, client, entry_id, model, definition):
        self._client = client
        self._entry_id = entry_id
        self._model = model
        self._def = definition
        self._attr_available = False

        self._attr_name = definition["name"]
        self._attr_unique_id = f"sprsun_{definition['unique_id']}_{entry_id}"
        self.entity_id = f"sensor.sprsun_{definition['unique_id']}_{entry_id}"

        self._attr_icon = definition["icon"]
        self._attr_device_class = definition["device_class"]
        self._attr_native_unit_of_measurement = definition["unit"]
        self._attr_state_class = definition.get("state_class")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "Sprsun Heat Pump",
            "manufacturer": "Sprsun",
            "model": self._model,
        }

    @property
    def icon(self):
        value = self._attr_native_value
        uid = self._def["unique_id"]

        if uid == "status":
            mapping = {
                0: ("Przygotowanie", "mdi:information"),
                1: ("Praca", "mdi:run"),
                2: ("Stop", "mdi:stop"),
                3: ("Stop timer", "mdi:timer-off"),
                4: ("Stop obsługa", "mdi:account-wrench"),
                5: ("Sterowanie", "mdi:remote"),
                6: ("Stop", "mdi:stop"),
                7: ("Tryb ręczny", "mdi:hand"),
                8: ("Antyzamarzanie", "mdi:snowflake"),
                9: ("Stop AC linkage", "mdi:alert-circle"),
                10: ("Zmiana trybu", "mdi:swap-horizontal"),
            }

            if value in mapping:
                text, icon = mapping[value]
                self._attr_native_value = text
                return icon

        if uid == "status_2":
            mapping = {
                0: "OK",
                1: "Sterowanie",
                2: "Graniczny",
            }
            if value in mapping:
                self._attr_native_value = mapping[value]
            return self._def["icon"]

        if uid == "tryb_pracy_pompy":
            mapping = {
                0: "Stop",
                1: "Praca",
                2: "Sterowanie",
                3: "Ręczny",
            }
            if value in mapping:
                self._attr_native_value = mapping[value]
            return self._def["icon"]

        return self._def["icon"]

    async def async_update(self):
        reg = self._def["register"]
        scale = self._def["scale"]
        signed = self._def["signed"]

        regs = await self._client.read_holding_registers(reg, 1)
        if not regs:
            self._attr_available = False
            return

        raw = regs[0]

        if signed and raw > 32767:
            raw -= 65536

        value = raw * scale
        self._attr_native_value = round(value, 2)
        self._attr_available = True
