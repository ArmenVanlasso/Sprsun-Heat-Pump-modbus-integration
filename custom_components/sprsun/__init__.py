import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_HOST,
    CONF_PORT,
    CONF_UNIT_ID,
    CONF_MODEL,
)
from .modbus_client import HeatPumpModbusClient

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Ogólny setup (nieużywany przy config entries)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup integracji z jednego config entry."""
    hass.data.setdefault(DOMAIN, {})

    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    unit_id = entry.data[CONF_UNIT_ID]
    model = entry.data[CONF_MODEL]

    _LOGGER.debug(
        "Inicjalizacja Sprsun Modbus: host=%s port=%s unit_id=%s model=%s",
        host, port, unit_id, model
    )

    # Tworzymy klienta Modbus
    client = HeatPumpModbusClient(host, port, unit_id)

    # Funkcja odświeżająca dane
    async def async_update_data():
        """Pobieranie wszystkich rejestrów z pompy."""
        try:
            return await client.read_all_registers()
        except Exception as err:
            _LOGGER.error("Błąd podczas odczytu danych z Modbus: %s", err)
            raise

    # Coordinator odpowiedzialny za cykliczne odświeżanie
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="sprsun_modbus",
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),
    )

    # Pierwsze odświeżenie
    await coordinator.async_config_entry_first_refresh()

    # Zapisujemy dane integracji
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "model": model,
        "coordinator": coordinator,
    }

    # Ładujemy platformy (sensor, binary_sensor)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload integracji."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id, {})
        client: HeatPumpModbusClient | None = data.get("client")
        if client:
            await client.close()

    return unload_ok
