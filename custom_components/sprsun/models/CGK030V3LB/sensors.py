SENSORS = [
    # --- CYFROWE / STATUSY / WYJŚCIA (Bity) ---
    {
        "unique_id": "d07_zaw_3_drog",
        "name": "Zawór trójdrogowy pozycja",
        "register": 6,  # 0x0005
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
        "unique_id": "temp_powrotu",
        "name": "Temperatura powrotu",
        "register": 19,
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.1,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "temp_zasilania",
        "name": "Temperatura zasilania",
        "register": 15,
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.1,
        "signed": True,
        "icon": "mdi:thermometer",
    },

]

DATA = SENSORS
