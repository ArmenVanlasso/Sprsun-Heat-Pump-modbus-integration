import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

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

            # -------------------------
            # HOLDING REGISTERS  (FC=3)
            # -------------------------
            BLOCK_SIZE = 120
            MAX_REGISTER = 400

            for start in range(0, MAX_REGISTER, BLOCK_SIZE):
                count = min(BLOCK_SIZE, MAX_REGISTER - start)
                regs = await self.client.read_holding_registers(start, count)
                if regs is None:
                    raise UpdateFailed(
                        f"Brak danych z read_holding_registers dla bloku {start}"
                    )
                for offset, raw_value in enumerate(regs):
                    reg = start + offset
                    new_data[reg] = raw_value

            # -------------------------
            # COILS  (FC=1)  -> NEW dict
            # -------------------------
            try:
                COIL_BLOCK = 120
                COIL_MAX = 200

                coil_bits = []
                for start in range(0, COIL_MAX, COIL_BLOCK):
                    count = min(COIL_BLOCK, COIL_MAX - start)
                    chunk = await self.client.read_coils(start, count)
                    if chunk:
                        coil_bits.extend(chunk)

                # NEW: map index -> bool
                self.data_coils = {idx: coil_bits[idx] for idx in range(len(coil_bits))}

            except Exception as err:
                _LOGGER.warning("Błąd odczytu coils: %s", err)
                self.data_coils = {}

            # -------------------------
            # DISCRETE INPUTS  (FC=2) – kept for compat
            # -------------------------
            try:
                DISCRETE_BLOCK = 120
                DISCRETE_MAX = 200

                bits = []
                for start in range(0, DISCRETE_MAX, DISCRETE_BLOCK):
                    count = min(DISCRETE_BLOCK, DISCRETE_MAX - start)
                    chunk = await self.client.read_discrete_inputs(start, count)
                    if chunk:
                        bits.extend(chunk)

                self.data_discrete = [[b] for b in bits]

            except Exception as err:
                _LOGGER.warning("Błąd odczytu discrete inputs: %s", err)
                self.data_discrete = None

            # zapisz nowe holdingi do self.data
            self.data = new_data
            self.async_set_updated_data(self.data)
            return self.data

        except Exception as err:
            _LOGGER.error("Błąd aktualizacji danych z Modbus: %s", err)
            raise UpdateFailed(err) from err
