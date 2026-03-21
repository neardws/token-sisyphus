---
name: token-sisyphus
description: >
  Burn LLM tokens toward a target count to satisfy corporate AI usage KPIs.
  Trigger when user says: burn tokens, consume tokens, fill KPI, push the boulder,
  sisyphus mode, or specifies a token target like "burn 100k tokens".
---

# token-sisyphus — OpenClaw Skill

Push the boulder. Watch it roll back. At least your KPI is green.

## Trigger examples

- "burn 100k tokens"
- "help me fill my AI KPI"
- "consume 500k tokens with DeepSeek"
- "sisyphus mode, 1 million tokens"

## How to run

Locate the `burn.py` script in the token-sisyphus repo and run:

```bash
# Basic (OpenAI)
python burn.py --target 100k

# Claude
python burn.py --target 100k --provider claude

# Gemini
python burn.py --target 100k --provider gemini

# OpenAI-compatible (DeepSeek, Kimi, Qwen...)
python burn.py --target 100k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Dry run
python burn.py --target 100k --dry-run
```

## Setup

```bash
git clone https://github.com/neardws/token-sisyphus
cd token-sisyphus
pip install openai          # for openai provider
pip install anthropic       # for claude provider
pip install google-generativeai  # for gemini provider
```

Set the relevant env var:
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
