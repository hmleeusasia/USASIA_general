# Granite DIA  (태그: #proj-granite-dia)
<!-- 이력 표를 손으로 쓰지 않는다. 이력은 아래 명령으로 기록에서 찾는다.
     금지: 금액·계약 조건 -->

- 개요: Granite를 통한 매장별 DIA(전용 인터넷) 회선 설치·청구 관리. 중개는 Leverage Cloud Solutions (kb/orgs.md)
- 대상 매장: Lynnwood, University Way, Bellevue, Redmond, Federal Way, Lakewood (드라이브 진행 현황 시트 기준)
- 알려진 것 (드라이브 색인·회의록에서):
  - Lynnwood 개통 완료 (2026-05-14 개통 확인서, 회선은 Ziply Fiber)
  - 일부 매장 취소 (이중화 불가·공사비)
  - 2026-08 회의: UW/BV 광패치 비용 문의 / 2026-09 회의: 청구는 되는데 LW만 사용 가능 / 2026-10 회의: Granite BV 제안
  - 할 일: Granite 계정 생성 (M-granite, 2026-10-19)
- 목표: 매장 회선 이중화 (기존 회선을 바꾸는 경우도 있음). 새 회선이 들어오는 과정을 추적하고, 문제가 생기면 기록하고 해결 방법을 찾는다
- 기간: 장기. 시작은 2026년 중반쯤(6개월 안쪽, 정확한 날짜 기억 안 남) ~ 모든 대상 매장에 Granite이 들어가면 끝
- 매장별 현재 단계의 원본: 드라이브 진행 현황 시트 (저장소에 단계 표를 따로 두지 않음)

## 기록하는 법
- 업무 기록에 `### 제목  #network #<종류> #proj-granite-dia #open` 한 건씩 남긴다
  - 설치 진행(주문·현장 조사·공사·개통): `#install`
  - 문제(지연·불통·속도·장애): `#outage` 또는 `#support`. 본문에 증상 → 원인 → 해결 순서로
  - 청구 문제: `#billing`
- 매장 이름은 본문에 쓴다 (매장 허브가 생기면 #store- 태그 추가)
- 해결 방법이 다음에도 쓸 만하면 `#tip`을 붙여 kb 후보로
- 결정 ID: —
- 드라이브 원본:
  - 진행 현황 시트 Granite DIA Installation: https://docs.google.com/spreadsheets/d/1HUUBKRUlChxjPFUrTl6gNGP1OLxi8X1hIpi3yNuN2u8/edit
  - DIA 계약 사본 (⚠금액): https://drive.google.com/file/d/1KM2YF7FcPabRUq61qjqZhPL9WbmWL0lQ/view
  - Lynnwood 개통 확인서: https://drive.google.com/file/d/1XFVfFIf4Ppalu40vN0zK-RAwIP2fgiL0/view
  - 관련 회의록: docs/drive-index/meeting-templates-programs.md (080326, 092126, 101226)

## 이력
`python3 tools/find.py "#proj-granite-dia"`
