# CURRENT_STATE (80줄 이하, 매 세션 덮어씀)

## A. 배포
- 릴리스 없음

## B. 브랜치·진행 중
- Handoff 2026-11-04 local → cloud. For the cloud session (Drive connector):
  1. Drive address book: ~30 approved contacts queued in docs/users/hmlee/todo.md M-contact (Granite/Leverage/Lumen/Comcast/vendors, 박상후, Jason Chung). Emails must come from the original mail → write a 90_변경대기 batch only for those whose email you can get; list the rest
  2. Drive 00_profile: add job title 사원 (STWS permission Manager), supervisor Dan Choi (최철룡), Git repository admin (copy is docs/users/hmlee/profile.md)
  3. Ask user M-names (13 internal names, Gregory Roman, POS manufacturer for T-640) — user had no time 11/04

## C. Repo / framework work (personal tasks: docs/users/<id>/todo.md, D-20261103-8)
| ID | 내용 | 상태 | 맡길 곳 |
|---|---|---|---|
| H-local | 로컬 PC 통과. 드라이브 커넥터·크롬(Gmail 텍스트 OK, Outlook 화면만) 확인(2026-11-02). 클라우드 계정 커넥터 동일 여부 미확인 | 거의 완료 | 사용자 |
| H-drive1 | 내 드라이브 1차 색인 완료. **사용자 리뷰 5/5 끝**(2026-11-03). 정리 후보는 색인에 표시(사용자가 정리). 다음: (질문은 하나씩 창으로). 그 뒤 공유 드라이브·공유 문서함 | 리뷰 중 | 사용자와 함께 |
| H-multi | **틀 고민은 docs/projects/ai-system-questions.md에 모았다가 한꺼번에 결정(사용자 요청 2026-11-03, 나올 때마다 추가).** 여러 사용자 1단계 완료(D-20261102-19). 2단계(팀원 합류 때): mail_triage 0절 → users/<id>/mail_rules.md, CURRENT_STATE 개인 할 일 분리, onboarding.md. 미정: 공용 규칙 승인자, 개인 파일 공개 범위. git 이력 정리 완료(D-34) | 대기 | 사용자 |
| H-tracker | 드라이브 Task Tracker를 할 일 화면으로 관리(D-20261102-22). 업무 파악 뒤 시작: 시트 구조 읽기 → 탭 설계 사용자와 → 클라우드 계정이 갱신 | 대기 (업무 파악 후) | 지휘·클라우드 |
| H-template | 드라이브 Templates(Switchport_and_IP·Network Map) 다듬기 — 매장마다 반복할 기본 문서. Claude가 구성도·포트표 작성을 돕는 방식 함께 설계 | 대기 | 사용자와 함께 |
| H-vendors | 주요 업체 파일 생성 (업무 기록하며 생길 때마다) | 대기 | 지휘 |
| H-hooks | Lean context + supervisor hooks (PLAN-lean-context-001-draft2, D-20261103-6): steps 0–6 done 11/03. Hooks only in hmlee `.claude/settings.local.json`. Next: step 7 ~11/17 — review tools/hooks/hits.log, flip warn rules to block one by one (test_hooks.py green). Unverified: cloud session hooks, digest in a fresh session. Shared settings.json move waits for Q2 | in progress | user + 지휘 |
| H-slim | Framework slim-down D-20261103-7/-8, D-33, D-34 done 11/03; design step 0 done (find.py all docs + store aliases); docs/ARCHITECTURE.md added (snapshot via tools/repo_map.py). Freeze on new skills/decisions to 11/17. 11/17 review agenda: hooks step 7 (real false positives), store registry + optional field line, binary-file block, equipment synonyms (저울=scale), status marking, friction lines in ai-system-questions. Delete local backup USASIA_general_backup_20261103.git ~11/10 | open | hmlee |
| H-db | Work data to a DB (D-20261104-5): usasia_db Rails app live at usasia-it.duckdns.org with HTTPS + Google login (2026-11-04). Daily Drive backup done 2026-11-04 (usasia_db ops/backup.sh). Todo board live 2026-11-05 (D-20261105-1). Next: import todo.md rows, Claude API token (no delete), invite developer, Dependabot PRs #1-#3. Server history: Claude memory oracle-server-setup | open | hmlee + Claude |

## D. 확인 안 된 것
- 없음

## E. 임시값
- keywords.md 분야·종류 키워드와 동의어 표 초안
- archive 이동 주기 3개월

## F. 함정
- check.py "민감 정보 의심"은 '비밀번호' 같은 단어에도 걸림(색인의 ⚠민감 표시) → 값이 있는지만 눈으로 확인
- Outlook web: no get_page_text. Gmail inbox/sent/search: get_page_text empty → JS on tr.zA (mail-triage skill). Intranet sent list: .message-list .message-item, 100 per page, page box at bottom
- 하위 에이전트가 제목만 보고 행을 채움 → 브리프에 "모든 문서 내용 읽기, 제목 기준 금지" 명시
- 동의어 검색은 짧은 영문(PO 등)이 다른 단어 속에 걸림 → find.py가 단어 단위로 처리. 셸 awk 대신 Python 사용
- Hooks: settings edits apply after a short delay; permissions.deny is prefix-only (guard.py covers force push); Stop does not run on user interrupt

## G. 새 세션 첫 멘트
/start-day (업무 시작 루틴, D-20261102-13)

## H. 마지막 업무 시작
2026-11-04. Today: LW·GLW scales (T-606), GitHub 2FA, M2M Bon Restaurant scope, UW Grab Go estimate
- 마지막 월초 점검: 없음 (drive-check, 다음 2026-12 초)
