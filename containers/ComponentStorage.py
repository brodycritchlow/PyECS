from typing import Literal
from common.Types import UUID4, Component, Entity, SuccessOrFailure
from containers.Archetype import Archetype
from helpers.Statuses import StatusCodes

class ComponentStorage(object):
    def __init__(self):
        self.archetypes: dict[frozenset[type], Archetype] = {}
        self.entity_to_archetype: dict[UUID4, UUID4] = {}

    def add_component(self, entity: Entity, component: Component) -> Literal[StatusCodes.COMPONENT_ADDED, StatusCodes.FAILURE]:
        # TODO: Implement add component logic
        ...

    def remove_component[T: Component](self, entity: Entity, component_type: type[T]) -> Literal[StatusCodes.COMPONENT_REMOVED, StatusCodes.FAILURE]:
        # TODO: Implement remove component logic
        ...
    
    def get_component[T: Component](self, entity: Entity, component_type: type[T]) -> Component:
        # TODO: Implement get component logic
        ...
    
    def has_component[T: Component](self, entity: Entity, component_type: type[T]) -> bool:
        # TODO: Implement has component logic
        ...

    def move_entity_to_archetype(self, entity: Entity, new_mask: frozenset[type]) -> SuccessOrFailure:
        # TODO: Implement move entity to archetype logic
        ...

    def remove_entity(self, entity: Entity) -> SuccessOrFailure: 
        # TODO: Implement remove entity logic
        ...