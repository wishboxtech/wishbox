from collections.abc import Callable
from contextlib import AbstractContextManager
from typing import Protocol


class TransactionBoundary(Protocol):
    """A factory gives each execution its own transaction context."""

    def __call__(self) -> AbstractContextManager[None]: ...


class AfterCommit(Protocol):
    def __call__(self, callback: Callable[[], None]) -> None: ...
