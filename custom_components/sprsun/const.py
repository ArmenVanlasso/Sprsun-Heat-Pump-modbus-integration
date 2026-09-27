# flake8: noqa
DOMAIN = "sprsun"

# --- nazwy głównych opcji ---------------------------------
CONF_HOST            = "host"
CONF_PORT            = "port"
CONF_UNIT_ID         = "unit_id"
CONF_SCAN_INTERVAL   = "scan_interval"
CONF_MODEL           = "model"

# --- rodzaj połączenia TCP / RTU -------------------------
CONF_CONNECTION_TYPE = "connection_type"
CONF_SERIAL_PORT     = "serial_port"
CONF_BAUDRATE        = "baudrate"
# --- Ustawienie początkowe czasów pracy sprężarki i wentylatora
CONF_INITIAL_HOURS = "initial_hours"
CONF_SET_FAN_HOURS = "set_fan_hours"
CONF_FAN_HOURS = "fan_hours"
CONF_SET_COMPRESSOR_HOURS = "set_compressor_hours"
CONF_COMPRESSOR_HOURS = "compressor_hours"
# --- język integracji ------------------------------------
CONF_LANGUAGE        = "language"

# --- wartości domyślne -----------------------------------
DEFAULT_PORT            = 502
DEFAULT_UNIT_ID         = 1
DEFAULT_SCAN_INTERVAL   = 30
DEFAULT_BAUDRATE        = 19200
DEFAULT_SERIAL_PORT     = "/dev/ttyUSB0"
DEFAULT_LANGUAGE        = "EN"

CONNECTION_TYPE_TCP = "tcp"
CONNECTION_TYPE_RTU = "rtu"

BAUDRATES = [9600, 19200, 38400, 57600, 115200]

# --- język integracji ------------------------------------
LANGUAGES = {
    "العربية": "ar",
    "Azərbaycan dili": "az",
    "Български": "bg",
    "বাংলা": "bn",
    "Català": "ca",
    "Čeština": "cs",
    "Dansk": "da",
    "Deutsch": "de",
    "Ελληνικά": "el",
    "English": "en",
    "Esperanto": "eo",
    "Español": "es",
    "Euskara": "eu",
    "Suomi": "fi",
    "Français": "fr",
    "Français (Canada)": "fr-CA",
    "Gaeilge": "ga",
    "עברית": "he",
    "हिन्दी": "hi",
    "Hrvatski": "hr",
    "Kreyòl Ayisyen": "ht",
    "Magyar": "hu",
    "Bahasa Indonesia": "id",
    "Italiano": "it",
    "日本語": "ja",
    "한국어": "ko",
    "Latina": "la",
    "Lietuvių": "lt",
    "Latviešu": "lv",
    "Norsk Bokmål": "nb",
    "Nederlands": "nl",
    "Polski": "pl",
    "Português": "pt",
    "Português (Brasil)": "pt-BR",
    "Română": "ro",
    "Русский": "ru",
    "Shqip": "sq",
    "Српски": "sr",
    "Svenska": "sv",
    "Kiswahili": "sw",
    "ไทย": "th",
    "Tagalog": "tl",
    "Türkçe": "tr",
    "Українська": "uk",
    "اردو": "ur",
    "Tiếng Việt": "vi",
    "ייִדיש": "yi",
    "简体中文": "zh_Hans",
    "isiZulu": "zu"
}

# --- dostępne modele -------------------------------------
MODELS = {
    "CGK-025V3L":   "cgk_025v3l",
    "CGK-025V3L-B": "cgk_025v3l_b",
    "CGK-030V3L":   "cgk_030v3l",
    "CGK-040V3L":   "cgk_040v3l",
    "CGK-050V3L":   "cgk_050v3l",
    "CGK-060V3L":   "cgk_060v3l",
}

# --- które platformy integracji będą ładowane ----------
PLATFORMS = [
    "sensor",
    "binary_sensor",
    "number",
    "switch",
    "select",
    "climate",
    "button"
]
