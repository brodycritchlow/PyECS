from pyecs import StatusCodes
from pyecs.managers.EntityManager import EntityManager


class TestEntityManagerCreation:
    def test_create_entity_returns_valid_uuid(self):
        manager = EntityManager()
        result = manager.create_entity()

        assert isinstance(result, tuple)
        assert result[0] == StatusCodes.ENTITY_CREATED
        assert result[1] in manager.alive_entities

    def test_create_multiple_entities_have_unique_ids(self):
        manager = EntityManager()
        entities = []

        for _ in range(100):
            result = manager.create_entity()
            entities.append(result[1])

        assert len(set(entities)) == 100
        assert all(manager.is_alive(entity) for entity in entities)

    def test_entities_start_alive(self):
        manager = EntityManager()
        result = manager.create_entity()
        entity = result[1]

        assert manager.is_alive(entity) is True


class TestEntityManagerDestruction:
    def test_destroy_entity_marks_as_dead(self):
        manager = EntityManager()
        result = manager.create_entity()
        entity = result[1]

        destroy_result = manager.destroy_entity(entity)

        assert destroy_result == StatusCodes.ENTITY_DESTROYED
        assert manager.is_alive(entity) is False
        assert entity not in manager.alive_entities

    def test_destroy_nonexistent_entity_returns_failure(self):
        manager = EntityManager()
        fake_entity = "00000000-0000-0000-0000-000000000000"

        result = manager.destroy_entity(fake_entity)

        assert result == StatusCodes.FAILURE

    def test_destroy_already_dead_entity_returns_failure(self):
        manager = EntityManager()
        result = manager.create_entity()
        entity = result[1]

        manager.destroy_entity(entity)
        second_destroy = manager.destroy_entity(entity)

        assert second_destroy == StatusCodes.FAILURE


class TestEntityManagerQueries:
    def test_is_alive_returns_true_for_living_entity(self):
        manager = EntityManager()
        result = manager.create_entity()
        entity = result[1]

        assert manager.is_alive(entity) is True

    def test_is_alive_returns_false_for_dead_entity(self):
        manager = EntityManager()
        result = manager.create_entity()
        entity = result[1]
        manager.destroy_entity(entity)

        assert manager.is_alive(entity) is False

    def test_is_alive_returns_false_for_nonexistent_entity(self):
        manager = EntityManager()
        fake_entity = "00000000-0000-0000-0000-000000000000"

        assert manager.is_alive(fake_entity) is False

    def test_is_alive_behaves_correctly_with_lifecycle(self):
        manager = EntityManager()
        result = manager.create_entity()
        entity = result[1]

        assert manager.is_alive(entity) is True

        manager.destroy_entity(entity)
        assert manager.is_alive(entity) is False


class TestEntityManagerEdgeCases:
    def test_manager_handles_many_entities(self):
        manager = EntityManager()
        entities = []

        for _ in range(10000):
            result = manager.create_entity()
            entities.append(result[1])

        assert len(manager.alive_entities) == 10000
        assert all(manager.is_alive(entity) for entity in entities)

    def test_manager_reuses_destroyed_entity_slots(self):
        manager = EntityManager()
        entities = []

        for _ in range(100):
            result = manager.create_entity()
            entity = result[1]
            entities.append(entity)
            manager.destroy_entity(entity)

        assert all(e not in manager.alive_entities for e in entities)
