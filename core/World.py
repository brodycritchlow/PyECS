from typing import Literal

from common.Types import Component, Entity
from containers.ComponentStorage import ComponentStorage
from helpers.Statuses import StatusCodes
from managers.EntityManager import EntityManager
from managers.SystemManager import SystemManager
from processing.System import System


class ECSWorld(object):
    def __init__(self):
        self.entity_manager: EntityManager = EntityManager()
        self.component_storage: ComponentStorage = ComponentStorage()
        self.system_manager: SystemManager = SystemManager()

    def create_entity(self) -> Entity | Literal[StatusCodes.FAILURE]:
        """
        Create a new entity in the ECS world.

        This method generates a unique entity identifier and registers it
        with both the entity manager and component storage system.

        Returns the new entity UUID on success, or FAILURE if entity
        creation fails.
        """
        result = self.entity_manager.create_entity()
        if isinstance(result, tuple):
            entity = result[1]
            empty_mask: frozenset[type] = frozenset()

            if empty_mask not in self.component_storage.archetypes:
                from containers.Archetype import Archetype

                self.component_storage.archetypes[empty_mask] = Archetype()

            self.component_storage.entity_to_archetype[entity] = empty_mask
            return entity
        return result

    def destroy_entity(self, entity: Entity) -> None:
        """
        Remove an entity and all its components from the world.

        This method removes the entity from the entity manager and cleans up
        all associated component data from the component storage system.

        The entity becomes invalid after this operation and should not be
        used in subsequent operations.
        """
        result = self.entity_manager.destroy_entity(entity)
        if result == StatusCodes.ENTITY_DESTROYED:
            self.component_storage.remove_entity(entity)

    def add_component(self, entity: Entity, component: Component) -> None:
        """
        Add a component to an existing entity.

        This method attaches the specified component to the entity, potentially
        moving the entity to a different archetype based on its new component set.

        Only adds the component if the entity is currently alive in the world.
        """
        if self.entity_manager.is_alive(entity):
            self.component_storage.add_component(entity, component)

    def remove_component(self, entity: Entity, component_type: type[Component]) -> None:
        """
        Remove a component type from an entity.

        This method detaches the specified component type from the entity,
        potentially moving the entity to a different archetype.

        Only removes the component if the entity is currently alive in the world.
        """
        if self.entity_manager.is_alive(entity):
            self.component_storage.remove_component(entity, component_type)

    def get_component(
        self, entity: Entity, component_type: type[Component]
    ) -> Component | Literal[StatusCodes.FAILURE]:
        """
        Retrieve a specific component from an entity.

        This method returns the component instance of the specified type
        attached to the entity.

        Returns the component instance if found, or FAILURE if the entity
        doesn't exist or doesn't have the specified component type.
        """
        if self.entity_manager.is_alive(entity):
            return self.component_storage.get_component(entity, component_type)
        return StatusCodes.FAILURE

    def add_system(self, system: System) -> None:
        """
        Register a system with the world.

        This method adds the system to the world's execution pipeline and
        calls the system's init method to perform any necessary setup.

        The system will be executed during subsequent world update cycles.
        """
        result = self.system_manager.register_system(system)
        if isinstance(result, tuple):
            system.init(self)

    def remove_system(self, system: System) -> None:
        """
        Unregister a system from the world.

        This method calls the system's cleanup method to release resources
        and removes it from the world's execution pipeline.

        The system will no longer be executed during world update cycles.
        """
        system.cleanup(self)
        self.system_manager.remove_system(system)

    def update(self, dt: float) -> None:
        """
        Execute one update cycle for all registered systems.

        This method calls the update method on all registered systems in
        registration order, passing the delta time for frame-independent updates.

        This is typically called once per frame in the main game loop.
        """
        self.system_manager.update_all(self, dt)
