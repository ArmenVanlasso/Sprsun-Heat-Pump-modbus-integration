import logging
import json
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
#  UNIWERSALNY SILNIK CLIMATE
# ============================================================
class HeatPumpClimate(ClimateEntity):
    """Uniwersalny silnik Climate — cała logika sterowana z climates.py."""

    def __init__(self, coordinator, definition, client, model):
        self.coordinator = coordinator
        self._definition = definition
        self._client = client
        self._model = model

        # Logika HVAC
        self._hvac_mode_register = definition.get("hvac_mode_register")
        self._hvac_mode_values = definition.get("hvac_mode_values", {})
        self._ignore_fallback = definition.get("ignore_fallback", True)
        self._hvac_mode_register_2 = definition.get("hvac_mode_register_2")
        self._hvac_mode_block_values = definition.get("hvac_mode_block_values", [])

        # Logika temperatury
        self._current_temp_reg = definition.get("current_temp_register")
        self._temp_hide_when_off = definition.get("temp_hide_when_off", True)
        self._temp_off_register = definition.get("temp_off_register")

        # Logika slidera
        self._target_temp_register = definition.get("target_temp_register")
        self._slider_disable_when = definition.get("slider_disable_when")
        self._slider_condition_register = definition.get("slider_condition_register")

        # Logika zapisu trybów
        self._write_logic = definition.get("write_logic", {})

        # Parametry temperatury
        self._scale = definition.get("scale", 0.1)
        self._min_temp = definition.get("min_temp", 20)
        self._max_temp = definition.get("max_temp", 60)
        self._step = definition.get("step", 1)

        # Atrybuty HA
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_name = definition.get("name")
        self._attr_unique_id = definition.get("unique_id")
        slug = (
            f"sprsun_{self._model}_{self._attr_name}"
            .lower()
            .replace(" ", "_")
            .replace("ą", "a").replace("ć", "c").replace("ę", "e")
            .replace("ł", "l").replace("ń", "n").replace("ó", "o")
            .replace("ś", "s").replace("ź", "z").replace("ż", "z")
        )
        self.entity_id = f"climate.{slug}"


    # ============================================================
    #  OBSŁUGA PLIKU state.json
    # ============================================================
    def _get_state_file_path(self):
        model_path = self._definition.get("model_path")
        if model_path is None:
            return None
        model_folder = os.path.dirname(model_path)
        return os.path.join(model_folder, "state.json")

    def _save_state_to_file(self, state):
        path = self._get_state_file_path()
        if path is None:
            return
        with open(path, "w") as f:
            json.dump(state, f)

    def _load_state_from_file(self):
        path = self._get_state_file_path()
        if path is None or not os.path.exists(path):
            return {}
        with open(path, "r") as f:
            return json.load(f)

    # ============================================================
    #  HVAC MODE
    # ============================================================
    @property
    def hvac_mode(self):
        # Główny rejestr trybu (np. 215)
        reg1 = self.coordinator.data.get(self._hvac_mode_register)

        # Drugi rejestr (np. 12) – opcjonalny
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
            # Uwaga: tu values mogą być listą lub pojedynczą liczbą
            if isinstance(values, (list, tuple, set)):
                if reg1 in values:
                    return HVACMode(mode)
            else:
                if reg1 == values:
                    return HVACMode(mode)

        return HVACMode.OFF

    @property
    def hvac_modes(self):
        return [HVACMode(mode) for mode in self._hvac_mode_values.keys()]

    @property
    def icon(self):
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
    def current_temperature(self):
        mode = self.hvac_mode

        # Ukrywanie temperatury w OFF
        if mode == HVACMode.OFF and self._temp_hide_when_off:
            return None

        # Osobny rejestr temperatury w OFF
        if mode == HVACMode.OFF and self._temp_off_register is not None:
            raw = self.coordinator.data.get(self._temp_off_register)
            return raw * self._scale if raw is not None else None
        # Normalna temperatura
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
    def target_temperature(self):
        raw = self.coordinator.data.get(self._target_temp_register)
        if raw is None:
            return None
        # obsługa signed int16
        if self._definition.get("data_type") == "int16" and raw > 32767:
            raw -= 65536

        return raw * self._scale


    @property
    def supported_features(self):
        # Wyłączenie slidera
        if self._slider_disable_when is not None:
            reg = self.coordinator.data.get(self._slider_condition_register)
            if isinstance(self._slider_disable_when, (list, tuple)) and reg in self._slider_disable_when:
                return ClimateEntityFeature(0)

        return ClimateEntityFeature.TARGET_TEMPERATURE

    async def async_set_temperature(self, **kwargs):
        temp = kwargs.get("temperature")
        if temp is None:
            return

        value = int(temp / self._scale)
        await self._client.write_register(self._target_temp_register, value)
        await self.coordinator.async_request_refresh()

    # ============================================================
    #  ZMIANA TRYBU HVAC
    # ============================================================
    async def async_set_hvac_mode(self, hvac_mode):
        mode = hvac_mode.value
        restore_regs = self._definition.get("restore_registers", [])

        # ------------------------------------------------------------
        # OFF → przywrócenie poprzednich wartości z pliku state.json
        # ------------------------------------------------------------
        if mode == "off":
            saved_state = self._load_state_from_file()

            for reg, value in saved_state.items():
                await self._client.write_register(int(reg), value)

            await self.coordinator.async_request_refresh()
            return

        # ------------------------------------------------------------
        # HEAT / COOL → zapisanie aktualnych rejestrów do pliku
        # ------------------------------------------------------------
        current_state = {}
        for reg in restore_regs:
            current_state[reg] = self.coordinator.data.get(reg)

        self._save_state_to_file(current_state)

        # ------------------------------------------------------------
        # Zapis trybu (np. HEAT → register 0 = 2)
        # ------------------------------------------------------------
        write_def = self._write_logic.get(mode)
        if write_def:
            await self._client.write_register(write_def["register"], write_def["value"])

        await self.coordinator.async_request_refresh()


    # ============================================================
    #  ODŚWIEŻANIE
    # ============================================================
    @property
    def should_poll(self):
        return False

    async def async_update(self):
        await self.coordinator.async_request_refresh()

    # ============================================================
    #  DEVICE INFO — przypisanie encji do jednego urządzenia
    # ============================================================
    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.entry_id)},
            "name": f"Pompa ciepła Sprsun {self._definition.get('model_path').split('/')[-2].upper()}",
            "manufacturer": "Sprsun",
            "model": self._definition.get("model_path").split("/")[-2].upper(),
        }

