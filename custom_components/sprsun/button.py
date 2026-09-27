import logging
from homeassistant.components.button import ButtonEntity
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
    """Rejestracja buttonów dla danego modelu i języka."""
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]

    # 🔥 Buttony z folderu model/lang
    buttons_def = data["buttons"]

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

        # nazwa encji — prosto z pliku model/lang
        self._attr_name = definition["name"]

        # unikalny ID
        self._attr_unique_id = f"{DOMAIN}_{model}_button_{self._register}"

        # ikona
        self._attr_icon = definition.get("icon", "mdi:gesture-tap-button")

        # entity_id generowane z nazwy encji
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
