"""
Components - Pure data containers attached to entities.

Components are just regular Python objects (dataclasses work great)
that hold data without logic.
"""

from dataclasses import dataclass
from typing import Literal

from common.Types import Component, Entity
from core.World import ECSWorld
from helpers.Statuses import StatusCodes


@dataclass
class Position:
    x: float
    y: float


@dataclass
class Name:
    value: str


world = ECSWorld()
player: Entity | Literal[StatusCodes.FAILURE] = world.create_entity()

if player != StatusCodes.FAILURE:
    world.add_component(player, Position(10.0, 20.0))
    world.add_component(player, Name("Hero"))

    pos: Component | Literal[StatusCodes.FAILURE] = world.get_component(player, Position)
    name: Component | Literal[StatusCodes.FAILURE] = world.get_component(player, Name)

    if isinstance(pos, Position) and isinstance(name, Name):
        print(f"Player '{name.value}' is at position ({pos.x}, {pos.y})")
