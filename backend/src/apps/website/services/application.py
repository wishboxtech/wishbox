from dataclasses import asdict

from src.apps.website.dto import ContactOutputDTO, ListContactsInputDTO
from src.apps.website.interfaces import ContactRepository
from src.shared.domain.errors import NotFound


class WebsiteService:
    def __init__(self, repository: ContactRepository):
        self.repository = repository

    def list_contacts(self, dto: ListContactsInputDTO) -> tuple[ContactOutputDTO, ...]:
        contacts = self.repository.list()
        if not contacts:
            raise NotFound("ContactUs instance not found")
        return tuple(ContactOutputDTO(**asdict(contact)) for contact in contacts)
