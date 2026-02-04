import asyncio
import logging

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

_LOGGER = logging.getLogger(__name__)


class HeatPumpModbusClient:
    """Asynchroniczny klient Modbus TCP dla pompy ciepła."""

    def __init__(self, host: str, port: int, unit_id: int):
        self._host = host
        self._port = port
        self._unit_id = unit_id
        self._client: AsyncModbusTcpClient | None = None
        self._lock = asyncio.Lock()

    async def connect(self):
        """Połączenie z urządzeniem, jeśli jeszcze nie jest połączone."""
        if self._client is not None and getattr(self._client, "connected", False):
            return

        _LOGGER.info(
            "Connecting to Modbus heat pump %s:%s (unit_id=%s)",
            self._host,
            self._port,
            self._unit_id,
        )
        self._client = AsyncModbusTcpClient(
            host=self._host,
            port=self._port,
            timeout=5,
        )

        # Ustaw unit/slave na kliencie (różne wersje pymodbus)
        if hasattr(self._client, "unit_id"):
            self._client.unit_id = self._unit_id
        elif hasattr(self._client, "unit"):
            self._client.unit = self._unit_id
        elif hasattr(self._client, "slave"):
            self._client.slave = self._unit_id

        await self._client.connect()
        if not getattr(self._client, "connected", False):
            raise ConnectionError("Cannot connect to Modbus heat pump")

    async def close(self):
        """Zamyka połączenie."""
        if self._client is not None:
            await self._client.close()
            self._client = None

    async def read_holding_registers(self, address: int, count: int = 1) -> list[int] | None:
        """Odczyt rejestrów holding."""
        async with self._lock:
            if self._client is None or not getattr(self._client, "connected", False):
                await self.connect()

            try:
                rr = await self._client.read_holding_registers(
                    address=address,
                    count=count,
                )
            except ModbusException as err:
                _LOGGER.error("Modbus error reading address %s: %s", address, err)
                return None
            except Exception as err:
                _LOGGER.error("Unexpected error reading address %s: %s", address, err)
                return None

            if hasattr(rr, "isError") and rr.isError():
                _LOGGER.error("Modbus error response at address %s: %s", address, rr)
                return None

            if rr is None or not hasattr(rr, "registers"):
                _LOGGER.error("Invalid Modbus response at address %s: %s", address, rr)
                return None

            return rr.registers

    async def read_all_registers(self) -> dict[int, int | None]:
        """Czyta wszystkie rejestry wymagane przez integrację."""
        from .const import ALL_REGISTERS  # lokalny import, żeby uniknąć cyklu

        results: dict[int, int | None] = {}

        for reg in ALL_REGISTERS:
            regs = await self.read_holding_registers(reg, 1)
            if regs is None or len(regs) == 0:
                results[reg] = None
            else:
                results[reg] = regs[0]

        return results
