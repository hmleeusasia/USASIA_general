# 지식 문서 목차

## Where to look first (moved from CLAUDE.md, 2026-11-03)
| Question | Look here |
|---|---|
| Current state / tasks | docs/CURRENT_STATE.md (repo work), docs/users/<id>/todo.md (personal work, synced with STWS) |
| Why a past decision | docs/decisions.md |
| Past vendor work | docs/vendors/INDEX.md → vendor file |
| Keyword / vendor / item | `python3 tools/find.py Granite demarc` (synonyms, AND) |
| Open / overdue items | `python3 tools/find.py --open` |
| Next 30 days | `python3 tools/find.py --due` |
| Drive documents | docs/drive-index/INDEX.md |
| IT team member context / questions for them | docs/team/INDEX.md (D-20261105-7) |
| Plans in progress | docs/requests/ |
| Emails, phones, account numbers | Drive Claude folder → docs/drive-index/claude-folder.md (IDs and column names only) |
| Users / personal settings | docs/users/INDEX.md |
| Repo architecture (principles, diagrams, tree) | docs/ARCHITECTURE.md (snapshot: tools/repo_map.py) |
| Procedures (skills) | .claude/skills/ (descriptions say when to use) |
| Hooks (supervisor) | tools/hooks/README.md |

## Documents

주제별 요약 문서를 이 폴더에 추가하고 여기 한 줄씩 적는다.

| 문서 | 내용 |
|---|---|
| facts.md | 계속 유효한 사실 (매장·시스템·업체·선호) |
| mail_triage.md | 메일 분류 기준 (내 범위·발신자 규칙·경계 사례) |
| orgs.md | 계열사·벤더·협력업체 목록 (새 이름은 물어서 추가) |
| reimbursement.md | 월별 경비 청구 정리(노션→시트→영수증) |
| store_codes.md | 매장·조직 약어 (TC·BV·RM·MW 등) |
| subagents.md | 하위 에이전트 활용법 (등급·모델 분담·프롬프트 틀·결과 확인) |
- pos_tips.md — Toshiba POS on-site fixes (error codes)
- work_overview.md — Work streams from sent mail Aug–Oct 2026 (Outlook)
- browser.md — Chrome use with small context (JS first, no computer scroll, output limits)
