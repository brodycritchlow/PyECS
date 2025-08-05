from pyecs import ECSWorld
from pyecs.processing.System import System

from .conftest import Position, Velocity


class MovementSystem(System):
    def __init__(self):
        super().__init__()
        self.init_called = False
        self.update_count = 0
        self.cleanup_called = False
        self.last_dt = 0

    def init(self, world: ECSWorld):
        self.init_called = True

    def update(self, world: ECSWorld, dt: float):
        self.update_count += 1
        self.last_dt = dt

        from pyecs.querying.Query import Query
        query = Query().with_components(Position, Velocity)
        entities = query.execute(world)
        
        for entity in entities:
            pos = world.get_component(entity, Position)
            vel = world.get_component(entity, Velocity)

            if isinstance(pos, Position) and isinstance(vel, Velocity):
                pos.x += vel.dx * dt
                pos.y += vel.dy * dt
                pos.z += vel.dz * dt

    def cleanup(self, world: ECSWorld):
        self.cleanup_called = True


class CountingSystem(System):
    def __init__(self):
        super().__init__()
        self.entity_count = 0

    def update(self, world: ECSWorld, dt: float):
        from pyecs.querying.Query import Query
        query = Query().with_components(Position)
        entities = query.execute(world)
        self.entity_count = len(entities)


class TestSystemLifecycle:
    def test_system_init_called_on_add(self, world):
        system = MovementSystem()

        assert not system.init_called

        world.add_system(system)

        assert system.init_called

    def test_system_cleanup_called_on_remove(self, world):
        system = MovementSystem()
        world.add_system(system)

        assert not system.cleanup_called

        world.remove_system(system)

        assert system.cleanup_called

    def test_system_update_called_on_world_update(self, world):
        system = MovementSystem()
        world.add_system(system)

        assert system.update_count == 0

        world.update(0.016)

        assert system.update_count == 1
        assert system.last_dt == 0.016

    def test_multiple_systems_update_in_order(self, world):
        update_order = []

        class OrderTestSystem(System):
            def __init__(self, name):
                super().__init__()
                self.name = name

            def update(self, world: ECSWorld, dt: float):
                update_order.append(self.name)

        system1 = OrderTestSystem("first")
        system2 = OrderTestSystem("second")
        system3 = OrderTestSystem("third")

        world.add_system(system1)
        world.add_system(system2)
        world.add_system(system3)

        world.update(0.016)

        assert update_order == ["first", "second", "third"]


class TestSystemQueries:
    def test_query_entities_finds_matching_entities(self, world):
        system = CountingSystem()
        world.add_system(system)

        entity1 = world.create_entity()
        entity2 = world.create_entity()
        entity3 = world.create_entity()

        world.add_component(entity1, Position())
        world.add_component(entity2, Position())
        world.add_component(entity3, Velocity())

        world.update(0.016)

        assert system.entity_count == 2

    def test_query_entities_with_multiple_components(self, world):
        system = MovementSystem()

        entity1 = world.create_entity()
        entity2 = world.create_entity()
        entity3 = world.create_entity()

        world.add_component(entity1, Position())
        world.add_component(entity1, Velocity())

        world.add_component(entity2, Position())

        world.add_component(entity3, Velocity())

        from pyecs.querying.Query import Query
        query = Query().with_components(Position, Velocity)
        entities = query.execute(world)

        assert len(entities) == 1
        assert entity1 in entities

    def test_query_entities_returns_empty_for_no_matches(self, world):
        system = MovementSystem()

        entity = world.create_entity()
        world.add_component(entity, Position())

        from pyecs.querying.Query import Query
        query = Query().with_components(Velocity)
        entities = query.execute(world)

        assert len(entities) == 0


class TestSystemFunctionality:
    def test_movement_system_updates_positions(self, world):
        system = MovementSystem()
        world.add_system(system)

        entity = world.create_entity()
        world.add_component(entity, Position(0, 0, 0))
        world.add_component(entity, Velocity(10, 20, 30))

        world.update(1.0)

        pos = world.get_component(entity, Position)
        assert pos.x == 10
        assert pos.y == 20
        assert pos.z == 30

    def test_system_handles_entity_removal(self, world):
        system = CountingSystem()
        world.add_system(system)

        entities = []
        for _ in range(5):
            entity = world.create_entity()
            world.add_component(entity, Position())
            entities.append(entity)

        world.update(0.016)
        assert system.entity_count == 5

        world.destroy_entity(entities[0])
        world.destroy_entity(entities[1])

        world.update(0.016)
        assert system.entity_count == 3

    def test_system_handles_component_removal(self, world):
        system = MovementSystem()
        world.add_system(system)

        entity = world.create_entity()
        world.add_component(entity, Position(0, 0, 0))
        world.add_component(entity, Velocity(10, 10, 10))

        world.update(1.0)
        pos = world.get_component(entity, Position)
        assert pos.x == 10

        world.remove_component(entity, Velocity)

        world.update(1.0)
        pos = world.get_component(entity, Position)
        assert pos.x == 10


class TestSystemEdgeCases:
    def test_empty_system_update(self, world):
        class EmptySystem(System):
            def update(self, world: ECSWorld, dt: float):
                pass

        system = EmptySystem()
        world.add_system(system)

        world.update(0.016)

    def test_system_with_no_matching_entities(self, world):
        system = MovementSystem()
        world.add_system(system)

        for _ in range(10):
            entity = world.create_entity()
            world.add_component(entity, Position())

        world.update(0.016)

        assert system.update_count == 1

    def test_multiple_updates_accumulate_correctly(self, world):
        system = MovementSystem()
        world.add_system(system)

        entity = world.create_entity()
        world.add_component(entity, Position(0, 0, 0))
        world.add_component(entity, Velocity(1, 1, 1))

        for _ in range(100):
            world.update(0.01)

        pos = world.get_component(entity, Position)
        assert abs(pos.x - 1.0) < 0.001
        assert abs(pos.y - 1.0) < 0.001
        assert abs(pos.z - 1.0) < 0.001
