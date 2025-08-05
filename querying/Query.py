from __future__ import annotations

from typing import overload

from pyecs.common.Types import Component, Entity
from pyecs.containers.ComponentStorage import ComponentStorage
from pyecs.core.World import ECSWorld
from pyecs.helpers.Deprecation import warn_deprecated


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

    @overload
    def execute(self, storage_or_world: ComponentStorage) -> list[Entity]: ...

    @overload
    def execute(self, storage_or_world: ECSWorld) -> list[Entity]: ...

    def execute(self, storage_or_world: ComponentStorage | ECSWorld) -> list[Entity]:
        """Execute the query on either a ComponentStorage or ECSWorld instance."""
        if isinstance(storage_or_world, ComponentStorage):
            warn_deprecated(
                "Passing ComponentStorage directly is deprecated",
                use_instead="query.execute(world)",
            )
            storage = storage_or_world
        else:
            storage = storage_or_world.component_storage

        matching: list[Entity] = []

        for mask, archetype in storage.archetypes.items():
            if self._with.issubset(mask) and not self._without.intersection(mask):
                matching.extend(archetype.entities)

        return matching
