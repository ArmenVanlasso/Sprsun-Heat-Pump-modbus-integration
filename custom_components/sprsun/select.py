import logging
from datetime import timedelta

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
from .modbus_client import HeatPumpModbusClient

# Import definicji selectów per model
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


# ============================================================
#   KLASA ENCJI SELECT (centralna)
# ============================================================

class SprsunSelectEntity(SelectEntity):
    _attr_should_poll = False

    def __init__(
        self,
        client,
        entry_id,
        model,
        name,
        register,
        options_map,
        icon,
        icons_map,
    ):
        self._client = client
        self._entry_id = entry_id
        self._model = model
        self._register = register

        self._options_map = options_map
        self._reverse_map = {v: k for k, v in options_map.items()}

        self._icon_default = icon
        self._icons_map = icons_map or {}

        slug = (
            f"sprsun_{model}_{name}"
            .lower()
            .replace(" ", "_")
            .replace("ą", "a")
            .replace("ć", "c")
            .replace("ę", "e")
            .replace("ł", "l")
            .replace("ń", "n")
            .replace("ó", "o")
            .replace("ś", "s")
            .replace("ź", "z")
            .replace("ż", "z")
        )

        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{model}_{slug}"
        self.entity_id = f"select.{slug}"

        self._attr_options = list(options_map.values())
        self._attr_current_option = None
        self._attr_available = True

    @property
    def icon(self):
        if self._attr_current_option is None:
            return self._icon_default
        value = self._reverse_map.get(self._attr_current_option)
        return self._icons_map.get(value, self._icon_default)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }

    async def async_update(self):
        try:
            value = await self._client.read_holding_registers(self._register, 1)
            if value:
                mapped = self._options_map.get(value[0])
                if mapped:
                    self._attr_current_option = mapped
                self._attr_available = True
        except Exception:
            self._attr_available = False

    async def async_select_option(self, option: str):
        try:
            value = self._reverse_map.get(option)
            if value is not None:
                await self._client.write_register(self._register, value)
                self._attr_current_option = option
                self.async_write_ha_state()
        except Exception:
            self._attr_available = False


# ============================================================
#   ŁADOWANIE ENCJI SELECT (centralny tryb)
# ============================================================

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    data = hass.data[DOMAIN][entry.entry_id]
    client: HeatPumpModbusClient = data["client"]
    model: str = data["model"]

    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    selects_def = MODEL_SELECTS_MAP.get(model)
    if selects_def is None:
        _LOGGER.error("Brak zdefiniowanych select entities dla modelu: %s", model)
        return

    entities = []

    for definition in selects_def:
        entities.append(
            SprsunSelectEntity(
                client,
                entry.entry_id,
                model,
                definition["name"],
                definition["register"],
                definition["options"],
                definition.get("icon"),
                definition.get("icons"),
            )
        )

    async_add_entities(entities)

    async def _periodic_update(now):
        for entity in entities:
            try:
                await entity.async_update()
                entity.async_write_ha_state()
            except Exception as err:
                _LOGGER.error("Błąd aktualizacji encji select %s: %s", entity.name, err)

    async_track_time_interval(
        hass,
        _periodic_update,
        timedelta(seconds=scan_interval),
    )
