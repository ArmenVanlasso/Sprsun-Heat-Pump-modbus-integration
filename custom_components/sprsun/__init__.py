from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_HOST,
    CONF_PORT,
    CONF_UNIT_ID,
    CONF_MODEL,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)

from .modbus_client import HeatPumpModbusClient
from .coordinator import SprsunCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Ogólny setup (nieużywany przy config entries)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup integracji z jednego config entry."""
    hass.data.setdefault(DOMAIN, {})

    host: str = entry.data[CONF_HOST]
    port: int = entry.data[CONF_PORT]
    unit_id: int = entry.data[CONF_UNIT_ID]
    model: str = entry.data[CONF_MODEL]
    scan_interval: int = entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    _LOGGER.debug(
        "Inicjalizacja Sprsun Modbus: host=%s port=%s unit_id=%s model=%s scan=%s",
        host,
        port,
        unit_id,
        model,
        scan_interval,
    )

    # Tworzymy klienta Modbus
    client = HeatPumpModbusClient(host, port, unit_id)

    # Tworzymy koordynator
    coordinator = SprsunCoordinator(
        hass,
        client,
        entry.entry_id,
        model,
        scan_interval,
    )

    # Pierwszy odczyt blokowy
    await coordinator.async_config_entry_first_refresh()

    # Zapisujemy dane integracji
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "model": model,
        "coordinator": coordinator,
    }

    # Ładujemy platformy (sensor, climate, select, switch, button)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload integracji."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        data: dict[str, Any] = hass.data[DOMAIN].pop(entry.entry_id, {})
        client: HeatPumpModbusClient | None = data.get("client")

        if client is not None:
            try:
                close_method = getattr(client, "close", None)
                if callable(close_method):
                    result = close_method()
                    if hasattr(result, "__await__"):
                        await result
            except Exception as exc:
                _LOGGER.warning("Błąd przy zamykaniu klienta Modbus: %s", exc)

    return unload_ok
