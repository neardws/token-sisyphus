<div align="center">
  <img src="../assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>Votre entreprise a créé un classement d'utilisation des tokens IA.<br>Félicitations — vous êtes désormais Sisyphe, et le rocher est un chatbot.</em></p>

  <p>
    <a href="../README.md">English</a> •
    <a href="README.zh.md">中文</a> •
    <a href="README.ja.md">日本語</a> •
    <a href="README.ko.md">한국어</a> •
    <a href="README.es.md">Español</a>
  </p>
</div>

---

## Pourquoi cet outil existe-t-il ?

De nombreuses entreprises mesurent désormais l'utilisation de l'IA comme KPI de productivité.  
Les grands utilisateurs de tokens sont récompensés. Les autres sont questionnés.

Cet outil consomme des tokens LLM en votre nom — pour que vous puissiez dominer le classement IA de votre entreprise sans rien faire.

De rien.

## Fonctionnalités

- 🎯 Consommer jusqu'à un nombre cible de tokens (ex: `100k`, `1m`)
- 🔌 Compatible avec OpenAI et toute API compatible OpenAI
- 📊 Barre de progression en temps réel
- ⚙️ Modèle, délai et tokens max configurables
- 🧪 Mode simulation sans appels API réels

## Démarrage rapide

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k
```

## Exemples

```bash
# Consommer 100k tokens
python burn.py --target 100k

# Utiliser un endpoint compatible OpenAI
python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Mode simulation
python burn.py --target 100k --dry-run
```

## Avertissement

> Ce projet est un **commentaire satirique** sur les métriques de productivité IA en entreprise.  
> Il est destiné à des fins éducatives et de divertissement uniquement.  
> Les auteurs ne cautionnent pas l'abus des services IA, la violation des politiques d'entreprise ou le gaspillage de ressources informatiques.

## Licence

MIT © 2025 token-sisyphus contributors
