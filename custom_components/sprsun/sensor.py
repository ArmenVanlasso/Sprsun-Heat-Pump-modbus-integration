import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.config_entries import ConfigEntry

from .const import (
    DOMAIN,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
    REG_RETURN_TEMP,
)
from .modbus_client import HeatPumpModbusClient

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup platformy sensor z config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    client: HeatPumpModbusClient = data["client"]
    model: str = data["model"]  # <-- pobieramy model urządzenia

    scan_interval = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    sensor = ReturnTemperatureSensor(client, entry.entry_id, model)
    async_add_entities([sensor])

    async def _periodic_update(now):
        await sensor.async_update()
        sensor.async_write_ha_state()

    async_track_time_interval(
        hass,
        _periodic_update,
        timedelta(seconds=scan_interval),
    )


class ReturnTemperatureSensor(SensorEntity):
    """Sensor 'Sprsun temperatura powrotu' jako INT16 * 0.1."""

    _attr_should_poll = False
    _attr_name = "Sprsun temperatura powrotu"
    _attr_device_class = "temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_icon = "mdi:thermometer"

    def __init__(self, client: HeatPumpModbusClient, entry_id: str, model: str):
        self._client = client
        self._entry_id = entry_id
        self._model = model
        self._attr_available = False

        # unikalne ID zgodne z domeną sprsun
        self._attr_unique_id = f"sprsun_return_temp_{entry_id}"

        # stabilne entity_id z prefiksem domeny
        self.entity_id = f"sensor.sprsun_return_temp_{entry_id}"

    @property
    def device_info(self):
        """Grupowanie encji w jedno urządzenie."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "Sprsun Heat Pump",
            "manufacturer": "Sprsun",
            "model": self._model,
        }

    async def async_update(self) -> None:
        """Odczyt temperatury powrotu z Modbus (INT16, skala 0.1)."""
        regs = await self._client.read_holding_registers(REG_RETURN_TEMP, 1)
        if not regs:
            self._attr_available = False
            return

        raw = regs[0]

        # Konwersja na int16 ze znakiem
        if raw > 32767:
            raw_signed = raw - 65536
        else:
            raw_signed = raw

        temp = raw_signed * 0.1

        self._attr_native_value = round(temp, 1)
        self._attr_available = True
