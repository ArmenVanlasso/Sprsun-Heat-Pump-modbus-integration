BINARY_SENSORS = [
    {
        "unique_id": "ac_linkage_switch",
        "name": "A/C linkage switch",
        "register": 3,
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "linkage_switch",
        "name": "Linkage switch",
        "register": 3,
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "heating_linkage",
        "name": "Heating linkage",
        "register": 3,
        "bit": 2,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "cooling_linkage",
        "name": "Cooling linkage",
        "register": 3,
        "bit": 3,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "flow_switch",
        "name": "Flow switch",
        "register": 3,
        "bit": 4,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "flow_switch",
        "name": "Czujnik przepływu",
        "register": 3,
        "bit": 5,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
{ 
  unique_id : phase_sequence_detection , 
  name : Kolejność faz , 
  register : 3, 
  bit : 6, 
  source : holding_register , 
  device_class: problem,
  icon_map : { 
    0: mdi:check-circle , 
    1: mdi:alert-circle , 
  }, 
}
    {
        "unique_id": "hotwater_demand",
        "name": "Hotwater demand",
        "register": 4,
        "bit": 0,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "heating_demand",
        "name": "Heating demand",
        "register": 4,
        "bit": 1,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "with_or_without_heating",
        "name": " With or without heating",
        "register": 4,
        "bit": 2,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "with_or_without_cooling",
        "name": "With or without cooling",
        "register": 4,
        "bit": 3,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "antilegionella_on",
        "name": "Antilegionella on",
        "register": 4,
        "bit": 4,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "cooling_demand",
        "name": "Cooling demand",
        "register": 4,
        "bit": 5,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "alarm_downtime",
        "name": "Alarm downtime",
        "register": 4,
        "bit": 6,
        "source": "holding_register",
        "icon": "mdi:valve-open",
        "mapping": {
            0: "off",
            1: "on",
        },
        "icon_map": {
            0: "mdi:valve-closed",,
            1: "mdi:valve-open",
        },
    },
    {
        "unique_id": "defrost",
        "name": "Defrost",
        "register": 4,
        "bit": 7,
        "source": "holding_register",
        "icon": ""mdi:snowflake-off",
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
        "unique_id": "sprezarka",
        "name": "Sprężarka",
        "register": 5,
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
        "unique_id": "wentylator",
        "name": "Wentylator",
        "register": 5,
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
        "unique_id": "zawor_4_drogowy",
        "name": "Zawór 4 drogowy",
        "register": 5,
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
        "unique_id": "wysoka_lub_niska_predkosc_wentylatora",
        "name": "Wysoka lub niska prędkość wentylatora",
        "register": 5,
        "bit": 7,
        "source": "holding_register",
        "icon": "mdi:fan",
        "mapping": {
            0: "low",
            1: "high",
    },
    {
        "unique_id": "grzalka_obudowy",
        "name": "Grzałka obudowy",
        "register": 6,
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
        "register": 6,
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
        "unique_id": "zawor_3_drogowy",
        "name": "Zawór 3 drogowy",
        "register": 6,
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
        "register": 6,
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
        "name": "AC pump",
        "register": 7,
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
        "unique_id": "grzalka_karteru_sprezarki",
        "name": "Grzałka karteru sprężarki",
        "register": 7,
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
        "register": 7,
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
        "register": 7,
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
        "unique_id": "pump",
        "name": "Pump",
        "register": 7,
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


]
DATA = BINARY_SENSORS
