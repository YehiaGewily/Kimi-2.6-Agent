# Kimi-2.6-Agent

A full AI agent for coding, studying, and summarising using the **Kimi 2.6** model.

## Features

- **Coding mode**: code review, debugging help, refactoring suggestions, and implementation planning.
- **Studying mode**: structured learning guidance, concept breakdowns, and practice prompts.
- **Summarising mode**: concise summaries of long text while preserving key points.

## Setup

1. Export your API key:

   ```bash
   export KIMI_API_KEY="your_api_key_here"
   ```

2. (Optional) Set a custom base URL:

   ```bash
   export KIMI_BASE_URL="https://api.moonshot.ai/v1"
   ```

## Usage

Run:

```bash
python /home/runner/work/Kimi-2.6-Agent/Kimi-2.6-Agent/YehiaGewily/Kimi-2.6-Agent/kimi_agent.py \
  --mode coding \
  --prompt "Review this Python function for bugs."
```

Modes:
- `coding`
- `studying`
- `summarising`

Optional flags:
- `--model` (default: `kimi-k2-260706`)
- `--temperature` (default: `0.3`)
- `--max-tokens` (default: `1200`)

## Run tests

```bash
python -m unittest -v
```