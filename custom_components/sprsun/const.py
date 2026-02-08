DOMAIN = "sprsun"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_UNIT_ID = "unit_id"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_MODEL = "model"

DEFAULT_PORT = 502
DEFAULT_UNIT_ID = 1
DEFAULT_SCAN_INTERVAL = 30

MODELS = {
    "CGK-025V3L": "cgk_025v3l",
    "CGK-030V3L": "cgk_030v3l",
    "CGK-040V3L": "cgk_040v3l",
    "CGK-050V3L": "cgk_050v3l",
    "CGK-060V3L": "cgk_060v3l",
}

PLATFORMS = ["sensor", "binary_sensor", "number"]
