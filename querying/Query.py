from __future__ import annotations

from common.Types import Component, Entity
from containers.ComponentStorage import ComponentStorage


class Query(object):
    def with_components(self, *types: type[Component]) -> Query:
        # TODO: Implement proper query condition logic
        ...

    def without_components(self, *types: type[Component]) -> Query:
        # TODO: Implement proper query condition logic
        ...

    def execute(self, storage: ComponentStorage) -> list[Entity]:
        # TODO: Implement proper query execution logic
        ...
