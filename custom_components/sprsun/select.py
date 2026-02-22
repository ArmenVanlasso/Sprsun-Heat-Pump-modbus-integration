import logging
from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import SprsunCoordinator

# Importy selectów modelowych
from .models.CGK025V3L.selects import ENTITIES as SELECTS_025
from .models.CGK030V3L.selects import ENTITIES as SELECTS_030
from .models.CGK040V3L.selects import ENTITIES as SELECTS_040
from .models.CGK050V3L.selects import ENTITIES as SELECTS_050
from .models.CGK060V3L.selects import ENTITIES as SELECTS_060

_LOGGER = logging.getLogger(__name__)

MODEL_SELECTS_MAP = {
    "cgk_025v3l": SELECTS_025,
    "cgk_030v3l": SELECTS_030,
    "cgk_040v3l": SELECTS_040,
    "cgk_050v3l": SELECTS_050,
    "cgk_060v3l": SELECTS_060,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Rejestracja selectów dla danego modelu."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]

    selects_def = MODEL_SELECTS_MAP.get(model, [])
    entities = [
        SprsunGenericSelect(coordinator, entry.entry_id, model, definition)
        for definition in selects_def
    ]

    async_add_entities(entities)


class SprsunGenericSelect(SelectEntity):
    """Select oparty o koordynator i rejestry Modbus."""

    _attr_should_poll = False

    def __init__(self, coordinator: SprsunCoordinator, entry_id, model, definition):
        self.coordinator = coordinator
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._register = definition["register"]
        self._options_map = definition["options"]
        self._reverse_map = {v: k for k, v in self._options_map.items()}

        self._icon = definition.get("icon")
        self._icons = definition.get("icons")

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{model}_select_{self._register}"

        slug = (
            f"sprsun_{model}_{definition['name']}"
            .lower()
            .replace(" ", "_")
            .replace("ą", "a").replace("ć", "c").replace("ę", "e")
            .replace("ł", "l").replace("ń", "n").replace("ó", "o")
            .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )

        self._attr_options = list(self._options_map.values())
        self._attr_current_option = None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }

    async def async_added_to_hass(self):
        """Aktualizacja przy każdej zmianie koordynatora."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    # ---------------------------------------------------------
    # IKONY
    # ---------------------------------------------------------

    @property
    def icon(self):
        """Ikona zależna od opcji lub stała."""
        if self._icons and self._attr_current_option:
            raw = self._reverse_map.get(self._attr_current_option)
            return self._icons.get(raw, self._icon)
        return self._icon

    # ---------------------------------------------------------
    # ODCZYT WARTOŚCI
    # ---------------------------------------------------------

    @property
    def current_option(self):
        """Aktualna opcja selecta."""
        raw = self.coordinator.data.get(self._register)
        if raw is None:
            return None
        return self._options_map.get(raw)

    # ---------------------------------------------------------
    # ZAPIS WARTOŚCI
    # ---------------------------------------------------------

    async def async_select_option(self, option: str) -> None:
        """Zapis wybranej opcji do rejestru Modbus."""
        raw_value = self._reverse_map.get(option)
        if raw_value is None:
            return

        try:
            await self.coordinator.client.write_register(self._register, raw_value)
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Błąd zapisu select %s: %s", self._attr_name, err)
