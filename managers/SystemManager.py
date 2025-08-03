# pyright: reportMissingParameterType=false
# pyright: reportUnknownParameterType=false
from __future__ import annotations

from random import randbytes
from typing import Literal

from pyecs.common.Types import UUID4
from pyecs.helpers.Statuses import StatusCodes
from pyecs.processing.System import System


class SystemManager(object):
    def __init__(self):
        self.systems: list[System] = []
        self.system_to_id: dict[System, UUID4] = {}
        self.id_to_system: dict[UUID4, System] = {}

    def _unique_id(self) -> UUID4:
        """
        Generate a Version 4 UUID according to RFC 9562 specification.

        UUIDv4 uses 122 random bits with 6 reserved bits for version and variant:
        - Byte 7 (time_hi_and_version): Sets version to 4 by clearing upper 4 bits
            and setting bit 6 (0x40) through (byte & 0x0F) | 0x40
        - Byte 9 (clock_seq_hi_and_reserved): Sets variant to RFC 9562 by clearing
            upper 2 bits and setting bit 7 (0x80) through (byte & 0x3F) | 0x80

        Returns a canonical UUID string in 8-4-4-4-12 format.

        Reference: https://digitalbunker.dev/understanding-how-uuids-are-generated/
        """
        rb: bytearray = bytearray(randbytes(16))

        rb[7] = (rb[7] & 0x0F) | 0x40
        rb[9] = (rb[9] & 0x3F) | 0x80

        return "-".join(
            [rb[:4].hex(), rb[4:6].hex(), rb[6:8].hex(), rb[8:10].hex(), rb[10:16].hex()]
        )

    def register_system(
        self, system: System
    ) -> tuple[Literal[StatusCodes.SYSTEM_REGISTERED], System] | Literal[StatusCodes.FAILURE]:
        """
        Register a new system with the system manager.

        This method assigns a unique UUID to the system and adds it to the
        systems list for execution during world updates.

        Returns a tuple containing SYSTEM_REGISTERED status and the system on success,
        or FAILURE if the system is already registered.
        """
        if system in self.system_to_id:
            return StatusCodes.FAILURE

        system_id: UUID4 = self._unique_id()
        self.systems.append(system)
        self.system_to_id[system] = system_id
        self.id_to_system[system_id] = system

        return (StatusCodes.SYSTEM_REGISTERED, system)

    def unregister_system(
        self, id: UUID4
    ) -> Literal[StatusCodes.SYSTEM_UNREGISTERED, StatusCodes.FAILURE]:
        """
        Remove a system from the system manager by UUID.

        This method removes the specified system from all tracking structures
        and prevents it from being executed during world updates.

        Returns SYSTEM_UNREGISTERED on successful removal, or FAILURE if
        the system ID does not exist.
        """
        if id not in self.id_to_system:
            return StatusCodes.FAILURE

        system: System = self.id_to_system[id]
        self.systems.remove(system)
        del self.system_to_id[system]
        del self.id_to_system[id]

        return StatusCodes.SYSTEM_UNREGISTERED

    def remove_system(
        self, system: System
    ) -> Literal[StatusCodes.SYSTEM_UNREGISTERED, StatusCodes.FAILURE]:
        """
        Remove a system from the system manager by reference.

        This convenience method allows removal using the System object directly
        rather than requiring the UUID. Internally delegates to unregister_system.

        Returns SYSTEM_UNREGISTERED on successful removal, or FAILURE if
        the system is not currently registered.
        """
        if system in self.system_to_id:
            system_id = self.system_to_id[system]
            return self.unregister_system(system_id)
        return StatusCodes.FAILURE

    def update_all(self, world, dt: float) -> None:
        """
        Execute the update method for all registered systems.

        This method calls the update method on each registered system in
        registration order, passing the world instance and delta time.

        Systems are responsible for querying entities and performing their
        specific logic during this update cycle.
        """
        for system in self.systems:
            system.update(world, dt)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
