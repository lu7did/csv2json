"""Project-specific exceptions."""


class Csv2JsonError(Exception):
    """Base exception for the package."""


class InputValidationError(Csv2JsonError):
    """Raised when the input data or options are invalid."""


class ConversionRuntimeError(Csv2JsonError):
    """Raised when a conversion cannot be completed."""
