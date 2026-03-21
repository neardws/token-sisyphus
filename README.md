# 🪨 llm-sisyphus

> Your company built a leaderboard for AI token usage.  
> Congratulations — you are now Sisyphus, and the boulder is a chatbot.

A simple CLI tool that burns LLM tokens on your behalf, so you can top the company AI usage chart without actually doing anything.

---

## Why does this exist?

Many companies now track employee AI usage as a productivity KPI.  
"Top token users" get recognition. "Low token users" get questioned.

This tool burns tokens meaningfully-pointlessly so you can focus on actual work — or on doing nothing, which is equally valid.

---

## Features

- Burn tokens toward a target count (e.g. 100k, 1m)
- Works with OpenAI and any OpenAI-compatible API
- Real-time progress bar
- Configurable model, delay, max tokens per request
- Dry-run mode for testing

---

## Quick Start

```bash
pip install openai

export OPENAI_API_KEY=sk-...

python burn.py --target 100k
```

---

## Usage

```
python burn.py --target <amount> [options]

Options:
  --target       Token count to burn: 50000, 100k, 1m  (required)
  --model        Model to use (default: gpt-4o-mini)
  --api-key      API key (or set OPENAI_API_KEY env var)
  --base-url     Custom base URL for OpenAI-compatible APIs
  --max-tokens   Max tokens per request (default: 500)
  --delay        Seconds between requests (default: 0.5)
  --dry-run      Simulate without real API calls
```

### Examples

```bash
# Burn 100k tokens with GPT-4o-mini
python burn.py --target 100k

# Use a custom OpenAI-compatible endpoint
python burn.py --target 500k --base-url https://your-api.com/v1 --model your-model

# Test the flow without real calls
python burn.py --target 100k --dry-run
```

---

## Compatible APIs

Any OpenAI-compatible endpoint works:

- OpenAI
- Azure OpenAI
- DeepSeek
- Qwen / Tongyi
- Zhipu / GLM
- Moonshot / Kimi
- Any self-hosted endpoint (vLLM, Ollama with OpenAI mode, etc.)

---

## Output

```
🪨  llm-sisyphus starting...
    Target : 100,000 tokens
    Model  : gpt-4o-mini
    Mode   : LIVE

  [████████████████████░░░░░░░░░░░░░░░░░░░░] 50.3% (50,312 / 100,000 tokens)  req#87

✅  Done.
    Total tokens burned : 100,412
    Requests made       : 174
    Time elapsed        : 91.3s
    Avg tokens/req      : 577

    Your boulder has reached the top. See you tomorrow.
```

---

## Disclaimer

This tool is a **satire** on corporate AI productivity metrics.  
Use responsibly. Don't burn tokens that cost real money for no reason.  
Unless your company is paying. Then go nuts.

---

## License

MIT
