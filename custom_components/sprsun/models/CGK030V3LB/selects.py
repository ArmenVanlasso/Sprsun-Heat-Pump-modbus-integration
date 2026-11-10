SELECTS = [
    {
        "name": "Tryb pracy pompy",
        "unique_id": "p06_unit_mode",
        "register": 54,  # 0x0036
        "options": {
            0: "CWU",
            1: "Ogrzewanie",
            2: "Chłodzenie",
            3: "Ogrzewanie + CWU",
            4: "Chłodzenie + CWU",
        },
        "icon": "mdi:heat-pump",
    },
    {
        "name": "Tryb sprężarki",
        "unique_id": "f23_compressor_mode",
        "register": 400,  # 0x0190
        "options": {
            0: "Normal",
            1: "ECO",
            2: "Noc",
            3: "Test",
        },
        "icon": "mdi:air-conditioner",
    },
    {
        "name": "Tryb pracy pompy obiegowej",
        "unique_id": "g02_pump_work",
        "register": 414,  # 0x019E
        "options": {
            0: "Interwał",
            1: "Normal",
            2: "Na żądanie",
        },
        "icon": "mdi:pump",
    },
    {
        "name": "Tryb MV",
        "unique_id": "mv_mode",
        "register": 50,  # 0x0032
        "bit": 1,
        "options": {
            0: "Auto",
            1: "Manual",
        },
        "icon": "mdi:cog",
        "entity_registry_enabled_default": False,
    },
    {
        "name": "Tryb AV",
        "unique_id": "av_mode",
        "register": 50,  # 0x0032
        "bit": 5,
        "options": {
            0: "Auto",
            1: "Manual",
        },
        "icon": "mdi:cog",
        "entity_registry_enabled_default": False,
    },
    {
        "name": "Tryb pompy DC",
        "unique_id": "f13_dc_pump_mode",
        "register": 390,  # 0x0186
        "options": {
            0: "Manual",
            1: "Auto",
        },
        "icon": "mdi:pump",
        "entity_registry_enabled_default": False,
    },
]

DATA = SELECTS
