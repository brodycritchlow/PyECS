from collections.abc import Iterator
from common.Types import UUID4, Component, Entity

class Archetype(object):
    def __init__(self):
        self.entities: list[UUID4] = []
        self.components: list[list[Component]] = []

    def add_entity(self, entity: Entity, components: list[Component]):
        # TODO: Implement proper add entity logic
        ...

    def remove_entity(self, entity: Entity):
        # TODO: Implement proper remove entity logic
        ...

    def get_component[T: Component](self, entity: Entity, component_type: type[T]) -> list[T]:
        # TODO: Implement proper component retrieval by type
        return []

    def iter_entities(self) -> Iterator[Entity]:
        return iter(self.entities)

    def iter_components(self, component_type: type) -> Iterator[Component]:
        # TODO: Implement proper filtering by component type
        for component_list in self.components:
            for component in component_list:
                yield component


    