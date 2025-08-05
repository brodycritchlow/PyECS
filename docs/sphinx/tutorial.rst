Tutorial
========

This tutorial will walk you through building a simple game with PyECS.

Creating Components
-------------------

Components in PyECS are simple Python classes that store data. They don't need to inherit from any base class:

.. code-block:: python

   class Position:
       def __init__(self, x: float, y: float):
           self.x = x
           self.y = y

   class Velocity:
       def __init__(self, x: float, y: float):
           self.x = x
           self.y = y
   
   class Health:
       def __init__(self, current: int, max_health: int):
           self.current = current
           self.max_health = max_health

   class PlayerTag:
       pass

**See Also:** :doc:`architecture` - :ref:`World.add_component <world-add-component>`

Creating Systems
----------------

Systems contain the game logic. The `update` method receives the world object:

.. code-block:: python

   from pyecs.processing.System import System
   from pyecs.querying.Query import Query
   
   class MovementSystem(System):
       def update(self, world, dt: float) -> None:
           query = Query().with_components(Position, Velocity)
           entities = query.execute(world)
           
           for entity in entities:
               pos = world.get_component(entity, Position)
               vel = world.get_component(entity, Velocity)
               pos.x += vel.x * dt
               pos.y += vel.y * dt

   class HealthSystem(System):
       def update(self, world, dt: float) -> None:
           query = Query().with_components(Health)
           entities = query.execute(world)
           
           for entity in entities:
               health = world.get_component(entity, Health)
               if health.current <= 0:
                   world.destroy_entity(entity)

**See Also:** :doc:`architecture` - :ref:`Query.execute <query-execute>`, :ref:`Query.with_components <query-with-components>`, :ref:`World.get_component <world-get-component>`, :ref:`World.destroy_entity <world-destroy-entity>`

Running the Game Loop
---------------------

Here's a complete example that ties everything together:

.. code-block:: python

   from pyecs import ECSWorld
   import time
   
   world = ECSWorld()
   
   movement_system = MovementSystem()
   health_system = HealthSystem()
   
   world.add_system(movement_system)
   world.add_system(health_system)
   
   player = world.create_entity()
   world.add_component(player, Position(0, 0))
   world.add_component(player, Velocity(10, 5))
   world.add_component(player, Health(100, 100))
   world.add_component(player, PlayerTag())
   
   for i in range(5):
       enemy = world.create_entity()
       world.add_component(enemy, Position(i * 10, 20))
       world.add_component(enemy, Velocity(-5, 0))
       world.add_component(enemy, Health(50, 50))
   
   last_time = time.time()
   
   for _ in range(100):
       current_time = time.time()
       dt = current_time - last_time
       last_time = current_time
       
       world.update(dt=dt)
       
       player_pos = world.get_component(player, Position)
       print(f"Player at: ({player_pos.x:.2f}, {player_pos.y:.2f})")
       
       time.sleep(0.016)

**See Also:** :doc:`architecture` - :ref:`World.add_system <world-add-system>`, :ref:`World.create_entity <world-create-entity>`, :ref:`World.add_component <world-add-component>`, :ref:`World.update <world-update>`, :ref:`SystemManager.update_all <systemmanager-update-all>`

Understanding Archetypes
------------------------

PyECS uses an archetype-based storage system. An archetype is a unique combination of component types that entities can have:

- When you add components to an entity, it moves to the archetype matching its component set
- Entities with the same set of components are stored together for efficient iteration
- The Query system uses archetypes internally for efficient entity filtering

.. code-block:: python

   entity1 = world.create_entity()
   world.add_component(entity1, Position(0, 0))
   
   world.add_component(entity1, Velocity(1, 1))
   
   entity2 = world.create_entity()
   world.add_component(entity2, Position(5, 5))
   world.add_component(entity2, Velocity(2, 2))
   
   query = Query().with_components(Position, Velocity)
   entities = query.execute(world)
   print(f"Found {len(entities)} entities with Position and Velocity")

**See Also:** :doc:`architecture` - :ref:`Query.execute <query-execute>`, :ref:`Archetype Operations <archetype-operations>`