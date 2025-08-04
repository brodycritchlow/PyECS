Tutorial
========

This tutorial will walk you through building a simple game with PyECS.

Creating Components
-------------------

Components are simple data containers:

.. code-block:: python

   class Position:
       def __init__(self, x: float, y: float):
           self.x = x
           self.y = y

   class Velocity:
       def __init__(self, x: float, y: float):
           self.x = x
           self.y = y

Creating Systems
----------------

Systems contain the game logic:

.. code-block:: python

   from pyecs.processing.System import System
   
   class MovementSystem(System):
       def update(self, world, dt: float) -> None:
           # Query entities with both Position and Velocity
           query = world.component_storage.query()
           query.with_components(Position, Velocity)
           
           for entity in query.execute(world.component_storage):
               pos = world.get_component(entity, Position)
               vel = world.get_component(entity, Velocity)
               
               pos.x += vel.x * dt
               pos.y += vel.y * dt

Running the Game Loop
---------------------

.. code-block:: python

   from pyecs.core.World import ECSWorld
   
   # Create world
   world = ECSWorld()
   
   # Add systems
   world.add_system(MovementSystem())
   
   # Create entities
   player = world.create_entity()
   world.add_component(player, Position(0, 0))
   world.add_component(player, Velocity(10, 0))
   
   # Game loop
   while True:
       world.update(dt=0.016)  # 60 FPS