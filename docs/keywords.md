# 키워드 표준 목록

규칙
- 태그는 건별 소제목 줄에만 붙인다 (`### 제목  #a #b`). 이 줄이 검색 기준.
- 3갈래 고정: 분야 1개 이상 + 종류 1개 이상 + 대상(해당 시). 목록 밖 태그는 여기 먼저 추가.
- 대상 태그(#vendor- #store- #asset- #proj-)는 허브 파일이 있을 때만 쓴다. 파일명 = 태그 뒷부분 (#vendor-granite → docs/vendors/granite.md)
- 검사: `python3 tools/check.py`

## 분야
#network #infra #dev #pos #store-ops #security #phone #software #hardware #general

## 종류
#billing #invoice #purchase #expense #contract #asset #vendor-mgmt #paperwork #support #outage #install #decision #schedule #tip #meeting #email

## 상태
#open #waiting #done   (닫을 때 원래 건 줄의 #open을 #done으로 고친다)

## 동의어 (검색 시 python3 tools/find.py가 자동으로 함께 찾음)
| 태그 | 같은 뜻 |
|---|---|
| #demarc | demarcation point, demarc, MPOE, 인입점 |
| #phone | landline, 유선전화, POTS, 전화선 |
| #billing | bill, 청구, 요금 |
| #invoice | 인보이스, 청구서 |
| #purchase | 구입, 구매, PO, 발주 |
| #expense | 개인 비용, reimbursement, 경비 |
| #contract | 계약, 갱신, renewal |
| #outage | 장애, 다운, down |
