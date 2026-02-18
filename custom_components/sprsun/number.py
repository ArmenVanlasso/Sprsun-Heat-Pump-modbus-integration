import logging
from datetime import datetime, timedelta

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import SprsunCoordinator

# Import definicji numberów per model
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


# ---------------------------------------------------------
# SETUP ENTRY
# ---------------------------------------------------------

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Rejestracja encji number dla danego modelu."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: SprsunCoordinator = data["coordinator"]
    model: str = data["model"]

    numbers_def = MODEL_NUMBERS_MAP.get(model, [])
    entities = []

    for definition in numbers_def:
        # Zwykły number (ma register)
        if "register" in definition:
            entities.append(
                SprsunNumberEntity(coordinator, entry.entry_id, model, definition)
            )
        else:
            # Licznik logiczny
            entities.append(
                SprsunCounterNumberEntity(coordinator, entry.entry_id, model, definition)
            )

    async_add_entities(entities)


# ---------------------------------------------------------
# NUMBER MODBUS
# ---------------------------------------------------------

class SprsunNumberEntity(NumberEntity):
    """Encja number oparta o koordynator i rejestry Modbus."""

    _attr_should_poll = False

    def __init__(self, coordinator: SprsunCoordinator, entry_id, model, definition):
        self.coordinator = coordinator
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._register = definition["register"]

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{model}_number_{self._register}"

        slug = (
            f"sprsun_{model}_{definition['name']}"
            .lower()
            .replace(" ", "_")
            .replace("ą", "a").replace("ć", "c").replace("ę", "e")
            .replace("ł", "l").replace("ń", "n").replace("ó", "o")
            .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )
        self.entity_id = f"number.{slug}"

        # Parametry liczbowe
        self._attr_native_min_value = definition["min"]
        self._attr_native_max_value = definition["max"]
        self._attr_native_step = definition["step"]
        self._attr_icon = definition.get("icon")
        self._attr_native_unit_of_measurement = definition.get("unit")

        mode = definition.get("mode", "slider")
        self._attr_mode = NumberMode.BOX if mode == "box" else NumberMode.SLIDER

        self._attr_available = True

    async def async_added_to_hass(self):
        """Aktualizacja przy każdej zmianie koordynatora."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def native_value(self):
        raw = self.coordinator.data.get(self._register)
        if raw is None:
            return None
        return raw

    async def async_set_native_value(self, value: float):
        try:
            await self.coordinator.client.write_register(self._register, int(value))
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Błąd zapisu number %s: %s", self._attr_name, err)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }


# ---------------------------------------------------------
# NUMBER COUNTER (LOGICZNY)
# ---------------------------------------------------------

class SprsunCounterNumberEntity(NumberEntity):
    """Licznik logiczny jako encja number."""

    _attr_should_poll = False

    def __init__(self, coordinator, entry_id, model, definition):
        self.coordinator = coordinator
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._key = definition["key"]
        self._condition = definition.get("condition")
        self._reset = definition.get("reset")

        self._value = 0
        self._last_reset = datetime.now()

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{model}_counter_{definition['unique_id']}"

        slug = (
            f"sprsun_{model}_{definition['unique_id']}"
            .lower()
            .replace(" ", "_")
        )
        self.entity_id = f"number.{slug}"

        self._attr_icon = definition.get("icon")
        self._attr_native_min_value = 0
        self._attr_native_max_value = 999999
        self._attr_native_step = 1
        self._attr_mode = NumberMode.BOX

        self._prev_179 = None
        self._prev_180 = None
        self._prev_11 = None
        self._defrost_active = False
        self._defrost_start = None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_update)
        )

    @property
    def native_value(self):
        return self._value

    async def async_set_native_value(self, value: float):
        """Pozwalamy użytkownikowi ręcznie zmienić licznik."""
        self._value = int(value)
        self.async_write_ha_state()

    def _handle_update(self):
        data = self.coordinator.data
        if not data:
            return

        now = datetime.now()

        # Resetowanie
        if self._reset == "daily" and now.date() != self._last_reset.date():
            self._value = 0
            self._last_reset = now

        if self._reset == "monthly" and now.month != self._last_reset.month:
            self._value = 0
            self._last_reset = now

        if self._reset == "yearly" and now.year != self._last_reset.year:
            self._value = 0
            self._last_reset = now

        reg179 = data.get(179, 0)
        reg180 = data.get(180, 0)
        reg11 = data.get(11, 0)

        # Sprężarka
        if self._condition == "sprezarka":
            if self._prev_179 == 0 and reg179 == 1:
                self._value += 1

        # Wentylator
        if self._condition == "wentylator":
            if self._prev_180 == 0 and reg180 == 1:
                self._value += 1

        # Defrost
        if self._condition == "sprezarka_i_wentylator":
            if reg180 == 0 and reg179 == 1:
                if not self._defrost_active:
                    self._defrost_active = True
                    self._defrost_start = now
                else:
                    if now - self._defrost_start >= timedelta(seconds=60):
                        self._value += 1
                        self._defrost_active = False
            else:
                self._defrost_active = False

        # Zawór 3D
        if self._key == "valve_count":
            if self._prev_11 is not None and reg11 != self._prev_11:
                self._value += 1

        # Zapamiętanie poprzednich wartości
        self._prev_179 = reg179
        self._prev_180 = reg180
        self._prev_11 = reg11

        self.async_write_ha_state()
