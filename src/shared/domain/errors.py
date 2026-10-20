class DomainError(Exception):
    """Business failure. HTTP status and translated messages belong to presentation."""

    code = "business_error"


class NotFound(DomainError):
    code = "not_found"


class DomainValidationError(DomainError):
    code = "invalid_data"

    def __init__(self, errors: dict[str, str]):
        self.errors = errors
        super().__init__(str(errors))
