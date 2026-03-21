<div align="center">
  <img src="../assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>Tu empresa creó un ranking de uso de tokens de IA.<br>Enhorabuena — ahora eres Sísifo, y la roca es un chatbot.</em></p>

  <p>
    <a href="../README.md">English</a> •
    <a href="README.zh.md">中文</a> •
    <a href="README.ja.md">日本語</a> •
    <a href="README.ko.md">한국어</a> •
    <a href="README.fr.md">Français</a>
  </p>

  <img src="https://github.com/neardws/token-sisyphus/actions/workflows/ci.yml/badge.svg" alt="CI" />
  <img src="https://img.shields.io/github/v/release/neardws/token-sisyphus" alt="Release" />
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
</div>

---

![demo](../assets/demo.gif)

## ¿Para qué sirve esto?

Cada vez más empresas miden el uso de IA como KPI de productividad.  
Los que más tokens consumen reciben felicitaciones. Los demás reciben un correo de su manager.

Esta herramienta consume tokens por ti — para que puedas liderar el ranking sin mover un dedo.

De nada.

## Características

- 🎯 Consumir hasta un número objetivo de tokens (ej: `100k`, `1m`)
- 🔌 Compatible con **OpenAI, Claude, Gemini** y cualquier API compatible con OpenAI
- 📊 Barra de progreso en tiempo real + contador de peticiones
- ⚙️ Modelo, retraso y tokens máximos totalmente configurables
- 🧪 Modo simulación para probar sin gastar dinero
- 🧩 Archivos Skill para Claude Code, Codex, Gemini CLI, OpenCode

## Inicio rápido

```bash
# OpenAI
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k

# Claude
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python burn.py --target 100k --provider claude

# Gemini
pip install google-generativeai
export GEMINI_API_KEY=...
python burn.py --target 100k --provider gemini
```

## Ejemplos

```bash
# OpenAI (por defecto)
python burn.py --target 100k

# Claude Haiku
python burn.py --target 100k --provider claude --model claude-3-haiku-20240307

# Gemini Flash
python burn.py --target 100k --provider gemini --model gemini-1.5-flash

# DeepSeek (compatible OpenAI)
python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Modo simulación (sin coste)
python burn.py --target 100k --dry-run
```

## Descargo de responsabilidad

> Este proyecto es una **sátira** del fenómeno de los KPI de uso de IA en las empresas. Su finalidad es exclusivamente educativa y de entretenimiento.  
> Los autores no promueven el mal uso de los servicios de IA, la violación de políticas corporativas ni el desperdicio de recursos computacionales.  
> Si tu empresa de verdad evalúa a sus empleados por tokens consumidos — el problema quizás no sea la roca.

## APIs compatibles

| Proveedor | Modelo recomendado | provider | --base-url |
|----------|-------------------|----------|------------|
| OpenAI | `gpt-5.4` / `gpt-4o-mini` | `openai` | (por defecto) |
| Anthropic Claude | `claude-sonnet-4-6` | `claude` | — |
| Google Gemini | `gemini-3.1-pro` / `gemini-2.5-flash` | `gemini` | — |
| DeepSeek | `deepseek-v4` | `openai` | `https://api.deepseek.com/v1` |
| Xiaomi MiMo | `mimo-v2-pro` / `mimo-v2-flash` | `openai` | `https://api.xiaomimimo.com/v1` |
| Qwen / Tongyi | `qwen-turbo` | `openai` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Moonshot / Kimi | `moonshot-v1-8k` | `openai` | `https://api.moonshot.cn/v1` |
| Zhipu / GLM | `glm-4-flash` | `openai` | `https://open.bigmodel.cn/api/paas/v4` |
| vLLM / Ollama | modelo local | `openai` | tu endpoint |

## Licencia

MIT License — Copyright (c) 2026 neardws and token-sisyphus contributors
