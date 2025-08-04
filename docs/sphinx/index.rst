.. PyECS documentation master file, created by
   sphinx-quickstart on Sun Aug  3 22:46:41 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyECS Documentation
===================

PyECS is a Python Entity Component System (ECS) implementation with runtime type safety powered by beartype.

Features
--------

* **Type-safe** - Leverages beartype for runtime type checking
* **Pure Python** - No external dependencies except beartype
* **Fast** - Archetype-based storage for efficient component queries
* **Simple** - Clean, Pythonic API that's easy to understand

Installation
------------

.. code-block:: bash

   pip install pyecs

Quick Start
-----------

.. code-block:: python

   from pyecs import ECSWorld, System
   
   # Create a world
   world = ECSWorld()
   
   # Create entities and add components
   entity = world.create_entity()
   world.add_component(entity, Position(x=0, y=0))
   world.add_component(entity, Velocity(x=1, y=0))
   
   # Create and add systems
   world.add_system(MovementSystem())
   
   # Update the world
   world.update(dt=1.0)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   tutorial
   api

