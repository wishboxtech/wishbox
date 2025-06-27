class BadRequestException(Exception):
    error_type = None
    message = None

    def __init__(self, message: dict, error_type: list):
        self.message = message
        self.error_type = error_type


class NotFoundException(Exception):
    error_type = None
    message = None

    def __init__(self, message: dict, error_type: list):
        self.message = message
        self.error_type = error_type


class Unauthorized(Exception):
    message = None

    def __init__(self, message):
        self.message = message
