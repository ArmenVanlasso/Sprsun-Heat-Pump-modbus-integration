SENSORS = [
    # --- CYFROWE / STATUSY / WYJŚCIA (Bity) ---
    {
        "unique_id": "d07_zaw_3_drog",
        "name": "Zawór trójdrogowy pozycja",
        "register": 5,  # 0x0005
        "bit": 6,
        "source": "holding_register",  # Zgodnie z 03H Read holding registers
        "icon": "mdi:valve-open",
        "mapping": {
            0: "C.O.",
            1: "C.W.U.",
        },
        "icon_map": {
            0: "mdi:radiator",
            1: "mdi:bathtub",
        },
    },
    {
        "unique_id": "d07_kompresor_status",
        "name": "Kompresor",
        "register": 4,  # 0x0004
        "bit": 0,
        "source": "holding_register",
        "mapping": {0: "Wyłączony", 1: "Włączony"},
        "icon_map": {0: "mdi:snowflake-off", 1: "mdi:snowflake"},
    },
    {
        "unique_id": "d07_wentylator_status",
        "name": "Wentylator",
        "register": 4,  # 0x0004
        "bit": 5,
        "source": "holding_register",
        "mapping": {0: "Wyłączony", 1: "Włączony"},
        "icon_map": {0: "mdi:fan-off", 1: "mdi:fan"},
    },
    {
        "unique_id": "d07_pompa_co_status",
        "name": "Pompa obiegowa",
        "register": 6,  # 0x0006
        "bit": 6,
        "source": "holding_register",
        "mapping": {0: "Wyłączona", 1: "Włączona"},
        "icon_map": {0: "mdi:pump-off", 1: "mdi:pump"},
    },
    {
        "unique_id": "d07_grzalka_cwu_status",
        "name": "Grzałka C.W.U.",
        "register": 5,  # 0x0005
        "bit": 7,
        "source": "holding_register",
        "mapping": {0: "Wyłączona", 1: "Włączona"},
        "icon_map": {0: "mdi:heating-coil", 1: "mdi:heating-coil"},
    },
    {
        "unique_id": "d07_zapotrzebowanie_cwu",
        "name": "Zapotrzebowanie na C.W.U.",
        "register": 3,  # 0x0003
        "bit": 0,
        "source": "holding_register",
        "mapping": {0: "Brak", 1: "Tak"},
        "icon_map": {0: "mdi:water-boiler-off", 1: "mdi:water-boiler"},
    },
    {
        "unique_id": "d07_tryb_odszraniania",
        "name": "Status odszraniania (Defrost)",
        "register": 3,  # 0x0003
        "bit": 7,
        "source": "holding_register",
        "mapping": {0: "Nie", 1: "Odszranianie"},
        "icon_map": {0: "mdi:calendar-check", 1: "mdi:melt"},
    },
    {
        "unique_id": "d07_alarm_blokada",
        "name": "Stan awarii (Downtime)",
        "register": 3,  # 0x0003
        "bit": 6,
        "source": "holding_register",
        "mapping": {0: "OK", 1: "Awaria / Zatrzymanie"},
        "icon_map": {0: "mdi:check-circle", 1: "mdi:alert-circle"},
    },

    # --- ANALOGOWE / SENSORY NUMERYCZNE ---
    {
        "unique_id": "d07_temp_wejsciowa",
        "name": "Temperatura wody na wejściu (Powrót)",
        "register": 14,  # 0x000E
        "source": "holding_register",
        "unit": "°C",
        "multiplier": 0.1,
        "icon": "mdi:thermometer-minus",
    },
    {
        "unique_id": "d07_temp_wyjsciowa",
        "name": "Temperatura wody na wyjściu (Zasilanie)",
        "register": 18,  # 0x0012
        "source": "holding_register",
        "unit": "°C",
        "multiplier": 0.1,
        "icon": "mdi:thermometer-plus",
    },
    {
        "unique_id": "d07_temp_cwu",
        "name": "Temperatura zasobnika C.W.U.",
        "register": 15,  # 0x000F
        "source": "holding_register",
        "unit": "°C",
        "multiplier": 0.1,
        "icon": "mdi:water-thermometer",
    },
    {
        "unique_id": "d07_temp_zewnetrzna",
        "name": "Temperatura zewnętrzna",
        "register": 17,  # 0x0011
        "source": "holding_register",
        "unit": "°C",
        "multiplier": 0.5,
        "icon": "mdi:home-thermometer",
    },
    {
        "unique_id": "d07_temp_spalin",
        "name": "Temperatura na tłoczeniu kompresora (Exhaust)",
        "register": 27,  # 0x001B
        "source": "holding_register",
        "unit": "°C",
        "multiplier": 1.0,
        "icon": "mdi:fire",
    },
    {
        "unique_id": "d07_czestotliwosc_kompresora",
        "name": "Aktualna częstotliwość kompresora",
        "register": 30,  # 0x001E
        "source": "holding_register",
        "unit": "Hz",
        "multiplier": 1.0,
        "icon": "mdi:frequency-generator",
    },
    {
        "unique_id": "d07_cisnienie_ssania",
        "name": "Ciśnienie ssania",
        "register": 47,  # 0x002F
        "source": "holding_register",
        "unit": "bar",
        "multiplier": 0.1,
        "icon": "mdi:gauge",
    },
    {
        "unique_id": "d07_cisnienie_tloczenia",
        "name": "Ciśnienie tłoczenia",
        "register": 48,  # 0x0030
        "source": "holding_register",
        "unit": "bar",
        "multiplier": 0.1,
        "icon": "mdi:gauge",
    },
    {
        "unique_id": "d07_prad_kompresora",
        "name": "Prąd pracy kompresora",
        "register": 35,  # 0x0023
        "source": "holding_register",
        "unit": "A",
        "multiplier": 1.0,
        "icon": "mdi:current-ac",
    }
]

DATA = SENSORS
