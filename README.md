<div align="center">
  <img src="assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>Your company built a leaderboard for AI token usage.<br>Congratulations — you are now Sisyphus, and the boulder is a chatbot.</em></p>

  <p>
    <a href="docs/README.zh.md">中文</a> •
    <a href="docs/README.ja.md">日本語</a> •
    <a href="docs/README.ko.md">한국어</a> •
    <a href="docs/README.fr.md">Français</a> •
    <a href="docs/README.es.md">Español</a>
  </p>

  <img src="https://img.shields.io/badge/python-3.8%2B-blue" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
  <img src="https://img.shields.io/badge/API-OpenAI%20compatible-orange" />
</div>

---

## Why does this exist?

Many companies now track employee AI usage as a productivity KPI.  
"Top token users" get recognition. "Low token users" get questioned.

This tool burns LLM tokens on your behalf — so you can top the company AI usage chart without actually doing anything.

You're welcome.

## Features

- 🎯 Burn toward a target token count (e.g. `100k`, `1m`)
- 🔌 Works with OpenAI and **any OpenAI-compatible API** (DeepSeek, Qwen, Kimi, etc.)
- 📊 Real-time progress bar with request counter
- ⚙️ Configurable model, delay, max tokens per request
- 🧪 Dry-run mode for testing without real API calls

## Quick Start

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k
```

## Usage

```
python burn.py --target <amount> [options]

  --target       Token count to burn: 50000, 100k, 1m  (required)
  --model        Model to use (default: gpt-4o-mini)
  --api-key      API key (or set OPENAI_API_KEY env var)
  --base-url     Custom base URL for OpenAI-compatible APIs
  --max-tokens   Max tokens per request (default: 500)
  --delay        Seconds between requests (default: 0.5)
  --dry-run      Simulate without real API calls
```

## Examples

```bash
# Burn 100k tokens with GPT-4o-mini
python burn.py --target 100k

# Use DeepSeek API
python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Test without real calls
python burn.py --target 100k --dry-run
```

## Output

```
🪨  token-sisyphus starting...
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

## Compatible APIs

Any OpenAI-compatible endpoint works out of the box:

| Provider | --base-url |
|----------|------------|
| OpenAI | (default) |
| DeepSeek | `https://api.deepseek.com/v1` |
| Qwen / Tongyi | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Moonshot / Kimi | `https://api.moonshot.cn/v1` |
| Zhipu / GLM | `https://open.bigmodel.cn/api/paas/v4` |
| Azure OpenAI | your Azure endpoint |
| vLLM / Ollama | your self-hosted endpoint |

## Disclaimer

> This project is a **satirical commentary** on corporate AI productivity metrics.  
> It is intended for educational and entertainment purposes only.  
> The authors do not encourage misuse of AI services, violation of company policies, or waste of computational resources.  
> Use responsibly. If your company is tracking token usage as a KPI, perhaps the real boulder was the meetings we had along the way.

## License

MIT © 2025 token-sisyphus contributors
