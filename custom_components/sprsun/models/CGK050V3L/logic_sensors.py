import logging
from datetime import timedelta, date

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_interval,
)

from ...const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def _parse_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _slugify(name: str) -> str:
    return (
        name.lower()
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


# ============================================================
#  BAZA TIMERÓW
# ============================================================

class SprsunBaseTimerSensor(RestoreEntity, SensorEntity):
    """Bazowa klasa dla sensorów czasu pracy."""

    _attr_should_poll = False
    _unit = "h"

    def __init__(self, name, unique_id, source_entity_id, reset_mode, entry_id, model):
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._source_entity_id = source_entity_id
        self._reset_mode = reset_mode
        self._entry_id = entry_id
        self._model = model

        self._seconds = 0.0
        self._last_reset = None
        self._unsub_interval = None

        slug = _slugify(name)
        self.entity_id = f"sensor.sprsun_{self._model}_{slug}"

    @property
    def native_unit_of_measurement(self):
        return self._unit

    @property
    def native_value(self):
        return round(self._seconds / 3600.0, 1)

    @property
    def extra_state_attributes(self):
        return {
            "seconds": self._seconds,
            "last_reset": self._last_reset.isoformat() if self._last_reset else None,
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        last_state = await self.async_get_last_state()
        if last_state:
            self._seconds = _parse_float(last_state.attributes.get("seconds"), 0.0)
            reset_str = last_state.attributes.get("last_reset")
            if reset_str:
                try:
                    self._last_reset = date.fromisoformat(reset_str)
                except Exception:
                    self._last_reset = None

        if self._last_reset is None:
            self._last_reset = date.today()

        self._unsub_interval = async_track_time_interval(
            self.hass, self._handle_interval, timedelta(seconds=60)
        )

    async def async_will_remove_from_hass(self):
        if self._unsub_interval:
            self._unsub_interval()
            self._unsub_interval = None

    async def _handle_interval(self, now):
        await self._maybe_reset(now.date())

        state = self.hass.states.get(self._source_entity_id)
        if state and state.state == "on":
            self._seconds += 60.0
            self.async_write_ha_state()

    async def _maybe_reset(self, today: date):
        if self._reset_mode == "total":
            return

        do_reset = False

        if self._reset_mode == "daily":
            if today > self._last_reset:
                do_reset = True

        elif self._reset_mode == "monthly":
            if (today.year, today.month) != (self._last_reset.year, self._last_reset.month):
                do_reset = True

        elif self._reset_mode == "yearly":
            if today.year != self._last_reset.year:
                do_reset = True

        if do_reset:
            self._seconds = 0.0
            self._last_reset = today
            self.async_write_ha_state()


# ============================================================
#  TIMER SPRĘŻARKI
# ============================================================

class SprsunCompressorRuntimeSensor(SprsunBaseTimerSensor):
    def __init__(self, name, unique_id, reset_mode, entry_id, model):
        super().__init__(
            name,
            unique_id,
            f"binary_sensor.sprsun_{model}_sprezarka",
            reset_mode,
            entry_id,
            model,
        )

    @property
    def icon(self):
        return "mdi:bag-personal"


# ============================================================
#  TIMER WENTYLATORA
# ============================================================

class SprsunFanRuntimeSensor(SprsunBaseTimerSensor):
    def __init__(self, name, unique_id, reset_mode, entry_id, model):
        super().__init__(
            name,
            unique_id,
            f"binary_sensor.sprsun_{model}_wentylator",
            reset_mode,
            entry_id,
            model,
        )

    @property
    def icon(self):
        return "mdi:fan"


# ============================================================
#  BAZA LICZNIKÓW
# ============================================================

class SprsunBaseCounterSensor(RestoreEntity, SensorEntity):
    _attr_should_poll = False

    def __init__(self, name, unique_id, reset_mode, entry_id, model):
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._reset_mode = reset_mode
        self._entry_id = entry_id
        self._model = model

        self._count = 0
        self._last_reset = None

        slug = _slugify(name)
        self.entity_id = f"sensor.sprsun_{self._model}_{slug}"

    @property
    def native_unit_of_measurement(self):
        return "count"

    @property
    def native_value(self):
        return self._count

    @property
    def extra_state_attributes(self):
        return {
            "last_reset": self._last_reset.isoformat() if self._last_reset else None,
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        last_state = await self.async_get_last_state()
        if last_state:
            self._count = _parse_int(last_state.state, 0)
            reset_str = last_state.attributes.get("last_reset")
            if reset_str:
                try:
                    self._last_reset = date.fromisoformat(reset_str)
                except Exception:
                    self._last_reset = None

        if self._last_reset is None:
            self._last_reset = date.today()

        async_track_time_interval(
            self.hass, self._handle_interval, timedelta(hours=1)
        )

    async def _handle_interval(self, now):
        await self._maybe_reset(now.date())

    async def _maybe_reset(self, today: date):
        if self._reset_mode == "total":
            return

        do_reset = False

        if self._reset_mode == "daily":
            if today > self._last_reset:
                do_reset = True

        elif self._reset_mode == "monthly":
            if (today.year, today.month) != (self._last_reset.year, self._last_reset.month):
                do_reset = True

        elif self._reset_mode == "yearly":
            if today.year != self._last_reset.year:
                do_reset = True

        if do_reset:
            self._count = 0
            self._last_reset = today
            self.async_write_ha_state()

    def _increment_safe(self):
        self._count = int(self._count) + 1
        self.async_write_ha_state()


# ============================================================
#  LICZNIK STARTÓW SPRĘŻARKI
# ============================================================

class SprsunCompressorStartCounter(SprsunBaseCounterSensor):
    def __init__(self, name, unique_id, reset_mode, entry_id, model):
        super().__init__(name, unique_id, reset_mode, entry_id, model)
        self._unsub = None
        self._compressor_entity = f"binary_sensor.sprsun_{model}_sprezarka"

    @property
    def icon(self):
        return "mdi:bag-personal"

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        self._unsub = async_track_state_change_event(
            self.hass, [self._compressor_entity], self._handle_change
        )

    async def async_will_remove_from_hass(self):
        if self._unsub:
            self._unsub()
            self._unsub = None

    @callback
    async def _handle_change(self, event):
        old = event.data.get("old_state")
        new = event.data.get("new_state")

        if old and new and old.state != "on" and new.state == "on":
            self._increment_safe()


# ============================================================
#  LICZNIK DEFROSTÓW
# ============================================================

class SprsunDefrostCounter(SprsunBaseCounterSensor):
    def __init__(self, name, unique_id, reset_mode, entry_id, model):
        super().__init__(name, unique_id, reset_mode, entry_id, model)
        self._unsub_interval = None
        self._condition_active = False

        self._compressor_entity = f"binary_sensor.sprsun_{model}_sprezarka"
        self._fan_entity = f"binary_sensor.sprsun_{model}_wentylator"

    @property
    def icon(self):
        return "mdi:snowflake-melt"

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        self._unsub_interval = async_track_time_interval(
            self.hass, self._handle_interval_defrost, timedelta(seconds=60)
        )

    async def async_will_remove_from_hass(self):
        if self._unsub_interval:
            self._unsub_interval()
            self._unsub_interval = None

    async def _handle_interval_defrost(self, now):
        await self._maybe_reset(now.date())

        compressor = self.hass.states.get(self._compressor_entity)
        fan = self.hass.states.get(self._fan_entity)

        if not compressor or not fan:
            self._condition_active = False
            return

        cond = (compressor.state == "on" and fan.state == "off")

        if cond and not self._condition_active:
            self._increment_safe()
            self._condition_active = True
        elif not cond:
            self._condition_active = False


# ============================================================
#  DNI POSIADANIA POMPY
# ============================================================

class SprsunOwnershipDaysSensor(RestoreEntity, SensorEntity):
    _attr_should_poll = False

    def __init__(self, name, unique_id, entry_id, model):
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._entry_id = entry_id
        self._model = model
        self._first_seen = None

        slug = _slugify(name)
        self.entity_id = f"sensor.sprsun_{self._model}_{slug}"

    @property
    def native_unit_of_measurement(self):
        return "d"

    @property
    def native_value(self):
        if not self._first_seen:
            return 0
        return (date.today() - self._first_seen).days

    @property
    def extra_state_attributes(self):
        return {
            "first_seen": self._first_seen.isoformat() if self._first_seen else None,
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }

    @property
    def icon(self):
        return "mdi:heat-pump"

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        last = await self.async_get_last_state()
        if last:
            fs = last.attributes.get("first_seen")
            if fs:
                try:
                    self._first_seen = date.fromisoformat(fs)
                except Exception:
                    self._first_seen = None

        if not self._first_seen:
            self._first_seen = date.today()

        self.async_write_ha_state()
