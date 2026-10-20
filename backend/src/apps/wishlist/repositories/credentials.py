import hashlib
import secrets


class SecureGiftCredentials:
    def issue(self):
        return secrets.token_urlsafe(32)

    def digest(self, token):
        return hashlib.sha256(token.encode()).hexdigest()

    def matches(self, token, digest):
        return bool(token and digest) and secrets.compare_digest(
            self.digest(token), digest
        )
