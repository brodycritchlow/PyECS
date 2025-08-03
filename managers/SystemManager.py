from typing import Literal

from common.Types import UUID4
from helpers.Statuses import StatusCodes
from processing.System import System


class SystemManager(object):
    def __init__(self): ...

    def register_system(
        self, system: System
    ) -> tuple[Literal[StatusCodes.SYSTEM_REGISTERED], System] | Literal[StatusCodes.FAILURE]:
        # TODO: Implement system registration logic
        return StatusCodes.FAILURE

    def unregister_system(
        self, id: UUID4
    ) -> Literal[StatusCodes.SYSTEM_UNREGISTERED, StatusCodes.FAILURE]:
        # TODO: Implement system unregistration logic
        return StatusCodes.SYSTEM_UNREGISTERED
