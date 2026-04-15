"""Top-level package for the Orangic Python SDK."""

from .client import (
    Orangic,
    OrangicError,
    completion,
    __version__,
)

__all__ = [
    "Orangic",
    "OrangicError",
    "completion",
    "__version__",
]

print(
    "Orangic is a pre-release package. "
    "Client functionality is not implemented yet. "
    "See https://orangic.tech for updates."
)
