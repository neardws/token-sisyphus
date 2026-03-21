<div align="center">
  <img src="../assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>Tu empresa creó un ranking de uso de tokens de IA.<br>Felicidades — ahora eres Sísifo, y la roca es un chatbot.</em></p>

  <p>
    <a href="../README.md">English</a> •
    <a href="README.zh.md">中文</a> •
    <a href="README.ja.md">日本語</a> •
    <a href="README.ko.md">한국어</a> •
    <a href="README.fr.md">Français</a>
  </p>
</div>

---

## ¿Por qué existe esta herramienta?

Muchas empresas miden el uso de IA como KPI de productividad.  
Los que más tokens consumen son reconocidos. Los demás son cuestionados.

Esta herramienta consume tokens de LLM en tu nombre — para que puedas liderar el ranking de uso de IA de tu empresa sin hacer absolutamente nada.

De nada.

## Características

- 🎯 Consumir hasta un número objetivo de tokens (ej: `100k`, `1m`)
- 🔌 Compatible con **OpenAI, Claude, Gemini** y cualquier API compatible con OpenAI
- 📊 Barra de progreso en tiempo real
- ⚙️ Modelo, retraso y tokens máximos configurables
- 🧪 Modo simulación sin llamadas API reales
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

# Modo simulación
python burn.py --target 100k --dry-run
```

## Descargo de responsabilidad

> Este proyecto es un **comentario satírico** sobre las métricas de productividad de IA corporativa.  
> Está destinado únicamente a fines educativos y de entretenimiento.  
> Los autores no fomentan el mal uso de los servicios de IA, la violación de las políticas de la empresa ni el desperdicio de recursos computacionales.

## Licencia

MIT © 2025 token-sisyphus contributors
