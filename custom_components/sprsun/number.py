import logging
from datetime import timedelta

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.config_entries import ConfigEntry

from .const import (
    DOMAIN,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)
from .modbus_client import HeatPumpModbusClient

from .models.CGK025V3L.numbers import ENTITIES as NUMBERS_025
from .models.CGK030V3L.numbers import ENTITIES as NUMBERS_030
from .models.CGK040V3L.numbers import ENTITIES as NUMBERS_040
from .models.CGK050V3L.numbers import ENTITIES as NUMBERS_050
from .models.CGK060V3L.numbers import ENTITIES as NUMBERS_060

_LOGGER = logging.getLogger(__name__)

MODEL_NUMBERS_MAP = {
    "cgk_025v3l": NUMBERS_025,
    "cgk_030v3l": NUMBERS_030,
    "cgk_040v3l": NUMBERS_040,
    "cgk_050v3l": NUMBERS_050,
    "cgk_060v3l": NUMBERS_060,
}


# ============================================================
#   KLASA ENCJI NUMBER (jedyna, centralna)
# ============================================================

class SprsunNumberEntity(NumberEntity):
    """Encja number obsługująca odczyt i zapis Modbus."""

    _attr_should_poll = False

    def __init__(
        self,
        client,
        entry_id,
        model,
        name,
        register,
        min_value,
        max_value,
        step,
        icon,
    ):
        self._client = client
        self._entry_id = entry_id
        self._model = model
        self._register = register

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
        self.entity_id = f"number.{slug}"

        self._attr_native_min_value = min_value
        self._attr_native_max_value = max_value
        self._attr_native_step = step
        self._attr_icon = icon
        self._attr_mode = NumberMode.SLIDER

        self._attr_native_value = None
        self._attr_available = True

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
                self._attr_native_value = value[0]
                self._attr_available = True
        except Exception:
            self._attr_available = False

    async def async_set_native_value(self, value: float):
        try:
            await self._client.write_register(self._register, int(value))
            self._attr_native_value = value
            self.async_write_ha_state()
        except Exception:
            self._attr_available = False


# ============================================================
#   ŁADOWANIE ENCJI NUMBER (centralny tryb)
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

    numbers_def = MODEL_NUMBERS_MAP.get(model)
    if numbers_def is None:
        _LOGGER.error("Brak zdefiniowanych number entities dla modelu: %s", model)
        return

    entities = []

    for definition in numbers_def:
        entities.append(
            SprsunNumberEntity(
                client,
                entry.entry_id,
                model,
                definition["name"],
                definition["register"],
                definition["min"],
                definition["max"],
                definition["step"],
                definition.get("icon"),
            )
        )

    async_add_entities(entities)

    async def _periodic_update(now):
        for entity in entities:
            try:
                await entity.async_update()
                entity.async_write_ha_state()
            except Exception as err:
                _LOGGER.error("Błąd aktualizacji encji number %s: %s", entity.name, err)

    async_track_time_interval(
        hass,
        _periodic_update,
        timedelta(seconds=scan_interval),
    )
