"""TCP Modbus klient dla pomp Sprsun."""
from __future__ import annotations

import asyncio
import logging

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException

_LOGGER = logging.getLogger(__name__)


class HeatPumpModbusTcpClient:
    """Klient Modbus TCP – zero zmian w logice."""

    def __init__(self, host: str, port: int, unit_id: int) -> None:
        self._host       = host
        self._port       = port
        self._unit_id    = unit_id
        self._client: AsyncModbusTcpClient | None = None
        self._lock       = asyncio.Lock()

    # ------------------------------------------------------------------
    async def connect(self) -> None:
        if self._client and getattr(self._client, "connected", False):
            return

        _LOGGER.info("Connecting to Modbus TCP heat-pump %s:%s (unit_id=%s)",
                     self._host, self._port, self._unit_id)
        self._client = AsyncModbusTcpClient(
            host=self._host, port=self._port, timeout=5,
        )
        # każda wersja pymodbus może mieć inny sposób ustawiania unit_id
        if hasattr(self._client, "unit_id"):
            self._client.unit_id = self._unit_id
        elif hasattr(self._client, "unit"):
            self._client.unit = self._unit_id
        elif hasattr(self._client, "slave"):
            self._client.slave = self._unit_id

        await self._client.connect()
        if not getattr(self._client, "connected", False):
            raise ConnectionError("Cannot connect to Modbus heat-pump")

    async def close(self) -> None:
        """Pewne zamknięcie połączenia TCP."""
        if self._client is None:
            return
        try:
            if hasattr(self._client, "protocol") and hasattr(self._client.protocol, "transport"):
                transport = self._client.protocol.transport
                if transport is not None:
                    transport.close()

            close_method = getattr(self._client, "close", None)
            if callable(close_method):
                result = close_method()
                if hasattr(result, "__await__"):
                    await result
        except Exception as err:
            _LOGGER.warning("Błąd przy zamykaniu Modbus TCP: %s", err)
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
                _LOGGER.error("Modbus TCP read error addr %s: %s", address, err)
                return None
            except Exception as err:
                _LOGGER.error("Unexpected TCP read error addr %s: %s", address, err)
                return None

            if rr and hasattr(rr, "isError") and rr.isError():
                _LOGGER.error("Modbus TCP error response addr %s: %s", address, rr)
                return None
            if rr is None or not hasattr(rr, "registers"):
                return None
            return rr.registers

    # ------------------------------------------------------------------
    async def read_discrete_inputs(self, address: int, count: int = 1) -> list[bool] | None:
        async with self._lock:
            if self._client is None or not getattr(self._client, "connected", False):
                await self.connect()
            try:
                rr = await self._client.read_discrete_inputs(address=address, count=count)
            except ModbusException as err:
                _LOGGER.error("Modbus TCP read DI error addr %s: %s", address, err)
                return None
            except Exception as err:
                _LOGGER.error("Unexpected TCP read DI error addr %s: %s", address, err)
                return None

            if rr and hasattr(rr, "isError") and rr.isError():
                _LOGGER.error("Modbus TCP DI error addr %s: %s", address, rr)
                return None
            if rr is None or not hasattr(rr, "bits"):
                return None
            return rr.bits

    async def read_coils(self, address: int, count: int = 1) -> list[bool] | None:
        async with self._lock:
            if self._client is None or not getattr(self._client, "connected", False):
                await self.connect()
            try:
                rr = await self._client.read_coils(address=address, count=count)
            except ModbusException as err:
                _LOGGER.error("Modbus TCP read coils error addr %s: %s", address, err)
                return None
            except Exception as err:
                _LOGGER.error("Unexpected TCP read coils error addr %s: %s", address, err)
                return None

            if rr and hasattr(rr, "isError") and rr.isError():
                _LOGGER.error("Modbus TCP coils error addr %s: %s", address, rr)
                return None
            if rr is None or not hasattr(rr, "bits"):
                return None
            return rr.bits[:count]

    async def write_register(self, address: int, value: int) -> bool:
        async with self._lock:
            if self._client is None or not getattr(self._client, "connected", False):
                await self.connect()
            try:
                rr = await self._client.write_register(address=address, value=value)
            except Exception as err:
                _LOGGER.error("Modbus TCP write register %s: %s", address, err)
                return False

            if rr and hasattr(rr, "isError") and rr.isError():
                _LOGGER.error("Modbus TCP write register error %s: %s", address, rr)
                return False
            return True

    async def write_registers(self, address: int, values: list[int]) -> bool:
        async with self._lock:
            if self._client is None or not getattr(self._client, "connected", False):
                await self.connect()
            try:
                rr = await self._client.write_registers(
                    address=address, values=values
                )
            except Exception as err:
                _LOGGER.error("Modbus TCP write registers %s: %s", address, err)
                return False

            if rr and hasattr(rr, "isError") and rr.isError():
                _LOGGER.error("Modbus TCP write registers error %s: %s", address, rr)
                return False
            return True

    async def write_coil(self, address: int, value: bool) -> bool:
        async with self._lock:
            if self._client is None or not getattr(self._client, "connected", False):
                await self.connect()
            try:
                rr = await self._client.write_coil(address=address, value=value)
            except Exception as err:
                _LOGGER.error("Modbus TCP write coil %s: %s", address, err)
                return False

            if rr and hasattr(rr, "isError") and rr.isError():
                _LOGGER.error("Modbus TCP write coil error %s: %s", address, rr)
                return False
            return True
