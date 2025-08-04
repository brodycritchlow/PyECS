from pyecs.helpers.Statuses import StatusCodes as StatusCodes
from typing import Literal

type UUID4 = str
type Entity = UUID4
type Component = object
type SuccessOrFailure = Literal[StatusCodes.SUCCESS, StatusCodes.FAILURE]
