"""
World - The main facade that coordinates all ECS operations.

The World manages entities, components, systems, and provides
a clean API for all ECS operations.
"""

from dataclasses import dataclass
from typing import Literal

from common.Types import Component, Entity
from core.World import ECSWorld
from helpers.Statuses import StatusCodes


@dataclass
class Health:
    current: int
    max: int


world: ECSWorld = ECSWorld()

player: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()
monster: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()

if player != StatusCodes.FAILURE:
    world.add_component(player, Health(100, 100))
    player_health: Component | Literal[StatusCodes.FAILURE] = world.get_component(player, Health)
    if isinstance(player_health, Health):
        print(f"Player health: {player_health.current}/{player_health.max}")

if monster != StatusCodes.FAILURE:
    world.add_component(monster, Health(50, 50))
    world.destroy_entity(monster)
    print(f"Monster still exists? {world.entity_manager.is_alive(monster)}")
