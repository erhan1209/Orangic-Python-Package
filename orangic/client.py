"""
Orangic Python SDK
A Python client library for the Orangic API
"""

import os
import json
import httpx
from typing import Optional, Dict, Any, List, Union, Iterator
from dataclasses import dataclass


__version__ = "1.0.0"


@dataclass
class OrangicError(Exception):
    """Base exception for Orangic API errors"""

    message: str
    status_code: Optional[int] = None

    def __str__(self):
        return f"{self.__class__.__name__}: {self.message}"


class AuthenticationError(OrangicError):
    """Raised when API key is invalid"""

    pass


class RateLimitError(OrangicError):
    """Raised when rate limit is exceeded"""

    pass


class APIError(OrangicError):
    """Raised for general API errors"""

    pass


class Message:
    """Represents a chat message"""

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_dict(self):
        return {"role": self.role, "content": self.content}


class Choice:
    """Represents a completion choice"""

    def __init__(self, data: Dict[str, Any]):
        self.index = data.get("index", 0)
        self.message = data.get("message", {})
        self.finish_reason = data.get("finish_reason")


class ChatCompletion:
    """Represents a chat completion response"""

    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id")
        self.object = data.get("object", "chat.completion")
        self.created = data.get("created")
        self.model = data.get("model")
        self.choices = [Choice(c) for c in data.get("choices", [])]
        self.usage = data.get("usage", {})


class ChatCompletionChunk:
    """Represents a streaming chat completion chunk"""

    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id")
        self.object = data.get("object", "chat.completion.chunk")
        self.created = data.get("created")
        self.model = data.get("model")
        self.choices = data.get("choices", [])


class Chat:
    """Chat completions API"""

    def __init__(self, client):
        self.client = client
        self.completions = ChatCompletions(client)


class ChatCompletions:
    """Chat completions endpoint"""

    def __init__(self, client):
        self.client = client

    def create(
        self,
        model: str,
        messages: List[Union[Dict[str, str], Message]],
        temperature: Optional[float] = 1.0,
        max_tokens: Optional[int] = None,
        top_p: Optional[float] = 1.0,
        frequency_penalty: Optional[float] = 0.0,
        presence_penalty: Optional[float] = 0.0,
        stop: Optional[Union[str, List[str]]] = None,
        stream: bool = False,
        **kwargs,
    ) -> Union[ChatCompletion, Iterator[ChatCompletionChunk]]:
        """Create a chat completion"""

        # Convert Message objects to dicts
        formatted_messages = []
        for msg in messages:
            if isinstance(msg, Message):
                formatted_messages.append(msg.to_dict())
            else:
                formatted_messages.append(msg)

        payload = {
            "model": model,
            "messages": formatted_messages,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stream": stream,
            **kwargs,
        }

        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        if stop is not None:
            payload["stop"] = stop

        if stream:
            return self._stream_completion(payload)
        else:
            response = self.client._request(
                "POST", "/v1/chat/completions", json=payload
            )
            return ChatCompletion(response)

    def _stream_completion(
        self, payload: Dict[str, Any]
    ) -> Iterator[ChatCompletionChunk]:
        """Stream chat completion chunks"""
        with httpx.stream(
            "POST",
            f"{self.client.base_url}/v1/chat/completions",
            json=payload,
            headers=self.client._headers(),
            timeout=self.client.timeout,
        ) as response:
            self.client._handle_error(response)

            for line in response.iter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data.strip() == "[DONE]":
                        break
                    try:
                        chunk_data = json.loads(data)
                        yield ChatCompletionChunk(chunk_data)
                    except json.JSONDecodeError:
                        continue



class Orangic:
    """Main Orangic API client"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.orangic.chat",
        timeout: float = 600.0,
        max_retries: int = 2,
    ):
        """
        Initialize the Orangic client

        Args:
            api_key: Your Orangic API key (or set ORANGIC_API_KEY env var)
            base_url: Base URL for the API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.api_key = api_key or os.environ.get("ORANGIC_API_KEY")
        if not self.api_key:
            raise AuthenticationError(
                "No API key provided. Set ORANGIC_API_KEY environment variable or pass api_key parameter."
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

        # Initialize API resources
        self.chat = Chat(self)

    def _headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"orangic-python/{__version__}",
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an API request"""
        url = f"{self.base_url}{endpoint}"
        headers = self._headers()

        with httpx.Client(timeout=self.timeout) as client:
            response = client.request(method, url, headers=headers, **kwargs)
            self._handle_error(response)
            return response.json()

    def _handle_error(self, response: httpx.Response):
        """Handle API errors"""
        if response.status_code < 400:
            return

        try:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", response.text)
        except:
            error_message = response.text

        if response.status_code == 401:
            raise AuthenticationError(error_message, response.status_code)
        elif response.status_code == 429:
            raise RateLimitError(error_message, response.status_code)
        else:
            raise APIError(error_message, response.status_code)


# Convenience function
def completion(
    model: str, messages: List[Dict[str, str]], api_key: Optional[str] = None, **kwargs
) -> ChatCompletion:
    """Quick completion without creating a client instance"""
    client = Orangic(api_key=api_key)
    return client.chat.completions.create(model=model, messages=messages, **kwargs)
