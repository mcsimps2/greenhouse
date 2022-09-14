class ApiError(Exception):
    """Base class for other exceptions"""


class EntityNotFound(ApiError):
    """Raised when a specified entity does not exist in storage"""


class InvalidQuery(ApiError):
    """Raised when the query specified is invalid"""


class InvalidUsage(ApiError):
    """Not using a resource correctly"""


class EmptyUpdate(ApiError):
    """No updates to apply"""


class ForbiddenAccess(ApiError):
    """Trying to access resources without proper permissions"""


class Unauthorized(ApiError):
    """Incorrect credentials"""


class DataIntegrityError(ApiError):
    """Database has been corrupted, loss of integrity"""


class UnknownError(ApiError):
    """An unknown error has occured without a good way to solve it"""


class ConfigurationError(ApiError):
    """Incorrect or invalid configuration"""


class Duplicate(ApiError):
    """Duplicate entry"""


class Conflict(ApiError):
    """Conflict"""
