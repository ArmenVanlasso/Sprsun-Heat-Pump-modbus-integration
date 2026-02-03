DOMAIN = "sprsun"

CONF_HOST = "host"
CONF_PORT = "port"
CONF_UNIT_ID = "unit_id"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_HOST = "192.168.10.66"
DEFAULT_PORT = 502
DEFAULT_UNIT_ID = 1
DEFAULT_SCAN_INTERVAL = 30  # sekundy

# index 188, modbus_address 40189 -> offset 188 (0-based)
# w Node-RED był to INT16 z mnożnikiem 0.1 (nie REAL)
REG_RETURN_TEMP = 188

PLATFORMS: list[str] = ["sensor"]
