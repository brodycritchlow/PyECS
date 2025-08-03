import threading
from random import randbytes
from typing import Literal

from common.Types import UUID4, Entity
from helpers.Statuses import StatusCodes


class EntityManager(object):
    def __init__(self):
        self.alive_entities: set[UUID4] = set()
        self._lock: threading.Lock = threading.Lock()

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

        return '-'.join([
            rb[:4].hex(),
            rb[4:6].hex(),
            rb[6:8].hex(),
            rb[8:10].hex(),
            rb[10:16].hex()
        ])

    def create_entity(self) -> tuple[Literal[StatusCodes.ENTITY_CREATED], Entity] | Literal[StatusCodes.FAILURE]:
        """
        Create a new entity in the entity component system.

        This method generates a unique UUID4 identifier for the entity and registers it
        in the alive_entities set.

        Returns a tuple containing ENTITY_CREATED status and the new entity UUID on success.
        FAILURE is typed for future expansion purposes only; currently cannot be returned.
        """

        with self._lock:
            new_entity: UUID4 = self._unique_id()

            self.alive_entities.add(new_entity)

            return (StatusCodes.ENTITY_CREATED, new_entity)

    def destroy_entity(self, entity: Entity) -> Literal[StatusCodes.ENTITY_DESTROYED, StatusCodes.FAILURE]:
        """
        Remove an entity from the entity component system.

        This method removes the specified entity UUID from the alive_entities set and
        triggers cleanup of all associated components. The entity becomes invalid after
        this operation and should not be used in subsequent operations.

        Returns ENTITY_DESTROYED status on successful removal, or FAILURE status if
        the entity does not exist or destruction fails.
        """

        with self._lock:
            if entity not in self.alive_entities:
                return StatusCodes.FAILURE

            self.alive_entities.remove(entity)
            return StatusCodes.ENTITY_DESTROYED

    def is_alive(self, entity: Entity) -> bool:
        with self._lock:
            return entity in self.alive_entities
