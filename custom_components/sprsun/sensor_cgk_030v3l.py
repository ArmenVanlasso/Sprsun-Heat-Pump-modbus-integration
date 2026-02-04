# custom_components/sprsun/sensor_cgk_030v3l.py
import logging

from .const import *  # REG_...

_LOGGER = logging.getLogger(__name__)


def _sensor_definitions_cgk_030v3l():
    sensors = []

    for name, value in globals().items():
        if not name.startswith("REG_"):
            continue

        register = value
        clean_name = name.replace("REG_", "")
        clean_name = clean_name.lower()

        unique_id = f"cgk_030v3l_{clean_name}"
        friendly = clean_name.replace("_", " ").capitalize()

        unit = None
        device_class = None
        icon = "mdi:checkbox-blank-circle-outline"
        scale = 1
        signed = False
        state_class = None

        # --- SPECJALNE SENSORY ---

        if clean_name == "temperatura_powrotu":
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        elif clean_name == "przegrzanie":
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        elif clean_name == "zawor_eev":
            friendly = "Zawór rozprężny"
            icon = "mdi:valve"
            unit = "steps"
            scale = 1
            signed = False

        elif clean_name == "napiecie_falownika":
            unit = "V"
            device_class = "voltage"
            icon = "mdi:flash"
            scale = 1
            signed = False
            state_class = "measurement"

        elif clean_name == "prad_falownika":
            unit = "A"
            device_class = "current"
            icon = "mdi:current-ac"
            scale = 0.1
            signed = False

        elif clean_name == "moc_pobierana":
            unit = "W"
            device_class = "power"
            icon = "mdi:flash"
            scale = 1
            signed = False
            state_class = "measurement"

        elif clean_name == "status":
            unit = None
            device_class = None
            icon = "mdi:information"
            scale = 1
            signed = False

        elif clean_name == "status_2":
            friendly = "Status 2"
            unit = None
            device_class = None
            icon = "mdi:information"
            scale = 1
            signed = False

        # --- automatyczne temperatury ---
        elif "temperatura" in clean_name:
            unit = "°C"
            device_class = "temperature"
            icon = "mdi:thermometer"
            scale = 0.1
            signed = True

        sensors.append(
            {
                "unique_id": unique_id,
                "name": friendly,
                "register": register,
                "unit": unit,
                "device_class": device_class,
                "icon": icon,
                "scale": scale,
                "signed": signed,
                "state_class": state_class,
            }
        )

    return sensors


SENSORS_CGK_030V3L = _sensor_definitions_cgk_030v3l()
