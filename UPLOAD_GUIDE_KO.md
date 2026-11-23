# HW2: Codespaces에 구현 파일 반영하기

## 1. 기존 저장소 보존
- GitHub 저장소 `minkyo031/algorithms-hw2`는 과제 시작 템플릿을 사용한 것으로 보임.
- **기존 `.devcontainer/`, `.vscode/`, `tools/`, `Dockerfile`, `compose.yml`은 유지**하세요.
- 이 ZIP은 독립 프로젝트입니다. ZIP의 `src/`, `tests/`, `experiments/`, `.github/copilot-instructions.md`, `PLAN.md`를 템플릿에 복사하되, 기존 `SPEC.md`·`README.md`·`Makefile`은 내용을 비교한 후 병합하세요.
- 보고서 `REPORT_DRAFT.pdf`는 참고용입니다. 수업 지시에 따라 본인의 실제 확인 기록과 회고를 직접 작성하세요.

## 2. 파일 옮기는 가장 쉬운 방법
1. ZIP을 PC에서 압축 해제합니다.
2. Codespaces 왼쪽 파일 탐색기에서 `work` 아래 기존 저장소가 열려 있는지 확인합니다.
3. 파일 탐색기에 폴더/파일을 드래그해서 업로드합니다. 업로드가 막히면 탐색기 빈 공간 오른쪽 클릭 메뉴의 Upload를 사용합니다.
4. 동일 이름 파일을 덮어쓸 때는 원본을 먼저 확인하고 필요한 수정 내용을 백업하세요.

## 3. 테스트와 실험
Codespaces 터미널에서 저장소 최상위 경로로 이동한 후:

```bash
make test
make experiment
make serve
```

`make serve` 뒤 포트 탭의 8000 포워딩 주소를 브라우저에서 확인합니다. `/table` 화면에서 두 테이블을 모두 확인하세요. 휴대폰 확인용으로 Public을 잠깐 켰다면 테스트 후 서버를 `Ctrl+C`로 종료하고 포트를 Private으로 되돌립니다.

## 4. GitHub 업로드 (실제 본인이 수행한 변경사항만 기록)
```bash
git status
# 개발 브랜치가 없다면 생성
git switch -c develop
# 파일을 직접 검토하고 테스트한 후
git add -A
git commit -m "Implement and test URL shortener and hash table comparison"
git push -u origin develop
```

이미 `develop`이 있다면 `git switch develop`을 사용하세요. 이후 GitHub에서 실제 작업 내용을 리뷰한 뒤 PR로 `main`에 합치거나 `git switch main && git merge develop && git push origin main`을 진행하세요. 최초 커밋부터 단계별 Copilot 수행 기록이 있었다고 주장하지 마세요.

## 5. 실제로 추가 작업이 필요한 항목
- GitHub Issues 8개 만들기, 수행한 내용과 테스트 검증을 정확히 기록하기
- 수업에서 요구한 Copilot 에이전트 사용 기록 (Copilot 장애로 수행하지 못했다면 그대로 명시)
- SPEC.md 본인 검토·편집, 규칙 파일 최종 선택
- Codespaces에서 휴대폰으로 실제 링크 확인하기
- PDF 2쪽 이내: GitHub 저장소 URL, 실험 결과, 본인 해석, **실제로 발생한 오류와 수정 과정** 직접 작성하기
- 제출 전 `main` 브랜치의 파일과 최종 URL 확인하기

과제 원문: https://lec-algorithm.github.io/lecture/slides/hw2-2026/
