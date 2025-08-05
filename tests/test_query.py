from pyecs.querying.Query import Query

from .conftest import Health, Name, Position, Velocity


class TestQueryBuilder:
    def test_query_starts_empty(self):
        query = Query()

        assert len(query._with) == 0
        assert len(query._without) == 0

    def test_with_components_adds_to_include(self):
        query = Query().with_components(Position, Velocity)

        assert Position in query._with
        assert Velocity in query._with
        assert len(query._with) == 2

    def test_without_components_adds_to_exclude(self):
        query = Query().without_components(Health, Name)

        assert Health in query._without
        assert Name in query._without
        assert len(query._without) == 2

    def test_chained_query_building(self):
        query = (Query()
                .with_components(Position, Velocity)
                .without_components(Health)
                .with_components(Name))

        assert len(query._with) == 3
        assert Position in query._with
        assert Velocity in query._with
        assert Name in query._with
        assert Health in query._without

    def test_duplicate_components_not_added(self):
        query = (Query()
                .with_components(Position)
                .with_components(Position, Velocity))

        assert len(query._with) == 2


class TestQueryExecution:
    def test_execute_on_empty_world_returns_empty(self, world):
        query = Query().with_components(Position)
        entities = query.execute(world)

        assert len(entities) == 0

    def test_execute_finds_entities_with_single_component(self, world):
        entity1 = world.create_entity()
        entity2 = world.create_entity()
        entity3 = world.create_entity()

        world.add_component(entity1, Position())
        world.add_component(entity2, Position())
        world.add_component(entity3, Velocity())

        query = Query().with_components(Position)
        entities = query.execute(world)

        assert len(entities) == 2
        assert entity1 in entities
        assert entity2 in entities
        assert entity3 not in entities

    def test_execute_finds_entities_with_multiple_components(self, world):
        entity1 = world.create_entity()
        entity2 = world.create_entity()
        entity3 = world.create_entity()

        world.add_component(entity1, Position())
        world.add_component(entity1, Velocity())

        world.add_component(entity2, Position())

        world.add_component(entity3, Position())
        world.add_component(entity3, Velocity())
        world.add_component(entity3, Health())

        query = Query().with_components(Position, Velocity)
        entities = query.execute(world)

        assert len(entities) == 2
        assert entity1 in entities
        assert entity2 not in entities
        assert entity3 in entities

    def test_execute_excludes_entities_with_excluded_components(self, world):
        entity1 = world.create_entity()
        entity2 = world.create_entity()
        entity3 = world.create_entity()

        world.add_component(entity1, Position())
        world.add_component(entity1, Health())

        world.add_component(entity2, Position())

        world.add_component(entity3, Position())
        world.add_component(entity3, Health())
        world.add_component(entity3, Name())

        query = Query().with_components(Position).without_components(Health)
        entities = query.execute(world)

        assert len(entities) == 1
        assert entity1 not in entities
        assert entity2 in entities
        assert entity3 not in entities

    def test_execute_with_no_requirements_returns_all(self, world):
        entities = []
        for _ in range(5):
            entity = world.create_entity()
            entities.append(entity)
            world.add_component(entity, Position())

        query = Query()
        result = query.execute(world)

        assert len(result) == 5
        assert all(e in result for e in entities)


class TestQueryComplexScenarios:
    def test_query_multiple_archetypes(self, world):
        entities_pos_only = []
        entities_pos_vel = []
        entities_all = []

        for _ in range(3):
            e = world.create_entity()
            world.add_component(e, Position())
            entities_pos_only.append(e)

        for _ in range(3):
            e = world.create_entity()
            world.add_component(e, Position())
            world.add_component(e, Velocity())
            entities_pos_vel.append(e)

        for _ in range(3):
            e = world.create_entity()
            world.add_component(e, Position())
            world.add_component(e, Velocity())
            world.add_component(e, Health())
            entities_all.append(e)

        query = Query().with_components(Position)
        result = query.execute(world)

        assert len(result) == 9
        assert all(e in result for e in entities_pos_only)
        assert all(e in result for e in entities_pos_vel)
        assert all(e in result for e in entities_all)

    def test_query_respects_entity_removal(self, world):
        entity1 = world.create_entity()
        entity2 = world.create_entity()

        world.add_component(entity1, Position())
        world.add_component(entity2, Position())

        query = Query().with_components(Position)

        initial_result = query.execute(world)
        assert len(initial_result) == 2

        world.destroy_entity(entity1)

        after_removal = query.execute(world)
        assert len(after_removal) == 1
        assert entity2 in after_removal
        assert entity1 not in after_removal

    def test_query_respects_component_removal(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position())
        world.add_component(entity, Velocity())

        query = Query().with_components(Position, Velocity)

        initial_result = query.execute(world)
        assert len(initial_result) == 1
        assert entity in initial_result

        world.remove_component(entity, Velocity)

        after_removal = query.execute(world)
        assert len(after_removal) == 0

    def test_query_handles_empty_archetypes(self, world):
        entity = world.create_entity()

        query = Query().with_components(Position)
        result = query.execute(world)

        assert len(result) == 0
        assert entity not in result


class TestQueryEdgeCases:
    def test_impossible_query_returns_empty(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position())

        query = Query().with_components(Position).without_components(Position)
        result = query.execute(world)

        assert len(result) == 0

    def test_query_with_many_components(self, world):
        entity = world.create_entity()
        world.add_component(entity, Position())
        world.add_component(entity, Velocity())
        world.add_component(entity, Health())
        world.add_component(entity, Name())

        query = Query().with_components(Position, Velocity, Health, Name)
        result = query.execute(world)

        assert len(result) == 1
        assert entity in result

    def test_query_performance_with_many_entities(self, world):
        target_entities = []

        for i in range(1000):
            entity = world.create_entity()
            world.add_component(entity, Position())

            if i % 10 == 0:
                world.add_component(entity, Velocity())
                target_entities.append(entity)

        query = Query().with_components(Position, Velocity)
        result = query.execute(world)

        assert len(result) == 100
        assert all(e in result for e in target_entities)
