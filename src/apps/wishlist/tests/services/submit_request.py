import faker
from django.test import TestCase

from src.apps.wishlist.models import ReservationRequest
from src.apps.wishlist.services import submit_request
from src.static import SerializerErrors
from src.utils.fakers import (AnonymousFriendFactory, ProfileFactory,
                              WishFactory)


class SubmitReservationRequestTestCase(TestCase):
    def setUp(self):
        self.fake = faker.Faker()
        self.profile = ProfileFactory()
        self.wish = WishFactory()
        self.anonymous_friend = AnonymousFriendFactory()

    def test_submit_reservation_request_valid_friend(self):
        """Should create a reservation request when valid friend data is given"""
        data = {
            "wish": self.wish.id,
            "friend": self.profile.profile_id,
        }

        created, reservation_data, errs = submit_request(data)

        self.assertTrue(created)
        self.assertIsInstance(reservation_data, ReservationRequest)
        self.assertEqual(reservation_data.wish, self.wish)
        self.assertEqual(reservation_data.friend, self.profile)
        self.assertEqual(errs, {})

    def test_submit_reservation_request_valid_anonymous_friend(self):
        """Should create a reservation request when valid anonymous_friend data is given"""
        data = {
            "wish": self.wish.id,
            "anonymous_friend": self.anonymous_friend.id,
        }

        created, reservation_data, errs = submit_request(data)

        self.assertTrue(created)
        self.assertIsInstance(reservation_data, ReservationRequest)
        self.assertEqual(reservation_data.wish, self.wish)
        self.assertEqual(reservation_data.anonymous_friend, self.anonymous_friend)
        self.assertEqual(errs, {})

    def test_submit_reservation_request_invalid_missing_fields(self):
        """Should fail when missing required fields"""
        data = {}

        created, reservation_data, errs = submit_request(data)

        self.assertFalse(created)
        self.assertIsNone(reservation_data)
        self.assertIn("errors", errs)
        self.assertIn("error_type", errs)

        expected_error_types = [
            SerializerErrors.ReservationRequest.errors.get("wish"),
        ]
        self.assertTrue(any(e in expected_error_types for e in errs["error_type"]))

    def test_submit_reservation_request_invalid_field_type(self):
        """Should fail when invalid field types are provided"""
        data = {
            "wish": "not-an-id",
            "friend": "invalid-id",
        }

        created, reservation_data, errs = submit_request(data)

        self.assertFalse(created)
        self.assertIsNone(reservation_data)
        self.assertIn("errors", errs)
        self.assertIn("error_type", errs)

        expected_error_types = [
            SerializerErrors.ReservationRequest.errors.get("wish"),
            SerializerErrors.ReservationRequest.errors.get("friend"),
        ]
        self.assertEqual(sorted(errs["error_type"]), sorted(expected_error_types))
