import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import SprsunCoordinator

# modele
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
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: SprsunCoordinator = data["coordinator"]
    client = data["client"]
    model: str = data["model"]

    switches_def = MODEL_SWITCHES_MAP.get(model.lower(), [])
    entities = [
        SprsunSwitchEntity(coordinator, client, entry.entry_id, model, definition)
        for definition in switches_def
    ]

    async_add_entities(entities)


class SprsunSwitchEntity(SwitchEntity):
    """Switch oparty o koordynator i rejestry Modbus."""

    _attr_should_poll = False

    def __init__(self, coordinator, client, entry_id, model, definition):
        self.coordinator = coordinator
        self._client = client
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._register = definition["address"]
        self._cmd_on = definition.get("command_on", 1)
        self._cmd_off = definition.get("command_off", 0)

        self._icon_on = definition.get("icon_on")
        self._icon_off = definition.get("icon_off")

        self._verify = definition.get("verify")

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

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def icon(self):
        return self._icon_on if self.is_on else self._icon_off

    @property
    def is_on(self) -> bool:
        """Stan włącznika z verify lub fallback."""
        if not self._verify:
            v = self.coordinator.data.get(1000 + self._register)
            return bool(v) == bool(self._cmd_on)          # ← NEW  (dla 1/0 lub True/False)

        v_dict      = self._verify
        addr        = v_dict["address"]
        itype       = v_dict.get("input_type", "coil").lower()
        state_on    = v_dict.get("state_on", 1)
        state_off   = v_dict.get("state_off", 0)

        if itype == "discrete":
            raw = self.coordinator.data_coils.get(addr, False)
            return bool(raw) == bool(state_on)          # ← NEW

        if itype == "coil":
            raw = self.coordinator.data.get(1000 + addr)
            return bool(raw) == bool(state_on)          # ← NEW

        if itype == "holding":
            raw = self.coordinator.data.get(addr)
            return bool(raw) == bool(state_on)          # ← NEW

        return False

    async def _write_value(self, value: int):
        """Zapis przez FC5 (coil), nie FC6 (holding)."""
        try:
            await self._client.write_coil(self._register, bool(value))
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Błąd zapisu switch %s: %s", self._attr_name, err)

    async def async_turn_on(self, **kwargs):
        await self._write_value(self._cmd_on)

    async def async_turn_off(self, **kwargs):
        await self._write_value(self._cmd_off)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }
