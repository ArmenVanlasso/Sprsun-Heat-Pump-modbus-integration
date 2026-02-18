import logging
from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import SprsunCoordinator

# Importy buttonów dla wszystkich modeli
from .models.CGK025V3L.buttons import ENTITIES as BUTTONS_025
from .models.CGK030V3L.buttons import ENTITIES as BUTTONS_030
from .models.CGK040V3L.buttons import ENTITIES as BUTTONS_040
from .models.CGK050V3L.buttons import ENTITIES as BUTTONS_050
from .models.CGK060V3L.buttons import ENTITIES as BUTTONS_060

_LOGGER = logging.getLogger(__name__)

MODEL_BUTTONS_MAP = {
    "cgk_025v3l": BUTTONS_025,
    "cgk_030v3l": BUTTONS_030,
    "cgk_040v3l": BUTTONS_040,
    "cgk_050v3l": BUTTONS_050,
    "cgk_060v3l": BUTTONS_060,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Rejestracja buttonów dla danego modelu."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]

    buttons_def = MODEL_BUTTONS_MAP.get(model, [])
    entities = [
        SprsunGenericButton(coordinator, entry.entry_id, model, definition)
        for definition in buttons_def
    ]

    async_add_entities(entities)


class SprsunGenericButton(ButtonEntity):
    """Button: zapis wartości 1 do rejestru Modbus."""

    _attr_should_poll = False

    def __init__(self, coordinator: SprsunCoordinator, entry_id, model, definition):
        self.coordinator = coordinator
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._register = definition["register"]

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{model}_button_{self._register}"
        self._attr_icon = definition.get("icon", "mdi:gesture-tap-button")

        slug = (
            f"sprsun_{model}_{definition['name']}"
            .lower()
            .replace(" ", "_")
            .replace("ą", "a").replace("ć", "c").replace("ę", "e")
            .replace("ł", "l").replace("ń", "n").replace("ó", "o")
            .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )
        self.entity_id = f"button.{slug}"

        self._attr_available = True

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }

    async def async_press(self) -> None:
        """Naciśnięcie przycisku = zapis 1 do rejestru."""
        try:
            await self.coordinator.client.write_register(self._register, 1)
            _LOGGER.info(
                "BUTTON %s: zapisano 1 do rejestru %s",
                self._attr_name,
                self._register,
            )
        except Exception as err:
            _LOGGER.error(
                "Błąd zapisu button %s (reg %s): %s",
                self._attr_name,
                self._register,
                err,
            )
            self._attr_available = False
