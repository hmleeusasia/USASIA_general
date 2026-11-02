---
name: session-end
description: 세션 마무리·인계 절차. 점검표(docs/session_review.md) 수행, CURRENT_STATE·facts·decisions 갱신, 틀 변경 제안·비효율 평가 표 보고, 커밋·push. "마무리", "인계", "세션 종료", "세션 닫기" 때 사용.
---

# 세션 마무리 (session-end)

1. docs/session_review.md 점검표 1절 전부 (check.py, find.py --open/--due, 줄 수, INDEX 일치, 민감 정보)
2. 드라이브 Claude 폴더 공유 0명 확인: get_file_permissions(폴더 ID는 docs/drive-index/claude-folder.md). 로컬 세션만
   - 클라우드 세션(시트 커넥터 있음): `완료_` 없는 90_변경대기_* 묶음 파일의 줄을 대상 시트 셀에 반영 → 90_변경대기에 옮겨 적고 상태 '완료'·반영일 → 묶음 파일 이름 앞에 `완료_` → CURRENT_STATE H-sheet 갱신 (D-20261102-17)
3. 열린 건(#open/#waiting) → CURRENT_STATE C절. 바뀐 절만 고침, 80줄 이하
4. 계속 유효한 새 사실 → kb/facts.md(확인일), 새 결정 → decisions.md(ID), 새 조직 → kb/orgs.md
5. 이번 세션에 만든 kb 문서·skill이 kb/INDEX.md·CLAUDE.md에 있는지
6. 보고 (한 번에):
   - 틀 변경 제안 표 (무엇·왜·영향 파일) — 없으면 "없음". 승인 전엔 바꾸지 않음
   - 비효율 평가 표 (session_review.md 2절 형식)
   - 남은 일·확인 안 된 것
7. 커밋 → 작업 장소 규칙대로 push (로컬: `git pull --rebase origin main` 후 `git push origin main` / 클라우드: session_review.md 3절)
