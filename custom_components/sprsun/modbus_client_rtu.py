
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
        self._port = port
        self._slave_id = slave_id
        self._baudrate = baudrate
        self._client: AsyncModbusSerialClient | None = None
        self._lock = asyncio.Lock()

    async def connect(self) -> None:
        """Nawiązanie połączenia RTU."""

        if self._client and getattr(self._client, "connected", False):
            return

        _LOGGER.info(
            "Connecting to Modbus RTU heat-pump %s baud=%s (slave=%s)",
            self._port,
            self._baudrate,
            self._slave_id,
        )

        self._client = AsyncModbusSerialClient(
            port=self._port,
            baudrate=self._baudrate,
            bytesize=8,
            stopbits=2,
            parity="N",
            timeout=5,
        )

        # ID urządzenia przekazujemy bezpośrednio
        # w każdym zapytaniu Modbus przez device_id.

        await self._client.connect()

        if not getattr(self._client, "connected", False):
            raise ConnectionError(f"Cannot connect to RTU {self._port}")

    async def _ensure_connected(self) -> None:
        """Sprawdzenie połączenia i ewentualne ponowne połączenie."""

        if self._client is None or not getattr(self._client, "connected", False):
            await self.connect()

    @staticmethod
    def _response_error(response) -> bool:
        """Sprawdzenie odpowiedzi Modbus."""
        return response is None or (
            hasattr(response, "isError") and response.isError()
        )

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

    async def read_holding_registers(
        self, address: int, count: int = 1
    ) -> list[int] | None:
        """Odczyt rejestrów holding (FC03)."""

        async with self._lock:
            await self._ensure_connected()

            try:
                assert self._client is not None

                rr = await self._client.read_holding_registers(
                    address=address,
                    count=count,
                    device_id=self._slave_id,
                )

                if self._response_error(rr):
                    _LOGGER.error(
                        "Modbus RTU error reading registers at %s: %s",
                        address,
                        rr,
                    )
                    return None

                if not hasattr(rr, "registers"):
                    return None

                return rr.registers

            except ModbusException as err:
                _LOGGER.error("Modbus RTU read error addr %s: %s", address, err)
                return None

            except Exception as err:
                _LOGGER.error(
                    "Unexpected RTU read error addr %s: %s", address, err
                )
                return None

    async def read_discrete_inputs(
        self, address: int, count: int = 1
    ) -> list[bool] | None:
        """Odczyt wejść dyskretnych (FC02)."""

        async with self._lock:
            await self._ensure_connected()

            try:
                assert self._client is not None

                rr = await self._client.read_discrete_inputs(
                    address=address,
                    count=count,
                    device_id=self._slave_id,
                )

                if self._response_error(rr):
                    _LOGGER.error(
                        "Modbus RTU error reading discrete inputs at %s: %s",
                        address,
                        rr,
                    )
                    return None

                if not hasattr(rr, "bits"):
                    return None

                return rr.bits[:count]

            except Exception as err:
                _LOGGER.error(
                    "Modbus RTU read discrete inputs error addr %s: %s",
                    address,
                    err,
                )
                return None

    async def read_coils(
        self, address: int, count: int = 1
    ) -> list[bool] | None:
        """Odczyt cewek (FC01)."""

        async with self._lock:
            await self._ensure_connected()

            try:
                assert self._client is not None

                rr = await self._client.read_coils(
                    address=address,
                    count=count,
                    device_id=self._slave_id,
                )

                if self._response_error(rr):
                    _LOGGER.error(
                        "Modbus RTU error reading coils at %s: %s",
                        address,
                        rr,
                    )
                    return None

                if not hasattr(rr, "bits"):
                    return None

                return rr.bits[:count]

            except Exception as err:
                _LOGGER.error(
                    "Modbus RTU read coils error addr %s: %s",
                    address,
                    err,
                )
                return None

    async def write_register(self, address: int, value: int) -> bool:
        """Zapis pojedynczego rejestru (FC06)."""

        async with self._lock:
            await self._ensure_connected()

            try:
                assert self._client is not None

                rr = await self._client.write_register(
                    address=address,
                    value=value,
                    device_id=self._slave_id,
                )

                if self._response_error(rr):
                    _LOGGER.error(
                        "Modbus RTU write register error %s: %s",
                        address,
                        rr,
                    )
                    return False

                return True

            except Exception as err:
                _LOGGER.error(
                    "Modbus RTU write register %s: %s", address, err
                )
                return False

    async def write_registers(
        self, address: int, values: list[int]
    ) -> bool:
        """Zapis wielu rejestrów (FC10)."""

        async with self._lock:
            await self._ensure_connected()

            try:
                assert self._client is not None

                rr = await self._client.write_registers(
                    address=address,
                    values=values,
                    device_id=self._slave_id,
                )

                if self._response_error(rr):
                    _LOGGER.error(
                        "Modbus RTU write registers error %s: %s",
                        address,
                        rr,
                    )
                    return False

                return True

            except Exception as err:
                _LOGGER.error(
                    "Modbus RTU write registers %s: %s", address, err
                )
                return False

    async def write_coil(self, address: int, value: bool) -> bool:
        """Zapis pojedynczej cewki (FC05)."""

        async with self._lock:
            await self._ensure_connected()

            try:
                assert self._client is not None

                rr = await self._client.write_coil(
                    address=address,
                    value=value,
                    device_id=self._slave_id,
                )

                if self._response_error(rr):
                    _LOGGER.error(
                        "Modbus RTU write coil error %s: %s",
                        address,
                        rr,
                    )
                    return False

                return True

            except Exception as err:
                _LOGGER.error(
                    "Modbus RTU write coil %s: %s", address, err
                )
                return False
