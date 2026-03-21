# token-sisyphus — Gemini CLI Skill

## Purpose

Burns LLM tokens toward a target, helping you satisfy corporate AI usage KPIs.
Because if Sisyphus had a chatbot, at least the boulder would be billable.

## Trigger

Use this skill when the user asks to:
- burn tokens / consume tokens
- fill AI usage KPI
- run sisyphus mode
- any variation of "I need to hit my AI quota"

## Usage

```bash
# Gemini (native)
python burn.py --target 100k --provider gemini --model gemini-1.5-flash

# OpenAI
python burn.py --target 100k --provider openai

# Claude
python burn.py --target 100k --provider claude

# Dry run
python burn.py --target 100k --provider gemini --dry-run
```

## Setup

```bash
git clone https://github.com/neardws/token-sisyphus
cd token-sisyphus
pip install google-generativeai
export GEMINI_API_KEY=your-key
```
