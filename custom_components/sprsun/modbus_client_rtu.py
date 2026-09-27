"""RTU Modbus klient dla pomp Sprsun."""
from __future__ import annotations

import asyncio
import logging

from pymodbus.client import AsyncModbusSerialClient
from pymodbus.exceptions import ModbusException

_LOGGER = logging.getLogger(__name__)


class HeatPumpModbusRtuClient:
    """Klient Modbus RTU (RS485)."""

    def __init__(self, port: str, slave_id: int, baudrate: int = 19200) -> None:
        self._port      = port
        self._slave_id  = slave_id
        self._baudrate  = baudrate
        self._client: AsyncModbusSerialClient | None = None
        self._lock      = asyncio.Lock()

    # ------------------------------------------------------------------
    async def connect(self) -> None:
        if self._client and getattr(self._client, "connected", False):
            return

        _LOGGER.info("Connecting to Modbus RTU heat-pump %s baud=%s (slave=%s)",
                     self._port, self._baudrate, self._slave_id)
        self._client = AsyncModbusSerialClient(
            port=self._port,
            baudrate=self._baudrate,
            bytesize=8,
            stopbits=2,
            parity='N',
            timeout=5,
        )
        if hasattr(self._client, "slave"):
            self._client.slave = self._slave_id

        await self._client.connect()
        if not getattr(self._client, "connected", False):
            raise ConnectionError(f"Cannot connect to RTU {self._port}")

    async def close(self) -> None:
        """Zamknięcie portu szeregowego."""
        if self._client is None:
            return

        try:
            transport = getattr(self._client, "transport", None)
            if transport is not None:
                transport.close()

            close_method = getattr(self._client, "close", None)
            if callable(close_method):
                result = close_method()
                if hasattr(result, "__await__"):
                    await result
        except Exception as exc:
            _LOGGER.warning("Błąd przy zamykaniu Modbus RTU: %s", exc)
        finally:
            self._client = None

    # ------------------------------------------------------------------
    async def read_holding_registers(self, address: int, count: int = 1) -> list[int] | None:
        async with self._lock:
            if self._client is None or not getattr(self._client, "connected", False):
                await self.connect()
            try:
                rr = await self._client.read_holding_registers(address=address, count=count)
            except ModbusException as err:
                _LOGGER.error("Modbus RTU read error addr %s: %s", address, err)
                return None
            except Exception as err:
                _LOGGER.error("Unexpected RTU read error addr %s: %s", address, err)
                return None

            if rr and hasattr(rr, "isError") and rr.isError():
                _LOGGER.error("Modbus RTU error response addr %s: %s", address, rr)
                return None
            if rr is None or not hasattr(rr, "registers"):
                return None
            return rr.registers

    async def read_discrete_inputs(self, address: int, count: int = 1) -> list[bool] | None:
        ...  # dokładnie jak wyżej – zmień tylko "RTU" w logach
    async def read_coils(self, address: int, count: int = 1) -> list[bool] | None:
        ...  # kopiej / wklej analogicznie
    async def write_register(self, address: int, value: int) -> bool:
        ...  # kopiej / wklej analogicznie
    async def write_registers(self, address: int, values: list[int]) -> bool:
        ...  # analogicznie
    async def write_coil(self, address: int, value: bool) -> bool:
        ...  # analogicznie
