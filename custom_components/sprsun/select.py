import logging
import re
from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SprsunCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Rejestracja selectów dla danego modelu i języka."""
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]

    selects_def = data["selects"]

    entities = [
        SprsunGenericSelect(
            coordinator=coordinator,
            entry_id=entry.entry_id,
            model=model,
            definition=definition,
        )
        for definition in selects_def
    ]

    async_add_entities(entities)


class SprsunGenericSelect(CoordinatorEntity, SelectEntity):
    """Select oparty o rejestry Modbus."""

    _attr_should_poll = False

    def __init__(self, coordinator, entry_id, model, definition):
        super().__init__(coordinator)

        self.coordinator = coordinator
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._register = definition["register"]
        self._options_map = definition["options"]

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{model}_select_{self._register}"

        raw = f"sprsun_{model}_{definition['name']}".lower()
        raw = (
            raw.replace("ą", "a").replace("ć", "c").replace("ę", "e")
               .replace("ł", "l").replace("ń", "n").replace("ó", "o")
               .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )
        slug = re.sub(r"[^a-z0-9_]", "_", raw)
        slug = re.sub(r"_+", "_", slug)
        slug = slug.strip("_")
        self.entity_id = f"select.{slug}"

        self._attr_options = list(self._options_map.values())

        self._icons = definition.get("icons")
        self._attr_icon = definition.get("icon")

    @property
    def current_option(self):
        raw = self.coordinator.data.get(self._register)
        if raw is None:
            return None
        return self._options_map.get(raw)

    async def async_select_option(self, option: str):
        # znajdź klucz (wartość Modbus) dla wybranej opcji
        for key, val in self._options_map.items():
            if val == option:
                await self.coordinator.client.write_register(self._register, key)
                return

    @property
    def icon(self):
        if self._icons:
            raw = self.coordinator.data.get(self._register)
            return self._icons.get(raw, self._attr_icon)
        return self._attr_icon

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }
