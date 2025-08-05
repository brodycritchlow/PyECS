import uuid

from pyecs import StatusCodes
from pyecs.containers.Archetype import Archetype

from .conftest import Health, Position, Velocity


class TestArchetypeBasics:
    def test_archetype_starts_empty(self):
        archetype = Archetype()

        assert len(archetype.entities) == 0
        assert len(archetype.entity_indices) == 0
        assert len(archetype.components) == 0

    def test_add_entity_with_components(self):
        archetype = Archetype()
        entity = str(uuid.uuid4())
        components = [Position(1, 2, 3), Velocity(4, 5, 6)]

        result = archetype.add_entity(entity, components)

        assert result == StatusCodes.SUCCESS
        assert entity in archetype.entities
        assert entity in archetype.entity_indices
        assert archetype.entity_indices[entity] == 0
        assert Position in archetype.components
        assert Velocity in archetype.components

    def test_add_entity_without_components(self):
        archetype = Archetype()
        entity = str(uuid.uuid4())

        result = archetype.add_entity(entity, [])

        assert result == StatusCodes.SUCCESS
        assert entity in archetype.entities
        assert len(archetype.components) == 0

    def test_add_duplicate_entity_fails(self):
        archetype = Archetype()
        entity = str(uuid.uuid4())

        archetype.add_entity(entity, [Position()])
        result = archetype.add_entity(entity, [Position()])

        assert result == StatusCodes.FAILURE


class TestArchetypeRemoval:
    def test_remove_entity_from_end(self):
        archetype = Archetype()
        entity1 = str(uuid.uuid4())
        entity2 = str(uuid.uuid4())

        archetype.add_entity(entity1, [Position(1, 2, 3)])
        archetype.add_entity(entity2, [Position(4, 5, 6)])

        result = archetype.remove_entity(entity2)

        assert result == StatusCodes.SUCCESS
        assert entity2 not in archetype.entities
        assert entity2 not in archetype.entity_indices
        assert len(archetype.entities) == 1

    def test_remove_entity_from_middle_swaps_with_last(self):
        archetype = Archetype()
        entity1 = str(uuid.uuid4())
        entity2 = str(uuid.uuid4())
        entity3 = str(uuid.uuid4())

        archetype.add_entity(entity1, [Position(1, 0, 0)])
        archetype.add_entity(entity2, [Position(2, 0, 0)])
        archetype.add_entity(entity3, [Position(3, 0, 0)])

        result = archetype.remove_entity(entity1)

        assert result == StatusCodes.SUCCESS
        assert entity1 not in archetype.entities
        assert entity3 in archetype.entities
        assert archetype.entity_indices[entity3] == 0
        assert archetype.components[Position][0].x == 3

    def test_remove_nonexistent_entity_fails(self):
        archetype = Archetype()
        entity = str(uuid.uuid4())

        result = archetype.remove_entity(entity)

        assert result == StatusCodes.FAILURE

    def test_remove_last_entity_empties_archetype(self):
        archetype = Archetype()
        entity = str(uuid.uuid4())

        archetype.add_entity(entity, [Position()])
        archetype.remove_entity(entity)

        assert len(archetype.entities) == 0
        assert len(archetype.entity_indices) == 0
        assert len(archetype.components[Position]) == 0


class TestArchetypeComponentRetrieval:
    def test_get_component_for_entity(self):
        archetype = Archetype()
        entity = str(uuid.uuid4())
        position = Position(10, 20, 30)

        archetype.add_entity(entity, [position])

        result = archetype.get_component(entity, Position)

        assert isinstance(result, Position)
        assert result.x == 10
        assert result.y == 20
        assert result.z == 30

    def test_get_nonexistent_component_type_fails(self):
        archetype = Archetype()
        entity = str(uuid.uuid4())

        archetype.add_entity(entity, [Position()])

        result = archetype.get_component(entity, Health)

        assert result == StatusCodes.FAILURE

    def test_get_component_for_nonexistent_entity_fails(self):
        archetype = Archetype()
        entity = str(uuid.uuid4())
        fake_entity = str(uuid.uuid4())

        archetype.add_entity(entity, [Position()])

        result = archetype.get_component(fake_entity, Position)

        assert result == StatusCodes.FAILURE


class TestArchetypeIteration:
    def test_iter_entities_returns_all_entities(self):
        archetype = Archetype()
        entities = [str(uuid.uuid4()) for _ in range(5)]

        for entity in entities:
            archetype.add_entity(entity, [Position()])

        iterated_entities = list(archetype.iter_entities())

        assert len(iterated_entities) == 5
        assert set(iterated_entities) == set(entities)

    def test_iter_components_returns_all_components_of_type(self):
        archetype = Archetype()
        positions = []

        for i in range(3):
            entity = str(uuid.uuid4())
            pos = Position(i, i*2, i*3)
            positions.append(pos)
            archetype.add_entity(entity, [pos, Velocity()])

        iterated_positions = list(archetype.iter_components(Position))

        assert len(iterated_positions) == 3
        for i, pos in enumerate(iterated_positions):
            assert pos.x == i
            assert pos.y == i * 2
            assert pos.z == i * 3

    def test_iter_components_empty_for_missing_type(self):
        archetype = Archetype()
        entity = str(uuid.uuid4())

        archetype.add_entity(entity, [Position()])

        iterated = list(archetype.iter_components(Health))

        assert len(iterated) == 0


class TestArchetypeParallelArrays:
    def test_entity_and_component_indices_match(self):
        archetype = Archetype()
        entities = []

        for i in range(10):
            entity = str(uuid.uuid4())
            entities.append(entity)
            archetype.add_entity(entity, [Position(i, 0, 0), Health(i, 100)])

        for i, entity in enumerate(entities):
            index = archetype.entity_indices[entity]
            assert index == i
            assert archetype.components[Position][index].x == i
            assert archetype.components[Health][index].current == i

    def test_parallel_arrays_maintained_after_removal(self):
        archetype = Archetype()
        entities = []

        for i in range(5):
            entity = str(uuid.uuid4())
            entities.append(entity)
            archetype.add_entity(entity, [Position(i, 0, 0), Velocity(i, 0, 0)])

        archetype.remove_entity(entities[2])

        for entity in archetype.entities:
            index = archetype.entity_indices[entity]
            pos = archetype.components[Position][index]
            vel = archetype.components[Velocity][index]
            assert pos.x == vel.dx

    def test_component_arrays_grow_together(self):
        archetype = Archetype()

        for i in range(100):
            entity = str(uuid.uuid4())
            archetype.add_entity(entity, [Position(i, 0, 0), Velocity(0, i, 0)])

        assert len(archetype.components[Position]) == 100
        assert len(archetype.components[Velocity]) == 100
        assert len(archetype.entities) == 100
