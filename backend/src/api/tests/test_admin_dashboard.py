from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from src.apps.authentication.models import User
from src.apps.website.services.dashboard import DashboardService
from src.apps.wishlist.models import ReservationRequest, Wish
from src.core.composition import dashboard_service
from src.utils.fakers import ProfileFactory, UserFactory, WishFactory, WishlistFactory


class AdminDashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.now = datetime(2026, 10, 22, 12, tzinfo=timezone.utc)
        cls.admin = UserFactory(is_staff=True, is_superuser=True)
        cls.active = UserFactory(last_login=cls.now - timedelta(days=1))
        cls.old = UserFactory(last_login=cls.now - timedelta(days=31))
        cls.boundary = UserFactory(last_login=cls.now - timedelta(days=30))
        cls.disabled = UserFactory(is_active=False, last_login=cls.now)
        cls.staff = UserFactory(is_staff=True, last_login=cls.now)
        cls.admin_type = UserFactory(type=User.UserType.ADMIN, last_login=cls.now)
        cls.female = ProfileFactory(profile=cls.active, gender="female")
        cls.male = ProfileFactory(profile=cls.old, gender="male")
        cls.unknown = ProfileFactory(profile=cls.boundary, gender=None)
        cls.blank = ProfileFactory(profile=cls.disabled, gender="")
        cls.female_wishlist = WishlistFactory(profile=cls.female)
        cls.received = WishFactory(wishlist=cls.female_wishlist)
        ReservationRequest.objects.create(
            wish=cls.received,
            status="received",
            received_at=cls.now - timedelta(days=1),
        )
        # Repeated failed attempts must never inflate the denominator or completion count.
        for status in ("cancelled", "expired", "rejected"):
            ReservationRequest.objects.create(wish=cls.received, status=status)
        cls.open = WishFactory(wishlist=cls.female_wishlist)
        cls.purchased = WishFactory(wishlist=WishlistFactory(profile=cls.male))
        ReservationRequest.objects.create(wish=cls.purchased, status="purchased")
        cls.reserved = WishFactory(wishlist=WishlistFactory(profile=cls.unknown))
        ReservationRequest.objects.create(wish=cls.reserved, status="reserved")
        cls.legacy = WishFactory(wishlist=WishlistFactory(profile=cls.blank))
        ReservationRequest.objects.create(wish=cls.legacy, status="accepted")
        Wish.objects.all().update(created_at=cls.now - timedelta(days=2))

    def overview(self):
        service = dashboard_service()
        service.clock = lambda: self.now
        return service.overview()

    def test_aggregates_use_distinct_wishes_receipt_and_owner_gender(self):
        with self.assertNumQueries(5):
            result = self.overview()
        self.assertEqual(result.wishes.total, 5)
        self.assertEqual(result.wishes.fulfilled, 1)
        self.assertEqual(result.fulfillment_rate, 20.0)
        self.assertEqual(result.wishes.reserved, 1)
        self.assertEqual(result.wishes.purchased, 1)
        self.assertEqual(result.awaiting, 2)
        female, male, unknown = result.by_gender
        self.assertEqual((female.total, female.fulfilled, female.rate), (2, 1, 50.0))
        self.assertEqual((male.total, male.fulfilled, male.rate), (1, 0, 0.0))
        self.assertEqual((unknown.total, unknown.fulfilled), (2, 0))
        self.assertEqual(sum(day.created for day in result.daily), 5)
        self.assertEqual(sum(day.fulfilled for day in result.daily), 1)
        self.assertEqual(result.daily[-2].fulfilled, 1)

    def test_activity_is_recent_enabled_customers_not_staff_or_all_enabled(self):
        result = self.overview()
        self.assertEqual(result.users.total, 4)
        self.assertEqual(result.users.enabled, 3)
        self.assertEqual(result.users.active, 2)

    def test_empty_and_deleted_wishes_do_not_create_a_rate(self):
        Wish.objects.all().delete()
        result = self.overview()
        self.assertEqual(result.wishes.fulfilled, 0)
        self.assertIsNone(result.fulfillment_rate)
        self.assertEqual(sum(day.fulfilled for day in result.daily), 0)

    def test_anonymous_is_redirected_and_staff_cannot_access_aggregate_metrics(self):
        self.assertRedirects(
            self.client.get(reverse("admin:index")),
            reverse("admin:login") + "?next=" + reverse("admin:index"),
        )
        self.client.force_login(self.staff)
        with patch("src.api.admin_dashboard.dashboard_service") as factory:
            response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        factory.assert_not_called()
        self.assertNotContains(response, "Fulfillment by gender")

    def test_superuser_dashboard_renders_metrics_and_existing_admin_content(self):
        self.client.force_login(self.admin)
        with patch.object(DashboardService, "overview", return_value=self.overview()):
            response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fulfillment by gender")
        self.assertContains(response, "20.0")
        self.assertContains(response, "Not specified")
        self.assertContains(response, "View daily counts")
        self.assertContains(response, "dashboard.css")
