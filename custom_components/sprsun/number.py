import logging
import re
import os
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import SprsunCoordinator
from .lang_loader import TranslationLoader

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]
    lang: str = data["language"]

    numbers_def = data["numbers"]

    # ŁADOWANIE TŁUMACZEŃ
    integration_path = os.path.dirname(__file__)
    loader = TranslationLoader(integration_path)
    translations = await hass.async_add_executor_job(loader.load_language, lang)

    entities: list[NumberEntity] = []

    for definition in numbers_def:
        if "register" in definition:
            entities.append(
                SprsunNumberEntity(
                    coordinator,
                    entry.entry_id,
                    model,
                    definition,
                    translations,
                    loader
                )
            )

    async_add_entities(entities)


class SprsunNumberEntity(NumberEntity):
    _attr_should_poll = False

    def __init__(
        self,
        coordinator: SprsunCoordinator,
        entry_id: str,
        model: str,
        definition: dict,
        translations,
        loader,
    ) -> None:
        super().__init__()

        self.coordinator = coordinator
        self._entry_id = entry_id
        self._model = model
        self._def = definition
        self._loader = loader

        self._register = definition["register"]

        unique_id = definition["unique_id"]

        # TŁUMACZENIA
        t = loader.get_sensor_translation(translations, unique_id)

        translated_name = t.get("name", definition["name"])
        translated_entity_id = t.get("entity_id", unique_id)

        # NAZWA
        self._attr_name = translated_name

        # UNIQUE ID
        self._attr_unique_id = f"{DOMAIN}_{model}_number_{unique_id}"

        # ENTITY ID — poprawne slugowanie
        raw = f"sprsun_{model}_{translated_entity_id}".lower()

        raw = (
            raw.replace("ą", "a").replace("ć", "c").replace("ę", "e")
               .replace("ł", "l").replace("ń", "n").replace("ó", "o")
               .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )

        slug = re.sub(r"[^a-z0-9_]", "_", raw)
        slug = re.sub(r"_+", "_", slug)
        slug = slug.strip("_")

        self.entity_id = f"number.{slug}"

        # PARAMETRY NUMBER
        self._attr_native_min_value = definition["min"]
        self._attr_native_max_value = definition["max"]
        self._attr_native_step = definition["step"]
        self._attr_icon = definition.get("icon")
        self._attr_native_unit_of_measurement = definition.get("unit")

        mode = definition.get("mode", "slider")
        self._attr_mode = NumberMode.BOX if mode == "box" else NumberMode.SLIDER

        self._attr_available = True

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def native_value(self):
        return self.coordinator.data.get(self._register)

    async def async_set_native_value(self, value: float) -> None:
        try:
            await self.coordinator.client.write_register(self._register, int(value))
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Błąd zapisu number %s: %s", self._attr_name, err)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }
