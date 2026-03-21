<div align="center">
  <img src="../assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>あなたの会社はAIトークン使用量のランキングを作りました。<br>おめでとうございます——あなたは今やシーシュポスで、その岩はチャットボットです。</em></p>

  <p>
    <a href="../README.md">English</a> •
    <a href="README.zh.md">中文</a> •
    <a href="README.ko.md">한국어</a> •
    <a href="README.fr.md">Français</a> •
    <a href="README.es.md">Español</a>
  </p>
</div>

---

## なぜこのツールが存在するのか

多くの企業がAI使用量を生産性KPIとして計測し始めています。  
トークンをたくさん使った社員は評価され、少ない社員は怠け者扱いされます。

このツールはあなたの代わりにトークンを消費し、何もしなくても社内AIランキングのトップに立てます。

どういたしまして。

## 機能

- 🎯 目標トークン数に向けて消費（例：`100k`、`1m`）
- 🔌 **OpenAI・Claude・Gemini** およびすべてのOpenAI互換API対応
- 📊 リアルタイムプログレスバー
- ⚙️ モデル・遅延・最大トークン数の設定可能
- 🧪 ドライランモード（実際のAPIコールなし）
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

# テストモード
python burn.py --target 100k --dry-run
```

## 免責事項

> 本プロジェクトは企業のAI利用KPI評価制度への**風刺的なコメント**であり、教育・娯楽目的のみを意図しています。  
> AIサービスの不正利用、社内規定への違反、計算資源の浪費を推奨するものではありません。  
> 責任ある使用をお願いします。

## ライセンス

MIT © 2025 token-sisyphus contributors
