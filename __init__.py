# ruff: noqa: E402
from beartype.claw import beartype_this_package

beartype_this_package()

from .managers.EntityManager import EntityManager
from .containers.ComponentStorage import ComponentStorage
from .containers.Archetype import Archetype
from .querying.Query import Query
from .core.World import ECSWorld
from .common.Types import UUID4, Entity, Component, SuccessOrFailure
from .helpers.Statuses import StatusCodes

__all__ = [
    'EntityManager',
    'ComponentStorage', 
    'Archetype',
    'Query',
    'ECSWorld',
    'UUID4',
    'Entity',
    'Component',
    'SuccessOrFailure',
    'StatusCodes',
]

__version__ = '0.1.0'