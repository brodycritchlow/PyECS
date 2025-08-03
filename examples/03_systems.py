"""
Systems - Logic processors that operate on entities with specific components.

Systems implement the System protocol and process entities each frame.
"""

from dataclasses import dataclass
from typing import Literal

from common.Types import Component, Entity
from core.World import ECSWorld
from helpers.Statuses import StatusCodes
from querying.Query import Query


@dataclass
class Position:
    x: float
    y: float


class PrintPositionSystem:
    """System that prints positions of all entities."""

    @property
    def required_components(self) -> set[type]:
        return {Position}

    def init(self, world: ECSWorld) -> None:
        print("PrintPositionSystem initialized!")

    def update(self, world: ECSWorld, dt: float) -> None:
        query: Query = Query().with_components(Position)
        entities: list[Entity] = query.execute(world.component_storage)

        for entity in entities:
            pos: Component | Literal[StatusCodes.FAILURE] = world.get_component(entity, Position)
            if isinstance(pos, Position):
                print(f"Entity {entity[:8]} at ({pos.x}, {pos.y})")

    def cleanup(self, world: ECSWorld) -> None:
        print("PrintPositionSystem cleaned up!")


world: ECSWorld = ECSWorld()
world.add_system(PrintPositionSystem())

entity: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()
if entity != StatusCodes.FAILURE:
    world.add_component(entity, Position(5.0, 10.0))

world.update(dt=0.016)
