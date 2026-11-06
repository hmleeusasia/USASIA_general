---
name: start-day
description: USASIA IT 업무 시작 루틴. 저장소 동기화, 상태·열린 건·일정 확인, Gmail·Outlook 새 메일과 드라이브 변경을 훑어 오늘 할 일 표를 만들고 승인받는다. "업무 시작", "아침 루틴", "/start-day" 때 사용.
---

# 업무 시작 루틴 (start-day)

읽기만 한다. 메일 보내기·지우기·이동, 드라이브 수정·공유 변경은 하지 않는다. Exception: the approved 05_Inbox → 06_Files move in step 5-1 (D-20261106-4).
결론 먼저, 표로 보고한다(한국어).

## 0. Minimal start (D-20261103-8)
- If the user only wants to pick up work ("짧게", "빠른 시작", a specific task named, or start-day already ran today): use the `[digest]` + docs/users/<id>/todo.md "Now" table only, show today's rows, and stop. No mail, Drive changes, or STWS — but still run step 5-1 (05_Inbox) when the Drive connector is available (D-20261106-4).
- Full routine below: first session of the day, or when asked.

## 0a. 장소 확인
- 로컬 PC(Windows, 크롬 확장 연결됨) → 아래 전부
- 클라우드 세션 → 1~3, 6만 (크롬 없음. 드라이브는 커넥터가 있으면 5·5-1도). C절 H-sheet가 1건 이상이면 90_변경대기 반영을 오늘 할 일 맨 앞에 (D-20261102-17)

## 1. 동기화
- 로컬: `git pull origin main` (충돌·미커밋 변경 있으면 멈추고 보고)

## 2. 상태 읽기
- CLAUDE.md → docs/CURRENT_STATE.md → docs/kb/facts.md
- CURRENT_STATE의 "마지막 업무 시작"을 기준일로 쓴다 (없으면 7일 전)

## 3. 열린 건·일정
- `py tools/find.py --open` (기한초과 표시 확인)
- `py tools/find.py --due` (30일 일정)

## 4. 메일 (기준일 이후만)
- mail-triage skill 절차대로 3개 메일함(받은편지함+보낸편지함) 점검·분류

## 4-1. 할 일
- 먼저: 어제(지난 업무일) todo skill로 받은 요청(todo.md 2절, 움직임=그날 M-건·덧붙인 T-건)을 보고 맨 위 "어제 받은 요청"으로
- todo-sync skill로 STWS 동기화 → "지금" 제안

## 4-2. 월요일 회의
- 월요일(10:00 회의 전)이면 weekly-meeting skill A(회의록 틀 만들기)를 오늘 할 일 맨 앞에 제안. 지난주 회의록이 아직 정리 안 됐으면 B도 (D-20261102-23)

## 4-3. 월초 점검
- CURRENT_STATE H절 "마지막 월초 점검"이 이번 달이 아니면 drive-check skill 실행을 오늘 할 일로 제안 (D-20261102-21)

## 5. 드라이브 변경
- 드라이브 커넥터 search_files: `modifiedTime > '<기준일>T00:00:00Z'`, excludeContentSnippets true
- docs/drive-index에 없는 새 문서·바뀐 문서를 표로 (색인 갱신 후보)

## 5-1. 05_Inbox (D-20261106-4)
- Folder ID: docs/drive-index/claude-folder.md (05_Inbox row). search_files `parentId = '<05_Inbox ID>'` — all files, no date filter (anything there is unfiled).
- Search fails or no connector → say so in one line and skip.
- Read each file, say what it is (ask the user if unclear) and which todo row it belongs to, propose a 06_Files/<Type>/<target> location (D-20261103-4). Move only after the user approves; then add the row to claude-folder.md "06_Files 내용" and the location to the todo row. No amounts or contacts in the repo.

## 6. 보고·승인
한 번에 보고:

| 구분 | 건 | 기한/날짜 | 제안 |
|---|---|---|---|
| 기한초과·열린 건 | | | |
| 30일 일정 | | | |
| 할 일 (todo-sync) | 새 티켓·해결 제안(Resolved)·⏸ | | "지금" 제안 |
| ⚠·기한·긴급 메일 | | | 맨 위 |
| 새 업무 메일 (할 일/기다림/참고) | | | 기록·답장 초안 등 |
| 새 연락처·조직 후보 | | | 승인 시 주소록·orgs.md |
| 드라이브 변경 | | | 색인 갱신 여부 |
| 05_Inbox | 파일 수·종류 | | 06_Files 분류 위치 |
| 월초 점검 | 이번 달 했는지 | | 안 했으면 drive-check |

그다음 오늘 계획(할 일·등급 가벼움/무거움·맡을 곳)을 제안하고 승인을 받는다.
승인 뒤 CURRENT_STATE의 "마지막 업무 시작" 날짜를 오늘로 고친다.

## 사용량 메모
- 이 루틴은 새 세션 첫머리에 돌린다(긴 세션일수록 호출 1번 비용이 큼)
- 크롬 동작은 가능하면 browser_batch로 묶는다. Browser rules: docs/kb/browser.md (no `computer scroll`, text before screenshots)
- Microsoft 365 커넥터가 승인되면 Outlook 단계를 커넥터로 바꾼다
