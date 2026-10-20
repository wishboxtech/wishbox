from src.apps.website.domain import Contact
from src.apps.website.models import ContactUs


class DjangoContactRepository:
    def list(self):
        return tuple(
            Contact(
                id=item.id,
                email=item.email,
                created_at=item.created_at,
                updated_at=item.updated_at,
            )
            for item in ContactUs.objects.order_by("created_at", "id")
        )
