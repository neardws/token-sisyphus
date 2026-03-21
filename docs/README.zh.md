<div align="center">
  <img src="../assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>公司做了一个 AI Token 使用排行榜。<br>恭喜你——你现在是西西弗斯，那块巨石是一个聊天机器人。</em></p>

  <p>
    <a href="../README.md">English</a> •
    <a href="README.ja.md">日本語</a> •
    <a href="README.ko.md">한국어</a> •
    <a href="README.fr.md">Français</a> •
    <a href="README.es.md">Español</a>
  </p>

  <img src="https://img.shields.io/badge/python-3.8%2B-blue" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
  <img src="https://img.shields.io/badge/API-OpenAI%20兼容-orange" />
</div>

---

## 为什么会有这个工具？

很多公司开始把"AI 使用量"作为员工 KPI 指标。  
Token 用得多的人受到表扬，用得少的人被质疑工作态度。

这个工具帮你自动消耗 Token，让你轻松登上公司 AI 使用排行榜——哪怕你什么都没做。

不客气。

## 功能特性

- 🎯 按目标 Token 数量消耗（如 `100k`、`1m`）
- 🔌 支持 OpenAI 及所有兼容接口（DeepSeek、通义、Kimi 等）
- 📊 实时进度条 + 请求计数
- ⚙️ 可配置模型、请求间隔、单次最大 Token 数
- 🧪 Dry-run 模式，不发真实请求

## 快速开始

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k
```

## 使用方式

```
python burn.py --target <数量> [选项]

  --target       目标 Token 数：50000、100k、1m（必填）
  --model        使用的模型（默认：gpt-4o-mini）
  --api-key      API Key（或设置 OPENAI_API_KEY 环境变量）
  --base-url     自定义 API 地址（OpenAI 兼容接口）
  --max-tokens   每次请求最大 Token 数（默认：500）
  --delay        请求间隔秒数（默认：0.5）
  --dry-run      模拟模式，不发真实请求
```

## 使用示例

```bash
# 消耗 100k tokens
python burn.py --target 100k

# 使用 DeepSeek API
python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# 使用通义千问
python burn.py --target 200k --base-url https://dashscope.aliyuncs.com/compatible-mode/v1 --model qwen-turbo

# 测试模式（不发真实请求）
python burn.py --target 100k --dry-run
```

## 兼容的 API

| 服务商 | --base-url |
|--------|------------|
| OpenAI | （默认） |
| DeepSeek | `https://api.deepseek.com/v1` |
| 通义千问 | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Moonshot / Kimi | `https://api.moonshot.cn/v1` |
| 智谱 / GLM | `https://open.bigmodel.cn/api/paas/v4` |
| Azure OpenAI | 你的 Azure 地址 |
| vLLM / Ollama | 你的自托管地址 |

## 免责声明

> 本项目是对企业 AI 使用 KPI 考核机制的**讽刺性评论**，仅供娱乐和学习目的。  
> 作者不鼓励滥用 AI 服务、违反公司政策或浪费算力资源。  
> 请合理使用。如果你的公司真的在用 Token 数量衡量工作成效——也许问题不在于 Token 本身。

## 许可证

MIT © 2025 token-sisyphus contributors
