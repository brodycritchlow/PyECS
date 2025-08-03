from typing import Literal

from pyecs.helpers.Statuses import StatusCodes

type UUID4 = str
type Entity = UUID4
type Component = object
type SuccessOrFailure = Literal[StatusCodes.SUCCESS, StatusCodes.FAILURE]
