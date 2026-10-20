from src.apps.authentication.dto import TokensOutputDTO
from src.apps.authentication.repositories.token_functions import login_by_id, refresh


class CachedTokenIssuer:
    def issue(self, user_id):
        return TokensOutputDTO(**login_by_id(user_id))

    def refresh(self, token):
        access, refresh_token = refresh(token)
        return TokensOutputDTO(access_token=access, refresh_token=refresh_token)
