# AAWS_Eval (Agentic AI Web Scraper Evaluation Framework)

AAWS_Eval은 멀티 에이전트 기반 웹 크롤링 파이프라인의 성능을 평가하고 고도화하기 위해 구축된 독립적인 테스트 및 평가 프레임워크입니다. 
기존 교육용 프로젝트(`AAWS_project`)에서 파생되어, 데이터 수집 에이전트의 강건성(Robustness)을 확보하고 에이전트 간의 협업 로직을 최적화하는 데 목적이 있습니다.

이 프레임워크는 Navigator(웹 탐색 및 청사진 설계), Coder(스크립트 작성 및 실행), Supervisor(워크플로우 총괄) 등 다양한 에이전트들이 복잡한 웹 환경에서 어떻게 상호작용하는지 체계적으로 시나리오 기반 테스트를 수행하고 그 결과를 스스로 평가합니다.

## 📂 폴더 구조 (Directory Structure)

레포지토리는 에이전트의 핵심 로직과 워크플로우 실행 스크립트, 그리고 격리된 테스트 결과물(Artifacts)이 명확하게 분리되어 있습니다.

```text
AAWS_Eval/
 ├── src/                      # 코어 로직 및 에이전트 정의
 │    ├── agents/              # 에이전트 생성 모듈 (Navigator, Coder 등)
 │    ├── tools/               # 에이전트가 사용하는 도구 (웹 탐색, 파일 제어, 검색 등)
 │    ├── prompts/             # 에이전트별 페르소나 및 시스템 프롬프트
 │    ├── schemas.py           # Pydantic 기반의 통신 데이터 스키마
 │    ├── scenario_parser.py   # Markdown 시나리오 파일을 파싱하는 유틸리티
 │    └── evaluator.py         # 에이전트 실행 결과를 평가하는 LLM-as-a-Judge 로직
 │
 ├── workflows/                # 워크플로우 파이프라인 및 테스트 실행 스크립트
 │    ├── 01_sequential_workflow.py    # Navigator -> Coder 순차적 파이프라인 로직
 │    └── 02_supervisor_workflow.py    # Supervisor 중심의 동적 라우팅 파이프라인 로직
 │
 ├── tests/                    # 시나리오 자동화 테스트 러너 스크립트 모음
 │    ├── run_sequential_scenarios.py  # 순차 워크플로우 기반 테스트 실행기
 │    └── run_supervisor_scenarios.py  # Supervisor 워크플로우 기반 테스트 실행기
 │
 └── artifacts/                # 샌드박스 환경 결과물 및 생성된 파일 (자동 생성)
      ├── scenarios/           # 테스트 시나리오 마크다운 파일 (.md) 모음
      ├── code/                # Coder 에이전트가 제한된 환경에서 작성한 크롤링 스크립트 저장소
      └── results/[scenario_id]/       # 시나리오별 실행 평가 로그(_log.md)와 추출된 결과 데이터(_result.json)

 └── samples/                  # 참고용 샘플 코드
      └── nano_banana_image_gen.py  # Gemini 이미지 생성(Nano Banana) 예제
```

## 🚀 사용 방법 (Usage)

### 1. 환경 설정
프로젝트 실행을 위해 환경 변수(`.env` 또는 시스템 설정)에 필요한 API 키가 설정되어 있어야 합니다. (Google Gemini, OpenAI, Web Search Tool API 등)
루트 경로 인식은 `workflows` 폴더를 기준으로 자동으로 탐지되므로 복잡한 경로 설정 없이 바로 실행할 수 있습니다.

### 2. 테스트 시나리오 등록
`artifacts/scenarios/` 디렉토리 내에 Markdown 형식으로 테스트 시나리오 파일(예: `scenario_01.md`)을 작성합니다.
파일 상단의 `YAML Frontmatter`를 통해 난이도, 예상 스키마(Expected Schema), 평가 기준(Evaluation Criteria)을 정의합니다.

### 3. 워크플로우 테스트 실행
터미널을 열고 `AAWS_Eval` 프로젝트 루트 경로에서 원하는 워크플로우의 실행 스크립트를 가동합니다.

**순차적 파이프라인 (Sequential) 테스트:**
Navigator가 청사진을 모두 만들고 난 뒤 Coder에게 일괄로 넘기는 단방향 워크플로우를 평가합니다.
```bash
python -m tests.run_sequential_scenarios
```

**슈퍼바이저 파이프라인 (Supervisor) 테스트:**
매니저 역할을 하는 Supervisor가 상황에 따라 능동적으로 Navigator와 Coder를 호출하고 피드백을 주고받는 대화형 워크플로우를 평가합니다.
```bash
python -m tests.run_supervisor_scenarios
```

### 4. 실행 및 평가 결과 분석
실행이 완료되면 자동으로 `evaluator.py`를 통해 "LLM-as-a-Judge" 기반 평가가 이루어지며,
`artifacts/[scenario_id]/` 폴더에 다음과 같은 결과물이 저장됩니다.
- `*_result.json`: 에이전트가 실행하여 수집한 실제 크롤링 결과 데이터
- `*_log.md`: 시나리오 평가 결과 (성공 여부, Schema Score, Strategy Score) 및 문제점, 개선 피드백 로그
- `artifacts/code/`: 에이전트가 실제 작성하고 디버깅하며 실행했던 `.py` 크롤링 코드 원문

### 5. 🍌 Nano Banana — AI 이미지 생성 샘플 실행

`samples/nano_banana_image_gen.py`는 Gemini의 이미지 생성 기능(일명 Nano Banana)을 사용하는 참고 코드입니다. Analyst 에이전트의 인포그래픽 생성 도구를 구현할 때 참고하세요.

**사전 설치:**
```bash
pip install google-genai pillow python-dotenv
```

**환경 변수 설정 (`.env`):**
```
GEMINI_API_KEY=your-api-key-here
```

**실행:**
```bash
# 프로젝트 루트에서 실행
python samples/nano_banana_image_gen.py
```

실행하면 텍스트 프롬프트로부터 이미지를 생성(`sample_generated.png`)하고, 이어서 해당 이미지를 편집(`sample_edited.png`)하는 두 가지 기능을 시연합니다.

**코드 내 주요 함수:**
| 함수 | 기능 | 사용 예시 |
|:---|:---|:---|
| `generate_image(prompt, output_path)` | 텍스트 → 이미지 생성 | 분석 결과를 인포그래픽으로 변환 |
| `edit_image_with_prompt(image_path, edit_prompt, output_path)` | 기존 이미지 편집 | 차트에 스타일 적용, 배경 변경 등 |
