Troubleshooting
===============

This page covers common issues and their solutions when using PyECS.

Common Issues
-------------

System Update Method Signature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Problem:** Documentation or examples show systems receiving ``entities`` parameter.

**Solution:** Systems receive the ``world`` object, not entities:

.. code-block:: python

   # Correct:
   class MySystem:
       def update(self, world, dt):
           # Use world to access entities
           pass
   
   # Incorrect:
   class MySystem:
       def update(self, entities, dt):  # This won't work!
           pass

Component Not Found
~~~~~~~~~~~~~~~~~~~

**Problem:** ``world.get_component()`` returns ``-1`` (StatusCodes.FAILURE).

**Common Causes:**

1. Entity was destroyed
2. Component was never added
3. Component was removed

**Debugging:**

.. code-block:: python

   # Check if entity exists
   if not world.entity_manager.is_alive(entity):
       print("Entity has been destroyed")
   
   # Check what components the entity has
   for arch_key, arch in world.component_storage.archetypes.items():
       if entity in arch.entities:
           print(f"Entity has components: {[c.__name__ for c in arch_key]}")

Entity Creation Failed
~~~~~~~~~~~~~~~~~~~~~~

**Problem:** ``world.create_entity()`` returns ``-1``.

**Solution:** This typically means the entity manager has run out of available entity IDs. This is extremely rare in normal usage. Check for:

- Entity leaks (creating entities without destroying them)
- Infinite loops creating entities

Best Practices
--------------

Component Design
~~~~~~~~~~~~~~~~

**Do:**

- Keep components small and focused
- Use plain data classes
- Make components immutable when possible

**Don't:**

- Put logic in components
- Store references to other entities (use entity IDs instead)
- Use inheritance for components

System Design
~~~~~~~~~~~~~

**Do:**

- Keep systems focused on one responsibility
- Process entities in batches
- Use the archetype system for efficient queries

**Don't:**

- Modify the entity's component set while iterating
- Store entity references between frames
- Assume entity IDs are sequential

Error Handling
~~~~~~~~~~~~~~

For production code, consider using the ``_or_raise`` methods:

.. code-block:: python

   # Instead of checking for -1:
   try:
       health = world.get_component_or_raise(entity, Health)
       # Process health
   except ComponentNotFoundError:
       # Handle missing component
       pass

Type Safety
~~~~~~~~~~~

PyECS uses beartype for runtime type checking. To disable it (e.g., for production):

.. code-block:: python

   import os
   os.environ["BEARTYPE_DISABLE"] = "1"
   
   # Must be set before importing pyecs
   from pyecs import ECSWorld

FAQ
---

**Q: Are entity IDs guaranteed to be sequential?**

A: No, entity IDs are managed internally and may have gaps.

**Q: Can I serialize/save the world state?**

A: PyECS doesn't provide built-in serialization. You'll need to implement custom save/load logic for your components.

**Q: Is PyECS thread-safe?**

A: No, PyECS is not thread-safe. Use it from a single thread or implement your own synchronization.

**Q: How do I handle parent-child relationships?**

A: Store parent/child entity IDs in components:

.. code-block:: python

   class Parent:
       def __init__(self, children=None):
           self.children = children or []
   
   class Child:
       def __init__(self, parent_id):
           self.parent_id = parent_id