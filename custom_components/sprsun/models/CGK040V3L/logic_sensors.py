import logging
from datetime import timedelta, date, datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import callback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.event import (
    async_track_state_change_event,
    async_track_time_interval,
    async_track_time_change,
)
from homeassistant.util import dt as dt_util
from custom_components.sprsun.const import (
    DOMAIN,
    CONF_SET_FAN_HOURS,
    CONF_FAN_HOURS,
    CONF_SET_COMPRESSOR_HOURS,
    CONF_COMPRESSOR_HOURS,
)
from custom_components.sprsun.lang_loader import TranslationLoader

_LOGGER = logging.getLogger(__name__)
_LOGGER.warning("Sprsun logic_sensors.py: plik został załadowany")


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
    _attr_should_poll = False
    _unit = "h"

    def __init__(self, name, unique_id, source_entity_id, reset_mode, entry_id, model, translations, loader, icon=None):
        _LOGGER.warning(
            "Tworzę timer: %s (model=%s, reset=%s, source=%s)",
            name,
            model,
            reset_mode,
            source_entity_id,
        )
        self._entry_id = entry_id
        self._model = model
        self._reset_mode = reset_mode
        self._source_entity_id_template = source_entity_id
        self._icon = icon
        self._attr_icon = icon
        t = loader.get_sensor_translation(translations, unique_id)
        translated_name = t.get("name", name)
        translated_entity_id = t.get("entity_id", unique_id)
        self._attr_name = translated_name
        self._attr_unique_id = unique_id
        slug = _slugify(translated_entity_id)
        self.entity_id = f"sensor.sprsun_{self._model.lower()}_{slug}"
        self._seconds = 0.0
        self._last_reset = None
        self._unsub_interval = None

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
            "model": self._model.upper().replace("_", "-"),
        }

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self._source_entity_id = self._source_entity_id_template.replace("<model>", self._model)
        data = self.hass.data[DOMAIN][self._entry_id]
        last_state = await self.async_get_last_state()

        if last_state:
            self._seconds = _parse_float(last_state.attributes.get("seconds"), 0.0)
            if "fan" in self._attr_unique_id and data.get(CONF_SET_FAN_HOURS, False):
                offset = int(data.get(CONF_FAN_HOURS, 0)) * 3600
                self._seconds = max(self._seconds, offset)
            if "compressor" in self._attr_unique_id and data.get(CONF_SET_COMPRESSOR_HOURS, False):
                offset = int(data.get(CONF_COMPRESSOR_HOURS, 0)) * 3600
                self._seconds = max(self._seconds, offset)
            reset_str = last_state.attributes.get("last_reset")
            if reset_str:
                try:
                    self._last_reset = date.fromisoformat(reset_str)
                except Exception:
                    self._last_reset = None
        else:
            offset_seconds = 0
            if "fan" in self._attr_unique_id and data.get(CONF_SET_FAN_HOURS, False):
                offset_seconds = int(data.get(CONF_FAN_HOURS, 0)) * 3600
            if "compressor" in self._attr_unique_id and data.get(CONF_SET_COMPRESSOR_HOURS, False):
                offset_seconds = int(data.get(CONF_COMPRESSOR_HOURS, 0)) * 3600
            self._seconds = offset_seconds

        if self._last_reset is None:
            self._last_reset = date.today()

        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                self._handle_interval,
                timedelta(seconds=60),
            )
        )

        # Reset dokładnie o północy czasu Home Assistant.
        if self._reset_mode == "daily":
            self.async_on_remove(
                async_track_time_change(
                    self.hass,
                    self._scheduled_reset,
                    hour=0,
                    minute=0,
                    second=0,
                )
            )

    async def _handle_interval(self, now):
        await self._maybe_reset(now.date())

        state = self.hass.states.get(self._source_entity_id)

        if state and state.state == "on":
            self._seconds += 60.0
            self.async_write_ha_state()

    async def _scheduled_reset(self, now):
        """Reset czasu pracy na granicy okresu."""
        today = now.date()
        last = self._last_reset

        if self._reset_mode == "daily":
            should_reset = last is None or last != today
        elif self._reset_mode == "monthly":
            should_reset = (
                last is None
                or (last.year, last.month) != (today.year, today.month)
            )
        elif self._reset_mode == "yearly":
            should_reset = last is None or last.year != today.year
        else:
            # Total nigdy nie resetuje się automatycznie.
            should_reset = False

        if should_reset:
            self._seconds = 0.0
            self._last_reset = today
            self.async_write_ha_state()

    async def _maybe_reset(self, today: date):
        """Zabezpieczenie, gdy Home Assistant był wyłączony o północy."""
        last = self._last_reset

        if self._reset_mode == "total":
            return

        if self._reset_mode == "daily":
            should_reset = last is None or today > last
        elif self._reset_mode == "monthly":
            should_reset = (
                last is None
                or (today.year, today.month) != (last.year, last.month)
            )
        elif self._reset_mode == "yearly":
            should_reset = last is None or today.year != last.year
        else:
            should_reset = False

        if should_reset:
            self._seconds = 0.0
            self._last_reset = today
            self.async_write_ha_state()


# ============================================================
#  TIMER SPRĘŻARKI
# ============================================================
class SprsunCompressorRuntimeSensor(SprsunBaseTimerSensor):
    def __init__(self, name, unique_id, reset_mode, entry_id, model, translations, loader, icon=None):
        super().__init__(
            name,
            unique_id,
            "binary_sensor.sprsun_<model>_sprezarka",
            reset_mode,
            entry_id,
            model,
            translations,
            loader,
            icon,
        )


# ============================================================
#  TIMER WENTYLATORA
# ============================================================
class SprsunFanRuntimeSensor(SprsunBaseTimerSensor):
    def __init__(self, name, unique_id, reset_mode, entry_id, model, translations, loader, icon=None):
        super().__init__(
            name,
            unique_id,
            "binary_sensor.sprsun_<model>_wentylator",
            reset_mode,
            entry_id,
            model,
            translations,
            loader,
            icon,
        )


# ============================================================
#  TIMER POMPY OBIEGOWEJ
# ============================================================
class SprsunPumpRuntimeSensor(SprsunBaseTimerSensor):
    def __init__(
        self,
        name,
        unique_id,
        reset_mode,
        entry_id,
        model,
        translations,
        loader,
        icon=None,
    ):
        super().__init__(
            name,
            unique_id,
            "binary_sensor.sprsun_cgk040v3l_pompa_obiegowa",
            reset_mode,
            entry_id,
            model,
            translations,
            loader,
            icon,
        )


# ============================================================
#  BAZA LICZNIKÓW
# ============================================================
class SprsunBaseCounterSensor(RestoreEntity, SensorEntity):
    _attr_should_poll = False

    def __init__(self, name, unique_id, reset_mode, entry_id, model, translations, loader, icon=None):
        t = loader.get_sensor_translation(translations, unique_id)
        translated_name = t.get("name", name)
        translated_entity_id = t.get("entity_id", unique_id)
        self._attr_name = translated_name
        self._attr_unique_id = unique_id
        self._reset_mode = reset_mode
        self._entry_id = entry_id
        self._model = model
        self._icon = icon
        self._attr_icon = icon
        slug = _slugify(translated_entity_id)
        self.entity_id = f"sensor.sprsun_{self._model.lower()}_{slug}"
        self._count = 0
        self._last_reset = None

    @property
    def native_value(self):
        return self._count

    @property
    def extra_state_attributes(self):
        return {
            "last_reset": self._last_reset.isoformat() if self._last_reset else None,
        }

    async def _maybe_reset(self, today: date):
        if self._reset_mode == "total" or self._last_reset is None:
            return

        do_reset = False
        if self._reset_mode == "daily" and today > self._last_reset:
            do_reset = True
        elif self._reset_mode == "monthly" and (today.year, today.month) != (self._last_reset.year, self._last_reset.month):
            do_reset = True
        elif self._reset_mode == "yearly" and today.year != self._last_reset.year:
            do_reset = True

        if do_reset:
            self._count = 0
            self._last_reset = today
            self.async_write_ha_state()

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

        self.async_on_remove(
            async_track_time_interval(
                self.hass,
                self._handle_interval,
                timedelta(hours=1),
            )
        )

        # Reset na granicy okresu, niezależnie od pracy pompy.
        if self._reset_mode == "daily":
            self.async_on_remove(
                async_track_time_change(
                    self.hass,
                    self._scheduled_reset,
                    hour=0,
                    minute=0,
                    second=0,
                )
            )

    async def _scheduled_reset(self, now):
        """Reset licznika dokładnie na granicy okresu."""
        today = now.date()
        last = self._last_reset

        if self._reset_mode == "daily":
            should_reset = last is None or last != today
        elif self._reset_mode == "monthly":
            should_reset = (
                last is None
                or (last.year, last.month) != (today.year, today.month)
            )
        elif self._reset_mode == "yearly":
            should_reset = last is None or last.year != today.year
        else:
            # Total nigdy nie resetuje się automatycznie.
            should_reset = False

        if should_reset:
            self._count = 0
            self._last_reset = today
            self.async_write_ha_state()

    async def _handle_interval(self, now):
        await self._maybe_reset(now.date())

    def _increment_safe(self):
        self._count = int(self._count) + 1
        self.async_write_ha_state()


# ============================================================
#  UNIWERSALNY LICZNIK (wentylator, defrost, zawór 3D, pompa obiegowa)
# ============================================================
class SprsunCounterSensor(SprsunBaseCounterSensor):
    def __init__(
        self,
        name,
        unique_id,
        reset_mode,
        entry_id,
        model,
        translations,
        loader,
        key=None,
        source_sensor=None,
        source_sensor_sprezarka=None,
        source_sensor_wentylator=None,
        allow_offset=False,
        icon=None,
    ):
        super().__init__(name, unique_id, reset_mode, entry_id, model, translations, loader, icon)
        self._key = key
        self._source_sensor = source_sensor
        self._source_sensor_sprezarka = source_sensor_sprezarka
        self._source_sensor_wentylator = source_sensor_wentylator
        self._allow_offset = allow_offset
        self._last_state = None
        self._defrost_active = False
        self._defrost_start_time = None

    @property
    def extra_state_attributes(self):
        attributes = dict(super().extra_state_attributes)
        if self._key == "defrost":
            if self._defrost_active == "waiting_for_end":
                active_state = "waiting_for_end"
            elif self._defrost_active is True:
                active_state = "active"
            else:
                active_state = "idle"

            attributes["defrost_active"] = active_state
            attributes["defrost_start_time"] = (
                self._defrost_start_time.isoformat()
                if self._defrost_start_time is not None
                else None
            )
        return attributes

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        # Odtworzenie stanu defrostu po restarcie Home Assistanta.
        if self._key == "defrost":
            last_state = await self.async_get_last_state()
            if last_state:
                saved_active = last_state.attributes.get("defrost_active", "idle")
                saved_start = last_state.attributes.get("defrost_start_time")

                if saved_active == "waiting_for_end":
                    self._defrost_active = "waiting_for_end"
                elif saved_active == "active":
                    self._defrost_active = True
                else:
                    self._defrost_active = False

                if saved_start:
                    try:
                        self._defrost_start_time = datetime.fromisoformat(saved_start)
                    except (TypeError, ValueError):
                        self._defrost_start_time = None

                # Bez czasu rozpoczęcia nie można wiarygodnie zweryfikować
                # aktywnego defrostu — zaczynamy obserwację od nowa.
                if self._defrost_active is True and self._defrost_start_time is None:
                    self._defrost_active = False

        # STARTY WENTYLATORA
        if self._key == "start_wentylatora" and self._source_sensor:
            sensor_id = self._source_sensor.replace("<model>", self._model)
            self.async_on_remove(
                async_track_state_change_event(
                    self.hass,
                    [sensor_id],
                    self._handle_start_event,
                )
            )

        # DEFROST
        if self._key == "defrost" and self._source_sensor_sprezarka and self._source_sensor_wentylator:
            self.async_on_remove(
                async_track_time_interval(
                    self.hass,
                    self._handle_defrost_check,
                    timedelta(seconds=5),
                )
            )

        # ZAWÓR 3D
        if self._key == "valve_count" and self._source_sensor:
            sensor_id = self._source_sensor.replace("<model>", self._model)
            self.async_on_remove(
                async_track_state_change_event(
                    self.hass,
                    [sensor_id],
                    self._handle_valve_event,
                )
            )

        # PRZEŁĄCZENIA POMPY OBIEGOWEJ
        if self._key == "pump_switch_count" and self._source_sensor:
            sensor_id = self._source_sensor.replace("<model>", self._model)
            self.async_on_remove(
                async_track_state_change_event(
                    self.hass,
                    [sensor_id],
                    self._handle_pump_event,
                )
            )

    # ============================
    #  PRZEŁĄCZENIA POMPY OBIEGOWEJ
    # ============================
    @callback
    def _handle_pump_event(self, event):
        old = event.data.get("old_state")
        new = event.data.get("new_state")

        if not old or not new:
            return

        old_val = old.state
        new_val = new.state

        # Interesują nas wyłącznie stany on i off.
        if old_val not in ("on", "off") or new_val not in ("on", "off"):
            return

        # Każde rzeczywiste przełączenie pompy = +1.
        if old_val != new_val:
            self._increment_safe()

    # ============================
    #  START WENTYLATORA
    # ============================
    @callback
    async def _handle_start_event(self, event):
        old = event.data.get("old_state")
        new = event.data.get("new_state")

        if old and new and old.state != "on" and new.state == "on":
            self._increment_safe()

    # ============================
    #  DEFROST — NOWA LOGIKA
    # ============================
    async def _handle_defrost_check(self, now):
        compressor = self.hass.states.get(
            self._source_sensor_sprezarka.replace("<model>", self._model)
        )
        fan = self.hass.states.get(
            self._source_sensor_wentylator.replace("<model>", self._model)
        )
        if not compressor or not fan:
            return

        comp_on = compressor.state == "on"
        fan_off = fan.state == "off"
        defrost_condition = comp_on and fan_off

        coordinator = self.hass.data[DOMAIN][self._entry_id]["coordinator"]
        interval = coordinator.update_interval.total_seconds()
        min_defrost_time = interval * 2

        # Stan 1: nie trwa defrost — wykryj jego początek.
        if self._defrost_active is False:
            if defrost_condition:
                self._defrost_active = True
                self._defrost_start_time = now
                self.async_write_ha_state()
            return

        # Stan 2: defrost trwa — zlicz go tylko raz po upływie
        # minimalnego czasu i przejdź do oczekiwania na jego koniec.
        if self._defrost_active is True:
            if not defrost_condition:
                self._defrost_active = False
                self._defrost_start_time = None
                self.async_write_ha_state()
                return

            if self._defrost_start_time is None:
                self._defrost_start_time = now
                self.async_write_ha_state()
                return

            elapsed = (now - self._defrost_start_time).total_seconds()
            if elapsed >= min_defrost_time:
                self._increment_safe()
                self._defrost_active = "waiting_for_end"
                # Zapis atrybutów nowego stanu, aby po restarcie nie
                # zliczyć tego samego defrostu ponownie.
                self.async_write_ha_state()
            return

        # Stan 3: ten defrost został już zliczony. Czekaj na koniec,
        # nie sprawdzając ponownie czasu i nie zwiększając licznika.
        if self._defrost_active == "waiting_for_end":
            if not defrost_condition:
                self._defrost_active = False
                self._defrost_start_time = None
                self.async_write_ha_state()
            return

    # ============================
    #  ZAWÓR 3D
    # ============================
    @callback
    def _handle_valve_event(self, event):
        old = event.data.get("old_state")
        new = event.data.get("new_state")

        if not old or not new:
            return

        old_val = str(old.state).strip().upper()
        new_val = str(new.state).strip().upper()

        # Normalizacja pozycji zaworu:
        # 1 lub C.W.U. = CWU
        # 2 lub C.O. = CO
        positions = {
            "1": "cwu",
            "C.W.U.": "cwu",
            "2": "co",
            "C.O.": "co",
        }

        old_position = positions.get(old_val)
        new_position = positions.get(new_val)

        # Pomijamy unknown, unavailable i inne nieprawidłowe wartości.
        if old_position is None or new_position is None:
            return

        # Zliczamy wyłącznie rzeczywistą zmianę pozycji.
        if old_position != new_position:
            self._increment_safe()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace("_", "-"),
        }


# ============================================================
#  LICZNIK STARTÓW SPRĘŻARKI
# ============================================================
class SprsunCompressorStartCounter(SprsunBaseCounterSensor):
    def __init__(self, name, unique_id, reset_mode, entry_id, model, translations, loader, icon=None):
        super().__init__(name, unique_id, reset_mode, entry_id, model, translations, loader, icon)
        self._compressor_entity = f"binary_sensor.sprsun_{model.lower()}_sprezarka"
        self._attr_icon = icon

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._compressor_entity],
                self._handle_change,
            )
        )

    @callback
    async def _handle_change(self, event):
        old = event.data.get("old_state")
        new = event.data.get("new_state")

        if old and new and old.state != "on" and new.state == "on":
            self._increment_safe()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace("_", "-"),
        }


# ============================================================
#  LICZNIK DEFROSTÓW (NIEUŻYWANY — ZASTĄPIONY)
# ============================================================
class SprsunDefrostCounter(SprsunBaseCounterSensor):
    def __init__(self, name, unique_id, reset_mode, entry_id, model, translations, loader, icon=None):
        super().__init__(name, unique_id, reset_mode, entry_id, model, translations, loader, icon)
        self._compressor_entity = f"binary_sensor.sprsun_{model}_sprezarka"
        self._fan_entity = f"binary_sensor.sprsun_{model}_wentylator"

    async def _handle_interval_defrost(self, now):
        compressor = self.hass.states.get(self._compressor_entity)
        fan = self.hass.states.get(self._fan_entity)
        if compressor and fan:
            if compressor.state == "on" and fan.state == "off":
                self._increment_safe()


# ============================================================
#  DNI POSIADANIA POMPY
# ============================================================
class SprsunOwnershipDaysSensor(RestoreEntity, SensorEntity):
    _attr_should_poll = False
    _attr_icon = "mdi:calendar-clock"
    _attr_native_unit_of_measurement = "d"

    def __init__(self, name, unique_id, entry_id, model, translations, loader):
        t = loader.get_sensor_translation(translations, unique_id)
        translated_name = t.get("name", name)
        translated_entity_id = t.get("entity_id", unique_id)
        self._attr_name = translated_name
        self._attr_unique_id = unique_id
        self._entry_id = entry_id
        self._model = model
        slug = _slugify(translated_entity_id)
        self.entity_id = f"sensor.sprsun_{self._model.lower()}_{slug}"
        self._days = 0
        self._last_increment = None

    @property
    def native_value(self):
        return self._days

    @property
    def extra_state_attributes(self):
        return {
            "last_increment": (
                self._last_increment.isoformat()
                if self._last_increment is not None
                else None
            ),
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
            self._days = _parse_int(last_state.state, 0)
            last_increment_str = last_state.attributes.get("last_increment")
            if last_increment_str:
                try:
                    self._last_increment = date.fromisoformat(last_increment_str)
                except (TypeError, ValueError):
                    self._last_increment = None

        today = dt_util.now().date()

        # Przy pierwszym uruchomieniu rozpoczynamy liczenie od bieżącego dnia.
        # Nie dodajemy dnia przy samym utworzeniu lub restarcie encji.
        if self._last_increment is None:
            self._last_increment = today
        else:
            # Uzupełnij wszystkie dni, w których Home Assistant był wyłączony.
            missed_days = (today - self._last_increment).days
            if missed_days > 0:
                self._days += missed_days
                self._last_increment = today
                self.async_write_ha_state()
            elif missed_days < 0:
                # Zmiana daty systemowej wstecz nie może zmniejszyć licznika.
                self._last_increment = today
                self.async_write_ha_state()

        # Zwiększaj licznik codziennie dokładnie o północy czasu Home Assistant.
        self.async_on_remove(
            async_track_time_change(
                self.hass,
                self._scheduled_daily_increment,
                hour=0,
                minute=0,
                second=0,
            )
        )

    async def _scheduled_daily_increment(self, now):
        """Dodaj jeden dzień posiadania po każdej północy."""
        today = now.date()

        if self._last_increment is None:
            self._last_increment = today
            self.async_write_ha_state()
            return

        elapsed_days = (today - self._last_increment).days
        if elapsed_days <= 0:
            return

        # Normalnie elapsed_days wynosi 1. Większa wartość zabezpiecza
        # przed pominiętymi północami, np. podczas wyłączenia HA.
        self._days += elapsed_days
        self._last_increment = today
        self.async_write_ha_state()


# ============================================================
#  LISTA SENSORÓW LOGICZNYCH
# ============================================================
logic_sensors = [
    {
        "class": "SprsunCompressorRuntimeSensor",
        "args": {
            "name": "Czas pracy sprężarki (total)",
            "unique_id": "sprsun_compressor_runtime_total",
            "reset_mode": "total",
            "icon": "mdi:bag-personal",
        }
    },
    {
        "class": "SprsunCompressorRuntimeSensor",
        "args": {
            "name": "Czas pracy sprężarki (dzienny)",
            "unique_id": "sprsun_compressor_runtime_daily",
            "reset_mode": "daily",
            "icon": "mdi:bag-personal",
        }
    },
    {
        "class": "SprsunCompressorRuntimeSensor",
        "args": {
            "name": "Czas pracy sprężarki (miesięczny)",
            "unique_id": "sprsun_compressor_runtime_monthly",
            "reset_mode": "monthly",
            "icon": "mdi:bag-personal",
        }
    },
    {
        "class": "SprsunCompressorRuntimeSensor",
        "args": {
            "name": "Czas pracy sprężarki (roczny)",
            "unique_id": "sprsun_compressor_runtime_yearly",
            "reset_mode": "yearly",
            "icon": "mdi:bag-personal",
        }
    },
    {
        "class": "SprsunCompressorStartCounter",
        "args": {
            "name": "Ilość włączeń sprężarki daily",
            "unique_id": "ilosc_wlaczen_sprezarki_daily",
            "reset_mode": "daily",
            "icon": "mdi:bag-personal",
        }
    },
    {
        "class": "SprsunCompressorStartCounter",
        "args": {
            "name": "Ilość włączeń sprężarki monthly",
            "unique_id": "ilosc_wlaczen_sprezarki_monthly",
            "reset_mode": "monthly",
            "icon": "mdi:bag-personal",
        }
    },
    {
        "class": "SprsunCompressorStartCounter",
        "args": {
            "name": "Ilość włączeń sprężarki yearly",
            "unique_id": "ilosc_wlaczen_sprezarki_yearly",
            "reset_mode": "yearly",
            "icon": "mdi:bag-personal",
        }
    },
    {
        "class": "SprsunCompressorStartCounter",
        "args": {
            "name": "Ilość włączeń sprężarki total",
            "unique_id": "ilosc_wlaczen_sprezarki_total",
            "reset_mode": "total",
            "icon": "mdi:bag-personal",
        }
    },
    {
        "class": "SprsunFanRuntimeSensor",
        "args": {
            "name": "Czas pracy wentylatora (total)",
            "unique_id": "sprsun_fan_runtime_total",
            "reset_mode": "total",
            "icon": "mdi:fan",
        }
    },
    {
        "class": "SprsunFanRuntimeSensor",
        "args": {
            "name": "Czas pracy wentylatora (dzienny)",
            "unique_id": "sprsun_fan_runtime_daily",
            "reset_mode": "daily",
            "icon": "mdi:fan",
        }
    },
    {
        "class": "SprsunFanRuntimeSensor",
        "args": {
            "name": "Czas pracy wentylatora (miesięczny)",
            "unique_id": "sprsun_fan_runtime_monthly",
            "reset_mode": "monthly",
            "icon": "mdi:fan",
        }
    },
    {
        "class": "SprsunFanRuntimeSensor",
        "args": {
            "name": "Czas pracy wentylatora (roczny)",
            "unique_id": "sprsun_fan_runtime_yearly",
            "reset_mode": "yearly",
            "icon": "mdi:fan",
        }
    },
    {
        "class": "SprsunCounterSensor",
        "args": {
            "key": "start_wentylatora",
            "name": "Ilość włączeń wentylatora daily",
            "unique_id": "ilosc_wlaczen_wentylatora_daily",
            "reset_mode": "daily",
            "source_sensor": "binary_sensor.sprsun_<model>_wentylator",
            "icon": "mdi:fan",
        }
    },
    {
        "class": "SprsunCounterSensor",
        "args": {
            "key": "start_wentylatora",
            "name": "Ilość włączeń wentylatora monthly",
            "unique_id": "ilosc_wlaczen_wentylatora_monthly",
            "reset_mode": "monthly",
            "source_sensor": "binary_sensor.sprsun_<model>_wentylator",
            "icon": "mdi:fan",
        }
    },
    {
        "class": "SprsunCounterSensor",
        "args": {
            "key": "start_wentylatora",
            "name": "Ilość włączeń wentylatora yearly",
            "unique_id": "ilosc_wlaczen_wentylatora_yearly",
            "reset_mode": "yearly",
            "source_sensor": "binary_sensor.sprsun_<model>_wentylator",
            "icon": "mdi:fan",
        }
    },
    {
        "class": "SprsunCounterSensor",
        "args": {
            "key": "start_wentylatora",
            "name": "Ilość włączeń wentylatora total",
            "unique_id": "ilosc_wlaczen_wentylatora_total",
            "reset_mode": "total",
            "source_sensor": "binary_sensor.sprsun_<model>_wentylator",
            "icon": "mdi:fan",
        }
    },
    {
        "class": "SprsunCounterSensor",
        "args": {
            "key": "defrost",
            "name": "Ilość defrostów daily",
            "unique_id": "ilosc_defrostow_daily",
            "reset_mode": "daily",
            "source_sensor_sprezarka": "binary_sensor.sprsun_<model>_sprezarka",
            "source_sensor_wentylator": "binary_sensor.sprsun_<model>_wentylator",
            "icon": "mdi:snowflake-melt",
        }
    },
    {
        "class": "SprsunCounterSensor",
        "args": {
            "key": "defrost",
            "name": "Ilość defrostów monthly",
            "unique_id": "ilosc_defrostow_monthly",
            "reset_mode": "monthly",
            "source_sensor_sprezarka": "binary_sensor.sprsun_<model>_sprezarka",
            "source_sensor_wentylator": "binary_sensor.sprsun_<model>_wentylator",
            "icon": "mdi:snowflake-melt",
        }
    },
    {
        "class": "SprsunCounterSensor",
        "args": {
            "key": "defrost",
            "name": "Ilość defrostów yearly",
            "unique_id": "ilosc_defrostow_yearly",
            "reset_mode": "yearly",
            "source_sensor_sprezarka": "binary_sensor.sprsun_<model>_sprezarka",
            "source_sensor_wentylator": "binary_sensor.sprsun_<model>_wentylator",
            "icon": "mdi:snowflake-melt",
        }
    },
    {
        "class": "SprsunCounterSensor",
        "args": {
            "key": "defrost",
            "name": "Ilość defrostów total",
            "unique_id": "ilosc_defrostow_total",
            "reset_mode": "total",
            "source_sensor_sprezarka": "binary_sensor.sprsun_<model>_sprezarka",
            "source_sensor_wentylator": "binary_sensor.sprsun_<model>_wentylator",
            "allow_offset": True,
            "icon": "mdi:snowflake-melt",
        }
    },

    # ============================
    #         ZAWÓR 3D
    # ============================
    {
        "class": "SprsunCounterSensor",
        "args": {
            "key": "valve_count",
            "name": "Ilość przełączeń zaworu 3D total",
            "unique_id": "ilosc_przelaczen_zaworu_3d_total",
            "reset_mode": "total",
            "source_sensor": "sensor.sprsun_<model>_zawor_trojdrogowy_pozycja",
            "allow_offset": True,
            "icon": "mdi:valve",
        }
    },

    # ============================
    #         POMPA OBIEGOWA
    # ============================
    {
        "class": "SprsunCounterSensor",
        "args": {
            "key": "pump_switch_count",
            "name": "Ilość przełączeń pompy obiegowej total",
            "unique_id": "ilosc_przelaczen_pompy_obiegowej_total",
            "reset_mode": "total",
            "source_sensor": "binary_sensor.sprsun_cgk040v3l_pompa_obiegowa",
            "icon": "mdi:pump",
        }
    },

    {
        "class": "SprsunPumpRuntimeSensor",
        "args": {
            "name": "Czas pracy pompy obiegowej (dzienny)",
            "unique_id": "sprsun_pump_runtime_daily",
            "reset_mode": "daily",
            "icon": "mdi:pump",
        },
    },
    {
        "class": "SprsunPumpRuntimeSensor",
        "args": {
            "name": "Czas pracy pompy obiegowej (miesięczny)",
            "unique_id": "sprsun_pump_runtime_monthly",
            "reset_mode": "monthly",
            "icon": "mdi:pump",
        },
    },
    {
        "class": "SprsunPumpRuntimeSensor",
        "args": {
            "name": "Czas pracy pompy obiegowej (roczny)",
            "unique_id": "sprsun_pump_runtime_yearly",
            "reset_mode": "yearly",
            "icon": "mdi:pump",
        },
    },
    {
        "class": "SprsunPumpRuntimeSensor",
        "args": {
            "name": "Czas pracy pompy obiegowej (total)",
            "unique_id": "sprsun_pump_runtime_total",
            "reset_mode": "total",
            "icon": "mdi:pump",
        },
    },
]
