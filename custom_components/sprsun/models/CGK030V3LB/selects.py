SELECTS = [
    {
        "name": "Tryb pracy pompy",
        "register": 55,  # 0x0036 + 1
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
        "register": 401,  # 0x0190 + 1
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
        "register": 415,  # 0x019E + 1
        "options": {
            0: "Interwał",
            1: "Normal",
            2: "Na żądanie",
        },
        "icon": "mdi:pump",
    },
    {
        "name": "Tryb MV",
        "register": 51,  # 0x0032 + 1
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
        "register": 51,  # 0x0032 + 1
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
        "register": 391,  # 0x0186 + 1
        "options": {
            0: "Manual",
            1: "Auto",
        },
        "icon": "mdi:pump",
        "entity_registry_enabled_default": False,
    },
]

DATA = SELECTS
