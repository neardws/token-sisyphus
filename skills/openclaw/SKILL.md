---
name: token-sisyphus
description: >
  Burn LLM tokens toward a target count to satisfy corporate AI usage KPIs.
  Use when the user asks to: burn tokens, consume tokens, fill AI KPI, hit token quota,
  push the boulder, sisyphus mode, or specifies a target like "burn 100k tokens".
  Supports OpenAI, Claude, Gemini, and any OpenAI-compatible API (DeepSeek, Qwen, Kimi, etc.).
---

# token-sisyphus

Push the boulder. Watch it roll back. At least your KPI is green.

## Setup

```bash
git clone https://github.com/neardws/token-sisyphus
cd token-sisyphus

# Install provider SDK(s) as needed
pip install openai              # OpenAI / compatible
pip install anthropic           # Claude
pip install google-generativeai # Gemini
```

Set the relevant env var:

| Provider | Env var |
|----------|---------|
| OpenAI / compatible | `OPENAI_API_KEY` |
| Claude | `ANTHROPIC_API_KEY` |
| Gemini | `GEMINI_API_KEY` |

## Usage

```
python burn.py --target <amount> [options]

  --target       Token count: 50000, 100k, 1m  (required)
  --provider     openai | claude | gemini  (default: openai)
  --model        Model name (omit to use provider default)
  --api-key      API key (falls back to env var)
  --base-url     Custom endpoint URL (openai provider only)
  --max-tokens   Max tokens per request (default: 500)
  --delay        Seconds between requests (default: 0.5)
  --dry-run      Simulate without real API calls
```

## Common invocations

```bash
# OpenAI (default, gpt-4o-mini)
python burn.py --target 100k

# Claude Haiku
python burn.py --target 100k --provider claude --model claude-3-haiku-20240307

# Gemini Flash
python burn.py --target 100k --provider gemini --model gemini-1.5-flash

# DeepSeek
python burn.py --target 100k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Qwen / Tongyi
python burn.py --target 100k --base-url https://dashscope.aliyuncs.com/compatible-mode/v1 --model qwen-turbo

# Kimi / Moonshot
python burn.py --target 100k --base-url https://api.moonshot.cn/v1 --model moonshot-v1-8k

# Dry run (no real API calls)
python burn.py --target 100k --dry-run
```

## Provider defaults

| Provider | Default model |
|----------|---------------|
| openai | gpt-4o-mini |
| claude | claude-3-haiku-20240307 |
| gemini | gemini-1.5-flash |

## Expected output

```
🪨  token-sisyphus starting...
    Provider : openai
    Target   : 100,000 tokens
    Model    : gpt-4o-mini
    Mode     : LIVE

  [████████████████████░░░░░░░░░░░░░░░░░░░░] 50.3% (50,312 / 100,000 tokens)  req#87

✅  Done.
    Total tokens burned : 100,412
    Requests made       : 174
    Time elapsed        : 91.3s
    Avg tokens/req      : 577

    Your boulder has reached the top. See you tomorrow.
```
