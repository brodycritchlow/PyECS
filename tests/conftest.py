import os

os.environ["BEARTYPE_DISABLE"] = "1"

from dataclasses import dataclass

import pytest

from pyecs import ECSWorld


@dataclass
class Position:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class Velocity:
    dx: float = 0.0
    dy: float = 0.0
    dz: float = 0.0


@dataclass
class Health:
    current: int = 100
    max: int = 100


@dataclass
class Name:
    value: str = "Entity"


@pytest.fixture
def world():
    return ECSWorld()


@pytest.fixture
def components():
    return {"Position": Position, "Velocity": Velocity, "Health": Health, "Name": Name}


@pytest.fixture
def entity_with_components(world):
    entity = world.create_entity()
    if entity == -1:  # StatusCodes.FAILURE
        raise ValueError("Failed to create entity")
    world.add_component(entity, Position(1.0, 2.0, 3.0))
    world.add_component(entity, Velocity(0.1, 0.2, 0.3))
    world.add_component(entity, Health(75, 100))
    return entity
