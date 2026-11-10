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
        "icon_heat": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
        "hvac_modes": ["heat", "off"],
        "hvac_mode_register": 54, # Tryb (CWU bit 0, Ogrzewanie bit 1, Chłodzenie bit 2, Ogrzewanie+CWU bit 3, Chłodzenie+CWU bit4)
        "hvac_mode_values": {
            "heat": 1,
            "off": [0, 2],
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
