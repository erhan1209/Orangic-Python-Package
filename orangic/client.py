"""Pre-release client surface for the Orangic Python SDK."""

__version__ = "0.1.0"


class OrangicError(Exception):
    """Base exception for Orangic API errors."""
    pass


class Orangic:
    """Main Orangic API client.

    This pre-release package reserves the project name on PyPI.
    The client is not implemented yet.
    """
    
    def __init__(self, api_key=None, base_url="https://api.orangic.tech", **kwargs):
        """Initialize the Orangic client placeholder."""
        raise NotImplementedError(
            "The Orangic Python client is not implemented yet. "
            "This pre-release package currently reserves the project name. "
            "See https://orangic.tech for updates."
        )


def completion(*args, **kwargs):
    """Placeholder completion helper."""
    raise NotImplementedError(
        "The Orangic Python client is not implemented yet. "
        "See https://orangic.tech for updates."
    )
