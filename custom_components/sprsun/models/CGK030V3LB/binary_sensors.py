BINARY_SENSORS = [
    {
        "unique_id": "ac_linkage_switch",
        "name": "A/C linkage switch",
        "register": 2,
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "linkage_switch",
        "name": "Linkage switch",
        "register": 2,
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "heating_linkage",
        "name": "Heating linkage",
        "register": 2,
        "bit": 2,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "cooling_linkage",
        "name": "Cooling linkage",
        "register": 2,
        "bit": 3,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "flow_switch",
        "name": "Flow switch",
        "register": 2,
        "bit": 4,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "high_pressure_switch",
        "name": "High pressure switch",
        "register": 2,
        "bit": 5,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "phase_sequence_detection",
        "name": "Kolejność faz",
        "register": 2,
        "bit": 6,
        "source": "holding_register",
        "device_class": "problem",
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert-circle",
        },
    },
    {
        "unique_id": "hotwater_demand",
        "name": "Hotwater demand",
        "register": 3,
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "heating_demand",
        "name": "Heating demand",
        "register": 3,
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "with_or_without_heating",
        "name": " With or without heating",
        "register": 3,
        "bit": 2,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "with_or_without_cooling",
        "name": "With or without cooling",
        "register": 3,
        "bit": 3,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "antilegionella_on",
        "name": "Antilegionella on",
        "register": 3,
        "bit": 4,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "cooling_demand",
        "name": "Cooling demand",
        "register": 3,
        "bit": 5,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "alarm_downtime",
        "name": "Alarm downtime",
        "register": 3,
        "bit": 6,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "defrost",
        "name": "Defrost",
        "register": 3,
        "bit": 7,
        "source": "holding_register",
        "icon": "mdi:snowflake-off",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:snowflake-off",
            1: "mdi:snowflake",
        },
    },
    {
        "unique_id": "compressor",
        "name": "Sprężarka",
        "register": 4,
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:bag-personal-off",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:bag-personal-off",
            1: "mdi:bag-personal-on",
        },
    },
    {
        "unique_id": "fan",
        "name": "Wentylator",
        "register": 4,
        "bit": 5,
        "source": "holding_register",
        "icon": "mdi:fan-off",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:fan-off",
            1: "mdi:fan-on",
        },
    },
    {
        "unique_id": "4_way_valve",
        "name": "Zawór 4 drogowy",
        "register": 4,
        "bit": 6,
        "source": "holding_register",
        "icon": "mdi:valve_closed",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-open",
            1: "mdi:valve_closed",
        },
    },
    {
        "unique_id": "high_or_low_fan_speed",
        "name": "Wysoka lub niska prędkość wentylatora",
        "register": 4,
        "bit": 7,
        "source": "holding_register",
        "icon": "mdi:fan",
        "mapping": {
            0: "low",
            1: "high",
        },
    },
    {
        "unique_id": "hassis_heater",
        "name": "Grzałka obudowy",
        "register": 5,
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:radiator-disabled",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:radiator-disabled",
            1: "mdi:radiator",
        },
    },
    {
        "unique_id": "heating_heater",
        "name": "Heating heater",
        "register": 5,
        "bit": 5,
        "source": "holding_register",
        "icon": "mdi:radiator-disabled",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:radiator-disabled",
            1: "mdi:radiator",
        },
    },
    {
        "unique_id": "three_way_valve",
        "name": "Zawór 3 drogowy",
        "register": 5,
        "bit": 6,
        "source": "holding_register",
        "icon": "mdi:valve-closed",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "hotwater_heater",
        "name": "Hotwater heater",
        "register": 5,
        "bit": 7,
        "source": "holding_register",
        "icon": "mdi:valve-closed",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "ac_pump",
        "name": "A/C pump",
        "register": 6,
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:pump-off",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:pump-off",
            1: "mdi:pump",
        },
    },
    {
        "unique_id": "crank_heater",
        "name": "Grzałka karteru sprężarki",
        "register": 6,
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:radiator-disabled",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:radiator-disabled",
            1: "mdi:radiator",
        },
    },
    {
        "unique_id": "assistant_solenoid_valve",
        "name": "Assistant solenoid valve",
        "register": 6,
        "bit": 5,
        "source": "holding_register",
        "icon": "mdi:valve-closed",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "pump",
        "name": "Pump",
        "register": 6,
        "bit": 6,
        "source": "holding_register",
        "icon": "mdi:pump-off",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:pump-off",
            1: "mdi:pump",
        },
    },
    {
        "unique_id": "hotwater_temp",
        "name": "Temperatura CWU",
        "entity_category": "diagnostic",
        "register": 7, #0x0007
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "ambi_temp",
        "name": "Temperatura zewnętrzna",
        "entity_category": "diagnostic",
        "register": 7, #0x0007
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "coil_temp",
        "name": "Temperatura parownika",
        "entity_category": "diagnostic",
        "register": 7, #0x0007
        "bit": 2,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "outlet_temp",
        "name": "Temperatura powrotu",
        "entity_category": "diagnostic",
        "register": 7, #0x0007
        "bit": 4,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "high_pressure_sensor_failure",
        "name": "Awaria czujnika wysokiego ciśnienia",
        "entity_category": "diagnostic",
        "register": 7, #0x0007
        "bit": 5,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "phase_sequence",
        "name": "Kolejność faz",
        "entity_category": "diagnostic",
        "register": 7, #0x0007
        "bit": 7,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "water_flow_failure",
        "name": "Brak przepływu wody",
        "entity_category": "diagnostic",
        "register": 8, #0x0008
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "high_protection_of_heating_water_outlet",
        "name": "High protection of heating water outlet",
        "entity_category": "diagnostic",
        "register": 8, #0x0008
        "bit": 2,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "outlet_gas_temp_failure",
        "name": " Outlet gas temp. failure",
        "entity_category": "diagnostic",
        "register": 9, #0x0009
        "bit": 6,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "water_inlet_temp_failure",
        "name": " Water inlet temp. failure",
        "entity_category": "diagnostic",
        "register": 10, #0x000A
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "exhaust_temperature_is_too_high",
        "name": "Exhaust temperature is too high",
        "entity_category": "diagnostic",
        "register": 10, #0x000A
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "low_protection_of_cooling_water_outlet",
        "name": "Low protection of cooling water outlet",
        "entity_category": "diagnostic",
        "register": 10, #0x000A
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "inlet_gas_temp_failure",
        "name": "Inlet gas temp. failure",
        "entity_category": "diagnostic",
        "register": 10, #0x000A
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "low_pressure_protection",
        "name": "Zabezpieczenie przed niskim ciśnieniem",
        "entity_category": "diagnostic",
        "register": 11, #0x000B
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "high_pressure_protection",
        "name": "Zabezpieczenie przed wysokim ciśnieniem",
        "entity_category": "diagnostic",
        "register": 11, #0x000B
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "coil_temperature_is_too_high",
        "name": "Temperatura parownika jest zbyt wysoka",
        "entity_category": "diagnostic",
        "register": 11, #0x000B
        "bit": 2,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "high_pressure_sensor_failure",
        "name": "Awaria czujnika wysokiego ciśnienia",
        "entity_category": "diagnostic",
        "register": 11, #0x000B
        "bit": 6,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "low_pressure_sensor_failure",
        "name": "Awaria czujnika niskiego ciśnienia",
        "entity_category": "diagnostic",
        "register": 11, #0x000B
        "bit": 7,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "low_pressure_sensor_failure",
        "name": "Awaria czujnika niskiego ciśnienia",
        "entity_category": "diagnostic",
        "register": 11, #0x000B
        "bit": 7,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "sec_antifreeze",
        "name": "Sec antifreeze",
        "entity_category": "diagnostic",
        "register": 12, #0x000C
        "bit": 4,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "one_antifreeze",
        "name": "One antifreeze",
        "entity_category": "diagnostic",
        "register": 12, #0x000C
        "bit": 5,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
    {
        "unique_id": "ambient_temperature_is_too_low",
        "name": "Zbyt niska temperatura otoczenia",
        "entity_category": "diagnostic",
        "register": 13, #0x000D
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:check-circle",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:check-circle",
            1: "mdi:alert",
        },
    },
]
DATA = BINARY_SENSORS
