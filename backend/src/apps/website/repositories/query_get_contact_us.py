from src.apps.website.models import ContactUs


def get_contact_us():
    return ContactUs.objects.first()
