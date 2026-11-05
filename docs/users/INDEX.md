# 사용자 (docs/users)
> 공용 규칙이 먼저, 개인 설정은 더하기만 (D-20261102-19). 이 폴더는 팀원·상사 모두 볼 수 있음 → 평가·인사 메모, 메일 원문, 이메일 주소·전화 금지

| 아이디 | 이름 | 역할 | 폴더 |
|---|---|---|---|
| hmlee | Hyunmyung Lee | 서북미 H Mart IT (네트워크·low voltage·인프라·POS 일부·필드) | [hmlee/](hmlee/) |

## 개인 값 찾는 순서 (D-20261103-3)
드라이브 본인 Claude 폴더(원본) → 이 폴더 users/<id>/(커넥터 없을 때 사본, 민감 값 없음) → 사용자에게 묻기. 값이 다르면 드라이브가 맞음

## 새 팀원 추가 (짧은 안내 — 2단계에서 docs/onboarding.md로)
1. `docs/users/<아이디>/` 에 CLAUDE.md(개인 설정), profile.md 만들기 (hmlee 폴더를 본뜸). profile.md에 시간대 필수 (WA = America/Los_Angeles, NJ = America/New_York, D-20261105-1)
2. 저장소 폴더에 `CLAUDE.local.md` (git 제외) 한 줄: `@docs/users/<아이디>/CLAUDE.md`
3. 자기 구글 드라이브에 Claude 폴더(비공개, 상속 권한 끔) 만들고, 그 안에 00_profile 시트(항목·값·비고, 원본)를 만들고, 폴더 ID를 profile.md(사본)에
4. 개인 skill은 `.claude/skills/<아이디>-<이름>/`, 설명에 "<아이디> 전용"
5. Once per clone/PC, turn on the pre-commit backstop: `git config core.hooksPath tools/githooks` (tools/hooks/README.md, D-20261103-6)
