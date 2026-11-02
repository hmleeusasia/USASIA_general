# CLAUDE.md

작업 원칙: **docs/project_instructions.md** 를 따른다 (이 파일은 저장소별 설정만 담는다).

## 세션 시작 순서
1. 이 파일 → `docs/CURRENT_STATE.md` → `docs/kb/facts.md` 전부 읽기
2. 할 일·등급(가벼움/무거움)·맡을 곳을 한 번에 알리고 승인받기
3. 끝날 때: CURRENT_STATE 바뀐 절만 고침(80줄 이하), 새 결정은 `docs/decisions.md`, 커밋·push → **main에 합치고 push** (D-20261102-6)

## 저장소 개요
- USASIA 마트(미국 워싱턴주, 여러 매장) IT 부서 업무 기록·색인 저장소
- 주 업무: ① 구글 드라이브 문서 색인(요약·키워드·링크) ② 이메일 작성 지원 + 날짜별 업무 기록(업체·결정·일정·팁)
- **원본·민감 정보는 구글 드라이브, GitHub엔 2차 문서만** → docs/storage_rules.md 필수 준수

## 문서 위치
| 종류 | 위치 | 템플릿 |
|---|---|---|
| 날짜별 업무 기록 | docs/log/YYYY/YYYY-MM-DD.md | docs/templates/daily_log.md |
| 허브(업체·매장·자산·프로젝트) | docs/{vendors,stores,assets,projects}/<이름>.md | docs/templates/{vendor,store,asset,project}.md |
| 일정·갱신·만료 | docs/calendar.md | — |
| 드라이브 색인 | docs/drive-index/<주제>.md | docs/templates/drive_index.md |
| 키워드 표준 | docs/keywords.md | — |
| 오래된 기록 | docs/archive/YYYY/ | — |

## 작업 규칙
- 업무 기록: 건마다 `### 제목  #분야 #종류 #대상` 한 줄이 검색 기준 (keywords.md 규칙)
- 허브는 관련 건이 처음 생길 때 만든다. 허브에 이력 표를 손으로 쓰지 않는다(검색 명령으로 대체)
- 결정 설명은 decisions.md에만, 기록에는 ID만. 날짜는 기록 건 본문이 원본(YYYY-MM-DD), calendar.md는 반복·장기 일정만 (D-20261102-11)
- 열린 건(#open/#waiting)은 세션 끝에 CURRENT_STATE C절에 반영
- 민감 정보 발견 시 빼고 "드라이브 보관 추천" 알림
- 드라이브 색인은 폴더 단위로 나눠 진행, 대량 읽기는 작은 모델 하위 에이전트에 맡김
- 세션 끝: docs/session_review.md 점검표 수행 후 비효율 평가 표 보고

## 작업 장소 (D-20261102-12)
| 장소 | 시작 | 브랜치 | 끝 |
|---|---|---|---|
| 클라우드 세션 | 자동 클론(main) | claude/* | push → main에 fast-forward 합침 |
| 로컬 PC (Claude Code·Cowork) | `git pull origin main` | main에서 바로 | 커밋 → `git push origin main` |
- 한 번에 한 곳에서만 작업 (동시 작업 시 충돌). 작업 단위마다 커밋, 세션 끝 push 필수
- 도구는 Python만 필요 (`python3 tools/find.py`, `python3 tools/check.py`). Windows에서는 `py` 또는 `python`

## 드라이브 색인 (크롬 화면 공유 방식)
- PC 드라이브의 구글 문서·시트는 바로가기(.gdoc/.gsheet)라 본문 없음 → 크롬으로 연다
- 사용량 절약: 문서 주소 `/edit...` → `/export?format=txt` (시트는 `/export?format=csv`)로 텍스트만 받기. 스크린샷 읽기 최소화
- 목록은 드라이브 검색 화면에서 한 번에, 긴 문서는 앞부분·목차만, 5~10개 단위로 끊어 커밋
- 색인 링크는 웹 주소(https://drive.google.com/...), PC 경로(G:\...) 금지

## 질문 유형별 먼저 볼 곳
| 질문 | 먼저 볼 곳 |
|---|---|
| 지금 상태·할 일 | docs/CURRENT_STATE.md |
| 과거 결정 이유 | docs/decisions.md |
| 업무 지식·팁 | docs/kb/INDEX.md |
| 과거 업체 일 | docs/vendors/INDEX.md → 업체 파일 |
| 특정 키워드·업체·일 | `python3 tools/find.py Granite demarc` (동의어 자동, AND) |
| 열린 건·기한초과 | `python3 tools/find.py --open` |
| 다가오는 일정(30일) | `python3 tools/find.py --due` |
| 드라이브 문서 찾기 | docs/drive-index/INDEX.md |
| 진행 중 계획 | docs/requests/ |

## 저장소별 설정 (임시값 — 정해지면 교체)
- 시험·빌드:          해당 없음 (문서 저장소). 점검은 python3 tools/check.py + session_review.md
- 검색 도구:          python3 tools/find.py <단어...>
- 문서 점검:          python3 tools/check.py (미등록 태그·허브 없는 태그·민감 정보 의심·줄 수)
- 지식 문서 시작점:   docs/kb/INDEX.md
- 작업 브랜치 규칙:   claude/* 브랜치에서 작업, 세션 마무리 때 main에 합침(fast-forward). 그 밖의 병합은 요청 시에만
- 사용자 언어·말투:   한국어, 결론 먼저, 표 활용
