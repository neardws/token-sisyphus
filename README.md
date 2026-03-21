<div align="center">
  <img src="assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>Your company built a leaderboard for AI token usage.<br>Congratulations — you are now Sisyphus, and the boulder is a chatbot.</em></p>

  <p>
    <a href="#english">English</a> •
    <a href="#chinese">中文</a> •
    <a href="#japanese">日本語</a> •
    <a href="#korean">한국어</a> •
    <a href="#french">Français</a> •
    <a href="#spanish">Español</a>
  </p>

  <img src="https://img.shields.io/badge/python-3.8%2B-blue" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
  <img src="https://img.shields.io/badge/API-OpenAI%20compatible-orange" />
</div>

---

<a name="english"></a>
## 🇬🇧 English

### Why does this exist?

Many companies now track employee AI usage as a productivity KPI.  
"Top token users" get recognition. "Low token users" get questioned.

This tool burns LLM tokens on your behalf — so you can top the company AI usage chart without actually doing anything.

You're welcome.

### Features

- 🎯 Burn toward a target token count (e.g. `100k`, `1m`)
- 🔌 Works with OpenAI and **any OpenAI-compatible API** (DeepSeek, Qwen, Kimi, etc.)
- 📊 Real-time progress bar with request counter
- ⚙️ Configurable model, delay, max tokens per request
- 🧪 Dry-run mode for testing without real API calls

### Quick Start

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k
```

### Usage

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

### Examples

```bash
# Burn 100k tokens with GPT-4o-mini
python burn.py --target 100k

# Use a custom OpenAI-compatible endpoint (e.g. DeepSeek)
python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Test without real calls
python burn.py --target 100k --dry-run
```

### Output

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

### Disclaimer

> This project is a **satirical commentary** on corporate AI productivity metrics.  
> It is intended for educational and entertainment purposes only.  
> The authors do not encourage misuse of AI services, violation of company policies, or waste of computational resources.  
> Use responsibly. If your company is tracking token usage as a KPI, perhaps the real boulder was the meetings we had along the way.

---

<a name="chinese"></a>
## 🇨🇳 中文

### 为什么会有这个工具？

很多公司开始把"AI 使用量"作为员工 KPI 指标。  
Token 用得多的人受到表扬，用得少的人被质疑工作态度。

这个工具帮你自动消耗 Token，让你轻松登上公司 AI 使用排行榜——哪怕你什么都没做。

不客气。

### 快速开始

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k
```

### 使用示例

```bash
# 消耗 100k tokens
python burn.py --target 100k

# 使用 DeepSeek / 通义 / Kimi 等国产 API
python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# 测试模式（不发真实请求）
python burn.py --target 100k --dry-run
```

### 免责声明

> 本项目是对企业 AI 使用 KPI 考核机制的**讽刺性评论**，仅供娱乐和学习目的。  
> 作者不鼓励滥用 AI 服务、违反公司政策或浪费算力资源。  
> 请合理使用。如果你的公司真的在用 Token 数量衡量工作成效——也许问题不在于 Token 本身。

---

<a name="japanese"></a>
## 🇯🇵 日本語

### なぜこのツールが存在するのか

多くの企業がAI使用量を生産性KPIとして計測し始めています。  
トークンをたくさん使った社員は評価され、少ない社員は怠け者扱いされます。

このツールはあなたの代わりにトークンを消費し、何もしなくても社内AIランキングのトップに立てます。

どういたしまして。

### クイックスタート

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k
```

### 免責事項

> 本プロジェクトは企業のAI利用KPI評価制度への**風刺的なコメント**であり、教育・娯楽目的のみを意図しています。  
> AIサービスの不正利用、社内規定への違反、計算資源の浪費を推奨するものではありません。  
> 責任ある使用をお願いします。

---

<a name="korean"></a>
## 🇰🇷 한국어

### 왜 이 도구가 존재하는가

많은 기업이 AI 사용량을 생산성 KPI로 측정하기 시작했습니다.  
토큰을 많이 사용한 직원은 인정받고, 적게 사용한 직원은 의심받습니다.

이 도구는 당신 대신 토큰을 소비하여 아무것도 하지 않아도 회사 AI 사용 순위 상위권에 오를 수 있게 해줍니다.

천만에요.

### 빠른 시작

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k
```

### 면책 조항

> 이 프로젝트는 기업의 AI 사용 KPI 평가 제도에 대한 **풍자적 논평**으로, 교육 및 오락 목적으로만 제작되었습니다.  
> AI 서비스 남용, 회사 정책 위반, 컴퓨팅 자원 낭비를 권장하지 않습니다.  
> 책임감 있게 사용하세요.

---

<a name="french"></a>
## 🇫🇷 Français

### Pourquoi cet outil existe-t-il ?

De nombreuses entreprises mesurent désormais l'utilisation de l'IA comme KPI de productivité.  
Les grands utilisateurs de tokens sont récompensés. Les autres sont questionnés.

Cet outil consomme des tokens LLM en votre nom — pour que vous puissiez dominer le classement IA de votre entreprise sans rien faire.

De rien.

### Démarrage rapide

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k
```

### Avertissement

> Ce projet est un **commentaire satirique** sur les métriques de productivité IA en entreprise.  
> Il est destiné à des fins éducatives et de divertissement uniquement.  
> Les auteurs ne cautionnent pas l'abus des services IA, la violation des politiques d'entreprise ou le gaspillage de ressources informatiques.

---

<a name="spanish"></a>
## 🇪🇸 Español

### ¿Por qué existe esta herramienta?

Muchas empresas miden el uso de IA como KPI de productividad.  
Los que más tokens consumen son reconocidos. Los demás son cuestionados.

Esta herramienta consume tokens de LLM en tu nombre — para que puedas liderar el ranking de uso de IA de tu empresa sin hacer absolutamente nada.

De nada.

### Inicio rápido

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k
```

### Descargo de responsabilidad

> Este proyecto es un **comentario satírico** sobre las métricas de productividad de IA corporativa.  
> Está destinado únicamente a fines educativos y de entretenimiento.  
> Los autores no fomentan el mal uso de los servicios de IA, la violación de las políticas de la empresa ni el desperdicio de recursos computacionales.

---

## Compatible APIs

Any OpenAI-compatible endpoint works out of the box:

| Provider | base-url |
|----------|----------|
| OpenAI | (default) |
| DeepSeek | `https://api.deepseek.com/v1` |
| Qwen / Tongyi | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Moonshot / Kimi | `https://api.moonshot.cn/v1` |
| Zhipu / GLM | `https://open.bigmodel.cn/api/paas/v4` |
| Azure OpenAI | your Azure endpoint |
| vLLM / Ollama | your self-hosted endpoint |

---

## License

MIT © 2025 token-sisyphus contributors
