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
    sensors = []

    for name, value in globals().items():
        if not name.startswith("REG_"):
            continue

        register = value
        clean_name = name.replace("REG_", "")
        friendly = clean_name.replace("_", " ").capitalize()

        # Domyślne wartości
        unit = None
        device_class = None
        icon = "mdi:checkbox-blank-circle-outline"
        scale = 1
        signed = False
        state_class = None

        # ---------------------------------------------------------
        # SPECJALNE SENSORY
        # ---------------------------------------------------------

        # Temperatura powrotu
        if clean_name == "temperatura_powrotu":
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        # Przegrzanie
        elif clean_name == "przegrzanie":
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        # Zawór EEV
        elif clean_name == "zawor_eev":
            friendly = "Zawór rozprężny"
            icon = "mdi:valve"
            unit = "steps"
            scale = 1
            signed = False

        # Napięcie falownika
        elif clean_name == "napiecie_falownika":
            unit = "V"
            device_class = "voltage"
            icon = "mdi:flash"
            scale = 1
            signed = False
            state_class = "measurement"

        # Prąd falownika
        elif clean_name == "prad_falownika":
            unit = "A"
            device_class = "current"
            icon = "mdi:current-ac"
            scale = 1
            signed = False

        # Moc pobierana
        elif clean_name == "moc_pobierana":
            unit = "W"
            device_class = "power"
            icon = "mdi:flash"
            scale = 1
            signed = False
            state_class = "measurement"

        # Status główny
        elif clean_name == "status":
            unit = None
            device_class = None
            icon = "mdi:information"
            scale = 1
            signed = False

        # Status 2
        elif clean_name == "status_2":
            friendly = "Status 2"
            unit = None
            device_class = None
            icon = "mdi:information"
            scale = 1
            signed = False

        # ---------------------------------------------------------
        # Automatyczne typowanie pozostałych temperatur
        # ---------------------------------------------------------
        elif "temperatura" in clean_name:
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        sensors.append({
            "unique_id": clean_name,
            "name": friendly,
            "register": register,
            "unit": unit,
            "device_class": device_class,
            "icon": icon,
            "scale": scale,
            "signed": signed,
            "state_class": state_class,
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

async def async_update(self):
    reg = self._def["register"]
    scale = self._def["scale"]
    signed = self._def["signed"]
    uid = self._def["unique_id"]

    regs = await self._client.read_holding_registers(reg, 1)
    if not regs:
        self._attr_available = False
        return

    raw = regs[0]

    if signed and raw > 32767:
        raw -= 65536

    # -----------------------------
    # STATUS (główny)
    # -----------------------------
    if uid == "status":
        mapping = {
            0: "Przygotowanie",
            1: "Praca",
            2: "Stop",
            3: "Stop timer",
            4: "Stop obsługa",
            5: "Sterowanie",
            6: "Stop",
            7: "Tryb ręczny",
            8: "Antyzamarzanie",
            9: "Stop AC linkage",
            10: "Zmiana trybu",
        }
        self._attr_native_value = mapping.get(raw, raw)
        self._attr_available = True
        return

    # -----------------------------
    # STATUS 2
    # -----------------------------
    if uid == "status_2":
        mapping = {
            0: "OK",
            1: "Sterowanie",
            2: "Graniczny",
        }
        self._attr_native_value = mapping.get(raw, raw)
        self._attr_available = True
        return

    # -----------------------------
    # TRYB PRACY POMPY
    # -----------------------------
    if uid == "tryb_pracy_pompy":
        mapping = {
            0: "Stop",
            1: "Praca",
            2: "Sterowanie",
            3: "Ręczny",
        }
        self._attr_native_value = mapping.get(raw, raw)
        self._attr_available = True
        return

    # -----------------------------
    # DOMYŚLNE SKALOWANIE
    # -----------------------------
    value = raw * scale
    self._attr_native_value = round(value, 2)
    self._attr_available = True

