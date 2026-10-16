# OpenAI Translate

[![PyPI version](https://badge.fury.io/py/openai-translate.svg)](https://pypi.org/project/openai-translate/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Translate text with OpenAI's ChatGPT Translate — no login, no API key required.

## Features

- No authentication or API keys needed
- Automatic source language detection
- 50+ languages supported
- Lightweight: only depends on `requests`

## Installation

```bash
pip install openai-translate
```

## Usage

```python
from openai_translate import OpenAITranslate

t = OpenAITranslate()

t.translate("Hello world", target="es", source="en")
# Hola mundo

t.translate("مرحبا بالعالم", target="en")
# Hello world (source auto-detected)

t.translate("Good morning", target="ar", source="en")
# صباح الخير
```

### `translate(text, target="en", source="detect")`

| Argument | Description                          | Default    |
|----------|--------------------------------------|------------|
| `text`   | Text to translate                    | —          |
| `target` | Target language code (e.g. `es`)     | `"en"`     |
| `source` | Source language code, or `"detect"`  | `"detect"` |

## How it works

The library replicates the public web flow of `chatgpt.com/translate`,
handling the session bootstrap and request handshake automatically —
everything is extracted at runtime, nothing for you to configure.

## License

MIT
