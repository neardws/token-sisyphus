<div align="center">
  <img src="../assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>회사가 AI 토큰 사용 순위표를 만들었습니다.<br>축하해요 — 이제 당신은 시시포스고, 그 바위는 챗봇입니다.</em></p>

  <p>
    <a href="../README.md">English</a> •
    <a href="README.zh.md">中文</a> •
    <a href="README.ja.md">日本語</a> •
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

## 이게 뭐예요?

요즘 많은 회사들이 AI 사용량을 생산성 KPI로 관리하기 시작했습니다.  
토큰 많이 쓰면 칭찬받고, 적게 쓰면 "AI 도입 의지가 없다"는 소리를 듣습니다.

이 툴은 여러분 대신 토큰을 소비해 줍니다.  
아무것도 안 해도 됩니다. 순위표는 알아서 올라갑니다.

천만에요.

## 기능

- 🎯 목표 토큰 수까지 자동 소비 (예: `100k`, `1m`)
- 🔌 **OpenAI, Claude, Gemini** 및 모든 OpenAI 호환 API 지원
- 📊 실시간 진행 막대 + 요청 수 표시
- ⚙️ 모델, 딜레이, 최대 토큰 수 커스터마이징 가능
- 🧪 드라이런 모드 (돈 안 쓰고 테스트)
- 🧩 Claude Code, Codex, Gemini CLI, OpenCode 용 Skill 파일 포함

## 빠른 시작

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

## 사용 예시

```bash
# OpenAI (기본값)
python burn.py --target 100k

# Claude Haiku
python burn.py --target 100k --provider claude --model claude-3-haiku-20240307

# Gemini Flash
python burn.py --target 100k --provider gemini --model gemini-1.5-flash

# DeepSeek (OpenAI 호환)
python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# 테스트 모드 (비용 없음)
python burn.py --target 100k --dry-run
```

## 면책 조항

> 이 프로젝트는 'AI 사용량 KPI' 문화에 대한 **풍자**로 만들어졌으며, 교육 및 오락 목적으로만 제작되었습니다.  
> AI 서비스 남용, 회사 정책 위반, 컴퓨팅 자원 낭비를 권장하지 않습니다.  
> 만약 정말로 토큰 수로 직원을 평가하는 회사에 다니신다면——문제는 바위가 아니라 평가 제도일 수 있습니다.

## 라이선스

MIT © 2025 token-sisyphus contributors
