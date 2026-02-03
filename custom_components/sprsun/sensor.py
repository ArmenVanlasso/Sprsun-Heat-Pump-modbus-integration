import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.config_entries import ConfigEntry

from .const import *
from .modbus_client import HeatPumpModbusClient

_LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------
# AUTOMATYCZNE MAPOWANIE SENSORÓW NA PODSTAWIE const.py
# ---------------------------------------------------------

def _sensor_definitions():
    """Automatyczne generowanie definicji sensorów na podstawie stałych REG_* w const.py."""
    sensors = []

    for name, value in globals().items():
        if not name.startswith("REG_"):
            continue

        register = value
        clean_name = name.replace("REG_", "")

        # Przyjazna nazwa (z podkreślników → spacje)
        friendly = clean_name.replace("_", " ").capitalize()

        # Automatyczne typowanie
        if clean_name == "temperatura_powrotu":
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        elif "temperatura" in clean_name or "temp" in clean_name:
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        elif "cisnienie" in clean_name:
            unit = "bar"
            device_class = None
            icon = "mdi:gauge"
            scale = 0.01
            signed = False

        elif "obroty" in clean_name or "wentylator" in clean_name:
            unit = "rpm"
            device_class = None
            icon = "mdi:fan"
            scale = 1
            signed = False

        elif "moc" in clean_name:
            unit = "W"
            device_class = "power"
            icon = "mdi:flash"
            scale = 1
            signed = False
            state_class = "measurement"
        else:
            unit = None
            device_class = None
            icon = "mdi:checkbox-blank-circle-outline"
            scale = 1
            signed = False
            state_class = None

        sensors.append({
            "unique_id": clean_name,
            "name": friendly,
            "register": register,
            "unit": unit,
            "device_class": device_class,
            "icon": icon,
            "scale": scale,
            "signed": signed,
            "state_class": state_class if "state_class" in locals() else None,
        })

    return sensors


SENSORS = _sensor_definitions()


# ---------------------------------------------------------
# SETUP ENTRY
# ---------------------------------------------------------

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    data = hass.data[DOMAIN][entry.entry_id]
    client: HeatPumpModbusClient = data["client"]
    model: str = data["model"]

    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    entities = [
        SprsunGenericSensor(client, entry.entry_id, model, definition)
        for definition in SENSORS
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


# ---------------------------------------------------------
# UNIWERSALNY SENSOR
# ---------------------------------------------------------

class SprsunGenericSensor(SensorEntity):
    """Uniwersalny sensor SPRSUN generowany automatycznie."""

    _attr_should_poll = False

    def __init__(self, client, entry_id, model, definition):
        self._client = client
        self._entry_id = entry_id
        self._model = model
        self._def = definition
        self._attr_available = False

        # Nazwa wyświetlana
        self._attr_name = definition["name"]

        # Unikalne ID
        self._attr_unique_id = f"sprsun_{definition['unique_id']}_{entry_id}"

        # Entity ID
        self.entity_id = f"sensor.sprsun_{definition['unique_id']}_{entry_id}"

        # Ikona, jednostka, device_class
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

    async def async_update(self):
        reg = self._def["register"]
        scale = self._def["scale"]
        signed = self._def["signed"]

        regs = await self._client.read_holding_registers(reg, 1)
        if not regs:
            self._attr_available = False
            return

        raw = regs[0]

        # Konwersja INT16
        if signed and raw > 32767:
            raw -= 65536

        # SPECJALNY PRZYPADEK: Temperatura powrotu
        if self._def["unique_id"] == "temperatura_powrotu":
            value = raw * 0.1
            self._attr_native_value = round(value, 1)
            self._attr_available = True
            return

        # Domyślne skalowanie
        value = raw * scale
        self._attr_native_value = round(value, 2)
        self._attr_available = True
