class ApiException(Exception):
    def __init__(self, message: str, error_code: str, status_code: int = 400):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationException(ApiException):
    def __init__(self, message: str):
        super().__init__(message, "VALIDATION_ERROR", 400)


class ProviderException(ApiException):
    pass


class ResourceNotFoundException(ApiException):
    pass
