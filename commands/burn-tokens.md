---
description: Burn LLM tokens toward a target count
argument-hint: <target> [--provider openai|claude|gemini] [--dry-run]
allowed-tools: Bash(python:*)
---

Run the token-sisyphus burn script with the user's arguments.

**First-time users:** suggest adding `--dry-run` to test without incurring API costs.

Execute:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/token-sisyphus/scripts/burn.py" $ARGUMENTS
```

If the command fails because a provider SDK is missing, tell the user which package to install:
- OpenAI: `pip install openai`
- Claude: `pip install anthropic`
- Gemini: `pip install google-generativeai`
