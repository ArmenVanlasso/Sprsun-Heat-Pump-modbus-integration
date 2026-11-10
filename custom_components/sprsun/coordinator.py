import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from . const import (
    DOMAIN, 
    DEFAULT_SCAN_INTERVAL, 
    MODEL_PROTOCOLS, 
    PROTOCOL_CUSTOM_BINARY_F4, 
    PROTOCOL_STANDARD_MODBUS
)

_LOGGER = logging.getLogger(__name__)


class SprsunCoordinator(DataUpdateCoordinator):
    """Koordynator odczytów Modbus dla pomp SPRSUN."""

    def __init__(
        self,
        hass: HomeAssistant,
        client,
        entry_id: str,
        model,
        scan_interval: int,
    ) -> None:

        self.hass = hass
        self.client = client
        self.entry_id = entry_id
        self.model = model

        # holding registers: key -> int
        self.data: dict[int, int] = {}

        # coils/discrete inputs: key -> bool  (NEW)
        self.data_coils: dict[int, bool] = {}

        # discrete inputs raw list (kept for backward compatibility)
        self.data_discrete: list[list[bool]] | None = None

        update_interval = timedelta(
            seconds=scan_interval if scan_interval else DEFAULT_SCAN_INTERVAL
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_coordinator_{entry_id}",
            update_interval=update_interval,
        )

    async def _async_update_data(self) -> dict[int, int]:
        """Główny cykl odczytu danych z Modbus."""
        try:
            new_data: dict[int, int] = {}
            protocol_type = MODEL_PROTOCOLS.get(self.model, PROTOCOL_STANDARD_MODBUS)

            # 1. SERIA B (Autorski protokół masowego zrzutu binarnego)
            if protocol_type == PROTOCOL_CUSTOM_BINARY_F4:
                cmd = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x78, 0x45, 0xE8])
                raw_packet = await self.client.read_sprsun_custom_v3l(cmd, expected_length=300)
                
                if raw_packet and len(raw_packet) > 5:
                    payload = raw_packet[3:-2]
                    for i in range(len(payload) // 2):
                        high_byte = payload[i * 2]
                        low_byte = payload[i * 2 + 1]
                        new_data[i] = (high_byte << 8) | low_byte
                        
                    self.data = new_data
                    self.data_coils = {}
                    self.data_discrete = None
                    self.async_set_updated_data(self.data)
                    return self.data
                else:
                    raise UpdateFailed(f"Brak lub uszkodzony pakiet binarny dla modelu z serii B: {self.model}")

            # 2. STARE MODELE (Standardowy protokół Modbus FC=03)
            elif protocol_type == PROTOCOL_STANDARD_MODBUS:
                BLOCK_SIZE = 120
                MAX_REGISTER = 444
                for start in range(0, MAX_REGISTER, BLOCK_SIZE):
                    count = min(BLOCK_SIZE, MAX_REGISTER - start)
                    regs = await self.client.read_holding_registers(start, count)
                    if regs is None:
                        raise UpdateFailed(f"Brak danych z read_holding_registers dla bloku {start}")
                    for offset, raw_value in enumerate(regs):
                        new_data[start + offset] = raw_value

                # COILS oraz DISCRETE INPUTS dla starszych modeli
                if self.model != "nowy_model_sprsun":
                    try:
                        coil_bits = []
                        for start in range(0, 200, 120):
                            chunk = await self.client.read_coils(start, min(120, 200 - start))
                            if chunk: coil_bits.extend(chunk)
                        self.data_coils = {idx: coil_bits[idx] for idx in range(len(coil_bits))}
                    except Exception as err:
                        _LOGGER.warning("Błąd odczytu coils: %s", err)
                        self.data_coils = {}

                    try:
                        bits = []
                        for start in range(0, 200, 120):
                            chunk = await self.client.read_discrete_inputs(start, min(120, 200 - start))
                            if chunk: bits.extend(chunk)
                        self.data_discrete = [[b] for b in bits]
                    except Exception as err:
                        _LOGGER.warning("Błąd odczytu discrete inputs: %s", err)
                        self.data_discrete = None
                else:
                    self.data_coils = {}
                    self.data_discrete = None

                self.data = new_data
                return self.data

        except Exception as err:
            _LOGGER.error("Błąd aktualizacji danych z Modbus: %s", err)
            raise UpdateFailed(err) from err
