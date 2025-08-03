"""
Archetypes - Automatic grouping of entities by component composition.

Entities with the same set of components are stored together in
archetypes for cache-efficient access.
"""

from dataclasses import dataclass
from typing import Literal

from common.Types import Entity
from core.World import ECSWorld
from helpers.Statuses import StatusCodes


@dataclass
class Position:
    x: float
    y: float


@dataclass
class Velocity:
    dx: float
    dy: float


world: ECSWorld = ECSWorld()

enemy1: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()
if enemy1 != StatusCodes.FAILURE:
    world.add_component(enemy1, Position(0, 0))
    world.add_component(enemy1, Velocity(1, 0))

enemy2: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()
if enemy2 != StatusCodes.FAILURE:
    world.add_component(enemy2, Position(10, 0))
    world.add_component(enemy2, Velocity(-1, 0))

wall: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()
if wall != StatusCodes.FAILURE:
    world.add_component(wall, Position(5, 5))

print("Archetype groupings:")
for mask, archetype in world.component_storage.archetypes.items():
    components = [t.__name__ for t in mask]
    entity_count = len(archetype.entities)
    print(f"  {components}: {entity_count} entities")

if wall != StatusCodes.FAILURE:
    print("\nAdding Velocity to wall...")
    world.add_component(wall, Velocity(0, 0))

print("\nArchetype groupings after change:")
for mask, archetype in world.component_storage.archetypes.items():
    components: list[str] = [t.__name__ for t in mask]
    entity_count: int = len(archetype.entities)
    print(f"  {components}: {entity_count} entities")
