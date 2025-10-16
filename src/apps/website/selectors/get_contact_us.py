from src.apps.website.models import ContactUs
from src.utils.exceptions import NotFoundException


def get_contact_us():
    contact_us = ContactUs.objects.first()
    if not contact_us:
        raise NotFoundException(
            {"detail": "ContactUs instance not found"}, [["not_found"]]
        )
    return contact_us
