from typing import Protocol

from src.apps.website.domain import Contact


class ContactRepository(Protocol):
    def list(self) -> tuple[Contact, ...]:
        ...
