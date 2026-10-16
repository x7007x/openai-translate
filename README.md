# OpenAI Translate without login/keys

`translate.py` translates via OpenAI's ChatGPT Translate (`chatgpt.com/translate/`)
with plain `requests` — no login, no API key. Everything is auto-extracted at
runtime by replicating the page's own anonymous handshake (reverse-engineered
from its JS bundles).

## Request chain

1. `GET https://chatgpt.com/translate/` → cookies (`oai-did` device id, Cloudflare).
2. `POST https://chatgpt.com/backend-api/sentinel/chat-requirements/prepare`
   body `{"p": "gAAAAAC" + base64(JSON(fingerprint config))}`
   → `{prepare_token, proofofwork: {seed, difficulty}, turnstile, so}`.
3. Solve the proof-of-work in Python: FNV-1a-32 + fmix32 avalanche over
   `seed + base64(JSON(config))`, find config with
   `digest[:len(difficulty)] <= difficulty` (string compare, ~2.6% hit rate,
   solves in milliseconds). Answer = `"gAAAAAB" + base64(JSON(config)) + "~S"`.
4. `POST https://chatgpt.com/backend-api/sentinel/chat-requirements/finalize`
   body `{"prepare_token", "proofofwork": answer}` → `{token}` (persona
   `chatgpt-noauth`). Turnstile is listed as required but the translate
   endpoint accepts a valid PoW without it.
5. `POST https://chatgpt.com/translate/stream` with anonymous headers
   (`OAI-Language`, `OAI-Device-Id`, `x-openai-web-frontend: core_web`,
   `OAI-Client-Version`, `OAI-Client-Build-Number`, `OAI-Session-Id`) and body
   `{request: {sourceLanguageCode, targetLanguageCode, text, pipeline:
   "latency-optimized", ...}, sentinel: {chatReqToken, chatReqPrepareToken,
   turnstileToken: null, proofToken}}`.
   Response is SSE: `data: {"delta": "..."}` chunks, ends with `data: [DONE]`.

Notes: tokens are effectively single-use — a 403 triggers one automatic fresh
handshake + retry. `source="detect"` auto-detects the input language.

## Usage

```python
from openai_translate import OpenAITranslate

t = OpenAITranslate()
print(t.translate("Hello world", target="es", source="en"))
print(t.translate("مرحبا بالعالم", target="en"))  # source auto-detected
```

Install as a library:

```bash
pip install .
```

Or from PyPI (after a GitHub release is published):

```bash
pip install openai-translate
```

Publishing to PyPI uses an API token:

1. On pypi.org: Account settings → API tokens → create a token scoped to the
   `openai-translate` project
2. In this repo: Settings → Secrets and variables → Actions → add it as
   `PYPI_API_TOKEN`
3. Create a GitHub release — the workflow builds and publishes automatically
