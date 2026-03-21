# Changelog

## v1.0.1 (2026-03-21)

### 🔧 Release improvements
- Split release artifacts into per-platform packages
  - `core` — `burn.py` only
  - `skills-all` — all platform skill files bundled
  - `skill-claude-code` / `skill-codex` / `skill-gemini-cli` / `skill-opencode` / `skill-openclaw` — individual skill files
  - `full` — everything

---

## v1.0.0 (2026-03-21)

### 🎉 Initial Release

**Core**
- `burn.py` — CLI tool to burn LLM tokens toward a target count
- Target formats: `50000`, `100k`, `1m`
- Real-time progress bar with request counter
- Dry-run mode (simulate without real API calls)

**Providers**
- `--provider openai` — OpenAI and any OpenAI-compatible API (DeepSeek, Qwen, Kimi, Moonshot, GLM, Azure, vLLM, Ollama, ...)
- `--provider claude` — Anthropic Claude (claude-3-haiku, claude-3-sonnet, claude-3-opus, ...)
- `--provider gemini` — Google Gemini (gemini-1.5-flash, gemini-1.5-pro, ...)

**Agent Skills**
- `skills/claude-code/CLAUDE.md` — Claude Code integration
- `skills/codex/AGENTS.md` — OpenAI Codex integration
- `skills/gemini-cli/gemini.md` — Gemini CLI integration
- `skills/opencode/rules.md` — OpenCode integration
- `skills/openclaw/SKILL.md` — OpenClaw integration

**Docs**
- README in 6 languages: English, 中文, 日本語, 한국어, Français, Español
- CI badge + Release badge
