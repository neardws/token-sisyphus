<div align="center">
  <img src="../assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>Votre entreprise a lancé un classement d'utilisation des tokens IA.<br>Félicitations — vous êtes désormais Sisyphe, et le rocher, c'est un chatbot.</em></p>

  <p>
    <a href="../README.md">English</a> •
    <a href="README.zh.md">中文</a> •
    <a href="README.ja.md">日本語</a> •
    <a href="README.ko.md">한국어</a> •
    <a href="README.es.md">Español</a>
  </p>

  <img src="https://github.com/neardws/token-sisyphus/actions/workflows/ci.yml/badge.svg" alt="CI" />
  <img src="https://img.shields.io/github/v/release/neardws/token-sisyphus" alt="Release" />
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
</div>

---

![demo](../assets/demo.gif)

## C'est quoi ce truc ?

De plus en plus d'entreprises mesurent l'utilisation de l'IA comme indicateur de productivité.  
Les grands consommateurs de tokens sont célébrés. Les autres reçoivent un mail de leur manager.

Cet outil consomme des tokens à votre place — pour que vous puissiez trôner en tête du classement sans lever le petit doigt.

De rien.

## Fonctionnalités

- 🎯 Consommer jusqu'à un nombre cible de tokens (ex : `100k`, `1m`)
- 🔌 Compatible **OpenAI, Claude, Gemini** et toute API compatible OpenAI
- 📊 Barre de progression en temps réel + compteur de requêtes
- ⚙️ Modèle, délai et tokens max entièrement configurables
- 🧪 Mode simulation pour tester sans frais
- 🧩 Fichiers Skill pour Claude Code, Codex, Gemini CLI, OpenCode

## Démarrage rapide

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

## Exemples

```bash
# OpenAI (par défaut)
python burn.py --target 100k

# Claude Haiku
python burn.py --target 100k --provider claude --model claude-3-haiku-20240307

# Gemini Flash
python burn.py --target 100k --provider gemini --model gemini-1.5-flash

# DeepSeek (compatible OpenAI)
python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Mode simulation (sans frais)
python burn.py --target 100k --dry-run
```

## Avertissement

> Ce projet est une **satire** du phénomène des KPI d'utilisation IA en entreprise. Il est destiné à des fins éducatives et humoristiques uniquement.  
> Les auteurs ne cautionnent pas l'abus de services IA, la violation de politiques d'entreprise, ni le gaspillage de ressources.  
> Si votre entreprise évalue vraiment ses employés au nombre de tokens consommés — le problème n'est peut-être pas le rocher.

## Licence

MIT © 2025 token-sisyphus contributors
