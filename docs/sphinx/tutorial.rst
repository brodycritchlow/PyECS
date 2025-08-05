Tutorial
========

This tutorial will walk you through building a simple game with PyECS.

Creating Components
-------------------

Components in PyECS are simple Python classes that store data. They don't need to inherit from any base class. We recommend using dataclasses for cleaner syntax:

.. code-block:: python

   from dataclasses import dataclass
   
   @dataclass
   class Position:
       x: float
       y: float

   @dataclass
   class Velocity:
       x: float
       y: float
   
   @dataclass
   class Health:
       current: int
       max_health: int

   @dataclass
   class PlayerTag:
       pass

**Tip:** You can make components immutable by using ``frozen=True``:

.. code-block:: python

   @dataclass(frozen=True)
   class Position:
       x: float
       y: float
   
   # This creates immutable components that cannot be modified after creation
   # pos = Position(10, 20)
   # pos.x = 30  # ❌ Raises FrozenInstanceError

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

Working with Immutable Components
----------------------------------

While mutable components work well for most use cases, immutable components can provide additional safety and predictability:

.. code-block:: python

   from dataclasses import dataclass, replace
   
   @dataclass(frozen=True)
   class Position:
       x: float
       y: float
       
       def moved_by(self, dx: float, dy: float) -> 'Position':
           """Returns a new Position moved by the given deltas."""
           return Position(self.x + dx, self.y + dy)
   
   # Using immutable components in a system
   class ImmutableMovementSystem:
       def update(self, world, dt: float) -> None:
           query = Query().with_components(Position, Velocity)
           entities = query.execute(world)
           
           for entity in entities:
               pos = world.get_component(entity, Position)
               vel = world.get_component(entity, Velocity)
               
               # Create a new position instead of modifying
               new_pos = pos.moved_by(vel.x * dt, vel.y * dt)
               
               # Replace the component
               world.remove_component(entity, Position)
               world.add_component(entity, new_pos)

**Benefits of Immutable Components:**

- **Thread Safety**: Immutable objects can be safely shared between threads
- **Predictability**: Components can't be accidentally modified elsewhere
- **Debugging**: Easier to track when and how values change
- **Hashability**: Can be used as dictionary keys or in sets

**Using dataclass replace():**

.. code-block:: python

   # The replace() function creates a new instance with some fields updated
   old_pos = Position(10, 20)
   new_pos = replace(old_pos, x=15)  # Position(x=15, y=20)

Choose between mutable and immutable components based on your needs. Mutable components are simpler for frequent updates, while immutable components provide better safety guarantees.