import pytest

from pyecs import StatusCodes
from pyecs.exceptions import ComponentNotFoundError

from .conftest import Health, Position, Velocity


class TestWorldEntityManagement:
    def test_create_entity(self, world):
        entity = world.create_entity()
        assert entity != StatusCodes.FAILURE
        assert world.entity_manager.is_alive(entity)

    def test_destroy_entity(self, world):
        entity = world.create_entity()
        world.destroy_entity(entity)
        assert not world.entity_manager.is_alive(entity)

    def test_destroy_entity_removes_components(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position(1, 2, 3))
        world.add_component(entity, Health(50, 100))

        world.destroy_entity(entity)

        assert entity not in world.component_storage.entity_to_archetype


class TestWorldComponentOperations:
    def test_add_component(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position(5, 10, 15))

        component = world.get_component(entity, Position)
        assert isinstance(component, Position)
        assert component.x == 5
        assert component.y == 10
        assert component.z == 15

    def test_add_multiple_components(self, world, entity_with_components):
        pos = world.get_component(entity_with_components, Position)
        vel = world.get_component(entity_with_components, Velocity)
        health = world.get_component(entity_with_components, Health)

        assert isinstance(pos, Position)
        assert isinstance(vel, Velocity)
        assert isinstance(health, Health)

    def test_update_existing_component(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position(1, 2, 3))
        world.add_component(entity, Position(4, 5, 6))

        pos = world.get_component(entity, Position)
        assert pos.x == 4
        assert pos.y == 5
        assert pos.z == 6

    def test_remove_component(self, world, entity_with_components):
        assert isinstance(world.get_component(entity_with_components, Health), Health)

        world.remove_component(entity_with_components, Health)

        assert world.get_component(entity_with_components, Health) == StatusCodes.FAILURE

        assert isinstance(world.get_component(entity_with_components, Position), Position)
        assert isinstance(world.get_component(entity_with_components, Velocity), Velocity)

    def test_remove_nonexistent_component(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position())

        world.remove_component(entity, Health)

    def test_get_nonexistent_component(self, world):
        entity = world.create_entity()
        result = world.get_component(entity, Position)
        assert result == StatusCodes.FAILURE

    def test_get_components_multiple(self, world, entity_with_components):
        components = world.get_components(entity_with_components, Position, Velocity)
        assert len(components) == 2
        assert isinstance(components[0], Position)
        assert isinstance(components[1], Velocity)

    def test_get_components_with_missing(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position())

        result = world.get_components(entity, Position, Health)
        assert result == StatusCodes.FAILURE


class TestWorldEdgeCases:
    def test_add_component_to_dead_entity(self, world):
        entity = world.create_entity()
        world.destroy_entity(entity)

        world.add_component(entity, Position())
        assert world.get_component(entity, Position) == StatusCodes.FAILURE

    def test_remove_component_from_dead_entity(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position())
        world.destroy_entity(entity)

        world.remove_component(entity, Position)

    def test_get_component_from_dead_entity(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position())
        world.destroy_entity(entity)

        result = world.get_component(entity, Position)
        assert result == StatusCodes.FAILURE


class TestWorldOrRaiseMethods:
    def test_create_entity_or_raise_succeeds(self, world):
        entity = world.create_entity_or_raise()

        assert entity != StatusCodes.FAILURE
        assert world.entity_manager.is_alive(entity)

    def test_get_component_or_raise_succeeds_when_component_exists(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position(1, 2, 3))

        component = world.get_component_or_raise(entity, Position)

        assert isinstance(component, Position)
        assert component.x == 1
        assert component.y == 2
        assert component.z == 3

    def test_get_component_or_raise_raises_when_component_missing(self, world):
        entity = world.create_entity()

        with pytest.raises(
            ComponentNotFoundError, match="Component operation 'get_component' failed"
        ):
            world.get_component_or_raise(entity, Position)

    def test_get_component_or_raise_raises_when_entity_dead(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position())
        world.destroy_entity(entity)

        with pytest.raises(
            ComponentNotFoundError, match="Component operation 'get_component' failed"
        ):
            world.get_component_or_raise(entity, Position)

    def test_get_components_or_raise_succeeds_when_all_components_exist(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position(1, 2, 3))
        world.add_component(entity, Velocity(4, 5, 6))

        components = world.get_components_or_raise(entity, Position, Velocity)

        assert len(components) == 2
        assert isinstance(components[0], Position)
        assert isinstance(components[1], Velocity)

    def test_get_components_or_raise_raises_when_any_component_missing(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position())

        with pytest.raises(
            ComponentNotFoundError, match="Component operation 'get_components' failed"
        ):
            world.get_components_or_raise(entity, Position, Health)

    def test_get_components_or_raise_raises_when_entity_dead(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position())
        world.destroy_entity(entity)

        with pytest.raises(
            ComponentNotFoundError, match="Component operation 'get_components' failed"
        ):
            world.get_components_or_raise(entity, Position)
