SWITCHES = [
    {
        "name": "Power",
        "unique_id": "power",
        "register": 50, #0x0032
        "bit": 0,
        "icon": "mdi:power",
        "description": "Włącza lub wyłącza pompę ciepła.",
    },
    {
        "name": "Manual Frequency Selection",
        "unique_id": "manual_frequency_selection",
        "register": 50, #0x0032
        "bit": 2,
        "icon": "mdi:tune",
        "description": "Włącza ręczne sterowanie częstotliwością sprężarki...",
        "entity_registry_enabled_default": False,
    },
    {
        "name": "AV Init Outlet STP",
        "unique_id": "av_init_outlet_stp",
        "register": 50, #0x0032
        "bit": 6,
        "icon": "mdi:thermometer-chevron-up",
        "description": "Funkcja powiązana z parametrem B93...",
        "entity_registry_enabled_default": False,
    },
]
DATA = SWITCHES
