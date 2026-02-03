import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS, CONF_HOST, CONF_PORT, CONF_UNIT_ID
from .modbus_client import HeatPumpModbusClient

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Ogólny setup (nic tu nie robimy, używamy config entries)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Setup integracji z jednego config entry (utworzonego w config_flow)."""
    hass.data.setdefault(DOMAIN, {})

    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    unit_id = entry.data[CONF_UNIT_ID]

    client = HeatPumpModbusClient(host, port, unit_id)
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
    }

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
