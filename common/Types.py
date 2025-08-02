from typing import Literal
from helpers.Statuses import StatusCodes

type UUID4 = str
type Entity = UUID4
type Component = object
type OperationResult = Literal[StatusCodes.SUCCESS, StatusCodes.FAILURE]