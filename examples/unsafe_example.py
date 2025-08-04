#!/usr/bin/env python3
"""Example showing safe vs unsafe method usage in PyECS."""

from dataclasses import dataclass

from pyecs import ECSWorld, StatusCodes
from pyecs.common.Types import Entity
from pyecs.exceptions import ComponentNotFoundError, EntityNotFoundError


@dataclass
class Position:
    x: float
    y: float


@dataclass
class Velocity:
    dx: float
    dy: float


def safe_example(world: ECSWorld, entity: Entity) -> None:
    """Example using safe methods that return StatusCodes.FAILURE."""
    print("=== Safe Example ===")

    # Safe get_component
    position = world.get_component(entity, Position)
    if position == StatusCodes.FAILURE:
        print("Position component not found")
    else:
        print(f"Position: x={position.x}, y={position.y}")

    # Safe get_components
    components = world.get_components(entity, Position, Velocity)
    if components == StatusCodes.FAILURE:
        print("One or more components not found")
    else:
        pos, vel = components
        print(f"Position: {pos}, Velocity: {vel}")


def unsafe_example(world: ECSWorld, entity: Entity) -> None:
    """Example using unsafe methods that raise exceptions."""
    print("\n=== Unsafe Example ===")

    try:
        # Unsafe get_component - raises exception if not found
        position = world.get_component_unsafe(entity, Position)
        print(f"Position: x={position.x}, y={position.y}")
    except ComponentNotFoundError as e:
        print(f"Error: {e}")

    try:
        # Unsafe get_components - raises exception if any component not found
        pos, vel = world.get_components_unsafe(entity, Position, Velocity)
        print(f"Position: {pos}, Velocity: {vel}")
    except ComponentNotFoundError as e:
        print(f"Error: {e}")


def main():
    world = ECSWorld()

    # Create entity with only Position
    entity = world.create_entity()
    world.add_component(entity, Position(10.0, 20.0))

    # Try both safe and unsafe approaches
    safe_example(world, entity)
    unsafe_example(world, entity)

    # Example with unsafe entity creation
    print("\n=== Unsafe Entity Creation ===")
    try:
        # This will work
        entity2 = world.create_entity_unsafe()
        print(f"Created entity: {entity2}")
    except EntityNotFoundError as e:
        print(f"Failed to create entity: {e}")


if __name__ == "__main__":
    main()
