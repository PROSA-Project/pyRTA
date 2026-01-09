from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, eq=True, order=True)
class Deadline:
    "A real-time task's relative deadline parameter."

    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("deadline must be positive")


@dataclass(frozen=True, eq=True, order=True)
class Priority:
    """A real-time task's priority parameter.
    Larger values mean higher priority, as in Linux.
    """

    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("priority must be non-negative")
