import logging
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import SprsunCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Rejestracja binary sensorów dla danego modelu i języka."""
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]
    lang: str = data["language"]

    # 🔥 Binary sensory z folderu model/lang
    sensors_def = data["binary_sensors"]

    entities = [
        SprsunBinarySensor(coordinator, entry.entry_id, model, definition)
        for definition in sensors_def
    ]

    # 🔥 Sensor aktywnych alarmów — z folderu modelowego (bez języka)
    try:
        model_folder = model.upper()

        module = __import__(
            f"custom_components.sprsun.models.{model_folder}.sensor_alarm",
            fromlist=["SprsunActiveAlarmsSensor"],
        )

        alarm_class = getattr(module, "SprsunActiveAlarmsSensor")
        alarm_sensor = alarm_class(coordinator, data["client"], entry.entry_id, model)
        entities.append(alarm_sensor)

    except Exception as err:
        _LOGGER.error("Nie udało się załadować sensora alarmów: %s", err)

    async_add_entities(entities)


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

        # nazwa encji — prosto z pliku model/lang
        self._attr_name = definition["name"]

        # unikalny ID
        self._attr_unique_id = f"{DOMAIN}_{model}_binary_{self._address}"

        # entity_id generowane z nazwy encji
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

    @property
    def icon(self):
        return self._icon_on if self.is_on else self._icon_off

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

    @property
    def extra_state_attributes(self):
        if not self._mapping:
            return None

        value = 1 if self.is_on else 0
        return {"description": self._mapping.get(value, "Nieznany")}

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }
