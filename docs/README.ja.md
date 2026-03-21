<div align="center">
  <img src="../assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>会社がAIトークン使用量のランキングを始めました。<br>おめでとうございます——あなたは今日からシーシュポスです。その岩、チャットボットです。</em></p>

  <p>
    <a href="../README.md">English</a> •
    <a href="README.zh.md">中文</a> •
    <a href="README.ko.md">한국어</a> •
    <a href="README.fr.md">Français</a> •
    <a href="README.es.md">Español</a>
  </p>

  <img src="https://github.com/neardws/token-sisyphus/actions/workflows/ci.yml/badge.svg" alt="CI" />
  <img src="https://img.shields.io/github/v/release/neardws/token-sisyphus" alt="Release" />
  <img src="https://img.shields.io/badge/python-3.9%2B-blue" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
</div>

---

![demo](../assets/demo.gif)

## これは何？

最近、多くの企業がAI使用量を生産性KPIとして管理し始めています。  
トークンをたくさん使えば表彰される。少なければ「AI活用意識が低い」と言われる。

このツールは、あなたの代わりにトークンを消費してくれます。  
あなたは何もしなくていい。ランキングはちゃんと上がります。

どういたしまして。

## 機能

- 🎯 目標トークン数まで自動消費（例：`100k`、`1m`）
- 🔌 **OpenAI・Claude・Gemini** + あらゆるOpenAI互換API対応
- 📊 リアルタイムプログレスバー＋リクエスト数表示
- ⚙️ モデル・待機時間・最大トークン数をカスタマイズ可能
- 🧪 ドライランモード（お金をかけずにテスト）
- 🧩 Claude Code・Codex・Gemini CLI・OpenCode 向けSkillファイル同梱

## クイックスタート

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

## 使用例

```bash
# OpenAI（デフォルト）
python burn.py --target 100k

# Claude Haiku
python burn.py --target 100k --provider claude --model claude-3-haiku-20240307

# Gemini Flash
python burn.py --target 100k --provider gemini --model gemini-1.5-flash

# DeepSeek（OpenAI互換）
python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# テストモード（費用なし）
python burn.py --target 100k --dry-run
```

## 免責事項

> 本プロジェクトは、企業のAI使用KPI文化への**風刺**として作られたものです。教育・娯楽目的のみを意図しています。  
> AIサービスの不正利用・社内規定違反・計算リソースの無駄遣いを推奨するものではありません。  
> もし本当にトークン数で社員を評価している会社にお勤めなら——問題は岩じゃなく、制度の方かもしれません。

## ライセンス

MIT © 2025 token-sisyphus contributors
