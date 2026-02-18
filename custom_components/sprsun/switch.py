import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import SprsunCoordinator

# Import definicji switchy per model
from .models.CGK025V3L.switches import ENTITIES as SWITCHES_025
from .models.CGK030V3L.switches import ENTITIES as SWITCHES_030
from .models.CGK040V3L.switches import ENTITIES as SWITCHES_040
from .models.CGK050V3L.switches import ENTITIES as SWITCHES_050
from .models.CGK060V3L.switches import ENTITIES as SWITCHES_060

_LOGGER = logging.getLogger(__name__)

MODEL_SWITCHES_MAP = {
    "cgk_025v3l": SWITCHES_025,
    "cgk_030v3l": SWITCHES_030,
    "cgk_040v3l": SWITCHES_040,
    "cgk_050v3l": SWITCHES_050,
    "cgk_060v3l": SWITCHES_060,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Rejestracja switchy dla danego modelu."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]

    switches_def = MODEL_SWITCHES_MAP.get(model, [])
    entities = [
        SprsunSwitchEntity(coordinator, entry.entry_id, model, definition)
        for definition in switches_def
    ]

    async_add_entities(entities)


class SprsunSwitchEntity(SwitchEntity):
    """Switch oparty o koordynator i rejestry Modbus."""

    _attr_should_poll = False

    def __init__(self, coordinator: SprsunCoordinator, entry_id, model, definition):
        self.coordinator = coordinator
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._register = definition["register"]
        self._icon_on = definition.get("icon_on")
        self._icon_off = definition.get("icon_off")

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{model}_switch_{self._register}"

        slug = (
            f"sprsun_{model}_{definition['name']}"
            .lower()
            .replace(" ", "_")
            .replace("ą", "a").replace("ć", "c").replace("ę", "e")
            .replace("ł", "l").replace("ń", "n").replace("ó", "o")
            .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )
        self.entity_id = f"switch.{slug}"

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
        raw = self.coordinator.data.get(self._register)
        if raw is None:
            return False
        return bool(raw)

    # ---------------------------------------------------------
    # ZAPIS STANU
    # ---------------------------------------------------------

    async def async_turn_on(self, **kwargs):
        try:
            await self.coordinator.client.write_register(self._register, 1)
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Błąd zapisu switch %s: %s", self._attr_name, err)

    async def async_turn_off(self, **kwargs):
        try:
            await self.coordinator.client.write_register(self._register, 0)
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Błąd zapisu switch %s: %s", self._attr_name, err)

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
