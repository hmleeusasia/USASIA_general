# USASIA_general 핸드북
이 저장소를 처음 보는 개발자용입니다. 영어 원본: [README.md](README.md).

| # | 문서 | 읽고 나면 |
|---|---|---|
| 1 | [../ARCHITECTURE.ko.md](../ARCHITECTURE.ko.md) | 저장소가 무엇인지, 원칙, Claude·hook·skill·Drive가 어떻게 맞물리는지(개요). 영어 원본은 ARCHITECTURE.md |
| 2 | [code-map.ko.md](code-map.ko.md) | 모든 Python 도구와 hook, 각 함수와 그것을 부르는 곳, hook 규칙 모드, 각 skill과 그것이 쓰는 것, 각 규칙 ID와 그것을 지키는 곳 |
| 3 | usasia_db 저장소 docs/handbook/ | DB 앱(데이터 사전, 요청 흐름) |

## 문서가 정확하게 유지되는 방법
- `code-map.md`와 `code-map.ko.md`는 `tools/handbook.py`가 코드에서 **자동으로 만듭니다**. 손으로 고치지 마세요.
- 모듈, 함수, skill의 의미(영어와 한국어)는 `docs/handbook/meta.json`에 있습니다. 영어는 docstring이 있으면 그것을 씁니다.
- git pre-commit hook(`tools/githooks/pre-commit`)이 tools/, .claude/skills/, docs/rules/, docs/handbook/를 건드리는 커밋마다 `tools/handbook.py --check`를 실행합니다. 문서가 오래됐거나, 의미가 빠졌거나, 이메일·IP 주소가 들어 있으면 커밋이 실패합니다.
- 코드를 바꾼 뒤: `py tools/handbook.py`를 실행하고 보고된 빈칸을 채워 stage한 다음 커밋합니다.

생성기가 읽지 않는 것(개인용이거나 PC마다 다름): docs/users/**, CLAUDE.local.md, .claude/settings*.json.
