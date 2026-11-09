SWITCHES = [
    {
        "name": "Power",
        "register": 0x0032,
        "bit": 0,
        "icon": "mdi:power",
        "description": "Włącza lub wyłącza pompę ciepła.",
    },
    {
        "name": "Manual Frequency Selection",
        "register": 0x0032,
        "bit": 2,
        "icon": "mdi:tune",
        "description": "Włącza ręczne sterowanie częstotliwością sprężarki. Wartość częstotliwości ustawiana jest parametrem Manual Frequency Setting.",
        "entity_registry_enabled_default": False,
    },
    {
        "name": "AV Init Outlet STP",
        "register": 0x0032,
        "bit": 6,
        "icon": "mdi:thermometer-chevron-up",
        "description": "Funkcja powiązana z parametrem B93 (AV init outlet stp). Dokładne działanie nie zostało opisane w dokumentacji producenta.",
        "entity_registry_enabled_default": False,
    },
]
DATA = SWITCHES
