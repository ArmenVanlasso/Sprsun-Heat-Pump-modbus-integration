import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import SprsunCoordinator

# Importy sensorów rejestrowych
from .models.CGK025V3L.sensors import SENSORS as SENSORS_025
from .models.CGK030V3L.sensors import SENSORS as SENSORS_030
from .models.CGK040V3L.sensors import SENSORS as SENSORS_040
from .models.CGK050V3L.sensors import SENSORS as SENSORS_050
from .models.CGK060V3L.sensors import SENSORS as SENSORS_060

# Importy logic sensors
from .models.CGK025V3L.logic_sensors import *
from .models.CGK030V3L.logic_sensors import *
from .models.CGK040V3L.logic_sensors import *
from .models.CGK050V3L.logic_sensors import *
from .models.CGK060V3L.logic_sensors import *

_LOGGER = logging.getLogger(__name__)

MODEL_SENSORS_MAP = {
    "cgk_025v3l": SENSORS_025,
    "cgk_030v3l": SENSORS_030,
    "cgk_040v3l": SENSORS_040,
    "cgk_050v3l": SENSORS_050,
    "cgk_060v3l": SENSORS_060,
}

# Usunięto CompressorStarts i DefrostCounter
MODEL_LOGIC_MAP = {
    "cgk_025v3l": {
        "CompressorRuntime": SprsunCompressorRuntimeSensor,
        "FanRuntime": SprsunFanRuntimeSensor,
        "OwnershipDays": SprsunOwnershipDaysSensor,
    },
    "cgk_030v3l": {
        "CompressorRuntime": SprsunCompressorRuntimeSensor,
        "FanRuntime": SprsunFanRuntimeSensor,
        "OwnershipDays": SprsunOwnershipDaysSensor,
    },
    "cgk_040v3l": {
        "CompressorRuntime": SprsunCompressorRuntimeSensor,
        "FanRuntime": SprsunFanRuntimeSensor,
        "OwnershipDays": SprsunOwnershipDaysSensor,
    },
    "cgk_050v3l": {
        "CompressorRuntime": SprsunCompressorRuntimeSensor,
        "FanRuntime": SprsunFanRuntimeSensor,
        "OwnershipDays": SprsunOwnershipDaysSensor,
    },
    "cgk_060v3l": {
        "CompressorRuntime": SprsunCompressorRuntimeSensor,
        "FanRuntime": SprsunFanRuntimeSensor,
        "OwnershipDays": SprsunOwnershipDaysSensor,
    },
}


# ---------------------------------------------------------
# SETUP ENTRY
# ---------------------------------------------------------

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]

    sensors_def = MODEL_SENSORS_MAP.get(model)
    if sensors_def is None:
        _LOGGER.error("Brak sensorów dla modelu %s", model)
        return

    entities: list[SensorEntity] = []

    # Sensory rejestrowe (z Modbus)
    for definition in sensors_def:
        entities.append(
            SprsunGenericSensor(
                coordinator,
                entry.entry_id,
                model,
                definition
            )
        )

    # LOGIC SENSORS
    logic = MODEL_LOGIC_MAP[model]

    entities.extend([
        logic["CompressorRuntime"]("Czas pracy sprężarki daily",
                                   f"{DOMAIN}_{model}_czas_pracy_sprezarki_daily",
                                   "daily", entry.entry_id, model),
        logic["CompressorRuntime"]("Czas pracy sprężarki monthly",
                                   f"{DOMAIN}_{model}_czas_pracy_sprezarki_monthly",
                                   "monthly", entry.entry_id, model),
        logic["CompressorRuntime"]("Czas pracy sprężarki yearly",
                                   f"{DOMAIN}_{model}_czas_pracy_sprezarki_yearly",
                                   "yearly", entry.entry_id, model),
        logic["CompressorRuntime"]("Czas pracy sprężarki total",
                                   f"{DOMAIN}_{model}_czas_pracy_sprezarki_total",
                                   "total", entry.entry_id, model),

        logic["FanRuntime"]("Czas pracy wentylatora daily",
                            f"{DOMAIN}_{model}_czas_pracy_wentylatora_daily",
                            "daily", entry.entry_id, model),
        logic["FanRuntime"]("Czas pracy wentylatora monthly",
                            f"{DOMAIN}_{model}_czas_pracy_wentylatora_monthly",
                            "monthly", entry.entry_id, model),
        logic["FanRuntime"]("Czas pracy wentylatora yearly",
                            f"{DOMAIN}_{model}_czas_pracy_wentylatora_yearly",
                            "yearly", entry.entry_id, model),
        logic["FanRuntime"]("Czas pracy wentylatora total",
                            f"{DOMAIN}_{model}_czas_pracy_wentylatora_total",
                            "total", entry.entry_id, model),

        logic["OwnershipDays"]("Czas posiadania pompy",
                               f"{DOMAIN}_{model}_czas_posiadania_pompy",
                               entry.entry_id, model),
    ])

    async_add_entities(entities)


# ---------------------------------------------------------
# SENSOR REJESTROWY (Modbus → koordynator)
# ---------------------------------------------------------

class SprsunGenericSensor(SensorEntity):
    _attr_should_poll = False

    def __init__(self, coordinator: SprsunCoordinator, entry_id, model, definition):
        self.coordinator = coordinator
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._register = definition["register"]
        self._scale = definition.get("scale", 1)
        self._signed = definition.get("signed", False)

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{model}_sensor_{self._register}"

        slug = (
            f"sprsun_{model}_{definition['name']}"
            .lower()
            .replace(" ", "_")
            .replace("ą", "a").replace("ć", "c").replace("ę", "e")
            .replace("ł", "l").replace("ń", "n").replace("ó", "o")
            .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )

        self.entity_id = f"sensor.{slug}"

        self._attr_native_unit_of_measurement = definition.get("unit")
        self._attr_device_class = definition.get("device_class")
        self._attr_state_class = definition.get("state_class")
        self._attr_icon = definition.get("icon")
        self._icon_map = definition.get("icon_map")

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def native_value(self):
        raw = self.coordinator.data.get(self._register)

        if raw is None:
            return None

        if self._signed and raw > 32767:
            raw -= 65536

        raw = raw * self._scale

        mapping = self._def.get("mapping")
        if mapping:
            return mapping.get(raw, raw)

        return raw

    @property
    def icon(self):
        if self._icon_map:
            raw = self.coordinator.data.get(self._register)
            return self._icon_map.get(raw, self._attr_icon)
        return self._attr_icon

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }
