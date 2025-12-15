"""
Orangic Python SDK

Example usage:
    import orangic

    client = orangic.Orangic(api_key="your-api-key")

    response = client.chat.completions.create(
        model="orangic-1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )

    print(response.choices[0].message)
"""

from .client import (
    Orangic,
    Message,
    ChatCompletion,
    ChatCompletionChunk,
    OrangicError,
    AuthenticationError,
    RateLimitError,
    APIError,
    completion,
    __version__,
)

__all__ = [
    "Orangic",
    "Message",
    "ChatCompletion",
    "ChatCompletionChunk",
    "OrangicError",
    "AuthenticationError",
    "RateLimitError",
    "APIError",
    "completion",
    "__version__",
]
