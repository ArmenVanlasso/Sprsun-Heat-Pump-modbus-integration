SENSORS = [
    # --- CYFROWE / STATUSY / WYJŚCIA (Bity) ---
    {
        "unique_id": "inlet_temp",
        "name": "Temperatura zasilania",
        "register": 14,  # 0x0012 wg dokumentacji CGK_B
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.1,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "hotwater_temp",
        "name": "Temperatura wody (CWU/zbiornik)",
        "register": 15,  # 0x000F wg dokumentacji CGK_B
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.1,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "ambi_temp",
        "name": "Temperatura zewnętrzna",
        "register": 17,  # 0x0011 wg dokumentacji CGK_B
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.5,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "outlet_temp",
        "name": "Temperatura powrotu",
        "register": 18,  # 0x000E wg dokumentacji CGK_B
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.1,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "suct_gas_temp",
        "name": "Temperatura ssania",
        "register": 21,  # 0x0015 wg dokumentacji CGK_B
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.5,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "coil_temp",
        "name": "Temperatura wężownicy (parownika)",
        "register": 22,  # 0x0016 wg dokumentacji CGK_B
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.5,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "exhaust_temperature",
        "name": "Temperatura tłoczenia (wylot gazu)",
        "register": 27,  # 0x001B wg dokumentacji CGK_B
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 1,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "eev1_step",
        "name": "EEV1 step.",
        "register": 28,  # 0x001C wg dokumentacji CGK_B
        # "scale": 0.1, Jaka to skala?
        "signed": True,
        "icon": "mdi:valve",
    },
    {
        "unique_id": "eev2_step",
        "name": "EEV2 step.",
        "register": 29,  # 0x001D wg dokumentacji CGK_B
        # "scale": 0.1, Jaka to skala?
        "signed": True,
        "icon": "mdi:valve",
    },
    {
        "unique_id": "comp_frequency",
        "name": "Częstotliwość sprężarki",
        "register": 30,  # 0x001E wg dokumentacji CGK_B
        "unit": "Hz",
        "device_class": "frequency",
        "state_class": "measurement",
        "scale": 1,
        "signed": True,
        "icon": "mdi:sine-wave",
    },
    {
        "unique_id": "dc_bus_voltage",
        "name": "DC bus voltage",
        "register": 33,  # 0x0021 wg dokumentacji CGK_B
        "unit": "V",
        "device_class": "voltage",
        "state_class": "measurement",
        "scale": 1,
        "signed": True,
        "icon": "mdi:lightning-bolt",
    },
    {
        "unique_id": "driving_temperature",
        "name": "Driving temperature",
        "register": 34,  # 0x0022 wg dokumentacji CGK_B
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.5,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "comp_current",
        "name": "Comp. current",
        "register": 35,  # 0x0023 wg dokumentacji CGK_B
        "unit": "A",
        "device_class": "current",
        "state_class": "measurement",
        "scale": 1,
        "signed": True,
        "icon": "mdi:current-ac",
    },
    {
        "unique_id": "target_frequency",
        "name": "Target frequency",
        "register": 36,  # 0x0024 wg dokumentacji CGK_B
        "unit": "Hz",
        "device_class": "frequency",
        "state_class": "measurement",
        "scale": 1,
        "signed": True,
        "icon": "mdi:sine-wave",
    },
    {
        "unique_id": "dc_fan_1_speed",
        "name": "DC fan 1 speed",
        "register": 38,  # 0x0026 wg dokumentacji CGK_B
        # "scale": 0.1, ?
        "icon": "mdi:fan",
    },
    {
        "unique_id": "dc_fan_2_speed",
        "name": "DC fan 2 speed",
        "register": 39,  # 0x0027 wg dokumentacji CGK_B
        # "scale": 0.1, ?
        "icon": "mdi:fan",
    },
    {
        "unique_id": "evap_temp",
        "name": "Temperatura odparowania",
        "register": 40,  # 0x0028 wg dokumentacji CGK_B
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.1,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "cond_temp",
        "name": "Temperatura kondensacji",
        "register": 41,  # 0x0029 wg dokumentacji CGK_B
        "unit": "°C",
        "device_class": "temperature",
        "state_class": "measurement",
        "scale": 0.1,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "dc_pump_speed",
        "name": "DC pump speed",
        "register": 46,  # 0x002E wg dokumentacji CGK_B
       # "device_class": "temperature",
        "state_class": "measurement",
       # "scale": 0.1,
        "signed": True,
        "icon": "mdi:thermometer",
    },
    {
        "unique_id": "suct_press",
        "name": "Ciśnienie ssania",
        "register": 47,  # 0x002F wg dokumentacji CGK_B
        "unit": "bar",
        "device_class": "pressure",
        "state_class": "measurement",
        "scale": 0.01,
        "icon": "mdi:gauge",
    },
    {
        "unique_id": "disch_press",
        "name": "Ciśnienie sprężania",
        "register": 48,  # 0x0030 wg dokumentacji CGK_B
        "unit": "bar",
        "device_class": "pressure",
        "state_class": "measurement",
        "scale": 0.01,
        "icon": "mdi:gauge",
    },
    {
        "unique_id": "dc_fan_target",
        "name": "DC fan target",
        "register": 49,  # 0x0031 wg dokumentacji CGK_B
        # "device_class": "pressure",
        "state_class": "measurement",
        # "scale": 0.1,
        # "icon": "mdi:gauge",
    },
    {
        "unique_id": "three_way_valve",
        "name": "Zawór trójdrogowy pozycja",
        "register": 5,  # 0x0005 wg dokumentacji CGK_B
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
]

DATA = SENSORS
