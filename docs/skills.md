# 작업 절차(skill) 목록
<!-- skill을 만들거나 이름·부르는 말을 바꾸면 이 표도 고친다 (session-end 5단계에서 확인). 파일: .claude/skills/<이름>/SKILL.md -->

| 이름 | 부르는 말 (예) | 하는 일 | 언제 | 결정 |
|---|---|---|---|---|
| start-day | `/start-day`, "업무 시작" | 동기화 → 상태·열린 건·일정 → 메일·할 일·드라이브 변경 → 오늘 계획 승인. 맨 위에 "어제 받은 요청" | 매일 첫 세션 | D-13 |
| todo | `Todo: …`, `할일: …`, `/todo` | 말로 준 요청을 todo.md·업무 기록에 추가 (요청자·매장·기한·티켓) | 요청 받았을 때 | D-18 |
| todo-sync | "할 일 목록", "티켓 동기화" | STWS 티켓과 todo.md 맞추기, '지금' 제안, 승인된 티켓 상태 변경(Resolved까지) | start-day 안, 수시 | D-18 |
| mail-triage | "메일 확인", "메일 정리" | 3개 메일함 읽고 할 일/기다림/참고/버림 분류, 새 연락처 묻기 | start-day 안, 수시 | D-15 |
| weekly-meeting | "회의 준비", "회의 정리" | 월요일 10:00 회의록 틀 만들기 → 회의 뒤 결정·To-do 정리 | 매주 월요일 | D-23 |
| drive-index | "드라이브 색인" | 드라이브 폴더를 읽어 docs/drive-index에 색인 | 새 폴더 색인할 때 | D-16 |
| drive-check | `/drive-check`, "월초 점검" | 색인 링크의 삭제·이름·공유 변경 점검, Claude 폴더 월 백업 | 매달 첫 업무일 | D-21 |
| session-end | "마무리", "인계" | 점검표, CURRENT_STATE·결정 갱신, 비효율 평가, main에 push | 세션 끝 | D-6 |

결정 번호는 D-20261102-NN의 줄임 (docs/decisions.md).
