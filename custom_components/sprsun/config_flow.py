from __future__ import annotations

import voluptuous as vol
import serial.tools.list_ports
import logging
_LOGGER = logging.getLogger(__name__)
from homeassistant import config_entries
from homeassistant.core import callback

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_UNIT_ID,
    CONF_SCAN_INTERVAL,
    CONF_MODEL,
    CONF_LANGUAGE,
    CONF_CONNECTION_TYPE,
    CONF_SERIAL_PORT,
    CONF_BAUDRATE,
    CONF_SET_FAN_HOURS,
    CONF_SET_COMPRESSOR_HOURS,
    CONF_FAN_HOURS,
    CONF_COMPRESSOR_HOURS,
    DEFAULT_PORT,
    DEFAULT_UNIT_ID,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_LANGUAGE,
    DEFAULT_BAUDRATE,
)
AVAILABLE_MODELS = {
    "CGK025V3L": "CGK025V3L",
    "CGK030V3L": "CGK030V3L",
    "CGK040V3L": "CGK040V3L",
    "CGK050V3L": "CGK050V3L",
    "CGK060V3L": "CGK060V3L",
}

AVAILABLE_LANGUAGES = {
    "Polski": "pl",
    "English": "en",
    "日本語": "ja",
}

class SprsunConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    # =====================================================================
    #  KROK 1 — WYBÓR TCP/RTU
    # =====================================================================
    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            if user_input[CONF_CONNECTION_TYPE] == "tcp":
                return await self.async_step_tcp()
            else:
                return await self.async_step_rtu()

        schema = vol.Schema({
            vol.Required(CONF_CONNECTION_TYPE): vol.In(["tcp", "rtu"])
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    # =====================================================================
    #  KROK 2 — TCP
    # =====================================================================
    async def async_step_tcp(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Walidacja pól TCP
            if not user_input[CONF_HOST]:
                errors[CONF_HOST] = "host_required"

            if user_input[CONF_PORT] < 1 or user_input[CONF_PORT] > 65535:
                errors[CONF_PORT] = "invalid_port"

            if user_input[CONF_UNIT_ID] < 1 or user_input[CONF_UNIT_ID] > 255:
                errors[CONF_UNIT_ID] = "invalid_unit_id"

            if user_input[CONF_SCAN_INTERVAL] < 5:
                errors[CONF_SCAN_INTERVAL] = "min_5"

            if not errors:
                # Jeśli żaden checkbox nie zaznaczony → koniec konfiguracji
                if not user_input.get(CONF_SET_FAN_HOURS) and not user_input.get(CONF_SET_COMPRESSOR_HOURS):
                    selected_label = user_input[CONF_MODEL]
                    model_internal = AVAILABLE_MODELS[selected_label]
                    language_internal = AVAILABLE_LANGUAGES[user_input[CONF_LANGUAGE]]

                    return self.async_create_entry(
                        title=f"Sprsun {selected_label}",
                        data={
                            CONF_CONNECTION_TYPE: "tcp",
                            CONF_HOST: user_input[CONF_HOST],
                            CONF_PORT: user_input[CONF_PORT],
                            CONF_BAUDRATE: user_input[CONF_BAUDRATE],
                            CONF_UNIT_ID: user_input[CONF_UNIT_ID],
                            CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                            CONF_MODEL: model_internal,
                            CONF_LANGUAGE: language_internal,
                            CONF_SET_FAN_HOURS: False,
                            CONF_FAN_HOURS: 0,
                            CONF_SET_COMPRESSOR_HOURS: False,
                            CONF_COMPRESSOR_HOURS: 0,
                        },
                    )

                # Jeśli zaznaczono 1 lub 2 checkboxy → przechodzimy do kroku offsets
                self._tcp_data = user_input.copy()
                self._tcp_data[CONF_CONNECTION_TYPE] = "tcp"
                return await self.async_step_offsets()
            
        schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT, default=DEFAULT_PORT): vol.All(int, vol.Range(min=1, max=65535)),
            vol.Required(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): vol.All(int, vol.Range(min=1200, max=115200)),
            vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): vol.All(int, vol.Range(min=1, max=255)),
            vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(int, vol.Range(min=5)),
            vol.Required(CONF_MODEL): vol.In(list(AVAILABLE_MODELS.keys())),
            vol.Required(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): vol.In(list(AVAILABLE_LANGUAGES.keys())),
            vol.Optional(CONF_SET_FAN_HOURS, default=False): bool,
            vol.Optional(CONF_SET_COMPRESSOR_HOURS, default=False): bool,

        })

        return self.async_show_form(step_id="tcp", data_schema=schema, errors=errors)

    # =====================================================================
    #  KROK 2 — RTU
    # =====================================================================
    async def async_step_rtu(self, user_input=None):
        errors = {}

        ports = {}

        import glob
        import os

        # 1. Pobieramy wszystkie aliasy z /dev/serial/by-id/*
        by_id_paths = glob.glob("/dev/serial/by-id/*")

        # Mapa: port fizyczny -> pełna nazwa urządzenia
        device_names = {}

        for path in by_id_paths:
            try:
                real = os.path.realpath(path)
                label = path.replace("/dev/serial/by-id/", "")
                device_names[real] = label
            except Exception:
                pass

        # 2. Tworzymy listę portów TYLKO z urządzeniami
        for port, name in device_names.items():
            label = f"{port} | {name}"
            ports[port] = label

        if user_input is not None:
            if user_input[CONF_UNIT_ID] < 1 or user_input[CONF_UNIT_ID] > 255:
                errors[CONF_UNIT_ID] = "invalid_unit_id"

            if user_input[CONF_SCAN_INTERVAL] < 5:
                errors[CONF_SCAN_INTERVAL] = "min_5"

            if not errors:
                # Jeśli żaden checkbox nie zaznaczony → koniec konfiguracji
                if not user_input.get(CONF_SET_FAN_HOURS) and not user_input.get(CONF_SET_COMPRESSOR_HOURS):
                    selected_label = user_input[CONF_MODEL]
                    model_internal = AVAILABLE_MODELS[selected_label]
                    language_internal = AVAILABLE_LANGUAGES[user_input[CONF_LANGUAGE]]

                    return self.async_create_entry(
                        title=f"Sprsun {selected_label}",
                        data={
                            CONF_CONNECTION_TYPE: "rtu",
                            CONF_SERIAL_PORT: user_input[CONF_SERIAL_PORT],
                            CONF_BAUDRATE: user_input[CONF_BAUDRATE],
                            CONF_UNIT_ID: user_input[CONF_UNIT_ID],
                            CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                            CONF_MODEL: model_internal,
                            CONF_LANGUAGE: language_internal,
                            CONF_SET_FAN_HOURS: False,
                            CONF_FAN_HOURS: 0,
                            CONF_SET_COMPRESSOR_HOURS: False,
                            CONF_COMPRESSOR_HOURS: 0,
                        },
                    )

                # Jeśli zaznaczono checkboxy → krok offsets
                self._rtu_data = user_input.copy()
                self._rtu_data[CONF_CONNECTION_TYPE] = "rtu"
                return await self.async_step_offsets()

        schema = vol.Schema({
            vol.Required(CONF_SERIAL_PORT): vol.In(ports),
            vol.Required(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): vol.All(int, vol.Range(min=1200, max=115200)),
            vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): vol.All(int, vol.Range(min=1, max=255)),
            vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): vol.All(int, vol.Range(min=5)),
            vol.Required(CONF_MODEL): vol.In(list(AVAILABLE_MODELS.keys())),
            vol.Required(CONF_LANGUAGE, default=DEFAULT_LANGUAGE): vol.In(list(AVAILABLE_LANGUAGES.keys())),
            vol.Optional(CONF_SET_FAN_HOURS, default=False): bool,
            vol.Optional(CONF_SET_COMPRESSOR_HOURS, default=False): bool,
        })

        return self.async_show_form(step_id="rtu", data_schema=schema, errors=errors)
    # =====================================================================
    #  KROK 3 — OFFSETY (jeśli zaznaczono checkboxy)
    # =====================================================================
    async def async_step_offsets(self, user_input=None):
        errors = {}

        _LOGGER.warning("OFFSET STEP START — user_input=%s", user_input)

        base = getattr(self, "_tcp_data", None) or getattr(self, "_rtu_data", None)
        _LOGGER.warning("OFFSET BASE DATA=%s", base)

        set_fan = base.get(CONF_SET_FAN_HOURS, False)
        set_comp = base.get(CONF_SET_COMPRESSOR_HOURS, False)
        _LOGGER.warning("OFFSET FLAGS — set_fan=%s set_comp=%s", set_fan, set_comp)

        if user_input is not None:
            final = base.copy()
            final[CONF_FAN_HOURS] = user_input.get(CONF_FAN_HOURS, 0)
            final[CONF_COMPRESSOR_HOURS] = user_input.get(CONF_COMPRESSOR_HOURS, 0)

            _LOGGER.warning("FINAL ENTRY DATA=%s", final)

            selected_label = final[CONF_MODEL]
            model_internal = AVAILABLE_MODELS[selected_label]

            # Tworzymy entry
            if final[CONF_CONNECTION_TYPE] == "tcp":
                return self.async_create_entry(
                    title=f"Sprsun {selected_label}",
                    data={
                        CONF_CONNECTION_TYPE: "tcp",
                        CONF_HOST: final[CONF_HOST],
                        CONF_PORT: final[CONF_PORT],
                        CONF_BAUDRATE: final[CONF_BAUDRATE],
                        CONF_UNIT_ID: final[CONF_UNIT_ID],
                        CONF_SCAN_INTERVAL: final[CONF_SCAN_INTERVAL],
                        CONF_MODEL: model_internal,
                        CONF_LANGUAGE: AVAILABLE_LANGUAGES[final[CONF_LANGUAGE]],
                        CONF_SET_FAN_HOURS: set_fan,
                        CONF_FAN_HOURS: final.get(CONF_FAN_HOURS, 0),
                        CONF_SET_COMPRESSOR_HOURS: set_comp,
                        CONF_COMPRESSOR_HOURS: final.get(CONF_COMPRESSOR_HOURS, 0),
                    },
                )
            else:
                return self.async_create_entry(
                    title=f"Sprsun {selected_label}",
                    data={
                        CONF_CONNECTION_TYPE: "rtu",
                        CONF_SERIAL_PORT: final[CONF_SERIAL_PORT],
                        CONF_BAUDRATE: final[CONF_BAUDRATE],
                        CONF_UNIT_ID: final[CONF_UNIT_ID],
                        CONF_SCAN_INTERVAL: final[CONF_SCAN_INTERVAL],
                        CONF_MODEL: model_internal,
                        CONF_LANGUAGE: AVAILABLE_LANGUAGES[final[CONF_LANGUAGE]],
                        CONF_SET_FAN_HOURS: set_fan,
                        CONF_FAN_HOURS: final.get(CONF_FAN_HOURS, 0),
                        CONF_SET_COMPRESSOR_HOURS: set_comp,
                        CONF_COMPRESSOR_HOURS: final.get(CONF_COMPRESSOR_HOURS, 0),
                    },
                )

        # Budujemy formularz offsetów
        schema_dict = {}

        # Offsety czasów pracy (jeśli zaznaczone)
        if set_fan:
            schema_dict[vol.Required(CONF_FAN_HOURS, default=0)] = vol.All(int, vol.Range(min=0, max=9999))

        if set_comp:
            schema_dict[vol.Required(CONF_COMPRESSOR_HOURS, default=0)] = vol.All(int, vol.Range(min=0, max=9999))

        # Offsety dla sensorów TOTAL
        schema_dict[vol.Optional("offset_sprezarka_total", default=0)] = vol.All(int, vol.Range(min=0, max=999999))
        schema_dict[vol.Optional("offset_wentylator_total", default=0)] = vol.All(int, vol.Range(min=0, max=999999))
        schema_dict[vol.Optional("offset_defrost_total", default=0)] = vol.All(int, vol.Range(min=0, max=999999))
        schema_dict[vol.Optional("offset_valve_total", default=0)] = vol.All(int, vol.Range(min=0, max=999999))

        return self.async_show_form(
            step_id="offsets",
            data_schema=vol.Schema(schema_dict),
            errors=errors
        )


    # =====================================================================
    #  OPTIONS FLOW
    # =====================================================================
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SprsunOptionsFlowHandler(config_entry)


class SprsunOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        super().__init__()
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        errors = {}

        data = self._config_entry.data
        options = self._config_entry.options

        scan_interval = options.get(
            CONF_SCAN_INTERVAL,
            data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )

        if user_input is not None:
            new_interval = user_input.get(CONF_SCAN_INTERVAL, scan_interval)

            if new_interval < 5:
                errors[CONF_SCAN_INTERVAL] = "min_5"
            else:
                return self.async_create_entry(
                    title="",
                    data={CONF_SCAN_INTERVAL: new_interval},
                )

        schema = vol.Schema({
            vol.Required(CONF_SCAN_INTERVAL, default=scan_interval):
                vol.All(int, vol.Range(min=5)),
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
