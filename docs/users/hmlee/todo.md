# 내 할 일 (todo.md)
갱신: 2026-11-04 · STWS 동기화: 2026-11-02 (담당 47건, 안 끝난 33건) · 규칙: D-20261102-18, 절차: todo-sync skill
<!-- 기한은 요청에 있을 때만 적는다(없으면 기한 없음). 원본은 이 파일. STWS는 보고용(상태 변경은 사용자가 직접). 장기 프로젝트는 따로 관리, 관련 있으면 이름만. 민감 값 금지 -->

## 1. Now (Claude suggests, user picks) — visit plan set 2026-11-03
| Day | ID | Task | Store |
|---|---|---|---|
| next FW visit | — | Deliver 1 scale picked up at InStore 11/03 (ticket?) | FW |
| Thu 11/05 AM | M-uw-grabgo-cable | Review UW Grab Go (Deli) cable estimate (ITSolution) → store manager; create STWS ticket | UW |
| Thu 11/05 | T-362 | NVR app: view DH cameras with MW (due 11/06) | DH·MW |
| Thu 11/05 | T-639/T-603, T-375 | Install manager PC (arrived 11/03), Wi-Fi dead zone / AP | MW |
| Any | M-wifi, M-granite, T-295+T-285 | Wi-Fi adapter, Granite account, EGMM internet vendor | office |

## 2. 전체 목록
상태: 할 일 / 진행 / 기다림(대상) / 끝 / 취소 · 움직임 = 마지막 업데이트(STWS 또는 기록) · ⏸ = 30일 넘게 안 움직임
| ID | 할 일 | 매장 | 분야 | 상태 | 움직임 | 다음 |
|---|---|---|---|---|---|---|
| M-uw-grabgo-cable | UW Grab Go estimate = UW Deli (separate building across the street): extend 4 cables. Vendor: ITSolution (Eric Kang). Estimate received 11/03 (Outlook) | UW | #network #vendor | 할 일 | 2026-11-04 | Thu 11/05 AM: review quote → forward to store manager; create STWS ticket (UW- Deli cable 4 extension) |
| T-619 | POS 시리얼 번호 기록 | BV | #pos | 진행 | 2026-11-04 | Survey done 11/03. STWS In progress (11/04, user): parent cannot be set to Resolved while subtask T-640 is open (tried 11/04). Resolve after T-640 |
| T-624 | POS 포인트 카드 테스트 (+ 하위 TICKET-635 smart card 스캔 테스트, James Yoo 생성 11/02) | BV | #pos | 끝 | 2026-11-04 | STWS Resolved 11/04 (user closes). BV 방문 때 함. 가기 전 James Yoo 과장님께 미리 연락. 블록한 스마트 포인트 카드가 POS에서 어떻게 막히고 찍히는지 + 미등록 smart card 스캔 시 POS 반응(11/03 추가) + 간단한 기타 테스트 |
| M-bv-printer | BV: 1st-floor printer drops connection often — investigate (new request 11/03). Ticket needed? | BV | #hardware #network | 대기 | 2026-11-03 | 11/03: no problem seen on site. Re-check next BV visit (wired/Wi-Fi, IP, sleep, port) |
| T-640 | BV: send POS manufacturer serial numbers per lane for receipt printer, cashier touch screen, scanner scale (manufacturer request, name TBD). Subtask of T-619, created 11/04 | BV | #pos #asset | 할 일 | 2026-11-04 | Collect on next BV visit if not in T-619 survey, then reply to the manufacturer |
| T-641 | Ballard: check how smart card #0012 (new H-mart point card, GBK) scans on POS. Created 11/04 | BL | #pos | 할 일 | 2026-11-04 | Requested by user 11/04 |
| T-585 | 새 CS 컴퓨터 세팅 | BV | #hardware | 할 일 | 2026-10-15 | |
| T-565 | PIN Pad Tap 스티커 붙이기 | BV | #pos | 할 일 | 2026-09-20 ⏸ | 진행: BV 방문 때 T-624와 함께 (11/03) |
| T-438 | POS 저울 유선 설치 | BV(구) | #pos | 진행 | 2026-11-03 | 아직 남음 (11/03 확인). Scales needing wired link: seafood FISH70, FISH71; meat MEAT73; produce PROD76 (11/03). Survey done 11/03; install = separate visit, schedule TBD |
| T-500 | Lumen 회선 개통 | BV(구) | #network | 진행 | 2026-11-03 | 아직 남음. Lumen 연락 없음 → Lumen에 재스케줄 확인 필요 (11/03) |
| T-606 | 델리 저울 고장 | LW | #pos | 진행 | 2026-11-04 | 11/04: 2 repaired scales delivered & set up; 1 still faulty (label feed fails, gap not detected mid-roll) → send back to InStore for re-repair. Keep open |
| T-486 | 델리 저울 연결 문제 | LW | #pos | 끝 | 2026-11-04 | Same issue as T-606, resolved 11/04. Close in STWS |
| T-579 | CS PC 교체 | LW | #hardware | 기다림(매장 구매) | 2026-11-04 | 11/04: store will buy new PCs → set up 2 new PCs (likely 1 store manager, 1 accounting — to confirm; spec given to store 11/04: Windows 11 Pro, 32GB RAM), then set up a leftover PC for CS |
| T-515 | 레이블 PC 파일 이상 | LW | #hardware | 할 일 | 2026-09-08 ⏸ | 진행: 이번 주 LW 방문 때 (11/03) |
| T-587 | 저울 문제 + PC 이동 지원 | GLW | #pos | 끝 | 2026-11-04 | Done 11/04: PC move + extra PC move/install, repaired scale installed, Soundtrack moved to new PC. Close in STWS |
| M-glw-scale-repair | GLW: send 1 extra Ishida scale for repair to InStore Technology (new 11/04). Ticket needed | GLW | #pos #vendor | 할 일 | 2026-11-04 | Create STWS ticket; arrange InStore pickup/repair |
| M-glw-touch | GLW: PC touchscreen phantom touches (ripple marks, random clicks, lost control) 11/04. Cause: touchscreen fault | GLW | #hardware | 할 일 | 2026-11-04 | Confirm fix (disable touch / replace monitor?) |
| T-386 | 컴퓨터 구입·Laptop 세팅 | GLW | #hardware | 기다림(매장) | 2026-11-03 | Pending 11/03 |
| T-603 | PC 급격히 느려짐 | MW | #hardware | 진행 | 2026-10-22 | 서브 T-639 |
| T-639 | MW 점장 PC 느려짐 → 새 PC 구입, 매장에서 설치. T-603 연장. 서브 티켓 TICKET-639 | MW | #hardware #install | 진행 | 2026-11-03 | 새 PC가 매장에 도착(11/03). 설치는 목 11/05 MW 방문 때 |
| T-375 | Wifi dead zone 확인·AP 추가 | MW | #network | 진행 | 2026-08-20 ⏸ | 진행: 오늘 MW에서 (11/03 판단) |
| T-362 | NVR 앱 재설정: DH 카메라를 NVR 앱에서 MW와 함께 보기. 이준호 점장(MW·DH 겸임) 2026-11-03 재촉 | DH·MW | #security | 진행 | 2026-11-03 | 기한 2026-11-06(이번 주, 사용자 추정) |
| T-600 | Comcast BB 연결 지원·카메라 설치 설계 | IQ | #network | 진행 | 2026-10-15 | |
| T-461 | 2번 스위치 33번 포트 CRC 에러 | RM | #network | 진행 | 2026-08-13 ⏸ | 미루기: 원격 확인 가능하면 진행 (11/03) |
| T-340 | 광 네트워크 연장 | RM | #network | 진행 | 2026-07-17 ⏸ | 미루기: 공사 건 (11/03) |
| T-302 | VoIP/전화 빌링 정리 | RM | #phone | 진행 | 2026-08-03 ⏸ | 미루기: 서류 일 (11/03) |
| T-392 | PC 이동 지원 | RM | #hardware | 기다림(재요청) | 2026-11-03 | Pending 11/03: 케이블 공사 필요, 보류. 다시 요청 오면 시작 |
| T-223 | Extra UPS 설치 | FW | #infra | 기다림(?) | 2026-06-16 ⏸ | 미루기 (11/03) |
| T-569 | PC 부팅/화면 안 나옴 | M2M | #hardware | 할 일 | 2026-10-08 | |
| T-385 | DHCP 이상 | CP | #network | 진행 | 2026-11-03 | 아직 남음: 네트워크 물리 분리 필요 (11/03 확인) |
| T-295 | 본부 인터넷 속도 증가 | 본부 | #network | 기다림(?) | 2026-10-22 | 업체 재확인 |
| T-285 | 본부 인터넷 미지불 비용 | 본부 | #network | 진행 | 2026-06-26 ⏸ | 진행: T-295와 함께 업체 확인 (11/03) |
| T-439 | 원격 프로그램 권한 추가 | 사업본부 | #software | 진행 | 2026-09-22 ⏸ | 확인 (11/03) |
| M-wifi | 데스크탑용 Wifi 어댑터 구입 | ? | #hardware | 진행 | 2026-10-22 | 티켓 없음 (log 2026-11-02) |
| M-granite | Granite 계정 생성 | — | #network | 진행 | 2026-10-19 | 티켓 없음 (log 2026-11-02) |
| T-637 | NWHQs PC 이동: 2층 PC → 1층, 1층 대기 PC 설치, 1층 사용 중 PC → 2층. 새 직원 오기 전. 요청 인신희 HR 팀장 | NWHQs | #hardware #install | 할 일 | 2026-11-03 | 기한 2026-11-30 |
| T-638 | LW 2층 사무실에 보관된 고장 저울 정리: Tommy Song(송대호) 님과 상의 → 필요한 부품 확보 → 폐기. 요청 Chris Kim 총무 | LW | #pos #hardware #asset | 할 일 | 2026-11-03 | 다음: 송대호 님과 상의 |

## 3. Follow-ups without a ticket (moved from CURRENT_STATE C, 2026-11-03)
| ID | Item | Status | Who |
|---|---|---|---|
| M-share | 공유 정리 후보 검토 (드라이브 Claude 폴더 30_드라이브 공유 점검) — 비밀번호 문서 외부 공유 등. 추가 후보: Ballard 캐셔 명단(낡은 문서, 비밀번호 포함)이 개인 Gmail 2명에 편집 공유 → 공유 해제·삭제 후보. 정리 후보 표시 문서들(색인 "정리 후보") | 대기 | 사용자 |
| M-mail | 메일 분류 첫 검토 완료(mail_triage.md 1절 규칙 8개, 2026-11-02). 남은 할 일: Wifi 어댑터 구입, Granite 계정 생성 (log/2026/2026-11-02_hmlee.md). 미확인 조직: KRM·Daifuku·SSP·beOne | 진행 중 | 사용자 |
| M-collect | 숙제: 기존 드라이브 문서(IT Information, Comcast Information 등)의 계정·회선 정보를 Claude 폴더 20_계정·회선으로 모으기 | 대기 | 사용자와 함께 |
| M-contact | Add to Drive address book (local session, approved 11/03): Jason Chung (정훈희), GBK, POS contact — email from his mail; 박상후 Sanghu Park, 마트지원본부 (EGMM) 차장/팀장 (approved 11/04) — email from M2M Bon Restaurant mail; Granite DIA contacts approved 11/04 (Valentina Castaneda, Daniel Leonard, Brendan Cook, Bill Dehoop, Shantell Campbell, Katie Kemp — Granite; Tae Lee, Lee Seto — Leverage; Ann Jacobson — Lumen; Micheline Lucero — Outsource Inc.) — emails from Gmail Granite threads; Outlook May–Jul contacts approved 11/04 (Coley Levin — Lumen; Christina Starr — Comcast; Mark Head — CP firewall mgmt; Julie Sinecio — 2nd Ave building owner; Danny Kim — GBK network). Gregory Roman (Comcast?) needs confirmation first; Nov–Apr contacts approved 11/04 (Silas Schroeder — Cannon; Robert Dill — Aspiretransforms; Jeremiah Hammett — Zayo; William Horbatt, Shaun Smith — Comcast; Mike Russell — Lumen billing; Yancy Yang — FS.com; Peyton Thiel — Dell; 이재호, 이동훈 — Hana Solution; 맹채윤 — H Mart UW accounting). Not 권오혁 (left the company) | 대기 | 로컬 |
| M-names | Ask user who these are (intranet sent review 11/04): 이원재, 장상도, 이성수, 심미순, 한승표, 양창우, 문기성, 이태호, 권상우, Jin Kim, Jane Lim, Eunhong Lee, LWADMIN. Also Gregory Roman (Comcast?), POS manufacturer name for T-640 | waiting | user |
| M-todo | Board docs/users/hmlee/todo.md. Visit plan in "Now": Tue 11/03 BV (call James Yoo first, T-624), Wed 11/04 Lynnwood (T-606 due 11/06), Thu 11/05 MW·DH (T-362 due 11/06, T-639 install). STWS cleaned 11/03 (5 Resolved, 1 Cancelled → user Closes). T-639 description in STWS needs fix ("PC arrived, install 11/05") | in progress | user |
| M-iq | IQ temp cameras (T-600): reply sent to John Byun 11/03 2PM with 2 Phase-1 quotes (Drive 06_Files/Quotes/IQ). Waiting John: outlets, option. Ask ITSolution Eric: camera models, wired-option recording. Later: John Byun, Kevin Donald → address book? | waiting | user |
| M-m365 | Microsoft 365 커넥터: 관리자 모름 → entra.microsoft.com 전역 관리자 확인 | 대기 | 사용자 |
| M-reimb | 10월 경비 청구 시트·노션 반영 완료. 남은 것: 노션 마일 6건, Yi's 금액, 렌트비 Note, Driving 시각 서식. 11월부터 매일 기록 방식(kb/reimbursement.md "Daily receipt intake"): 영수증은 Drive 스캔 → 말하면 Claude가 노션·시트·링크, 운행은 출발/도착 말하면 노션+Driving 탭 | 진행 중 | 사용자·클라우드 |
| M-bv | BV 11/03 방문 끝. 대기: GBK 답(B062 500불 근처 오버라이드 안 됨), 1층 프린터 재확인, T-438 저울 4대 유선 설치 일정, T-565·T-585·T-500 | 대기 | 사용자 |
| M-overview | Work overview from Outlook sent mail Aug–Oct (kb/work_overview.md). Gmail/intranet sent not read. Ask user: BV Lumen cutover, RM fiber uplink, STI warehouse, GFC VoIP, Smart Point — done? | waiting | user |

## 3a. 참고 (내 담당 아님, 내가 올린 티켓)
| ID | 할 일 | 담당 | 상태 |
|---|---|---|---|
| T-625 | MW POS 문의(임의 생성 상품·가격 변동) | Dan Choi | 할 일 |

## 4. 동기화 메모
- 2026-11-02 T-556 → Resolved (Claude가 반영, 시험 성공) → Closed (확인창은 사용자가 누름)
- 2026-11-02 첫 동기화. ⏸ 18건 → 사용자 판단 필요(닫기/미루기/진행)
- 2026-11-03 ⏸ 18건+3건 판단(사용자 '제안대로'): 진행 5 · 미루기 5 · 확인 후 닫기 11. 닫기는 사용자 확인 뒤 STWS Resolved
- 2026-11-03 확인 11건: Resolved 5(368·437·268·493·402) · Cancelled 1(323) · Pending 2(392·386) · 계속 3(438·500·385). STWS 반영 완료, Close는 사용자
