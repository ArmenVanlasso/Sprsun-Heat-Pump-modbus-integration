DOMAIN = "sprsun"

# Pola konfiguracyjne
CONF_HOST = "host"
CONF_PORT = "port"
CONF_UNIT_ID = "unit_id"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_MODEL = "model"

# Domyślne wartości (bez domyślnego hosta — użytkownik wpisuje ręcznie)
DEFAULT_PORT = 502
DEFAULT_UNIT_ID = 1
DEFAULT_SCAN_INTERVAL = 30  # sekundy

# Lista modeli dostępnych w config_flow
MODELS = {
    "CGK-025V3L": "cgk_025v3l",
    "CGK-030V3L": "cgk_030v3l",
    "CGK-040V3L": "cgk_040v3l",
    "CGK-050V3L": "cgk_050v3l",
    "CGK-060V3L": "cgk_060v3l",
}

# Twój jeden sensor (wspólny dla wszystkich modeli)
# index 188, modbus_address 40189 -> offset 188 (0-based)
REG_RETURN_TEMP = 188

# Platformy obsługiwane przez integrację
PLATFORMS: list[str] = ["sensor"]
