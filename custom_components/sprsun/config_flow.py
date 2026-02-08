# config_flow.py
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_HOST,
    CONF_PORT,
    CONF_UNIT_ID,
    CONF_SCAN_INTERVAL,
    CONF_MODEL,
    DEFAULT_PORT,
    DEFAULT_UNIT_ID,
    DEFAULT_SCAN_INTERVAL,
    MODELS,
)

class SprsunConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        errors = {}

        if user_input is not None:

            for entry in self._async_current_entries():
                if entry.data.get(CONF_HOST) == user_input[CONF_HOST]:
                    return self.async_abort(reason="already_configured")

            if not user_input[CONF_HOST]:
                errors[CONF_HOST] = "host_required"

            if user_input[CONF_PORT] < 1 or user_input[CONF_PORT] > 65535:
                errors[CONF_PORT] = "invalid_port"

            if user_input[CONF_UNIT_ID] < 1 or user_input[CONF_UNIT_ID] > 255:
                errors[CONF_UNIT_ID] = "invalid_unit_id"

            if user_input[CONF_SCAN_INTERVAL] < 5:
                errors[CONF_SCAN_INTERVAL] = "min_5"

            if not errors:
                selected_label = user_input[CONF_MODEL]
                model_internal = MODELS[selected_label]

                return self.async_create_entry(
                    title=f"Sprsun {selected_label}",
                    data={
                        CONF_HOST: user_input[CONF_HOST],
                        CONF_PORT: user_input[CONF_PORT],
                        CONF_UNIT_ID: user_input[CONF_UNIT_ID],
                        CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                        CONF_MODEL: model_internal,
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_HOST): selector.TextSelector(
                    selector.TextSelectorConfig(
                        type=selector.TextSelectorType.TEXT,
                    )
                ),
                vol.Required(CONF_PORT, default=DEFAULT_PORT): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=65535,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Required(CONF_UNIT_ID, default=DEFAULT_UNIT_ID): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=255,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Required(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=5,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Required(CONF_MODEL): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=list(MODELS.keys()),
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SprsunOptionsFlowHandler(config_entry)


class SprsunOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        errors = {}

        data = self.config_entry.data
        options = self.config_entry.options

        scan_interval = options.get(
            CONF_SCAN_INTERVAL, data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )

        if user_input is not None:
            if user_input[CONF_SCAN_INTERVAL] < 5:
                errors[CONF_SCAN_INTERVAL] = "min_5"

            if not errors:
                return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_SCAN_INTERVAL, default=scan_interval): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=5,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )
