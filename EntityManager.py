from random import randbytes
from typing import Literal
from helpers.Statuses import StatusCodes

type UUID4 = str

class EntityManager(object):
    def __init__(self):
        self.alive_entities: set[UUID4]

    def unique_id(self) -> UUID4:
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
        rb: bytearray = bytearray(randbytes(128))

        rb[7] = (rb[7] & 0x0F) | 0x40
        rb[9] = (rb[9] & 0x3F) | 0x80

        return '-'.join([
            rb[:4].hex(),
            rb[4:6].hex(),
            rb[6:8].hex(),
            rb[8:10].hex(),
            rb[10:16].hex()
        ])

    def create_entity(self, entity: UUID4) -> tuple[Literal[StatusCodes.ENTITY_CREATED], UUID4] | Literal[StatusCodes.FAILURE]:
        # TODO: Implement entity creation logic
        new_entity: UUID4 = self.unique_id()
        return (StatusCodes.ENTITY_CREATED, new_entity)

    def destroy_entity(self, entity: UUID4) -> Literal[StatusCodes.ENTITY_DESTROYED, StatusCodes.FAILURE]:
        # TODO: Implement entity destroy logic
        return StatusCodes.ENTITY_DESTROYED