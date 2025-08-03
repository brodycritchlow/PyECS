"""
Entities - Unique identifiers for game objects.

Entities are just UUIDs that act as handles to reference
collections of components.
"""

from typing import Literal

from pyecs.common.Types import Entity
from pyecs.core.World import ECSWorld
from pyecs.helpers.Statuses import StatusCodes

world = ECSWorld()

player: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()
enemy: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()
item: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()

if player != StatusCodes.FAILURE:
    print(f"Player ID: {player}")
    print(f"\nIs player alive? {world.entity_manager.is_alive(player)}")

if enemy != StatusCodes.FAILURE:
    print(f"Enemy ID: {enemy}")
    world.destroy_entity(enemy)
    print(f"Is enemy alive after destruction? {world.entity_manager.is_alive(enemy)}")

if item != StatusCodes.FAILURE:
    print(f"Item ID: {item}")
