from typing import Protocol

from core.World import ECSWorld


class System(Protocol):
    @property
    def required_components(self) -> set[type]:
        """
        Define which component types this system requires.

        Systems will only process entities that have ALL of the specified
        component types. This allows the world to efficiently query and
        cache relevant entities for each system.

        Returns a set of component types that entities must have to be
        processed by this system.
        """
        ...

    def init(self, world: ECSWorld) -> None:
        """
        Initialize the system when added to the world.

        This method is called once when the system is registered with the world.
        Use it to set up resources, caches, event subscriptions, or perform any
        one-time initialization required by the system.

        The world parameter provides access to entity queries, component storage,
        and other world systems for initial setup.
        """
        ...

    def update(self, world: ECSWorld, dt: float) -> None:
        """
        Process system logic for the current frame.

        This method is called every frame by the world's update loop. It should
        contain the core logic of the system, typically querying entities with
        specific component combinations and updating their state.

        The dt parameter represents delta time in seconds since the last frame,
        enabling frame-rate independent updates for physics and animations.
        """
        ...

    def cleanup(self, world: ECSWorld) -> None:
        """
        Clean up system resources when removed from the world.

        This method is called when the system is unregistered from the world or
        when the world is shutting down. Use it to release resources, close
        connections, unsubscribe from events, and perform proper cleanup.

        Proper cleanup prevents memory leaks and ensures graceful shutdown of
        system resources.
        """
        ...
