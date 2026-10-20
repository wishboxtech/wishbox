"""The only place that assembles concrete application dependencies."""

from src.apps.wishlist.repositories.gifting import DjangoGiftRepository
from src.apps.wishlist.repositories.credentials import SecureGiftCredentials
from src.apps.wishlist.services.gifting import GiftingService
from src.apps.wishlist.services.guest import GuestClaimService
from src.apps.wishlist.repositories.guest import DjangoGuestRepository

from django.utils.timezone import now
from settings import UNDER_DEVELOPMENT
from src.apps.authentication.repositories.otp import CachedOTPRepository
from src.apps.authentication.repositories.tokens import CachedTokenIssuer
from src.apps.authentication.repositories.user import DjangoUserRepository
from src.apps.authentication.services import AuthenticationService
from src.apps.profile.repositories.profile import DjangoProfileRepository
from src.apps.profile.services import ProfileService
from src.apps.storage.repositories.media import DjangoMediaRepository
from src.apps.storage.services import StorageService
from src.apps.website.repositories.contact import DjangoContactRepository
from src.apps.website.services import WebsiteService
from src.apps.wishlist.repositories.wishlist import DjangoWishlistRepository
from src.apps.wishlist.services import WishlistService
from src.shared.transactions import after_commit, transaction_boundary
from src.utils.otp import send_sms_otp


def notify_otp(phone, code):
    if not UNDER_DEVELOPMENT:
        send_sms_otp(phone=phone, otp=code)


def authentication_service() -> AuthenticationService:
    return AuthenticationService(
        users=DjangoUserRepository(),
        otps=CachedOTPRepository(),
        tokens=CachedTokenIssuer(),
        notify=notify_otp,
        transaction=transaction_boundary,
        after_commit=after_commit,
        guest_claims=GuestClaimService(
            DjangoGuestRepository(), SecureGiftCredentials(), transaction_boundary
        ),
    )


def storage_service() -> StorageService:
    return StorageService(
        repository=DjangoMediaRepository(), transaction=transaction_boundary
    )


def profile_service() -> ProfileService:
    return ProfileService(
        repository=DjangoProfileRepository(),
        authentication=authentication_service(),
        storage=storage_service(),
        transaction=transaction_boundary,
    )


def wishlist_service() -> WishlistService:
    return WishlistService(
        repository=DjangoWishlistRepository(),
        profile=profile_service(),
        storage=storage_service(),
        transaction=transaction_boundary,
    )


def website_service() -> WebsiteService:
    return WebsiteService(repository=DjangoContactRepository())


def gifting_service():
    return GiftingService(
        repository=DjangoGiftRepository(DjangoWishlistRepository()),
        credentials=SecureGiftCredentials(),
        wishlists=wishlist_service(),
        profiles=profile_service(),
        transaction=transaction_boundary,
        clock=now,
    )
