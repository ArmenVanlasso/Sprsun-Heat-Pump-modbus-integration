import logging
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import SprsunCoordinator

# Import definicji binary sensorów per model
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
    """Rejestracja binary sensorów dla danego modelu."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]

    sensors_def = MODEL_BINARY_MAP.get(model, [])
    entities = [
        SprsunBinarySensor(coordinator, entry.entry_id, model, definition)
        for definition in sensors_def
    ]

    async_add_entities(entities)

    # Sensor aktywnych alarmów
    try:
        model_folder = model.replace("_", "").upper()

        module = __import__(
        f"custom_components.sprsun.models.{model_folder}.sensor_alarm",
        fromlist=["SprsunActiveAlarmsSensor"],
        )

        alarm_class = getattr(module, "SprsunActiveAlarmsSensor")
        alarm_sensor = alarm_class(coordinator, entry.entry_id, model)
        async_add_entities([alarm_sensor])
    except Exception as err:
        _LOGGER.error("Nie udało się załadować sensora alarmów: %s", err)


class SprsunBinarySensor(BinarySensorEntity):
    """Binary sensor oparty o koordynator i discrete inputs."""

    _attr_should_poll = False

    def __init__(self, coordinator: SprsunCoordinator, entry_id, model, definition):
        self.coordinator = coordinator
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._address = definition["address"]
        self._index = definition.get("index", 0)

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{model}_binary_{self._address}"

        slug = (
            f"sprsun_{model}_{definition['name']}"
            .lower()
            .replace(" ", "_")
            .replace("ą", "a").replace("ć", "c").replace("ę", "e")
            .replace("ł", "l").replace("ń", "n").replace("ó", "o")
            .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )
        self.entity_id = f"binary_sensor.{slug}"

        self._attr_device_class = definition.get("device_class")

        self._icon_on = definition.get("icon_on", "mdi:check-circle")
        self._icon_off = definition.get("icon_off", "mdi:alert-circle")

        self._mapping = definition.get("mapping", {})

        self._attr_available = True

    async def async_added_to_hass(self):
        """Aktualizacja przy każdej zmianie koordynatora."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    # ---------------------------------------------------------
    # IKONA
    # ---------------------------------------------------------

    @property
    def icon(self):
        return self._icon_on if self.is_on else self._icon_off

    # ---------------------------------------------------------
    # ODCZYT STANU
    # ---------------------------------------------------------

    @property
    def is_on(self):
        """Stan z discrete inputs."""
        bits = self.coordinator.data_discrete
        if bits is None:
            return False

        try:
            return bool(bits[self._address][self._index])
        except Exception:
            return False

    # ---------------------------------------------------------
    # DODATKOWE ATRYBUTY
    # ---------------------------------------------------------

    @property
    def extra_state_attributes(self):
        if not self._mapping:
            return None

        value = 1 if self.is_on else 0
        return {"description": self._mapping.get(value, "Nieznany")}

    # ---------------------------------------------------------
    # DEVICE INFO
    # ---------------------------------------------------------

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }
