Getting Started
===============

This guide will help you get started with PyECS, a Python Entity Component System implementation with runtime type safety.

Installation
------------

Install PyECS using pip:

.. code-block:: bash

   pip install pyecs

Basic Concepts
--------------

PyECS follows the Entity Component System (ECS) architectural pattern:

* **Entities** - Unique identifiers (UUIDs) that represent game objects
* **Components** - Plain Python classes that store data (no logic)
* **Systems** - Classes that contain the game logic and operate on entities
* **World** - The main container that manages everything
* **Archetypes** - Groups of entities that share the same component types

**See Also:** :doc:`architecture` for detailed flowcharts of these concepts

Your First PyECS Program
------------------------

Here's a minimal example to get you started:

.. code-block:: python

   from dataclasses import dataclass
   from pyecs import ECSWorld
   
   @dataclass
   class Position:
       x: float = 0
       y: float = 0
   
   @dataclass
   class Velocity:
       dx: float = 0
       dy: float = 0
   
   class MovementSystem:
       def update(self, world, dt):
           from pyecs.querying.Query import Query
           
           query = Query().with_components(Position, Velocity)
           entities = query.execute(world)
           
           for entity in entities:
               pos = world.get_component(entity, Position)
               vel = world.get_component(entity, Velocity)
               pos.x += vel.dx * dt
               pos.y += vel.dy * dt
   
   world = ECSWorld()
   world.add_system(MovementSystem())
   
   player = world.create_entity()
   world.add_component(player, Position(x=0, y=0))
   world.add_component(player, Velocity(dx=5, dy=0))
   
   for i in range(10):
       world.update(dt=0.1)
       pos = world.get_component(player, Position)
       print(f"Frame {i}: Player at ({pos.x}, {pos.y})")

**See Also:** :doc:`architecture` - :ref:`World.create_entity <world-create-entity>`, :ref:`World.add_component <world-add-component>`, :ref:`World.add_system <world-add-system>`, :ref:`World.update <world-update>`, :ref:`World.get_component <world-get-component>`

Key Points to Remember
----------------------

1. **Components are just data** - Any Python class can be a component
2. **Systems receive the world** - The `update` method gets the world object, not entities
3. **Use archetypes for queries** - This is the most efficient way to find entities
4. **Entity IDs are UUIDs** - Unique identifiers for each entity

Common Patterns
---------------

**Creating multiple entities:**

.. code-block:: python

   for i in range(10):
       enemy = world.create_entity()
       world.add_component(enemy, Position(x=i*10, y=0))
       world.add_component(enemy, Health(hp=100))

**See Also:** :doc:`architecture` - :ref:`World.create_entity <world-create-entity>`, :ref:`World.add_component <world-add-component>`

**Checking if entity has component:**

.. code-block:: python

   health = world.get_component(entity, Health)
   if health != -1:
       print(f"Entity has {health.hp} health")

**Removing components:**

.. code-block:: python

   world.remove_component(entity, PowerUp)

**See Also:** :doc:`architecture` - :ref:`World.remove_component <world-remove-component>`

Next Steps
----------

- Read the :doc:`tutorial` for a more comprehensive example
- Explore the :doc:`api` for detailed documentation
- See :doc:`troubleshooting` if you encounter issues

.. toctree::
   :hidden:

   self
   tutorial
   architecture
   api
   troubleshooting

