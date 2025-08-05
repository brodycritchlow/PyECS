import uuid

from pyecs import StatusCodes
from pyecs.containers.Archetype import Archetype
from pyecs.containers.ComponentStorage import ComponentStorage

from .conftest import Health, Name, Position, Velocity


class TestComponentStorageBasics:
    def test_storage_starts_empty(self):
        storage = ComponentStorage()

        assert len(storage.archetypes) == 0
        assert len(storage.entity_to_archetype) == 0

    def test_add_component_to_new_entity(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()

        result = storage.add_component(entity, Position(1, 2, 3))

        assert result == StatusCodes.COMPONENT_ADDED
        assert entity in storage.entity_to_archetype
        assert Position in storage.entity_to_archetype[entity]

    def test_add_component_to_nonexistent_entity_fails(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        result = storage.add_component(entity, Position())

        assert result == StatusCodes.FAILURE

    def test_update_existing_component(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()

        storage.add_component(entity, Position(1, 2, 3))
        result = storage.add_component(entity, Position(4, 5, 6))

        assert result == StatusCodes.COMPONENT_UPDATED

        component = storage.get_component(entity, Position)
        assert component.x == 4
        assert component.y == 5
        assert component.z == 6


class TestComponentStorageRetrieval:
    def test_get_component_from_entity(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()

        storage.add_component(entity, Position(10, 20, 30))

        component = storage.get_component(entity, Position)
        assert isinstance(component, Position)
        assert component.x == 10
        assert component.y == 20
        assert component.z == 30

    def test_get_nonexistent_component_returns_failure(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset([Position])
        storage.archetypes[frozenset([Position])] = Archetype()

        result = storage.get_component(entity, Health)
        assert result == StatusCodes.FAILURE

    def test_get_component_from_nonexistent_entity_returns_failure(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        result = storage.get_component(entity, Position)
        assert result == StatusCodes.FAILURE

    def test_has_component_returns_true_when_exists(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()
        storage.add_component(entity, Position())

        assert storage.has_component(entity, Position) is True

    def test_has_component_returns_false_when_missing(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset([Position])

        assert storage.has_component(entity, Health) is False

    def test_has_component_returns_false_for_nonexistent_entity(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        assert storage.has_component(entity, Position) is False


class TestComponentStorageRemoval:
    def test_remove_component_from_entity(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()

        storage.add_component(entity, Position())
        storage.add_component(entity, Health())

        result = storage.remove_component(entity, Health)

        assert result == StatusCodes.COMPONENT_REMOVED
        assert storage.has_component(entity, Health) is False
        assert storage.has_component(entity, Position) is True

    def test_remove_nonexistent_component_returns_failure(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset([Position])
        storage.archetypes[frozenset([Position])] = Archetype()

        result = storage.remove_component(entity, Health)
        assert result == StatusCodes.FAILURE

    def test_remove_last_component_removes_entity(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()
        storage.add_component(entity, Position())

        result = storage.remove_component(entity, Position)

        assert result == StatusCodes.COMPONENT_REMOVED
        assert entity not in storage.entity_to_archetype

    def test_remove_entity_clears_all_data(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()
        storage.add_component(entity, Position())
        storage.add_component(entity, Health())

        result = storage.remove_entity(entity)

        assert result == StatusCodes.SUCCESS
        assert entity not in storage.entity_to_archetype


class TestComponentStorageArchetypes:
    def test_entity_moves_between_archetypes(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()

        storage.add_component(entity, Position())
        assert Position in storage.entity_to_archetype[entity]

        storage.add_component(entity, Velocity())
        assert Position in storage.entity_to_archetype[entity]
        assert Velocity in storage.entity_to_archetype[entity]

        storage.remove_component(entity, Position)
        assert Position not in storage.entity_to_archetype[entity]
        assert Velocity in storage.entity_to_archetype[entity]

    def test_archetype_created_on_demand(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()

        initial_count = len(storage.archetypes)

        storage.add_component(entity, Position())
        storage.add_component(entity, Velocity())

        assert len(storage.archetypes) > initial_count
        assert frozenset([Position, Velocity]) in storage.archetypes

    def test_multiple_entities_share_archetype(self):
        storage = ComponentStorage()
        entity1 = str(uuid.uuid4())
        entity2 = str(uuid.uuid4())

        storage.entity_to_archetype[entity1] = frozenset()
        storage.entity_to_archetype[entity2] = frozenset()
        storage.archetypes[frozenset()] = Archetype()

        storage.add_component(entity1, Position())
        storage.add_component(entity1, Health())

        storage.add_component(entity2, Position())
        storage.add_component(entity2, Health())

        assert storage.entity_to_archetype[entity1] == storage.entity_to_archetype[entity2]
        assert len(storage.archetypes[frozenset([Position, Health])].entities) == 2


class TestComponentStorageEdgeCases:
    def test_get_entity_components_returns_all_components(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()

        storage.add_component(entity, Position(1, 2, 3))
        storage.add_component(entity, Velocity(4, 5, 6))
        storage.add_component(entity, Health(75, 100))

        components = storage.get_entity_components(entity)

        assert len(components) == 3
        assert any(isinstance(c, Position) for c in components)
        assert any(isinstance(c, Velocity) for c in components)
        assert any(isinstance(c, Health) for c in components)

    def test_move_entity_preserves_component_data(self):
        storage = ComponentStorage()
        entity = str(uuid.uuid4())

        storage.entity_to_archetype[entity] = frozenset()
        storage.archetypes[frozenset()] = Archetype()

        storage.add_component(entity, Position(10, 20, 30))
        storage.add_component(entity, Name("TestEntity"))

        pos_before = storage.get_component(entity, Position)
        name_before = storage.get_component(entity, Name)

        storage.add_component(entity, Health(50, 100))

        pos_after = storage.get_component(entity, Position)
        name_after = storage.get_component(entity, Name)

        assert pos_before.x == pos_after.x
        assert pos_before.y == pos_after.y
        assert pos_before.z == pos_after.z
        assert name_before.value == name_after.value
