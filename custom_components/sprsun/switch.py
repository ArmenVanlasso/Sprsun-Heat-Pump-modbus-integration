import logging
from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
import re

from .const import DOMAIN
from .coordinator import SprsunCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: SprsunCoordinator = data["coordinator"]
    client = data["client"]
    model: str = data["model"]

    switches_def = data["switches"]

    entities = [
        SprsunSwitchEntity(coordinator, client, entry.entry_id, model, definition)
        for definition in switches_def
    ]

    async_add_entities(entities)


class SprsunSwitchEntity(SwitchEntity):

    _attr_should_poll = False

    def __init__(self, coordinator, client, entry_id, model, definition):
        self.coordinator = coordinator
        self._client = client
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._register = definition.get("register", definition.get("address"))
        self._bit = definition.get("bit")
        
        self._cmd_on = definition.get("command_on", 1)
        self._cmd_off = definition.get("command_off", 0)
        self._attr_entity_registry_enabled_default = definition.get("entity_registry_enabled_default", True)

        self._icon_on = definition.get("icon_on")
        self._icon_off = definition.get("icon_off")

        self._verify = definition.get("verify")

        self._attr_name = definition["name"]
        
        if self._bit is not None:
            self._attr_unique_id = f"{DOMAIN}_{model}_switch_{self._register}_bit_{self._bit}"
        else:
            self._attr_unique_id = f"{DOMAIN}_{model}_switch_{self._register}"

        raw_slug = f"sprsun_{model}_{definition['name']}".lower()
        raw_slug = (
            raw_slug.replace("ą", "a").replace("ć", "c").replace("ę", "e")
               .replace("ł", "l").replace("ń", "n").replace("ó", "o")
               .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )
        slug = re.sub(r"[^a-z0-9_]", "_", raw_slug)
        slug = re.sub(r"_+", "_", slug)
        slug = slug.strip("_")
        self.entity_id = f"switch.{slug}"

        # Zabezpieczenie przed samoczynnym zapisem podczas wczytywania integracji
        self._boot_zabezpieczony = False
        self.coordinator.hass.async_create_task(self._zdejmij_blokade_bootu())

    async def _zdejmij_blokade_bootu(self):
        """Zdejmuje blokadę zapisu dla platformy switch po 15 sekundach od startu."""
        import asyncio
        await asyncio.sleep(15.0)
        self._boot_zabezpieczony = True
        _LOGGER.info("Zgoda na zapis odblokowana dla encji switch: %s", self._attr_name)

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def icon(self):
        return self._icon_on if self.is_on else self._icon_off

    @property
    def is_on(self) -> bool:
        from .const import MODEL_PROTOCOLS, PROTOCOL_CUSTOM_BINARY_F4
        protocol_type = MODEL_PROTOCOLS.get(self._model, "standard_modbus")

        if protocol_type == PROTOCOL_CUSTOM_BINARY_F4 and self._bit is not None:
            raw = self.coordinator.data.get(self._register)

            _LOGGER.warning(
                "SWITCH READ [%s] register=%s raw=%s bit=%s",
                self._attr_name,
                self._register,
                raw,
                self._bit,
            )

            if raw is None:
                return False

            bit_state = (raw >> self._bit) & 1

            return bool(bit_state) == bool(self._cmd_on)

        if not self._verify:
            raw = self.coordinator.data.get(1000 + self._register)
            return bool(raw) == bool(self._cmd_on)

        v = self._verify
        addr = v["address"]
        itype = v.get("input_type", "coil").lower()
        state_on = v.get("state_on", 1)
        state_off = v.get("state_off", 0)

        if itype == "discrete":
            raw = self.coordinator.data_coils.get(addr, False)
            return bool(raw) == bool(state_on)

        if itype == "coil":
            raw = self.coordinator.data.get(1000 + addr)
            return bool(raw) == bool(state_on)

        if itype == "holding":
            raw = self.coordinator.data.get(addr)
            return bool(raw) == bool(state_on)

        return False

    async def _write_value(self, value: int):
        """Zapis z uwzględnieniem RMW i bezpiecznej kolejki dla serii B lub FC5 dla starych pomp."""
        if not self._boot_zabezpieczony:
            _LOGGER.warning("Zablokowano samoczynną próbę zapisu przełącznika podczas startu integracji dla %s", self._attr_name)
            return

        from .const import MODEL_PROTOCOLS, PROTOCOL_CUSTOM_BINARY_F4
        protocol_type = MODEL_PROTOCOLS.get(self._model, "standard_modbus")

        try:
            # 1. Bezpieczny zapis Read-Modify-Write dla switchy bitowych zapisanych w rejestrach
            if self._bit is not None:
                current_reg_value = self.coordinator.data.get(self._register, 0)
                
                if value == self._cmd_on:
                    new_reg_value = current_reg_value | (1 << self._bit)
                else:
                    new_reg_value = current_reg_value & ~(1 << self._bit)
                    
                _LOGGER.debug(
                    "Modyfikacja bitu switcha %s w rejestrze %s dla serii B. Stara wartość: %s, Nowa wartość: %s",
                    self._bit, self._register, current_reg_value, new_reg_value
                )
                await self.coordinator.async_execute_safe_write(
                    self._client.write_register,
                    self._register,
                    new_reg_value
                )
            
            # 2. Oryginalny zapis przez kolejkę koordynatora (FC05) dla starszych modeli Modbus
            else:
                await self.coordinator.async_execute_safe_write(
                    self._client.write_coil,
                    self._register,
                    bool(value)
                )
                
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
