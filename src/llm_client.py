from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Dict

from .config import ModelConfig


def _endpoint(model_name: str, api_key: str) -> str:
    return f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"


def generate_text(
    api_key: str,
    model: ModelConfig,
    prompt: str,
    response_mime_type: str = "text/plain",
    retries: int = 2,
    timeout_s: int = 30,
) -> Dict[str, object]:
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": model.temperature,
            "maxOutputTokens": model.max_output_tokens,
            "responseMimeType": response_mime_type,
        },
    }
    data = json.dumps(payload).encode("utf-8")

    last_err = None
    for attempt in range(retries + 1):
        start = time.time()
        req = urllib.request.Request(
            _endpoint(model.name, api_key),
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout_s) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            text = (
                body.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
                .strip()
            )
            latency_ms = int((time.time() - start) * 1000)
            return {"text": text, "latency_ms": latency_ms, "raw": body}
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            last_err = exc
            if attempt < retries:
                time.sleep(0.8 * (attempt + 1))
                continue
            raise RuntimeError(f"Gemini API request failed: {exc}") from exc
    raise RuntimeError(f"Gemini API request failed: {last_err}")
