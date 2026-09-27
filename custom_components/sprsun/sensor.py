import logging
import os
import importlib
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_change,
)

from .const import DOMAIN
from .coordinator import SprsunCoordinator
from .lang_loader import TranslationLoader

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    _LOGGER.warning("Sprsun sensor.py: START async_setup_entry dla entry_id=%s", entry.entry_id)

    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]
    lang: str = data["language"]

    sensors_def = data["sensors"]

    # -----------------------------------------------------
    # ŁADOWANIE TŁUMACZEŃ
    # -----------------------------------------------------
    integration_path = os.path.dirname(__file__)
    loader = TranslationLoader(integration_path)
    translations = await hass.async_add_executor_job(loader.load_language, lang)

    entities: list[SensorEntity] = []

    # -----------------------------------------------------
    # SENSORY MODBUS
    # -----------------------------------------------------
    for definition in sensors_def:
        entities.append(
            SprsunGenericSensor(
                coordinator,
                entry.entry_id,
                model,
                definition,
                translations,
                loader
            )
        )

    # -----------------------------------------------------
    # LOGIC SENSORS – dynamiczne z folderu modelowego
    # -----------------------------------------------------
    try:
        model_folder = model.upper()

        logic_module = await hass.async_add_executor_job(
            importlib.import_module,
            f"custom_components.sprsun.models.{model_folder}.logic_sensors"
        )

        logic_def = logic_module.logic_sensors

        for definition in logic_def:
            cls_name = definition["class"]

            try:
                cls = getattr(logic_module, cls_name)
            except Exception as e:
                _LOGGER.error("Sprsun sensor.py: NIE ZNALEZIONO klasy %s: %s", cls_name, e)
                continue

            try:
                args = definition.get("args", {})
                args["translations"] = translations
                args["loader"] = loader

                entity = cls(
                    entry_id=entry.entry_id,
                    model=model,
                    **args
                )
                entities.append(entity)

            except Exception as e:
                _LOGGER.error("Sprsun sensor.py: BŁĄD podczas tworzenia instancji %s: %s", cls_name, e)

    except Exception as err:
        _LOGGER.error("Sprsun sensor.py: Nie udało się załadować logic_sensors: %s", err)

    async_add_entities(entities)


# ============================================================
#  GENERIC SENSOR (Modbus)
# ============================================================

class SprsunGenericSensor(CoordinatorEntity, SensorEntity):
    _attr_should_poll = False

    def __init__(self, coordinator, entry_id, model, definition, translations, loader):
        super().__init__(coordinator)

        self.coordinator = coordinator
        self._entry_id = entry_id
        self._model = model
        self._def = definition
        self._loader = loader

        self._register = definition["register"]
        self._scale = definition.get("scale", 1)
        self._signed = definition.get("signed", False)

        unique_id = definition["unique_id"]

        # -----------------------------------------------------
        # TŁUMACZENIE SENSORA
        # -----------------------------------------------------
        t = loader.get_sensor_translation(translations, unique_id)

        translated_name = t.get("name", definition["name"])
        translated_entity_id = t.get("entity_id", unique_id)

        # -----------------------------------------------------
        # NAZWA ENCJI
        # -----------------------------------------------------
        self._attr_name = translated_name

        # -----------------------------------------------------
        # UNIQUE ID
        # -----------------------------------------------------
        self._attr_unique_id = f"{DOMAIN}_{model}_sensor_{unique_id}"

        # -----------------------------------------------------
        # ENTITY ID
        # -----------------------------------------------------
        slug = (
            f"sprsun_{model}_{translated_entity_id}"
            .lower()
            .replace(" ", "_")
        )
        self.entity_id = f"sensor.{slug}"

        # -----------------------------------------------------
        # MAPPINGI I IKONY
        # -----------------------------------------------------
        self._mapping = t.get("mapping", definition.get("mapping"))
        self._icon_map = t.get("icon_map", definition.get("icon_map"))

        self._attr_native_unit_of_measurement = definition.get("unit")
        self._attr_device_class = definition.get("device_class")
        self._attr_state_class = definition.get("state_class")
        self._attr_icon = definition.get("icon")

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }

    @property
    def native_value(self):
        raw = self.coordinator.data.get(self._register)

        if raw is None:
            return None

        if self._signed and raw > 32767:
            raw -= 65536

        raw = raw * self._scale

        if self._mapping:
            return self._mapping.get(str(raw), raw)

        return raw

    @property
    def icon(self):
        if self._icon_map:
            raw = self.coordinator.data.get(self._register)
            return self._icon_map.get(str(raw), self._attr_icon)
        return self._attr_icon
