from django.utils.translation import gettext_lazy as _


class SerializerErrors:
    class CreateProfile:
        errors = {
            "profile": _("CREATE_PROFILE_SERIALIZER_INVALID_USERID"),
            "first_name": ("CREATE_PROFILE_SERIALZER_INALID_FIRST_NAME"),
            "last_name": _("CREATE_PROFILE_SERIALZER_INALID_LAST_NAME"),
            "birthdate": _("CREATE_PROFILE_SERIALZER_INALID_BIRTHDATE"),
            "bio": _("CREATE_PROFILE_SERIALZER_INALID_BIO"),
            "gender": _("CREATE_PROFILE_SERIALZER_INALID_GENDER"),
            "photo": _("CREATE_PROFILE_SERIALZER_INALID_PHOTO"),
        }

    class CreateWishlist:
        errors = {
            "name": _("CREATE_WISHLIST_SERIALZER_INVALID_NAME"),
            "description": _("CREATE_WISHLIST_SERIALIZER_INVALID_DESCRIPTION"),
            "cover": _("CREATE_WISHLIST_SERIALIZER_INVALID_COVER"),
        }
