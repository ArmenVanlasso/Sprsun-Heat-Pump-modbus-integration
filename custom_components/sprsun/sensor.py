import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.config_entries import ConfigEntry

from .models.CGK025V3L.logic_sensors import (
    SprsunCompressorRuntimeSensor,
    SprsunFanRuntimeSensor,
    SprsunOwnershipDaysSensor,
    SprsunCompressorStartCounter,
    SprsunDefrostCounter,
)

from .models.CGK030V3L.logic_sensors import (
    SprsunCompressorRuntimeSensor as SprsunCompressorRuntimeSensor_030,
    SprsunFanRuntimeSensor as SprsunFanRuntimeSensor_030,
    SprsunOwnershipDaysSensor as SprsunOwnershipDaysSensor_030,
    SprsunCompressorStartCounter as SprsunCompressorStartCounter_030,
    SprsunDefrostCounter as SprsunDefrostCounter_030,
)

from .models.CGK040V3L.logic_sensors import (
    SprsunCompressorRuntimeSensor as SprsunCompressorRuntimeSensor_040,
    SprsunFanRuntimeSensor as SprsunFanRuntimeSensor_040,
    SprsunOwnershipDaysSensor as SprsunOwnershipDaysSensor_040,
    SprsunCompressorStartCounter as SprsunCompressorStartCounter_040,
    SprsunDefrostCounter as SprsunDefrostCounter_040,
)

from .models.CGK050V3L.logic_sensors import (
    SprsunCompressorRuntimeSensor as SprsunCompressorRuntimeSensor_050,
    SprsunFanRuntimeSensor as SprsunFanRuntimeSensor_050,
    SprsunOwnershipDaysSensor as SprsunOwnershipDaysSensor_050,
    SprsunCompressorStartCounter as SprsunCompressorStartCounter_050,
    SprsunDefrostCounter as SprsunDefrostCounter_050,
)

from .models.CGK060V3L.logic_sensors import (
    SprsunCompressorRuntimeSensor as SprsunCompressorRuntimeSensor_060,
    SprsunFanRuntimeSensor as SprsunFanRuntimeSensor_060,
    SprsunOwnershipDaysSensor as SprsunOwnershipDaysSensor_060,
    SprsunCompressorStartCounter as SprsunCompressorStartCounter_060,
    SprsunDefrostCounter as SprsunDefrostCounter_060,
)

from .const import (
    DOMAIN,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)
from .modbus_client import HeatPumpModbusClient

from .models.CGK025V3L.sensors import SENSORS as SENSORS_025
from .models.CGK030V3L.sensors import SENSORS as SENSORS_030
from .models.CGK040V3L.sensors import SENSORS as SENSORS_040
from .models.CGK050V3L.sensors import SENSORS as SENSORS_050
from .models.CGK060V3L.sensors import SENSORS as SENSORS_060

_LOGGER = logging.getLogger(__name__)

MODEL_SENSORS_MAP = {
    "cgk_025v3l": SENSORS_025,
    "cgk_030v3l": SENSORS_030,
    "cgk_040v3l": SENSORS_040,
    "cgk_050v3l": SENSORS_050,
    "cgk_060v3l": SENSORS_060,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    data = hass.data[DOMAIN][entry.entry_id]
    client: HeatPumpModbusClient = data["client"]
    model: str = data["model"]

    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    sensors_def = MODEL_SENSORS_MAP.get(model)
    if sensors_def is None:
        _LOGGER.error("Brak zdefiniowanych sensorów dla modelu: %s", model)
        return

    entities: list[SensorEntity] = [
        SprsunGenericSensor(client, entry.entry_id, model, definition)
        for definition in sensors_def
    ]

    # LOGIC SENSORS – wybór klas per model
    if model == "cgk_025v3l":
        CompressorRuntime = SprsunCompressorRuntimeSensor
        FanRuntime = SprsunFanRuntimeSensor
        OwnershipDays = SprsunOwnershipDaysSensor
        CompressorStarts = SprsunCompressorStartCounter
        DefrostCounter = SprsunDefrostCounter
    elif model == "cgk_030v3l":
        CompressorRuntime = SprsunCompressorRuntimeSensor_030
        FanRuntime = SprsunFanRuntimeSensor_030
        OwnershipDays = SprsunOwnershipDaysSensor_030
        CompressorStarts = SprsunCompressorStartCounter_030
        DefrostCounter = SprsunDefrostCounter_030
    elif model == "cgk_040v3l":
        CompressorRuntime = SprsunCompressorRuntimeSensor_040
        FanRuntime = SprsunFanRuntimeSensor_040
        OwnershipDays = SprsunOwnershipDaysSensor_040
        CompressorStarts = SprsunCompressorStartCounter_040
        DefrostCounter = SprsunDefrostCounter_040
    elif model == "cgk_050v3l":
        CompressorRuntime = SprsunCompressorRuntimeSensor_050
        FanRuntime = SprsunFanRuntimeSensor_050
        OwnershipDays = SprsunOwnershipDaysSensor_050
        CompressorStarts = SprsunCompressorStartCounter_050
        DefrostCounter = SprsunDefrostCounter_050
    else:
        CompressorRuntime = SprsunCompressorRuntimeSensor_060
        FanRuntime = SprsunFanRuntimeSensor_060
        OwnershipDays = SprsunOwnershipDaysSensor_060
        CompressorStarts = SprsunCompressorStartCounter_060
        DefrostCounter = SprsunDefrostCounter_060

    logic_sensors: list[SensorEntity] = [
        CompressorRuntime("Czas pracy sprężarki daily",
                          f"{DOMAIN}_{model}_czas_pracy_sprezarki_daily",
                          "daily", entry.entry_id, model),
        CompressorRuntime("Czas pracy sprężarki monthly",
                          f"{DOMAIN}_{model}_czas_pracy_sprezarki_monthly",
                          "monthly", entry.entry_id, model),
        CompressorRuntime("Czas pracy sprężarki yearly",
                          f"{DOMAIN}_{model}_czas_pracy_sprezarki_yearly",
                          "yearly", entry.entry_id, model),
        CompressorRuntime("Czas pracy sprężarki total",
                          f"{DOMAIN}_{model}_czas_pracy_sprezarki_total",
                          "total", entry.entry_id, model),

        FanRuntime("Czas pracy wentylatora daily",
                   f"{DOMAIN}_{model}_czas_pracy_wentylatora_daily",
                   "daily", entry.entry_id, model),
        FanRuntime("Czas pracy wentylatora monthly",
                   f"{DOMAIN}_{model}_czas_pracy_wentylatora_monthly",
                   "monthly", entry.entry_id, model),
        FanRuntime("Czas pracy wentylatora yearly",
                   f"{DOMAIN}_{model}_czas_pracy_wentylatora_yearly",
                   "yearly", entry.entry_id, model),
        FanRuntime("Czas pracy wentylatora total",
                   f"{DOMAIN}_{model}_czas_pracy_wentylatora_total",
                   "total", entry.entry_id, model),

        OwnershipDays("Czas posiadania pompy",
                      f"{DOMAIN}_{model}_czas_posiadania_pompy",
                      entry.entry_id, model),

        CompressorStarts("Ilość włączeń sprężarki daily",
                         f"{DOMAIN}_{model}_ilosc_wlaczen_sprezarki_daily",
                         "daily", entry.entry_id, model),
        CompressorStarts("Ilość włączeń sprężarki monthly",
                         f"{DOMAIN}_{model}_ilosc_wlaczen_sprezarki_monthly",
                         "monthly", entry.entry_id, model),
        CompressorStarts("Ilość włączeń sprężarki yearly",
                         f"{DOMAIN}_{model}_ilosc_wlaczen_sprezarki_yearly",
                         "yearly", entry.entry_id, model),
        CompressorStarts("Ilość włączeń sprężarki total",
                         f"{DOMAIN}_{model}_ilosc_wlaczen_sprezarki_total",
                         "total", entry.entry_id, model),

        DefrostCounter("Ilość defrostów dzisiaj",
                       f"{DOMAIN}_{model}_ilosc_defrostow_daily",
                       "daily", entry.entry_id, model),
        DefrostCounter("Ilość defrostów w tym miesiącu",
                       f"{DOMAIN}_{model}_ilosc_defrostow_monthly",
                       "monthly", entry.entry_id, model),
        DefrostCounter("Ilość defrostów w tym roku",
                       f"{DOMAIN}_{model}_ilosc_defrostow_yearly",
                       "yearly", entry.entry_id, model),
        DefrostCounter("Ilość defrostów total",
                       f"{DOMAIN}_{model}_ilosc_defrostow_total",
                       "total", entry.entry_id, model),
    ]

    entities.extend(logic_sensors)

    class SprsunModbusWorkerSensor(SensorEntity):
        _attr_should_poll = False

        def __init__(self, client, entry_id, model):
            self._client = client
            self._entry_id = entry_id
            self._model = model
            self._last_ok = True
            self._last_error = None

            self._attr_name = "Modbus worker"
            self._attr_unique_id = f"{DOMAIN}_{model}_{entry.entry_id}_modbus_worker"
            self.entity_id = f"sensor.sprsun_{model}_modbus_worker"

        @property
        def device_info(self):
            return {
                "identifiers": {(DOMAIN, self._entry_id)},
                "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
                "manufacturer": "Sprsun",
                "model": self._model.upper().replace('_', '-'),
            }

        @property
        def native_value(self):
            return "ok" if self._last_ok else "brak połączenia"

        @property
        def icon(self):
            return "mdi:check-network" if self._last_ok else "mdi:close-network"

        async def async_update(self):
            try:
                test = await self._client.read_holding_registers(0, 1)
                if test is None:
                    raise Exception("Brak odpowiedzi")
                self._last_ok = True
                self._last_error = None
            except Exception as err:
                self._last_ok = False
                self._last_error = str(err)

    class SprsunModbusErrorSensor(SensorEntity):
        _attr_should_poll = False

        def __init__(self, worker_sensor, entry_id, model):
            self._worker = worker_sensor
            self._entry_id = entry_id
            self._model = model

            self._attr_name = "Modbus errors"
            self._attr_unique_id = f"{DOMAIN}_{model}_{entry.entry_id}_modbus_errors"
            self.entity_id = f"sensor.sprsun_{model}_modbus_errors"

        @property
        def device_info(self):
            return {
                "identifiers": {(DOMAIN, self._entry_id)},
                "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
                "manufacturer": "Sprsun",
                "model": self._model.upper().replace('_', '-'),
            }

        @property
        def native_value(self):
            if self._worker._last_error is None:
                return "brak błędów"
            return self._worker._last_error

        @property
        def icon(self):
            return (
                "mdi:check-circle-outline"
                if self._worker._last_error is None
                else "mdi:alert-circle-outline"
            )

        async def async_update(self):
            pass

    modbus_worker = SprsunModbusWorkerSensor(client, entry.entry_id, model)
    modbus_errors = SprsunModbusErrorSensor(modbus_worker, entry.entry_id, model)

    entities.append(modbus_worker)
    entities.append(modbus_errors)

    async_add_entities(entities)

    async def _periodic_update(now):
        for entity in entities:
            try:
                await entity.async_update()
                entity.async_write_ha_state()
            except Exception as err:
                _LOGGER.error("Błąd aktualizacji sensora %s: %s", entity.name, err)

    async_track_time_interval(
        hass,
        _periodic_update,
        timedelta(seconds=scan_interval),
    )


class SprsunGenericSensor(SensorEntity):
    _attr_should_poll = False

    def __init__(self, client, entry_id, model, definition):
        self._client = client
        self._entry_id = entry_id
        self._model = model
        self._def = definition
        self._attr_available = False

        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{self._model}_{self._def['register']}"

        slug = (
            f"sprsun_{self._model}_{definition['name']}"
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
        self.entity_id = f"sensor.{slug}"

        self._attr_device_class = definition.get("device_class")
        self._attr_native_unit_of_measurement = definition.get("unit")
        self._attr_state_class = definition.get("state_class")

        self._raw_value = None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }

    @property
    def native_value(self):
        raw = self._raw_value
        if raw is None:
            return None

        mapping = self._def.get("mapping")
        if mapping:
            return mapping.get(raw, raw)

        return raw

    @property
    def icon(self):
        raw = self._raw_value
        icon_map = self._def.get("icon_map")
        if icon_map:
            return icon_map.get(raw, self._def.get("icon"))
        return self._def.get("icon")

    async def async_update(self):
        reg = self._def["register"]
        scale = self._def.get("scale", 1)
        signed = self._def.get("signed", False)

        regs = await self._client.read_holding_registers(reg, 1)
        if not regs:
            self._attr_available = False
            return

        raw = regs[0]

        if signed and raw > 32767:
            raw -= 65536

        self._raw_value = raw * scale
        self._attr_available = True
