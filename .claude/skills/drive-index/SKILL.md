---
name: drive-index
description: 구글 드라이브 폴더를 커넥터로 읽어 문서별 목적·담긴 정보·대상·공유 상태·링크를 docs/drive-index에 색인. 하위 에이전트 병렬 분담과 재작업 방지 브리프 포함. "드라이브 색인", "문서 정리", "드라이브 리뷰" 때 사용.
---

# 드라이브 색인 (drive-index)

## 절차
1. 대상 폴더를 정하고 크기를 본다(search_files `parentId = '<id>'`). 폴더 묶음 3~5개로 나눔
2. 묶음마다 sonnet 하위 에이전트 1개, 병렬. 아래 브리프를 그대로 주고 출력은 scratchpad의 idx_<묶음>.md
3. 돌아온 결과 점검: "제목 기준"·"미확인"·일반 문구 반복이 많으면 그 부분만 되돌려 보냄 (D-20261102-14)
4. 민감 값 스캔(금액·IP·전화·비밀번호 패턴) → docs/drive-index/<묶음>.md 로 옮기고 INDEX.md 갱신 → check.py → 묶음별 커밋
5. 넓게 공유된 민감 문서는 본인 드라이브 Claude 폴더 30_드라이브 공유 점검에 추가(저장소엔 건수만) (공유 변경은 사용자가)

## 하위 에이전트 브리프 (그대로 붙여 넣기)
**모든 문서를 실제로 읽는다. 제목만 보고 쓰기 금지(사진·영상·바이너리만 예외). nextPageToken이 없어질 때까지 따라간다.**


Task: index every file in the Google Drive folder(s) assigned to you, at every depth. Use Google Drive MCP tools (load with ToolSearch "select:mcp__c43fb702-b4ed-4d33-b91f-703b5da9d14e__search_files,mcp__c43fb702-b4ed-4d33-b91f-703b5da9d14e__read_file_content,mcp__c43fb702-b4ed-4d33-b91f-703b5da9d14e__get_file_metadata,mcp__c43fb702-b4ed-4d33-b91f-703b5da9d14e__get_file_permissions"). STRICTLY READ-ONLY: never create/update/copy/share/trash.

Listing: search_files `parentId = '<folderId>'`, pageSize 100, excludeContentSnippets true; follow nextPageToken until absent (short pages may still have a token). Recurse into every subfolder.

Reading (save context): for each file call get_file_metadata with snippetVerbosity "MEDIUM" — usually enough to know purpose. Only call read_file_content if the snippet is unclear. Images/drawio/zip/video: index from title + folder only. Near-duplicate files (backups, "Copy of", v1/v2) may share one row: list them together.

Output: write to the output file named in your prompt, appending as you go (write after each folder so nothing is lost). Korean. Format:

## <폴더 경로>
| 문서 | 목적·요약 | 담긴 정보 | 대상 | 공유 | 키워드 | 수정일 | 링크 |
|---|---|---|---|---|---|---|---|

- 목적·요약: what the document is for (1 sentence).
- 담긴 정보: kinds of information inside (e.g. "매장별 회선 목록, 업체 연락처(이름), 설치 일정").
- 대상: stores, vendors, systems, projects it concerns (e.g. Bellevue, Granite, Cisco, POS).
- 공유: call get_file_permissions for every file (and each folder once; if a file has exactly its folder's permissions write "폴더와 같음"). Write who besides the owner has access: display name (or email if no name) + role (편집/댓글/보기). Link sharing: "링크 공개(보기)" etc. Domain-wide: "도메인 전체". Owner only: "비공개". Flag external (non-seoultradingusa.com) people with 🌐.
- 키워드: 2–5 from: network infra dev pos store-ops security phone software hardware general billing invoice purchase expense contract asset vendor-mgmt paperwork support outage install decision schedule tip meeting — plus free words if useful.
- 수정일 YYYY-MM-DD. 링크: web viewUrl with `?usp=...`/`&ouid=...` removed. Never G:\ paths.

SENSITIVE — NEVER COPY VALUES: passwords, accounts/usernames, API/license/Wi-Fi keys, IP addresses/subnets/firewall rules, network diagrams detail, prices/quotes/contract terms/invoice amounts, personal info (phone, address, SSN, salary, employee hours), POS/payment details, HR/legal matters. Instead write in 담긴 정보: "⚠민감: 비밀번호 포함" / "⚠민감: IP 대역" / "⚠민감: 금액" etc. Vendor contacts: name+title only.

Final reply (short): folders done, file count, files you could not read, list of ⚠민감 files. Do not paste the table.
