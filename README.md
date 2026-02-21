# Orangic Python SDK

The official Python library for the Orangic API.

## Installation

```bash
pip install orangic
```

## Quick Start

```python
import orangic

client = orangic.Orangic(api_key="your-api-key")

response = client.chat.completions.create(
    model="org-1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
)

print(response.content)
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
    base_url="https://custom.orangic.chat"
)
```

## Usage Examples

### Basic Chat Completion

```python
import orangic

client = orangic.Orangic()

response = client.chat.completions.create(
    model="org-1",
    messages=[
        {"role": "user", "content": "Tell me a joke"}
    ]
)

print(response.content)
```

### Streaming Responses

```python
import orangic

client = orangic.Orangic()

stream = client.chat.completions.create(
    model="org-1",
    messages=[{"role": "user", "content": "Write a story"}],
    stream=True
)

for chunk in stream:
    if chunk.channel == "final" and chunk.content:
        print(chunk.content, end="", flush=True)
```

### Streaming with Reasoning (Narrative Channel)

When `reasoning > 0`, the model may emit `"narrative"` chunks — visible commentary on its thinking process.

```python
stream = client.chat.completions.create(
    model="org-1",
    messages=[{"role": "user", "content": "Solve: if a train leaves at 3pm..."}],
    stream=True,
    reasoning=3  # medium reasoning
)

for chunk in stream:
    if chunk.channel == "narrative":
        print(f"[thinking] {chunk.content}", end="", flush=True)
    elif chunk.channel == "final":
        print(chunk.content, end="", flush=True)
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
    model="org-1",
    messages=messages
)

print(response.content)
```

### Advanced Parameters

```python
response = client.chat.completions.create(
    model="org-1",
    messages=[{"role": "user", "content": "Explain quantum computing"}],
    temperature=0.7,
    max_tokens=500,
    top_p=0.9,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    stop=["END"]
)
```

### Reasoning

The `reasoning` parameter controls how much the model thinks before responding. Reasoning tokens are **not billed**.

```python
response = client.chat.completions.create(
    model="org-1",
    messages=[{"role": "user", "content": "A farmer has 17 sheep. All but 9 die. How many are left?"}],
    reasoning=4  # or "high"
)

print(response.content)
```

| Value | String  | Behavior                                     |
|-------|---------|----------------------------------------------|
| `0`   | `"off"` | No reasoning. Fastest. Default.              |
| `1`   | `"auto"`| Model decides how much reasoning to use.     |
| `2`   | `"low"` | Light reasoning before responding.           |
| `3`   | `"medium"` | Balanced. Good for code and analysis.     |
| `4`   | `"high"`| Deep step-by-step analysis. Best for math.  |

### Quick Completion (No Client Instance)

```python
import orangic

response = orangic.completion(
    model="org-1",
    messages=[{"role": "user", "content": "Hello"}],
    api_key="your-api-key"
)

print(response.content)
```

## Error Handling

```python
import orangic

client = orangic.Orangic()

try:
    response = client.chat.completions.create(
        model="org-1",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.content)
except orangic.AuthenticationError as e:
    print(f"Authentication failed: {e}")
except orangic.RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except orangic.APIError as e:
    print(f"API error {e.status_code}: {e}")
```

## API Reference

### Client Initialization

```python
Orangic(
    api_key: Optional[str] = None,
    base_url: str = "https://api.orangic.chat",
    timeout: float = 600.0,
    max_retries: int = 2
)
```

### Chat Completions

```python
client.chat.completions.create(
    model: str,                              # "org-1"
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    top_p: Optional[float] = None,
    frequency_penalty: float = 0.0,
    presence_penalty: float = 0.0,
    stop: Optional[Union[str, List[str]]] = None,
    stream: bool = False,
    reasoning: Optional[Union[int, str]] = None  # 0-4 or "off"/"auto"/"low"/"medium"/"high"
)
```

### Response Object

```python
response.content        # str — the model's reply
response.id             # str — completion ID
response.model          # str — model used
response.finish_reason  # str — "stop" or "tool_calls"
response.usage          # dict — {"prompt_tokens": ..., "completion_tokens": ..., "total_tokens": ...}
```

### Streaming Chunk

```python
chunk.content   # str — token text
chunk.channel   # str — "final" (response) or "narrative" (thinking commentary)
```

## Requirements

- Python 3.8+
- httpx >= 0.24.0

## License

MIT License

## Support

For support, email support@orangic.chat or visit https://orangic.chat/docs
