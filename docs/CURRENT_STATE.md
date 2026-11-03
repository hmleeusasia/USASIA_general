# CURRENT_STATE (80줄 이하, 매 세션 덮어씀)

## A. 배포
- 릴리스 없음

## B. 브랜치·진행 중
- 없음 (claude/wonderful-brahmagupta-5nf6ku main에 합침)

## C. 할 일
| ID | 내용 | 상태 | 맡길 곳 |
|---|---|---|---|
| H-local | 로컬 PC 통과. 드라이브 커넥터·크롬(Gmail 텍스트 OK, Outlook 화면만) 확인(2026-11-02). 클라우드 계정 커넥터 동일 여부 미확인 | 거의 완료 | 사용자 |
| H-drive1 | 내 드라이브 1차 색인 완료. **사용자 리뷰 3/5 끝**(Ongoing·ITIL·Meeting, 2026-11-02). 다음: purchase-reimbursement.md → archive-saves.md (질문은 하나씩 창으로). 그 뒤 공유 드라이브·공유 문서함 | 리뷰 중 | 사용자와 함께 |
| H-share | 공유 정리 후보 검토 (드라이브 Claude 폴더 30_드라이브 공유 점검) — 비밀번호 문서 외부 공유 등. 추가 후보: Ballard 캐셔 명단이 yksccl(Comcast·Cannon 쪽 추정)에 편집 공유. 정리 후보 표시 문서들(색인 "정리 후보") | 대기 | 사용자 |
| H-mail | 메일 분류 첫 검토 완료(mail_triage.md 1절 규칙 8개, 2026-11-02). 남은 할 일: Wifi 어댑터 구입, Granite 계정 생성 (log/2026/2026-11-02_hmlee.md). 미확인 조직: KRM·Daifuku·SSP·beOne | 진행 중 | 사용자 |
| H-collect | 숙제: 기존 드라이브 문서(IT Information, Comcast Information 등)의 계정·회선 정보를 Claude 폴더 20_계정·회선으로 모으기 | 대기 | 사용자와 함께 |
| H-sheet | 드라이브 시트 수정 대기 4묶음(90_변경대기_2026-11-02_1~_3, 2026-11-03_1, 주소록 15줄). 클라우드 계정이 반영 (D-20261102-17) | 대기 4 | 클라우드 |
| H-todo | 할 일 보드 docs/users/hmlee/todo.md. **2026-11-02 받은 요청 4건 → 다음 start-day 맨 위에 알림**: T-606 LW 저울(~11/06), M-nwhq-pc NWHQs PC 이동(~11/30), M-lw-scale-junk LW 고장 저울 폐기, T-624 BV 포인트 카드 테스트(BV 갈 때 James 과장님께 연락). 티켓 작성 필요 2건(M-). ⏸ 18건 판단·'지금' 확정 남음 | 진행 중 | 사용자 |
| H-multi | 여러 사용자 1단계 완료(D-20261102-19). 2단계(팀원 합류 때): mail_triage 0절 → users/<id>/mail_rules.md, CURRENT_STATE 개인 할 일 분리, onboarding.md. 미정: 공용 규칙 승인자, 개인 파일 공개 범위. 팀원 합류 전 git 이력 정리(예전 이메일 주소·sharing-review.md, 강제 push 필요) 여부 결정 | 대기 | 사용자 |
| H-m365 | Microsoft 365 커넥터: 관리자 모름 → entra.microsoft.com 전역 관리자 확인 | 대기 | 사용자 |
| H-reimb | 10월 경비 청구 시트·노션 반영 완료. 남은 것: 노션 마일 6건, Yi's 금액, 렌트비 Note, Driving 시각 서식 (log 2026-11-02, kb/reimbursement.md) | 진행 중 | 사용자 |
| H-tracker | 드라이브 Task Tracker를 할 일 화면으로 관리(D-20261102-22). 업무 파악 뒤 시작: 시트 구조 읽기 → 탭 설계 사용자와 → 클라우드 계정이 갱신 | 대기 (업무 파악 후) | 지휘·클라우드 |
| H-template | 드라이브 Templates(Switchport_and_IP·Network Map) 다듬기 — 매장마다 반복할 기본 문서. Claude가 구성도·포트표 작성을 돕는 방식 함께 설계 | 대기 | 사용자와 함께 |
| H-vendors | 주요 업체 파일 생성 (업무 기록하며 생길 때마다) | 대기 | 지휘 |

## D. 확인 안 된 것
- 없음

## E. 임시값
- keywords.md 분야·종류 키워드와 동의어 표 초안
- archive 이동 주기 3개월

## F. 함정
- check.py "민감 정보 의심"은 '비밀번호' 같은 단어에도 걸림(색인의 ⚠민감 표시) → 값이 있는지만 눈으로 확인
- Outlook 웹 get_page_text 불가, Gmail 검색결과 화면도 get_page_text 비어 나옴 → start-day skill 참고
- 하위 에이전트가 제목만 보고 행을 채움 → 브리프에 "모든 문서 내용 읽기, 제목 기준 금지" 명시
- 동의어 검색은 짧은 영문(PO 등)이 다른 단어 속에 걸림 → find.py가 단어 단위로 처리. 셸 awk 대신 Python 사용

## G. 새 세션 첫 멘트
/start-day (업무 시작 루틴, D-20261102-13)

## H. 마지막 업무 시작
2026-11-03
- 마지막 월초 점검: 없음 (drive-check, 다음 2026-12 초)
