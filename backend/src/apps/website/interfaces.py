from typing import Protocol
from datetime import datetime

from src.apps.website.domain import Contact
from src.apps.website.dto.dashboard import UserMetricsDTO, WishMetricsDTO


class ContactRepository(Protocol):
    def list(self) -> tuple[Contact, ...]:
        ...


class UserMetricsReader(Protocol):
    def read(self, since: datetime, until: datetime) -> UserMetricsDTO:
        ...


class WishMetricsReader(Protocol):
    def read(self, since: datetime, until: datetime) -> WishMetricsDTO:
        ...
