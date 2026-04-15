# Orangic Python SDK

Python package for the Orangic API.

## Current Status

`orangic` is a pre-release placeholder package.

What that means right now:

- The package can be installed from PyPI.
- The public client surface is not implemented yet.
- Creating an `Orangic` client or calling helper functions raises `NotImplementedError`.

The current release exists to reserve the package name and provide a stable place for future updates.

## Installation

```bash
pip install orangic
```

## Current Behavior

The example below shows the current state of the package:

```python
import orangic

client = orangic.Orangic(api_key="your-api-key")
```

Running this raises `NotImplementedError` because the API client has not been released yet.

## What To Expect Later

Planned work includes:

- A usable API client
- Authentication support
- Streaming support
- Expanded documentation

## Links

- Website: https://orangic.tech
- Documentation: https://orangic.tech/docs
- PyPI: https://pypi.org/project/orangic/
- Support: support@orangic.tech

## Contributing

This repository is not ready for external contributions yet.

## License

MIT. See [LICENSE](LICENSE).
