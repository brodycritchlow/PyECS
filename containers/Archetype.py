from collections.abc import Iterator
from common.Types import UUID4, Component, Entity, SuccessOrFailure

class Archetype(object):
    def __init__(self):
        self.entities: list[UUID4] = []
        self.components: dict[type, list[Component]] = {}

    def add_entity(self, entity: Entity, components: list[Component]) -> SuccessOrFailure:
        # TODO: Implement proper add entity logic
        ...

    def remove_entity(self, entity: Entity) -> SuccessOrFailure:
        # TODO: Implement proper remove entity logic
        ...

    def get_component(self, entity: Entity, component_type: type[Component]) -> Component:
        # TODO: Implement proper component retrieval by type
        return []

    def iter_entities(self) -> Iterator[Entity]:
        return iter(self.entities)

    def iter_components(self, component_type: type) -> Iterator[Component]:
        # TODO: Implement proper filtering by component type
        if component_type in self.components:
            yield from self.components[component_type]