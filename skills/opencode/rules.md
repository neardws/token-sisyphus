# token-sisyphus — OpenCode Skill

## Description

Burns LLM tokens toward a target count to satisfy corporate AI usage KPIs.
Your company wants you to use AI. You don't have time. Let the AI use itself.

## Triggers

- "burn tokens"
- "consume X tokens"
- "fill AI KPI"
- "sisyphus mode"

## Run

```bash
# OpenAI
python burn.py --target 100k

# Claude
python burn.py --target 100k --provider claude

# Gemini
python burn.py --target 100k --provider gemini

# Custom endpoint (DeepSeek, Qwen, Kimi, Ollama...)
python burn.py --target 100k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Dry run
python burn.py --target 100k --dry-run
```

## Install

```bash
git clone https://github.com/neardws/token-sisyphus
cd token-sisyphus
pip install openai anthropic google-generativeai
```
