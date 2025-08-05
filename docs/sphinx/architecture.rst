Architecture & Internals
========================

This section provides detailed flowcharts showing how PyECS components work internally.

Core Components
---------------

World Operations
~~~~~~~~~~~~~~~~

.. _world-create-entity:

create_entity
^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/World/create_entity.mermaid

create_entity_or_raise
^^^^^^^^^^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/World/create_entity_or_raise.mermaid

.. _world-get-component:

get_component
^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/World/get_component.mermaid

get_component_or_raise
^^^^^^^^^^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/World/get_component_or_raise.mermaid

get_components
^^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/World/get_components.mermaid

get_components_or_raise
^^^^^^^^^^^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/World/get_components_or_raise.mermaid

.. _world-add-component:

add_component
^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/World/add_component.mermaid

.. _world-remove-component:

remove_component
^^^^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/World/remove_component.mermaid

.. _world-destroy-entity:

destroy_entity
^^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/World/destroy_entity.mermaid

.. _world-add-system:

add_system
^^^^^^^^^^

.. mermaid:: ../../mermaid/World/add_system.mermaid

remove_system
^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/World/remove_system.mermaid

.. _world-update:

update
^^^^^^

.. mermaid:: ../../mermaid/World/update.mermaid

Query System
~~~~~~~~~~~~

Query Construction
^^^^^^^^^^^^^^^^^^

.. _query-with-components:

with_components
"""""""""""""""

.. mermaid:: ../../mermaid/Query/with_components.mermaid

without_components
""""""""""""""""""

.. mermaid:: ../../mermaid/Query/without_components.mermaid

.. _query-execute:

Query Execution
^^^^^^^^^^^^^^^

.. mermaid:: ../../mermaid/Query/execute.mermaid

Storage Layer
~~~~~~~~~~~~~

ComponentStorage Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

add_component
"""""""""""""

.. mermaid:: ../../mermaid/ComponentStorage/add_component.mermaid

remove_component
""""""""""""""""

.. mermaid:: ../../mermaid/ComponentStorage/remove_component.mermaid

get_component
"""""""""""""

.. mermaid:: ../../mermaid/ComponentStorage/get_component.mermaid

get_entity_components
"""""""""""""""""""""

.. mermaid:: ../../mermaid/ComponentStorage/get_entity_components.mermaid

has_component
"""""""""""""

.. mermaid:: ../../mermaid/ComponentStorage/has_component.mermaid

move_entity_to_archetype
""""""""""""""""""""""""

.. mermaid:: ../../mermaid/ComponentStorage/move_entity_to_archetype.mermaid

remove_entity
"""""""""""""

.. mermaid:: ../../mermaid/ComponentStorage/remove_entity.mermaid

.. _archetype-operations:

Archetype Operations
^^^^^^^^^^^^^^^^^^^^

add_entity
""""""""""

.. mermaid:: ../../mermaid/Archetype/add_entity.mermaid

remove_entity
"""""""""""""

.. mermaid:: ../../mermaid/Archetype/remove_entity.mermaid

get_component
"""""""""""""

.. mermaid:: ../../mermaid/Archetype/get_component.mermaid

iter_components
"""""""""""""""

.. mermaid:: ../../mermaid/Archetype/iter_components.mermaid

iter_entities
"""""""""""""

.. mermaid:: ../../mermaid/Archetype/iter_entities.mermaid

Entity Management
~~~~~~~~~~~~~~~~~

EntityManager Operations
^^^^^^^^^^^^^^^^^^^^^^^^

create_entity
"""""""""""""

.. mermaid:: ../../mermaid/EntityManager/create_entity.mermaid

destroy_entity
""""""""""""""

.. mermaid:: ../../mermaid/EntityManager/destroy_entity.mermaid

is_alive
""""""""

.. mermaid:: ../../mermaid/EntityManager/is_alive.mermaid

System Management
~~~~~~~~~~~~~~~~~

SystemManager Operations
^^^^^^^^^^^^^^^^^^^^^^^^

register_system
"""""""""""""""

.. mermaid:: ../../mermaid/SystemManager/register_system.mermaid

remove_system
"""""""""""""

.. mermaid:: ../../mermaid/SystemManager/remove_system.mermaid

unregister_system
"""""""""""""""""

.. mermaid:: ../../mermaid/SystemManager/unregister_system.mermaid

.. _systemmanager-update-all:

update_all
""""""""""

.. mermaid:: ../../mermaid/SystemManager/update_all.mermaid

Exception Handling
------------------

PyECS provides both safe (status code) and unsafe (exception-based) APIs for error handling.

Exception Hierarchy
~~~~~~~~~~~~~~~~~~~

.. mermaid:: ../../mermaid/Unsafe/exception_hierarchy.mermaid

Unsafe Decorator Flow
~~~~~~~~~~~~~~~~~~~~~

.. mermaid:: ../../mermaid/Unsafe/auto_unsafe_decorator.mermaid

Unsafe Method Execution
~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid:: ../../mermaid/Unsafe/unsafe_method_flow.mermaid
