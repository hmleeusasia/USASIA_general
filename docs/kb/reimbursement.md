# 경비 청구(Reimbursement) 월별 정리 방법 (확인: 2026-11)

## 흐름
노션 DB "Reimbursement"(평소 기록) → 구글 시트 "Reimbursement"로 월 단위 옮김 → 영수증 폴더에서 링크 연결
- 노션: https://app.notion.com/p/24d0aac49b1680e0a2d8f30adf16e33d
- 시트: https://docs.google.com/spreadsheets/d/1MifTpXF_xGcix8ULSKGXnWDnS1pPOi76D2Nh9MmnZEU
- 영수증 폴더: https://drive.google.com/drive/folders/1nrYiVV5Nrwp9glxhdM_Vjyz8P8Gx6hx0 (코드별 하위 폴더)

## 제출
- Dan Choi 부장님 소유 공유 폴더 "Hyunmyung Lee"/Monthly 개인경비/<연도>/ 에 그 달 폴더 `YYYYMM(신청)`을 만들고 정산 시트·사용 내역을 넣는다 (회계 KF 2명 편집 공유)
- 처리 끝나면 폴더 이름을 `YYYYMM(완료)`로 바꾼다. 영수증 원본은 내 드라이브 Reimbursement/PDF/Archive/<월> 아래 WE코드 폴더
- 위치: docs/drive-index/purchase-reimbursement.md "공유 폴더" 절

## Rules → docs/rules/expense.md
R-EXP-01 (depart/arrive live), R-EXP-02 (time zone, Notion UTC), R-EXP-03 (read row back), R-EXP-04 (empty miles), R-EXP-05 (tabs, codes, lunch cap), R-EXP-06 (receipt intake), R-EXP-07 (photo in chat).

## Sheet layout and codes (data for R-EXP-05)
- Others tab A–I; Driving tab: H miles, J `=$I$1*H<row>`, rate in I1
- Codes: Meal → WE0002, Business Trip → WE0001, Parking → WE0006, Office → WE0011, Meal+Visitor → WE0003, flat trip allowance → ETC
- Flat trip allowance rows (e.g. 5 days) are not in Notion → add them separately
- New month: tick 요청여부 (requested); last month: tick 완료 (done) (Others I / Driving L)

## Daily receipt intake (agreed 2026-11-03, rules R-EXP-06/07)
- User scans with the Drive app (+ → Scan) straight into the code folder (e.g. WE0002), then says "receipt uploaded"
- Steps: find the new file → read date/amount → rename → Notion row (Unpaid) → Sheet Others row with link (요청여부/완료 FALSE until month-end)
- Meal receipt: Notion Doc name "점심", Category Meal, code WE0002
