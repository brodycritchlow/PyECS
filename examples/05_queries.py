"""
Queries - Powerful entity filtering by component composition.

Queries let you find entities based on which components they have
or don't have.
"""

from dataclasses import dataclass
from typing import Literal

from common.Types import Entity
from core.World import ECSWorld
from helpers.Statuses import StatusCodes
from querying.Query import Query


@dataclass
class Position:
    x: float
    y: float


@dataclass
class Velocity:
    dx: float
    dy: float


@dataclass
class Static:
    """Marker component for non-moving entities."""

    pass


world: ECSWorld = ECSWorld()

player: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()
if player != StatusCodes.FAILURE:
    world.add_component(player, Position(0, 0))
    world.add_component(player, Velocity(1, 0))

wall: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()
if wall != StatusCodes.FAILURE:
    world.add_component(wall, Position(10, 10))
    world.add_component(wall, Static())

moving_query: Query = Query().with_components(Position, Velocity).without_components(Static)
moving_entities: list[Entity] = moving_query.execute(world.component_storage)

print(f"Found {len(moving_entities)} moving entities")
for entity in moving_entities:
    print(f"  Entity {entity[:8]} is moving")
