from __future__ import annotations

from common.Types import Component, Entity
from containers.ComponentStorage import ComponentStorage


class Query(object):
    def __init__(self):
        self._with: set[type[Component]] = set()
        self._without: set[type[Component]] = set()

    def with_components(self, *types: type[Component]) -> Query:
        self._with.update(types)
        return self

    def without_components(self, *types: type[Component]) -> Query:
        self._without.update(types)
        return self

    def execute(self, storage: ComponentStorage) -> list[Entity]:
        matching: list[Entity] = []

        for mask, archetype in storage.archetypes.items():
            if self._with.issubset(mask) and not self._without.intersection(mask):
                matching.extend(archetype.entities)

        return matching
