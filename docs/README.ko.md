<div align="center">
  <img src="../assets/logo.png" alt="token-sisyphus logo" width="180" />
  <h1>🪨 token-sisyphus</h1>
  <p><em>회사가 AI 토큰 사용량 리더보드를 만들었습니다.<br>축하합니다 — 당신은 이제 시시포스이고, 바위는 챗봇입니다.</em></p>

  <p>
    <a href="../README.md">English</a> •
    <a href="README.zh.md">中文</a> •
    <a href="README.ja.md">日本語</a> •
    <a href="README.fr.md">Français</a> •
    <a href="README.es.md">Español</a>
  </p>
</div>

---

## 왜 이 도구가 존재하는가

많은 기업이 AI 사용량을 생산성 KPI로 측정하기 시작했습니다.  
토큰을 많이 사용한 직원은 인정받고, 적게 사용한 직원은 의심받습니다.

이 도구는 당신 대신 토큰을 소비하여 아무것도 하지 않아도 회사 AI 사용 순위 상위권에 오를 수 있게 해줍니다.

천만에요.

## 기능

- 🎯 목표 토큰 수까지 소비 (예: `100k`, `1m`)
- 🔌 OpenAI 및 모든 OpenAI 호환 API 지원
- 📊 실시간 진행 막대
- ⚙️ 모델, 딜레이, 최대 토큰 수 설정 가능
- 🧪 드라이런 모드 (실제 API 호출 없음)

## 빠른 시작

```bash
pip install openai
export OPENAI_API_KEY=sk-...
python burn.py --target 100k
```

## 사용 예시

```bash
# 100k 토큰 소비
python burn.py --target 100k

# 커스텀 API 엔드포인트 사용
python burn.py --target 500k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# 테스트 모드 (실제 API 호출 없음)
python burn.py --target 100k --dry-run
```

## 면책 조항

> 이 프로젝트는 기업의 AI 사용 KPI 평가 제도에 대한 **풍자적 논평**으로, 교육 및 오락 목적으로만 제작되었습니다.  
> AI 서비스 남용, 회사 정책 위반, 컴퓨팅 자원 낭비를 권장하지 않습니다.  
> 책임감 있게 사용하세요.

## 라이선스

MIT © 2025 token-sisyphus contributors
