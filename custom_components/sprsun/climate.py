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

# Import definicji climate z modeli
from .models.CGK025V3L.climates import ENTITIES as CLIMATES_025
from .models.CGK030V3L.climates import ENTITIES as CLIMATES_030
from .models.CGK040V3L.climates import ENTITIES as CLIMATES_040
from .models.CGK050V3L.climates import ENTITIES as CLIMATES_050
from .models.CGK060V3L.climates import ENTITIES as CLIMATES_060

_LOGGER = logging.getLogger(__name__)

MODEL_CLIMATE_MAP = {
    "cgk_025v3l": CLIMATES_025,
    "cgk_030v3l": CLIMATES_030,
    "cgk_040v3l": CLIMATES_040,
    "cgk_050v3l": CLIMATES_050,
    "cgk_060v3l": CLIMATES_060,
}


# ============================================================
#  SETUP PLATFORM
# ============================================================
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Tworzy encje climate na podstawie modelu i definicji."""
    coordinator: SprsunCoordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    client = hass.data[DOMAIN][entry.entry_id]["client"]
    model = hass.data[DOMAIN][entry.entry_id]["model"]

    definitions = MODEL_CLIMATE_MAP.get(model.lower(), [])

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

        # --- Logika HVAC (tylko odczyt) ---
        self._hvac_mode_register = definition.get("hvac_mode_register")
        self._hvac_mode_values = definition.get("hvac_mode_values", {})

        # Opcjonalny drugi rejestr i wartości blokujące (jeśli kiedyś użyjesz)
        self._hvac_mode_register_2 = definition.get("hvac_mode_register_2")
        self._hvac_mode_block_values = definition.get("hvac_mode_block_values", [])

        # --- Logika temperatury ---
        self._current_temp_reg = definition.get("current_temp_register")
        self._target_temp_register = definition.get("target_temp_register")

        # Parametry temperatury
        self._scale = definition.get("scale", 0.1)
        self._min_temp = definition.get("min_temp", 20)
        self._max_temp = definition.get("max_temp", 60)
        self._step = definition.get("temp_step", 1)

        # --- Sterowanie ukrywaniem w OFF na podstawie climates.py ---
        self._hide_temp_when_off = definition.get("hide_temp_when_off", False)
        self._disable_slider_when_off = definition.get(
            "disable_slider_when_off", False
        )

        # --- PRESETY (tryby pracy z jednego wspólnego rejestru) ---
        self._preset_register = definition.get("preset_register")
        self._preset_values = definition.get("preset_values", {})
        self._preset_reverse = {
            value: name for name, value in self._preset_values.items()
        }

        # Atrybuty HA
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_name = definition.get("name")
        self._attr_unique_id = definition.get("unique_id")

        # Tworzenie "ładnego" entity_id (bez polskich znaków)
        slug = (
            f"sprsun_{self._model}_{self._attr_name}"
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
        self.entity_id = f"climate.{slug}"

        # Zakres i krok temperatury zadanej – używane przez HA
        self._attr_min_temp = self._min_temp
        self._attr_max_temp = self._max_temp
        self._attr_target_temperature_step = self._step

    # ============================================================
    #  HVAC MODE – tylko odczyt z rejestru wg climates.py
    # ============================================================
    @property
    def hvac_mode(self) -> HVACMode:
        """Aktualny tryb HVAC na podstawie wartości rejestrów."""

        if self._hvac_mode_register is None:
            # Jeśli nie zdefiniowano rejestru – traktujemy jako OFF
            return HVACMode.OFF

        reg1 = self.coordinator.data.get(self._hvac_mode_register)

        # Opcjonalny drugi rejestr do blokowania trybów (jeśli użyty w definicji)
        reg2 = None
        if self._hvac_mode_register_2 is not None:
            reg2 = self.coordinator.data.get(self._hvac_mode_register_2)

        # Brak danych z głównego rejestru → OFF
        if reg1 is None:
            return HVACMode.OFF

        # Jeśli drugi rejestr jest ustawiony na wartość blokującą → ZAWSZE OFF
        if reg2 is not None and reg2 in self._hvac_mode_block_values:
            return HVACMode.OFF

        # Standardowa logika z climates.py
        for mode, values in self._hvac_mode_values.items():
            # values mogą być listą lub pojedynczą liczbą
            if isinstance(values, (list, tuple, set)):
                if reg1 in values:
                    return HVACMode(mode)
            else:
                if reg1 == values:
                    return HVACMode(mode)

        # Brak dopasowania → OFF
        return HVACMode.OFF

    @property
    def hvac_modes(self) -> list[HVACMode]:
        """
        Lista dostępnych trybów HVAC.

        Jeśli w definicji jest 'hvac_modes', używamy jej.
        W przeciwnym razie bierzemy klucze z 'hvac_mode_values'.
        """
        defined_modes = self._definition.get("hvac_modes")
        if defined_modes:
            return [HVACMode(m) for m in defined_modes]

        return [HVACMode(mode) for mode in self._hvac_mode_values.keys()]

    # ============================================================
    #  PRESETY – wspólny rejestr dla wszystkich encji
    # ============================================================
    @property
    def preset_modes(self) -> list[str] | None:
        """Lista dostępnych presetów (jeśli zdefiniowane w climates.py)."""
        if not self._preset_values:
            return None
        return list(self._preset_values.keys())

    @property
    def preset_mode(self) -> str | None:
        """Aktualny preset na podstawie wspólnego rejestru."""
        if self._preset_register is None or not self._preset_values:
            return None

        raw = self.coordinator.data.get(self._preset_register)
        if raw is None:
            return None

        return self._preset_reverse.get(raw)

    async def async_set_preset_mode(self, preset_mode: str):
        """Ustawia preset – tylko ta encja zapisuje do rejestru."""
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

        _LOGGER.debug(
            "Ustawiam preset_mode '%s' (wartość %s) w rejestrze %s dla %s",
            preset_mode,
            value,
            self._preset_register,
            self.entity_id,
        )

        await self._client.write_register(self._preset_register, value)
        await self.coordinator.async_request_refresh()

    # ============================================================
    #  IKONA – na podstawie aktualnego trybu
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
        """Bieżąca temperatura zdefiniowana w climates.py."""

        # Jeśli mamy ukrywać temperaturę w OFF i tryb jest OFF → nie pokazuj
        if self._hide_temp_when_off and self.hvac_mode == HVACMode.OFF:
            return None

        if self._current_temp_reg is None:
            return None

        raw = self.coordinator.data.get(self._current_temp_reg)
        if raw is None:
            return None

        # obsługa signed int16
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

        # obsługa signed int16
        if self._definition.get("data_type") == "int16" and raw > 32767:
            raw -= 65536

        return raw * self._scale

    # ============================================================
    #  WSPARCIE FUNKCJI – slider + presety
    # ============================================================
    @property
    def supported_features(self) -> ClimateEntityFeature:
        features = ClimateEntityFeature(0)

        # Presety – jeśli są zdefiniowane
        if self._preset_values:
            features |= ClimateEntityFeature.PRESET_MODE

        # Slider temperatury – tylko gdy nie ma blokady w OFF
        if not (self._disable_slider_when_off and self.hvac_mode == HVACMode.OFF):
            features |= ClimateEntityFeature.TARGET_TEMPERATURE

        return features

    # ============================================================
    #  ZMIANA TEMPERATURY – zapis do Modbus
    # ============================================================
    async def async_set_temperature(self, **kwargs):
        temp = kwargs.get("temperature")
        if temp is None or self._target_temp_register is None:
            _LOGGER.debug("%s: Brak temperatury lub rejestru docelowego", self.entity_id)
            return

        if self._disable_slider_when_off and self.hvac_mode == HVACMode.OFF:
            _LOGGER.debug("%s: Ignoruję zapis temperatury – HVAC OFF", self.entity_id)
            return

        value = int(temp / self._scale)

        _LOGGER.debug(
            "%s: Próba zapisu temperatury %.1f°C (wartość raw=%s) do rejestru %s",
            self.entity_id,
            temp,
            value,
            self._target_temp_register,
        )

        # --- ZAPIS ---
        await self._client.write_register(self._target_temp_register, value)

        # Daj pompie czas na zapis
        await asyncio.sleep(0.5)

        # Odśwież dane
        await self.coordinator.async_request_refresh()

        # Sprawdź, co pompa zwróciła po zapisie
        new_raw = self.coordinator.data.get(self._target_temp_register)
        new_temp = None
        if new_raw is not None:
            if self._definition.get("data_type") == "int16" and new_raw > 32767:
                new_raw -= 65536
            new_temp = new_raw * self._scale

        _LOGGER.debug(
            "%s: Po zapisie rejestr %s zwraca raw=%s (%.1f°C)",
            self.entity_id,
            self._target_temp_register,
            new_raw,
            new_temp if new_temp is not None else -999,
        )

        # Ostrzeżenie, jeśli pompa nie przyjęła wartości
        if new_temp is not None and abs(new_temp - temp) > 0.1:
            _LOGGER.warning(
                "%s: Pompa NIE przyjęła nowej temperatury! Ustawiono %.1f°C, ale odczytano %.1f°C",
                self.entity_id,
                temp,
                new_temp,
            )

    # ============================================================
    #  ZMIANA TRYBU HVAC – NIE STERUJEMY URZĄDZENIEM
    # ============================================================
    async def async_set_hvac_mode(self, hvac_mode: HVACMode):
        """
        Nie zapisujemy nic do Modbus przy zmianie trybu.
        Tryb HVAC jest tylko odczytem z rejestru wg climates.py.
        """
        _LOGGER.debug(
            "Ignoruję próbę zmiany hvac_mode na %s dla %s – tylko odczyt.",
            hvac_mode,
            self.entity_id,
        )
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
        """Subskrybuj aktualizacje z coordinatora."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )


    # ============================================================
    #  DEVICE INFO — przypisanie encji do jednego urządzenia
    # ============================================================
    @property
    def device_info(self):
        model_path = self._definition.get("model_path", "")
        model_folder = (
            os.path.basename(os.path.dirname(model_path)) if model_path else ""
        )
        model_name = model_folder.upper() if model_folder else self._model.upper()

        return {
            "identifiers": {(DOMAIN, self.coordinator.entry_id)},
            "name": f"Pompa ciepła Sprsun {model_name}",
            "manufacturer": "Sprsun",
            "model": model_name,
        }
