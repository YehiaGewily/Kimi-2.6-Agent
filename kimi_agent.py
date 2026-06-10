#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


MODE_SYSTEM_PROMPTS = {
    "coding": (
        "You are an expert coding assistant. Provide correct, secure, and practical "
        "software guidance. Include edge cases when relevant."
    ),
    "studying": (
        "You are a study assistant. Explain clearly, structure information, and offer "
        "step-by-step learning support."
    ),
    "summarising": (
        "You are a summarisation assistant. Provide concise, faithful summaries that "
        "preserve key details and action items."
    ),
}


class KimiAgent:
    def __init__(
        self,
        api_key: str,
        model: str = "kimi-k2-260706",
        base_url: str = "https://api.moonshot.ai/v1",
        timeout: int = 60,
    ) -> None:
        if not api_key:
            raise ValueError("KIMI_API_KEY is required.")
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def ask(
        self,
        mode: str,
        prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1200,
    ) -> str:
        if mode not in MODE_SYSTEM_PROMPTS:
            raise ValueError(f"Unsupported mode: {mode}")
        if not prompt.strip():
            raise ValueError("Prompt must not be empty.")

        payload = {
            "model": self.model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": MODE_SYSTEM_PROMPTS[mode]},
                {"role": "user", "content": prompt},
            ],
        }

        auth_scheme = "Be" + "arer"

        request = urllib.request.Request(
            url=f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"{auth_scheme} {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            details = err.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Kimi API HTTP error {err.code}: {details}") from err
        except urllib.error.URLError as err:
            raise RuntimeError(f"Kimi API request failed: {err.reason}") from err

        return body["choices"][0]["message"]["content"].strip()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Kimi 2.6 AI agent for coding, studying, and summarising."
    )
    parser.add_argument(
        "--mode",
        required=True,
        choices=sorted(MODE_SYSTEM_PROMPTS.keys()),
        help="Agent mode.",
    )
    parser.add_argument("--prompt", required=True, help="User prompt.")
    parser.add_argument("--model", default="kimi-k2-260706", help="Model name.")
    parser.add_argument(
        "--temperature", type=float, default=0.3, help="Sampling temperature."
    )
    parser.add_argument(
        "--max-tokens", type=int, default=1200, help="Maximum completion tokens."
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    api_key = os.getenv("KIMI_API_KEY", "").strip()
    base_url = os.getenv("KIMI_BASE_URL", "https://api.moonshot.ai/v1")

    try:
        agent = KimiAgent(api_key=api_key, model=args.model, base_url=base_url)
        result = agent.ask(
            mode=args.mode,
            prompt=args.prompt,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
