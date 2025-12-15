# Orangic Python SDK

The official Python library for the Orangic API.

## Installation

```bash
pip install orangic
```

## Quick Start

```python
import orangic

# Initialize the client
client = orangic.Orangic(api_key="your-api-key")

# Create a chat completion
response = client.chat.completions.create(
    model="orangic-1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.choices[0].message["content"])
```

## Configuration

### API Key

Set your API key in one of two ways:

1. **Environment variable** (recommended):
```bash
export ORANGIC_API_KEY='your-api-key'
```

2. **Direct initialization**:
```python
client = orangic.Orangic(api_key="your-api-key")
```

### Custom Base URL

```python
client = orangic.Orangic(
    api_key="your-api-key",
    base_url="https://custom.orangic.tech"
)
```

## Usage Examples

### Basic Chat Completion

```python
import orangic

client = orangic.Orangic()

response = client.chat.completions.create(
    model="orangic-1",
    messages=[
        {"role": "user", "content": "Tell me a joke"}
    ]
)

print(response.choices[0].message["content"])
```

### Streaming Responses

```python
import orangic

client = orangic.Orangic()

stream = client.chat.completions.create(
    model="orangic-1",
    messages=[{"role": "user", "content": "Write a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.get("content"):
        print(chunk.choices[0].delta["content"], end="")
```

### Using Message Objects

```python
import orangic

client = orangic.Orangic()

messages = [
    orangic.Message(role="system", content="You are a helpful assistant"),
    orangic.Message(role="user", content="Hello!")
]

response = client.chat.completions.create(
    model="orangic-1",
    messages=messages
)
```

### Advanced Parameters

```python
response = client.chat.completions.create(
    model="orangic-1",
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    temperature=0.7,
    max_tokens=500,
    top_p=0.9,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    stop=["END"]
)
```

### Quick Completion (No Client Instance)

```python
import orangic

response = orangic.completion(
    model="orangic-1",
    messages=[{"role": "user", "content": "Hello"}],
    api_key="your-api-key"
)
```

### List Available Models

```python
import orangic

client = orangic.Orangic()

models = client.models.list()
print(models)
```

### Get Specific Model Info

```python
model_info = client.models.retrieve("orangic-1")
print(model_info)
```

## Error Handling

```python
import orangic

client = orangic.Orangic()

try:
    response = client.chat.completions.create(
        model="orangic-1",
        messages=[{"role": "user", "content": "Hello"}]
    )
except orangic.AuthenticationError as e:
    print(f"Authentication failed: {e}")
except orangic.RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except orangic.APIError as e:
    print(f"API error: {e}")
```

## API Reference

### Client Initialization

```python
Orangic(
    api_key: Optional[str] = None,
    base_url: str = "https://api.orangic.tech",
    timeout: float = 600.0,
    max_retries: int = 2
)
```

### Chat Completions

```python
client.chat.completions.create(
    model: str,
    messages: List[Dict[str, str]],
    temperature: float = 1.0,
    max_tokens: Optional[int] = None,
    top_p: float = 1.0,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stop: Optional[Union[str, List[str]]] = None,
    stream: bool = False
)
```

### Models

```python
# List all models
client.models.list()

# Get specific model
client.models.retrieve(model: str)
```

## Requirements

- Python 3.8+
- httpx >= 0.24.0

## License

MIT License

## Support

For support, email support@orangic.tech or visit https://orangic.tech/docs