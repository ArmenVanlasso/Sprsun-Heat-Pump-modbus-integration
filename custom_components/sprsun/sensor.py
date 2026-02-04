import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .modbus_client import HeatPumpModbusClient  # zostawione, jeśli kiedyś będzie potrzebne

_LOGGER = logging.getLogger(__name__)


def _sensor_definitions():
    sensors = []

    for name, value in globals().items():
        if not name.startswith("REG_"):
            continue

        register = value
        clean_name = name.replace("REG_", "")
        friendly = clean_name.replace("_", " ").capitalize()

        unit = None
        device_class = None
        icon = "mdi:checkbox-blank-circle-outline"
        scale = 1
        signed = False
        state_class = None

        if clean_name == "temperatura_powrotu":
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        elif clean_name == "przegrzanie":
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        elif clean_name == "zawor_eev":
            friendly = "Zawór rozprężny"
            icon = "mdi:valve"
            unit = "steps"
            scale = 1
            signed = False

        elif clean_name == "napiecie_falownika":
            unit = "V"
            device_class = "voltage"
            icon = "mdi:flash"
            scale = 1
            signed = False
            state_class = "measurement"

        elif clean_name == "prad_falownika":
            unit = "A"
            device_class = "current"
            icon = "mdi:current-ac"
            scale = 1
            signed = False

        elif clean_name == "moc_pobierana":
            unit = "W"
            device_class = "power"
            icon = "mdi:flash"
            scale = 1
            signed = False
            state_class = "measurement"

        elif clean_name == "status":
            unit = None
            device_class = None
            icon = "mdi:information"
            scale = 1
            signed = False

        elif clean_name == "status_2":
            friendly = "Status 2"
            unit = None
            device_class = None
            icon = "mdi:information"
            scale = 1
            signed = False

        elif "temperatura" in clean_name:
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        sensors.append(
            {
                "unique_id": clean_name,
                "name": friendly,
                "register": register,
                "unit": unit,
                "device_class": device_class,
                "icon": icon,
                "scale": scale,
                "signed": signed,
                "state_class": state_class,
            }
        )

    return sensors


SENSORS = _sensor_definitions()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    model: str = data["model"]

    entities = [
        SprsunGenericSensor(coordinator, entry.entry_id, model, definition)
        for definition in SENSORS
    ]

    async_add_entities(entities)


class SprsunGenericSensor(CoordinatorEntity, SensorEntity):
    _attr_should_poll = False

    def __init__(self, coordinator, entry_id, model, definition):
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._attr_available = False
        self._attr_name = definition["name"]
        self._attr_unique_id = f"sprsun_{definition['unique_id']}_{entry_id}"
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
    def native_value(self):
        reg = self._def["register"]
        scale = self._def["scale"]
        signed = self._def["signed"]
        uid = self._def["unique_id"]

        data = self.coordinator.data or {}
        raw = data.get(reg)

        if raw is None:
            return None

        if signed and raw > 32767:
            raw -= 65536

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
            return mapping.get(raw, raw)

        if uid == "status_2":
            mapping = {
                0: "OK",
                1: "Sterowanie",
                2: "Graniczny",
            }
            return mapping.get(raw, raw)

        if uid == "tryb_pracy_pompy":
            mapping = {
                0: "Stop",
                1: "Praca",
                2: "Sterowanie",
                3: "Ręczny",
            }
            return mapping.get(raw, raw)

        value = raw * scale
        return round(value, 2)

    @property
    def available(self) -> bool:
        reg = self._def["register"]
        data = self.coordinator.data or {}
        return reg in data and data[reg] is not None
