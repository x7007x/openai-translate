import base64
import json
import time
import uuid

import requests


class OpenAITranslate:
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    BASE = "https://chatgpt.com"
    def __init__(self):
        self.s = requests.Session()
        self.s.headers.update({
            "User-Agent": self.UA,
            "Origin": self.BASE,
            "Referer": self.BASE + "/translate/",
        })

    @staticmethod
    def _fnv(s):
        e = 2166136261
        for ch in s:
            e ^= ord(ch)
            e = (e * 16777619) & 0xFFFFFFFF
        e ^= e >> 16
        e = (e * 2246822507) & 0xFFFFFFFF
        e ^= e >> 13
        e = (e * 3266489909) & 0xFFFFFFFF
        e ^= e >> 16
        return format(e & 0xFFFFFFFF, "08x")

    @staticmethod
    def _b64json(o):
        return base64.b64encode(json.dumps(o, separators=(",", ":"), ensure_ascii=False).encode()).decode()

    @classmethod
    def _config(cls):
        return [3000, "Fri Oct 16 2026 23:10:00 GMT+0200", 1792191746000.5, 0, cls.UA,
                "https://chatgpt.com/cdn/assets/entry.client.js", "20260219f9f6",
                "en-US", "en-US,en", 0, "webdriver-function", "hidden", "location",
                1234.5, str(uuid.uuid4()), "", 8, {"totalJSHeapSize": 1000000},
                0, 0, 0, 0, 0, 0, 0]

    @classmethod
    def _solve_pow(cls, seed, difficulty):
        cfg = cls._config()
        t0 = time.time()
        n = len(difficulty)
        for attempt in range(500000):
            cfg[3] = attempt
            cfg[9] = round((time.time() - t0) * 1000)
            b = cls._b64json(cfg)
            if cls._fnv(seed + b)[:n] <= difficulty:
                return "gAAAAAB" + b + "~S"
        raise RuntimeError("proof-of-work failed")

    def _handshake(self):
        self.s.get(self.BASE + "/translate/", timeout=30)
        c = self._config()
        c[3] = 1
        c[9] = 1
        prep = self.s.post(self.BASE + "/backend-api/sentinel/chat-requirements/prepare",
                           json={"p": "gAAAAAC" + self._b64json(c)}, timeout=30).json()
        self._prepare_token = prep["prepare_token"]
        self._proof = self._solve_pow(prep["proofofwork"]["seed"], prep["proofofwork"]["difficulty"])
        fin = self.s.post(self.BASE + "/backend-api/sentinel/chat-requirements/finalize",
                          json={"prepare_token": self._prepare_token,
                                "proofofwork": self._proof}, timeout=30).json()
        if not fin.get("token"):
            raise RuntimeError("handshake failed")
        self._token = fin["token"]

    def _stream(self, text, target, source):
        payload = {
            "text": text,
            "sourceLanguageCode": source,
            "targetLanguageCode": target,
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "OAI-Device-Id": self.s.cookies.get("oai-did", ""),
            "OAI-Session-Id": str(uuid.uuid4()),
            "OpenAI-Sentinel-Chat-Requirements-Token": self._token,
            "OpenAI-Sentinel-Proof-Token": self._proof,
        }
        return self.s.post(self.BASE + "/backend-anon/translate/stream", json=payload,
                           headers=headers, timeout=90, stream=True)

    @staticmethod
    def _read_deltas(response):
        out = []
        for line in response.iter_lines(decode_unicode=True):
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            try:
                out.append(json.loads(data).get("delta", ""))
            except ValueError:
                pass
        return "".join(out)

    def translate(self, text, target="en", source="detect"):
        self._handshake()
        r = self._stream(text, target, source)
        if r.status_code == 403:
            self._handshake()
            r = self._stream(text, target, source)
        if r.status_code != 200:
            raise RuntimeError(f"translate failed ({r.status_code})")
        return self._read_deltas(r)


if __name__ == "__main__":
    t = OpenAITranslate()
    print(t.translate("Hello world, how are you today?", target="es", source="en"))
    print(t.translate("مرحبا بالعالم، كيف حالك اليوم؟", target="en"))
    print(t.translate("Good morning", target="ar", source="en"))
