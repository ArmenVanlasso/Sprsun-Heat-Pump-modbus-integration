from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_CONNECTION_TYPE,
    CONF_HOST,
    CONF_PORT,
    CONF_SERIAL_PORT,
    CONF_UNIT_ID,
    CONF_MODEL,
    CONF_SCAN_INTERVAL,
    CONF_BAUDRATE,
    CONF_LANGUAGE,
    CONF_SET_FAN_HOURS,
    CONF_SET_COMPRESSOR_HOURS,
    CONF_FAN_HOURS,
    CONF_COMPRESSOR_HOURS,
    DEFAULT_SCAN_INTERVAL,
    CONNECTION_TYPE_RTU,
)

from .modbus_client_tcp import HeatPumpModbusTcpClient
from .modbus_client_rtu import HeatPumpModbusRtuClient
from .coordinator import SprsunCoordinator

_LOGGER = logging.getLogger(__name__)


# ==================================================================
#  WCZYTYWANIE PLIKÓW MODEL/LANG (*.py) — ZWRACA CAŁY NAMESPACE
# ==================================================================
async def async_load_py_dict(hass: HomeAssistant, path: Path) -> dict:
    """Czyta plik Python i zwraca pełny namespace jako dict."""

    def _load_sync() -> dict:
        if not path.exists():
            return {}

        namespace = {
            "__name__": path.stem,
            "__file__": str(path),
            "__package__": "custom_components.sprsun",
        }

        with path.open("r", encoding="utf-8") as f:
            code = compile(f.read(), str(path), "exec")
            exec(code, namespace)

        return namespace

    return await hass.async_add_executor_job(_load_sync)


# ==================================================================
#  HA SETUP
# ==================================================================
async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Konfiguracja integracji dla jednego wpisu."""
    hass.data.setdefault(DOMAIN, {})

    model = entry.data[CONF_MODEL].replace("-", "").replace("_", "")
    lang = entry.data[CONF_LANGUAGE].lower()
    unit_id = int(entry.data[CONF_UNIT_ID])
    scan_interval = int(entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL))
    connection_type = entry.data[CONF_CONNECTION_TYPE]

    # NOWE — pobranie ustawień offsetów czasów pracy
    set_fan_hours = entry.data.get(CONF_SET_FAN_HOURS, False)
    fan_hours = int(entry.data.get(CONF_FAN_HOURS, 0))

    set_compressor_hours = entry.data.get(CONF_SET_COMPRESSOR_HOURS, False)
    compressor_hours = int(entry.data.get(CONF_COMPRESSOR_HOURS, 0))

    # --- klient TCP/RTU ---
    if connection_type == CONNECTION_TYPE_RTU:
        client = HeatPumpModbusRtuClient(
            port=entry.data[CONF_SERIAL_PORT],
            slave_id=unit_id,
            baudrate=int(entry.data.get(CONF_BAUDRATE, 19200)),
        )
    else:
        client = HeatPumpModbusTcpClient(
            host=entry.data[CONF_HOST],
            port=int(entry.data[CONF_PORT]),
            unit_id=unit_id,
        )

    # --- koordynator ---
    coordinator = SprsunCoordinator(hass, client, entry.entry_id, model, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    # --- ścieżki do plików modelowych ---
    model_folder = Path(__file__).parent / "models" / model.upper()

    sensors        = await async_load_py_dict(hass, model_folder / "sensors.py")
    switches       = await async_load_py_dict(hass, model_folder / "switches.py")
    binary_sensors = await async_load_py_dict(hass, model_folder / "binary_sensors.py")
    numbers        = await async_load_py_dict(hass, model_folder / "numbers.py")
    selects        = await async_load_py_dict(hass, model_folder / "selects.py")
    buttons        = await async_load_py_dict(hass, model_folder / "buttons.py")
    climates       = await async_load_py_dict(hass, model_folder / "climates.py")
    logic_ns       = await async_load_py_dict(hass, model_folder / "logic_sensors.py")

    # --- zapis w hass.data ---
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "model": model,
        "language": lang,
        "coordinator": coordinator,

        # offsety czasów pracy
        "set_fan_hours": set_fan_hours,
        "fan_hours": fan_hours,
        "set_compressor_hours": set_compressor_hours,
        "compressor_hours": compressor_hours,

        "sensors": sensors.get("DATA", sensors),
        "switches": switches.get("DATA", switches),
        "binary_sensors": binary_sensors.get("DATA", binary_sensors),
        "numbers": numbers.get("DATA", numbers),
        "selects": selects.get("DATA", selects),
        "buttons": buttons.get("DATA", buttons),
        "climates": climates.get("DATA", climates),

        "logic_sensors": logic_ns.get("logic_sensors", []),
    }

    # ==================================================================
    #  NOWE — WSTRZYKNIĘCIE OFFSETÓW DO SENSORÓW LOGICZNYCH (TOTAL)
    # ==================================================================
    logic_sensors = hass.data[DOMAIN][entry.entry_id]["logic_sensors"]
    logic_offsets = entry.data.get("logic_offsets", {})

    for ls in logic_sensors:
        args = ls.get("args", {})
        uid = args.get("unique_id")

        if args.get("allow_offset") and uid:
            args["offset"] = logic_offsets.get(uid, 0)
            _LOGGER.debug(
                "Sprsun: ustawiam offset=%s dla logicznego sensora %s",
                args["offset"], uid
            )

    # ==================================================================
    #  ŁADOWANIE PLATFORM
    # ==================================================================
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


# ==================================================================
#  UNLOAD ENTRY
# ==================================================================
async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id, {})
        client = data.get("client")
        if client:
            try:
                result = client.close()
                if hasattr(result, "__await__"):
                    await result
            except Exception as exc:
                _LOGGER.warning("Błąd przy zamykaniu klienta Modbus: %s", exc)

    return unload_ok
