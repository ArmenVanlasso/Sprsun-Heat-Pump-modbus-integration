# climates.py
from __future__ import annotations
CLIMATES = [
    {
        "name": "P04 nastawa CWU",
        "unique_id": "p04_hotwater_setpoint",
        "temperature_unit": "C",
        "precision": 0,
        "temp_step": 0.5,
        "max_temp": 55,
        "min_temp": 10,
        "data_type": "uint16",
        "input_type": "holding",
        "scale": 0.1,
        "current_temp_register": 18, # Temperatura powrotu
        "target_temp_register": 202, # Grzanie nastawa (climate)
        "icon_heat": "mdi:bathtub",
        "icon_off": "mdi:bathtub-outline",
        "hvac_modes": ["heat", "off"],
        "hvac_mode_register": 54, # Tryb (CWU bit 0, Ogrzewanie bit 1, Chłodzenie bit 2, Ogrzewanie+CWU bit 3, Chłodzenie+CWU bit4)
        "hvac_mode_values": {
            "heat": [0, 3, 4],
            "off": [1, 2],
        },
            "preset_register": 0,
            "preset_values": {
            "CWU": 0,
            "Ogrzewanie": 1,
            "Chłodzenie": 2,
            "Ogrzewanie+CWU": 3,
            "Chłodzenie+CWU": 4,
        },
    },

    {
        "name": "P02 Nastawa chłodzenie",
        "unique_id": "p02_cooling_setpoint",
        "temperature_unit": "C",
        "precision": 0,
        "temp_step": 0.5,
        "max_temp": 30,
        "min_temp": 12,
        "data_type": "uint16",
        "input_type": "holding",
        "scale": 0.1,
        "current_temp_register": 18, # Temperatura powrotu
        "target_temp_register": 203, # Grzanie nastawa (climate)
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
        "hvac_modes": ["cool", "off"],
        "hvac_mode_register": 54, # Tryb (CWU bit 0, Ogrzewanie bit 1, Chłodzenie bit 2, Ogrzewanie+CWU bit 3, Chłodzenie+CWU bit4)
        "hvac_mode_values": {
            "cool": [2, 4],
            "off": [0, 1, 3],
        },
            "preset_register": 0,
            "preset_values": {
            "CWU": 0,
            "Ogrzewanie": 1,
            "Chłodzenie": 2,
            "Ogrzewanie+CWU": 3,
            "Chłodzenie+CWU": 4,
        },
    },

    {
        "name": "P01 nastawa ogrzewanie",
        "unique_id": "p01_heating_setpoint",
        "temperature_unit": "C",
        "precision": 0,
        "temp_step": 0.5,
        "max_temp": 55,
        "min_temp": 10,
        "data_type": "uint16",
        "input_type": "holding",
        "scale": 0.1,
        "current_temp_register": 18, # Temperatura powrotu
        "target_temp_register": 204, # Grzanie nastawa (climate)
        "icon_heat": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
        "hvac_modes": ["heat", "off"],
        "hvac_mode_register": 54, # Tryb (CWU bit 0, Ogrzewanie bit 1, Chłodzenie bit 2, Ogrzewanie+CWU bit 3, Chłodzenie+CWU bit4)
        "hvac_mode_values": {
            "haeat": [1, 3],
            "off": [0, 2, 4],
        },
            "preset_register": 0,
            "preset_values": {
            "CWU": 0,
            "Ogrzewanie": 1,
            "Chłodzenie": 2,
            "Ogrzewanie+CWU": 3,
            "Chłodzenie+CWU": 4,
        },
    },
]
DATA = CLIMATES
