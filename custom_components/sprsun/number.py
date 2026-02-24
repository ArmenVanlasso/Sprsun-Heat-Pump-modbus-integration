import logging
from datetime import datetime

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_change,
)

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
    entities: list[NumberEntity] = []

    for definition in numbers_def:
        # Encje oparte o Modbus (mają "register")
        if "register" in definition:
            entities.append(
                SprsunNumberEntity(coordinator, entry.entry_id, model, definition)
            )
        # Liczniki logiczne (nie mają "register")
        else:
            entities.append(
                SprsunCounterNumberEntity(hass, entry.entry_id, model, definition)
            )

    async_add_entities(entities)


# ---------------------------------------------------------
# NUMBER MODBUS
# ---------------------------------------------------------


class SprsunNumberEntity(NumberEntity):
    """Encja number oparta o koordynator i rejestry Modbus."""

    _attr_should_poll = False

    def __init__(
        self,
        coordinator: SprsunCoordinator,
        entry_id: str,
        model: str,
        definition: dict,
    ) -> None:
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

        self.entity_id = f"sensor.{slug}"
        self._attr_native_min_value = definition["min"]
        self._attr_native_max_value = definition["max"]
        self._attr_native_step = definition["step"]
        self._attr_icon = definition.get("icon")
        self._attr_native_unit_of_measurement = definition.get("unit")

        mode = definition.get("mode", "slider")
        self._attr_mode = NumberMode.BOX if mode == "box" else NumberMode.SLIDER

        self._attr_available = True

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def native_value(self):
        return self.coordinator.data.get(self._register)

    async def async_set_native_value(self, value: float) -> None:
        try:
            await self.coordinator.client.write_register(self._register, int(value))
            await self.coordinator.async_request_refresh()
        except Exception as err:  # pylint: disable=broad-except
            _LOGGER.error("Błąd zapisu number %s: %s", self._attr_name, err)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace("_", "-"),
        }


# ---------------------------------------------------------
# NUMBER COUNTER (LOGICZNY OPARTY O SENSORY HA)
# ---------------------------------------------------------


class SprsunCounterNumberEntity(NumberEntity, RestoreEntity):
    """Licznik logiczny oparty o istniejące sensory HA."""

    _attr_should_poll = False
    _attr_native_min_value = 0
    _attr_native_max_value = 999999
    _attr_native_step = 1
    _attr_mode = NumberMode.BOX

    def __init__(self, hass: HomeAssistant, entry_id: str, model: str, definition: dict):
        self.hass = hass
        self._entry_id = entry_id
        self._model = model
        self._def = definition

        self._key = definition["key"]
        self._reset = definition.get("reset")  # None / daily / monthly / yearly

        # Źródła danych – zamiana <model> na faktyczny model
        raw_src = definition.get("source_sensor")
        self._source_sensor = (
            raw_src.replace("<model>", self._model)
            if raw_src and "<model>" in raw_src
            else raw_src
        )

        raw_sp = definition.get("source_sensor_sprezarka")
        self._source_sensor_sprezarka = (
            raw_sp.replace("<model>", self._model)
            if raw_sp and "<model>" in raw_sp
            else raw_sp
        )

        raw_we = definition.get("source_sensor_wentylator")
        self._source_sensor_wentylator = (
            raw_we.replace("<model>", self._model)
            if raw_we and "<model>" in raw_we
            else raw_we
        )

        self._value: int = 0

        # Atrybuty defrostu (detekcja sekwencji)
        self._defrost_active: bool = False
        self._defrost_start: datetime | None = None

        # Unsubscribery
        self._unsub_state = None
        self._unsub_defrost = None

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{model}_counter_{definition['unique_id']}"
        self._attr_icon = definition.get("icon")

        # state_class – tylko total jest total_increasing
        if self._reset is None:
            # total – nie resetuje się, może być total_increasing
            self._attr_state_class = "total_increasing"
        else:
            # daily/monthly/yearly – resetuje się do 0, więc NIE total_increasing
            self._attr_state_class = None

    async def async_added_to_hass(self) -> None:
        """Przywróć stan i podłącz subskrypcje."""
        await super().async_added_to_hass()

        # Przywrócenie ostatniego stanu
        last_state = await self.async_get_last_state()
        if last_state is not None:
            try:
                self._value = int(float(last_state.state))
            except Exception:  # pylint: disable=broad-except
                self._value = 0

        self._attr_native_value = self._value
        self.async_write_ha_state()

        # Subskrypcja zmian stanu dla prostych liczników (sprężarka, wentylator, zawór)
        if self._source_sensor:
            self._unsub_state = async_track_state_change_event(
                self.hass,
                [self._source_sensor],
                self._handle_state_change,
            )

        # Subskrypcja zmian stanu dla defrostu (sprężarka + wentylator)
        if self._source_sensor_sprezarka and self._source_sensor_wentylator:
            self._unsub_defrost = async_track_state_change_event(
                self.hass,
                [
                    self._source_sensor_sprezarka,
                    self._source_sensor_wentylator,
                ],
                self._handle_defrost_state_change,
            )

        # Harmonogram resetu liczników (daily / monthly / yearly)
        if self._reset in ("daily", "monthly", "yearly"):
            async_track_time_change(
                self.hass,
                self._handle_reset_time_event,
                hour=0,
                minute=0,
                second=0,
            )

    async def async_will_remove_from_hass(self) -> None:
        """Czyszczenie subskrypcji przy usuwaniu encji."""
        if self._unsub_state:
            self._unsub_state()
            self._unsub_state = None
        if self._unsub_defrost:
            self._unsub_defrost()
            self._unsub_defrost = None

    @property
    def native_value(self):
        return self._value

    async def async_set_native_value(self, value: float) -> None:
        """Ręczne ustawienie licznika (np. korekta przez użytkownika)."""
        self._value = int(value)
        self._attr_native_value = self._value
        self.async_write_ha_state()

    # -----------------------------------------------------
    # RESET LICZNIKÓW: daily / monthly / yearly
    # -----------------------------------------------------

    async def _handle_reset_time_event(self, now: datetime) -> None:
        """Wywoływane codziennie o północy – na tej podstawie robimy reset."""
        if self._reset == "daily":
            # reset codziennie o północy
            self._value = 0
        elif self._reset == "monthly":
            # reset pierwszego dnia miesiąca
            if now.day != 1:
                return
            self._value = 0
        elif self._reset == "yearly":
            # reset pierwszego dnia roku
            if not (now.month == 1 and now.day == 1):
                return
            self._value = 0
        else:
            # brak resetu
            return

        self._attr_native_value = self._value
        self.async_write_ha_state()

    # -----------------------------------------------------
    # PROSTE LICZNIKI: SPRĘŻARKA / WENTYLATOR / ZAWÓR 3D
    # -----------------------------------------------------

    async def _handle_state_change(self, event) -> None:
        """Zliczanie przejść OFF → ON dla pojedynczego sensora."""
        new = event.data.get("new_state")
        old = event.data.get("old_state")

        if not new or not old:
            return

        if old.state == "off" and new.state == "on":
            self._value += 1
            self._attr_native_value = self._value
            self.async_write_ha_state()

    # -----------------------------------------------------
    # LICZNIK DEFROSTÓW
    # -----------------------------------------------------

    async def _handle_defrost_state_change(self, event) -> None:
        """
        Detekcja defrostu:
        - Defrost trwa, gdy sprężarka == on i wentylator == off
        - Jeden pełny cykl: wejście w stan (on/off) i późniejszy powrót
          do jakiegokolwiek innego stanu.
        """
        now = datetime.now()

        sp = self.hass.states.get(self._source_sensor_sprezarka)
        we = self.hass.states.get(self._source_sensor_wentylator)

        if not sp or not we:
            return

        sp_on = sp.state == "on"
        we_off = we.state == "off"

        # Jesteśmy w potencjalnym defroście: sprężarka ON, wentylator OFF
        if sp_on and we_off:
            if not self._defrost_active:
                # Start defrostu
                self._defrost_active = True
                self._defrost_start = now
            # Jeśli już aktywny, nie robimy nic – czekamy na koniec
            return

        # Wychodzimy z warunku defrostu
        if self._defrost_active:
            # Możesz tu opcjonalnie dodać warunek minimalnego czasu trwania,
            # np. jeśli defrost trwał > 60 s:
            if self._defrost_start and (now - self._defrost_start).total_seconds() >= 60:
                self._value += 1
                self._attr_native_value = self._value
                self.async_write_ha_state()

        # Zawsze resetujemy stan pomocniczy przy wyjściu
        self._defrost_active = False
        self._defrost_start = None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace("_", "-"),
        }
