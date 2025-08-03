from collections.abc import Iterator
from typing import Literal

from common.Types import UUID4, Component, Entity, SuccessOrFailure
from helpers.Statuses import StatusCodes


class Archetype(object):
    def __init__(self):
        self.entities: list[UUID4] = []
        self.components: dict[type, list[Component]] = {}

    def add_entity(self, entity: Entity, components: list[Component]) -> SuccessOrFailure:
        """
        Add an entity and its components to this archetype.

        This method stores the entity and its components in parallel arrays,
        maintaining alignment between entity indices and component indices.

        Returns SUCCESS if the entity was added, or FAILURE if the entity
        already exists in this archetype.
        """
        if entity in self.entities:
            return StatusCodes.FAILURE

        self.entities.append(entity)
        entity_index = len(self.entities) - 1

        for component in components:
            comp_type: type[object] = component.__class__

            if comp_type not in self.components:
                self.components[comp_type] = [None] * entity_index

            self.components[comp_type].append(component)

        return StatusCodes.SUCCESS

    def remove_entity(self, entity: Entity) -> SuccessOrFailure:
        """
        Remove an entity and all its component data from this archetype.

        This method maintains the parallel array structure by removing the
        entity and its components from the same index across all arrays.

        Returns SUCCESS if the entity was removed, or FAILURE if the entity
        does not exist in this archetype.
        """
        if entity not in self.entities:
            return StatusCodes.FAILURE

        entity_index = self.entities.index(entity)

        self.entities.remove(entity)

        for _, comp_list in self.components.items():
            del comp_list[entity_index]

        return StatusCodes.SUCCESS

    def get_component(
        self, entity: Entity, component_type: type[Component]
    ) -> Component | Literal[StatusCodes.FAILURE]:
        """
        Retrieve a specific component for an entity.

        This method uses the parallel array structure to efficiently locate
        the requested component by finding the entity's index.

        Returns the component instance if found, or FAILURE if the entity
        doesn't exist or doesn't have the specified component type.
        """
        if entity not in self.entities:
            return StatusCodes.FAILURE

        entity_index = self.entities.index(entity)

        if component_type in self.components.keys():
            return self.components[component_type][entity_index]

        return StatusCodes.FAILURE

    def iter_entities(self) -> Iterator[Entity]:
        """
        Iterate over all entities in this archetype.

        This method provides direct iteration over the entities list,
        useful for systems that need to process all entities with a
        specific component combination.

        Returns an iterator over all entity UUIDs in this archetype.
        """
        return iter(self.entities)

    def iter_components(self, component_type: type) -> Iterator[Component]:
        """
        Iterate over all components of a specific type.

        This method yields all component instances of the requested type
        stored in this archetype, in the same order as their entities.

        Yields component instances if the archetype contains the specified
        component type, otherwise yields nothing.
        """
        if component_type in self.components:
            yield from self.components[component_type]
