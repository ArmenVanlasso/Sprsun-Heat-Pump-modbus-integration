# climate.py

from __future__ import annotations

import logging
import asyncio
import os

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .coordinator import SprsunCoordinator

_LOGGER = logging.getLogger(__name__)


# ============================================================
#  SETUP PLATFORM
# ============================================================
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Tworzy encje climate na podstawie modelu i języka."""
    data = hass.data[DOMAIN][entry.entry_id]

    coordinator: SprsunCoordinator = data["coordinator"]
    client = data["client"]
    model = data["model"]

    # 🔥 definicje climate z folderu model/lang
    definitions = data["climates"]

    entities = [
        HeatPumpClimate(coordinator, definition, client, model)
        for definition in definitions
    ]

    async_add_entities(entities)


# ============================================================
#  UNIWERSALNY SILNIK CLIMATE – odczyt HVAC + presety
# ============================================================
class HeatPumpClimate(ClimateEntity):
    """Uniwersalny silnik Climate — logika zdefiniowana w climates.py."""

    def __init__(self, coordinator, definition: dict, client, model: str):
        self.coordinator = coordinator
        self._definition = definition
        self._client = client
        self._model = model

        # --- Logika HVAC ---
        self._hvac_mode_register = definition.get("hvac_mode_register")
        self._hvac_mode_values = definition.get("hvac_mode_values", {})

        self._hvac_mode_register_2 = definition.get("hvac_mode_register_2")
        self._hvac_mode_block_values = definition.get("hvac_mode_block_values", [])

        # --- Temperatury ---
        self._current_temp_reg = definition.get("current_temp_register")
        self._target_temp_register = definition.get("target_temp_register")

        self._scale = definition.get("scale", 0.1)
        self._min_temp = definition.get("min_temp", 20)
        self._max_temp = definition.get("max_temp", 60)
        self._step = definition.get("temp_step", 1)

        self._hide_temp_when_off = definition.get("hide_temp_when_off", False)
        self._disable_slider_when_off = definition.get("disable_slider_when_off", False)

        # --- Presety ---
        self._preset_register = definition.get("preset_register")
        self._preset_values = definition.get("preset_values", {})
        self._preset_reverse = {
            value: name for name, value in self._preset_values.items()
        }

        # --- Atrybuty HA ---
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_name = definition.get("name")
        self._attr_unique_id = definition.get("unique_id")

        # entity_id generowane z nazwy encji
        slug = (
            f"sprsun_{self._model}_{self._attr_name}"
            .lower()
            .replace(" ", "_")
            .replace("ą", "a").replace("ć", "c").replace("ę", "e")
            .replace("ł", "l").replace("ń", "n").replace("ó", "o")
            .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )
        self.entity_id = f"climate.{slug}"

        # Zakres temperatury
        self._attr_min_temp = self._min_temp
        self._attr_max_temp = self._max_temp
        self._attr_target_temperature_step = self._step

    # ============================================================
    #  HVAC MODE – tylko odczyt
    # ============================================================
    @property
    def hvac_mode(self) -> HVACMode:
        if self._hvac_mode_register is None:
            return HVACMode.OFF

        reg1 = self.coordinator.data.get(self._hvac_mode_register)

        reg2 = None
        if self._hvac_mode_register_2 is not None:
            reg2 = self.coordinator.data.get(self._hvac_mode_register_2)

        if reg1 is None:
            return HVACMode.OFF

        if reg2 is not None and reg2 in self._hvac_mode_block_values:
            return HVACMode.OFF

        for mode, values in self._hvac_mode_values.items():
            if isinstance(values, (list, tuple, set)):
                if reg1 in values:
                    return HVACMode(mode)
            else:
                if reg1 == values:
                    return HVACMode(mode)

        return HVACMode.OFF

    @property
    def hvac_modes(self) -> list[HVACMode]:
        defined_modes = self._definition.get("hvac_modes")
        if defined_modes:
            return [HVACMode(m) for m in defined_modes]

        return [HVACMode(mode) for mode in self._hvac_mode_values.keys()]

    # ============================================================
    #  PRESETY
    # ============================================================
    @property
    def preset_modes(self) -> list[str] | None:
        if not self._preset_values:
            return None
        return list(self._preset_values.keys())

    @property
    def preset_mode(self) -> str | None:
        if self._preset_register is None or not self._preset_values:
            return None

        raw = self.coordinator.data.get(self._preset_register)
        if raw is None:
            return None

        return self._preset_reverse.get(raw)

    async def async_set_preset_mode(self, preset_mode: str):
        if self._preset_register is None or not self._preset_values:
            return

        if preset_mode not in self._preset_values:
            _LOGGER.warning(
                "Nieznany preset_mode '%s' dla encji %s",
                preset_mode,
                self.entity_id,
            )
            return

        value = self._preset_values[preset_mode]

        await self._client.write_register(self._preset_register, value)
        await self.coordinator.async_request_refresh()

    # ============================================================
    #  IKONA
    # ============================================================
    @property
    def icon(self) -> str:
        mode = self.hvac_mode

        if mode == HVACMode.HEAT:
            return self._definition.get("icon_heat", "mdi:radiator")

        if mode == HVACMode.COOL:
            return self._definition.get("icon_cool", "mdi:snowflake")

        return self._definition.get("icon_off", "mdi:radiator-off")

    # ============================================================
    #  TEMPERATURA BIEŻĄCA
    # ============================================================
    @property
    def current_temperature(self) -> float | None:
        if self._hide_temp_when_off and self.hvac_mode == HVACMode.OFF:
            return None

        if self._current_temp_reg is None:
            return None

        raw = self.coordinator.data.get(self._current_temp_reg)
        if raw is None:
            return None

        if self._definition.get("data_type") == "int16" and raw > 32767:
            raw -= 65536

        return raw * self._scale

    # ============================================================
    #  TEMPERATURA ZADANA
    # ============================================================
    @property
    def target_temperature(self) -> float | None:
        if self._target_temp_register is None:
            return None

        raw = self.coordinator.data.get(self._target_temp_register)
        if raw is None:
            return None

        if self._definition.get("data_type") == "int16" and raw > 32767:
            raw -= 65536

        return raw * self._scale

    # ============================================================
    #  FUNKCJE
    # ============================================================
    @property
    def supported_features(self) -> ClimateEntityFeature:
        features = ClimateEntityFeature(0)

        if self._preset_values:
            features |= ClimateEntityFeature.PRESET_MODE

        if not (self._disable_slider_when_off and self.hvac_mode == HVACMode.OFF):
            features |= ClimateEntityFeature.TARGET_TEMPERATURE

        return features

    # ============================================================
    #  ZMIANA TEMPERATURY
    # ============================================================
    async def async_set_temperature(self, **kwargs):
        temp = kwargs.get("temperature")
        if temp is None or self._target_temp_register is None:
            return

        if self._disable_slider_when_off and self.hvac_mode == HVACMode.OFF:
            return

        value = int(temp / self._scale)

        await self._client.write_register(self._target_temp_register, value)
        await asyncio.sleep(0.5)
        await self.coordinator.async_request_refresh()

    # ============================================================
    #  ZMIANA TRYBU HVAC – ignorujemy
    # ============================================================
    async def async_set_hvac_mode(self, hvac_mode: HVACMode):
        await self.coordinator.async_request_refresh()

    # ============================================================
    #  ODŚWIEŻANIE
    # ============================================================
    @property
    def should_poll(self) -> bool:
        return False

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    async def async_added_to_hass(self):
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    # ============================================================
    #  DEVICE INFO
    # ============================================================
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.entry_id)},
            "name": f"Pompa ciepła Sprsun {self._model.upper().replace('_', '-')}",
            "manufacturer": "Sprsun",
            "model": self._model.upper().replace('_', '-'),
        }
