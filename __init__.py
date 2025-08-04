import os
import warnings

if not os.environ.get("PYECS_DISABLE_WARNINGS"):
    warnings.filterwarnings("default", category=DeprecationWarning, module="pyecs")

if not os.environ.get("BEARTYPE_DISABLE"):
    from beartype.claw import beartype_this_package

    beartype_this_package()

from .common.Types import UUID4, Component, Entity, SuccessOrFailure
from .containers.Archetype import Archetype
from .containers.ComponentStorage import ComponentStorage
from .core.World import ECSWorld
from .helpers.Statuses import StatusCodes
from .managers.EntityManager import EntityManager
from .querying.Query import Query

__all__ = [
    "UUID4",
    "Archetype",
    "Component",
    "ComponentStorage",
    "ECSWorld",
    "Entity",
    "EntityManager",
    "Query",
    "StatusCodes",
    "SuccessOrFailure",
]

__version__ = "0.1.0"
