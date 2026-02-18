# climates.py
ENTITIES = [
    {
        "name": "Ogrzewanie temperatura zadana",                                      # Nazwa encji wyświetlana w Home Assistant
        "unique_id": "ogrzewanie_temperatura_zadana",                                 # Unikalny identyfikator encji
        "model_path": __file__,                                                       # Ścieżka do pliku modelu — potrzebne do zapisu state.json

        # --- Rejestry temperatury ---
        "current_temp_register": 188,                                                 # Rejestr Modbus z aktualną temperaturą
        "target_temp_register": 1,                                                    # Rejestr Modbus z temperaturą zadaną (do ustawiania)
        "scale": 0.1,                                                                 # Skala — 188 → 18.8°C

        # --- Parametry slidera temperatury ---
        "min_temp": 10,                                                               # Minimalna temperatura możliwa do ustawienia
        "max_temp": 55,                                                               # Maksymalna temperatura możliwa do ustawienia
        "step": 1,                                                                    # Krok zmiany temperatury

        # --- Logika trybu HVAC (tylko ogrzewanie) ---
        "hvac_mode_register": 215,                                                    # Rejestr określający tryb pracy pompy
        "hvac_mode_values": {
            "heat": [1],                                                              # Jaka wartość ustawia Tryb  grzanie
            "off": [0, 2]                                                             # Jaka wartość ustawia Tryb off
        },
        "hvac_mode_register_2": 12,
        "hvac_mode_block_values": [2],
        "ignore_fallback": True,                                                      # Nie używamy fallbacku na rejestr 0
        "temp_hide_when_off": True,                                                   # Ukryj temperaturę, gdy encja jest w OFF
        "temp_off_register": None,                                                    # Brak osobnego rejestru temperatury w OFF

        # --- Logika slidera ---
        "slider_condition_register": 215,                                             # Rejestr, od którego zależy aktywność slidera
        "slider_disable_when": [0, 2],                                                # Wartości z rejestru, przy których slider jest wyłączony

        # --- Zapis trybu (tylko HEAT) ---
        "write_logic": {
            "heat": {"register": 0, "value": 1}                                       # Do którego rejestru i jaką wartość wysłać
        },

        # --- Restore (przy OFF przywracamy poprzednie ustawienia z pliku state.json) ---
        "restore_registers": [0, 10, 38, 39, 40],                                     # Lista rejestrów, które mają być przywracane po przejściu w OFF, które są zapisywane w pliku modelowym pod nazwą state.json

        "icon_heat": "mdi:radiator",                                                    # Ikona encji w interfejsie HA, gdy Tryb jest ustawiony na ogrzewanie
        "icon_off": "mdi:radiator-off",                                                 # Ikona encji w interfejsie HA, gdy Tryb jest ustawiony na off
    },


    {
        "name": "Chłodzenie temperatura zadana",
        "unique_id": "chlodzenie_temperatura_zadana",
        "model_path": __file__,
        "current_temperature_register": 188,
        "target_temp_register": 2,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 12,
        "max": 25,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
            
        },
        "hvac_mode_register_2": 12,
        "hvac_mode_block_values": [2],
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",

    },
    {
        "name": "CWU temperatura zadana",
        "unique_id": "cwu_temperatura_zadana",
        "model_path": __file__,
        "current_temperature_register": 195,
        "target_temp_register": 3,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 10,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [2],
            "off": [0, 1]
        },
        "hvac_mode_register_2": 12,
        "hvac_mode_block_values": [2],
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 1],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "Histereza ogrzewania i chłodzenia start",
        "unique_id": "histereza_ogrzewania_i_chlodzenia_start",
        "model_path": __file__,
        "current_temperature_register": 6,
        "target_temp_register": 6,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 1,
        "max": 15,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "cool": [0],
            "off": [2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": 2,
        "write_logic": {
            "heat": {"register": 0, "value": 1},
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
    },
    {
        "name": "Histereza ogrzewania i chłodzenia stop",
        "unique_id": "histereza_ogrzewania_i_chlodzenia_stop",
        "model_path": __file__,
        "current_temperature_register": 7,
        "target_temp_register": 7,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 0,
        "max": 5,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "cool": [0],
            "off": [2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": 2,
        "write_logic": {
            "heat": {"register": 0, "value": 1},
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
    },
    {
        "name": "CWU histereza start",
        "unique_id": "cwu_histereza_start",
        "model_path": __file__,
        "current_temperature_register": 4,
        "target_temp_register": 4,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 1,
        "max": 15,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": 2,
            "off": [0, 1]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "CWU histereza stop",
        "unique_id": "cwu_histereza_stop",
        "model_path": __file__,
        "current_temperature_register": 5,
        "target_temp_register": 5,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 0,
        "max": 5,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [2],
            "off": [0, 1]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 1],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "Chłodzenie temperatura zewnętrzna X1",
        "unique_id": "chlodzenie_temperatura_zewnetrzna_x1",
        "model_path": __file__,
        "current_temperature_register": 276,
        "target_temp_register": 276,
        "data_type": "int16",
        "scale": 0.1,
        "min": 16,
        "max": 60,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Chłodzenie temperatura zewnętrzna X2",
        "unique_id": "chlodzenie_temperatura_zewnetrzna_x2",
        "model_path": __file__,
        "current_temperature_register": 277,
        "target_temp_register": 277,
        "data_type": "int16",
        "scale": 0.1,
        "min": 16,
        "max": 60,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Chłodzenie temperatura zewnętrzna X3",
        "unique_id": "chlodzenie_temperatura_zewnetrzna_x3",
        "model_path": __file__,
        "current_temperature_register": 278,
        "target_temp_register": 278,
        "data_type": "int16",
        "scale": 0.1,
        "min": 16,
        "max": 60,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Chłodzenie temperatura zewnętrzna X4",
        "unique_id": "chlodzenie_temperatura_zewnetrzna_x4",
        "model_path": __file__,
        "current_temperature_register": 279,
        "target_temp_register": 279,
        "data_type": "int16",
        "scale": 0.1,
        "min": 16,
        "max": 60,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Chłodzenie temperatura zasilania Y1",
        "unique_id": "chlodzenie_temperatura_zasilania_y1",
        "model_path": __file__,
        "current_temperature_register": 336,
        "target_temp_register": 336,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 7,
        "max": 18,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Chłodzenie temperatura zasilania Y2",
        "unique_id": "chlodzenie_temperatura_zasilania_y2",
        "model_path": __file__,
        "current_temperature_register": 288,
        "target_temp_register": 288,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 7,
        "max": 18,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Chłodzenie temperatura zasilania Y3",
        "unique_id": "chlodzenie_temperatura_zasilania_y3",
        "model_path": __file__,
        "current_temperature_register": 289,
        "target_temp_register": 288,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 7,
        "max": 18,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Chłodzenie temperatura zasilania Y4",
        "unique_id": "chlodzenie_temperatura_zasilania_y4",
        "model_path": __file__,
        "current_temperature_register": 290,
        "target_temp_register": 290,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 7,
        "max": 18,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Ogrzewanie temperatura zewnętrzna X1",
        "unique_id": "ogrzewanie_temperatura_zewnetrzna_x1",
        "model_path": __file__,
        "current_temperature_register": 280,
        "target_temp_register": 280,
        "data_type": "int16",
        "scale": 0.1,
        "min": -50,
        "max": 20,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Ogrzewanie temperatura zewnętrzna X2",
        "unique_id": "ogrzewanie_temperatura_zewnetrzna_x2",
        "model_path": __file__,
        "current_temperature_register": 281,
        "target_temp_register": 281,
        "data_type": "int16",
        "scale": 0.1,
        "min": -50,
        "max": 20,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Ogrzewanie temperatura zewnętrzna X3",
        "unique_id": "ogrzewanie_temperatura_zewnetrzna_x3",
        "model_path": __file__,
        "current_temperature_register": 282,
        "target_temp_register": 282,
        "data_type": "int16",
        "scale": 0.1,
        "min": -50,
        "max": 20,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Ogrzewanie temperatura zewnętrzna X4",
        "unique_id": "ogrzewanie_temperatura_zewnetrzna_4",
        "model_path": __file__,
        "current_temperature_register": 283,
        "target_temp_register": 283,
        "data_type": "int16",
        "scale": 0.1,
        "min": -50,
        "max": 20,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Ogrzewanie temperatura zasilania Y1",
        "unique_id": "ogrzewanie_temperatura_zasilania_y1",
        "model_path": __file__,
        "current_temperature_register": 291,
        "target_temp_register": 291,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 15,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Ogrzewanie temperatura zasilania Y2",
        "unique_id": "ogrzewanie_temperatura_zasilania_y2",
        "model_path": __file__,
        "current_temperature_register": 292,
        "target_temp_register": 292,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 15,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Ogrzewanie temperatura zasilania Y3",
        "unique_id": "ogrzewanie_temperatura_zasilania_y3",
        "model_path": __file__,
        "current_temperature_register": 293,
        "target_temp_register": 293,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 15,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Ogrzewanie temperatura zasilania Y4",
        "unique_id": "ogrzewanie_temperatura_zasilania_y4",
        "model_path": __file__,
        "current_temperature_register": 337,
        "target_temp_register": 337,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 15,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "CWU temperatura zewnętrzna X1",
        "unique_id": "cwu_temperatura_zewnetrzna_x1",
        "model_path": __file__,
        "current_temperature_register": 284,
        "target_temp_register": 284,
        "data_type": "int16",
        "scale": 0.1,
        "min": -50,
        "max": 50,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [2],
            "off": [0, 1]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 1],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "CWU temperatura zewnętrzna X2",
        "unique_id": "cwu_temperatura_zewnetrzna_x2",
        "model_path": __file__,
        "current_temperature_register": 285,
        "target_temp_register": 285,
        "data_type": "int16",
        "scale": 0.1,
        "min": -50,
        "max": 50,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [2],
            "off": [0, 1]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 1],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "CWU temperatura zewnętrzna X3",
        "unique_id": "cwu_temperatura_zewnetrzna_x3",
        "model_path": __file__,
        "current_temperature_register": 286,
        "target_temp_register": 286,
        "data_type": "int16",
        "scale": 0.1,
        "min": -50,
        "max": 50,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [2],
            "off": [0, 1]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 1],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "CWU temperatura zewnętrzna X4",
        "unique_id": "cwu_temperatura_zewnetrzna_x4",
        "model_path": __file__,
        "current_temperature_register": 287,
        "target_temp_register": 287,
        "data_type": "int16",
        "scale": 0.1,
        "min": -50,
        "max": 50,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [2],
            "off": [0, 1]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 1],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "CWU temperatura zasilania Y1",
        "unique_id": "cwu_temperatura_zasilania_y1",
        "model_path": __file__,
        "current_temperature_register": 294,
        "target_temp_register": 294,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 10,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [2],
            "off": [0, 1]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 1],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "CWU temperatura zasilania Y2",
        "unique_id": "cwu_temperatura_zasilania_y2",
        "model_path": __file__,
        "current_temperature_register": 295,
        "target_temp_register": 295,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 10,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [2],
            "off": [0, 1]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 1],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "CWU temperatura zasilania Y3",
        "unique_id": "cwu_temperatura_zasilania_y3",
        "model_path": __file__,
        "current_temperature_register": 296,
        "target_temp_register": 296,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 10,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [2],
            "off": [0, 1]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 1],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "CWU temperatura zasilania Y4",
        "unique_id": "cwu_temperatura_zasilania_y4",
        "model_path": __file__,
        "current_temperature_register": 297,
        "target_temp_register": 297,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 10,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [2],
            "off": [0, 1]
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 1],
        "write_logic": {
            "heat": {"register": 0, "value": 2}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_heat": "mdi:shower",
        "icon_off": "mdi:water-off",
    },
    {
        "name": "Funkcja czasowa temperatura chłodzenia X1",
        "unique_id": "funkcja_czasowa_temperatura_chlodzenia_x1",
        "model_path": __file__,
        "current_temperature_register": 248,
        "target_temp_register": 248,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 7,
        "max": 18,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "hvac_mode_register_2": 39,
        "hvac_mode_block_values": [0],
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Funkcja czasowa temperatura ogrzewania X1",
        "unique_id": "funkcja_czasowa_temperatura_ogrzewania_x1",
        "model_path": __file__,
        "current_temperature_register": 249,
        "target_temp_register": 249,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 15,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "hvac_mode_register_2": 39,
        "hvac_mode_block_values": [0],
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Funkcja czasowa temperatura chłodzenia X2",
        "unique_id": "funkcja_czasowa_temperatura_chlodzenia_x2",
        "model_path": __file__,
        "current_temperature_register": 252,
        "target_temp_register": 252,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 7,
        "max": 18,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "hvac_mode_register_2": 39,
        "hvac_mode_block_values": [0],
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Funkcja czasowa temperatura ogrzewania X2",
        "unique_id": "funkcja_czasowa_temperatura_ogrzewania_x2",
        "model_path": __file__,
        "current_temperature_register": 253,
        "target_temp_register": 253,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 15,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "hvac_mode_register_2": 39,
        "hvac_mode_block_values": [0],
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Funkcja czasowa temperatura chłodzenia X3",
        "unique_id": "funkcja_czasowa_temperatura_chlodzenia_x3",
        "model_path": __file__,
        "current_temperature_register": 256,
        "target_temp_register": 256,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 7,
        "max": 18,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "hvac_mode_register_2": 39,
        "hvac_mode_block_values": [0],
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Funkcja czasowa temperatura ogrzewania X3",
        "unique_id": "funkcja_czasowa_temperatura_ogrzewania_x3",
        "model_path": __file__,
        "current_temperature_register": 257,
        "target_temp_register": 257,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 15,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "hvac_mode_register_2": 39,
        "hvac_mode_block_values": [0],
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Funkcja czasowa temperatura chłodzenia X4",
        "unique_id": "funkcja_czasowa_temperatura_chlodzenia_x4",
        "model_path": __file__,
        "current_temperature_register": 260,
        "target_temp_register": 260,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 7,
        "max": 18,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "cool": [0],
            "off": [1, 2]
        },
        "hvac_mode_register_2": 39,
        "hvac_mode_block_values": [0],
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [1, 2],
        "write_logic": {
            "cool": {"register": 0, "value": 0}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:snowflake",
        "icon_off": "mdi:snowflake-off",
    },
    {
        "name": "Funkcja czasowa temperatura ogrzewania X4",
        "unique_id": "funkcja_czasowa_temperatura_ogrzewania_x4",
        "model_path": __file__,
        "current_temperature_register": 261,
        "target_temp_register": 261,
        "data_type": "uint16",
        "scale": 0.1,
        "min": 15,
        "max": 55,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1],
            "off": [0, 2]
        },
        "hvac_mode_register_2": 39,
        "hvac_mode_block_values": [0],
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0, 2],
        "write_logic": {
            "heat": {"register": 0, "value": 1}
        },
        "restore_registers": [0, 10, 38, 39, 40],
        "icon_cool": "mdi:radiator",
        "icon_off": "mdi:radiator-off",
    },
    {
        "name": "Temperatura załączenia grzałki",
        "unique_id": "funkcja_czasowa_temperatura_ogrzewania_x4",
        "model_path": __file__,
        "current_temperature_register": 14,
        "target_temp_register": 14,
        "data_type": "int16",
        "scale": 0.1,
        "min": -30,
        "max": 20,
        "step": 1,
        "hvac_mode_register": 215,
        "hvac_mode_values": {
            "heat": [1, 2],
            "off": [0],
        },
        "ignore_fallback": True,
        "temp_hide_when_off": True,
        "temp_off_register": None,
        "slider_condition_register": 215,
        "slider_disable_when": [0],
    },
    {
        "name": "Delta T",
        "unique_id": "delta_t",
        "model_path": __file__,
        "current_temperature_register": 15,
        "target_temp_register": 15,
        "data_type": "uint16",
        "min": 2,
        "max": 15,
        "step": 1,
        "scale": 0.1,
        "temp_hide_when_off": False,
        "slider_disable_when": [],
    },

]
