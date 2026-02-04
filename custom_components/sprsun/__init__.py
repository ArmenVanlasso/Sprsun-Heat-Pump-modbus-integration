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
)
from .modbus_client import HeatPumpModbusClient

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
    # Tu zakładamy, że w config_flow zapisujesz już wartość z MODELS,
    # np. "cgk_025v3l", "cgk_030v3l" itd.
    model: str = entry.data[CONF_MODEL]

    _LOGGER.debug(
        "Inicjalizacja Sprsun Modbus: host=%s port=%s unit_id=%s model=%s",
        host,
        port,
        unit_id,
        model,
    )

    # Tworzymy klienta Modbus
    client = HeatPumpModbusClient(host, port, unit_id)

    # Zapisujemy dane integracji (dostępne potem w sensor.py)
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "model": model,
    }

    # Ładujemy platformy (np. sensor)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload integracji."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        data: dict[str, Any] = hass.data[DOMAIN].pop(entry.entry_id, {})
        client: HeatPumpModbusClient | None = data.get("client")
        if client is not None:
            # Jeśli HeatPumpModbusClient ma asynchroniczne zamknięcie:
            try:
                close_method = getattr(client, "close", None)
                if callable(close_method):
                    result = close_method()
                    # Jeśli close jest korutyną – await
                    if hasattr(result, "__await__"):
                        await result
            except Exception as exc:  # noqa: BLE001
                _LOGGER.warning("Błąd przy zamykaniu klienta Modbus: %s", exc)

    return unload_ok
