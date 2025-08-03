from typing import Literal

from pyecs.common.Types import UUID4, Component, Entity, SuccessOrFailure
from pyecs.containers.Archetype import Archetype
from pyecs.helpers.Statuses import StatusCodes


class ComponentStorage(object):
    def __init__(self):
        self.archetypes: dict[frozenset[type], Archetype] = {}
        self.entity_to_archetype: dict[UUID4, frozenset[type]] = {}

    def add_component(
        self, entity: Entity, component: Component
    ) -> Literal[StatusCodes.COMPONENT_ADDED, StatusCodes.COMPONENT_UPDATED, StatusCodes.FAILURE]:
        """
        Add or update a component for an entity.

        If the component type doesn't exist on the entity, adds it and transitions
        the entity to a new archetype. If the component type already exists,
        updates the existing component in place.

        Returns COMPONENT_ADDED for new components, COMPONENT_UPDATED for existing
        components, or FAILURE if the entity doesn't exist.
        """
        if entity not in self.entity_to_archetype:
            return StatusCodes.FAILURE

        mask: frozenset[type] = self.entity_to_archetype[entity]
        current_archetype: Archetype = self.archetypes[mask]

        if component.__class__ not in mask:
            new_mask: frozenset[type] = mask | {component.__class__}

            components: list[Component] = self.get_entity_components(entity)
            components.append(component)

            self.move_entity_to_archetype(entity, new_mask, components)

            return StatusCodes.COMPONENT_ADDED
        else:
            entity_index = current_archetype.entities.index(entity)
            current_archetype.components[component.__class__][entity_index] = component
            return StatusCodes.COMPONENT_UPDATED

    def remove_component[T: Component](
        self, entity: Entity, component_type: type[T]
    ) -> Literal[StatusCodes.COMPONENT_REMOVED, StatusCodes.FAILURE]:
        """
        Remove a component type from an entity.

        Transitions the entity to a new archetype without the specified component.
        If this was the last component, removes the entity entirely.

        Returns COMPONENT_REMOVED on success, or FAILURE if the entity doesn't
        exist or doesn't have the specified component type.
        """
        if entity not in self.entity_to_archetype:
            return StatusCodes.FAILURE

        mask: frozenset[type] = self.entity_to_archetype[entity]
        current_archetype: Archetype = self.archetypes[mask]

        if component_type not in mask:
            return StatusCodes.FAILURE

        new_mask: frozenset[type] = mask - {component_type}

        if new_mask:
            components: list[Component] = []
            for comp_type in mask:
                if comp_type != component_type:
                    comp = current_archetype.get_component(entity, comp_type)
                    components.append(comp)

            self.move_entity_to_archetype(entity, new_mask, components)

            return StatusCodes.COMPONENT_REMOVED
        else:
            self.remove_entity(entity)
            return StatusCodes.COMPONENT_REMOVED

    def get_component[T: Component](
        self, entity: Entity, component_type: type[T]
    ) -> Component | Literal[StatusCodes.FAILURE]:
        """
        Retrieve a specific component from an entity.

        Returns the component instance if found, or FAILURE if the entity
        doesn't exist or doesn't have the specified component type.
        """
        if entity not in self.entity_to_archetype:
            return StatusCodes.FAILURE

        mask: frozenset[type] = self.entity_to_archetype[entity]
        current_archetype: Archetype = self.archetypes[mask]

        if component_type not in mask:
            return StatusCodes.FAILURE

        return current_archetype.get_component(entity, component_type)

    def has_component[T: Component](self, entity: Entity, component_type: type[T]) -> bool:
        """
        Check if an entity has a specific component type.

        Returns True if the entity exists and has the component type,
        False otherwise.
        """
        if entity not in self.entity_to_archetype:
            return False
        mask: frozenset[type] = self.entity_to_archetype[entity]
        return component_type in mask

    def move_entity_to_archetype(
        self, entity: Entity, new_mask: frozenset[type], components: list[Component] | None = None
    ) -> SuccessOrFailure:
        """
        Move an entity to a different archetype.

        Handles the transition of an entity between archetypes when components
        are added or removed. Creates the target archetype if it doesn't exist.

        Returns SUCCESS after moving the entity to the new archetype.
        """
        if entity in self.entity_to_archetype:
            current_mask = self.entity_to_archetype[entity]
            current_archetype = self.archetypes[current_mask]

            if components is None:
                components = self.get_entity_components(entity)

            current_archetype.remove_entity(entity)
        else:
            if components is None:
                components = []

        if new_mask not in self.archetypes:
            self.archetypes[new_mask] = Archetype()

        target_archetype = self.archetypes[new_mask]
        target_archetype.add_entity(entity, components)

        self.entity_to_archetype[entity] = new_mask

        return StatusCodes.SUCCESS

    def remove_entity(self, entity: Entity) -> SuccessOrFailure:
        """
        Remove an entity and all its components from storage.

        Removes the entity from its current archetype and clears all
        component data associated with it.

        Returns SUCCESS on removal, or FAILURE if the entity doesn't exist.
        """
        if entity not in self.entity_to_archetype:
            return StatusCodes.FAILURE

        mask: frozenset[type] = self.entity_to_archetype[entity]
        archetype = self.archetypes[mask]
        archetype.remove_entity(entity)
        del self.entity_to_archetype[entity]

        return StatusCodes.SUCCESS

    def get_entity_components(self, entity: Entity) -> list[Component]:
        """
        Retrieve all components for an entity.

        Returns a list containing all component instances attached to the
        entity, in the order they appear in the archetype mask.
        """
        mask = self.entity_to_archetype[entity]
        archetype = self.archetypes[mask]

        components: list[Component] = []
        for component_type in mask:
            component: Component = archetype.get_component(entity, component_type)
            components.append(component)

        return components
