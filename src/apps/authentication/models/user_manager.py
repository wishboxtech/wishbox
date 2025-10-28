from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, phone_number=None, email=None, **extra_fields):
        """
        Create and save a user with the given username, and password.
        """
        if not (phone_number or email):
            raise ValueError("Phone number or email must be set")
        if phone_number:
            user = self.model(phone_number=phone_number, **extra_fields)
        elif email:
            user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if not (phone_number or email):
            raise ValueError("User must have phone_number or email")
        return self._create_user(
            phone_number=phone_number, email=email, password=password, **extra_fields
        )

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("type", "AD")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(phone_number, password, **extra_fields)
