import logging
import re
import asyncio
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
        self._bit = definition.get("bit")
        self._options_map = definition["options"]

        self._attr_name = definition["name"]

        if "unique_id" in definition:
            self._attr_unique_id = (
                f"{DOMAIN}_{model}_{definition['unique_id']}"
            )
        else:
            self._attr_unique_id = (
                f"{DOMAIN}_{model}_select_{self._register}"
            )

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
        self._attr_entity_registry_enabled_default = definition.get("entity_registry_enabled_default", True)

        # Zabezpieczenie przed samoczynnym zapisem podczas wczytywania integracji
        self._boot_zabezpieczony = False
        self.coordinator.hass.async_create_task(self._zdejmij_blokade_bootu())

    async def _zdejmij_blokade_bootu(self):
        """Zdejmuje blokadę zapisu dla platformy select po 15 sekundach od startu."""
        await asyncio.sleep(15.0)
        self._boot_zabezpieczony = True
        _LOGGER.info("Zgoda na zapis odblokowana dla encji select: %s", self._attr_name)

    @property
    def current_option(self):
        raw = self.coordinator.data.get(self._register)
        if raw is None:
            return None

        if self._bit is not None:
            raw = (raw >> self._bit) & 1

        return self._options_map.get(raw)

    async def async_select_option(self, option: str):
        """Bezpieczna zmiana opcji z uwzględnieniem masek bitowych (RMW) i kolejki rozgłoszeniowej."""
        if not self._boot_zabezpieczony:
            _LOGGER.warning(
                "Zablokowano samoczynną próbę zapisu opcji select podczas startu integracji dla %s [Model: %s]", 
                self._attr_name, self._model.upper().replace('_', '-')
            )
            return

        from .const import MODEL_PROTOCOLS, PROTOCOL_CUSTOM_BINARY_F4
        protocol_type = MODEL_PROTOCOLS.get(self._model, "standard_modbus")

        target_value = None
        for key, val in self._options_map.items():
            if val == option:
                target_value = key
                break

        if target_value is None:
            _LOGGER.error("Nie znaleziono wartości Modbus dla opcji: %s", option)
            return

        # 1. Obsługa dla SERII B (Tryb Read-Modify-Write przez bezpieczną kolejkę koordynatora - FC06)
        if protocol_type == PROTOCOL_CUSTOM_BINARY_F4 and self._bit is not None:
            current_reg_value = self.coordinator.data.get(self._register, 0)
            
            if target_value == 1:
                new_reg_value = current_reg_value | (1 << self._bit)
            else:
                new_reg_value = current_reg_value & ~(1 << self._bit)
                
            _LOGGER.debug(
                "Modyfikacja bitu %s w rejestrze %s dla serii B. Stara wartość: %s, Nowa wartość: %s",
                self._bit, self._register, current_reg_value, new_reg_value
            )
            await self.coordinator.async_execute_safe_write(
                self.coordinator.client.write_register,
                self._register,
                new_reg_value
            )
            return

        # 2. Zachowanie oryginalnej logiki dla starszych modeli Modbus (Zapis przez bezpieczną kolejkę)
        await self.coordinator.async_execute_safe_write(
            self.coordinator.client.write_register,
            self._register,
            target_value
        )



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
